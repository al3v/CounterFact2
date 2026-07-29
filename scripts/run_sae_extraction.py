import argparse

from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.worker.sae_extraction import SAEExtractionWorker


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run SAE feature extraction."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only validate inputs and print paths; do not run extraction.",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    config = get_counterfact_gemma3_config()

    worker = SAEExtractionWorker(config=config)
    worker.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
