from adl_sae.config import (
    get_counterfact_gemma3_config,
    get_counterfact_qwen25_config,
    get_counterfact_llama32_config,
)


CONFIG_REGISTRY = {
    "gemma3": get_counterfact_gemma3_config,
    "qwen25": get_counterfact_qwen25_config,
    "llama32": get_counterfact_llama32_config,
}


def get_config(config_name: str):
    if config_name not in CONFIG_REGISTRY:
        valid = ", ".join(sorted(CONFIG_REGISTRY.keys()))
        raise ValueError(
            f"Unknown config: {config_name}. Valid configs are: {valid}"
        )

    return CONFIG_REGISTRY[config_name]()


def add_config_argument(parser):
    parser.add_argument(
        "--config",
        choices=sorted(CONFIG_REGISTRY.keys()),
        default="gemma3",
        help="Experiment/model config to use.",
    )
