import os
import pandas as pd


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"


def main():
    prompt_summary_path = f"{REPORTS_DIR}/sae_prompt_summary_{EXPERIMENT_NAME}.csv"
    active_features_path = f"outputs/sae_active_features_{EXPERIMENT_NAME}.csv"

    out_prompt_stats = f"{REPORTS_DIR}/sae_prompt_group_stats_{EXPERIMENT_NAME}.csv"
    out_switching_stats = f"{REPORTS_DIR}/sae_switching_correct_vs_wrong_stats_{EXPERIMENT_NAME}.csv"
    out_top_features = f"{REPORTS_DIR}/sae_top_correct_vs_wrong_features_{EXPERIMENT_NAME}.csv"
    out_top_switching_features = f"{REPORTS_DIR}/sae_top_switching_features_{EXPERIMENT_NAME}.csv"

    os.makedirs(REPORTS_DIR, exist_ok=True)

    prompt_df = pd.read_csv(prompt_summary_path)
    active_df = pd.read_csv(active_features_path)

    prompt_df["is_correct"] = prompt_df["is_correct"].astype(str).str.lower().isin(["true", "1", "yes"])
    active_df["is_correct"] = active_df["is_correct"].astype(str).str.lower().isin(["true", "1", "yes"])

    print("Prompt summary rows:", len(prompt_df))
    print("Active feature rows:", len(active_df))
    print("Layers:", sorted(prompt_df["layer"].unique()))
    print()

    # ============================================================
    # 1) Prompt-level SAE sparsity stats by pair_type and layer
    # ============================================================
    prompt_group_stats = (
        prompt_df
        .groupby(["layer", "pair_type"])
        .agg(
            n_rows=("row_id", "count"),
            mean_active_features=("n_active_features", "mean"),
            std_active_features=("n_active_features", "std"),
            mean_sum_activation=("sum_active_activation", "mean"),
            mean_max_activation=("max_active_activation", "mean"),
            accuracy=("is_correct", "mean"),
        )
        .reset_index()
    )

    prompt_group_stats.to_csv(out_prompt_stats, index=False)

    print("=== Prompt-level group stats ===")
    print(prompt_group_stats.to_string(index=False))
    print()

    # ============================================================
    # 2) Within switching facts: correct paraphrase vs wrong paraphrase
    # ============================================================
    switching_df = prompt_df[prompt_df["pair_type"] == "correct_wrong"].copy()

    switching_stats = (
        switching_df
        .groupby(["layer", "is_correct"])
        .agg(
            n_rows=("row_id", "count"),
            mean_active_features=("n_active_features", "mean"),
            std_active_features=("n_active_features", "std"),
            mean_sum_activation=("sum_active_activation", "mean"),
            mean_max_activation=("max_active_activation", "mean"),
        )
        .reset_index()
    )

    switching_stats.to_csv(out_switching_stats, index=False)

    print("=== Switching facts: correct vs wrong prompt stats ===")
    print(switching_stats.to_string(index=False))
    print()

    # ============================================================
    # 3) Feature-level correct vs wrong differences across all prompts
    # ============================================================
    layer_row_counts = (
        prompt_df
        .groupby(["layer", "is_correct"])["row_id"]
        .nunique()
        .rename("n_prompts")
        .reset_index()
    )

    feature_counts = (
        active_df
        .groupby(["layer", "feature_id", "is_correct"])
        .agg(
            active_count=("row_id", "nunique"),
            mean_activation_when_active=("activation", "mean"),
            max_activation=("activation", "max"),
        )
        .reset_index()
    )

    feature_counts = feature_counts.merge(
        layer_row_counts,
        on=["layer", "is_correct"],
        how="left",
    )

    feature_counts["active_fraction"] = feature_counts["active_count"] / feature_counts["n_prompts"]

    # pivot correct/wrong active fractions
    pivot = feature_counts.pivot_table(
        index=["layer", "feature_id"],
        columns="is_correct",
        values="active_fraction",
        fill_value=0.0,
    ).reset_index()

    if True not in pivot.columns:
        pivot[True] = 0.0
    if False not in pivot.columns:
        pivot[False] = 0.0

    pivot = pivot.rename(columns={True: "active_fraction_correct", False: "active_fraction_wrong"})
    pivot["fraction_diff_correct_minus_wrong"] = (
        pivot["active_fraction_correct"] - pivot["active_fraction_wrong"]
    )
    pivot["abs_fraction_diff"] = pivot["fraction_diff_correct_minus_wrong"].abs()

    # total active count for filtering
    total_counts = (
        active_df
        .groupby(["layer", "feature_id"])["row_id"]
        .nunique()
        .rename("total_active_count")
        .reset_index()
    )

    pivot = pivot.merge(total_counts, on=["layer", "feature_id"], how="left")
    pivot = pivot[pivot["total_active_count"] >= 10].copy()

    top_features = (
        pivot
        .sort_values(["layer", "abs_fraction_diff"], ascending=[True, False])
        .groupby("layer")
        .head(25)
        .reset_index(drop=True)
    )

    top_features.to_csv(out_top_features, index=False)

    print("=== Top correctness-associated SAE features ===")
    print(top_features.head(60).to_string(index=False))
    print()

    # ============================================================
    # 4) Feature-level differences only inside switching facts
    # ============================================================
    switching_row_ids = set(switching_df["row_id"].unique())
    active_switch = active_df[active_df["row_id"].isin(switching_row_ids)].copy()

    switching_layer_row_counts = (
        switching_df
        .groupby(["layer", "is_correct"])["row_id"]
        .nunique()
        .rename("n_prompts")
        .reset_index()
    )

    switch_feature_counts = (
        active_switch
        .groupby(["layer", "feature_id", "is_correct"])
        .agg(
            active_count=("row_id", "nunique"),
            mean_activation_when_active=("activation", "mean"),
            max_activation=("activation", "max"),
        )
        .reset_index()
    )

    switch_feature_counts = switch_feature_counts.merge(
        switching_layer_row_counts,
        on=["layer", "is_correct"],
        how="left",
    )

    switch_feature_counts["active_fraction"] = (
        switch_feature_counts["active_count"] / switch_feature_counts["n_prompts"]
    )

    switch_pivot = switch_feature_counts.pivot_table(
        index=["layer", "feature_id"],
        columns="is_correct",
        values="active_fraction",
        fill_value=0.0,
    ).reset_index()

    if True not in switch_pivot.columns:
        switch_pivot[True] = 0.0
    if False not in switch_pivot.columns:
        switch_pivot[False] = 0.0

    switch_pivot = switch_pivot.rename(
        columns={True: "active_fraction_correct", False: "active_fraction_wrong"}
    )

    switch_pivot["fraction_diff_correct_minus_wrong"] = (
        switch_pivot["active_fraction_correct"] - switch_pivot["active_fraction_wrong"]
    )
    switch_pivot["abs_fraction_diff"] = switch_pivot["fraction_diff_correct_minus_wrong"].abs()

    switch_total_counts = (
        active_switch
        .groupby(["layer", "feature_id"])["row_id"]
        .nunique()
        .rename("total_active_count")
        .reset_index()
    )

    switch_pivot = switch_pivot.merge(
        switch_total_counts,
        on=["layer", "feature_id"],
        how="left",
    )

    switch_pivot = switch_pivot[switch_pivot["total_active_count"] >= 5].copy()

    top_switching_features = (
        switch_pivot
        .sort_values(["layer", "abs_fraction_diff"], ascending=[True, False])
        .groupby("layer")
        .head(25)
        .reset_index(drop=True)
    )

    top_switching_features.to_csv(out_top_switching_features, index=False)

    print("=== Top switching-specific SAE features ===")
    print(top_switching_features.head(60).to_string(index=False))
    print()

    print("Saved:")
    print(out_prompt_stats)
    print(out_switching_stats)
    print(out_top_features)
    print(out_top_switching_features)


if __name__ == "__main__":
    main()
