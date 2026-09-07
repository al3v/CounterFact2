# Qwen3 SAE full-run verification outputs

This folder contains compact verification outputs for the full Qwen3 SAE run.

The full raw outputs are not duplicated here because some files are very large, especially the SAE active feature table. Instead, this folder contains summaries and small samples that verify the full run completed and that the requested columns are present.

Full run:
- Model: Qwen/Qwen3-1.7B-Base
- Experiment: counterfact_paraphrase_qwen3_17b_sae_lasttoken
- Layers: 2, 3, 4, 12, 18, 24
- Slurm state: COMPLETED
- ExitCode: 0:0
- Elapsed: 00:40:32

Main verification points:
- Prompt rows: 4382
- Hidden shape: 4382 x 6 x 2048
- SAE active feature rows: 2629200
- Answer likelihood rows: 8764
- Prompt token metadata present:
  - prompt_token_ids
  - last_nonpad_position
  - final_prompt_token_id
- Raw likelihood columns present:
  - score_S
  - length_normalized_log_likelihood
  - sum_answer_logprob
  - sequence_log_likelihood
  - answer_token_logprobs
- Margin columns present:
  - S_true
  - S_counterfactual
  - M_cf
  - length_normalized_log_likelihood_true
  - length_normalized_log_likelihood_counterfactual
  - sequence_log_likelihood_true
  - sequence_log_likelihood_counterfactual
  - sequence_log_likelihood_margin

Files:
- qwen_full_run_verification_checks.csv: compact checklist of all verification results
- qwen_pair_type_rows_summary.csv: row-level pair type counts
- qwen_pair_type_facts_summary.csv: fact-level pair type counts
- qwen_likelihood_summary_by_answer_type.csv: raw likelihood summary by true/counterfactual answer
- qwen_margin_summary.csv: factual margin summary
- qwen_sae_active_rows_by_layer.csv: SAE active feature row counts per layer
- sample_prompt_outputs_head20.csv: small sample of generation output
- sample_prompt_token_metadata_head20.csv: small sample of token metadata
- sample_answer_likelihood_scores_head20.csv: small sample of answer likelihood scores
- sample_factual_margins_head20.csv: small sample of factual margins
- sample_delta_margins_head20.csv: small sample of delta margins
- sample_sae_active_features_head100.csv: small sample of SAE active features
