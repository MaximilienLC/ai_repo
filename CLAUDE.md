See @README.md for project overview.

Never generate more than 200 characters at a time.
Always start the writing of new code by writing high-level design comments/docstrings.

You can run a task with the following command:

```
docker run -it \
--cap-add=SYS_PTRACE  \
--security-opt seccomp=unconfined \
--ipc=host \
--shm-size 8G \
--device=/dev/dxg -v /usr/lib/wsl/lib/libdxcore.so:/usr/lib/libdxcore.so -v /opt/rocm/lib/libhsa-runtime64.so.1:/opt/rocm/lib/libhsa-runtime64.so.1  \
mleclei/ai_repo:rocm python -m projects.PROJECT_NAME task=TASK_NAME
```
