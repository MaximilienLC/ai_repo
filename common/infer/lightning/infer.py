from functools import partial

from common.infer.lightning.config import LightningInferenceSubtaskConfig
from common.optim.dl.litmodule import BaseLitModule
from common.utils.misc import seed_all


def infer(
    litmodule: partial[BaseLitModule],  # noqa: ARG001
    config: LightningInferenceSubtaskConfig,
) -> float:
    seed_all(config.seed)
    return 0
