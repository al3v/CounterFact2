from __future__ import annotations

from pathlib import Path

import pandas as pd

from adl_sae.config import ExperimentConfig


def to_bool(x) -> bool:
    if isinstance(x, bool):
        return x
    if pd.isna(x):
        return False
    return str(x).strip().lower() in {"true", "1", "yes"}


class GenericSAEFeatureAnalysis:
    def __init__(self, config: ExperimentConfig) -> None:
        self.config = config

    @property
    def active_features_path(self) -> Path:
        return Path(self.config.sae_active_features_path)

    @property
    def prompt_summary_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"sae_prompt_summary_{self.config.experiment_name}.csv"
        )

    @property
    def prompt_group_stats_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"sae_prompt_group_stats_{self.config.experiment_name}.csv"
        )

    @property
    def switching_stats_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"sae_switching_correct_vs_wrong_stats_{self.config.experiment_name}.csv"
        )

    @property
    def top_correct_wrong_features_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"sae_top_correct_vs_wrong_features_{self.config.experiment_name}.csv"
        )

    @property
    def top_switching_features_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"sae_top_switching_features_{self.config.experiment_name}.csv"
        )

    def run(self):
        if not self.active_features_path.exists():
            raise FileNotFoundError(f"Active features not found: {self.active_features_path}")

        if not self.prompt_summary_path.exists():
            raise FileNotFoundError(f"Prompt summary not found: {self.prompt_summary_path}")

        active = pd.read_csv(self.active_features_path)
        prompt_summary = pd.read_csv(self.prompt_summary_path)

        required_prompt_cols = {
            "layer",
            "row_id",
            "pair_type",
            "is_correct",
            "n_active_features",
            "sum_activation",
            "max_activation",
            "mean_activation",
        }

        missing_prompt = required_prompt_cols - set(prompt_summary.columns)
        if missing_prompt:
            raise ValueError(f"Prompt summary missing columns: {sorted(missing_prompt)}")

        required_active_cols = {
            "layer",
            "row_id",
            "feature_id",
            "activation",
            "pair_type",
            "is_correct",
        }

        missing_active = required_active_cols - set(active.columns)
        if missing_active:
            raise ValueError(f"Active features missing columns: {sorted(missing_active)}")

        prompt_summary["is_correct_bool"] = prompt_summary["is_correct"].map(to_bool)
        active["is_correct_bool"] = active["is_correct"].map(to_bool)

        print("=== Generic SAE feature analysis ===")
        print("Experiment:", self.config.experiment_name)
        print("Active features:", self.active_features_path)
        print("Prompt summary:", self.prompt_summary_path)
        print("Active rows:", len(active))
        print("Prompt summary rows:", len(prompt_summary))

        prompt_group_stats = (
            prompt_summary.groupby(["layer", "pair_type", "is_correct_bool"])
            .agg(
                n_rows=("row_id", "count"),
                mean_active_features=("n_active_features", "mean"),
                std_active_features=("n_active_features", "std"),
                mean_sum_activation=("sum_activation", "mean"),
                std_sum_activation=("sum_activation", "std"),
                mean_max_activation=("max_activation", "mean"),
                std_max_activation=("max_activation", "std"),
                mean_activation=("mean_activation", "mean"),
            )
            .reset_index()
        )

        switching = prompt_summary[prompt_summary["pair_type"] == "correct_wrong"].copy()

        switching_stats = (
            switching.groupby(["layer", "is_correct_bool"])
            .agg(
                n_rows=("row_id", "count"),
                mean_active_features=("n_active_features", "mean"),
                std_active_features=("n_active_features", "std"),
                mean_sum_activation=("sum_activation", "mean"),
                std_sum_activation=("sum_activation", "std"),
                mean_max_activation=("max_activation", "mean"),
                std_max_activation=("max_activation", "std"),
            )
            .reset_index()
        )

        layer_correct_counts = (
            prompt_summary.groupby(["layer", "is_correct_bool"])["row_id"]
            .nunique()
            .reset_index(name="n_prompts")
        )

        feature_counts = (
            active.groupby(["layer", "feature_id", "is_correct_bool"])
            .agg(
                active_count=("row_id", "nunique"),
                total_activation=("activation", "sum"),
                mean_activation_when_active=("activation", "mean"),
                max_activation=("activation", "max"),
            )
            .reset_index()
        )

        feature_counts = feature_counts.merge(
            layer_correct_counts,
            on=["layer", "is_correct_bool"],
            how="left",
        )

        feature_counts["active_fraction"] = (
            feature_counts["active_count"] / feature_counts["n_prompts"]
        )

        pivot = feature_counts.pivot_table(
            index=["layer", "feature_id"],
            columns="is_correct_bool",
            values=["active_count", "active_fraction", "total_activation"],
            fill_value=0,
        )

        pivot.columns = [
            f"{metric}_{'correct' if is_correct else 'wrong'}"
            for metric, is_correct in pivot.columns
        ]
        pivot = pivot.reset_index()

        for col in [
            "active_count_correct",
            "active_count_wrong",
            "active_fraction_correct",
            "active_fraction_wrong",
            "total_activation_correct",
            "total_activation_wrong",
        ]:
            if col not in pivot.columns:
                pivot[col] = 0

        pivot["fraction_diff_correct_minus_wrong"] = (
            pivot["active_fraction_correct"] - pivot["active_fraction_wrong"]
        )
        pivot["abs_fraction_diff"] = pivot["fraction_diff_correct_minus_wrong"].abs()
        pivot["direction"] = pivot["fraction_diff_correct_minus_wrong"].apply(
            lambda x: "more_correct" if x > 0 else ("more_wrong" if x < 0 else "equal")
        )

        top_correct_wrong = (
            pivot.sort_values(["abs_fraction_diff"], ascending=False)
            .head(200)
            .reset_index(drop=True)
        )

        switching_active = active[active["pair_type"] == "correct_wrong"].copy()

        if len(switching_active) > 0:
            switching_feature_counts = (
                switching_active.groupby(["layer", "feature_id", "is_correct_bool"])
                .agg(
                    active_count=("row_id", "nunique"),
                    total_activation=("activation", "sum"),
                    mean_activation_when_active=("activation", "mean"),
                    max_activation=("activation", "max"),
                )
                .reset_index()
            )

            switching_prompt_counts = (
                switching.groupby(["layer", "is_correct_bool"])["row_id"]
                .nunique()
                .reset_index(name="n_prompts")
            )

            switching_feature_counts = switching_feature_counts.merge(
                switching_prompt_counts,
                on=["layer", "is_correct_bool"],
                how="left",
            )

            switching_feature_counts["active_fraction"] = (
                switching_feature_counts["active_count"]
                / switching_feature_counts["n_prompts"]
            )

            switching_pivot = switching_feature_counts.pivot_table(
                index=["layer", "feature_id"],
                columns="is_correct_bool",
                values=["active_count", "active_fraction", "total_activation"],
                fill_value=0,
            )

            switching_pivot.columns = [
                f"{metric}_{'correct' if is_correct else 'wrong'}"
                for metric, is_correct in switching_pivot.columns
            ]
            switching_pivot = switching_pivot.reset_index()

            for col in [
                "active_count_correct",
                "active_count_wrong",
                "active_fraction_correct",
                "active_fraction_wrong",
                "total_activation_correct",
                "total_activation_wrong",
            ]:
                if col not in switching_pivot.columns:
                    switching_pivot[col] = 0

            switching_pivot["fraction_diff_correct_minus_wrong"] = (
                switching_pivot["active_fraction_correct"]
                - switching_pivot["active_fraction_wrong"]
            )
            switching_pivot["abs_fraction_diff"] = switching_pivot[
                "fraction_diff_correct_minus_wrong"
            ].abs()
            switching_pivot["direction"] = switching_pivot[
                "fraction_diff_correct_minus_wrong"
            ].apply(
                lambda x: "more_correct" if x > 0 else ("more_wrong" if x < 0 else "equal")
            )

            top_switching = (
                switching_pivot.sort_values(["abs_fraction_diff"], ascending=False)
                .head(200)
                .reset_index(drop=True)
            )
        else:
            top_switching = pd.DataFrame()

        self.prompt_group_stats_path.parent.mkdir(parents=True, exist_ok=True)

        prompt_group_stats.to_csv(self.prompt_group_stats_path, index=False)
        switching_stats.to_csv(self.switching_stats_path, index=False)
        top_correct_wrong.to_csv(self.top_correct_wrong_features_path, index=False)
        top_switching.to_csv(self.top_switching_features_path, index=False)

        print()
        print("Saved prompt group stats:", self.prompt_group_stats_path)
        print("Saved switching stats:", self.switching_stats_path)
        print("Saved top correct/wrong features:", self.top_correct_wrong_features_path)
        print("Saved top switching features:", self.top_switching_features_path)
        print()
        print("Switching stats:")
        print(switching_stats)

        return {
            "prompt_group_stats": self.prompt_group_stats_path,
            "switching_stats": self.switching_stats_path,
            "top_correct_wrong": self.top_correct_wrong_features_path,
            "top_switching": self.top_switching_features_path,
        }
