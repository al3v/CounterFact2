from dataclasses import dataclass
from pathlib import Path
import runpy
import sys


@dataclass
class PairDistancePlotter:
    """
    Wrapper for pair-distance plotting.

    For now, this calls the existing legacy plotting script:
    scripts/plot_sae_pair_distance_counterfact.py

    This keeps the plotting logic unchanged while moving the pipeline
    toward the new src/adl_sae package structure.
    """

    config: object
    legacy_script_path: str = "scripts/plot_sae_pair_distance_counterfact.py"

    def pair_distance_summary_path(self) -> Path:
        return Path(
            f"{self.config.reports_dir}/"
            f"sae_pair_distance_summary_{self.config.experiment_name}.csv"
        )

    def validate_inputs(self):
        script_path = Path(self.legacy_script_path)
        summary_path = self.pair_distance_summary_path()

        required_paths = [
            script_path,
            summary_path,
        ]

        missing = [path for path in required_paths if not path.exists()]

        if missing:
            missing_text = "\n".join(str(path) for path in missing)
            raise FileNotFoundError(f"Missing required input files:\n{missing_text}")

        print("Pair-distance plotting inputs look OK.")
        print("Experiment:", self.config.experiment_name)
        print("Pair-distance summary:", summary_path)
        print("Legacy script:", script_path)

    def run(self, dry_run: bool = False):
        self.validate_inputs()

        if dry_run:
            print("Dry run only. Did not create plots.")
            return

        print("Running pair-distance plotting via legacy script...")
        old_argv = sys.argv
        try:
            sys.argv = [self.legacy_script_path]
            runpy.run_path(self.legacy_script_path, run_name="__main__")
        finally:
            sys.argv = old_argv
