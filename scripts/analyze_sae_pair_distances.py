import os
import shutil
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
from scipy.stats import mannwhitneyu


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"
SAE_WIDTH = 16384


def to_bool(x):
    if isinstance(x, float) and x != x:
        return False
    if isinstance(x, bool):
        return x
    return str(x).lower() in ["true", "1", "yes"]


def jaccard_distance(set_a, set_b):
    """
    Jaccard distance on sets of active SAE feature ids.

    If both sets are empty, distance is 0 because the sets are identical.
    """
    union = set_a | set_b

    if len(union) == 0:
        return 0.0

    intersection = set_a & set_b
    return 1.0 - len(intersection) / len(union)


def build_dense_vector(feature_ids, activations, width=SAE_WIDTH):
    """
    Build dense SAE feature vector of shape (width,)
    from sparse active feature ids and activation values.
    """
    vec = np.zeros(width, dtype=np.float32)

    for fid, act in zip(feature_ids, activations):
        vec[int(fid)] = float(act)

    return vec


def main():
    active_features_path = f"outputs/sae_active_features_{EXPERIMENT_NAME}.csv"
    prompt_summary_path = f"{REPORTS_DIR}/sae_prompt_summary_{EXPERIMENT_NAME}.csv"

    out_pair_distances = f"{REPORTS_DIR}/sae_pair_distances_{EXPERIMENT_NAME}.csv"
    out_layer_summary = f"{REPORTS_DIR}/sae_pair_distance_summary_{EXPERIMENT_NAME}.csv"

    os.makedirs(REPORTS_DIR, exist_ok=True)

    print("Loading data...")
    active_df = pd.read_csv(active_features_path)
    prompt_df = pd.read_csv(prompt_summary_path)

    prompt_df["is_correct"] = prompt_df["is_correct"].apply(to_bool)
    active_df["is_correct"] = active_df["is_correct"].apply(to_bool)

    print("Active feature rows:", len(active_df))
    print("Prompt summary rows:", len(prompt_df))
    print("Layers:", sorted(active_df["layer"].unique()))
    print()

    # ------------------------------------------------------------
    # Build lookup: (row_id, layer) -> (feature_ids, activations)
    # ------------------------------------------------------------
    print("Building sparse feature lookup...")

    lookup = {}

    for (row_id, layer), grp in active_df.groupby(["row_id", "layer"]):
        lookup[(row_id, layer)] = (
            grp["feature_id"].tolist(),
            grp["activation"].tolist(),
        )

    # ------------------------------------------------------------
    # Pair metadata:
    # for each fact and each layer, compare the two paraphrase rows
    # ------------------------------------------------------------
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

        pair_type = row_a["pair_type"]

        ids_a, acts_a = lookup.get((row_a["row_id"], layer), ([], []))
        ids_b, acts_b = lookup.get((row_b["row_id"], layer), ([], []))

        set_a = set(ids_a)
        set_b = set(ids_b)

        jacc = jaccard_distance(set_a, set_b)

        vec_a = build_dense_vector(ids_a, acts_a)
        vec_b = build_dense_vector(ids_b, acts_b)

        if np.linalg.norm(vec_a) == 0 or np.linalg.norm(vec_b) == 0:
            cos_dist = 1.0
        else:
            cos_dist = float(cosine(vec_a, vec_b))

        l2_dist = float(np.linalg.norm(vec_a - vec_b))

        pair_records.append(
            {
                "fact_id": fact_id,
                "layer": layer,
                "pair_type": pair_type,
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
    pair_df.to_csv(out_pair_distances, index=False)

    print("Saved pair distances:", out_pair_distances)
    print("Total pairs:", len(pair_df))
    print()

    # ------------------------------------------------------------
    # Summary by layer and pair_type
    # ------------------------------------------------------------
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

    summary_df.to_csv(out_layer_summary, index=False)

    print("=== Pairwise distance summary by layer and pair_type ===")
    print(summary_df.to_string(index=False))
    print()

    # ------------------------------------------------------------
    # Statistical tests
    # ------------------------------------------------------------
    print("=== Mann-Whitney U: correct_wrong vs wrong_wrong | cosine distance ===")
    print(f"{'Layer':<8} {'CW mean':>10} {'WW mean':>10} {'U stat':>10} {'p-value':>12} {'significant':>12}")
    print("-" * 70)

    for layer in sorted(pair_df["layer"].unique()):
        sub = pair_df[pair_df["layer"] == layer]

        cw = sub[sub["pair_type"] == "correct_wrong"]["cosine_distance"].dropna()
        ww = sub[sub["pair_type"] == "wrong_wrong"]["cosine_distance"].dropna()

        if len(cw) < 5 or len(ww) < 5:
            continue

        stat, p = mannwhitneyu(cw, ww, alternative="two-sided")
        sig = "YES *" if p < 0.05 else "no"

        print(f"{layer:<8} {cw.mean():>10.4f} {ww.mean():>10.4f} {stat:>10.0f} {p:>12.4e} {sig:>12}")

    print()
    print("=== Mann-Whitney U: correct_wrong vs correct_correct | cosine distance ===")
    print(f"{'Layer':<8} {'CW mean':>10} {'CC mean':>10} {'U stat':>10} {'p-value':>12} {'significant':>12}")
    print("-" * 70)

    for layer in sorted(pair_df["layer"].unique()):
        sub = pair_df[pair_df["layer"] == layer]

        cw = sub[sub["pair_type"] == "correct_wrong"]["cosine_distance"].dropna()
        cc = sub[sub["pair_type"] == "correct_correct"]["cosine_distance"].dropna()

        if len(cw) < 5 or len(cc) < 5:
            continue

        stat, p = mannwhitneyu(cw, cc, alternative="two-sided")
        sig = "YES *" if p < 0.05 else "no"

        print(f"{layer:<8} {cw.mean():>10.4f} {cc.mean():>10.4f} {stat:>10.0f} {p:>12.4e} {sig:>12}")

    print()
    print("=== Mann-Whitney U: correct_wrong vs wrong_wrong | Jaccard distance ===")
    print(f"{'Layer':<8} {'CW mean':>10} {'WW mean':>10} {'U stat':>10} {'p-value':>12} {'significant':>12}")
    print("-" * 70)

    for layer in sorted(pair_df["layer"].unique()):
        sub = pair_df[pair_df["layer"] == layer]

        cw = sub[sub["pair_type"] == "correct_wrong"]["jaccard_distance"].dropna()
        ww = sub[sub["pair_type"] == "wrong_wrong"]["jaccard_distance"].dropna()

        if len(cw) < 5 or len(ww) < 5:
            continue

        stat, p = mannwhitneyu(cw, ww, alternative="two-sided")
        sig = "YES *" if p < 0.05 else "no"

        print(f"{layer:<8} {cw.mean():>10.4f} {ww.mean():>10.4f} {stat:>10.0f} {p:>12.4e} {sig:>12}")

    print()
    print("=== Mann-Whitney U: correct_wrong vs correct_correct | Jaccard distance ===")
    print(f"{'Layer':<8} {'CW mean':>10} {'CC mean':>10} {'U stat':>10} {'p-value':>12} {'significant':>12}")
    print("-" * 70)

    for layer in sorted(pair_df["layer"].unique()):
        sub = pair_df[pair_df["layer"] == layer]

        cw = sub[sub["pair_type"] == "correct_wrong"]["jaccard_distance"].dropna()
        cc = sub[sub["pair_type"] == "correct_correct"]["jaccard_distance"].dropna()

        if len(cw) < 5 or len(cc) < 5:
            continue

        stat, p = mannwhitneyu(cw, cc, alternative="two-sided")
        sig = "YES *" if p < 0.05 else "no"

        print(f"{layer:<8} {cw.mean():>10.4f} {cc.mean():>10.4f} {stat:>10.0f} {p:>12.4e} {sig:>12}")

    print()
    print("Saved:")
    print(out_pair_distances)
    print(out_layer_summary)

    for src in [out_pair_distances, out_layer_summary]:
        dst = os.path.join(REPORTS_DIR, os.path.basename(src))

        if os.path.abspath(src) != os.path.abspath(dst):
            shutil.copy2(src, dst)
            print("Copied:", dst)


if __name__ == "__main__":
    main()
