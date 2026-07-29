from adl_sae.model.hf_causal import HFCausalLMWrapper


class GemmaWrapper(HFCausalLMWrapper):
    """
    Gemma model wrapper.

    Currently it uses the generic Hugging Face causal LM logic.
    If Gemma-specific behavior is needed later, it can be added here.
    """

    pass
