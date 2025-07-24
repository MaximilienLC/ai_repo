See @README.md for project overview.

Never generate more than 200 characters at a time.
Always start the writing of new code by writing high-level design comments/docstrings.

Always use `docker run` when running code.
Make sure to include these flags:

```
--rm --cap-add=SYS_PTRACE --security-opt seccomp=unconfined --ipc=host
--device=/dev/dxg -v /usr/lib/wsl/lib/libdxcore.so:/usr/lib/libdxcore.so
-v /opt/rocm/lib/libhsa-runtime64.so.1:/opt/rocm/lib/libhsa-runtime64.so.1
-e AI_REPO_PATH=${AI_REPO_PATH} -e PYTHONPATH=${PYTHONPATH}:${AI_REPO_PATH}
-v ${AI_REPO_PATH}:${AI_REPO_PATH} -v /dev/shm:/dev/shm -w ${AI_REPO_PATH}
mleclei/ai_repo:rocm python -m projects.PATH_TO_PY_FILE task=TASK_NAME
```

The corresponding log file can be found in data/PROJECT_NAME/TASK_NAME/DATE_TIME/<...>.out.

When asked to run code, follow the convention in @projects/haptic_pred/scripts/,
meaning create a new .sh file with the docker command to run, and run that script instead.

When asked to look at runs, do that through your `wandb` MCP. Make sure to not only communicate
final results but also trends, ex: loss converging, accuracy diverging, train and val loss distancing
each other, etc.

## Getting W&B Historical Data
- Use `history(samples: xxxx)` field in GraphQL query, NOT `sampledHistory`
- Returns JSON strings with step-by-step metrics including train/val/... loss/acc/...
- Parse JSON strings to extract training trajectories and analyze patterns

