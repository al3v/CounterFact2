import os
import json
import pandas as pd
import matplotlib.pyplot as plt


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"
PLOTS_DIR = f"{REPORTS_DIR}/plots"

PAIR_TYPES = ["correct_correct", "correct_wrong", "wrong_wrong"]
PAIR_LABELS = {
    "correct_correct": "correct correct",
    "correct_wrong": "correct wrong",
    "wrong_wrong": "wrong wrong",
}

LINESTYLES = {
    "correct_correct": "-",
    "correct_wrong": ":",
    "wrong_wrong": "--",
}

MARKERS = {
    "correct_correct": "o",
    "correct_wrong": "D",
    "wrong_wrong": "s",
}


def save_plot(name, caption, description):
    os.makedirs(PLOTS_DIR, exist_ok=True)

    png_path = f"{PLOTS_DIR}/{name}.png"
    pdf_path = f"{PLOTS_DIR}/{name}.pdf"
    meta_path = f"{PLOTS_DIR}/{name}.meta.json"

    plt.savefig(png_path, dpi=220, bbox_inches="tight")
    plt.savefig(pdf_path, bbox_inches="tight")

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "caption": caption,
                "description": description,
            },
            f,
            indent=2,
        )

    print("Saved:", png_path)
    print("Saved:", pdf_path)
    print("Saved:", meta_path)


def plot_metric(df, layers, metric, ylabel, title, name, caption, description):
    layer_labels = [f"L{int(l)}" for l in layers]

    plt.figure(figsize=(9, 5.2))

    for pt in PAIR_TYPES:
        vals = []

        for layer in layers:
            sub = df[(df["layer"] == layer) & (df["pair_type"] == pt)]
            vals.append(float(sub.iloc[0][metric]))

        plt.plot(
            layer_labels,
            vals,
            linestyle=LINESTYLES[pt],
            marker=MARKERS[pt],
            linewidth=2.2,
            markersize=7,
            label=PAIR_LABELS[pt],
        )

    plt.title(title)
    plt.xlabel("Layer")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.35)
    plt.legend(loc="best")
    plt.tight_layout()

    save_plot(name, caption, description)
    plt.close()


def plot_gap(df, layers):
    layer_labels = [f"L{int(l)}" for l in layers]

    cw_cos = []
    ww_cos = []
    cw_jac = []
    ww_jac = []

    for layer in layers:
        cw_row = df[(df["layer"] == layer) & (df["pair_type"] == "correct_wrong")].iloc[0]
        ww_row = df[(df["layer"] == layer) & (df["pair_type"] == "wrong_wrong")].iloc[0]

        cw_cos.append(float(cw_row["mean_cosine"]))
        ww_cos.append(float(ww_row["mean_cosine"]))
        cw_jac.append(float(cw_row["mean_jaccard"]))
        ww_jac.append(float(ww_row["mean_jaccard"]))

    cos_gap = [a - b for a, b in zip(cw_cos, ww_cos)]
    jac_gap = [a - b for a, b in zip(cw_jac, ww_jac)]

    x = range(len(layers))
    width = 0.35

    plt.figure(figsize=(9, 5.2))

    plt.bar(
        [i - width / 2 for i in x],
        cos_gap,
        width=width,
        label="Cosine gap: correct_wrong - wrong_wrong",
    )
    plt.bar(
        [i + width / 2 for i in x],
        jac_gap,
        width=width,
        label="Jaccard gap: correct_wrong - wrong_wrong",
    )

    plt.axhline(0, linestyle="--", linewidth=1)

    for i, value in enumerate(cos_gap):
        plt.text(i - width / 2, value, f"{value:+.3f}", ha="center", va="bottom", fontsize=8)

    for i, value in enumerate(jac_gap):
        plt.text(i + width / 2, value, f"{value:+.3f}", ha="center", va="bottom", fontsize=8)

    plt.xticks(list(x), layer_labels)
    plt.title("Distance gap: correct_wrong minus wrong_wrong")
    plt.xlabel("Layer")
    plt.ylabel("Distance gap")
    plt.grid(True, axis="y", alpha=0.35)
    plt.legend(loc="best")
    plt.tight_layout()

    save_plot(
        "sae_gap_cw_minus_ww",
        "Distance gap between correct_wrong and wrong_wrong pairs",
        "Grouped bar chart showing how much larger the correct_wrong pair distance is compared with wrong_wrong pairs.",
    )
    plt.close()


def main():
    summary_path = f"{REPORTS_DIR}/sae_pair_distance_summary_{EXPERIMENT_NAME}.csv"

    if not os.path.exists(summary_path):
        raise FileNotFoundError(
            f"Missing input file: {summary_path}\n"
            "Run this script from the repo root: ~/ADL-SAE-COUNTERFACT"
        )

    df = pd.read_csv(summary_path)
    df = df.sort_values(["layer", "pair_type"]).reset_index(drop=True)

    layers = sorted(df["layer"].unique())

    print("Loaded:", summary_path)
    print("Layers:", layers)
    print("Pair types:", sorted(df["pair_type"].unique()))
    print()

    plot_metric(
        df=df,
        layers=layers,
        metric="mean_cosine",
        ylabel="Mean cosine distance",
        title="Mean cosine distance by layer and pair type",
        name="sae_cosine_by_layer",
        caption="Mean cosine distance by layer and pair type",
        description="Cosine distance between the two paraphrase prompts for each fact, split by pair type.",
    )

    plot_metric(
        df=df,
        layers=layers,
        metric="mean_jaccard",
        ylabel="Mean Jaccard distance",
        title="Mean Jaccard distance by layer and pair type",
        name="sae_jaccard_by_layer",
        caption="Mean Jaccard distance by layer and pair type",
        description="Jaccard distance between active SAE feature sets for the two paraphrases of each fact.",
    )

    plot_metric(
        df=df,
        layers=layers,
        metric="mean_l2",
        ylabel="Mean L2 distance",
        title="Mean L2 distance by layer and pair type",
        name="sae_l2_by_layer",
        caption="Mean L2 distance by layer and pair type",
        description="L2 distance between dense SAE activation vectors for the two paraphrases of each fact.",
    )

    plot_gap(df, layers)

    print()
    print("All plots saved to:", PLOTS_DIR)


if __name__ == "__main__":
    main()
