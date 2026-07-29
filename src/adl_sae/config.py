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
