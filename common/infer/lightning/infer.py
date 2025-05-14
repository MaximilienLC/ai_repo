from functools import partial

from common.optim.dl.config import DeepLearningSubtaskConfig
from common.optim.dl.litmodule import BaseLitModule
from common.utils.misc import seed_all


def infer(
    litmodule: partial[BaseLitModule],
    config: DeepLearningSubtaskConfig,
) -> float:
    seed_all(config.seed)
    litmodule = BaseLitModule.load_from_checkpoint(  # noqa: F841
        config.ckpt_path,
    )
