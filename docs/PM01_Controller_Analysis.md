# EngineAI PM01 Controller Analysis

**Source:** https://github.com/engineai-robotics/engineai_humanoid  
**Date:** 2026-07-06  
**Analyst:** Miles / Performance Supply Depot LLC

---

## FSM State Architecture

The PM01 controller uses a **Finite State Machine** with 6 operational states:

| State ID | Name | Description | Use Case |
|----------|------|-------------|----------|
| 0 | **ESTOP** | Emergency stop - cuts power | Safety critical |
| 1 | **PASSIVE** | Zero torque, gravity compensation | Startup, idle |
| 2 | **RL_LOCOMOTION** | Reinforcement learning walking | Normal operation |
| 3 | **BALANCE_STAND** | Static balancing | Standing still |
| 15 | **LOCK_JOINT** | Freeze joints in place | Transition, error |
| 51 | **JOINT_PD** | Joint-level PD control | Calibration, testing |

---

## State Transitions

```
┌─────────┐     ┌──────────┐     ┌──────────────┐
│ PASSIVE │────▶│ RL_LOCO  │────▶│ BALANCE_STAND│
└─────────┘     └──────────┘     └──────────────┘
      │               │                  │
      ▼               ▼                  ▼
┌─────────┐     ┌──────────┐     ┌──────────────┐
│ ESTOP   │◄────│ LOCK_JNT │◄────│  JOINT_PD    │
└─────────┘     └──────────┘     └──────────────┘
      ▲
      │
   Any state (emergency)
```

---

## RL Locomotion State (Key Integration Point)

**File:** `FSM_State_RL_Locomotion.cpp`

### Safety Checks (`locomotionSafe()`)

The RL controller has **hard-coded safety limits**:

| Parameter | SA01 | SA01P (PM01) |
|-----------|------|--------------|
| Max Roll | ±80° | ±50° |
| Max Pitch | ±80° | ±60° |
| Leg Y Offset | ±0.56m | ±0.30m |
| Max Leg Velocity | 19 m/s | 19 m/s |

**Automatic transition to LOCK_JOINT if any limit exceeded.**

### Integration Architecture

```
AOS Brain Intent
      ↓ (gRPC/mTLS)
Agent Personality Layer (Python)
      ↓ (Observation/Action)
LearningBasedController (C++)
      ↓ (Joint targets)
FSM_State_RL_Locomotion
      ↓ (Torque commands)
LegController → Motors
```

### LocomotionControlStep()

```cpp
void FSM_State_RL_Locomotion<T>::LocomotionControlStep() {
    rlActualController->update();  // Runs RL policy inference
}
```

**This is our injection point.** The `LearningBasedController` calls the ONNX policy.

---

## Control Data Flow

### High-Level (Our Code)
1. **IntentCommand** → "Navigate to reception desk"
2. **Agent Personality** → Miles: social navigation
3. **RL Observation** → Convert to policy input
4. **ONNX Inference** → Action output

### Low-Level (EngineAI Code)
1. **LearningBasedController** → Loads `.onnx` policy
2. **FSM_State_RL_Locomotion** → Safety checks
3. **LegController** → Joint PD control
4. **Motor Driver** → Hardware commands

---

## Key Files for Integration

| File | Purpose | Our Modification? |
|------|---------|-------------------|
| `FSM_State_RL_Locomotion.cpp` | RL state machine | NO (safety) |
| `LearningBasedController.cpp` | Policy inference | EXTEND |
| `ControlFSM.cpp` | State transitions | NO |
| `legged_robot.cpp` | Low-level control | NO |

---

## Integration Strategy

### Option 1: Sim2Sim First (Recommended)
1. Train in Isaac Gym (`engineai_legged_gym`)
2. Test in sim2sim environment
3. Export ONNX policy
4. Deploy to real PM01

### Option 2: Direct Sim2Real
1. Train policy with domain randomization
2. Export ONNX
3. Deploy to hardware
4. Tune on real robot

---

## AOS Bridge Integration Points

Our `pm01_aos_bridge` connects to the Controller via:

1. **Socket Interface** → Unix domain socket to control process
2. **LCM Messages** → State telemetry from robot
3. **Gamepad Input** → High-level velocity commands

### Command Path
```
AOS Client (Python) ──▶ gRPC (mTLS)
                              ↓
                      PM01 Bridge Server
                              ↓
                      LearningBasedController
                              ↓
                      FSM_State_RL_Locomotion
                              ↓
                      NeZha Mainboard → Motors
```

---

## Safety Architecture

### Software Limits (C++)
- Roll/Pitch limits → Auto-ESTOP
- Joint limits → Clip to range
- Velocity limits → Scale down

### Hardware Watchdog
- Communication timeout → ESTOP
- Motor fault → ESTOP
- Emergency button → ESTOP

---

## NeZha Mainboard

The PM01 uses a custom **NeZha** mainboard with:
- ARM Cortex-A72 (Raspberry Pi CM4 based)
- Real-time motor control
- CAN bus motor drivers
- Ubuntu 20.04

**Connection:** Ethernet from development PC to NeZha for deployment.

---

## Next Steps

1. ✅ **Complete:** Architecture analysis
2. 🔄 **In Progress:** Train agents in Isaac Gym
3. ⏳ **Pending:** Sim2Sim validation
4. ⏳ **Pending:** Hardware deployment test

---

## References

- EngineAI Humanoid: https://github.com/engineai-robotics/engineai_humanoid
- EngineAI Legged Gym: https://github.com/engineai-robotics/engineai_legged_gym
- MIT Cheetah: https://github.com/mit-biomimetics/Cheetah-Software
