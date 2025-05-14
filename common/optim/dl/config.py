from dataclasses import dataclass, field
from typing import Any

from hydra_zen import make_config
from lightning.pytorch import Trainer
from lightning.pytorch.loggers.wandb import WandbLogger

from common.optim.config import OptimizationSubtaskConfig
from common.optim.dl.datamodule import BaseDataModule, BaseDataModuleConfig
from common.optim.dl.litmodule import BaseLitModule
from common.utils.hydra_zen import generate_config, generate_config_partial


@dataclass
class DeepLearningSubtaskConfig(OptimizationSubtaskConfig):
    """Deep Learning ``subtask`` config.

    Args:
        compile: Whether to compile the :class:`.BaseLitModule`
            before training. Requires
            :paramref:`OptimizationSubtaskConfig.device` to be set to
            ``"gpu"`` & a CUDA 7+ compatible GPU.
        save_every_n_train_steps: The frequency at which to save
            training checkpoints.
        ckpt_path: The path to a checkpoint to resume training from.
    """

    compile: bool = False
    save_every_n_train_steps: int | None = 1
    ckpt_path: str | None = "last"


@dataclass
class DeepLearningTaskConfig(
    make_config(  # type: ignore[misc]
        trainer=generate_config_partial(Trainer),
        datamodule=generate_config(
            BaseDataModule,
            config=BaseDataModuleConfig(),
        ),
        litmodule=generate_config(BaseLitModule),
        logger=generate_config_partial(WandbLogger),
        config=generate_config(DeepLearningSubtaskConfig),
    ),
):
    defaults: list[Any] = field(
        default_factory=lambda: [
            "_self_",
            {"trainer": "base"},
            {"litmodule/nnmodule": "mlp"},
            {"litmodule/scheduler": "constant"},
            {"litmodule/optimizer": "adamw"},
            {"logger": "wandb_simexp"},
            "project",
            "task",
            {"task": None},
        ],
    )
