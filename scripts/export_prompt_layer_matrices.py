from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from scipy import sparse

from adl_sae.config_registry import add_config_argument, get_config


def load_hidden_state_object(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Hidden-state file not found: {path}")

    obj = torch.load(path, map_location="cpu")

    if "hidden_states" in obj:
        hidden = obj["hidden_states"]
    elif "activations" in obj:
        hidden = obj["activations"]
    else:
        raise KeyError("Expected key 'hidden_states' or 'activations' in hidden-state file.")

    if not isinstance(hidden, torch.Tensor):
        hidden = torch.tensor(hidden)

    layers = obj.get("layers")
    if layers is None:
        raise KeyError("Hidden-state file does not contain 'layers'.")

    if "row_metadata" in obj:
        row_metadata = pd.DataFrame(obj["row_metadata"])
    else:
        row_metadata = None

    return hidden.float().cpu(), list(layers), row_metadata


def load_row_metadata(config, hidden_n_rows: int):
    hidden_path = Path(config.hidden_states_path)
    hidden, layers, row_metadata = load_hidden_state_object(hidden_path)

    if row_metadata is not None and len(row_metadata) == hidden_n_rows:
        return row_metadata

    metadata_path = Path(config.hidden_states_metadata_path)
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    metadata = pd.read_csv(metadata_path)

    # Some metadata files are long format: one row per prompt × layer.
    # For matrix export we need one row per prompt.
    if "row_id" in metadata.columns:
        metadata = metadata.drop_duplicates(subset=["row_id"]).copy()
        metadata = metadata.sort_values("row_id").reset_index(drop=True)
    else:
        metadata = metadata.drop_duplicates().reset_index(drop=True)
        metadata["row_id"] = np.arange(len(metadata))

    if len(metadata) != hidden_n_rows:
        raise ValueError(
            f"Metadata rows after dedup ({len(metadata)}) do not match hidden rows ({hidden_n_rows})."
        )

    return metadata


def build_sae_sparse_matrix(active_df: pd.DataFrame, metadata: pd.DataFrame, layer: int, sae_width: int):
    layer_df = active_df[active_df["layer"].astype(int) == int(layer)].copy()

    if "row_id" not in layer_df.columns:
        raise KeyError("Active-feature table must contain row_id.")

    if "feature_id" not in layer_df.columns or "activation" not in layer_df.columns:
        raise KeyError("Active-feature table must contain feature_id and activation.")

    row_ids = metadata["row_id"].tolist()
    row_id_to_position = {rid: pos for pos, rid in enumerate(row_ids)}

    layer_df = layer_df[layer_df["row_id"].isin(row_id_to_position)].copy()

    row_positions = layer_df["row_id"].map(row_id_to_position).to_numpy()
    feature_ids = layer_df["feature_id"].astype(int).to_numpy()
    activations = layer_df["activation"].astype(float).to_numpy()

    mat = sparse.csr_matrix(
        (activations, (row_positions, feature_ids)),
        shape=(len(metadata), int(sae_width)),
        dtype=np.float32,
    )

    return mat


def main():
    parser = argparse.ArgumentParser(
        description="Export prompt-only residual and SAE activation matrices per layer."
    )
    add_config_argument(parser)
    args = parser.parse_args()

    config = get_config(args.config)

    hidden_path = Path(config.hidden_states_path)
    active_path = Path(config.sae_active_features_path)

    hidden, layers, row_metadata_from_obj = load_hidden_state_object(hidden_path)
    metadata = load_row_metadata(config, hidden.shape[0])

    if "row_id" not in metadata.columns:
        metadata["row_id"] = np.arange(len(metadata))

    if not active_path.exists():
        raise FileNotFoundError(f"SAE active-feature file not found: {active_path}")

    active_df = pd.read_csv(active_path)

    out_dir = Path(config.reports_dir) / "prompt_layer_matrices"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=== Export prompt layer matrices ===")
    print("Experiment:", config.experiment_name)
    print("Hidden states:", hidden_path)
    print("Hidden shape:", tuple(hidden.shape))
    print("SAE active features:", active_path)
    print("Rows:", hidden.shape[0])
    print("Layers:", layers)
    print("SAE width:", config.sae_width)
    print("Output dir:", out_dir)

    all_layer_metadata = []

    for layer_pos, layer in enumerate(layers):
        layer = int(layer)

        residual_matrix = hidden[:, layer_pos, :].numpy().astype(np.float32)
        sae_matrix = build_sae_sparse_matrix(
            active_df=active_df,
            metadata=metadata,
            layer=layer,
            sae_width=config.sae_width,
        )

        layer_meta = metadata.copy()
        layer_meta["layer"] = layer
        layer_meta["residual_matrix_file"] = f"layer_{layer}_prompt_residuals.npz"
        layer_meta["sae_matrix_file"] = f"layer_{layer}_sae_activations_sparse.npz"

        residual_path = out_dir / f"layer_{layer}_prompt_residuals.npz"
        sae_path = out_dir / f"layer_{layer}_sae_activations_sparse.npz"
        meta_path = out_dir / f"layer_{layer}_metadata.csv"

        np.savez_compressed(
            residual_path,
            residuals=residual_matrix,
            row_id=metadata["row_id"].to_numpy(),
            layer=np.array([layer]),
        )

        sparse.save_npz(sae_path, sae_matrix)
        layer_meta.to_csv(meta_path, index=False)

        all_layer_metadata.append(layer_meta)

        print()
        print(f"Layer {layer}")
        print("  residuals:", residual_path, residual_matrix.shape)
        print("  SAE sparse:", sae_path, sae_matrix.shape, "nnz=", sae_matrix.nnz)
        print("  metadata:", meta_path, layer_meta.shape)

    combined_metadata = pd.concat(all_layer_metadata, ignore_index=True)
    combined_metadata_path = out_dir / f"all_layers_metadata_{config.experiment_name}.csv"
    combined_metadata.to_csv(combined_metadata_path, index=False)

    print()
    print("Saved combined metadata:", combined_metadata_path)
    print("Done.")


if __name__ == "__main__":
    main()
