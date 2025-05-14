from dataclasses import dataclass, field
from typing import Any

from hydra_zen import make_config

from common.infer.config import InferenceSubtaskConfig
from common.optim.dl.litmodule import BaseLitModule
from common.utils.hydra_zen import generate_config, generate_config_partial


@dataclass
class LightningInferenceSubtaskConfig(InferenceSubtaskConfig):
    """.

    Args:
        ckpt_path: The path to a Lightning checkpoint to load the model
            from.
    """

    ckpt_path: str | None = "last"


@dataclass
class LightningInferenceTaskConfig(
    make_config(  # type: ignore[misc]
        litmodule=generate_config_partial(BaseLitModule),
        config=generate_config(LightningInferenceSubtaskConfig),
    ),
):

    defaults: list[Any] = field(
        default_factory=lambda: [
            "_self_",
            "project",
            "task",
            {"task": None},
        ],
    )
