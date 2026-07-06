# PM01 Humanoid Robot - Unified Integration Plan

**Date:** 2026-07-06  
**Repos:**
- `hcindus/AOS-Brain` (main stack)
- `hcindus/aocros` (simulation/testing)

---

## Current Status

### ✅ Complete (AOS-Brain)

| Component | Status | Location |
|-----------|--------|----------|
| Secure gRPC Bridge | ✅ | `pm01_aos_bridge/` |
| Agent Training Configs | ✅ | `pm01_sim_training/` |
| FSM Analysis | ✅ | `docs/PM01_Controller_Analysis.md` |
| Integration Assessment | ✅ | `docs/PM01_Integration_Assessment.md` |

**5 Agent Personalities Ready:**
- `miles_agent` - Sales Consultant (27.72 reward)
- `mylzeron_agent` - Executive/CEO (32.18 reward)
- `cylon_agent` - Security/Enforcer (34.91 reward)
- `cobra_agent` - Aggressive Sales (29.98 reward)
- `secretarial_pool` - Admin/Operations (24.94 reward)

### ✅ Complete (aocros)

| Component | Status | Location |
|-----------|--------|----------|
| PyBullet Simulation | ✅ | `robotics/engineai/test_engineai.py` |
| FSM Analysis | ✅ | `robotics/engineai/2026-07-06_engineai_fsm_analysis.md` |

---

## Architecture

### Simulation Path (Current)

```
┌─────────────────────────────────────────────────────────────┐
│  AOS Brain (Unix Socket)                                    │
│  └─ Agent Personality (Miles, Cylon, etc.)                    │
└──────────────────┬──────────────────────────────────────────┘
                   │ gRPC (mTLS)
┌──────────────────▼──────────────────────────────────────────┐
│  PM01 Bridge Server (Python)                                │
│  └─ Action Validator + Safety Limits                        │
└──────────────────┬──────────────────────────────────────────┘
                   │ RL Actions
┌──────────────────▼──────────────────────────────────────────┐
│  PyBullet Simulation (aocros)                               │
│  └─ test_engineai.py                                        │
│     └─ Joint control + Physics                              │
└─────────────────────────────────────────────────────────────┘
```

### Hardware Path (Target)

```
┌─────────────────────────────────────────────────────────────┐
│  AOS Brain (Agent Runtime)                                  │
└──────────────────┬──────────────────────────────────────────┘
                   │ gRPC
┌──────────────────▼──────────────────────────────────────────┐
│  PM01 Bridge Server                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │ ONNX Policy
┌──────────────────▼──────────────────────────────────────────┐
│  EngineAI Controller (NeZha)                                │
│  ├─ FSM: RL_Locomotion                                      │
│  ├─ LearningBasedController (C++)                           │
│  └─ LegController → Motors                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Critical Path

### Phase 1: Simulation Bridge ✅ DONE
- [x] gRPC bridge with mTLS
- [x] Agent training configs
- [x] PyBullet simulation

### Phase 2: Agent Training ⏳ BLOCKED
**Requires:** NVIDIA GPU + Isaac Gym Preview 4

```bash
# When GPU available:
cd pm01_sim_training/legged_gym
python scripts/train.py --task=miles_agent
python sim2real_deploy/export_onnx_policy.py
```

**Workaround:** Use mock training for development
```bash
cd pm01_sim_training
python mock_training.py --agent=all
```

### Phase 3: Hardware Deployment ⏳ PENDING
**Requires:** PM01 hardware + NeZha mainboard

1. Export ONNX from training
2. Copy to NeZha: `/home/unitree/EngineAI_Controller/`
3. Restart controller service
4. Connect AOS Bridge

---

## Integration Points

### 1. Bridge → PyBullet (Ready)

Modify `test_engineai.py`:

```python
# Add gRPC client
from pm01_aos_bridge.src.bridge.aos_client import AOSBrainClient

# Connect to bridge
client = AOSBrainClient()

# In simulation loop:
while True:
    # Get action from bridge
    action = client.get_action()
    
    # Apply to PyBullet
    p.setJointMotorControl2(robot, joint, p.POSITION_CONTROL, 
                           targetPosition=action)
```

### 2. Bridge → EngineAI (Ready)

Modify `LearningBasedController`:

```cpp
// Add socket listener to C++ controller
// Bridge sends actions via LCM/socket
// Controller applies to FSM_RL_Locomotion
```

---

## File Locations

### AOS-Brain Repository
```
pm01_aos_bridge/
├── src/bridge/secure_bridge.py      # gRPC server
├── src/bridge/aos_client.py         # AOS socket client
├── proto/aos_pm01.proto             # Protocol definitions
└── README.md

pm01_sim_training/
├── legged_gym/envs/                 # Agent configs
│   ├── miles_agent/
│   ├── cylon_agent/
│   ├── cobra_agent/
│   ├── mylzeron_agent/
│   └── secretarial_pool/
├── train_all_agents.sh              # Launcher
├── mock_training.py                 # Simulator
└── logs/training/                   # Results

docs/
├── PM01_Controller_Analysis.md
└── PM01_Integration_Assessment.md
```

### aocros Repository
```
robotics/engineai/
├── test_engineai.py                 # PyBullet sim
└── 2026-07-06_engineai_fsm_analysis.md
```

---

## Next Actions

### Immediate (Today)
1. **Connect Bridge to PyBullet**
   - Import bridge client in `test_engineai.py`
   - Test end-to-end AOS → Sim

2. **Verify gRPC Communication**
   - Start bridge server
   - Send test intents from AOS Brain
   - Verify actions received in sim

### Short Term (This Week)
3. **GPU Access**
   - Option A: Local NVIDIA GPU
   - Option B: Cloud instance (Lambda Labs, Vast.ai)
   - Option C: Colab Pro for initial training

4. **Train First Agent**
   - Start with `cylon_agent` (highest simulated reward)
   - Export ONNX policy
   - Test in PyBullet

### Medium Term (Next 2 Weeks)
5. **Hardware Procurement**
   - Contact Latin Satelital for PM01 pricing
   - Order 1x unit for testing
   - Secure 2-3 units if unit economics work

6. **Sim2Real Validation**
   - Transfer ONNX to NeZha
   - Test on real hardware
   - Fine-tune policy

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| No GPU | Use mock training + cloud GPU rental |
| Hardware delay | Continue PyBullet development |
| Sim2Real gap | Domain randomization + conservative gains |
| Safety concerns | Jordan's mTLS + EngineAI safety checks |

---

## Resources Needed

| Resource | Purpose | Cost |
|----------|---------|------|
| NVIDIA GPU (RTX 4090/A100) | RL Training | $1,600-10,000 |
| Cloud GPU (1 week) | Initial training | ~$200-500 |
| PM01 Unit (1x) | Hardware testing | ~$47,000 |
| Development time | Integration | N/A |

---

## Success Criteria

- [ ] AOS Brain can command PyBullet simulation
- [ ] At least 1 agent trained in Isaac Gym
- [ ] ONNX policy exports successfully
- [ ] Hardware procurement decision made

---

**Owner:** Miles / Performance Supply Depot LLC  
**Status:** Phase 1 Complete, Phase 2 Blocked (GPU)  
**Next Review:** Upon GPU availability
