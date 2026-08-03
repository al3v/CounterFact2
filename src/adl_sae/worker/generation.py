from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

import pandas as pd
from tqdm import tqdm

from adl_sae.config import ExperimentConfig
from adl_sae.model.registry import create_model_wrapper


def normalize_answer(text: object) -> str:
    if text is None:
        return ""

    text = str(text).lower()
    text = text.strip()
    text = re.sub(r"[\n\r\t]+", " ", text)
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_first_answer_segment(text: str) -> str:
    text = str(text)

    # For completion-style CounterFact prompts, the answer should appear early.
    first_line = text.splitlines()[0] if text.splitlines() else text
    short_chars = first_line[:160]
    words = short_chars.split()
    return " ".join(words[:12])


def strict_match(generated_answer: str, correct_answer: str) -> tuple[bool, str, str]:
    segment = get_first_answer_segment(generated_answer)

    norm_segment = normalize_answer(segment)
    norm_correct = normalize_answer(correct_answer)

    if not norm_correct:
        return False, segment, ""

    # Strict but simple: correct answer must appear near the beginning.
    is_correct = norm_correct in norm_segment

    matched_answer = correct_answer if is_correct else ""
    return is_correct, segment, matched_answer


def find_prompt_column(df: pd.DataFrame) -> str:
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


def find_answer_column(df: pd.DataFrame) -> str:
    candidates = [
        "correct_answer",
        "target_true",
        "answer",
    ]

    for col in candidates:
        if col in df.columns:
            return col

    raise ValueError(
        "Could not find correct-answer column. Expected one of: "
        + ", ".join(candidates)
    )


class GenerationWorker:
    def __init__(
        self,
        config: ExperimentConfig,
        input_path: Optional[str] = None,
        output_suffix: str = "",
    ) -> None:
        self.config = config
        self.input_path = Path(input_path) if input_path else self.default_input_path()
        self.output_suffix = output_suffix

    def default_input_path(self) -> Path:
        return Path(
            "data/counterfact/"
            "counterfact_paraphrase_prompts_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv"
        )

    def output_path(self) -> Path:
        suffix = f"_{self.output_suffix}" if self.output_suffix else ""
        return Path(
            self.config.outputs_dir
        ) / f"prompt_outputs_{self.config.experiment_name}{suffix}.csv"

    def run(
        self,
        max_rows: Optional[int] = None,
        batch_size: int = 4,
        max_new_tokens: int = 32,
        dry_run: bool = False,
    ) -> Path:
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input prompt file not found: {self.input_path}")

        df = pd.read_csv(self.input_path)

        if max_rows is not None:
            df = df.head(max_rows).copy()

        prompt_col = find_prompt_column(df)
        answer_col = find_answer_column(df)

        output_path = self.output_path()

        print("=== Generation worker ===")
        print("Experiment:", self.config.experiment_name)
        print("Model:", self.config.model_name)
        print("Input:", self.input_path)
        print("Output:", output_path)
        print("Rows:", len(df))
        print("Prompt column:", prompt_col)
        print("Answer column:", answer_col)
        print("Batch size:", batch_size)
        print("Max new tokens:", max_new_tokens)

        if dry_run:
            print("Dry run only. Did not load model or generate.")
            return output_path

        wrapper = create_model_wrapper(self.config)
        wrapper.load()

        prompts = df[prompt_col].astype(str).tolist()
        generated_answers: list[str] = []

        for start in tqdm(range(0, len(prompts), batch_size), desc="Generating"):
            batch_prompts = prompts[start : start + batch_size]
            batch_outputs = wrapper.generate_text(
                prompts=batch_prompts,
                max_new_tokens=max_new_tokens,
            )

            for prompt, full_output in zip(batch_prompts, batch_outputs):
                full_output = str(full_output)

                # Some wrappers decode full prompt+completion. If so, strip prompt.
                if full_output.startswith(prompt):
                    generated = full_output[len(prompt):].strip()
                else:
                    generated = full_output.strip()

                generated_answers.append(generated)

        df["generated_answer"] = generated_answers

        correct_flags = []
        strict_segments = []
        matched_answers = []

        for generated, correct in zip(df["generated_answer"], df[answer_col]):
            is_correct, segment, matched = strict_match(generated, correct)
            correct_flags.append(is_correct)
            strict_segments.append(segment)
            matched_answers.append(matched)

        df["is_correct"] = correct_flags
        df["strict_answer_segment"] = strict_segments
        df["strict_matched_answer"] = matched_answers
        df["model_name"] = self.config.model_name
        df["experiment_name"] = self.config.experiment_name

        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

        print("Saved:", output_path)
        print("Correct rows:", int(df["is_correct"].sum()))
        print("Wrong rows:", int((~df["is_correct"]).sum()))
        print("Accuracy:", float(df["is_correct"].mean()))

        return output_path
