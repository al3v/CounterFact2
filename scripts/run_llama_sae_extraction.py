import argparse

from adl_sae.config_registry import add_config_argument, get_config
from adl_sae.worker.llama_sae_extraction import LlamaScopeSAEExtractionWorker


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract Llama-Scope SAE activations from saved hidden states."
    )

    add_config_argument(parser)

    return parser.parse_args()


def main():
    args = parse_args()
    config = get_config(args.config)

    worker = LlamaScopeSAEExtractionWorker(config=config)
    worker.run()


if __name__ == "__main__":
    main()
