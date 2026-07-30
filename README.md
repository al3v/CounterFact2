# CounterFact Paraphrase Sensitivity with Gemma 3 and SAE Features

This project is about checking whether Gemma 3 gives the same factual answer when the same fact is asked with different paraphrases.

The main idea is simple:

```text
same fact
two different paraphrases
Gemma gives answers
answers are checked as correct or wrong
internal representations are compared with SAE features
```

The current experiment uses:

```text
Dataset: CounterFact paraphrase prompts
Model: google/gemma-3-4b-pt
SAE: google/gemma-scope-2-4b-pt
Layers: 2, 3, 4, 12, 15, 18
SAE width: 16384
```

## Project goal

The goal is to see whether answer changes caused by paraphrasing are also visible inside the model.

For every fact, there are two paraphrase prompts.

Each fact is grouped into one of these groups:

```text
correct_correct = both paraphrases are answered correctly
wrong_wrong     = both paraphrases are answered wrongly
correct_wrong   = one paraphrase is correct and the other one is wrong
```

The most interesting group is:

```text
correct_wrong
```

because this means the model knows the answer in one wording, but fails in another wording.

This group is called the switching group.

## Main result

The main result is:

```text
correct_wrong pairs usually have larger SAE representation distances
than stable correct_correct pairs
```

This means that when the model changes from correct to wrong between two paraphrases, the sparse SAE feature representation also changes more strongly.

Important: this is only an association.

It should not be said that the SAE features caused the wrong answer, because no feature intervention was done.

Better wording:

```text
Paraphrase-induced correctness switches are associated with larger internal representation shifts.
```

## Refactored code structure

The code is now organized as a Python package under:

```text
src/adl_sae/
```

Current structure:

```text
CounterFact2/
│
├── pyproject.toml
├── README.md
│
├── scripts/
│   ├── run_pair_types.py
│   ├── run_hidden_states.py
│   ├── run_sae_extraction.py
│   ├── run_sae_feature_analysis.py
│   ├── run_pair_distances.py
│   ├── run_pair_distance_plots.py
│   └── run_pipeline.py
│
├── src/
│   └── adl_sae/
│       ├── config.py
│       │
│       ├── data/
│       │   └── pair_types.py
│       │
│       ├── model/
│       │   ├── base.py
│       │   ├── hf_causal.py
│       │   ├── gemma.py
│       │   ├── qwen.py
│       │   ├── llama.py
│       │   └── registry.py
│       │
│       ├── worker/
│       │   ├── hidden_states.py
│       │   ├── sae_extraction.py
│       │   └── pipeline.py
│       │
│       └── analysis/
│           ├── pair_distances.py
│           ├── sae_features.py
│           └── plots.py
│
├── data/
├── outputs/
├── reports/
└── logs/
```

## What each folder does

### `src/adl_sae/config.py`

This file stores the central experiment settings.

Example:

```text
experiment_name = counterfact_paraphrase_gemma3_4b_scope2_lasttoken
model_family    = gemma
model_name      = google/gemma-3-4b-pt
sae_release     = google/gemma-scope-2-4b-pt
sae_width       = 16384
layers          = 2, 3, 4, 12, 15, 18
```

This makes the code easier to change later.

For example, if Qwen or Llama should be used later, the model config can be changed more cleanly.

### `src/adl_sae/model/`

This folder contains model wrapper code.

The structure is prepared for:

```text
Gemma
Qwen
Llama
```

Currently Gemma is used.

The model registry creates the correct wrapper from the config.

### `src/adl_sae/data/`

This folder contains dataset-related code.

Currently it contains:

```text
pair_types.py
```

This creates:

```text
correct_correct
correct_wrong
wrong_wrong
switching_facts
```

### `src/adl_sae/worker/`

This folder contains heavier processing steps.

Current files:

```text
hidden_states.py
sae_extraction.py
pipeline.py
```

`hidden_states.py` extracts hidden states from selected Gemma layers.

`sae_extraction.py` currently wraps the old SAE extraction script. This was done so the scientific logic is not accidentally changed during refactoring.

`pipeline.py` connects the steps together.

### `src/adl_sae/analysis/`

