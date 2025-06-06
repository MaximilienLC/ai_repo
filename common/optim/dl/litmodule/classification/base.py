""":class:`.BaseClassificationLitModule` & its config."""

from abc import ABC, abstractmethod
from collections.abc import Callable  # noqa: TC003
from dataclasses import dataclass, field
from typing import Annotated as An
from typing import Any, final

import torch
import torch.nn.functional as f
from jaxtyping import Float, Int
from torch import Tensor
from torchmetrics.classification import MulticlassAccuracy

from common.optim.dl.litmodule import BaseLitModule, BaseLitModuleConfig
from common.utils.beartype import ge, one_of


@dataclass
class BaseClassificationLitModuleConfig(BaseLitModuleConfig):
    """Holds :class:`BaseClassificationLitModule` config values.

    Args:
        num_classes
        wandb_columns
    """

    num_classes: An[int, ge(2)] = 2
    wandb_column_names: list[str] = field(
        default_factory=lambda: ["x", "y", "y_hat", "logits"],
    )


class BaseClassificationLitModule(BaseLitModule, ABC):
    """Base Classification ``LightningModule``.

    Ref: :class:`lightning.pytorch.core.LightningModule`

    Attributes:
        config (BaseClassificationLitModuleConfig)
        accuracy (torchmetrics.classification.MulticlassAccuracy)
        wandb_table (wandb.Table): A table to upload to W&B
            containing validation data.
    """

    def __init__(
        self: "BaseClassificationLitModule",
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        super().__init__(*args, **kwargs)
        self.config: BaseClassificationLitModuleConfig
        self.accuracy = MulticlassAccuracy(
            num_classes=self.config.num_classes,
        )
        self.to_wandb_media: Callable[..., Any] = lambda x: x

    @property
    @abstractmethod
    def wandb_media_x(self):  # type: ignore[no-untyped-def] # noqa: ANN201
        """Converts a tensor to a W&B media object."""

    @final
    def step(
        self: "BaseClassificationLitModule",
        data: tuple[
            Float[Tensor, " batch_size *x_dim"],
            Int[Tensor, " batch_size"],
        ],
        stage: An[str, one_of("train", "val", "test")],
    ) -> Float[Tensor, " "]:
        """Computes the model accuracy and cross entropy loss.

        Args:
            data: A tuple ``(x, y)`` where ``x`` is the input data and
                ``y`` is the target data.
            stage: See
                :paramref:`~.BaseLitModule.stage_step.stage`.

        Returns:
            The cross entropy loss.
        """
        x: Float[Tensor, " batch_size *x_dim"] = data[0]
        y: Int[Tensor, " batch_size"] = data[1]
        logits: Float[Tensor, " batch_size num_classes"] = self.nnmodule(x)
        y_hat: Int[Tensor, " batch_size"] = torch.argmax(input=logits, dim=1)
        accuracy: Float[Tensor, " "] = self.accuracy(preds=y_hat, target=y)
        self.log(name=f"{stage}/acc", value=accuracy)
        self.save_wandb_data(stage, x, y, y_hat, logits)
        return f.cross_entropy(input=logits, target=y)

    @final
    def save_wandb_data(
        self: "BaseClassificationLitModule",
        stage: An[str, one_of("train", "val", "test")],
        x: Float[Tensor, " batch_size *x_dim"],
        y: Int[Tensor, " batch_size"],
        y_hat: Int[Tensor, " batch_size"],
        logits: Float[Tensor, " batch_size num_classes"],
    ) -> None:
        """Saves rich data to be logged to W&B.

        Args:
            stage
            x
            y
            y_hat
            logits: The raw `num_classes` network outputs.
        """
        data = (
            self.wandb_train_data if stage == "train" else self.wandb_val_data
        )
        if data or self.global_rank != 0:
            return
        x, y, y_hat, logits = x.cpu(), y.cpu(), y_hat.cpu(), logits.cpu()
        for i in range(self.config.wandb_num_samples):
            index = (
                self.curr_val_epoch * self.config.wandb_num_samples + i
            ) % len(x)
            data.append(
                {
                    "x": self.wandb_media_x(x[index]),
                    "y": y[index],
                    "y_hat": y_hat[index],
                    "logits": logits[index].tolist(),
                },
            )
