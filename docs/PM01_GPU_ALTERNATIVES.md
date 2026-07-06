# PM01 Training - GPU Alternatives Analysis

**Date:** 2026-07-06  
**Constraint:** No local GPU available  
**Goal:** Deploy embodied agents on PM01 hardware

---

## Option 1: Cloud GPU Rental (RECOMMENDED) ⭐

### Services

| Provider | GPU | Cost/Hour | Setup Time |
|----------|-----|-----------|------------|
| **Lambda Labs** | A100 40GB | $1.10 | 5 min |
| **Vast.ai** | RTX 3090 | $0.40-0.80 | 10 min |
| **RunPod** | RTX A6000 | $0.74 | 5 min |
| **Google Colab Pro** | V100/T4 | $10/month | Immediate |

### Lambda Labs Quick Start

```bash
# Rent instance
ssh ubuntu@<lambda-ip>

# Setup (one-time)
git clone https://github.com/engineai-robotics/engineai_legged_gym
cd engineai_legged_gym
pip install -e .

# Train
python legged_gym/scripts/train.py --task=cylon_agent --headless
```

**Cost Estimate:**
- 1 agent × 3000 iterations ≈ 4-6 hours
- Cost: $2-7 per agent
- 5 agents: ~$15-35 total

**Pros:**
- Fast (A100 trains 10x faster than RTX 4090)
- No hardware purchase
- Easy scaling

**Cons:**
- Requires internet
- Data transfer (download ONNX after)
- No persistent storage (save checkpoints!)

---

## Option 2: Google Colab Pro (BUDGET) 💰

### Setup

```python
# In Colab notebook
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
!git clone https://github.com/engineai-robotics/engineai_legged_gym
%cd engineai_legged_gym
!pip install -e .

# Mount Google Drive for persistence
from google.colab import drive
drive.mount('/content/drive')

# Train
!python legged_gym/scripts/train.py --task=miles_agent --headless
```

**Limitations:**
- 12-hour session limit (free), 24-hour (Pro)
- T4 GPU (slower than A100)
- Need to reconnect periodically

**Cost:** $10/month (Pro) or free with limitations

**Best for:** Testing configs, single agent training

---

## Option 3: CPU-Only Training (SLOW) 🐌

### Feasibility

```bash
# Reduce complexity for CPU
--num_envs=32      # Down from 4096
--max_iterations=1000  # Down from 3000
--mini_batches=2   # Smaller batches
```

**Time Estimate:**
- CPU training: ~100-200 hours per agent
- 5 agents: ~500-1000 hours (20-40 days continuous)

**Verdict:** Not practical. Skip this.

---

## Option 4: Skip Training, Use Default Policy (FASTEST) ⚡

### EngineAI Default Controller

The PM01 ships with a **pre-trained locomotion policy** for basic walking.

**Path:**
1. Buy PM01 hardware first
2. Use EngineAI's default `zqsa01_policy.onnx`
3. Add our **high-level behavior layer** on top

### Architecture

```
Default Policy (EngineAI)
    ↓ Joint commands
Our Behavior Layer (Python)
    ↓ Intent → Velocity commands
AOS Brain Agent
    ↓ Social/Navigation logic
```

**Implementation:**

```python
# On NeZha mainboard
class BehaviorController:
    """Wraps default policy with agent personality."""
    
    def __init__(self):
        # Load EngineAI default
        self.default_policy = OnnxPolicy("zqsa01_policy.onnx")
        
    def step(self, agent_intent):
        """Convert intent to velocity commands."""
        
        # Miles: approach target smoothly
        if agent_intent == "approach_customer":
            cmd = self.calculate_approach_trajectory()
            
        # Cylon: rapid threat response
        elif agent_intent == "investigate_noise":
            cmd = self.calculate_tactical_path()
            
        # Default policy handles low-level walking
        joint_targets = self.default_policy.get_actions(cmd)
        return joint_targets
```

**Pros:**
- Immediate hardware testing
- No GPU needed
- Proven locomotion (won't fall)

**Cons:**
- Limited personality expression
- Can't customize gait
- Behavior layer only (not true RL)

**Best for:** MVP demo, first customer pilots

---

## Option 5: Transfer Learning from Existing Policies (SMART) 🧠

### Concept

Use **EngineAI's pretrained weights** as initialization, fine-tune for agents.

```python
# Load default policy
policy = ActorCritic()
policy.load("zqsa01_policy.onnx")

# Freeze locomotion layers
for param in policy.locomotion_layers:
    param.requires_grad = False

# Train only behavior head
for param in policy.behavior_head:
    param.requires_grad = True

# Fine-tune with small learning rate
trainer = PPO(policy, lr=1e-5)  # 10x smaller
```

**Training Time:**
- Fine-tuning: 1-2 hours (vs 4-6 hours from scratch)
- Requires GPU, but much less time

**Pros:**
- Faster training
- Better stability
- Leverages EngineAI's work

**Cons:**
- Still needs GPU
- Policy must be compatible

---

## Recommendation: Hybrid Approach

### Phase 1 (Now - No GPU)

**Buy PM01 hardware first.** Use Option 4 (default policy + behavior layer).

```
Week 1: Order PM01 from Latin Satelital
Week 2: Receive, setup default controller
Week 3: Implement behavior layer for Miles
Week 4: Demo to first customer
```

**Deliverable:** Working robot with personality (not RL-optimized)

### Phase 2 (Later - Cloud GPU)

**Rent GPU for 1 week.** Train custom policies.

```
Rent Lambda Labs A100 for 7 days ($185)
Train all 5 agents (4 hours each = 20 hours)
Export ONNX policies
Deploy to PM01
```

**Deliverable:** RL-optimized agents with unique gaits

### Phase 3 (Scale - Buy GPU)

**Buy local GPU** once unit economics proven.

```
Unit economics require: 20+ PM01 units
At 20 units: Revenue $59.4K/unit × 20 = $1.18M
Cost: $940K
Margin: $240K
GPU cost: $2K (RTX 4090)
ROI: Justified
```

---

## Cost Comparison

| Option | Upfront Cost | Training Time | Hardware Needed | Risk |
|--------|--------------|---------------|-----------------|------|
| Cloud GPU | $15-35 | 1 day | None | Low |
| Colab Pro | $10/month | 1-2 weeks | None | Medium |
| CPU | $0 | 40 days | None | High (time) |
| Default + Behavior | $47K (PM01) | 1 week | PM01 | Low |
| Transfer Learning | $15 + $47K | 3 days | PM01 + Cloud | Low |

---

## My Recommendation

**Do Option 4 + Option 1 in parallel:**

1. **Today:** Contact Latin Satelital, quote 1x PM01
2. **This week:** While waiting for hardware, rent Lambda Labs GPU for 1 day, train `cylon_agent` as proof-of-concept
3. **Next week:** PM01 arrives, test default controller + behavior layer
4. **Following week:** Deploy trained policy if sim2real transfer works

**Fallback:** If sim2real fails, default policy + behavior layer still delivers value.

---

## Immediate Action Items

- [ ] Contact Latin Satelital for PM01 quote
- [ ] Create Lambda Labs account (backup: Vast.ai)
- [ ] Prepare training configs for cloud deployment
- [ ] Document behavior layer architecture

**Decision needed:** Proceed with hardware-first approach?