This folder contains analysis code.

Current files:

```text
pair_distances.py
sae_features.py
plots.py
```

`pair_distances.py` compares the two paraphrases of each fact in SAE feature space.

`sae_features.py` currently wraps the old SAE feature analysis script.

`plots.py` currently wraps the old plotting script.

## Installation

Install the package in editable mode:

```bash
pip install -e .
```

Then imports like this should work:

```python
from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.model.registry import create_model_wrapper
```

A quick test:

```bash
python - <<'PY'
from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.model.registry import create_model_wrapper

config = get_counterfact_gemma3_config()
wrapper = create_model_wrapper(config)

print("model_family:", config.model_family)
print("model_name:", config.model_name)
print("wrapper_class:", type(wrapper).__name__)
print("layers:", config.layers)
PY
```

Expected output:

```text
model_family: gemma
model_name: google/gemma-3-4b-pt
wrapper_class: GemmaWrapper
layers: (2, 3, 4, 12, 15, 18)
```

## Pipeline

A dry run of the pipeline can be done with:

```bash
python scripts/run_pipeline.py
```

This only prints the planned steps. It does not run the heavy GPU steps.

To run selected lightweight steps:

```bash
python scripts/run_pipeline.py --steps pair_types pair_distances plots --execute
```

To run only pair-type creation:

```bash
python scripts/run_pipeline.py --steps pair_types --execute
```

## Main runner scripts

### 1. Pair-type creation

```bash
python scripts/run_pair_types.py
```

This creates the files:

```text
outputs/all_facts_pair_types_*.csv
outputs/switching_facts_*.csv
reports/.../all_facts_pair_types_*.csv
reports/.../switching_facts_*.csv
```

Current result:

```text
correct_correct = 401 facts
correct_wrong   = 541 facts
wrong_wrong     = 1249 facts
```

So there are:

```text
541 switching facts
1082 switching rows
```

because each switching fact has two prompt rows.

### 2. Hidden-state extraction

```bash
python scripts/run_hidden_states.py
```

This extracts last-token hidden states from selected layers.

For the full experiment, the expected hidden-state tensor shape is:

```text
4382 x 6 x 2560
```

Meaning:

```text
4382 = prompt rows
6    = selected layers
2560 = Gemma hidden dimension
```

A small smoke test can be run with:

```bash
python scripts/run_hidden_states.py \
  --max-rows 2 \
  --batch-size 2 \
  --output-suffix smoke_test
```

Expected shape:

```text
Shape: (2, 6, 2560)
Rows: 12
```

Smoke-test output files should not be committed.

### 3. SAE extraction

Dry run:

```bash
python scripts/run_sae_extraction.py --dry-run
```

Full run:

```bash
python scripts/run_sae_extraction.py
```

This step converts Gemma hidden states into sparse SAE feature activations.

Currently this runner calls the older trusted SAE extraction script through a worker wrapper.

### 4. SAE feature analysis

Dry run:

```bash
python scripts/run_sae_feature_analysis.py --dry-run
```

Full run:

```bash
python scripts/run_sae_feature_analysis.py
```

This analyzes SAE activations by correctness group.

### 5. Pair-distance analysis

```bash
python scripts/run_pair_distances.py
```

This is one of the main analysis steps.

For each fact and layer, this compares:

```text
SAE activation vector of paraphrase_00
vs
SAE activation vector of paraphrase_01
```

The distances are:

```text
cosine_distance
l2_distance
jaccard_distance
n_shared_features
```

Mann-Whitney U test results are also saved as a CSV.

### 6. Pair-distance plots

Dry run:

```bash
python scripts/run_pair_distance_plots.py --dry-run
```

Full run:

```bash
python scripts/run_pair_distance_plots.py
```

This creates plots in:

```text
reports/.../plots/
```

## Important output files

Prompt outputs:

```text
outputs/prompt_outputs_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
```

Pair-type outputs:

```text
outputs/all_facts_pair_types_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
outputs/switching_facts_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
```

Hidden states:

```text
outputs/hidden_states_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.pt
reports/counterfact_paraphrase_gemma3_4b_scope2_lasttoken/hidden_states_metadata_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
```

