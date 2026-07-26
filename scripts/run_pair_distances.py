from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.analysis.pair_distances import PairDistanceAnalyzer


def main():
    config = get_counterfact_gemma3_config()

    analyzer = PairDistanceAnalyzer(
        experiment_name=config.experiment_name,
        reports_dir=config.reports_dir,
        sae_width=config.sae_width,
    )

    analyzer.run()


if __name__ == "__main__":
    main()
