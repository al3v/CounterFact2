from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from adl_sae.config import ExperimentConfig


class GenericPairDistancePlotter:
    def __init__(self, config: ExperimentConfig) -> None:
        self.config = config

    @property
    def summary_path(self) -> Path:
        return (
            Path(self.config.reports_dir)
            / f"sae_pair_distance_summary_{self.config.experiment_name}.csv"
        )

    @property
    def plots_dir(self) -> Path:
        return Path(self.config.reports_dir) / "plots"

    def plot_metric(self, summary: pd.DataFrame, metric: str, filename: str, ylabel: str):
        fig, ax = plt.subplots(figsize=(8, 5))

        for pair_type, group in summary.groupby("pair_type"):
            group = group.sort_values("layer")
            ax.plot(group["layer"], group[metric], marker="o", label=pair_type)

        ax.set_xlabel("Layer")
        ax.set_ylabel(ylabel)
        ax.set_title(f"{ylabel} by layer and pair type")
        ax.legend()
        ax.grid(True, alpha=0.3)

        png_path = self.plots_dir / f"{filename}.png"
        pdf_path = self.plots_dir / f"{filename}.pdf"
        meta_path = self.plots_dir / f"{filename}.meta.json"

        fig.tight_layout()
        fig.savefig(png_path, dpi=200)
        fig.savefig(pdf_path)
        plt.close(fig)

        meta = {
            "experiment_name": self.config.experiment_name,
            "model_name": self.config.model_name,
            "metric": metric,
            "source": str(self.summary_path),
            "png": str(png_path),
            "pdf": str(pdf_path),
        }

        meta_path.write_text(json.dumps(meta, indent=2))

        print("Saved plot:", png_path)

    def plot_gap(self, summary: pd.DataFrame):
        pivot = summary.pivot_table(
            index="layer",
            columns="pair_type",
            values="mean_cosine",
        )

        if "correct_wrong" not in pivot.columns or "wrong_wrong" not in pivot.columns:
            print("Skipping gap plot because correct_wrong or wrong_wrong is missing.")
            return

        gap = pivot["correct_wrong"] - pivot["wrong_wrong"]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(gap.index, gap.values, marker="o")
        ax.axhline(0, linestyle="--", linewidth=1)
        ax.set_xlabel("Layer")
        ax.set_ylabel("Mean cosine gap")
        ax.set_title("Mean cosine gap: correct_wrong minus wrong_wrong")
        ax.grid(True, alpha=0.3)

        png_path = self.plots_dir / "sae_gap_cw_minus_ww.png"
        pdf_path = self.plots_dir / "sae_gap_cw_minus_ww.pdf"
        meta_path = self.plots_dir / "sae_gap_cw_minus_ww.meta.json"

        fig.tight_layout()
        fig.savefig(png_path, dpi=200)
        fig.savefig(pdf_path)
        plt.close(fig)

        meta = {
            "experiment_name": self.config.experiment_name,
            "model_name": self.config.model_name,
            "source": str(self.summary_path),
            "description": "mean_cosine(correct_wrong) - mean_cosine(wrong_wrong)",
            "png": str(png_path),
            "pdf": str(pdf_path),
        }

        meta_path.write_text(json.dumps(meta, indent=2))

        print("Saved plot:", png_path)

    def run(self):
        if not self.summary_path.exists():
            raise FileNotFoundError(f"Pair-distance summary not found: {self.summary_path}")

        summary = pd.read_csv(self.summary_path)

        required_cols = {
            "layer",
            "pair_type",
            "mean_cosine",
            "mean_l2",
            "mean_jaccard",
            "mean_shared",
        }
        missing = required_cols - set(summary.columns)
        if missing:
            raise ValueError(f"Summary missing columns: {sorted(missing)}")

        self.plots_dir.mkdir(parents=True, exist_ok=True)

        print("=== Generic pair-distance plots ===")
        print("Experiment:", self.config.experiment_name)
        print("Summary:", self.summary_path)
        print("Plots dir:", self.plots_dir)

        self.plot_metric(
            summary,
            metric="mean_cosine",
            filename="sae_cosine_by_layer",
            ylabel="Mean cosine distance",
        )
        self.plot_metric(
            summary,
            metric="mean_jaccard",
            filename="sae_jaccard_by_layer",
            ylabel="Mean Jaccard distance",
        )
        self.plot_metric(
            summary,
            metric="mean_l2",
            filename="sae_l2_by_layer",
            ylabel="Mean L2 distance",
        )
        self.plot_metric(
            summary,
            metric="mean_shared",
            filename="sae_shared_features_by_layer",
            ylabel="Mean shared active features",
        )
        self.plot_gap(summary)

        print("All plots saved to:", self.plots_dir)
