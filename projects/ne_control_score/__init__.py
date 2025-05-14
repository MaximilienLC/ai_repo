"""Score Optimization w/ Neuroevolution on Gym control environments."""

from beartype import BeartypeConf
from beartype.claw import beartype_this_package

from .agent import GymAgent, GymAgentConfig
from .space import GymReinforcementSpace, GymReinforcementSpaceConfig

beartype_this_package(conf=BeartypeConf(is_pep484_tower=True))

__all__ = [
    "GymAgent",
    "GymAgentConfig",
    "GymReinforcementSpace",
    "GymReinforcementSpaceConfig",
]
