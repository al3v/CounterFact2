# ADL SAE Controlled QA Experiment

The project is about checking how small changes in a factual question can affect the answer of a language model. I use Gemma 2B and then look inside the model using hidden states and Sparse Autoencoder features.

## Goal of the project

The main question I wanted to test was:

Can very small surface/tokenization changes in a question make the model switch between a correct and wrong factual answer?

And if that happens:

Can we also see this change inside the model representations?

So the project is not only about checking the final generated answer. I also compare the internal representations of the model.

## Experiment idea

I started from factual QA examples and created controlled prompt variants.

For each factual question, I used small changes such as:

- original question
- leading space
- trailing space
- space before the question mark
- no question mark
- lowercased first character
- double space after the first word

The meaning of the question is almost the same, but the exact input string changes. This can also change tokenization, so the model may process the prompt slightly differently.

The prompt format was kept fixed as:

Question: ...
Answer:

## Strict grading

The model sometimes continued generating extra text, for example another Question: after the first answer.

Because of that, I graded only the first answer segment.

So instead of grading the whole generated continuation, I cut the output before the next generated question and then checked whether the expected answer appeared in the first answer segment.

This made the grading stricter and more fair.

## Final dataset summary

In the final strict setup:

- 60 facts were tested
- 420 prompt rows were generated
- 167 rows were correct after strict grading
- 253 rows were wrong after strict grading
- 13 facts showed switching behavior
- The switching facts contained 91 prompt rows
- Among the switching rows, 48 were correct and 43 were wrong

Here, switching means that different variants of the same factual question led to different correctness outcomes.

For example, one variant was answered correctly, while another variant of the same question was answered wrongly.

## Internal representation analysis

After finding the switching facts, I extracted hidden states from Gemma 2B.

I used layers:

- 6
- 9
- 12

For each prompt variant, I saved the last-token activation.

I used this because the last prompt token is close to the point where the model starts generating the answer.

Then I compared distances between prompt variants.

The pair types were:

- correct_correct: both variants were answered correctly
- correct_wrong: one variant was correct and the other was wrong
- wrong_wrong: both variants were wrong

The main comparison was:

correct_wrong distance > correct_correct distance

This means that variants where correctness changes are usually farther apart internally than variants where both answers stay correct.

## SAE feature analysis

I also encoded the hidden states using Gemma Scope Sparse Autoencoders.

This gives sparse feature activations instead of only raw hidden-state vectors.

I compared the same pair types again in SAE feature space using:

- SAE cosine distance
- SAE L2 distance
- active Jaccard distance

The same pattern also appeared in SAE space:

correct_wrong distance > correct_correct distance

So the switching behavior is not only visible in the final answer, but also in internal model representations.

## Main result

The main result is:

Small surface/tokenization changes can affect factual answer correctness in Gemma 2B, and these correctness switches are reflected in hidden-state and SAE feature-space distances.

More carefully, I do not claim that tokenization alone causes hallucination.

A safer conclusion is that the model shows surface/tokenization sensitivity.

## Important files

data/prompt_variants.csv

The input factual QA source used to recreate the controlled dataset.

data/controlled/controlled_qa_prompt_variants.csv

The final controlled prompt variant dataset.

reports/controlled_qa_base_v4_strict/results_summary_controlled_qa_base_v4_strict.md

Main result summary with the final numbers.

reports/controlled_qa_base_v4_strict/qa_readable_review_controlled_qa_base_v4_strict.md

Readable review of switching facts, model answers, expected answers, and correctness labels.

reports/controlled_qa_base_v4_strict/activation_pair_type_mean_summary_controlled_qa_base_v4_strict.csv

Mean hidden-state distances by layer and pair type.

reports/controlled_qa_base_v4_strict/activation_pair_type_distances_controlled_qa_base_v4_strict.png

Hidden-state distance plot.

reports/controlled_qa_base_v4_strict/sae_pair_type_summary_controlled_qa_base_v4_strict.csv

SAE feature-space distance summary.

reports/controlled_qa_base_v4_strict/sae_pair_type_distances_controlled_qa_base_v4_strict.png

SAE feature-space distance plot.

## How to rerun

The main pipeline is in the scripts folder.

The rough order is:

python scripts/create_controlled_qa_prompt_variants.py
python scripts/run_prompt_variants.py
python scripts/regrade_prompt_outputs_strict.py --input outputs/prompt_outputs_controlled_qa_base_v4_strict_raw.csv --output outputs/prompt_outputs_controlled_qa_base_v4_strict.csv
python scripts/create_clean_switching_subset.py
python scripts/analyze_tokenization.py
python scripts/extract_hidden_states.py
python scripts/analyze_activation_pair_types.py
python scripts/plot_activation_pair_distances.py
python scripts/extract_sae_features.py
python scripts/analyze_sae_pair_types.py
python scripts/plot_sae_pair_distances.py

Some steps need a GPU, especially model generation, hidden-state extraction, and SAE feature extraction.
