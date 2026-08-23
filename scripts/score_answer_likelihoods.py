from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import torch
import torch.nn.functional as F
from tqdm import tqdm

from adl_sae.config_registry import add_config_argument, get_config
from adl_sae.model.registry import create_model_wrapper


def find_answer_token_positions(offsets, attention_mask, answer_start_char, answer_end_char):
    """
    Find token positions in full_text that overlap with the answer character span.

    A token belongs to the answer if:
    token_end > answer_start_char and token_start < answer_end_char

    This is safer than separately tokenizing prompt and answer, because BPE/SentencePiece
    tokenization can change at the prompt-answer boundary.
    """
    positions = []

    for pos, ((start, end), mask_value) in enumerate(zip(offsets, attention_mask)):
        if int(mask_value) == 0:
            continue

        # Skip special tokens, usually offset (0, 0)
        if int(start) == 0 and int(end) == 0:
            continue

        if int(end) > answer_start_char and int(start) < answer_end_char:
            positions.append(pos)

    return positions


def score_batch(model, tokenizer, batch_df, device):
    full_texts = batch_df["full_text"].astype(str).tolist()

    enc = tokenizer(
        full_texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        return_offsets_mapping=True,
    )

    offset_mapping = enc.pop("offset_mapping")
    input_ids = enc["input_ids"]
    attention_mask = enc["attention_mask"]

    model_inputs = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        outputs = model(**model_inputs, use_cache=False)

    logits = outputs.logits.float().cpu()
    input_ids_cpu = input_ids.cpu()
    attention_mask_cpu = attention_mask.cpu()
    offset_mapping_cpu = offset_mapping.cpu()

    rows = []

    for local_i, (_, row) in enumerate(batch_df.iterrows()):
        prompt_text = str(row["prompt_text"])
        answer_text = str(row["answer_text_for_scoring"])
        full_text = str(row["full_text"])

        answer_start_char = len(prompt_text)
        answer_end_char = len(full_text)

        offsets = offset_mapping_cpu[local_i].tolist()
        mask = attention_mask_cpu[local_i].tolist()

        answer_positions = find_answer_token_positions(
            offsets=offsets,
            attention_mask=mask,
            answer_start_char=answer_start_char,
            answer_end_char=answer_end_char,
        )

        token_logprobs = []
        token_ids = []
        token_texts = []
        token_offsets = []

        for pos in answer_positions:
            if pos == 0:
                # Cannot score token at position 0 because there is no previous-token logit.
                continue

            token_id = int(input_ids_cpu[local_i, pos].item())
            prev_logits = logits[local_i, pos - 1, :]
            log_probs = F.log_softmax(prev_logits, dim=-1)
            token_logprob = float(log_probs[token_id].item())

            token_ids.append(token_id)
            token_logprobs.append(token_logprob)
            token_offsets.append(offsets[pos])

            try:
                token_text = tokenizer.decode([token_id], skip_special_tokens=False)
            except Exception:
                token_text = ""

            token_texts.append(token_text)

        if len(token_logprobs) == 0:
            score = float("nan")
            sum_logprob = float("nan")
        else:
            sum_logprob = float(sum(token_logprobs))
            score = float(sum_logprob / len(token_logprobs))

        out = row.to_dict()
        out.update(
            {
                "answer_start_char": answer_start_char,
                "answer_end_char": answer_end_char,
                "answer_token_positions": json.dumps(answer_positions),
                "answer_token_ids": json.dumps(token_ids),
                "answer_token_texts": json.dumps(token_texts, ensure_ascii=False),
                "answer_token_offsets": json.dumps(token_offsets),
                "answer_token_logprobs": json.dumps(token_logprobs),
                "n_answer_tokens": len(token_logprobs),
                "sum_answer_logprob": sum_logprob,
                "score_S": score,
            }
        )

        rows.append(out)

    return rows


