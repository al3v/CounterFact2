"""
Create small readable Markdown previews for:

1. The prompts passed to Gemma.
2. The outputs produced by run_counterfact_gemma3.py.

This is only for human inspection / documentation.
It does not affect the experiment results.
"""

import argparse
import os
import pandas as pd


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"

INPUT_PROMPTS_PATH = (
    f"data/counterfact/"
    f"counterfact_paraphrase_prompts_{EXPERIMENT_NAME}.csv"
)

PROMPT_OUTPUTS_PATH = (
    f"reports/{EXPERIMENT_NAME}/"
    f"prompt_outputs_{EXPERIMENT_NAME}.csv"
)

READABLE_DIR = f"reports/{EXPERIMENT_NAME}/readable_tables"


def clean_text(x):
    if pd.isna(x):
        return ""
    return str(x).replace("\n", " ").strip()


def write_input_prompt_preview(df, out_path, n_facts):
    lines = []
    lines.append("# Input prompts passed to Gemma")
    lines.append("")
    lines.append(
        "This file shows a small readable preview of the CounterFact paraphrase prompts "
        "that are passed to Gemma 3."
    )
    lines.append("")

    shown_facts = df["fact_id"].drop_duplicates().head(n_facts).tolist()
    preview = df[df["fact_id"].isin(shown_facts)].copy()

    for fact_id, group in preview.groupby("fact_id", sort=False):
        first = group.iloc[0]

        lines.append(f"## Fact: {fact_id}")
        lines.append("")
        lines.append(f"- **case_id:** {first.get('case_id', '')}")
        lines.append(f"- **relation_id:** {first.get('relation_id', '')}")
        lines.append(f"- **subject:** {first.get('subject', '')}")
        lines.append(f"- **correct_answer:** {first.get('correct_answer', '')}")
        lines.append(f"- **target_new:** {first.get('target_new', '')}")
        lines.append(f"- **base_prompt:** {clean_text(first.get('base_prompt', ''))}")
        lines.append("")

        for _, row in group.iterrows():
            lines.append(f"### {row.get('variant_id', '')}")
            lines.append("")
            lines.append(f"- **variant_source:** {row.get('variant_source', '')}")
            lines.append("")
            lines.append("**Prompt passed to Gemma:**")
            lines.append("")
            lines.append(f"> {clean_text(row.get('prompt', ''))}")
            lines.append("")

        lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_gemma_output_preview(df, out_path, n_facts):
    lines = []
    lines.append("# Gemma generation output preview")
    lines.append("")
    lines.append(
        "This file shows a small readable preview of Gemma 3 outputs and the strict "
        "correctness labels produced by run_counterfact_gemma3.py."
    )
    lines.append("")

    shown_facts = df["fact_id"].drop_duplicates().head(n_facts).tolist()
    preview = df[df["fact_id"].isin(shown_facts)].copy()

    for fact_id, group in preview.groupby("fact_id", sort=False):
        first = group.iloc[0]

        lines.append(f"## Fact: {fact_id}")
        lines.append("")
        lines.append(f"- **case_id:** {first.get('case_id', '')}")
        lines.append(f"- **relation_id:** {first.get('relation_id', '')}")
        lines.append(f"- **subject:** {first.get('subject', '')}")
        lines.append(f"- **correct_answer:** {first.get('correct_answer', '')}")
        lines.append(f"- **target_new:** {first.get('target_new', '')}")
        lines.append("")

        for _, row in group.iterrows():
            lines.append(f"### {row.get('variant_id', '')}")
            lines.append("")
            lines.append(f"- **is_correct:** {row.get('is_correct', '')}")
            matched = clean_text(row.get("strict_matched_answer", "")) or "N/A"
            lines.append(f"- **strict_matched_answer:** {matched}")
            lines.append("")
            lines.append("**Prompt:**")
            lines.append("")
            lines.append(f"> {clean_text(row.get('prompt', ''))}")
            lines.append("")
            lines.append("**Gemma generated answer:**")
            lines.append("")
            lines.append(f"> {clean_text(row.get('generated_answer', ''))}")
            lines.append("")
            lines.append("**Strict answer segment used for grading:**")
            lines.append("")
            lines.append(f"> {clean_text(row.get('strict_answer_segment', ''))}")
            lines.append("")

        lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-facts", type=int, default=10)
    parser.add_argument("--input-prompts", default=INPUT_PROMPTS_PATH)
    parser.add_argument("--prompt-outputs", default=PROMPT_OUTPUTS_PATH)
    args = parser.parse_args()

    os.makedirs(READABLE_DIR, exist_ok=True)

    input_df = pd.read_csv(args.input_prompts)
    output_df = pd.read_csv(args.prompt_outputs)

    input_out = f"{READABLE_DIR}/input_prompts_readable_preview.md"
    output_out = f"{READABLE_DIR}/gemma_outputs_readable_preview.md"

    write_input_prompt_preview(input_df, input_out, args.n_facts)
    write_gemma_output_preview(output_df, output_out, args.n_facts)

    print("Saved:", input_out)
    print("Saved:", output_out)
    print("Facts shown:", args.n_facts)


if __name__ == "__main__":
    main()
