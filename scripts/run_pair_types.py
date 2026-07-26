from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.data.pair_types import CounterFactPairTypeBuilder


def main():
    config = get_counterfact_gemma3_config()

    builder = CounterFactPairTypeBuilder(
        experiment_name=config.experiment_name,
        reports_dir=config.reports_dir,
    )

    builder.run()


if __name__ == "__main__":
    main()
