# Smoke-test metadata and matrix outputs

This folder contains 20-row smoke-test outputs for the prompt SAE and answer-likelihood extraction update.

The files are included so the output format can be inspected directly in GitHub before running the full dataset.

Important note:
These are small smoke-test outputs only. Full-dataset outputs should not be committed unless explicitly needed, because the matrix files can become large.

## Experiments included

- counterfact_paraphrase_llama31_8b_sae_lasttoken
- counterfact_paraphrase_qwen3_17b_sae_lasttoken
- counterfact_paraphrase_gemma3_4b_scope2_lasttoken

Each experiment has its own folder under:

metadata/smoke_tests/<experiment_name>/

## 1. Prompt-answer metadata

File:

answer_augmented_prompts_<experiment_name>.csv

Purpose:

This file contains the constructed prompt + answer sequences.

For each fact, there are two paraphrased prompts and two answer choices:

- true answer
- counterfactual answer

Therefore, the constructed set is:

- prompt_1 + answer_true
- prompt_1 + answer_counterfactual
- prompt_2 + answer_true
- prompt_2 + answer_counterfactual

Important columns:

- original_row_id
- extended_id
- fact_id
- variant_id
- answer_type
- prompt_text
- raw_answer_text
- answer_text_for_scoring
- full_text
- added_space_before_answer
- source_experiment_name

Identifier logic:

original_row_id identifies the original prompt-only row.

extended_id identifies the extended prompt-answer row.

Example:

0__true
0__counterfactual
1__true
1__counterfactual

This makes it possible to reconstruct the four prompt-answer sequences belonging to the same fact.

## 2. Answer likelihood scores

File:

answer_likelihood_scores_<experiment_name>.csv

Purpose:

This file contains the log-softmax answer likelihood scores.

For each prompt + answer sequence, the answer tokens are identified inside the full tokenized sequence. The score is computed as the average log-probability of the answer tokens.

The score is called:

score_S

Important columns:

- extended_id
- original_row_id
- fact_id
- variant_id
- answer_type
- prompt_text
- answer_text_for_scoring
- full_text
- answer_start_char
- answer_end_char
- answer_token_positions
- answer_token_ids
- answer_token_texts
- answer_token_offsets
- answer_token_logprobs
- n_answer_tokens
- sum_answer_logprob
- score_S

The token positions and token ids are saved so the scored answer span can be checked later.

## 3. Factual margin table

File:

factual_margins_<experiment_name>.csv

Purpose:

This file contains one row per original prompt.

It compares the model score for the true answer against the model score for the counterfactual answer.

Important columns:

- original_row_id
- fact_id
- variant_id
- prompt_text
- target_true
- target_new
- is_correct
- pair_type
- S_true
- S_counterfactual
- M_cf

Margin definition:

M_cf = S_true - S_counterfactual

A larger positive value means that the model gives higher likelihood to the true answer than to the counterfactual answer for that prompt.

## 4. Delta margin table

File:

delta_margins_<experiment_name>.csv

Purpose:

This file contains one row per prompt-sensitive switching fact.

These are the facts where one paraphrase was answered correctly and the other paraphrase was answered incorrectly.

Important columns:

- fact_id
- success_original_row_id
- failure_original_row_id
- success_variant_id
- failure_variant_id
- M_success
- M_failure
- delta_M
- S_true_success
- S_true_failure
- S_counterfactual_success
- S_counterfactual_failure
- pair_type

Delta definition:

delta_M = M_success - M_failure

This table can be used later to compare how factual preference changes between the successful and failed paraphrase.

## 5. Prompt-only layer metadata

Files:

all_layers_metadata_<experiment_name>.csv
layer_<layer>_metadata.csv

Purpose:

These files connect prompt-only residual vectors and SAE activation vectors back to the original prompt metadata.

The intended indexing is:

fact_id x variant_id x layer

Important columns:

- row_id
- fact_id
- case_id
- split
- relation_id
- subject
- variant_id
- variant_source
- prompt
- correct_answer
- target_true
- target_new
- generated_answer
- is_correct
- pair_type
- layer
- residual_matrix_file
- sae_matrix_file

The per-layer metadata files correspond to one model layer.

The all-layers metadata file combines all extracted layers into one table.

## 6. Included matrix files

Folder:

metadata/smoke_tests/<experiment_name>/matrices/

Included files:

layer_<layer>_prompt_residuals.npz
layer_<layer>_sae_activations_sparse.npz

Purpose:

The prompt residual files contain the dense hidden-state residual vectors extracted at the final non-padding prompt token.

The SAE activation files contain sparse SAE activation matrices.

Matrix shapes:

Prompt residual matrix:

number_of_prompts x hidden_dim

SAE activation matrix:

number_of_prompts x sae_width

The SAE activation matrix is saved as a sparse CSR matrix.

Inactive SAE features are represented as implicit zeros.

Nonzero entries store active feature magnitudes.

These matrix files are included only for the small 20-row smoke tests so the output format can be inspected directly in GitHub.

## 7. How these files were generated

Prompt-only matrix export:

python scripts/export_prompt_layer_matrices.py --config <config_name>

Prompt-answer dataset creation:

python scripts/create_answer_augmented_prompts.py --config <config_name>

Answer likelihood scoring:

python scripts/score_answer_likelihoods.py --config <config_name>

The tested config names were:

- llama31_sae
- qwen3_sae
- gemma3
