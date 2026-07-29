from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentConfig:
    experiment_name: str
    model_family: str
    model_name: str
    sae_release: str
    sae_width: int
    layers: tuple[int, ...]
    outputs_dir: str = "outputs"
    reports_root: str = "reports"
    data_dir: str = "data/counterfact"
    torch_dtype: str = "bfloat16"
    device_map: str = "auto"
    padding_side: str = "left"
    trust_remote_code: bool = False

    @property
    def reports_dir(self) -> str:
        return f"{self.reports_root}/{self.experiment_name}"

    @property
    def prompt_outputs_path(self) -> str:
        return f"{self.outputs_dir}/prompt_outputs_{self.experiment_name}.csv"

    @property
    def all_pair_types_path(self) -> str:
        return f"{self.outputs_dir}/all_facts_pair_types_{self.experiment_name}.csv"

    @property
    def switching_facts_path(self) -> str:
        return f"{self.outputs_dir}/switching_facts_{self.experiment_name}.csv"

    @property
    def hidden_states_path(self) -> str:
        return f"{self.outputs_dir}/hidden_states_{self.experiment_name}.pt"

    @property
    def hidden_states_metadata_path(self) -> str:
        return f"{self.reports_dir}/hidden_states_metadata_{self.experiment_name}.csv"

    @property
    def hidden_states_metadata_path(self) -> str:
        return f"{self.reports_dir}/hidden_states_metadata_{self.experiment_name}.csv"

    @property
    def sae_active_features_path(self) -> str:
        return f"{self.outputs_dir}/sae_active_features_{self.experiment_name}.csv"


def get_counterfact_gemma3_config() -> ExperimentConfig:
    return ExperimentConfig(
        experiment_name="counterfact_paraphrase_gemma3_4b_scope2_lasttoken",
        model_family="gemma",
        model_name="google/gemma-3-4b-pt",
        sae_release="google/gemma-scope-2-4b-pt",
        sae_width=16384,
        layers=(2, 3, 4, 12, 15, 18),
    )


def get_counterfact_qwen25_config() -> ExperimentConfig:
    return ExperimentConfig(
        experiment_name="counterfact_paraphrase_qwen25_3b_lasttoken",
        model_family="qwen",
        model_name="Qwen/Qwen2.5-3B-Instruct",
        sae_release="none",
        sae_width=0,
        layers=(2, 3, 4, 12, 18, 24),
        trust_remote_code=True,
    )


def get_counterfact_llama32_config() -> ExperimentConfig:
    return ExperimentConfig(
        experiment_name="counterfact_paraphrase_llama32_3b_lasttoken",
        model_family="llama",
        model_name="meta-llama/Llama-3.2-3B-Instruct",
        sae_release="none",
        sae_width=0,
        layers=(2, 3, 4, 12, 18, 24),
    )

