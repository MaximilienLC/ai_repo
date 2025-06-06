""":class:`.BaseSpace` and its config."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Annotated as An
from typing import Any

import numpy as np

from common.optim.ne.agent import BaseAgent
from common.utils.beartype import ge


@dataclass
class BaseSpaceConfig:
    """Holds :class:`BaseSpace` config values.

    Args:
        eval_num_steps: See
            :paramref:`~.NeuroevolutionSubtaskConfig.eval_num_steps`.
        logging: See :paramref:`~.NeuroevolutionSubtaskConfig.logging`.
    """

    eval_num_steps: An[int, ge(0)] = "${config.eval_num_steps}"  # type: ignore[assignment]
    logging: bool = "${config.logging}"  # type: ignore[assignment]


class BaseSpace(ABC):
    """Space Base class.

    A ``Space`` is a `torchrl <https://pytorch.org/rl/>`_ environment
    wrapper with which agents produce behaviour and receive fitness
    scores.

    Args:
        config
        num_pops: Number of agents interacting with each other in a
            given space.
        evaluates_on_gpu: Whether GPU devices are used to evaluate
            agents.
    """

    def __init__(
        self: "BaseSpace",
        config: BaseSpaceConfig,
        num_pops: int,
        *,
        evaluates_on_gpu: bool,
    ) -> None:
        self.config = config
        self.num_pops = num_pops
        self.evaluates_on_gpu = evaluates_on_gpu

    @abstractmethod
    def evaluate(
        self: "BaseSpace",
        agents: list[list[BaseAgent]],
        curr_gen: An[int, ge(1)],
    ) -> np.ndarray[np.float32, Any]:
        """.

        Method called once per iteration (every generation) in order to
        evaluate and attribute fitnesses to agents.

        Args:
            agents: Agent(s) to evaluate.
            curr_gen: The current generation number/index.

        Returns:
            The fitnesses and number of steps ran.
        """
