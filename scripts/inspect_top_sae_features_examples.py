import os
import pandas as pd


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"


def main():
    active_path = f"outputs/sae_active_features_{EXPERIMENT_NAME}.csv"
    prompt_outputs_path = f"outputs/prompt_outputs_{EXPERIMENT_NAME}.csv"
    top_switch_path = f"{REPORTS_DIR}/sae_top_switching_features_{EXPERIMENT_NAME}.csv"

    out_path = f"{REPORTS_DIR}/sae_top_feature_prompt_examples_{EXPERIMENT_NAME}.csv"

    active_df = pd.read_csv(active_path)
    prompt_df = pd.read_csv(prompt_outputs_path)
    top_df = pd.read_csv(top_switch_path)

    active_df["is_correct"] = active_df["is_correct"].astype(str).str.lower().isin(["true", "1", "yes"])
    prompt_df["is_correct"] = prompt_df["is_correct"].astype(str).str.lower().isin(["true", "1", "yes"])

    # row_id in SAE files corresponds to original prompt-output row index
    prompt_df = prompt_df.reset_index(drop=True)
    prompt_df["row_id"] = range(len(prompt_df))

    # Keep only top 10 switching-associated features per layer
    top_df = (
        top_df.sort_values(["layer", "abs_fraction_diff"], ascending=[True, False])
        .groupby("layer")
        .head(10)
        .copy()
    )

    rows = []

    for _, feat_row in top_df.iterrows():
        layer = int(feat_row["layer"])
        feature_id = int(feat_row["feature_id"])

        subset = active_df[
            (active_df["layer"] == layer)
            & (active_df["feature_id"] == feature_id)
        ].copy()

        # strongest activating prompts for this feature
        subset = subset.sort_values("activation", ascending=False).head(8)

        merged = subset.merge(
            prompt_df[
                [
                    "row_id",
                    "prompt",
                    "generated_answer",
                ]
            ],
            on="row_id",
            how="left",
        )

        for _, row in merged.iterrows():
            rows.append(
                {
                    "layer": layer,
                    "feature_id": feature_id,
                    "feature_direction": (
                        "more_correct"
                        if feat_row["fraction_diff_correct_minus_wrong"] > 0
                        else "more_wrong"
                    ),
                    "active_fraction_correct": feat_row["active_fraction_correct"],
                    "active_fraction_wrong": feat_row["active_fraction_wrong"],
                    "fraction_diff_correct_minus_wrong": feat_row["fraction_diff_correct_minus_wrong"],
                    "activation": row["activation"],
                    "row_id": row["row_id"],
                    "fact_id": row["fact_id"],
                    "variant_id": row["variant_id"],
                    "pair_type": row["pair_type"],
                    "is_correct": row["is_correct"],
                    "subject": row["subject"],
                    "correct_answer": row["correct_answer"],
                    "target_new": row["target_new"],
                    "prompt": row["prompt"],
                    "generated_answer": row["generated_answer"],
                }
            )

    out_df = pd.DataFrame(rows)
    out_df.to_csv(out_path, index=False)

    print("Saved:", out_path)
    print("Rows:", len(out_df))
    print()
    print(out_df.head(40).to_string(index=False))


if __name__ == "__main__":
    main()
