from __future__ import annotations

from pathlib import Path

import pandas as pd
import torch
from huggingface_hub import hf_hub_download
from tqdm import tqdm

from adl_sae.config import ExperimentConfig


class QwenScopeSAEExtractionWorker:
    def __init__(self, config: ExperimentConfig, top_k: int = 100) -> None:
        self.config = config
        self.top_k = top_k

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

    def load_hidden_states(self):
        if not self.hidden_states_path.exists():
            raise FileNotFoundError(f"Hidden states not found: {self.hidden_states_path}")

        obj = torch.load(self.hidden_states_path, map_location="cpu")

        if "hidden_states" in obj:
            hidden_states = obj["hidden_states"]
        elif "activations" in obj:
            hidden_states = obj["activations"]
        else:
            raise KeyError("Expected key 'hidden_states' or 'activations' in hidden-state file.")

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
        filename = f"layer{layer}.sae.pt"

        local_path = hf_hub_download(
            repo_id=self.config.sae_release,
            filename=filename,
        )

        sae = torch.load(local_path, map_location="cpu")

        required = {"W_enc", "b_enc"}
        missing = required - set(sae.keys())
        if missing:
            raise KeyError(f"SAE checkpoint {filename} missing keys: {sorted(missing)}")

        W_enc = sae["W_enc"].float()
        b_enc = sae["b_enc"].float()

        return W_enc, b_enc, local_path

    def run(self):
        hidden_states, metadata, layers = self.load_hidden_states()

        if len(metadata) != hidden_states.shape[0]:
            raise ValueError(
                f"Metadata rows ({len(metadata)}) do not match hidden states "
                f"({hidden_states.shape[0]})."
            )

        print("=== Qwen-Scope SAE extraction ===")
        print("Experiment:", self.config.experiment_name)
        print("Model:", self.config.model_name)
        print("SAE release:", self.config.sae_release)
        print("Hidden states:", self.hidden_states_path)
        print("Hidden shape:", tuple(hidden_states.shape))
        print("Layers:", layers)
        print("Top-K:", self.top_k)

        active_rows = []
        prompt_summary_rows = []

        for layer_pos, layer in enumerate(layers):
            print()
            print(f"Loading Qwen-Scope SAE for layer {layer}...")
            W_enc, b_enc, local_path = self.load_sae_for_layer(layer)
            print("SAE file:", local_path)
            print("W_enc shape:", tuple(W_enc.shape))
            print("b_enc shape:", tuple(b_enc.shape))

            layer_hidden = hidden_states[:, layer_pos, :]

            if layer_hidden.shape[-1] != W_enc.shape[-1]:
                raise ValueError(
                    f"Hidden dim mismatch for layer {layer}: "
                    f"hidden dim {layer_hidden.shape[-1]} vs W_enc dim {W_enc.shape[-1]}"
                )

            pre_acts = layer_hidden @ W_enc.T + b_enc
            top_vals, top_idx = torch.topk(pre_acts, k=self.top_k, dim=-1)

            for row_i in tqdm(range(top_vals.shape[0]), desc=f"Layer {layer}"):
                meta = metadata.iloc[row_i].to_dict()

                row_id = meta.get("row_id", row_i)
                fact_id = meta.get("fact_id", "")
                variant_id = meta.get("variant_id", "")
                pair_type = meta.get("pair_type", "")
                is_correct = meta.get("is_correct", "")

                vals = top_vals[row_i]
                idxs = top_idx[row_i]

                prompt_summary_rows.append(
                    {
                        "row_id": row_id,
                        "layer": layer,
                        "n_active_features": int(self.top_k),
                        "sum_activation": float(vals.sum().item()),
                        "max_activation": float(vals.max().item()),
                        "mean_activation": float(vals.mean().item()),
                        "fact_id": fact_id,
                        "variant_id": variant_id,
                        "pair_type": pair_type,
                        "is_correct": is_correct,
                    }
                )

                for feature_id, activation in zip(idxs.tolist(), vals.tolist()):
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
