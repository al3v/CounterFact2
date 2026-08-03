import argparse

from adl_sae.analysis.dense_pair_distances import DensePairDistanceAnalyzer
from adl_sae.config_registry import add_config_argument, get_config


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute dense hidden-state pair distances between paraphrases."
    )

    add_config_argument(parser)

    return parser.parse_args()


def main():
    args = parse_args()

    config = get_config(args.config)

    analyzer = DensePairDistanceAnalyzer(config=config)
    analyzer.run()


if __name__ == "__main__":
    main()
