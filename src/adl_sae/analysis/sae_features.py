from dataclasses import dataclass
from pathlib import Path
import runpy


@dataclass
class SAEFeatureAnalysis:
    """
    Worker wrapper for SAE feature analysis.

    For now, this safely calls the existing legacy script:
    scripts/analyze_sae_features_counterfact.py

    This keeps the scientific logic unchanged while moving the pipeline
    toward the new src/adl_sae package structure.
    """

    config: object
    legacy_script_path: str = "scripts/analyze_sae_features_counterfact.py"

    def sae_prompt_summary_path(self) -> Path:
        return Path(
            f"{self.config.reports_dir}/"
            f"sae_prompt_summary_{self.config.experiment_name}.csv"
        )

    def all_pair_types_path(self) -> Path:
        return Path(
            f"outputs/all_facts_pair_types_{self.config.experiment_name}.csv"
        )

    def validate_inputs(self):
        script_path = Path(self.legacy_script_path)

        required_paths = [
            script_path,
            Path(self.config.sae_active_features_path),
            self.sae_prompt_summary_path(),
            self.all_pair_types_path(),
        ]

        missing = [path for path in required_paths if not path.exists()]

        if missing:
            missing_text = "\n".join(str(path) for path in missing)
            raise FileNotFoundError(f"Missing required input files:\n{missing_text}")

        print("SAE feature analysis inputs look OK.")
        print("Experiment:", self.config.experiment_name)
        print("Active features:", self.config.sae_active_features_path)
        print("Prompt summary:", self.sae_prompt_summary_path())
        print("Pair types:", self.all_pair_types_path())
        print("Legacy script:", script_path)

    def run(self, dry_run: bool = False):
        self.validate_inputs()

        if dry_run:
            print("Dry run only. Did not execute SAE feature analysis.")
            return

        print("Running SAE feature analysis via legacy script...")
        runpy.run_path(self.legacy_script_path, run_name="__main__")
