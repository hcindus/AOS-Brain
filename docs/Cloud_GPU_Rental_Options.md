# Cloud GPU Rental Options - RL Training

**Date:** 2026-07-06  
**Purpose:** Train PM01 agent policies in Isaac Gym  
**Requirements:** CUDA-capable GPU, PyTorch, Isaac Gym compatible

---

## Option 1: Lambda Labs (RECOMMENDED) ⭐

**URL:** https://lambdalabs.com/service/gpu-cloud  
**Best for:** Reliable, fast, straightforward

### Available GPUs

| GPU | VRAM | Cost/Hour | Speed (vs RTX 4090) |
|-----|------|-----------|---------------------|
| **A100 40GB** | 40 GB | $1.10 | 10x faster |
| **A100 80GB** | 80 GB | $1.60 | 10x faster |
| **H100 80GB** | 80 GB | $2.50 | 15x faster |

### Quick Start

```bash
# Sign up at lambdalabs.com
# Add SSH key
# Launch instance

ssh ubuntu@<instance-ip>

# Setup
sudo apt update
git clone https://github.com/engineai-robotics/engineai_legged_gym
cd engineai_legged_gym

# Install Isaac Gym (manual download required)
# See: https://developer.nvidia.com/isaac-gym

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -e .

# Train
python legged_gym/scripts/train.py --task=cylon_agent --headless
```

### Cost Estimate

| Scenario | GPU | Time | Cost |
|----------|-----|------|------|
| Single agent (test) | A100 | 4 hrs | $4.40 |
| All 5 agents | A100 | 20 hrs | $22.00 |
| With debugging | A100 | 30 hrs | $33.00 |
| Full training + tuning | A100 | 50 hrs | $55.00 |

**Pros:**
- Fast provisioning (~2 min)
- Clean Ubuntu images
- No hidden costs
- Good documentation

**Cons:**
- A100s can be in high demand (waitlist)
- Isaac Gym requires manual install

---

## Option 2: Vast.ai (BUDGET) 💰

**URL:** https://vast.ai  
**Best for:** Cheapest prices, spot instances

### Pricing (as of 2026-07-06)

| GPU | VRAM | Cost/Hour | Reliability |
|-----|------|-----------|-------------|
| RTX 3090 | 24 GB | $0.40-0.60 | Good |
| RTX 4090 | 24 GB | $0.70-1.00 | Good |
| A100 40GB | 40 GB | $1.00-1.50 | Variable |
| A6000 | 48 GB | $0.80-1.20 | Good |

### Quick Start

```bash
# Search for instances
# Filter: CUDA version ≥ 11.3, PyTorch pre-installed
# Rent and SSH in

# Most instances have PyTorch ready
pip install isaacgym  # Or manual install
pip install -e .
python legged_gym/scripts/train.py --task=miles_agent
```

### Cost Estimate

| Scenario | GPU | Time | Cost |
|----------|-----|------|------|
| Single agent | RTX 3090 | 6 hrs | $2.40-3.60 |
| All 5 agents | RTX 3090 | 30 hrs | $12-18 |
| Full project | RTX 4090 | 40 hrs | $28-40 |

**Pros:**
- Cheapest option
- Spot instances for lower cost
- Variety of GPU choices

**Cons:**
- Quality varies by host
- Some hosts unreliable
- Must check CUDA/PyTorch versions

---

## Option 3: RunPod

**URL:** https://www.runpod.io  
**Best for:** Serverless inference (future), persistent storage

### Pricing

| GPU | Cost/Hour | Persistent Storage |
|-----|-----------|-------------------|
| RTX A5000 | $0.44 | $0.10/GB/month |
| RTX A6000 | $0.74 | $0.10/GB/month |
| A100 40GB | $1.99 | $0.10/GB/month |

### Features
- Template-based (pre-configured environments)
- Persistent network volumes
- Can save checkpoint to cloud

---

## Option 4: Google Colab Pro/Pro+

**URL:** https://colab.research.google.com  
**Best for:** Quick tests, single experiments

### Plans

| Plan | Cost | GPU | Session Time |
|------|------|-----|--------------|
| Free | $0 | T4 | 12 hrs |
| Pro | $10/mo | V100/T4 | 24 hrs |
| Pro+ | $50/mo | V100/P100 | 24 hrs |

### Limitations
- T4 is slow (2x slower than A100)
- Session disconnects after timeout
- Must reconnect, lose state
- Notebook format (not ideal for long training)

**Verdict:** Good for testing configs, not for full training.

---

## Option 5: Paperspace Core

**URL:** https://www.paperspace.com/core  
**Best for:** Persistent notebooks, simple UI

### Pricing

| GPU | Cost/Hour |
|-----|-----------|
| RTX A4000 | $0.51 |
| RTX A5000 | $0.78 |
| RTX A6000 | $1.10 |
| A100 80GB | $3.09 |

---

## Recommendation

**Primary:** Lambda Labs A100 ($1.10/hr)
- Reliable
- Fast (10x speedup)
- Good for focused training runs

**Budget:** Vast.ai RTX 3090 ($0.50/hr avg)
- If A100 unavailable
- Longer training but cheaper

**Order:**
1. Try Lambda Labs A100 first
2. Fallback to Vast.ai RTX 3090 if waitlisted
3. Start with 1 agent (4-6 hrs) to validate
4. Scale to all 5 agents if successful

---

## Training Checklist (Pre-Rental)

- [ ] Isaac Gym Preview 4 downloaded (requires NVIDIA developer account)
- [ ] `engineai_legged_gym` forked/cloned
- [ ] Agent configs validated (`python -m py_compile`)
- [ ] Cloud credits/account ready
- [ ] Checkpoint save strategy (Google Drive/S3)
- [ ] Local backup of training data

---

## Cost Summary

| Provider | Best For | Est. Cost (5 agents) | Setup Time |
|----------|----------|---------------------|------------|
| Lambda Labs | Reliability | $22 | 5 min |
| Vast.ai | Budget | $15 | 10 min |
| Colab Pro | Testing | $10/mo | Immediate |

---

**Next Step:** Create Lambda Labs account, add payment method, test 1-hour instance
