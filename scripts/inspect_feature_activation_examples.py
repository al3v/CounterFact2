"""
Inspect top activating CounterFact prompts for selected SAE features.

Local alternative to Neuronpedia lookup.

It answers:
    For a given SAE feature, which CounterFact prompts activate it most strongly?

This helps manually interpret SAE features using the exact experiment data.

Inputs:
    outputs/sae_active_features_<EXP>.csv
    reports/<EXP>/prompt_outputs_<EXP>.csv
    reports/<EXP>/sae_top_correct_vs_wrong_features_<EXP>.csv
    reports/<EXP>/sae_top_switching_features_<EXP>.csv

Outputs:
    reports/<EXP>/<output_prefix>_<EXP>.csv
    reports/<EXP>/<output_prefix>_<EXP>.md
"""

import argparse
import os
import pandas as pd


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"

ACTIVE_FEATURES_PATH = f"outputs/sae_active_features_{EXPERIMENT_NAME}.csv"
PROMPT_OUTPUTS_PATH = f"{REPORTS_DIR}/prompt_outputs_{EXPERIMENT_NAME}.csv"

TOP_CORRECT_WRONG_PATH = (
    f"{REPORTS_DIR}/sae_top_correct_vs_wrong_features_{EXPERIMENT_NAME}.csv"
)

TOP_SWITCHING_PATH = (
    f"{REPORTS_DIR}/sae_top_switching_features_{EXPERIMENT_NAME}.csv"
)


def to_bool(x):
    if pd.isna(x):
        return False
    if isinstance(x, bool):
        return x
    return str(x).strip().lower() in ["true", "1", "yes"]


def parse_layers(x):
    return [int(v.strip()) for v in x.split(",") if v.strip()]


def parse_manual_features(x):
    """
    Format:
        12:505,15:2034,18:123
    """
    pairs = []

    if not x:
        return pairs

    for item in x.split(","):
        item = item.strip()

        if not item:
            continue

        layer, feature_id = item.split(":")
        pairs.append((int(layer), int(feature_id)))

    return pairs


def safe_cols(df, cols):
    return [c for c in cols if c in df.columns]


def get_first_available_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def load_top_features(source, layers, top_n, direction):
    if source == "correct_vs_wrong":
        path = TOP_CORRECT_WRONG_PATH
    elif source == "switching":
        path = TOP_SWITCHING_PATH
    else:
        raise ValueError(f"Unknown source: {source}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing top feature file: {path}")

    df = pd.read_csv(path)
    df = df[df["layer"].isin(layers)].copy()

    diff_col = get_first_available_column(
        df,
        [
            "fraction_diff_correct_minus_wrong",
            "fraction_diff",
            "active_fraction_diff",
        ],
    )

    abs_diff_col = get_first_available_column(
        df,
        [
            "abs_fraction_diff",
            "abs_diff",
        ],
    )

    if diff_col is not None:
        df[diff_col] = pd.to_numeric(df[diff_col], errors="coerce")

        if direction == "more_correct":
            df = df[df[diff_col] > 0].copy()
            df = df.sort_values(["layer", diff_col], ascending=[True, False])

        elif direction == "more_wrong":
            df = df[df[diff_col] < 0].copy()
            df["ranking_score"] = df[diff_col].abs()
            df = df.sort_values(["layer", "ranking_score"], ascending=[True, False])

        else:
            df["ranking_score"] = df[diff_col].abs()
            df = df.sort_values(["layer", "ranking_score"], ascending=[True, False])

    elif abs_diff_col is not None:
        df[abs_diff_col] = pd.to_numeric(df[abs_diff_col], errors="coerce")
        df = df.sort_values(["layer", abs_diff_col], ascending=[True, False])

    else:
        print("WARNING: No difference column found. Sorting by layer and feature_id.")
        df = df.sort_values(["layer", "feature_id"], ascending=[True, True])

    top = df.groupby("layer").head(top_n).reset_index(drop=True)

    required = ["layer", "feature_id"]
    for col in required:
        if col not in top.columns:
            raise ValueError(f"Missing required column in top feature file: {col}")

    return top.drop_duplicates(subset=["layer", "feature_id"])


