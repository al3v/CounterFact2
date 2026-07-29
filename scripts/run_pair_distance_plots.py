import argparse

from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.analysis.plots import PairDistancePlotter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create pair-distance plots."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only validate inputs and print paths; do not create plots.",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    config = get_counterfact_gemma3_config()

    plotter = PairDistancePlotter(config=config)
    plotter.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
