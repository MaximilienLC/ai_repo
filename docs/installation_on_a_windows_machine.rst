On a Windows machine
====================

Documentation beautification in progress...

Step 1. Install GitHub Desktop
Step 2. Clone the repository
Step 3. Win + R -> sysdm.cpl -> Advanced -> Environment Variables...
Step 4. System variables -> New...
Step 5. Variable name: AI_REPO_PATH
Step 6. Variable value: <PATH TO AI_REPO>
Step 7. Click OK

If:
- You have a Maxwell or newer NVIDIA GPU
- You have one of these AMD GPUs:
AMD Radeon™ RX 7900 XTX
AMD Radeon™ RX 7900 XT
AMD Radeon™ RX 7900 GRE
AMD Radeon™ PRO W7900
AMD Radeon™ PRO W7800
AMD Radeon™ PRO W7900 Dual Slot

Then you can run GPU workloads in WSL2, which is the easiest way.

Otherwise, you will need to install the dependencies on your Windows machine.

If you have a different AMD GPU, you can follow `this tutorial
<https://github.com/Filip7700/unofficial-pytorch-rocm-hack-for-windows>`_.

In that case do not make use of a Docker image but instead install the
dependencies directly on your Windows machine. Make sure PyTorch is installed
with CUDA 11 and not CUDA 12+.
