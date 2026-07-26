import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
from scipy.stats import mannwhitneyu


def to_bool(x):
    if isinstance(x, float) and x != x:
        return False
    if isinstance(x, bool):
        return x
    return str(x).lower() in ["true", "1", "yes"]


def jaccard_distance(set_a, set_b):
    """
    Jaccard distance on sets of active SAE feature ids.

    0 means identical active feature sets.
    Larger values mean less overlap.
    """
    union = set_a | set_b

    if len(union) == 0:
        return 0.0

    intersection = set_a & set_b
    return 1.0 - len(intersection) / len(union)


def build_dense_vector(feature_ids, activations, width):
    """
    Build dense SAE activation vector from sparse active feature ids.

    Example:
    feature_ids = [9020, 749]
    activations = [31.2, 8.7]

    creates a vector where:
    vec[9020] = 31.2
    vec[749] = 8.7
    all other entries are 0
    """
    vec = np.zeros(width, dtype=np.float32)

    for fid, act in zip(feature_ids, activations):
        vec[int(fid)] = float(act)

    return vec


@dataclass
class PairDistanceAnalyzer:
    experiment_name: str
    reports_dir: str
    sae_width: int = 16384

    def active_features_path(self):
        return f"outputs/sae_active_features_{self.experiment_name}.csv"

    def prompt_summary_path(self):
        return f"{self.reports_dir}/sae_prompt_summary_{self.experiment_name}.csv"

    def out_pair_distances_path(self):
        return f"{self.reports_dir}/sae_pair_distances_{self.experiment_name}.csv"

    def out_layer_summary_path(self):
        return f"{self.reports_dir}/sae_pair_distance_summary_{self.experiment_name}.csv"

    def out_stats_path(self):
        return f"{self.reports_dir}/sae_pair_distance_mannwhitney_{self.experiment_name}.csv"

    def load_data(self):
        print("Loading data...")

        active_df = pd.read_csv(self.active_features_path())
        prompt_df = pd.read_csv(self.prompt_summary_path())

        prompt_df["is_correct"] = prompt_df["is_correct"].apply(to_bool)
        active_df["is_correct"] = active_df["is_correct"].apply(to_bool)

        print("Active feature rows:", len(active_df))
        print("Prompt summary rows:", len(prompt_df))
        print("Layers:", sorted(active_df["layer"].unique()))
        print()

        return active_df, prompt_df

    def build_sparse_lookup(self, active_df):
        """
        Build lookup:

        (row_id, layer) -> (feature_ids, activations)

        This lets us quickly get the SAE activations for a prompt row
        at a specific layer.
        """
        print("Building sparse feature lookup...")

        lookup = {}

        for (row_id, layer), grp in active_df.groupby(["row_id", "layer"]):
            lookup[(row_id, layer)] = (
                grp["feature_id"].tolist(),
                grp["activation"].tolist(),
            )

        return lookup

    def compute_pairwise_distances(self, prompt_df, lookup):
        """
        For each fact and layer, compare the two paraphrases:

        paraphrase_00 SAE vector vs paraphrase_01 SAE vector
        """
        meta = (
            prompt_df[
                [
                    "fact_id",
                    "row_id",
                    "layer",
                    "variant_id",
                    "pair_type",
                    "is_correct",
                ]
            ]
            .drop_duplicates()
        )

        pair_records = []

        print("Computing pairwise distances...")

        for (fact_id, layer), grp in meta.groupby(["fact_id", "layer"]):
            grp = grp.sort_values("variant_id").reset_index(drop=True)

            if len(grp) != 2:
                continue

            row_a = grp.iloc[0]
            row_b = grp.iloc[1]

            ids_a, acts_a = lookup.get((row_a["row_id"], layer), ([], []))
            ids_b, acts_b = lookup.get((row_b["row_id"], layer), ([], []))

            set_a = set(ids_a)
            set_b = set(ids_b)

            jacc = jaccard_distance(set_a, set_b)

            vec_a = build_dense_vector(ids_a, acts_a, width=self.sae_width)
            vec_b = build_dense_vector(ids_b, acts_b, width=self.sae_width)

            if np.linalg.norm(vec_a) == 0 or np.linalg.norm(vec_b) == 0:
                cos_dist = 1.0
            else:
                cos_dist = float(cosine(vec_a, vec_b))

            l2_dist = float(np.linalg.norm(vec_a - vec_b))

            pair_records.append(
                {
                    "fact_id": fact_id,
                    "layer": layer,
                    "pair_type": row_a["pair_type"],
                    "variant_id_a": row_a["variant_id"],
                    "variant_id_b": row_b["variant_id"],
                    "is_correct_a": row_a["is_correct"],
                    "is_correct_b": row_b["is_correct"],
                    "cosine_distance": cos_dist,
                    "l2_distance": l2_dist,
                    "jaccard_distance": jacc,
                    "n_active_a": len(ids_a),
                    "n_active_b": len(ids_b),
                    "n_shared_features": len(set_a & set_b),
                }
            )

        pair_df = pd.DataFrame(pair_records)
        return pair_df

    def summarize_by_layer(self, pair_df):
        summary_df = (
            pair_df.groupby(["layer", "pair_type"])
            .agg(
                n_pairs=("fact_id", "count"),
                mean_cosine=("cosine_distance", "mean"),
                std_cosine=("cosine_distance", "std"),
                mean_l2=("l2_distance", "mean"),
                std_l2=("l2_distance", "std"),
                mean_jaccard=("jaccard_distance", "mean"),
                std_jaccard=("jaccard_distance", "std"),
                mean_shared=("n_shared_features", "mean"),
            )
            .reset_index()
            .sort_values(["layer", "pair_type"])
        )

        return summary_df

    def run_mannwhitney_tests(self, pair_df):
        """
        Statistical comparison between pair types.

        This does not compute the distances.
        It only checks whether the distance distributions differ.
        """
        records = []

        comparisons = [
            ("correct_wrong", "wrong_wrong"),
            ("correct_wrong", "correct_correct"),
        ]

        metrics = [
            "cosine_distance",
            "jaccard_distance",
            "l2_distance",
        ]

        for layer in sorted(pair_df["layer"].unique()):
            sub = pair_df[pair_df["layer"] == layer]

            for group_a, group_b in comparisons:
                for metric in metrics:
                    values_a = sub[sub["pair_type"] == group_a][metric].dropna()
                    values_b = sub[sub["pair_type"] == group_b][metric].dropna()

                    if len(values_a) < 5 or len(values_b) < 5:
                        continue

                    stat, p_value = mannwhitneyu(
                        values_a,
                        values_b,
                        alternative="two-sided",
                    )

                    records.append(
                        {
                            "layer": layer,
                            "comparison": f"{group_a}_vs_{group_b}",
                            "metric": metric,
                            "group_a": group_a,
                            "group_b": group_b,
                            "mean_a": values_a.mean(),
                            "mean_b": values_b.mean(),
                            "u_stat": stat,
                            "p_value": p_value,
                            "significant_p_lt_0_05": p_value < 0.05,
                            "n_a": len(values_a),
                            "n_b": len(values_b),
                        }
                    )

        return pd.DataFrame(records)

    def save_outputs(self, pair_df, summary_df, stats_df):
        os.makedirs(self.reports_dir, exist_ok=True)

        pair_df.to_csv(self.out_pair_distances_path(), index=False)
        summary_df.to_csv(self.out_layer_summary_path(), index=False)
        stats_df.to_csv(self.out_stats_path(), index=False)

        print("Saved:")
        print(self.out_pair_distances_path())
        print(self.out_layer_summary_path())
        print(self.out_stats_path())

    def run(self):
        active_df, prompt_df = self.load_data()
        lookup = self.build_sparse_lookup(active_df)

        pair_df = self.compute_pairwise_distances(prompt_df, lookup)
        summary_df = self.summarize_by_layer(pair_df)
        stats_df = self.run_mannwhitney_tests(pair_df)

        self.save_outputs(pair_df, summary_df, stats_df)

        print()
        print("=== Pairwise distance summary by layer and pair_type ===")
        print(summary_df.to_string(index=False))

        print()
        print("=== Mann-Whitney U tests ===")
        print(stats_df.to_string(index=False))

        return pair_df, summary_df, stats_df
