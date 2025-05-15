from hydra_zen import ZenStore

from common.optim.ne.runner import NeuroevolutionTaskRunner
from common.utils.hydra_zen import generate_config

from .agent import GymAgent, GymAgentConfig
from .space import GymReinforcementSpace, GymReinforcementSpaceConfig


class TaskRunner(NeuroevolutionTaskRunner):

    @classmethod
    def store_configs(cls: type["TaskRunner"], store: ZenStore) -> None:
        super().store_configs(store)
        store(
            generate_config(
                GymReinforcementSpace,
                config=generate_config(GymReinforcementSpaceConfig),
            ),
            name="ne_control_score",
            group="space",
        )
        store(
            generate_config(
                GymAgent,
                config=generate_config(GymAgentConfig),
            ),
            name="ne_control_score",
            group="agent",
        )


TaskRunner.run_task()
