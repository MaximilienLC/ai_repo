On a Slurm cluster
==================

.. note ::

    Suggestion: Open a tmux session to run the following commands.

Run a python script
-------------------

.. note::

    The following command was designed for the Béluga cluster. It will most
    likely need refining on other clusters.

.. code-block:: bash

    # Example of a simple MNIST training run
    module load apptainer && cd ${AI_REPO_PATH} && export PYTHONPATH=${PYTHONPATH}:${AI_REPO_PATH} && \
        export APPTAINERENV_APPEND_PATH=/opt/software/slurm/bin:/cvmfs/soft.computecanada.ca/easybuild/software/2020/Core/apptainer/1.1.8/bin && \
        apptainer exec --no-home -B /etc/passwd -B /etc/slurm/ -B /opt/software/slurm -B /usr/lib64/libmunge.so.2 \
                       -B /cvmfs/soft.computecanada.ca/easybuild/software/2020/Core/apptainer/1.1.8/bin/apptainer \
                       -B /var/run/munge/ --env LD_LIBRARY_PATH=/opt/software/slurm/lib64/slurm  -B $AI_REPO_PATH $SCRATCH/ai_repo.sif \
                       python -m project.classify_mnist task=mlp_beluga

Run Jupyter-lab
---------------

From your own machine create a SSH tunnel to the compute node.

.. code-block:: bash

    # Fill in the appropriate values
    sshuttle --dns -Nr USER@ADDRESS:8888

Run the lab.

.. code-block:: bash

    # Fill in the appropriate values
    salloc --account=ACCOUNT bash -c "module load apptainer && \
        cd ${AI_REPO_PATH} && \
        apptainer exec --nv -v ${AI_REPO_PATH}:${AI_REPO_PATH} \
        ${SCRATCH}/ai_repo.sif jupyter-lab --allow-root --ip $(hostname -f) --port 8888"
