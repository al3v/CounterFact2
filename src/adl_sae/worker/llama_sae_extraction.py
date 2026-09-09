from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Optional

import pandas as pd
import torch
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from tqdm import tqdm

from adl_sae.config import ExperimentConfig


class LlamaScopeSAEExtractionWorker:
    def __init__(
        self,
        config: ExperimentConfig,
        max_rows: Optional[int] = None,
    ) -> None:
        self.config = config
        self.max_rows = max_rows

    @property
    def hidden_states_path(self) -> Path:
        return Path(self.config.hidden_states_path)

    @property
    def active_features_path(self) -> Path:
        return Path(self.config.sae_active_features_path)

    @property
    def prompt_summary_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"sae_prompt_summary_{self.config.experiment_name}.csv"
        )

    @property
    def global_feature_summary_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"sae_global_feature_summary_{self.config.experiment_name}.csv"
        )

    def layer_folder(self, layer: int) -> str:
        return f"Llama3_1-8B-Base-L{layer}R-8x"

    def load_hidden_states(self):
        if not self.hidden_states_path.exists():
            raise FileNotFoundError(f"Hidden states not found: {self.hidden_states_path}")

        obj = torch.load(self.hidden_states_path, map_location="cpu")

        if "hidden_states" in obj:
            hidden_states = obj["hidden_states"]
        elif "activations" in obj:
            hidden_states = obj["activations"]
        else:
            raise KeyError("Expected key 'hidden_states' or 'activations'.")

        if not isinstance(hidden_states, torch.Tensor):
            hidden_states = torch.tensor(hidden_states)

        if "row_metadata" in obj:
            metadata = pd.DataFrame(obj["row_metadata"])
        else:
            metadata_path = Path(self.config.hidden_states_metadata_path)
            if not metadata_path.exists():
                raise FileNotFoundError(f"Metadata CSV not found: {metadata_path}")
            metadata = pd.read_csv(metadata_path)

            if "layer" in metadata.columns:
                metadata = metadata.drop_duplicates(subset=["row_id"]).reset_index(drop=True)

        layers = [int(x) for x in obj.get("layers", list(self.config.layers))]

        if self.max_rows is not None:
            hidden_states = hidden_states[: self.max_rows]
            metadata = metadata.head(self.max_rows).copy()

        metadata = metadata.reset_index(drop=True)

        return hidden_states.cpu().float(), metadata, layers

    def load_sae_for_layer(self, layer: int):
        folder = self.layer_folder(layer)

        hyper_path = hf_hub_download(
            repo_id=self.config.sae_release,
            filename=f"{folder}/hyperparams.json",
        )

        ckpt_path = hf_hub_download(
            repo_id=self.config.sae_release,
            filename=f"{folder}/checkpoints/final.safetensors",
        )

        with open(hyper_path) as f:
            hyperparams = json.load(f)

        tensors = load_file(ckpt_path)

        required = {
            "encoder.weight",
            "encoder.bias",
            "decoder.weight",
            "decoder.bias",
        }
        missing = required - set(tensors.keys())
        if missing:
            raise KeyError(f"SAE checkpoint missing keys: {sorted(missing)}")

        W_enc = tensors["encoder.weight"].float()
        b_enc = tensors["encoder.bias"].float()
        W_dec = tensors["decoder.weight"].float()

        # decoder.weight has shape d_model x d_sae.
        # Each SAE feature corresponds to one decoder column.
        decoder_norms = W_dec.norm(dim=0)

        threshold = float(hyperparams.get("jump_relu_threshold", 0.0))

        return W_enc, b_enc, decoder_norms, threshold, hyperparams, ckpt_path

    def activation_normalization_scale(self, hyperparams: dict) -> tuple[float, float]:
        """
        Llama-Scope uses norm_activation='dataset-wise'.

        The cached hyperparams store the dataset average activation norm.
        During SAE encoding, hidden states are rescaled to average norm sqrt(d_model).
        """
        norm_mode = hyperparams.get("norm_activation")

        if norm_mode != "dataset-wise":
            return 1.0, float("nan")

        avg_norm = hyperparams.get("dataset_average_activation_norm", {}).get("in")
        if avg_norm is None:
            raise ValueError(
                "Llama-Scope hyperparams use dataset-wise normalization, "
                "but dataset_average_activation_norm['in'] is missing."
            )

        avg_norm = float(avg_norm)
        if avg_norm <= 0:
            raise ValueError(f"Invalid dataset average activation norm: {avg_norm}")

        d_model = int(hyperparams.get("d_model", 0))
        if d_model <= 0:
            raise ValueError(f"Invalid d_model in hyperparams: {d_model}")

        scale = math.sqrt(d_model) / avg_norm
        return scale, avg_norm

    def safe_meta(self, meta: dict, key: str, default=""):
        value = meta.get(key, default)
        if pd.isna(value):
            return default
        return value

    def run(self):
        hidden_states, metadata, layers = self.load_hidden_states()

        if len(metadata) != hidden_states.shape[0]:
            raise ValueError(
                f"Metadata rows ({len(metadata)}) do not match hidden states "
                f"({hidden_states.shape[0]})."
            )

        print("=== Llama-Scope SAE extraction ===")
        print("Experiment:", self.config.experiment_name)
        print("Model:", self.config.model_name)
        print("SAE release:", self.config.sae_release)
        print("Hidden states:", self.hidden_states_path)
        print("Hidden shape:", tuple(hidden_states.shape))
        print("Layers:", layers)

        active_rows = []
        prompt_summary_rows = []

        for layer_pos, layer in enumerate(layers):
            print()
            print(f"Loading Llama-Scope SAE for layer {layer}...")

            W_enc, b_enc, decoder_norms, threshold, hyperparams, ckpt_path = self.load_sae_for_layer(layer)

            norm_scale, dataset_avg_norm_in = self.activation_normalization_scale(hyperparams)
            decoder_norm_scaling_applied = bool(hyperparams.get("sparsity_include_decoder_norm", False))

            print("SAE file:", ckpt_path)
            print("W_enc shape:", tuple(W_enc.shape))
            print("b_enc shape:", tuple(b_enc.shape))
            print("decoder_norms shape:", tuple(decoder_norms.shape))
            print("JumpReLU threshold:", threshold)
            print("act_fn:", hyperparams.get("act_fn"))
            print("norm_activation:", hyperparams.get("norm_activation"))
            print("dataset_average_activation_norm_in:", dataset_avg_norm_in)
            print("activation_normalization_scale:", norm_scale)
            print("sparsity_include_decoder_norm:", decoder_norm_scaling_applied)

            layer_hidden = hidden_states[:, layer_pos, :]

            if layer_hidden.shape[-1] != W_enc.shape[-1]:
                raise ValueError(
                    f"Hidden dim mismatch for layer {layer}: "
                    f"hidden dim {layer_hidden.shape[-1]} vs W_enc dim {W_enc.shape[-1]}"
                )

            # Dataset-wise activation normalization.
            layer_hidden_for_sae = layer_hidden * norm_scale

            pre_acts = layer_hidden_for_sae @ W_enc.T + b_enc

            decoder_norms = decoder_norms.to(device=pre_acts.device, dtype=pre_acts.dtype)
            threshold_tensor = torch.as_tensor(threshold, device=pre_acts.device, dtype=pre_acts.dtype)

            if decoder_norm_scaling_applied:
                gated_pre = pre_acts * decoder_norms.unsqueeze(0)
            else:
                gated_pre = pre_acts

            raw_feature_acts = torch.relu(gated_pre) * (gated_pre > threshold_tensor)

            if decoder_norm_scaling_applied:
                feature_acts = raw_feature_acts / decoder_norms.unsqueeze(0)
            else:
                feature_acts = raw_feature_acts

            for row_i in tqdm(range(feature_acts.shape[0]), desc=f"Layer {layer}"):
                meta = metadata.iloc[row_i].to_dict()

                row_id = self.safe_meta(meta, "row_id", row_i)
                fact_id = self.safe_meta(meta, "fact_id", "")
                variant_id = self.safe_meta(meta, "variant_id", "")
                pair_type = self.safe_meta(meta, "pair_type", "")
                is_correct = self.safe_meta(meta, "is_correct", "")

                vals = feature_acts[row_i]
                raw_vals = raw_feature_acts[row_i]

                active_idx = torch.nonzero(vals > 0, as_tuple=False).flatten()
                active_vals = vals[active_idx]
                active_raw_vals = raw_vals[active_idx]
                active_decoder_norms = decoder_norms[active_idx]

                n_active = int(active_idx.numel())

                prompt_summary_rows.append(
                    {
                        "row_id": row_id,
                        "layer": layer,
                        "n_active_features": n_active,

                        "sum_activation": float(active_vals.sum().item()) if n_active else 0.0,
                        "max_activation": float(active_vals.max().item()) if n_active else 0.0,
                        "mean_activation": float(active_vals.mean().item()) if n_active else 0.0,

                        "sum_raw_activation": float(active_raw_vals.sum().item()) if n_active else 0.0,
                        "max_raw_activation": float(active_raw_vals.max().item()) if n_active else 0.0,
                        "mean_raw_activation": float(active_raw_vals.mean().item()) if n_active else 0.0,

                        "dataset_average_activation_norm_in": dataset_avg_norm_in,
                        "activation_normalization_scale": norm_scale,
                        "decoder_norm_scaling_applied": decoder_norm_scaling_applied,
                        "fact_id": fact_id,
                        "variant_id": variant_id,
                        "pair_type": pair_type,
                        "is_correct": is_correct,
                    }
                )

                for feature_id, activation, raw_activation, decoder_norm in zip(
                    active_idx.tolist(),
                    active_vals.tolist(),
                    active_raw_vals.tolist(),
                    active_decoder_norms.tolist(),
                ):
                    active_rows.append(
                        {
                            "row_id": row_id,
                            "layer": layer,
                            "feature_id": int(feature_id),

                            # Main activation used by downstream analyses.
                            "activation": float(activation),

                            # Raw SAE activation before decoder norm scaling.
                            "raw_activation": float(raw_activation),
                            "decoder_norm": float(decoder_norm),

                            "dataset_average_activation_norm_in": dataset_avg_norm_in,
                            "activation_normalization_scale": norm_scale,
                            "decoder_norm_scaling_applied": decoder_norm_scaling_applied,
                            "fact_id": fact_id,
                            "variant_id": variant_id,
                            "pair_type": pair_type,
                            "is_correct": is_correct,
                        }
                    )

            del pre_acts
            del gated_pre
            del raw_feature_acts
            del feature_acts

        active_df = pd.DataFrame(active_rows)
        prompt_summary_df = pd.DataFrame(prompt_summary_rows)

        if active_df.empty:
            global_feature_summary = pd.DataFrame()
        else:
            global_feature_summary = (
                active_df.groupby(["layer", "feature_id"])
                .agg(
                    active_count=("activation", "count"),
                    total_activation=("activation", "sum"),
                    mean_activation_when_active=("activation", "mean"),
                    max_activation=("activation", "max"),
                    total_raw_activation=("raw_activation", "sum"),
                    mean_raw_activation_when_active=("raw_activation", "mean"),
                    max_raw_activation=("raw_activation", "max"),
                    decoder_norm=("decoder_norm", "first"),
                    dataset_average_activation_norm_in=(
                        "dataset_average_activation_norm_in",
                        "first",
                    ),
                    activation_normalization_scale=(
                        "activation_normalization_scale",
                        "first",
                    ),
                    decoder_norm_scaling_applied=(
                        "decoder_norm_scaling_applied",
                        "first",
                    ),
                )
                .reset_index()
            )

        self.active_features_path.parent.mkdir(parents=True, exist_ok=True)
        self.prompt_summary_path.parent.mkdir(parents=True, exist_ok=True)
        self.global_feature_summary_path.parent.mkdir(parents=True, exist_ok=True)

        active_df.to_csv(self.active_features_path, index=False)
        prompt_summary_df.to_csv(self.prompt_summary_path, index=False)
        global_feature_summary.to_csv(self.global_feature_summary_path, index=False)

        print()
        print("Saved active features:", self.active_features_path)
        print("Saved prompt summary:", self.prompt_summary_path)
        print("Saved global feature summary:", self.global_feature_summary_path)
        print("Active feature rows:", len(active_df))
        print("Prompt summary rows:", len(prompt_summary_df))

        return self.active_features_path
