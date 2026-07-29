from dataclasses import dataclass

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from adl_sae.model.base import BaseModelWrapper


def resolve_torch_dtype(dtype_name: str):
    if dtype_name == "bfloat16":
        return torch.bfloat16

    if dtype_name == "float16":
        return torch.float16

    if dtype_name == "float32":
        return torch.float32

    raise ValueError(f"Unsupported torch dtype: {dtype_name}")


@dataclass
class HFCausalLMWrapper(BaseModelWrapper):
    """
    Generic Hugging Face causal language model wrapper.

    Gemma, Qwen, and Llama are all causal language models, so most of
    the loading, generation, and hidden-state extraction logic can be shared.
    """

    model_name: str
    torch_dtype: str = "bfloat16"
    device_map: str = "auto"
    padding_side: str = "left"
    trust_remote_code: bool = False

    def __post_init__(self):
        self.tokenizer = None
        self.model = None

    def load(self):
        print(f"Loading tokenizer: {self.model_name}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=self.trust_remote_code,
        )

        self.tokenizer.padding_side = self.padding_side

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        print(f"Loading model: {self.model_name}")

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=resolve_torch_dtype(self.torch_dtype),
            device_map=self.device_map,
            trust_remote_code=self.trust_remote_code,
        )

        self.model.eval()

        return self

    def _get_input_device(self):
        if self.model is None:
            raise RuntimeError("Model is not loaded. Call .load() first.")

        return next(self.model.parameters()).device

    def generate_text(self, prompts, max_new_tokens=32):
        """
        Generate continuations for prompts.

        Returns a list of decoded generated texts.
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model/tokenizer is not loaded. Call .load() first.")

        inputs = self.tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )

        inputs = {k: v.to(self._get_input_device()) for k, v in inputs.items()}

        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.pad_token_id,
            )

        decoded = self.tokenizer.batch_decode(
            generated_ids,
            skip_special_tokens=True,
        )

        return decoded

    def extract_last_token_hidden_states(self, prompts, layers):
        """
        Extract hidden states at the last prompt token.

        Important:
        We use left padding, so the final sequence position is the real
        last prompt token for every prompt in the batch.

        Hugging Face hidden_states indexing:
        hidden_states[0] is embedding output.
        hidden_states[layer + 1] corresponds to transformer layer `layer`.
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model/tokenizer is not loaded. Call .load() first.")

        inputs = self.tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )

        inputs = {k: v.to(self._get_input_device()) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(
                **inputs,
                output_hidden_states=True,
                use_cache=False,
            )

        selected_hidden_states = []

        for layer in layers:
            hidden = outputs.hidden_states[layer + 1]

            # left padding means the last position is the last real prompt token
            last_token_hidden = hidden[:, -1, :]

            selected_hidden_states.append(last_token_hidden)

        stacked = torch.stack(selected_hidden_states, dim=1)

        return stacked.detach().float().cpu()
