import argparse
import os
import pandas as pd
from datasets import load_dataset


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", default="test", choices=["train", "test"])
    parser.add_argument("--max-facts", type=int, default=None)
    parser.add_argument(
        "--output",
        default=f"data/counterfact/counterfact_paraphrase_prompts_{EXPERIMENT_NAME}.csv",
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    ds = load_dataset("azhx/counterfact")
    data = ds[args.split]

    if args.max_facts is not None:
        data = data.select(range(min(args.max_facts, len(data))))

    rows = []
    skipped_prompts = 0
    facts_with_one_prompt = []

    for ex in data:
        rr = ex["requested_rewrite"]

        case_id = ex["case_id"]
        subject = rr["subject"]
        relation_id = rr["relation_id"]
        template = rr["prompt"]

        # Use replace instead of .format() to avoid crashes if templates contain extra curly braces.
        base_prompt = template.replace("{}", subject, 1)

        target_true = rr["target_true"]["str"]
        target_new = rr["target_new"]["str"]

        paraphrase_prompts = ex["paraphrase_prompts"]

        kept = 0
        for prompt in paraphrase_prompts:
            if prompt is None:
                skipped_prompts += 1
                continue

            prompt = str(prompt).strip()

            if not prompt:
                skipped_prompts += 1
                continue

            rows.append(
                {
                    "fact_id": f"cf_{case_id}",
                    "case_id": case_id,
                    "split": args.split,
                    "relation_id": relation_id,
                    "subject": subject,
                    "template": template,
                    "base_prompt": base_prompt,
                    "variant_id": f"paraphrase_{kept:02d}",
                    "variant_source": "paraphrase_prompts",
                    "prompt": prompt,
                    "correct_answer": target_true,
                    "target_true": target_true,
                    "target_new": target_new,
                }
            )
            kept += 1

        if kept == 1:
            facts_with_one_prompt.append(f"cf_{case_id}")

    df = pd.DataFrame(rows)

    if len(df) == 0:
        raise ValueError("No paraphrase prompts were extracted. Something is wrong.")

    df.to_csv(args.output, index=False)

    print("Saved:", args.output)
    print("Split:", args.split)
    print("Facts:", df["fact_id"].nunique())
    print("Rows:", len(df))
    print("Average prompts per fact:", round(len(df) / df["fact_id"].nunique(), 3))
    print("Skipped prompts (None or empty):", skipped_prompts)
    print(f"Facts with only 1 valid prompt (cannot switch): {len(facts_with_one_prompt)}")
    if facts_with_one_prompt:
        print("  Examples:", facts_with_one_prompt[:5])
    print("Variant ID examples:", sorted(df["variant_id"].unique())[:10])
    print()
    print(df.head(15).to_string(index=False))


if __name__ == "__main__":
    main()
