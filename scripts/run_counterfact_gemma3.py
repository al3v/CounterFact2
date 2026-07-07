import argparse
import os
import re
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"


def normalize_text(x):
    """
    Normalize text for simple factual completion grading.
    This makes matching more robust to capitalization and punctuation.

    Example:
    'Pope,' -> 'pope'
    'Africa.' -> 'africa'
    """
    x = str(x).lower().strip()
    x = x.replace("\n", " ")
    x = re.sub(r"\s+", " ", x)

    # replace punctuation with spaces
    x = re.sub(r"[^\w\s]", " ", x)

    x = re.sub(r"\s+", " ", x).strip()
    return x


def grade_counterfact_completion(generated_answer, correct_answer):
    """
    CounterFact prompts are completion-style prompts.

    Example:
        prompt:   Angola belongs to the continent of
        expected: Africa

    We check whether the true answer appears near the beginning of the
    generated continuation.
    """
    gen = str(generated_answer).strip()

    # use only the first line / beginning of generation
    first_line = gen.split("\n")[0].strip()

    # avoid matching answers that appear very late
    answer_segment = first_line[:160]

    norm_segment = normalize_text(answer_segment)
    norm_answer = normalize_text(correct_answer)

    if not norm_answer:
        return False, ""

    words = norm_segment.split()

    # only inspect the beginning of the generated continuation
    first_12_words = " ".join(words[:12])

    is_correct = (
        first_12_words == norm_answer
        or first_12_words.startswith(norm_answer + " ")
        or norm_answer in words[:12]
        or norm_answer in first_12_words
    )

    return bool(is_correct), correct_answer if is_correct else ""


def save_checkpoint(rows, output_path):
    if rows:
        pd.DataFrame(rows).to_csv(output_path, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=f"data/counterfact/counterfact_paraphrase_prompts_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument(
        "--output",
        default=f"outputs/prompt_outputs_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument("--model-name", default="google/gemma-3-4b-pt")
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-new-tokens", type=int, default=16)
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=200,
        help="Save partial CSV every N batches.",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Ignore existing output file and start generation from scratch.",
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    df = pd.read_csv(args.input)

    if args.max_rows is not None:
        df = df.head(args.max_rows).copy()

    # Resume logic:
    # If output already exists, skip rows already generated.
    already_done = set()
    rows = []

    if os.path.exists(args.output) and not args.no_resume:
        existing = pd.read_csv(args.output)

        if (
            len(existing) > 0
            and "fact_id" in existing.columns
            and "variant_id" in existing.columns
        ):
            rows = existing.to_dict(orient="records")
            already_done = set(zip(existing["fact_id"], existing["variant_id"]))
            print(f"Resuming: found {len(rows)} already-processed rows.")

    if already_done:
        mask = [
            (row["fact_id"], row["variant_id"]) not in already_done
            for _, row in df.iterrows()
        ]
        df_todo = df[mask].reset_index(drop=True)
    else:
        df_todo = df.reset_index(drop=True)

    print("Input rows total:", len(df))
    print("Already processed:", len(already_done))
    print("Remaining to process:", len(df_todo))
    print("Model:", args.model_name)

    if len(df_todo) == 0:
        print("Nothing left to process. Output is already complete.")
        return

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.padding_side = "left"

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        # eager is safer for later hook-based representation extraction
        attn_implementation="eager",
    )
    model.eval()

    input_device = next(model.parameters()).device

    if hasattr(model, "hf_device_map"):
        print("Device map:", model.hf_device_map)
    print("Dtype:", next(model.parameters()).dtype)
    print("Input device:", input_device)
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))

    prompts = df_todo["prompt"].astype(str).tolist()

    for batch_idx, start in enumerate(tqdm(range(0, len(df_todo), args.batch_size))):
        batch_df = df_todo.iloc[start : start + args.batch_size]
        batch_prompts = prompts[start : start + args.batch_size]

        inputs = tokenizer(
            batch_prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        inputs = {k: v.to(input_device) for k, v in inputs.items()}

        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        # With left padding, prompt_len is the padded prompt length.
        # Everything after prompt_len is newly generated tokens.
        prompt_len = inputs["input_ids"].shape[1]
        new_token_ids = output_ids[:, prompt_len:]
        generated_texts = tokenizer.batch_decode(new_token_ids, skip_special_tokens=True)

        for (_, row), generated_answer in zip(batch_df.iterrows(), generated_texts):
            is_correct, matched_answer = grade_counterfact_completion(
                generated_answer=generated_answer,
                correct_answer=row["correct_answer"],
            )

            out = row.to_dict()
            out["model_name"] = args.model_name
            out["generated_answer"] = generated_answer
            out["strict_answer_segment"] = str(generated_answer).split("\n")[0].strip()[:160]
            out["strict_matched_answer"] = matched_answer
            out["is_correct"] = is_correct
            rows.append(out)

        if (batch_idx + 1) % args.checkpoint_every == 0:
            save_checkpoint(rows, args.output)
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    out_df = pd.DataFrame(rows)
    out_df.to_csv(args.output, index=False)

    print()
    print("Saved:", args.output)
    print("Rows:", len(out_df))
    print("Correct:", int(out_df["is_correct"].sum()))
    print("Wrong:", int((~out_df["is_correct"]).sum()))
    print("Accuracy:", round(out_df["is_correct"].sum() / len(out_df) * 100, 2), "%")
    print("Facts:", out_df["fact_id"].nunique())


if __name__ == "__main__":
    main()
