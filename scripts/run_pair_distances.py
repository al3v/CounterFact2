from adl_sae.analysis.pair_distances import PairDistanceAnalyzer


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"


def main():
    analyzer = PairDistanceAnalyzer(
        experiment_name=EXPERIMENT_NAME,
        reports_dir=REPORTS_DIR,
        sae_width=16384,
    )

    analyzer.run()


if __name__ == "__main__":
    main()
