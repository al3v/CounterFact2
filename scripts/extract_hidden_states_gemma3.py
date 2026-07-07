import argparse
import os
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM


EXPERIMENT_NAME = "counterfact_paraphrase_gemma3_4b_scope2_lasttoken"
REPORTS_DIR = f"reports/{EXPERIMENT_NAME}"


def to_bool(x):
    if isinstance(x, bool):
        return x
    return str(x).lower() in ["true", "1", "yes"]


def parse_layers(layer_string):
    return [int(x.strip()) for x in layer_string.split(",") if x.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=f"outputs/prompt_outputs_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument(
        "--pair-types",
        default=f"outputs/all_facts_pair_types_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument(
        "--output",
        default=f"outputs/hidden_states_{EXPERIMENT_NAME}.pt",
    )
    parser.add_argument(
        "--metadata-output",
        default=f"{REPORTS_DIR}/hidden_states_metadata_{EXPERIMENT_NAME}.csv",
    )
    parser.add_argument("--model-name", default="google/gemma-3-4b-pt")
    parser.add_argument("--layers", default="2,3,4,12,15,18")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--max-rows", type=int, default=None)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    os.makedirs(os.path.dirname(args.metadata_output), exist_ok=True)

    layers = parse_layers(args.layers)

    df = pd.read_csv(args.input)
    df["is_correct"] = df["is_correct"].apply(to_bool)

    if os.path.exists(args.pair_types):
        pair_df = pd.read_csv(args.pair_types)
        df = df.merge(pair_df[["fact_id", "pair_type"]], on="fact_id", how="left")
    else:
        df["pair_type"] = "unknown"

    if args.max_rows is not None:
        df = df.head(args.max_rows).copy()

    df = df.reset_index(drop=True)
    df["row_id"] = range(len(df))

    print("Input rows:", len(df))
    print("Facts:", df["fact_id"].nunique())
    print("Requested model layers:", layers)
    print("HF hidden-state indices:", {layer: layer + 1 for layer in layers})
    print("Model:", args.model_name)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.padding_side = "left"

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        dtype=torch.bfloat16,
        device_map="auto",
        attn_implementation="eager",
    )
    model.eval()

    input_device = next(model.parameters()).device

    print("Dtype:", next(model.parameters()).dtype)
    print("Input device:", input_device)
    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))

    all_hidden_batches = []
    metadata_rows = []

    prompts = df["prompt"].astype(str).tolist()

    for start in tqdm(range(0, len(df), args.batch_size)):
        batch_df = df.iloc[start:start + args.batch_size].copy()
        batch_prompts = prompts[start:start + args.batch_size]

        inputs = tokenizer(
            batch_prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        inputs = {k: v.to(input_device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(
                **inputs,
                output_hidden_states=True,
                use_cache=False,
            )

        hidden_states = outputs.hidden_states

        layer_vectors = []

        for layer in layers:
            # HF hidden_states[0] is embedding output.
            # Therefore model.layers.{layer}.output corresponds to hidden_states[layer + 1].
            hf_index = layer + 1

            if hf_index >= len(hidden_states):
                raise ValueError(
                    f"Requested model layer {layer}, which needs hidden_states[{hf_index}], "
                    f"but model returned only {len(hidden_states)} hidden-state entries."
                )

            vec = hidden_states[hf_index][:, -1, :].detach().cpu()
            layer_vectors.append(vec)

        batch_hidden = torch.stack(layer_vectors, dim=1)
        all_hidden_batches.append(batch_hidden)

        n_tokens = inputs["attention_mask"].sum(dim=1).detach().cpu().tolist()

        for i, (_, row) in enumerate(batch_df.iterrows()):
            for layer in layers:
                metadata_rows.append(
                    {
                        "row_id": int(row["row_id"]),
                        "fact_id": row["fact_id"],
                        "variant_id": row["variant_id"],
                        "layer": layer,
                        "hf_hidden_state_index": layer + 1,
                        "pair_type": row["pair_type"],
                        "is_correct": bool(row["is_correct"]),
                        "subject": row["subject"],
                        "correct_answer": row["correct_answer"],
                        "target_new": row["target_new"],
                        "prompt": row["prompt"],
                        "generated_answer": row["generated_answer"],
                        "n_tokens": int(n_tokens[i]),
                    }
                )

        del outputs
        del hidden_states

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    activations = torch.cat(all_hidden_batches, dim=0)

    save_obj = {
        "experiment_name": EXPERIMENT_NAME,
        "model_name": args.model_name,
        "layers": layers,
        "hf_hidden_state_indices": {layer: layer + 1 for layer in layers},
        "activation_type": "last_prompt_token_resid_post",
        "activations": activations,
        "row_metadata": df.to_dict(orient="records"),
    }

    torch.save(save_obj, args.output)

    metadata_df = pd.DataFrame(metadata_rows)
    metadata_df.to_csv(args.metadata_output, index=False)

    print()
    print("Saved hidden states:", args.output)
    print("Activation tensor shape:", tuple(activations.shape))
    print("Saved metadata:", args.metadata_output)
    print("Metadata rows:", len(metadata_df))


if __name__ == "__main__":
    main()
