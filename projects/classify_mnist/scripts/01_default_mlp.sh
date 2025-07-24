#!/bin/bash
EXPERIMENT_NAME="$(basename "${0%.*}")"

docker run --rm --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --ipc=host \
    --device=/dev/dxg -v /usr/lib/wsl/lib/libdxcore.so:/usr/lib/libdxcore.so \
    -v /opt/rocm/lib/libhsa-runtime64.so.1:/opt/rocm/lib/libhsa-runtime64.so.1 \
    -e AI_REPO_PATH=${AI_REPO_PATH} -e PYTHONPATH=${PYTHONPATH}:${AI_REPO_PATH} \
    -v ${AI_REPO_PATH}:${AI_REPO_PATH} -v /dev/shm:/dev/shm -w ${AI_REPO_PATH} \
    mleclei/ai_repo:rocm python -m projects.classify_mnist.train task=mlp \
    logger.name=${EXPERIMENT_NAME}