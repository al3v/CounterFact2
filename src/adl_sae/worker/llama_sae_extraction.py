from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import torch
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from tqdm import tqdm

from adl_sae.config import ExperimentConfig


class LlamaScopeSAEExtractionWorker:
    def __init__(self, config: ExperimentConfig) -> None:
        self.config = config

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

        layers = obj.get("layers", list(self.config.layers))

        return hidden_states.cpu().float(), metadata, list(layers)

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

        threshold = float(hyperparams.get("jump_relu_threshold", 0.0))

        return W_enc, b_enc, threshold, hyperparams, ckpt_path

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
            W_enc, b_enc, threshold, hyperparams, ckpt_path = self.load_sae_for_layer(layer)

            print("SAE file:", ckpt_path)
            print("W_enc shape:", tuple(W_enc.shape))
            print("b_enc shape:", tuple(b_enc.shape))
            print("JumpReLU threshold:", threshold)
            print("act_fn:", hyperparams.get("act_fn"))

            layer_hidden = hidden_states[:, layer_pos, :]

            if layer_hidden.shape[-1] != W_enc.shape[-1]:
                raise ValueError(
                    f"Hidden dim mismatch for layer {layer}: "
                    f"hidden dim {layer_hidden.shape[-1]} vs W_enc dim {W_enc.shape[-1]}"
                )

            pre_acts = layer_hidden @ W_enc.T + b_enc

            # Llama-Scope hyperparams say act_fn = jumprelu.
            # So we keep features whose pre-activation is above the learned threshold.
            feature_acts = torch.relu(pre_acts) * (pre_acts > threshold)

            for row_i in tqdm(range(feature_acts.shape[0]), desc=f"Layer {layer}"):
                meta = metadata.iloc[row_i].to_dict()

                row_id = meta.get("row_id", row_i)
                fact_id = meta.get("fact_id", "")
                variant_id = meta.get("variant_id", "")
                pair_type = meta.get("pair_type", "")
                is_correct = meta.get("is_correct", "")

                vals = feature_acts[row_i]
                active_idx = torch.nonzero(vals > 0, as_tuple=False).flatten()
                active_vals = vals[active_idx]

                n_active = int(active_idx.numel())

                prompt_summary_rows.append(
                    {
                        "row_id": row_id,
                        "layer": layer,
                        "n_active_features": n_active,
                        "sum_activation": float(active_vals.sum().item()) if n_active else 0.0,
                        "max_activation": float(active_vals.max().item()) if n_active else 0.0,
                        "mean_activation": float(active_vals.mean().item()) if n_active else 0.0,
                        "fact_id": fact_id,
                        "variant_id": variant_id,
                        "pair_type": pair_type,
                        "is_correct": is_correct,
                    }
                )

                for feature_id, activation in zip(active_idx.tolist(), active_vals.tolist()):
                    active_rows.append(
                        {
                            "row_id": row_id,
                            "layer": layer,
                            "feature_id": int(feature_id),
                            "activation": float(activation),
                            "fact_id": fact_id,
                            "variant_id": variant_id,
                            "pair_type": pair_type,
                            "is_correct": is_correct,
                        }
                    )

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
                )
                .reset_index()
            )

        self.active_features_path.parent.mkdir(parents=True, exist_ok=True)
        self.prompt_summary_path.parent.mkdir(parents=True, exist_ok=True)

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
