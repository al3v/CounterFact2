import argparse

from adl_sae.config_registry import add_config_argument, get_config
from adl_sae.worker.generation import GenerationWorker


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run model generation and strict grading for CounterFact prompts."
    )

    add_config_argument(parser)

    parser.add_argument(
        "--input-path",
        type=str,
        default=None,
        help="Input prompt CSV. If omitted, the default CounterFact prompt CSV is used.",
    )

    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional number of rows for a smoke test.",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Generation batch size.",
    )

    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=32,
        help="Maximum number of new tokens to generate.",
    )

    parser.add_argument(
        "--output-suffix",
        type=str,
        default="",
        help="Optional suffix for smoke-test outputs.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would run without loading the model.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    config = get_config(args.config)

    worker = GenerationWorker(
        config=config,
        input_path=args.input_path,
        output_suffix=args.output_suffix,
    )

    worker.run(
        max_rows=args.max_rows,
        batch_size=args.batch_size,
        max_new_tokens=args.max_new_tokens,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
