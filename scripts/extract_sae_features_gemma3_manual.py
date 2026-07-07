import argparse
import csv
import json
import os

import pandas as pd
import torch
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from tqdm import tqdm


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"


def parse_layers(layer_string):
    return [int(x.strip()) for x in layer_string.split(",") if x.strip()]


def safe_torch_load(path):
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


def load_gemma_scope_sae(repo, folder, device):
    config_path = hf_hub_download(repo_id=repo, filename=f"{folder}/config.json")
    params_path = hf_hub_download(repo_id=repo, filename=f"{folder}/params.safetensors")

    with open(config_path, "r") as f:
        cfg = json.load(f)

    state = load_file(params_path)

    sae = {
        "cfg": cfg,
        "w_enc": state["w_enc"].to(device=device, dtype=torch.float32),
        "b_enc": state["b_enc"].to(device=device, dtype=torch.float32),
        "b_dec": state["b_dec"].to(device=device, dtype=torch.float32),
        "threshold": state["threshold"].to(device=device, dtype=torch.float32),
    }

    return sae


def encode_jumprelu(x, sae):
    """
    Manual Gemma Scope 2 JumpReLU SAE encoder.

    x shape:
        batch_size x d_model

    SAE:
        pre_acts = x @ w_enc + b_enc
        feature_acts = ReLU(pre_acts) if pre_acts > threshold else 0

    Important:
        Do NOT subtract b_dec before encoding.
        In Gemma Scope 2, the inference encoder uses the folded encoder bias.
    """
    pre_acts = x @ sae["w_enc"] + sae["b_enc"]
    feature_acts = torch.relu(pre_acts) * (pre_acts > sae["threshold"])
    return feature_acts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--hidden-states",
        default=f"outputs/hidden_states_{EXPERIMENT_NAME}.pt",
    )
    parser.add_argument(
        "--active-output",
        default=f"outputs/sae_active_features_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument(
        "--prompt-summary-output",
        default=f"{REPORTS_DIR}/sae_prompt_summary_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument(
        "--feature-summary-output",
        default=f"{REPORTS_DIR}/sae_global_feature_summary_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument("--repo", default="google/gemma-scope-2-4b-pt")
    parser.add_argument(
        "--sae-folder-template",
        default="resid_post_all/layer_{layer}_width_16k_l0_small",
    )
    parser.add_argument("--layers", default="2,3,4,12,15,18")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.active_output), exist_ok=True)
    os.makedirs(os.path.dirname(args.prompt_summary_output), exist_ok=True)
    os.makedirs(os.path.dirname(args.feature_summary_output), exist_ok=True)

    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    requested_layers = parse_layers(args.layers)

    obj = safe_torch_load(args.hidden_states)

    activations = obj["activations"]
    saved_layers = [int(x) for x in obj["layers"]]

    if args.max_rows is not None:
        activations = activations[: args.max_rows]

    row_meta = pd.DataFrame(obj["row_metadata"])
    if args.max_rows is not None:
        row_meta = row_meta.head(args.max_rows).copy()

    row_meta = row_meta.reset_index(drop=True)

    print("Hidden-state file:", args.hidden_states)
    print("Activation shape:", tuple(activations.shape))
    print("Saved layers:", saved_layers)
    print("Requested SAE layers:", requested_layers)
    print("Rows:", len(row_meta))
    print("Device:", device)
    print("SAE repo:", args.repo)
    print()

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

    with open(args.active_output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=active_fieldnames)
        writer.writeheader()

        for layer in requested_layers:
            if layer not in saved_layers:
                raise ValueError(f"Layer {layer} not found in saved hidden states: {saved_layers}")

            layer_index = saved_layers.index(layer)
            folder = args.sae_folder_template.format(layer=layer)

            print("=" * 80)
            print(f"Loading SAE for layer {layer}")
            print("Folder:", folder)

            sae = load_gemma_scope_sae(
                repo=args.repo,
                folder=folder,
                device=device,
            )

            cfg = sae["cfg"]
            d_sae = int(cfg["width"])

            print("Hook in:", cfg.get("hf_hook_point_in"))
            print("Architecture:", cfg.get("architecture"))
            print("Width:", d_sae)
            print("L0:", cfg.get("l0"))

            layer_acts = activations[:, layer_index, :]

            feature_counts = torch.zeros(d_sae, dtype=torch.long)
            feature_sums = torch.zeros(d_sae, dtype=torch.float64)
            feature_max = torch.zeros(d_sae, dtype=torch.float32)

            for start in tqdm(range(0, len(row_meta), args.batch_size), desc=f"Layer {layer}"):
                end = min(start + args.batch_size, len(row_meta))

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

                    # update max activation per feature
                    active_indices_cpu = active_indices.detach().cpu()
                    active_values_cpu = active_values.detach().cpu().float()

                    for fid, val in zip(active_indices_cpu[:, 1].tolist(), active_values_cpu.tolist()):
                        if val > feature_max[fid]:
                            feature_max[fid] = val

                    for idx, value in zip(active_indices_cpu.tolist(), active_values_cpu.tolist()):
                        local_row_idx, feature_id = idx
                        global_row_idx = start + local_row_idx
                        meta = row_meta.iloc[global_row_idx]

                        writer.writerow(
                            {
                                "row_id": int(meta["row_id"]),
                                "fact_id": meta["fact_id"],
                                "variant_id": meta["variant_id"],
                                "layer": layer,
                                "pair_type": meta["pair_type"],
                                "is_correct": bool(meta["is_correct"]),
                                "subject": meta["subject"],
                                "correct_answer": meta["correct_answer"],
                                "target_new": meta["target_new"],
                                "feature_id": int(feature_id),
                                "activation": float(value),
                            }
                        )

                for i in range(end - start):
                    meta = row_meta.iloc[start + i]
                    na = int(n_active[i])
                    sa = float(sum_active[i])
                    ma = float(max_active[i])

                    prompt_summary_rows.append(
                        {
                            "row_id": int(meta["row_id"]),
                            "fact_id": meta["fact_id"],
                            "variant_id": meta["variant_id"],
                            "layer": layer,
                            "pair_type": meta["pair_type"],
                            "is_correct": bool(meta["is_correct"]),
                            "subject": meta["subject"],
                            "correct_answer": meta["correct_answer"],
                            "target_new": meta["target_new"],
                            "n_active_features": na,
                            "sum_active_activation": sa,
                            "max_active_activation": ma,
                            "mean_active_activation": sa / na if na > 0 else 0.0,
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
                        "active_fraction": count / len(row_meta),
                        "total_activation": total_activation,
                        "mean_activation_when_active": total_activation / count,
                        "max_activation": float(feature_max[feature_id]),
                        "sae_folder": folder,
                    }
                )

            del sae
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    prompt_summary_df = pd.DataFrame(prompt_summary_rows)
    prompt_summary_df.to_csv(args.prompt_summary_output, index=False)

    global_summary_df = pd.DataFrame(global_summary_rows)
    global_summary_df = global_summary_df.sort_values(
        ["layer", "active_count", "total_activation"],
        ascending=[True, False, False],
    )
    global_summary_df.to_csv(args.feature_summary_output, index=False)

    print()
    print("Saved active SAE feature table:", args.active_output)
    print("Saved prompt SAE summary:", args.prompt_summary_output)
    print("Saved global SAE feature summary:", args.feature_summary_output)
    print("Prompt summary rows:", len(prompt_summary_df))
    print("Global active features:", len(global_summary_df))

    print()
    print("Mean active features by layer:")
    print(prompt_summary_df.groupby("layer")["n_active_features"].mean())


if __name__ == "__main__":
    main()
