*********
Execution
*********

Through Docker
--------------

.. code-block:: bash

    # Example: Train MNIST on NVIDIA GPUs
    docker run --privileged --gpus all --rm -e AI_REPO_PATH=${AI_REPO_PATH} \
               -e PYTHONPATH=${PYTHONPATH}:${AI_REPO_PATH} \
               -v ${AI_REPO_PATH}:${AI_REPO_PATH} -v /dev/shm:/dev/shm \
               -w ${AI_REPO_PATH} mleclei/ai_repo:latest \
               python -m project.classify_mnist task=mlp

Through Apptainer
-----------------

.. code-block:: bash

    # Example: Train MNIST on the Béluga cluster
    module load apptainer && cd ${AI_REPO_PATH} && export PYTHONPATH=${PYTHONPATH}:${AI_REPO_PATH} && \
        export APPTAINERENV_APPEND_PATH=/opt/software/slurm/bin:/cvmfs/soft.computecanada.ca/easybuild/software/2020/Core/apptainer/1.1.8/bin && \
        apptainer exec --no-home -B /etc/passwd -B /etc/slurm/ -B /opt/software/slurm -B /usr/lib64/libmunge.so.2 \
                       -B /cvmfs/soft.computecanada.ca/easybuild/software/2020/Core/apptainer/1.1.8/bin/apptainer \
                       -B /var/run/munge/ --env LD_LIBRARY_PATH=/opt/software/slurm/lib64/slurm  -B $AI_REPO_PATH $SCRATCH/ai_repo.sif \
                       python -m project.classify_mnist task=mlp_beluga
