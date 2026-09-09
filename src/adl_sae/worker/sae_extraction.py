from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
import torch
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from tqdm import tqdm

from adl_sae.config import ExperimentConfig


def safe_torch_load(path: Path):
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


def encode_jumprelu(x: torch.Tensor, sae: dict) -> torch.Tensor:
    """
    Manual Gemma Scope JumpReLU SAE encoder.

    feature_acts = ReLU(x @ w_enc + b_enc) if pre_act > threshold else 0
    """
    pre_acts = x @ sae["w_enc"] + sae["b_enc"]
    return torch.relu(pre_acts) * (pre_acts > sae["threshold"])


@dataclass
class SAEExtractionWorker:
    """
    Gemma-Scope SAE feature extraction worker.

    This worker no longer executes the legacy script through command-line globals.
    It explicitly uses paths and settings from ExperimentConfig:
    - hidden states: config.hidden_states_path
    - active feature output: config.sae_active_features_path
    - SAE repo: config.sae_release
    - layers: config.layers
    """

    config: ExperimentConfig
    sae_folder_template: str = "resid_post_all/layer_{layer}_width_16k_l0_small"
    batch_size: int = 64
    max_rows: Optional[int] = None
    output_suffix: Optional[str] = None
    device: str = "cuda"

    def with_output_suffix(self, path) -> Path:
        path = Path(path)

        if self.output_suffix is None:
            return path

        return path.with_name(f"{path.stem}_{self.output_suffix}{path.suffix}")

    @property
    def hidden_states_path(self) -> Path:
        return self.with_output_suffix(self.config.hidden_states_path)

    @property
    def active_features_path(self) -> Path:
        return self.with_output_suffix(self.config.sae_active_features_path)

    @property
    def prompt_summary_path(self) -> Path:
        path = (
            Path(self.config.reports_dir)
            / f"sae_prompt_summary_{self.config.experiment_name}.csv"
        )
        return self.with_output_suffix(path)

    @property
    def global_feature_summary_path(self) -> Path:
        path = (
            Path(self.config.reports_dir)
            / f"sae_global_feature_summary_{self.config.experiment_name}.csv"
        )
        return self.with_output_suffix(path)

    def resolve_device(self) -> str:
        if self.device == "cuda" and not torch.cuda.is_available():
            return "cpu"
        return self.device

    def load_hidden_states(self):
        if not self.hidden_states_path.exists():
            raise FileNotFoundError(f"Hidden states file not found: {self.hidden_states_path}")

        obj = safe_torch_load(self.hidden_states_path)

        if "hidden_states" in obj:
            hidden_states = obj["hidden_states"]
        elif "activations" in obj:
            hidden_states = obj["activations"]
        else:
            raise KeyError("Expected key 'hidden_states' or 'activations' in hidden-state file.")

        if not isinstance(hidden_states, torch.Tensor):
            hidden_states = torch.tensor(hidden_states)

        saved_layers = [int(x) for x in obj.get("layers", list(self.config.layers))]

        if "row_metadata" in obj:
            metadata = pd.DataFrame(obj["row_metadata"])
        else:
            metadata_path = Path(self.config.hidden_states_metadata_path)
            if not metadata_path.exists():
                raise FileNotFoundError(f"Metadata CSV not found: {metadata_path}")

            metadata = pd.read_csv(metadata_path)
            if "layer" in metadata.columns:
                metadata = metadata.drop_duplicates(subset=["row_id"]).reset_index(drop=True)

        if self.max_rows is not None:
            hidden_states = hidden_states[: self.max_rows]
            metadata = metadata.head(self.max_rows).copy()

        metadata = metadata.reset_index(drop=True)

        if len(metadata) != hidden_states.shape[0]:
            raise ValueError(
                f"Metadata rows ({len(metadata)}) do not match hidden states "
                f"({hidden_states.shape[0]})."
            )

        return hidden_states.cpu().float(), metadata, saved_layers

    def load_sae_for_layer(self, layer: int, device: str):
        folder = self.sae_folder_template.format(layer=layer)

        config_path = hf_hub_download(
            repo_id=self.config.sae_release,
            filename=f"{folder}/config.json",
        )
        params_path = hf_hub_download(
            repo_id=self.config.sae_release,
            filename=f"{folder}/params.safetensors",
        )

        with open(config_path, "r") as f:
            cfg = json.load(f)

        state = load_file(params_path)

        required = {"w_enc", "b_enc", "b_dec", "threshold"}
        missing = required - set(state.keys())
        if missing:
            raise KeyError(
                f"Gemma-Scope SAE layer {layer} missing keys: {sorted(missing)}"
            )

        sae = {
            "cfg": cfg,
            "folder": folder,
            "config_path": config_path,
            "params_path": params_path,
            "w_enc": state["w_enc"].to(device=device, dtype=torch.float32),
            "b_enc": state["b_enc"].to(device=device, dtype=torch.float32),
            "b_dec": state["b_dec"].to(device=device, dtype=torch.float32),
            "threshold": state["threshold"].to(device=device, dtype=torch.float32),
        }

        return sae

    def get_metadata_value(self, meta: pd.Series, key: str, default=""):
        value = meta.get(key, default)
        if pd.isna(value):
            return default
        return value

    def validate_requested_layers(self, requested_layers, saved_layers):
        missing = [layer for layer in requested_layers if layer not in saved_layers]
        if missing:
            raise ValueError(
                "Requested SAE layers are missing from the hidden-state file. "
                f"Missing: {missing}. Saved hidden-state layers: {saved_layers}."
            )

    def run(self, dry_run: bool = False):
        hidden_states, metadata, saved_layers = self.load_hidden_states()
        requested_layers = [int(layer) for layer in self.config.layers]
        self.validate_requested_layers(requested_layers, saved_layers)

        device = self.resolve_device()

        print("=== Gemma-Scope SAE extraction ===")
        print("Experiment:", self.config.experiment_name)
        print("Model:", self.config.model_name)
        print("SAE release:", self.config.sae_release)
        print("Hidden states:", self.hidden_states_path)
        print("Active output:", self.active_features_path)
        print("Prompt summary output:", self.prompt_summary_path)
        print("Feature summary output:", self.global_feature_summary_path)
        print("Hidden shape:", tuple(hidden_states.shape))
        print("Saved hidden-state layers:", saved_layers)
        print("Requested SAE layers:", requested_layers)
        print("Rows:", len(metadata))
        print("Device:", device)

        if dry_run:
            print("Dry run only. Did not execute SAE extraction.")
            return self.active_features_path

        self.active_features_path.parent.mkdir(parents=True, exist_ok=True)
        self.prompt_summary_path.parent.mkdir(parents=True, exist_ok=True)
        self.global_feature_summary_path.parent.mkdir(parents=True, exist_ok=True)

        active_fieldnames = [
            "row_id",
            "fact_id",
            "variant_id",
            "layer",
            "pair_type",
            "is_correct",
            "subject",
            "correct_answer",
            "target_new",
            "feature_id",
            "activation",
        ]

        prompt_summary_rows = []
        global_summary_rows = []

        with open(self.active_features_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=active_fieldnames)
            writer.writeheader()

            for layer in requested_layers:
                layer_index = saved_layers.index(layer)

                print()
                print("=" * 80)
                print(f"Loading Gemma-Scope SAE for layer {layer}")

                sae = self.load_sae_for_layer(layer=layer, device=device)
                cfg = sae["cfg"]
                d_sae = int(cfg["width"])

                print("Folder:", sae["folder"])
                print("Hook in:", cfg.get("hf_hook_point_in"))
                print("Architecture:", cfg.get("architecture"))
                print("Width:", d_sae)
                print("L0:", cfg.get("l0"))
                print("SAE params:", sae["params_path"])

                if d_sae != int(self.config.sae_width):
                    raise ValueError(
                        f"SAE width mismatch for layer {layer}: "
                        f"config width {self.config.sae_width}, checkpoint width {d_sae}"
                    )

                layer_acts = hidden_states[:, layer_index, :]

                if layer_acts.shape[-1] != sae["w_enc"].shape[0]:
                    raise ValueError(
                        f"Hidden dim mismatch for layer {layer}: "
                        f"hidden dim {layer_acts.shape[-1]} vs w_enc dim {sae['w_enc'].shape[0]}"
                    )

                feature_counts = torch.zeros(d_sae, dtype=torch.long)
                feature_sums = torch.zeros(d_sae, dtype=torch.float64)
                feature_max = torch.zeros(d_sae, dtype=torch.float32)

                for start in tqdm(range(0, len(metadata), self.batch_size), desc=f"Layer {layer}"):
                    end = min(start + self.batch_size, len(metadata))
                    x = layer_acts[start:end].to(device=device, dtype=torch.float32)

                    with torch.no_grad():
                        feat = encode_jumprelu(x, sae)

                    active_mask = feat != 0
                    n_active = active_mask.sum(dim=1).detach().cpu()
                    sum_active = feat.sum(dim=1).detach().cpu()
                    max_active = feat.max(dim=1).values.detach().cpu()

                    active_indices = active_mask.nonzero(as_tuple=False)

                    if active_indices.numel() > 0:
                        active_values = feat[active_indices[:, 0], active_indices[:, 1]].detach()
                        feature_ids_gpu = active_indices[:, 1]

                        batch_counts = torch.bincount(
                            feature_ids_gpu.detach().cpu(),
                            minlength=d_sae,
                        )
                        batch_sums = torch.bincount(
                            feature_ids_gpu.detach().cpu(),
                            weights=active_values.detach().cpu().double(),
                            minlength=d_sae,
                        )

                        feature_counts += batch_counts
                        feature_sums += batch_sums

                        active_indices_cpu = active_indices.detach().cpu()
                        active_values_cpu = active_values.detach().cpu().float()

                        for fid, val in zip(
                            active_indices_cpu[:, 1].tolist(),
                            active_values_cpu.tolist(),
                        ):
                            if val > feature_max[fid]:
                                feature_max[fid] = val

                        for idx, value in zip(
                            active_indices_cpu.tolist(),
                            active_values_cpu.tolist(),
                        ):
                            local_row_idx, feature_id = idx
                            global_row_idx = start + local_row_idx
                            meta = metadata.iloc[global_row_idx]

                            writer.writerow(
                                {
                                    "row_id": int(self.get_metadata_value(meta, "row_id", global_row_idx)),
                                    "fact_id": self.get_metadata_value(meta, "fact_id"),
                                    "variant_id": self.get_metadata_value(meta, "variant_id"),
                                    "layer": layer,
                                    "pair_type": self.get_metadata_value(meta, "pair_type"),
                                    "is_correct": self.get_metadata_value(meta, "is_correct"),
                                    "subject": self.get_metadata_value(meta, "subject"),
                                    "correct_answer": self.get_metadata_value(meta, "correct_answer"),
                                    "target_new": self.get_metadata_value(meta, "target_new"),
                                    "feature_id": int(feature_id),
                                    "activation": float(value),
                                }
                            )

                    for i in range(end - start):
                        meta = metadata.iloc[start + i]
                        na = int(n_active[i])
                        sa = float(sum_active[i])
                        ma = float(max_active[i])

                        prompt_summary_rows.append(
                            {
                                "row_id": int(self.get_metadata_value(meta, "row_id", start + i)),
                                "fact_id": self.get_metadata_value(meta, "fact_id"),
                                "variant_id": self.get_metadata_value(meta, "variant_id"),
                                "layer": layer,
                                "pair_type": self.get_metadata_value(meta, "pair_type"),
                                "is_correct": self.get_metadata_value(meta, "is_correct"),
                                "subject": self.get_metadata_value(meta, "subject"),
                                "correct_answer": self.get_metadata_value(meta, "correct_answer"),
                                "target_new": self.get_metadata_value(meta, "target_new"),
                                "n_active_features": na,
                                "sum_active_activation": sa,
                                "max_active_activation": ma,
                                "mean_active_activation": sa / na if na > 0 else 0.0,
                                "sae_folder": sae["folder"],
                            }
                        )

                    del feat
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()

                for feature_id in range(d_sae):
                    count = int(feature_counts[feature_id])
                    if count == 0:
                        continue

                    total_activation = float(feature_sums[feature_id])
                    global_summary_rows.append(
                        {
                            "layer": layer,
                            "feature_id": feature_id,
                            "active_count": count,
                            "active_fraction": count / len(metadata),
                            "total_activation": total_activation,
                            "mean_activation_when_active": total_activation / count,
                            "max_activation": float(feature_max[feature_id]),
                            "sae_folder": sae["folder"],
                        }
                    )

                del sae
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

        prompt_summary_df = pd.DataFrame(prompt_summary_rows)
        global_summary_df = pd.DataFrame(global_summary_rows)

        if not global_summary_df.empty:
            global_summary_df = global_summary_df.sort_values(
                ["layer", "active_count", "total_activation"],
                ascending=[True, False, False],
            )

        prompt_summary_df.to_csv(self.prompt_summary_path, index=False)
        global_summary_df.to_csv(self.global_feature_summary_path, index=False)

        print()
        print("Saved active SAE feature table:", self.active_features_path)
        print("Saved prompt SAE summary:", self.prompt_summary_path)
        print("Saved global SAE feature summary:", self.global_feature_summary_path)
        print("Prompt summary rows:", len(prompt_summary_df))
        print("Global active features:", len(global_summary_df))

        if not prompt_summary_df.empty:
            print()
            print("Mean active features by layer:")
            print(prompt_summary_df.groupby("layer")["n_active_features"].mean())

        return self.active_features_path
