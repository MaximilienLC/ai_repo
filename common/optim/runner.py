from abc import ABC

from hydra_zen import ZenStore

from common.runner import BaseTaskRunner

from .store import store_launcher_configs


class OptimTaskRunner(BaseTaskRunner, ABC):

    @classmethod
    def store_configs(cls: type["OptimTaskRunner"], store: ZenStore) -> None:
        """.

        .. warning::

            Make sure to call this method if you are overriding it.
        """
        super().store_configs(store)
        store_launcher_configs(store)
