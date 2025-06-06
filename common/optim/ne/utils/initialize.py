"""Variable initialization for Neuroevolution fitting."""

from functools import partial
from typing import Annotated as An

import numpy as np
from mpi4py import MPI

from common.optim.ne.agent import BaseAgent
from common.optim.ne.utils.type import (
    Exchange_and_mutate_info_batch_type,
    Exchange_and_mutate_info_type,
    Generation_results_batch_type,
    Generation_results_type,
    Seeds_batch_type,
)
from common.optim.utils.hydra import get_launcher_config
from common.utils.beartype import ge, le
from common.utils.misc import seed_all
from common.utils.mpi4py import get_mpi_variables


def initialize_common_variables(
    agents_per_task: An[int, ge(1)],
    num_pops: An[int, ge(1), le(2)],
) -> tuple[
    An[int, ge(1)],  # pop_size
    An[int, ge(1)],  # len_agents_batch
    Exchange_and_mutate_info_type | None,  # exchange_and_mutate_info
    Exchange_and_mutate_info_batch_type,  # exchange_and_mutate_info_batch
    Seeds_batch_type,  # seeds_batch
    Generation_results_type | None,  # generation_results
    Generation_results_batch_type,  # generation_results_batch
    An[int, ge(0)] | None,  # total_num_env_steps
]:
    """Initializes variables common to all execution modes.

    Args:
        agents_per_task: See
            :paramref:`~.NeuroevolutionSubtaskConfig.agents_per_task`.
        num_pops: See :meth:`~.BaseSpace.num_pops`.

    Returns:
        :paramref:`~.compute_start_time_and_seeds.pop_size`,
            :paramref:`~initialize_agents.len_agents_batch`,
            :paramref:`~.update_exchange_and_mutate_info.exchange_and_mutate_info`,
            :paramref:`~.mutate.exchange_and_mutate_info_batch`,
            An array used as a buffer by all processes to receive the
            seeds from the primary process during the first generation
            only.
            :paramref:`~.compute_generation_results.generation_results`,
            :paramref:`~.compute_generation_results.generation_results_batch`,
            :paramref:`~.compute_total_num_env_steps_and_process_fitnesses.total_num_env_steps`.
    """
    comm, rank, size = get_mpi_variables()
    launcher_config = get_launcher_config()
    pop_size = (
        launcher_config.nodes
        * launcher_config.tasks_per_node
        * agents_per_task
    )
    len_agents_batch = pop_size // size
    exchange_and_mutate_info = (
        None
        if rank != 0
        else np.empty(
            shape=(pop_size, num_pops, 4),
            dtype=np.uint32,
        )
    )
    exchange_and_mutate_info_batch = np.empty(
        shape=(len_agents_batch, num_pops, 4),
        dtype=np.uint32,
    )
    seeds_batch = np.empty(
        shape=(len_agents_batch, num_pops),
        dtype=np.uint32,
    )
    generation_results_batch = np.empty(
        shape=(len_agents_batch, num_pops, 3),
        dtype=np.float32,
    )
    generation_results = (
        None
        if rank != 0
        else np.empty(
            shape=(pop_size, num_pops, 3),
            dtype=np.float32,
        )
    )
    total_num_env_steps = None if rank != 0 else 0
    return (
        pop_size,
        len_agents_batch,
        exchange_and_mutate_info,
        exchange_and_mutate_info_batch,
        seeds_batch,
        generation_results,
        generation_results_batch,
        total_num_env_steps,
    )


def initialize_gpu_comm() -> MPI.Comm:
    """Initializes a communicator for GPU work queueing.

    Assuming the experiment is ran with ``N`` MPI processes &
    ``M`` GPUs, this function will create ``M`` communicators, each
    containing ``N/M`` processes. Each communicator will be used to
    gather mutated agents onto one process, which will then
    evaluate them on the GPU.

    Returns:
        See :paramref:`~.evaluate_on_gpu.ith_gpu_comm`.
    """
    comm, rank, size = get_mpi_variables()
    launcher_config = get_launcher_config()
    if not launcher_config.gpus_per_node:
        error_msg = (
            "The number of GPUs per node must be a positive integer "
            "in order to setup GPU work queueing."
        )
        raise ValueError(error_msg)
    tasks_per_gpu = size // launcher_config.gpus_per_node
    gpu_idx = rank // tasks_per_gpu
    ith_gpu_comm_task_list = np.arange(
        start=gpu_idx * tasks_per_gpu,
        stop=(gpu_idx + 1) * tasks_per_gpu,
    ).tolist()
    return comm.Create(comm.group.Incl(ith_gpu_comm_task_list))


def initialize_agents(
    agent: partial[BaseAgent],
    len_agents_batch: An[int, ge(1)],
    num_pops: An[int, ge(1), le(2)],
    *,
    pop_merge: bool,
) -> list[list[BaseAgent]]:  # agents_batch
    """Initializes a batch of agents.

    Args:
        agent
        len_agents_batch: The number of agents per population
            maintained in
            :paramref:`~.compute_generation_results.agents_batch`
            by the process calling this function during a
            given generation.
        num_pops: See :meth:`~.BaseSpace.num_pops`.
        pop_merge: See
            :paramref:`~.NeuroevolutionSubtaskConfig.pop_merge`.

    Returns:
        A 2D list of agents maintained by this process.
    """
    agents_batch: list[list[BaseAgent]] = []
    for _ in range(len_agents_batch):
        agents_batch.append([])
        for j in range(num_pops):
            seed_all(0)
            agents_batch[-1].append(
                agent(pop_idx=j, pops_are_merged=pop_merge),
            )

    return agents_batch
