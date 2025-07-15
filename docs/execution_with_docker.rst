With Docker
===========

Run a python script
-------------------

.. note::

    Replace ``task=mlp`` with ``task=mlp_cpu`` if you don't have a GPU. You
    might also need to remove the ``--gpus all`` flag.

.. code-block:: bash

    # Example of a simple MNIST training run
    docker run --privileged --gpus all --rm -e AI_REPO_PATH=${AI_REPO_PATH} \
               -e PYTHONPATH=${PYTHONPATH}:${AI_REPO_PATH} \
               -v ${AI_REPO_PATH}:${AI_REPO_PATH} -v /dev/shm:/dev/shm \
               -w ${AI_REPO_PATH} mleclei/ai_repo:cpu \
               python -m projects.classify_mnist task=mlp


Run a notebook
--------------

From your own machine create a SSH tunnel to the running machine.

.. code-block:: bash

   # Example
   ssh MY_USER@123.456.7.8 -NL 8888:localhost:8888

Run the lab.

.. code-block:: bash

    docker run --rm -e AI_REPO_PATH=${AI_REPO_PATH} \
               -e PYTHONPATH=${PYTHONPATH}:${AI_REPO_PATH} \
               -v ${AI_REPO_PATH}:${AI_REPO_PATH} \
               -w ${AI_REPO_PATH} mleclei/ai_repo:latest \
               jupyter-lab --allow-root --ip 0.0.0.0 --port 8888
