from dataclasses import dataclass
from typing import Optional

from adl_sae.analysis.pair_distances import PairDistanceAnalyzer
from adl_sae.analysis.plots import PairDistancePlotter
from adl_sae.analysis.sae_features import SAEFeatureAnalysis
from adl_sae.data.pair_types import CounterFactPairTypeBuilder
from adl_sae.worker.hidden_states import HiddenStateWorker
from adl_sae.worker.sae_extraction import SAEExtractionWorker


ALL_STEPS = (
    "pair_types",
    "hidden_states",
    "sae_extraction",
    "sae_feature_analysis",
    "pair_distances",
    "plots",
)


@dataclass
class ExperimentPipeline:
    """
    Small orchestrator for the ADL SAE pipeline.

    By default this can dry-run and print the planned steps.
    Use execute=True only when you actually want to run the steps.
    """

    config: object
    batch_size: int = 8
    max_rows: Optional[int] = None
    output_suffix: Optional[str] = None

    def validate_steps(self, steps):
        unknown = [step for step in steps if step not in ALL_STEPS]

        if unknown:
            valid = ", ".join(ALL_STEPS)
            raise ValueError(
                f"Unknown pipeline steps: {unknown}. Valid steps are: {valid}"
            )

    def print_plan(self, steps, execute: bool):
        mode = "EXECUTE" if execute else "DRY RUN"

        print("=== ADL SAE Pipeline ===")
        print("Mode:", mode)
        print("Experiment:", self.config.experiment_name)
        print("Model:", self.config.model_name)
        print("SAE release:", self.config.sae_release)
        print("Layers:", self.config.layers)
        print("Steps:", " -> ".join(steps))
        print()

    def run(self, steps=ALL_STEPS, execute: bool = False):
        self.validate_steps(steps)
        self.print_plan(steps, execute=execute)

        for step in steps:
            print()
            print("=" * 80)
            print(f"Step: {step}")
            print("=" * 80)

            if step == "pair_types":
                if not execute:
                    print("Would create pair types and switching subset.")
                    continue

                builder = CounterFactPairTypeBuilder(
                    experiment_name=self.config.experiment_name,
                    reports_dir=self.config.reports_dir,
                )
                builder.run()

            elif step == "hidden_states":
                if not execute:
                    print("Would extract selected-layer last-token hidden states.")
                    print("This is a GPU-heavy step.")
                    continue

                worker = HiddenStateWorker(
                    config=self.config,
                    batch_size=self.batch_size,
                    max_rows=self.max_rows,
                    output_suffix=self.output_suffix,
                )
                worker.run()

            elif step == "sae_extraction":
                if not execute:
                    print("Would extract SAE features from hidden states.")
                    print("This step is currently Gemma/Gemma-Scope specific.")
                    continue

                worker = SAEExtractionWorker(config=self.config)
                worker.run(dry_run=False)

            elif step == "sae_feature_analysis":
                if not execute:
                    print("Would analyze SAE features by correctness group.")
                    continue

                analysis = SAEFeatureAnalysis(config=self.config)
                analysis.run(dry_run=False)

            elif step == "pair_distances":
                if not execute:
                    print("Would compute pairwise SAE distances between paraphrases.")
                    continue

                analyzer = PairDistanceAnalyzer(
                    experiment_name=self.config.experiment_name,
                    reports_dir=self.config.reports_dir,
                    sae_width=self.config.sae_width,
                )
                analyzer.run()

            elif step == "plots":
                if not execute:
                    print("Would create pair-distance plots.")
                    continue

                plotter = PairDistancePlotter(config=self.config)
                plotter.run(dry_run=False)

        print()
        print("Pipeline finished.")
