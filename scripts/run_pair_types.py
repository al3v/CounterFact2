from adl_sae.data.pair_types import CounterFactPairTypeBuilder


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"


def main():
    builder = CounterFactPairTypeBuilder(
        experiment_name=EXPERIMENT_NAME,
        reports_dir=REPORTS_DIR,
    )

    builder.run()


if __name__ == "__main__":
    main()
