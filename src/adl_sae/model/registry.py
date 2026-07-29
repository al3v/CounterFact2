from adl_sae.model.gemma import GemmaWrapper
from adl_sae.model.llama import LlamaWrapper
from adl_sae.model.qwen import QwenWrapper


MODEL_REGISTRY = {
    "gemma": GemmaWrapper,
    "qwen": QwenWrapper,
    "llama": LlamaWrapper,
}


def create_model_wrapper(config):
    """
    Create model wrapper from ExperimentConfig.

    Example:
    config.model_family = "gemma"
    config.model_name = "google/gemma-3-4b-pt"
    """
    model_family = config.model_family.lower()

    if model_family not in MODEL_REGISTRY:
        valid = ", ".join(sorted(MODEL_REGISTRY.keys()))
        raise ValueError(
            f"Unknown model family: {config.model_family}. "
            f"Valid options are: {valid}"
        )

    wrapper_class = MODEL_REGISTRY[model_family]

    return wrapper_class(
        model_name=config.model_name,
        torch_dtype=config.torch_dtype,
        device_map=config.device_map,
        padding_side=config.padding_side,
        trust_remote_code=config.trust_remote_code,
    )
