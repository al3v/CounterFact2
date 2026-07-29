from adl_sae.model.hf_causal import HFCausalLMWrapper


class LlamaWrapper(HFCausalLMWrapper):
    """
    Llama model wrapper.

    Currently it uses the generic Hugging Face causal LM logic.
    If Llama-specific behavior is needed later, it can be added here.
    """

    pass
