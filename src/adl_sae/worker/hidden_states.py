import os
from dataclasses import dataclass
from typing import Optional

import pandas as pd
import torch
from tqdm import tqdm

from adl_sae.model.registry import create_model_wrapper


def find_prompt_column(df: pd.DataFrame) -> str:
    """
    Find the column containing the prompt text.
    Different scripts may name this slightly differently.
    """
    candidates = [
        "prompt_given_to_model",
        "prompt",
        "base_prompt",
        "template",
    ]

    for col in candidates:
        if col in df.columns:
            return col

    raise ValueError(
        "Could not find prompt column. Expected one of: "
        + ", ".join(candidates)
    )


def count_prompt_tokens(tokenizer, prompts):
    """
    Count prompt tokens using attention_mask.
    """
    inputs = tokenizer(
        prompts,
        return_tensors="pt",
        padding=True,
        truncation=True,
    )

    return inputs["attention_mask"].sum(dim=1).cpu().tolist()


@dataclass
class HiddenStateWorker:
    """
    Extract last-prompt-token hidden states from selected model layers.

    Output tensor shape:
    n_prompts x n_layers x hidden_dim

    Example for this project:
    4382 x 6 x 2560
    """

    config: object
    batch_size: int = 8
    max_rows: Optional[int] = None
    output_suffix: Optional[str] = None

    def prompt_outputs_path(self) -> str:
        return self.config.prompt_outputs_path

    def hidden_states_path(self) -> str:
        if self.output_suffix is None:
            return self.config.hidden_states_path

        base = self.config.hidden_states_path.replace(".pt", "")
        return f"{base}_{self.output_suffix}.pt"

    def metadata_path(self) -> str:
        if self.output_suffix is None:
            return self.config.hidden_states_metadata_path

        base = self.config.hidden_states_metadata_path.replace(".csv", "")
        return f"{base}_{self.output_suffix}.csv"

    def load_prompt_outputs(self) -> pd.DataFrame:
        print("Loading prompt outputs:")
        print(self.prompt_outputs_path())

        df = pd.read_csv(self.prompt_outputs_path())

        if self.max_rows is not None:
            df = df.head(self.max_rows).copy()
            print(f"Using only first {self.max_rows} rows for test run.")

        print("Prompt rows:", len(df))
        print("Columns:", list(df.columns))
        print()

        return df

    def build_metadata_rows(self, batch_df, layers, n_tokens):
        metadata_rows = []

        for i, (_, row) in enumerate(batch_df.iterrows()):
            for layer in layers:
                metadata_rows.append(
                    {
                        "row_id": row.get("row_id", row.name),
                        "fact_id": row.get("fact_id", None),
                        "variant_id": row.get("variant_id", None),
                        "variant_source": row.get("variant_source", None),
                        "pair_type": row.get("pair_type", None),
                        "is_correct": row.get("is_correct", None),
                        "layer": layer,
                        "hf_hidden_state_index": layer + 1,
                        "n_tokens": n_tokens[i],
                        "model_name": self.config.model_name,
                        "experiment_name": self.config.experiment_name,
                    }
                )

        return metadata_rows

    def run(self):
        os.makedirs(self.config.outputs_dir, exist_ok=True)
        os.makedirs(self.config.reports_dir, exist_ok=True)

        prompt_df = self.load_prompt_outputs()
        prompt_col = find_prompt_column(prompt_df)

        print("Prompt column:", prompt_col)
        print("Selected layers:", self.config.layers)
        print("Batch size:", self.batch_size)
        print()

        model_wrapper = create_model_wrapper(self.config)
        model_wrapper.load()

        all_hidden_states = []
        all_metadata_rows = []

        for start in tqdm(range(0, len(prompt_df), self.batch_size), desc="Extracting hidden states"):
            end = start + self.batch_size
            batch_df = prompt_df.iloc[start:end].copy()
            prompts = batch_df[prompt_col].astype(str).tolist()

            batch_hidden = model_wrapper.extract_last_token_hidden_states(
                prompts=prompts,
                layers=self.config.layers,
            )

            n_tokens = count_prompt_tokens(model_wrapper.tokenizer, prompts)

            all_hidden_states.append(batch_hidden)

            batch_metadata = self.build_metadata_rows(
                batch_df=batch_df,
                layers=self.config.layers,
                n_tokens=n_tokens,
            )
            all_metadata_rows.extend(batch_metadata)

        hidden_tensor = torch.cat(all_hidden_states, dim=0)
        metadata_df = pd.DataFrame(all_metadata_rows)

        torch.save(
            {
                "hidden_states": hidden_tensor,
                "layers": list(self.config.layers),
                "model_name": self.config.model_name,
                "experiment_name": self.config.experiment_name,
            },
            self.hidden_states_path(),
        )

        metadata_df.to_csv(self.metadata_path(), index=False)

        print()
        print("Saved hidden states:")
        print(self.hidden_states_path())
        print("Shape:", tuple(hidden_tensor.shape))

        print()
        print("Saved metadata:")
        print(self.metadata_path())
        print("Rows:", len(metadata_df))

        return hidden_tensor, metadata_df
