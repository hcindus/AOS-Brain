#!/bin/bash
# Lambda Labs A100 Setup Script for PM01 Agent Training
# Run this after SSHing into Lambda instance

set -e

echo "=============================================="
echo "PM01 Agent Training Setup - Lambda Labs A100"
echo "=============================================="
echo ""

# Configuration
REPO_URL="https://github.com/hcindus/AOS-Brain"
AGENT="cylon_agent"  # Start with highest reward agent
MAX_ITERATIONS=3000
SAVE_INTERVAL=100

echo "Step 1: System Updates"
echo "----------------------------------------------"
sudo apt update && sudo apt install -y git wget curl python3-pip python3-venv htop nvtop

echo ""
echo "Step 2: Install PyTorch with CUDA 11.8"
echo "----------------------------------------------"
pip3 install torch==2.0.1+cu118 torchvision==0.15.2+cu118 --index-url https://download.pytorch.org/whl/cu118

echo ""
echo "Step 3: Setup Training Directory"
echo "----------------------------------------------"
cd ~
mkdir -p pm01_training && cd pm01_training

echo ""
echo "Step 4: Clone Training Repository"
echo "----------------------------------------------"
git clone --recursive $REPO_URL

echo ""
echo "Step 5: Install Isaac Gym Preview 4"
echo "----------------------------------------------"
echo "NOTE: Isaac Gym requires manual download from NVIDIA"
echo "Downloading from official source..."

# Isaac Gym must be downloaded manually from NVIDIA Developer
# For now, we'll use the engineai_legged_gym repo which has compatibility layers
cd AOS-Brain/pm01_sim_training

pip3 install -e .

echo ""
echo "Step 6: Install rsl_rl (RL library)"
echo "----------------------------------------------"
cd rsl_rl
pip3 install -e .
cd ..

echo ""
echo "Step 7: Verify GPU"
echo "----------------------------------------------"
nvidia-smi
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0)}')"

echo ""
echo "Step 8: Start Training"
echo "----------------------------------------------"
echo "Training agent: $AGENT"
echo "Max iterations: $MAX_ITERATIONS"
echo "Save interval: $SAVE_INTERVAL"
echo ""

# Create training script
cat > train_and_monitor.sh << 'EOF'
#!/bin/bash
AGENT=$1
MAX_ITER=$2
SAVE_INT=$3

echo "Starting training for $AGENT"
echo "Logging to: logs/${AGENT}_training.log"

python3 legged_gym/scripts/train.py \
    --task=$AGENT \
    --headless \
    --max_iterations=$MAX_ITER \
    --save_interval=$SAVE_INT \
    2&1 | tee logs/${AGENT}_training.log

echo "Training complete!"
echo "Exporting ONNX policy..."

python3 sim2real_deploy/export_onnx_policy.py \
    --load_model logs/${AGENT}_ppo/*/model_${MAX_ITER}.pt \
    --output ${AGENT}_policy.onnx

echo "ONNX exported: ${AGENT}_policy.onnx"
EOF

chmod +x train_and_monitor.sh

mkdir -p logs

# Start training in background
nohup ./train_and_monitor.sh $AGENT $MAX_ITERATIONS $SAVE_INTERVAL > logs/setup.log 2>&1 &

echo ""
echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo "Training started in background."
echo ""
echo "Monitor progress:"
echo "  tail -f ~/pm01_training/AOS-Brain/pm01_sim_training/logs/${AGENT}_training.log"
echo ""
echo "Check GPU usage:"
echo "  watch -n 1 nvidia-smi"
echo ""
echo "When training completes:"
echo "  ONNX policy: ~/pm01_training/AOS-Brain/pm01_sim_training/${AGENT}_policy.onnx"
echo ""
echo "=============================================="
