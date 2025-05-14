On an Linux machine
===================

1. Move to the desired containing folder
----------------------------------------

.. note::

    We recommend, in the ``Contribution`` section, to make use of Dropbox or
    its headless Python package Maestral if you plan to alter the code on
    different machines.

.. code-block:: bash

    # Example
    cd ${HOME}/Dropbox/

2. Clone the repository
-----------------------

.. code-block:: bash

    git clone git@github.com:MaximilienLC/ai_repo.git

3. Define the ``AI_REPO_PATH`` variable
-----------------------------------------

.. code-block:: bash

    echo -e "\nexport AI_REPO_PATH=${PWD}/ai_repo" >> ~/.bashrc \
        && source ~/.bashrc

4. Install Docker or Podman
---------------------------

.. note::

    Skip to Step 7 if you do not have administrator privileges.

.. note::

    We suggest installing Docker if you meet any of the following conditions:

    - This is your own machine and plan to contribute to the library
      (Development Containers are smoother with Docker than Podman).
    - You are an administrator of this machine, do not want to install Podman
      and are fine with adding users to the ``docker`` group. See this `link
      on security implications
      <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`_.

    Otherwise, install Podman.

**Option A) Install Docker**

Follow the `Docker installation guide
<https://docs.docker.com/desktop/install/ubuntu/>`_.
Do not forget the `Docker post-installation steps
<https://docs.docker.com/engine/install/linux-postinstall/>`_.

.. note::

    You could be interested in setting up Rootless mode if you plan
    to make use of the library's Development Container (so that files created
    by the container are owned by your user and not by root). See this `link
    <https://docs.docker.com/engine/security/rootless/>`_ for more information.

**Option B) Install Podman**

Follow the `Podman installation guide
<https://podman.io/getting-started/installation>`_.

5. Install the NVIDIA driver
----------------------------

.. note::

    Skip this step if your machine does not have an NVIDIA GPU.
    If you have an AMD GPU, check-out ROCm. Note that you will
    need to replace the CUDA base image with ROCm in the Dockerfile.

.. note::

    In addition to the method described below, Ubuntu users can also install
    the driver by opening the "Software & Updates" application, going to the
    "Additional Drivers" tab and selecting the "Using NVIDIA driver
    metapackage from nvidia-driver-XXX (proprietary, tested)" option.

Follow the `NVIDIA driver installation guide
<https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html>`_.

6. Install the NVIDIA Container Toolkit
---------------------------------------

.. note::

    Skip this step if your machine does not have an NVIDIA GPU.
    If you have an AMD GPU, check-out ROCm. Note that you will
    need to replace the CUDA base image with ROCm in the Dockerfile.

Follow the `NVIDIA Container Toolkit installation guide
<https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`_.

If you are using a Rootless Docker or Podman, make sure to follow the
`Rootless setup
<https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/1.13.5/install-guide.html#step-3-rootless-containers-setup>`_.

7. Pull the image
-----------------

.. code-block:: bash

    # Substitute `docker` with `podman` if you installed Podman.
    docker pull docker.io/mleclei/ai_repo:latest

    # On a Slurm cluster
    apptainer build -F ai_repo.sif docker://mleclei/ai_repo:latest
