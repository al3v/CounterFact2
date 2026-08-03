import argparse

from adl_sae.config_registry import add_config_argument, get_config
from adl_sae.worker.qwen_sae_extraction import QwenScopeSAEExtractionWorker


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract Qwen-Scope SAE activations from saved hidden states."
    )

    add_config_argument(parser)

    parser.add_argument(
        "--top-k",
        type=int,
        default=100,
        help="Number of Top-K SAE features to keep.",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    config = get_config(args.config)

    worker = QwenScopeSAEExtractionWorker(config=config, top_k=args.top_k)
    worker.run()


if __name__ == "__main__":
    main()
