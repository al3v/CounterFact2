# CounterFact data used in this experiment

This folder contains the CounterFact-based input data for the Gemma 3 SAE experiment.

The main file is:

`counterfact_paraphrase_prompts_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv`

This file was created from the Hugging Face dataset:

`azhx/counterfact`

## What the file contains

I used the CounterFact test split.

- CounterFact test facts: 2191
- Paraphrase prompts per fact: 2
- Total prompt rows: 4382

Each row is one paraphrase prompt given to Gemma 3.

## Important columns

`fact_id`

One CounterFact case.

`case_id`

Original CounterFact case ID.

`subject`

The entity of the factual statement.

`template`

The original CounterFact prompt template.

`base_prompt`

The template filled with the subject.

`variant_id`

The paraphrase prompt ID. In this setup it is usually `paraphrase_00` or `paraphrase_01`.

`prompt`

The actual prompt given to Gemma 3.

`correct_answer` / `target_true`

The real factual answer. This is used for grading.

`target_new`

The counterfactual alternative from CounterFact. This is kept for reference, but it is not used as the correct factual answer.

## Note about weird prompts

Some prompts look strange because CounterFact paraphrase prompts often include noisy Wikipedia-style context before the actual factual completion prompt.

Example structure:

random context + factual completion prompt

These prompts are kept unchanged because they come directly from the official `paraphrase_prompts` field of CounterFact.
