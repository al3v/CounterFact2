from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import torch

from adl_sae.config import ExperimentConfig


def to_bool(x) -> bool:
    if isinstance(x, bool):
        return x

    if pd.isna(x):
        return False

    return str(x).strip().lower() in {"true", "1", "yes"}


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)

    if denom == 0:
        return float("nan")

    cosine_similarity = float(np.dot(a, b) / denom)
    return 1.0 - cosine_similarity


def l2_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


class DensePairDistanceAnalyzer:
    def __init__(self, config: ExperimentConfig) -> None:
        self.config = config

    @property
    def hidden_states_path(self) -> Path:
        return Path(self.config.hidden_states_path)

    @property
    def output_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"dense_pair_distances_{self.config.experiment_name}.csv"
        )

    @property
    def summary_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"dense_pair_distance_summary_{self.config.experiment_name}.csv"
        )

    def load_hidden_state_object(self):
        if not self.hidden_states_path.exists():
            raise FileNotFoundError(
                f"Hidden-state file not found: {self.hidden_states_path}"
            )

        obj = torch.load(self.hidden_states_path, map_location="cpu")

        if "hidden_states" in obj:
            hidden_states = obj["hidden_states"]
        elif "activations" in obj:
            hidden_states = obj["activations"]
        else:
            raise KeyError("Expected key 'hidden_states' or 'activations' in .pt file.")

        if not isinstance(hidden_states, torch.Tensor):
            hidden_states = torch.tensor(hidden_states)

        if "row_metadata" in obj:
            metadata = pd.DataFrame(obj["row_metadata"])
        else:
            metadata_path = self.config.hidden_states_metadata_path
            if not metadata_path.exists():
                raise FileNotFoundError(
                    "No row_metadata in hidden-state file and metadata CSV not found: "
                    f"{metadata_path}"
                )
            metadata = pd.read_csv(metadata_path)

        layers = obj.get("layers", list(self.config.layers))

        return hidden_states.cpu(), metadata, list(layers)

    def infer_pair_type(self, group: pd.DataFrame) -> str:
        if "pair_type" in group.columns:
            values = group["pair_type"].dropna().unique()
            if len(values) > 0:
                return str(values[0])

        correct_count = int(group["is_correct"].map(to_bool).sum())

        if correct_count == 2:
            return "correct_correct"
        if correct_count == 1:
            return "correct_wrong"
        return "wrong_wrong"

    def run(self) -> tuple[Path, Path]:
        hidden_states, metadata, layers = self.load_hidden_state_object()

        if len(metadata) != hidden_states.shape[0]:
            raise ValueError(
                f"Metadata rows ({len(metadata)}) do not match hidden states "
                f"({hidden_states.shape[0]})."
            )

        required_cols = {"fact_id", "variant_id", "is_correct"}
        missing = required_cols - set(metadata.columns)
        if missing:
            raise ValueError(f"Missing required metadata columns: {sorted(missing)}")

        rows = []

        print("=== Dense pair-distance analysis ===")
        print("Experiment:", self.config.experiment_name)
        print("Model:", self.config.model_name)
        print("Hidden states:", self.hidden_states_path)
        print("Hidden shape:", tuple(hidden_states.shape))
        print("Layers:", layers)

        for fact_id, group in metadata.groupby("fact_id", sort=False):
            if len(group) != 2:
                continue

            group = group.sort_values("variant_id")
            indices = group.index.to_list()

            idx_a, idx_b = indices[0], indices[1]
            pair_type = self.infer_pair_type(group)

            row_a = group.iloc[0]
            row_b = group.iloc[1]

            for layer_position, layer in enumerate(layers):
                vec_a = hidden_states[idx_a, layer_position, :].numpy()
                vec_b = hidden_states[idx_b, layer_position, :].numpy()

                rows.append(
                    {
                        "experiment_name": self.config.experiment_name,
                        "model_name": self.config.model_name,
                        "fact_id": fact_id,
                        "layer": layer,
                        "pair_type": pair_type,
                        "variant_a": row_a["variant_id"],
                        "variant_b": row_b["variant_id"],
                        "is_correct_a": to_bool(row_a["is_correct"]),
                        "is_correct_b": to_bool(row_b["is_correct"]),
                        "cosine_distance": cosine_distance(vec_a, vec_b),
                        "l2_distance": l2_distance(vec_a, vec_b),
                    }
                )

        distances = pd.DataFrame(rows)

        if distances.empty:
            raise ValueError("No two-row fact pairs found. Could not compute distances.")

        summary = (
            distances.groupby(["layer", "pair_type"])
            .agg(
                n_pairs=("fact_id", "count"),
                mean_cosine_distance=("cosine_distance", "mean"),
                median_cosine_distance=("cosine_distance", "median"),
                std_cosine_distance=("cosine_distance", "std"),
                mean_l2_distance=("l2_distance", "mean"),
                median_l2_distance=("l2_distance", "median"),
                std_l2_distance=("l2_distance", "std"),
            )
            .reset_index()
        )

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        distances.to_csv(self.output_path, index=False)
        summary.to_csv(self.summary_path, index=False)

        print()
        print("Saved distances:", self.output_path)
        print("Saved summary:", self.summary_path)
        print()
        print("Summary:")
        print(summary)

        return self.output_path, self.summary_path
