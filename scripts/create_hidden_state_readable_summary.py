import os
import pandas as pd
import torch


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"

HIDDEN_PATH = f"outputs/hidden_states_{EXPERIMENT_NAME}.pt"
METADATA_PATH = f"reports/{EXPERIMENT_NAME}/hidden_states_metadata_{EXPERIMENT_NAME}.csv"

OUT_DIR = f"reports/{EXPERIMENT_NAME}/readable_tables"
OUT_MD = f"{OUT_DIR}/hidden_states_readable_summary.md"
OUT_CSV = f"{OUT_DIR}/hidden_state_layer_norm_summary.csv"


def clean_text(x, max_len=120):
    if pd.isna(x):
        return ""
    x = str(x).replace("\n", " ").strip()
    if len(x) > max_len:
        return x[:max_len] + "..."
    return x


def to_bool(x):
    if isinstance(x, bool):
        return x
    return str(x).lower() in ["true", "1", "yes"]


def df_to_markdown(df):
    if df.empty:
        return "_No rows._"

    df = df.copy()

    for col in df.columns:
        df[col] = df[col].astype(str).str.replace("|", "\\|", regex=False)

    headers = list(df.columns)
    lines = []

    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")

    return "\n".join(lines)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    if not os.path.exists(HIDDEN_PATH):
        raise FileNotFoundError(f"Missing hidden-state file: {HIDDEN_PATH}")

    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(f"Missing metadata file: {METADATA_PATH}")

    obj = torch.load(HIDDEN_PATH, map_location="cpu")
    metadata_df = pd.read_csv(METADATA_PATH)

    activations = obj["activations"]
    layers = obj["layers"]
    hf_indices = obj["hf_hidden_state_indices"]

    n_prompts, n_layers, hidden_dim = activations.shape

    metadata_df["is_correct"] = metadata_df["is_correct"].apply(to_bool)

    summary_rows = []

    for layer_idx, layer in enumerate(layers):
        layer_acts = activations[:, layer_idx, :].float()
        norms = torch.linalg.norm(layer_acts, dim=1).numpy()

        norm_df = pd.DataFrame(
            {
                "row_id": range(n_prompts),
                "layer": layer,
                "hidden_state_l2_norm": norms,
            }
        )

        layer_meta = metadata_df[metadata_df["layer"] == layer].copy()
        layer_meta = layer_meta.merge(norm_df, on=["row_id", "layer"], how="left")

        for pair_type, group in layer_meta.groupby("pair_type"):
            summary_rows.append(
                {
                    "layer": layer,
                    "hf_hidden_state_index": hf_indices[layer],
                    "pair_type": pair_type,
                    "n_prompts": len(group),
                    "n_facts": group["fact_id"].nunique(),
                    "correct_rate": round(group["is_correct"].mean(), 4),
                    "mean_n_tokens": round(group["n_tokens"].mean(), 2),
                    "mean_l2_norm": round(group["hidden_state_l2_norm"].mean(), 4),
                    "std_l2_norm": round(group["hidden_state_l2_norm"].std(), 4),
                }
            )

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_CSV, index=False)

    layer_table = pd.DataFrame(
        [
            {
                "model_layer": layer,
                "hf_hidden_state_index": hf_indices[layer],
                "n_prompts": n_prompts,
                "hidden_dim": hidden_dim,
            }
            for layer in layers
        ]
    )

    example_cols = [
        "fact_id",
        "variant_id",
        "pair_type",
        "is_correct",
        "subject",
        "correct_answer",
        "target_new",
        "n_tokens",
        "prompt",
        "generated_answer",
    ]

    first_layer = layers[0]
    examples = metadata_df[metadata_df["layer"] == first_layer][example_cols].head(12).copy()
    examples["prompt"] = examples["prompt"].apply(clean_text)
    examples["generated_answer"] = examples["generated_answer"].apply(clean_text)

    lines = []

    lines.append("# Hidden-state extraction readable summary")
    lines.append("")
    lines.append("This file summarizes the hidden states extracted from Gemma 3.")
    lines.append("The raw hidden-state vectors are not shown because each vector has 2560 dimensions.")
    lines.append("")

    lines.append("## Extraction overview")
    lines.append("")
    lines.append(f"- **Experiment:** {obj['experiment_name']}")
    lines.append(f"- **Model:** {obj['model_name']}")
    lines.append(f"- **Activation type:** {obj['activation_type']}")
    lines.append(f"- **Activation tensor shape:** `{tuple(activations.shape)}`")
    lines.append(f"- **Prompts:** {n_prompts}")
    lines.append(f"- **Selected layers:** {layers}")
    lines.append(f"- **Hidden dimension:** {hidden_dim}")
    lines.append("")

    lines.append("## Layer indexing")
    lines.append("")
    lines.append(df_to_markdown(layer_table))
    lines.append("")

    lines.append("## Hidden-state norm summary by layer and pair type")
    lines.append("")
    lines.append(df_to_markdown(summary_df))
    lines.append("")

    lines.append("## Example prompt metadata")
    lines.append("")
    lines.append(df_to_markdown(examples))
    lines.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Saved:", OUT_MD)
    print("Saved:", OUT_CSV)


if __name__ == "__main__":
    main()
