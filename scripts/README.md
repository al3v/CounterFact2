# Scripts

This folder contains the final controlled QA experiment pipeline.

## Pipeline order

1. `create_controlled_qa_prompt_variants.py`  
   Creates controlled prompt variants from factual QA examples.

2. `run_prompt_variants.py`  
   Runs Gemma 2B on the controlled QA prompts.

3. `regrade_prompt_outputs_strict.py`  
   Strictly grades model outputs using only the first answer segment.

4. `create_clean_switching_subset.py`  
   Keeps facts where some prompt variants are correct and others are wrong.

5. `analyze_tokenization.py`  
   Checks how prompt variants differ at tokenizer level.

6. `extract_hidden_states.py`  
   Extracts model hidden states for selected layers.

7. `analyze_activation_distances.py` and `analyze_activation_pair_types.py`  
   Compare hidden-state distances between correct-correct, correct-wrong, and wrong-wrong pairs.

8. `plot_activation_pair_distances.py`  
   Creates the hidden-state distance plot.

9. `extract_sae_features.py`  
   Applies SAE feature extraction to the hidden states.

10. `analyze_sae_pair_types.py`  
   Compares SAE feature-space distances between pair types.

11. `plot_sae_pair_distances.py`  
   Creates the SAE distance plot.
