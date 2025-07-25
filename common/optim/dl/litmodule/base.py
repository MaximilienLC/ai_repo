from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass
from functools import partial
from typing import Annotated as An
from typing import Any, final

import wandb
from jaxtyping import Num
from lightning.pytorch import LightningModule
from torch import Tensor, nn
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LRScheduler

from common.utils.beartype import ge, one_of


@dataclass
class BaseLitModuleConfig:
    """.

    Args:
        wandb_train_log_interval: `0` means no logging.
    """

    wandb_column_names: list[str]
    wandb_train_log_interval: An[int, ge(0)] = 50
    wandb_num_samples: An[int, ge(1)] = 3


class BaseLitModule(LightningModule, ABC):
    """.

    We propose to split the PyTorch module definition from the
    Lightning module definition for (arguably) better code organization,
    reuse & readability. As a result, each Lightning module receives a
    PyTorch module as an argument which it turns into an instance
    attribute. This is despite the fact that Lightning modules
    subclass PyTorch modules, and thus allow PyTorch module method
    definitions in the Lightning module.
    """

    def __init__(
        self: "BaseLitModule",
        config: BaseLitModuleConfig,
        nnmodule: nn.Module,
        optimizer: partial[Optimizer],
        scheduler: partial[LRScheduler],
    ) -> None:
        super().__init__()
        self.config = config
        self.nnmodule = nnmodule
        self.optimizer_partial = optimizer
        self.scheduler_partial = scheduler
        self.curr_train_step = 0
        self.curr_val_epoch = 0
        self.initialize_wandb_objects()

    @final
    def initialize_wandb_objects(self: "BaseLitModule") -> None:
        create_wandb_table = lambda iter_type: wandb.Table(  # noqa: E731
            columns=[
                "data_idx",
                iter_type,
                *self.config.wandb_column_names,
            ],
        )
        self.wandb_train_table = create_wandb_table("train_step")  # type: ignore[no-untyped-call]
        self.wandb_val_table = create_wandb_table("val_epoch")  # type: ignore[no-untyped-call]
        self.wandb_train_data: list[dict[str, Any]] = []
        self.wandb_val_data: list[dict[str, Any]] = []

    def on_save_checkpoint(
        self: "BaseLitModule",
        checkpoint: dict[str, Any],
    ) -> None:
        checkpoint["curr_train_step"] = self.curr_train_step
        checkpoint["curr_val_epoch"] = self.curr_val_epoch
        return super().on_save_checkpoint(checkpoint)

    def on_load_checkpoint(
        self: "BaseLitModule",
        checkpoint: dict[str, Any],
    ) -> None:
        self.curr_train_step = checkpoint["curr_train_step"]
        self.curr_val_epoch = checkpoint["curr_val_epoch"]
        return super().on_load_checkpoint(checkpoint)

    def on_validation_end(self: "BaseLitModule") -> None:
        self.wandb_train_data = []
        self.wandb_val_data = []
        super().on_validation_end()

    def optimizer_step(
        self: "BaseLitModule",
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().optimizer_step(*args, **kwargs)
        if (
            self.config.wandb_train_log_interval
            and self.curr_train_step % self.config.wandb_train_log_interval
            == 0
        ):
            self.log_table(self.wandb_train_data, "train")
        self.curr_train_step += 1

    def on_validation_epoch_end(self: "BaseLitModule") -> None:
        super().on_validation_epoch_end()
        if self.config.wandb_train_log_interval:
            self.log_table(self.wandb_val_data, "val")
        self.curr_val_epoch += 1

    def update_wandb_data_before_log(
        self: "BaseLitModule",
        data: list[dict[str, Any]],
        stage: An[str, one_of("train", "val")],
    ) -> None: ...

    @final
    def log_table(
        self: "BaseLitModule",
        data: list[dict[str, Any]],
        stage: An[str, one_of("train", "val")],
    ) -> None:
        self.update_wandb_data_before_log(data, stage)
        if data is self.wandb_train_data:
            name = "train_data"
            table = self.wandb_train_table
            it = self.curr_train_step
        else:  # data is self.wandb_val_data
            name = "val_data"
            table = self.wandb_val_table
            it = self.curr_val_epoch
        for i, data_i in enumerate(data):
            table.add_data(
                i,
                it,
                *[data_i[key] for key in self.config.wandb_column_names],
            )
        # 1) Static type checking discrepancy:
        # `logger.experiment` is a `wandb.wandb_run.Run` instance.
        # 2) Cannot log the same table twice:
        # https://github.com/wandb/wandb/issues/2981#issuecomment-1458447291
        try:
            self.logger.experiment.log(  # type: ignore[union-attr]
                {name: copy(table)},
            )
        except Exception as e:
            error_msg = (
                "Failed to log validation data to W&B. "
                "You might be trying to log tensors."
            )
            raise ValueError(error_msg) from e

    @abstractmethod
    def step(  # type: ignore[no-untyped-def]
        self: "BaseLitModule",
        data,  # noqa: ANN001
        stage: An[str, one_of("train", "val", "test", "predict")],
    ) -> Num[Tensor, " *_"]:
        """.

        Returns:
            The loss value(s).
        """

    @final
    def stage_step(
        self: "BaseLitModule",
        data: Any,  # noqa: ANN401
        stage: An[str, one_of("train", "val", "test", "predict")],
    ) -> Num[Tensor, " *_"]:
        if isinstance(data, list):
            data = tuple(data)
        loss: Num[Tensor, " *_"] = self.step(data, stage)
        self.log(name=f"{stage}/loss", value=loss)
        return loss

    @final
    def training_step(
        self: "BaseLitModule",
        data: Any,  # noqa: ANN401
    ) -> Num[Tensor, " *_"]:
        return self.stage_step(data=data, stage="train")

    @final
    def validation_step(
        self: "BaseLitModule",
        data: Any,  # noqa: ANN401
        # :paramref:`*args` & :paramref:`**kwargs` type annotations
        # cannot be more specific because of
        # :meth:`LightningModule.validation_step`\'s signature.
        *args: Any,  # noqa: ANN401, ARG002
        **kwargs: Any,  # noqa: ANN401, ARG002
    ) -> Num[Tensor, " *_"]:
        return self.stage_step(data=data, stage="val")

    @final
    def test_step(
        self: "BaseLitModule",
        data: Any,  # noqa: ANN401
    ) -> Num[Tensor, " *_"]:
        return self.stage_step(data=data, stage="test")

    @final
    def configure_optimizers(
        self: "BaseLitModule",
    ) -> tuple[list[Optimizer], list[LRScheduler]]:
        self.optimizer = self.optimizer_partial(params=self.parameters())
        self.scheduler = self.scheduler_partial(optimizer=self.optimizer)
        return [self.optimizer], [self.scheduler]
