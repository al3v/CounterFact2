import argparse
import os
import shutil
import pandas as pd


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"


def to_bool(x):
    if isinstance(x, float) and x != x:
        return False
    if isinstance(x, bool):
        return x
    return str(x).lower() in ["true", "1", "yes"]


def get_pair_type(correctness_list):
    """
    Given correctness labels for all paraphrases of one fact,
    return the fact-level correctness type.

    correct_correct = all paraphrases correct
    wrong_wrong     = all paraphrases wrong
    correct_wrong   = mixed correctness
    """
    s = set(correctness_list)

    if s == {True}:
        return "correct_correct"
    elif s == {False}:
        return "wrong_wrong"
    else:
        return "correct_wrong"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=f"outputs/prompt_outputs_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument(
        "--output",
        default=f"outputs/switching_facts_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument(
        "--all-pairs-output",
        default=f"outputs/all_facts_pair_types_{EXPERIMENT_NAME}.csv",
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(os.path.dirname(args.all_pairs_output), exist_ok=True)

    df = pd.read_csv(args.input)
    df["is_correct"] = df["is_correct"].apply(to_bool)

    pair_type_records = []

    for fact_id, group in df.groupby("fact_id"):
        correctness_list = group["is_correct"].tolist()
        pair_type = get_pair_type(correctness_list)

        pair_type_records.append(
            {
                "fact_id": fact_id,
                "pair_type": pair_type,
                "n_variants": len(correctness_list),
                "n_correct": int(sum(correctness_list)),
                "n_wrong": int(sum(not c for c in correctness_list)),
            }
        )

    pair_type_df = pd.DataFrame(pair_type_records)

    df = df.merge(
        pair_type_df[["fact_id", "pair_type"]],
        on="fact_id",
        how="left",
    )

    pair_type_df.to_csv(args.all_pairs_output, index=False)

    switching_df = df[df["pair_type"] == "correct_wrong"].copy()
    switching_df.to_csv(args.output, index=False)

    total_facts = df["fact_id"].nunique()
    counts = pair_type_df["pair_type"].value_counts()

    print("Saved switching facts:", args.output)
    print("Saved all-facts pair types:", args.all_pairs_output)
    print()
    print("Total rows:", len(df))
    print("Total facts:", total_facts)
    print("Correct rows:", int(df["is_correct"].sum()))
    print("Wrong rows:", int((~df["is_correct"]).sum()))
    print()
    print("=== Pair Type Breakdown ===")

    for pt in ["correct_correct", "correct_wrong", "wrong_wrong"]:
        n = int(counts.get(pt, 0))
        pct = round(n / total_facts * 100, 1)
        print(f"  {pt:<20}: {n:>5} facts  ({pct}%)")

    print()
    print("Switching facts:", switching_df["fact_id"].nunique())
    print("Switching rows:", len(switching_df))

    if len(switching_df) > 0:
        print()
        print(
            switching_df[
                [
                    "fact_id",
                    "variant_id",
                    "subject",
                    "correct_answer",
                    "target_new",
                    "generated_answer",
                    "is_correct",
                    "pair_type",
                ]
            ]
            .head(20)
            .to_string(index=False)
        )

    os.makedirs(REPORTS_DIR, exist_ok=True)

    for src in [args.output, args.all_pairs_output]:
        dst = os.path.join(REPORTS_DIR, os.path.basename(src))
        shutil.copy2(src, dst)
        print("Copied to reports:", dst)


if __name__ == "__main__":
    main()
