from __future__ import annotations

from typing import Iterable, Optional

from adl_sae.analysis.dense_pair_distances import DensePairDistanceAnalyzer
from adl_sae.analysis.pair_distances import PairDistanceAnalyzer
from adl_sae.analysis.plots import PairDistancePlotter
from adl_sae.analysis.generic_pair_distance_plots import GenericPairDistancePlotter
from adl_sae.analysis.sae_features import SAEFeatureAnalysis
from adl_sae.analysis.generic_sae_features import GenericSAEFeatureAnalysis
from adl_sae.config import ExperimentConfig
from adl_sae.data.pair_types import CounterFactPairTypeBuilder
from adl_sae.worker.generation import GenerationWorker
from adl_sae.worker.hidden_states import HiddenStateWorker
from adl_sae.worker.sae_extraction import SAEExtractionWorker
from adl_sae.worker.qwen_sae_extraction import QwenScopeSAEExtractionWorker


ALL_STEPS = (
    "generation",
    "pair_types",
    "hidden_states",
    "sae_extraction",
    "sae_feature_analysis",
    "pair_distances",
    "dense_pair_distances",
    "plots",
)


class ExperimentPipeline:
    def __init__(self, config: ExperimentConfig) -> None:
        self.config = config

    def validate_steps(self, steps: Iterable[str]) -> None:
        unknown = [step for step in steps if step not in ALL_STEPS]

        if unknown:
            valid = ", ".join(ALL_STEPS)
            raise ValueError(
                f"Unknown pipeline step(s): {unknown}. Valid steps are: {valid}"
            )

    def print_header(self, steps: Iterable[str], execute: bool) -> None:
        print("=== ADL SAE Pipeline ===")
        print("Mode:", "EXECUTE" if execute else "DRY RUN")
        print("Experiment:", self.config.experiment_name)
        print("Model:", self.config.model_name)
        print("SAE release:", self.config.sae_release)
        print("Layers:", self.config.layers)
        print("Steps:", " -> ".join(steps))
        print()

    def run(
        self,
        steps: Iterable[str] = ALL_STEPS,
        execute: bool = False,
        max_rows: Optional[int] = None,
        batch_size: int = 4,
        max_new_tokens: int = 32,
        output_suffix: str = "",
        input_path: Optional[str] = None,
    ) -> None:
        steps = tuple(steps)

        self.validate_steps(steps)
        self.print_header(steps=steps, execute=execute)

        for step in steps:
            print()
            print("=" * 80)
            print(f"Step: {step}")
            print("=" * 80)

            if step == "generation":
                worker = GenerationWorker(
                    config=self.config,
                    input_path=input_path,
                    output_suffix=output_suffix,
                )

                worker.run(
                    max_rows=max_rows,
                    batch_size=batch_size,
                    max_new_tokens=max_new_tokens,
                    dry_run=not execute,
                )

            elif step == "pair_types":
                if not execute:
                    print("Would create pair types and switching subset.")
                    continue

                builder = CounterFactPairTypeBuilder(
                    self.config.experiment_name,
                    self.config.reports_dir,
                )
                builder.run()

            elif step == "hidden_states":
                if not execute:
                    print("Would extract selected-layer last-token hidden states.")
                    print("This is a GPU-heavy step.")
                    continue

                worker = HiddenStateWorker(config=self.config)
                worker.run()

            elif step == "sae_extraction":
                if not execute:
                    print("Would extract SAE features from hidden states.")
                    print("Gemma configs use Gemma Scope.")
                    print("Qwen SAE configs use Qwen-Scope.")
                    continue

                if str(self.config.sae_release).startswith("Qwen/SAE-"):
                    worker = QwenScopeSAEExtractionWorker(config=self.config, top_k=100)
                    worker.run()
                else:
                    worker = SAEExtractionWorker(config=self.config)
                    worker.run(dry_run=False)

            elif step == "sae_feature_analysis":
                if not execute:
                    print("Would analyze SAE features by correctness group.")
                    continue

                if str(self.config.sae_release).startswith("Qwen/SAE-"):
                    analysis = GenericSAEFeatureAnalysis(config=self.config)
                    analysis.run()
                else:
                    analysis = SAEFeatureAnalysis(config=self.config)
                    analysis.run(dry_run=False)

            elif step == "pair_distances":
                if not execute:
                    print("Would compute pairwise SAE distances between paraphrases.")
                    continue

                analyzer = PairDistanceAnalyzer(
                    self.config.experiment_name,
                    self.config.reports_dir,
                    self.config.sae_width,
                )
                analyzer.run()

            elif step == "dense_pair_distances":
                if not execute:
                    print("Would compute dense hidden-state pair distances.")
                    continue

                analyzer = DensePairDistanceAnalyzer(config=self.config)
                analyzer.run()

            elif step == "plots":
                if not execute:
                    print("Would create pair-distance plots.")
                    continue

                if str(self.config.sae_release).startswith("Qwen/SAE-"):
                    plotter = GenericPairDistancePlotter(config=self.config)
                    plotter.run()
                else:
                    plotter = PairDistancePlotter(config=self.config)
                    plotter.run(dry_run=False)

        print()
        print("Pipeline finished.")
