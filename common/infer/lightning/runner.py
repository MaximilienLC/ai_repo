from functools import partial
from typing import Any

from hydra_zen import ZenStore

from common.infer.runner import InferTaskRunner
from common.optim.dl.litmodule import BaseLitModule

from .config import LightningInferenceSubtaskConfig
from .infer import infer


class LightningInferTaskRunner(InferTaskRunner):

    @classmethod
    def store_configs(
        cls: type["LightningInferTaskRunner"],
        store: ZenStore,
    ) -> None:
        super().store_configs(store)
        store(LightningInferenceSubtaskConfig, name="config")

    @classmethod
    def run_subtask(
        cls: type["LightningInferTaskRunner"],
        litmodule: partial[BaseLitModule],
        config: LightningInferenceSubtaskConfig,
    ) -> Any:  # noqa: ANN401
        """Runs the ``subtask``."""
        return infer(litmodule, config)