def build_margin_tables(scores_df: pd.DataFrame, config):
    true_df = scores_df[scores_df["answer_type"] == "true"].copy()
    cf_df = scores_df[scores_df["answer_type"] == "counterfactual"].copy()

    key = "original_row_id"

    true_small = true_df[[key, "score_S"]].rename(columns={"score_S": "S_true"})
    cf_small = cf_df[[key, "score_S"]].rename(columns={"score_S": "S_counterfactual"})

    margins = true_df.drop(columns=["score_S"]).merge(true_small, on=key, how="left")
    margins = margins.merge(cf_small, on=key, how="left")

    margins["M_cf"] = margins["S_true"] - margins["S_counterfactual"]

    # Keep one row per original prompt.
    keep_cols_first = [
        "original_row_id",
        "fact_id",
        "case_id",
        "split",
        "relation_id",
        "subject",
        "variant_id",
        "prompt_text",
        "raw_answer_text",
        "target_true",
        "target_new",
        "correct_answer",
        "generated_answer",
        "is_correct",
        "pair_type",
        "S_true",
        "S_counterfactual",
        "M_cf",
    ]
    keep_cols = [c for c in keep_cols_first if c in margins.columns]
    margins = margins[keep_cols].copy()

    delta_rows = []

    if "pair_type" in margins.columns and "fact_id" in margins.columns and "is_correct" in margins.columns:
        psk = margins[margins["pair_type"] == "correct_wrong"].copy()

        for fact_id, group in psk.groupby("fact_id"):
            correct_rows = group[group["is_correct"].astype(str).str.lower().isin(["true", "1"])]
            wrong_rows = group[group["is_correct"].astype(str).str.lower().isin(["false", "0"])]

            if len(correct_rows) != 1 or len(wrong_rows) != 1:
                continue

            success = correct_rows.iloc[0]
            failure = wrong_rows.iloc[0]

            delta_rows.append(
                {
                    "fact_id": fact_id,
                    "success_original_row_id": success["original_row_id"],
                    "failure_original_row_id": failure["original_row_id"],
                    "success_variant_id": success.get("variant_id", ""),
                    "failure_variant_id": failure.get("variant_id", ""),
                    "M_success": success["M_cf"],
                    "M_failure": failure["M_cf"],
                    "delta_M": success["M_cf"] - failure["M_cf"],
                    "S_true_success": success["S_true"],
                    "S_true_failure": failure["S_true"],
                    "S_counterfactual_success": success["S_counterfactual"],
                    "S_counterfactual_failure": failure["S_counterfactual"],
                    "pair_type": "correct_wrong",
                }
            )

    delta_margins = pd.DataFrame(delta_rows)

    reports_dir = Path(config.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    margins_path = reports_dir / f"factual_margins_{config.experiment_name}.csv"
    delta_path = reports_dir / f"delta_margins_{config.experiment_name}.csv"

    margins.to_csv(margins_path, index=False)
    delta_margins.to_csv(delta_path, index=False)

    return margins_path, delta_path, margins, delta_margins


def main():
    parser = argparse.ArgumentParser(
        description="Compute length-normalized answer log-likelihood scores S(answer | prompt)."
    )
    add_config_argument(parser)
    parser.add_argument("--input-path", default=None)
    parser.add_argument("--output-path", default=None)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-rows", type=int, default=None)
    args = parser.parse_args()

    config = get_config(args.config)

    input_path = (
        Path(args.input_path)
        if args.input_path is not None
        else Path(config.outputs_dir) / f"answer_augmented_prompts_{config.experiment_name}.csv"
    )

    output_path = (
        Path(args.output_path)
        if args.output_path is not None
        else Path(config.outputs_dir) / f"answer_likelihood_scores_{config.experiment_name}.csv"
    )

    if not input_path.exists():
        raise FileNotFoundError(f"Answer-augmented prompt file not found: {input_path}")

    df = pd.read_csv(input_path)

    if args.max_rows is not None:
        df = df.head(args.max_rows).copy()

    required = ["full_text", "prompt_text", "answer_text_for_scoring", "answer_type", "original_row_id"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    print("=== Answer likelihood scoring ===")
    print("Experiment:", config.experiment_name)
    print("Model:", config.model_name)
    print("Input:", input_path)
    print("Rows:", len(df))
    print("Batch size:", args.batch_size)
    print("Output:", output_path)

    wrapper = create_model_wrapper(config)
    wrapper.load()

    tokenizer = wrapper.tokenizer
    model = wrapper.model
    device = wrapper._get_input_device()

    all_rows = []

    for start in tqdm(range(0, len(df), args.batch_size), desc="Scoring"):
        batch_df = df.iloc[start : start + args.batch_size].copy()
        all_rows.extend(
            score_batch(
                model=model,
                tokenizer=tokenizer,
                batch_df=batch_df,
                device=device,
            )
        )

    scores_df = pd.DataFrame(all_rows)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    scores_df.to_csv(output_path, index=False)

    margins_path, delta_path, margins, delta_margins = build_margin_tables(scores_df, config)

    print()
    print("Saved answer likelihood scores:", output_path)
    print("Saved factual margins:", margins_path)
    print("Saved delta margins:", delta_path)

    print()
    print("Score summary by answer_type:")
    print(scores_df.groupby("answer_type")["score_S"].describe())

    print()
    print("Margin preview:")
    print(margins.head(8).to_string(index=False))

    print()
    print("Delta margin preview:")
    if delta_margins.empty:
        print("No correct_wrong pairs found or not enough paired rows.")
    else:
        print(delta_margins.head(8).to_string(index=False))


if __name__ == "__main__":
    main()
