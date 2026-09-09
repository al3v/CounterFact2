from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from adl_sae.config_registry import add_config_argument, get_config


def get_first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str:
    for col in candidates:
        if col in df.columns:
            return col
    raise KeyError(f"None of these columns exist: {candidates}")


def join_prompt_and_answer(prompt: str, answer: str) -> tuple[str, str, bool]:
    """
    Build the continuation text.

    We keep the raw answer separately, but for scoring we usually need a
    leading space if the prompt does not already end with whitespace and
    the answer does not already begin with whitespace.
    """
    prompt = "" if pd.isna(prompt) else str(prompt)
    answer = "" if pd.isna(answer) else str(answer)

    added_space = False

    if prompt and answer and (not prompt[-1].isspace()) and (not answer[0].isspace()):
        answer_for_scoring = " " + answer
        added_space = True
    else:
        answer_for_scoring = answer

    full_text = prompt + answer_for_scoring

    return full_text, answer_for_scoring, added_space


def main():
    parser = argparse.ArgumentParser(
        description="Create prompt+answer rows for true/counterfactual answer scoring."
    )
    add_config_argument(parser)
    parser.add_argument(
        "--input-path",
        default=None,
        help="Optional input CSV. Defaults to all_facts_pair_types for the config.",
    )
    parser.add_argument(
        "--output-path",
        default=None,
        help="Optional output CSV path.",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional limit on prompt rows before expanding to true/counterfactual answers.",
    )
    args = parser.parse_args()

    config = get_config(args.config)

    if args.input_path is not None:
        input_path = Path(args.input_path)
    else:
        input_path = Path(config.all_pair_types_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input prompt table not found: {input_path}")

    if args.output_path is not None:
        output_path = Path(args.output_path)
    else:
        output_path = Path(config.outputs_dir) / (
            f"answer_augmented_prompts_{config.experiment_name}.csv"
        )

    df = pd.read_csv(input_path)

    if args.max_rows is not None:
        df = df.head(args.max_rows).copy()

    prompt_col = get_first_existing_column(
        df,
        ["prompt", "prompt_given_to_model", "base_prompt", "template"],
    )

    true_col = get_first_existing_column(
        df,
        ["target_true", "correct_answer", "answer"],
    )

    counterfactual_col = get_first_existing_column(
        df,
        ["target_new", "counterfactual_answer", "target_false"],
    )

    rows = []

    for idx, row in df.iterrows():
        prompt = row[prompt_col]
        true_answer = row[true_col]
        counterfactual_answer = row[counterfactual_col]

        base_meta = row.to_dict()

        for answer_type, answer in [
            ("true", true_answer),
            ("counterfactual", counterfactual_answer),
        ]:
            full_text, answer_for_scoring, added_space = join_prompt_and_answer(
                prompt=prompt,
                answer=answer,
            )

            out = dict(base_meta)

            original_row_id = out.get("row_id", idx)

            out.update(
                {
                    "original_row_id": original_row_id,
                    "extended_id": f"{original_row_id}__{answer_type}",
                    "answer_type": answer_type,
                    "prompt_text": str(prompt),
                    "raw_answer_text": "" if pd.isna(answer) else str(answer),
                    "answer_text_for_scoring": answer_for_scoring,
                    "full_text": full_text,
                    "added_space_before_answer": added_space,
                    "source_experiment_name": config.experiment_name,
                }
            )

            rows.append(out)

    out_df = pd.DataFrame(rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output_path, index=False)

    print("=== Answer-augmented prompt dataset ===")
    print("Experiment:", config.experiment_name)
    print("Input:", input_path)
    print("Prompt rows:", len(df))
    print("Output rows:", len(out_df))
    print("Output:", output_path)
    print()
    print("Answer type counts:")
    print(out_df["answer_type"].value_counts())
    print()
    print("Preview:")
    preview_cols = [
        "extended_id",
        "fact_id",
        "variant_id",
        "answer_type",
        "prompt_text",
        "answer_text_for_scoring",
        "full_text",
    ]
    preview_cols = [c for c in preview_cols if c in out_df.columns]
    print(out_df[preview_cols].head(8).to_string(index=False))


if __name__ == "__main__":
    main()