def prepare_prompt_metadata(prompt_df):
    """
    prompt_outputs has no row_id in your current file, but it has:
        fact_id, variant_id

    active_df also has:
        fact_id, variant_id

    So we merge using fact_id + variant_id.
    """

    merge_cols = ["fact_id", "variant_id"]

    for col in merge_cols:
        if col not in prompt_df.columns:
            raise ValueError(f"prompt_df is missing merge column: {col}")

    prompt_meta_cols = [
        "fact_id",
        "variant_id",
        "case_id",
        "split",
        "relation_id",
        "template",
        "base_prompt",
        "variant_source",
        "prompt",
        "target_true",
        "model_name",
        "generated_answer",
        "strict_answer_segment",
        "strict_matched_answer",
    ]

    prompt_meta_cols = [c for c in prompt_meta_cols if c in prompt_df.columns]
    prompt_meta_df = prompt_df[prompt_meta_cols].drop_duplicates(subset=merge_cols).copy()

    for col in merge_cols:
        prompt_meta_df[col] = prompt_meta_df[col].astype(str)

    return prompt_meta_df, merge_cols


def format_counts(series, top_k=5):
    if series is None or len(series) == 0:
        return "N/A"

    counts = series.dropna().astype(str).value_counts().head(top_k)

    if len(counts) == 0:
        return "N/A"

    return ", ".join(f"{idx}:{cnt}" for idx, cnt in counts.items())


