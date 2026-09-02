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

    def _select_last_nonpad_hidden(self, hidden, attention_mask):
        """
        Select the hidden state at the final real token, not at padding.

        This helper is padding-side agnostic:
        - right padding: [1, 1, 1, 0, 0] -> position 2
        - left padding:  [0, 0, 1, 1, 1] -> position 4

        The largest sequence index with attention_mask value 1 is selected.
        """
        mask = attention_mask.to(hidden.device).long()

        positions = torch.arange(
            mask.shape[1],
            device=hidden.device,
        ).unsqueeze(0)

        last_nonpad = (mask * positions).max(dim=1).values.long()

        batch_indices = torch.arange(
            hidden.shape[0],
            device=hidden.device,
        )

        return hidden[batch_indices, last_nonpad, :]

    def get_prompt_token_metadata(self, prompts):
        """
        Return token-level metadata for the prompt batch.

        The same tokenizer settings as hidden-state extraction are used.
        The final prompt token is selected from the last non-padding position.
        """
        if self.tokenizer is None:
            raise RuntimeError("Tokenizer is not loaded. Call .load() first.")

        inputs = self.tokenizer(
            prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )

        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"].long()

        positions = torch.arange(
            attention_mask.shape[1],
            device=attention_mask.device,
        ).unsqueeze(0)

        last_nonpad = (attention_mask * positions).max(dim=1).values.long()

        metadata = []

        for i in range(input_ids.shape[0]):
            mask_i = attention_mask[i].bool()
            prompt_token_ids = input_ids[i][mask_i].tolist()
            last_pos = int(last_nonpad[i].item())
            final_token_id = int(input_ids[i, last_pos].item())

            try:
                final_prompt_token_text = self.tokenizer.decode(
                    [final_token_id],
                    skip_special_tokens=False,
                )
            except Exception:
                final_prompt_token_text = ""

            metadata.append(
                {
                    "prompt_token_ids": prompt_token_ids,
                    "n_prompt_tokens": len(prompt_token_ids),
                    "last_nonpad_position": last_pos,
                    "final_prompt_token_id": final_token_id,
                    "final_prompt_token_text": final_prompt_token_text,
                }
            )

        return metadata


    def extract_last_token_hidden_states(self, prompts, layers):
        """
        Extract hidden states at the last real prompt token.

        Padding side is not assumed.
        The attention mask is used to select the final non-padding token
        for each prompt in the batch.

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
        attention_mask = inputs["attention_mask"]

        with torch.no_grad():
            outputs = self.model(
                **inputs,
                output_hidden_states=True,
                use_cache=False,
            )

        selected_hidden_states = []

        for layer in layers:
            hidden = outputs.hidden_states[layer + 1]
            last_token_hidden = self._select_last_nonpad_hidden(
                hidden=hidden,
                attention_mask=attention_mask,
            )

            selected_hidden_states.append(last_token_hidden)

        stacked = torch.stack(selected_hidden_states, dim=1)

        return stacked.detach().float().cpu()
