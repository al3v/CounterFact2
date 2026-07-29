from abc import ABC, abstractmethod


class BaseModelWrapper(ABC):
    """
    Common interface for language model wrappers.

    The goal is that Gemma, Qwen, and Llama can all be used through
    the same methods.
    """

    @abstractmethod
    def load(self):
        """Load tokenizer and model."""
        raise NotImplementedError

    @abstractmethod
    def generate_text(self, prompts, max_new_tokens=32):
        """Generate text continuations for a list of prompts."""
        raise NotImplementedError

    @abstractmethod
    def extract_last_token_hidden_states(self, prompts, layers):
        """
        Extract hidden states at the last prompt token.

        Returns tensor with shape:
        batch_size x n_layers x hidden_dim
        """
        raise NotImplementedError
