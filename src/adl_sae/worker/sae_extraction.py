from dataclasses import dataclass
from pathlib import Path
import runpy
import sys


@dataclass
class SAEExtractionWorker:
    """
    Worker wrapper for SAE feature extraction.

    For now, this safely calls the existing legacy script:
    scripts/extract_sae_features_gemma3_manual.py

    This keeps the scientific logic unchanged while moving the pipeline
    toward the new src/adl_sae package structure.
    """

    config: object
    legacy_script_path: str = "scripts/extract_sae_features_gemma3_manual.py"

    def validate_inputs(self):
        script_path = Path(self.legacy_script_path)

        if not script_path.exists():
            raise FileNotFoundError(f"Legacy SAE extraction script not found: {script_path}")

        hidden_states_path = Path(self.config.hidden_states_path)

        if not hidden_states_path.exists():
            raise FileNotFoundError(f"Hidden states file not found: {hidden_states_path}")

        print("SAE extraction inputs look OK.")
        print("Experiment:", self.config.experiment_name)
        print("Model:", self.config.model_name)
        print("SAE release:", self.config.sae_release)
        print("Hidden states:", hidden_states_path)
        print("Legacy script:", script_path)

    def run(self, dry_run: bool = False):
        self.validate_inputs()

        if dry_run:
            print("Dry run only. Did not execute SAE extraction.")
            return

        print("Running SAE extraction via legacy script...")
        old_argv = sys.argv
        try:
            sys.argv = [self.legacy_script_path]
            runpy.run_path(self.legacy_script_path, run_name="__main__")
        finally:
            sys.argv = old_argv
