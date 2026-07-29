import argparse

from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.worker.hidden_states import HiddenStateWorker


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract last-token hidden states for selected layers."
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=8,
        help="Batch size for hidden-state extraction.",
    )

    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional small number of rows for a smoke test.",
    )

    parser.add_argument(
        "--output-suffix",
        type=str,
        default=None,
        help="Optional suffix to avoid overwriting full outputs during tests.",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    config = get_counterfact_gemma3_config()

    worker = HiddenStateWorker(
        config=config,
        batch_size=args.batch_size,
        max_rows=args.max_rows,
        output_suffix=args.output_suffix,
    )

    worker.run()


if __name__ == "__main__":
    main()
