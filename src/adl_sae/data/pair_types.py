import os
from dataclasses import dataclass

import pandas as pd


def to_bool(x):
    if isinstance(x, float) and x != x:
        return False
    if isinstance(x, bool):
        return x
    return str(x).lower() in ["true", "1", "yes"]


def assign_pair_type(correct_values):
    """
    Assign pair type for the two paraphrases of the same fact.

    correct_correct: both paraphrases correct
    wrong_wrong: both paraphrases wrong
    correct_wrong: one correct and one wrong
    """
    n_correct = sum(correct_values)

    if n_correct == 2:
        return "correct_correct"

    if n_correct == 0:
        return "wrong_wrong"

    return "correct_wrong"


@dataclass
class CounterFactPairTypeBuilder:
    experiment_name: str
    reports_dir: str

    def prompt_outputs_path(self):
        return f"outputs/prompt_outputs_{self.experiment_name}.csv"

    def out_all_pairs_path(self):
        return f"outputs/all_facts_pair_types_{self.experiment_name}.csv"

    def out_switching_path(self):
        return f"outputs/switching_facts_{self.experiment_name}.csv"

    def report_all_pairs_path(self):
        return f"{self.reports_dir}/all_facts_pair_types_{self.experiment_name}.csv"

    def report_switching_path(self):
        return f"{self.reports_dir}/switching_facts_{self.experiment_name}.csv"

    def load_prompt_outputs(self):
        print("Loading prompt outputs...")
        df = pd.read_csv(self.prompt_outputs_path())

        if "is_correct" not in df.columns:
            raise ValueError("Expected column 'is_correct' in prompt output CSV.")

        df["is_correct"] = df["is_correct"].apply(to_bool)

        print("Prompt rows:", len(df))
        print("Facts:", df["fact_id"].nunique())
        print()

        return df

    def build_pair_types(self, df):
        """
        Add pair_type to each prompt row by grouping the two paraphrases
        belonging to the same fact.
        """
        required_cols = ["fact_id", "variant_id", "is_correct"]

        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Expected column '{col}' in prompt output CSV.")

        pair_records = []

        for fact_id, group in df.groupby("fact_id"):
            group = group.sort_values("variant_id").copy()

            if len(group) != 2:
                continue

            pair_type = assign_pair_type(group["is_correct"].tolist())
            group["pair_type"] = pair_type

            pair_records.append(group)

        if not pair_records:
            raise ValueError("No valid two-paraphrase fact pairs found.")

        pair_df = pd.concat(pair_records, ignore_index=True)

        return pair_df

    def save_outputs(self, pair_df):
        os.makedirs("outputs", exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

        switching_df = pair_df[pair_df["pair_type"] == "correct_wrong"].copy()

        pair_df.to_csv(self.out_all_pairs_path(), index=False)
        switching_df.to_csv(self.out_switching_path(), index=False)

        pair_df.to_csv(self.report_all_pairs_path(), index=False)
        switching_df.to_csv(self.report_switching_path(), index=False)

        print("Saved:")
        print(self.out_all_pairs_path())
        print(self.out_switching_path())
        print(self.report_all_pairs_path())
        print(self.report_switching_path())
        print()

        return switching_df

    def print_summary(self, pair_df, switching_df):
        fact_summary = (
            pair_df[["fact_id", "pair_type"]]
            .drop_duplicates()
            ["pair_type"]
            .value_counts()
            .rename_axis("pair_type")
            .reset_index(name="n_facts")
        )

        total_facts = fact_summary["n_facts"].sum()
        fact_summary["fraction"] = fact_summary["n_facts"] / total_facts

        print("=== Pair type summary ===")
        print(fact_summary.to_string(index=False))
        print()

        print("Switching facts:", switching_df["fact_id"].nunique())
        print("Switching rows:", len(switching_df))

    def run(self):
        df = self.load_prompt_outputs()
        pair_df = self.build_pair_types(df)
        switching_df = self.save_outputs(pair_df)
        self.print_summary(pair_df, switching_df)

        return pair_df, switching_df
