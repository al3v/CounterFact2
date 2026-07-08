import os
import pandas as pd

EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"
READABLE_DIR = f"{REPORTS_DIR}/readable_tables"

PROMPT_SUMMARY_PATH = f"{REPORTS_DIR}/sae_prompt_summary_{EXPERIMENT_NAME}.csv"
GLOBAL_SUMMARY_PATH = f"{REPORTS_DIR}/sae_global_feature_summary_{EXPERIMENT_NAME}.csv"

SELECTED_LAYERS = [2, 12, 18]
TOP_K = 10


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
    os.makedirs(READABLE_DIR, exist_ok=True)

    prompt_df = pd.read_csv(PROMPT_SUMMARY_PATH)
    global_df = pd.read_csv(GLOBAL_SUMMARY_PATH)

    # make sure is_correct is numeric/bool for mean
    prompt_df["is_correct"] = prompt_df["is_correct"].astype(str).str.lower().isin(["true", "1", "yes"])

    # -------------------------
    # 1) Prompt-level readable summary
    # -------------------------
    prompt_small = prompt_df[prompt_df["layer"].isin(SELECTED_LAYERS)].copy()

    prompt_table = (
        prompt_small
        .groupby(["layer", "pair_type"], as_index=False)
        .agg(
            n_prompts=("row_id", "count"),
            n_facts=("fact_id", "nunique"),
            correct_rate=("is_correct", "mean"),
            mean_n_active_features=("n_active_features", "mean"),
            mean_sum_active_activation=("sum_active_activation", "mean"),
            mean_max_active_activation=("max_active_activation", "mean"),
        )
        .sort_values(["layer", "pair_type"])
    )

    for col in ["correct_rate", "mean_n_active_features", "mean_sum_active_activation", "mean_max_active_activation"]:
        prompt_table[col] = prompt_table[col].round(4)

    prompt_csv = f"{READABLE_DIR}/sae_prompt_summary_selected_layers.csv"
    prompt_md = f"{READABLE_DIR}/sae_prompt_summary_selected_layers.md"
    prompt_table.to_csv(prompt_csv, index=False)

    with open(prompt_md, "w", encoding="utf-8") as f:
        f.write("# SAE prompt summary (selected layers)\n\n")
        f.write(f"Selected layers: {SELECTED_LAYERS}\n\n")
        f.write(df_to_markdown(prompt_table))
        f.write("\n")

    # -------------------------
    # 2) Top SAE features per selected layer
    # -------------------------
    global_small = global_df[global_df["layer"].isin(SELECTED_LAYERS)].copy()

    top_features = (
        global_small
        .sort_values(["layer", "active_count", "total_activation"], ascending=[True, False, False])
        .groupby("layer", group_keys=False)
        .head(TOP_K)
        .copy()
    )

    for col in ["active_fraction", "total_activation", "mean_activation_when_active", "max_activation"]:
        top_features[col] = top_features[col].round(4)

    top_csv = f"{READABLE_DIR}/sae_top_features_selected_layers.csv"
    top_md = f"{READABLE_DIR}/sae_top_features_selected_layers.md"
    top_features.to_csv(top_csv, index=False)

    with open(top_md, "w", encoding="utf-8") as f:
        f.write("# Top SAE features (selected layers)\n\n")
        f.write(f"Selected layers: {SELECTED_LAYERS}\n\n")
        f.write(f"Top {TOP_K} features per layer by active_count.\n\n")
        f.write(df_to_markdown(top_features))
        f.write("\n")

    print("Saved:", prompt_csv)
    print("Saved:", prompt_md)
    print("Saved:", top_csv)
    print("Saved:", top_md)


if __name__ == "__main__":
    main()
