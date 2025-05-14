from typing import Any

from hydra_zen import ZenStore

from common.optim.dl.litmodule import BaseLitModule

from .config import LightningInferenceSubtaskConfig
from .infer import infer
from .runner import InferTaskRunner


class LightningInferTaskRunner(InferTaskRunner):

    @classmethod
    def store_configs(
        cls: type["LightningInferTaskRunner"],
        store: ZenStore,
    ) -> None:
        """Stores structured configs.

        .. warning::

            Make sure to call this method if you are overriding it.

        Args:
            store:
                See :paramref:`~.OptimTaskRunner.store_configs.store`.
        """
        super().store_configs(store)
        store_basic_nnmodule_config(store)  # noqa: F821
        store(LightningInferenceSubtaskConfig, name="config")

    @classmethod
    def run_subtask(
        cls: type["LightningInferTaskRunner"],
        litmodule: BaseLitModule,
        config: LightningInferenceSubtaskConfig,
    ) -> Any:  # noqa: ANN401
        """Runs the ``subtask``."""
        return infer(litmodule, config)