def write_markdown(out_md, examples_df):
    lines = []

    lines.append("# SAE Feature Activation Examples")
    lines.append("")
    lines.append(
        "This file shows the top CounterFact prompts that activate selected SAE features."
    )
    lines.append("")
    lines.append(
        "These examples are for qualitative/manual interpretation only. "
        "They are not causal proof of feature meaning."
    )
    lines.append("")

    group_cols = ["inspected_layer", "inspected_feature_id"]

    for (layer, feature_id), group in examples_df.groupby(group_cols):
        first = group.iloc[0]

        lines.append(f"## Layer {layer}, Feature {feature_id}")
        lines.append("")

        if (
            "feature_fraction_diff_correct_minus_wrong" in first
            and pd.notna(first["feature_fraction_diff_correct_minus_wrong"])
        ):
            lines.append(
                f"- **fraction diff correct - wrong:** "
                f"{first['feature_fraction_diff_correct_minus_wrong']}"
            )

        if (
            "feature_active_fraction_correct" in first
            and pd.notna(first["feature_active_fraction_correct"])
        ):
            lines.append(
                f"- **active fraction correct:** "
                f"{first['feature_active_fraction_correct']}"
            )

        if (
            "feature_active_fraction_wrong" in first
            and pd.notna(first["feature_active_fraction_wrong"])
        ):
            lines.append(
                f"- **active fraction wrong:** "
                f"{first['feature_active_fraction_wrong']}"
            )

        if (
            "feature_total_active_count" in first
            and pd.notna(first["feature_total_active_count"])
        ):
            lines.append(
                f"- **total active count:** "
                f"{int(first['feature_total_active_count'])}"
            )

        if (
            "n_correct_activations_in_dataset" in first
            and pd.notna(first["n_correct_activations_in_dataset"])
        ):
            lines.append(
                f"- **activations on correct prompts in dataset:** "
                f"{int(first['n_correct_activations_in_dataset'])}"
            )

        if (
            "n_wrong_activations_in_dataset" in first
            and pd.notna(first["n_wrong_activations_in_dataset"])
        ):
            lines.append(
                f"- **activations on wrong prompts in dataset:** "
                f"{int(first['n_wrong_activations_in_dataset'])}"
            )

        if "top_relations" in first and pd.notna(first["top_relations"]):
            lines.append(f"- **top relations:** {first['top_relations']}")

        if "top_subjects" in first and pd.notna(first["top_subjects"]):
            lines.append(f"- **top subjects:** {first['top_subjects']}")

        lines.append("")
        lines.append("### Top activating prompts")
        lines.append("")

        for _, row in group.iterrows():
            activation = row.get("activation", "N/A")
            rank = row.get("prompt_rank", "N/A")

            lines.append(f"#### Rank {rank} | activation = {activation}")
            lines.append("")

            for col in [
                "row_id",
                "case_id",
                "fact_id",
                "variant_id",
                "variant_source",
                "pair_type",
                "is_correct",
                "subject",
                "relation_id",
                "correct_answer",
                "target_true",
                "target_new",
                "generated_answer",
                "strict_answer_segment",
                "strict_matched_answer",
            ]:
                if col in row and pd.notna(row[col]):
                    value = str(row[col]).replace("\n", " ")
                    lines.append(f"- **{col}:** {value}")

            if "prompt" in row and pd.notna(row["prompt"]):
                prompt = str(row["prompt"]).replace("\n", " ")
                lines.append("")
                lines.append("**Prompt:**")
                lines.append("")
                lines.append(f"> {prompt}")

            lines.append("")

        lines.append("")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source",
        choices=["correct_vs_wrong", "switching"],
        default="correct_vs_wrong",
        help="Which top-feature table to use.",
    )

    parser.add_argument(
        "--layers",
        default="12,15,18",
        help="Comma-separated layers to inspect.",
    )

    parser.add_argument(
        "--top-n-features",
        type=int,
        default=5,
        help="How many features per layer to inspect.",
    )

    parser.add_argument(
        "--top-k-prompts",
        type=int,
        default=10,
        help="How many top activating prompts per feature.",
    )

    parser.add_argument(
        "--manual",
        default="",
        help="Optional manual feature list like 12:505,15:2034.",
    )

    parser.add_argument(
        "--direction",
        choices=["more_correct", "more_wrong", "both"],
        default="more_correct",
        help="Which feature direction to inspect when using top-feature tables.",
    )

    parser.add_argument(
        "--output-prefix",
        default="feature_activation_examples",
    )

    args = parser.parse_args()

    layers = parse_layers(args.layers)
    manual_features = parse_manual_features(args.manual)

    if not os.path.exists(ACTIVE_FEATURES_PATH):
        raise FileNotFoundError(
            f"Missing active features file: {ACTIVE_FEATURES_PATH}\n"
            "This file is expected in outputs/ and is not committed to git."
        )

    if not os.path.exists(PROMPT_OUTPUTS_PATH):
        raise FileNotFoundError(
            f"Missing prompt outputs file: {PROMPT_OUTPUTS_PATH}"
        )

    print("Loading active features:", ACTIVE_FEATURES_PATH)
    active_df = pd.read_csv(ACTIVE_FEATURES_PATH)

    print("Loading prompt outputs:", PROMPT_OUTPUTS_PATH)
    prompt_df = pd.read_csv(PROMPT_OUTPUTS_PATH)

    required_active_cols = [
        "row_id",
        "fact_id",
        "variant_id",
        "layer",
        "feature_id",
        "activation",
        "is_correct",
    ]

    missing = [c for c in required_active_cols if c not in active_df.columns]
    if missing:
        raise ValueError(f"active_df is missing required columns: {missing}")

    active_df["activation"] = pd.to_numeric(active_df["activation"], errors="coerce")
    active_df["is_correct"] = active_df["is_correct"].apply(to_bool)

    merge_cols = ["fact_id", "variant_id"]

    for col in merge_cols:
        active_df[col] = active_df[col].astype(str)

    prompt_meta_df, merge_cols = prepare_prompt_metadata(prompt_df)

    if manual_features:
        feature_pairs = pd.DataFrame(
            manual_features,
            columns=["layer", "feature_id"],
        )
        top_features = feature_pairs.copy()
    else:
        top_features = load_top_features(
            source=args.source,
            layers=layers,
            top_n=args.top_n_features,
            direction=args.direction,
        )
        feature_pairs = top_features[["layer", "feature_id"]].copy()

    print()
    print("Features selected:")
    print(feature_pairs.to_string(index=False))
    print()

    all_examples = []

    for _, feat in feature_pairs.iterrows():
        layer = int(feat["layer"])
        feature_id = int(feat["feature_id"])

        sub = active_df[
            (active_df["layer"] == layer)
            & (active_df["feature_id"] == feature_id)
        ].copy()

        if len(sub) == 0:
            print(f"No activations found for L{layer} feature {feature_id}")
            continue

        is_correct_bool = sub["is_correct"].fillna(False).astype(bool)

        n_correct = int(is_correct_bool.sum())
        n_wrong = int((~is_correct_bool).sum())

        if "subject" in sub.columns:
            top_subjects = format_counts(sub["subject"], top_k=5)
        else:
            top_subjects = "N/A"

        sub_merged = sub.merge(prompt_meta_df, on=merge_cols, how="left")

        if "relation_id" in sub_merged.columns:
            top_relations = format_counts(sub_merged["relation_id"], top_k=5)
        else:
            top_relations = "N/A"

        top_prompts = (
            sub_merged
            .sort_values("activation", ascending=False)
            .head(args.top_k_prompts)
            .copy()
        )

        top_prompts["inspected_layer"] = layer
        top_prompts["inspected_feature_id"] = feature_id
        top_prompts["prompt_rank"] = range(1, len(top_prompts) + 1)

        feature_info = top_features[
            (top_features["layer"] == layer)
            & (top_features["feature_id"] == feature_id)
        ]

        if len(feature_info) > 0:
            info = feature_info.iloc[0]

            if (
                "fraction_diff_correct_minus_wrong" in info
                and pd.notna(info["fraction_diff_correct_minus_wrong"])
            ):
                top_prompts["feature_fraction_diff_correct_minus_wrong"] = round(
                    float(info["fraction_diff_correct_minus_wrong"]),
                    4,
                )

            if (
                "active_fraction_correct" in info
                and pd.notna(info["active_fraction_correct"])
            ):
                top_prompts["feature_active_fraction_correct"] = round(
                    float(info["active_fraction_correct"]),
                    4,
                )

            if (
                "active_fraction_wrong" in info
                and pd.notna(info["active_fraction_wrong"])
            ):
                top_prompts["feature_active_fraction_wrong"] = round(
                    float(info["active_fraction_wrong"]),
                    4,
                )

            if (
                "total_active_count" in info
                and pd.notna(info["total_active_count"])
            ):
                top_prompts["feature_total_active_count"] = int(
                    info["total_active_count"]
                )

        top_prompts["n_correct_activations_in_dataset"] = n_correct
        top_prompts["n_wrong_activations_in_dataset"] = n_wrong
        top_prompts["top_relations"] = top_relations
        top_prompts["top_subjects"] = top_subjects
        top_prompts["analysis_source"] = args.source
        top_prompts["analysis_direction"] = args.direction

        all_examples.append(top_prompts)

        print(
            f"L{layer} feature {feature_id}: "
            f"{len(sub)} activations, "
            f"correct={n_correct}, wrong={n_wrong}, "
            f"top_relations={top_relations}"
        )

    if not all_examples:
        raise RuntimeError("No examples found.")

    examples_df = pd.concat(all_examples, ignore_index=True)

    preferred_cols = [
        "inspected_layer",
        "inspected_feature_id",
        "layer",
        "feature_id",
        "activation",
        "prompt_rank",
        "row_id",
        "case_id",
        "fact_id",
        "variant_id",
        "variant_source",
        "pair_type",
        "is_correct",
        "subject",
        "relation_id",
        "correct_answer",
        "target_true",
        "target_new",
        "generated_answer",
        "strict_answer_segment",
        "strict_matched_answer",
        "prompt",
        "template",
        "base_prompt",
        "feature_fraction_diff_correct_minus_wrong",
        "feature_active_fraction_correct",
        "feature_active_fraction_wrong",
        "feature_total_active_count",
        "n_correct_activations_in_dataset",
        "n_wrong_activations_in_dataset",
        "top_relations",
        "top_subjects",
        "analysis_source",
        "analysis_direction",
    ]

    ordered_cols = safe_cols(examples_df, preferred_cols)
    remaining_cols = [c for c in examples_df.columns if c not in ordered_cols]
    examples_df = examples_df[ordered_cols + remaining_cols]

    out_csv = f"{REPORTS_DIR}/{args.output_prefix}_{EXPERIMENT_NAME}.csv"
    out_md = f"{REPORTS_DIR}/{args.output_prefix}_{EXPERIMENT_NAME}.md"

    examples_df.to_csv(out_csv, index=False)
    write_markdown(out_md, examples_df)

    print()
    print("Saved CSV:", out_csv)
    print("Saved Markdown:", out_md)
    print("Rows:", len(examples_df))


if __name__ == "__main__":
    main()