SAE activations:

```text
outputs/sae_active_features_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
reports/counterfact_paraphrase_gemma3_4b_scope2_lasttoken/sae_prompt_summary_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
reports/counterfact_paraphrase_gemma3_4b_scope2_lasttoken/sae_global_feature_summary_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
```

Pair distances:

```text
reports/counterfact_paraphrase_gemma3_4b_scope2_lasttoken/sae_pair_distances_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
reports/counterfact_paraphrase_gemma3_4b_scope2_lasttoken/sae_pair_distance_summary_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
reports/counterfact_paraphrase_gemma3_4b_scope2_lasttoken/sae_pair_distance_mannwhitney_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
```

## How the pair-distance comparison works

Each prompt gets converted into a sparse SAE activation vector.

Example:

```text
paraphrase_00 -> [0, 0, 31.2, 0, 8.7, ...]
paraphrase_01 -> [0, 5.1, 12.4, 0, 0, ...]
```

Then the two vectors are compared.

For cosine distance, the code uses:

```python
from scipy.spatial.distance import cosine

cos_dist = float(cosine(vec_a, vec_b))
```

This SciPy function already returns cosine distance.

So internally it is:

```text
cosine distance = 1 - cosine similarity
```

A larger cosine distance means the two paraphrases have more different SAE activation patterns.

## Interpretation

The analysis does not directly compare only the generated text.

Instead, it compares internal representations:

```text
same fact
same layer
two paraphrases
two SAE activation vectors
```

The main question is:

```text
Are correct_wrong pairs farther apart than stable pairs?
```

The current result suggests yes.

However, this should be said carefully:

```text
Switching facts are associated with larger sparse representation shifts.
```

It should not be said as:

```text
These SAE features cause the wrong answer.
```

because no causal intervention was done.

## Current refactor status

Already moved into the new package structure:

```text
central config
model wrapper registry
pair-type creation
hidden-state extraction worker
pair-distance analysis
pipeline runner
```

Currently wrapped around older scripts:

```text
SAE extraction
SAE feature analysis
pair-distance plotting
```

This was done to keep the scientific outputs stable while the code is being cleaned.

A future step can move the internal SAE extraction and plotting logic fully into the package.

## Git note

After running:

```bash
pip install -e .
```

this folder may appear:

```text
src/adl_sae.egg-info/
```

It should not be committed.

It can be deleted with:

```bash
rm -rf src/adl_sae.egg-info
```

The `.gitignore` should include:

```text
*.egg-info/
```

## Environment setup

For a new environment, the package can be installed like this:

```bash
python -m venv ~/venvs/adl-sae
source ~/venvs/adl-sae/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

After installation, the package import can be tested with:

```bash
python - <<'PY'
from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.model.registry import create_model_wrapper

config = get_counterfact_gemma3_config()
wrapper = create_model_wrapper(config)

print("model_family:", config.model_family)
print("model_name:", config.model_name)
print("wrapper_class:", type(wrapper).__name__)
print("layers:", config.layers)
PY
```

Expected output:

```text
model_family: gemma
model_name: google/gemma-3-4b-pt
wrapper_class: GemmaWrapper
layers: (2, 3, 4, 12, 15, 18)
```

## Running the pipeline

A dry run can be used first. This only prints the planned steps and does not execute the heavy GPU parts:

```bash
python -u scripts/run_pipeline.py
```

Expected pipeline order:

```text
pair_types
hidden_states
sae_extraction
sae_feature_analysis
pair_distances
plots
```

A lightweight execution can be run with only the analysis steps:

```bash
python -u scripts/run_pipeline.py \
  --steps pair_types pair_distances plots \
  --execute
```

The full pipeline can be run with:

```bash
python -u scripts/run_pipeline.py --execute
```

This full command runs:

```text
pair_types
hidden_states
sae_extraction
sae_feature_analysis
pair_distances
plots
```

The full pipeline is GPU-heavy because hidden-state extraction and SAE extraction are included.

For safer testing, the full pipeline can be run in a temporary copy of the repo so the original outputs are not overwritten:

```bash
cd ~/CounterFact2-upload

