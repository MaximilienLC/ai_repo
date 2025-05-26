"""`Hydra <https://hydra.cc>`_ utilities."""

from hydra.core.hydra_config import HydraConfig
from hydra_plugins.hydra_submitit_launcher.config import (
    LocalQueueConf,
    SlurmQueueConf,
)
from hydra_plugins.hydra_submitit_launcher.submitit_launcher import (
    LocalLauncher,
    SlurmLauncher,
)
from omegaconf import DictConfig, OmegaConf

from common.utils.misc import get_path


def get_launcher_config() -> LocalQueueConf | SlurmQueueConf:
    """Retrieves/validates this job's ``hydra`` launcher config.

    Ref: `Hydra <https://hydra.cc>`_.

    Returns:
        The `Hydra <https://hydra.cc>`_ launcher config.

    Raises:
        TypeError: If the launcher config is not a dict or if the
            launcher is not supported.
    """
    launcher_dict_config: DictConfig = HydraConfig.get().launcher
    launcher_container_config = OmegaConf.to_container(
        cfg=launcher_dict_config,
    )
    if not isinstance(launcher_container_config, dict):
        raise TypeError
    launcher_config_dict = dict(launcher_container_config)
    if launcher_dict_config._target_ == get_path(
        LocalLauncher,
    ):
        return LocalQueueConf(**launcher_config_dict)
    if launcher_dict_config._target_ == get_path(
        SlurmLauncher,
    ):
        return SlurmQueueConf(**launcher_config_dict)
    error_msg = f"Unsupported launcher: {launcher_dict_config._target_}"
    raise TypeError(error_msg)
