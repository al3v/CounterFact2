import argparse

from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.worker.pipeline import ALL_STEPS, ExperimentPipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the ADL SAE experiment pipeline."
    )

    parser.add_argument(
        "--steps",
        nargs="+",
        default=list(ALL_STEPS),
        choices=list(ALL_STEPS),
        help="Pipeline steps to run.",
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually execute steps. Without this flag, only dry-run/validate.",
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
        help="Optional number of rows for a smoke test.",
    )

    parser.add_argument(
        "--output-suffix",
        type=str,
        default=None,
        help="Optional suffix for hidden-state smoke-test outputs.",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    config = get_counterfact_gemma3_config()

    pipeline = ExperimentPipeline(
        config=config,
        batch_size=args.batch_size,
        max_rows=args.max_rows,
        output_suffix=args.output_suffix,
    )

    pipeline.run(
        steps=args.steps,
        execute=args.execute,
    )


if __name__ == "__main__":
    main()