TEST_DIR=~/CounterFact2-pipeline-test-$(date +%Y%m%d_%H%M)

rsync -a \
  --exclude ".git" \
  --exclude "logs" \
  --exclude "src/adl_sae.egg-info" \
  ~/CounterFact2-upload/ "$TEST_DIR"/

cd "$TEST_DIR"

pip install -e .

mkdir -p logs

python -u scripts/run_pipeline.py --execute \
  2>&1 | tee logs/full_pipeline_test.log
```

A successful full run should end with:

```text
Pipeline finished.
```

After testing, the temporary folder can be deleted with:

```bash
cd ~
rm -rf "$TEST_DIR"
```

## Running in a new environment

A new user can set up the repository like this:

```bash
git clone https://github.com/al3v/CounterFact2.git
cd CounterFact2

python -m venv ~/venvs/adl-sae
source ~/venvs/adl-sae/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

If large files are tracked with Git LFS, the following should also be run:

```bash
git lfs install
git lfs pull
```

The package installation can be tested with:

```bash
python - <<'PY'
from adl_sae.config import get_counterfact_gemma3_config
from adl_sae.model.registry import create_model_wrapper

config = get_counterfact_gemma3_config()
wrapper = create_model_wrapper(config)

print(config.model_name)
print(type(wrapper).__name__)
print(config.layers)
PY
```

Expected output:

```text
google/gemma-3-4b-pt
GemmaWrapper
(2, 3, 4, 12, 15, 18)
```

Before running the full pipeline, a dry run should be done:

```bash
python -u scripts/run_pipeline.py
```

This only prints the planned pipeline steps. It does not run the heavy GPU parts.

The full pipeline can be run with:

```bash
python -u scripts/run_pipeline.py --execute
```

The full pipeline runs the following steps:

```text
pair_types
hidden_states
sae_extraction
sae_feature_analysis
pair_distances
plots
```

Important requirements:

```text
GPU node
Hugging Face access to google/gemma-3-4b-pt
Hugging Face access to google/gemma-scope-2-4b-pt
required input CSV files
enough disk space
```

At the moment, the refactored pipeline starts from the generated Gemma prompt-output CSV:

```text
outputs/prompt_outputs_counterfact_paraphrase_gemma3_4b_scope2_lasttoken.csv
```

So this file must exist before the pipeline is executed. The pipeline can then recreate pair types, hidden states, SAE activations, analysis tables, and plots.

## Current model support status

The refactored code supports multiple experiment configs through the config registry.

Available configs:

- gemma3
- qwen25
- llama32

Example dry runs:

    python -u scripts/run_pipeline.py --config gemma3
    python -u scripts/run_pipeline.py --config qwen25 --steps hidden_states
    python -u scripts/run_pipeline.py --config llama32 --steps hidden_states

The current full SAE pipeline has been tested for the Gemma experiment:

    python -u scripts/run_pipeline.py --config gemma3 --execute

This Gemma pipeline uses:

- google/gemma-3-4b-pt
- google/gemma-scope-2-4b-pt

The Qwen and Llama configs are included to prepare the model side of the refactor. They use the same config/model-wrapper interface and are intended for generation and hidden-state extraction tests.

Important limitation:

The full SAE analysis is currently Gemma-specific.

This is because SAE extraction currently depends on Gemma Scope SAE files, Gemma-specific layer choices, and Gemma-specific SAE folder names. Running full SAE analysis for Qwen or Llama would require matching SAE releases, correct layer mappings, and compatible activation dimensions.

Current status:

Gemma:
- full SAE pipeline tested

Qwen/Llama:
- structurally prepared through config registry and model wrappers
- hidden-state smoke tests can be run
- full SAE analysis not integrated yet

Optional smoke test for Qwen hidden states:

    python -u scripts/run_hidden_states.py --config qwen25 --max-rows 2 --batch-size 2 --output-suffix qwen_smoke_test

Optional smoke test for Llama hidden states:

    python -u scripts/run_hidden_states.py --config llama32 --max-rows 2 --batch-size 2 --output-suffix llama_smoke_test

A Llama smoke test may require Hugging Face access approval/login because some Llama models are gated.

