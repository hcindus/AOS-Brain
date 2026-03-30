# AOS-H1 Humanoid Robot
## Complete Build Documentation

**Project:** AOS-H1 (Autonomous Operating System - Humanoid 1)  
**Version:** 1.0  
**Date:** March 30, 2026  
**Classification:** Open Source Hardware (CERN OHL v2)

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Mechanical Design](#mechanical-design)
4. [Electronics Stack](#electronics-stack)
5. [Software Architecture](#software-architecture)
6. [Bill of Materials](#bill-of-materials)
7. [3D Printing Guide](#3d-printing-guide)
8. [Assembly Instructions](#assembly-instructions)
9. [Calibration & Testing](#calibration--testing)
10. [Agent Harness Integration](#agent-harness-integration)

---

## EXECUTIVE SUMMARY

The AOS-H1 is a fully open-source bipedal humanoid robot designed for AGI agent embodiment. Standing 120cm (4ft) tall with 25+ degrees of freedom, the H1 provides a physical platform for AI agents to interact with the real world.

### Key Specifications
- **Height:** 120cm (4ft)
- **Weight:** ~8kg (17.6 lbs)
- **DOF:** 25 (7 per arm, 6 per leg, 2 head, 2 torso, 1 waist)
- **Power:** 24V LiPo battery, ~2hr runtime
- **Compute:** Raspberry Pi 5 (8GB) + ESP32 nodes
- **Sensors:** 4 cameras, IMU, ultrasonic, pressure pads
- **Connectivity:** WiFi 6, Bluetooth 5, 4G LTE (optional)
- **Materials:** PETG-CF, TPU (flexible), aluminum 6061

### Design Philosophy
- **Modular:** Every component can be replaced/upgraded
- **Hackable:** Open STL files, open firmware
- **Affordable:** ~$1,200 total build cost
- **Safe:** Force-limited joints, compliant design

---

## SYSTEM ARCHITECTURE

### Brain-Heart-Stomach Model

```
┌─────────────────────────────────────────────────────────────┐
│                        AOS-H1 SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                           BRAIN                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐│
│  │   Cortex    │  │   PFC       │  │   Hippocampus       ││
│  │  (Pi 5)     │  │  (AI HAT+)  │  │   (ChromaDB)        ││
│  │  8GB RAM    │  │   13 TOPS   │  │   Episodic Memory   ││
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────┘│
│         │                │                                   │
│  ┌──────▼────────────────▼───────────────────────────────┐   │
│  │              Neural Bus (CAN 2.0B)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                           HEART                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Motor     │  │   Sensor    │  │   Safety            │  │
│  │   Drivers   │  │   Fusion    │  │   Monitor           │  │
│  │   (PCA9685) │  │   (Kalman)  │  │   (Watchdog)        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                          STOMACH                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Power     │  │   Thermal   │  │   Structural        │  │
│  │   (24V)     │  │   Mgmt      │  │   (Frame)           │  │
│  │   5000mAh   │  │   (Fans)    │  │   (PETG-CF)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Distributed Node Architecture

| Node | MCU | Function | Location |
|------|-----|----------|----------|
| Head Node | ESP32-S3 | Vision, Audio, Speech | Skull |
| Torso Node | ESP32-S3 | Balance, IMU, Core | Chest |
| Left Arm | ESP32 | 7x Servo Control | Shoulder |
| Right Arm | ESP32 | 7x Servo Control | Shoulder |
| Left Leg | ESP32 | 6x Servo + Balance | Hip |
| Right Leg | ESP32 | 6x Servo + Balance | Hip |
| Power Node | ESP32-C3 | Battery, Charging, Safety | Lower Back |

---

## MECHANICAL DESIGN

### 1. Torso Assembly (STLs: torso_*.stl)

**Main Torso Housing**
```
Dimensions: 200mm (W) × 150mm (H) × 120mm (D)
Volume: 3.6L internal
Print Time: 18 hours
Material: PETG-CF (2kg)
```

**Features:**
- Brain mount (Pi 5 + active cooler)
- Battery bay (24V 5000mAh LiPo)
- CAN bus hub mounting
- Cooling duct (120mm fan)
- Access panels (magnetic)
- Cable management channels

**Components:**
- torso_main_upper.stl
- torso_main_lower.stl
- torso_bracket_left.stl
- torso_bracket_right.stl
- torso_back_panel.stl
- torso_front_panel.stl
- torso_battery_mount.stl

### 2. Head Assembly (STLs: head_*.stl)

**Head Structure**
```
Dimensions: 120mm (W) × 150mm (H) × 140mm (D)
Weight: ~400g
Neck DOF: 2 (pan/tilt)
```

**Features:**
- 4-camera array (front, back, left, right)
- Speaker enclosure (stereo)
- Microphone array (4x MEMS)
- LED eyes (RGB, expressive)
- SD card slot (external)
- USB-C ports (x2)

**Components:**
- head_skull_main.stl
- head_face_panel.stl
- head_neck_base.stl
- head_neck_pivot.stl
- head_camera_mount_front.stl
- head_camera_mount_rear.stl
- head_speaker_left.stl
- head_speaker_right.stl

### 3. Arm Assemblies (STLs: arm_*.stl)

**Right & Left Arm (Mirror Design)**
```
Length: 450mm (shoulder to fingertip)
Weight: ~800g each
DOF: 7
  - Shoulder: 2 (pitch, roll)
  - Upper Arm: 1 (twist)
  - Elbow: 1 (pitch)
  - Forearm: 1 (twist)
  - Wrist: 2 (pitch, yaw)
  - Hand: 12 (4 fingers + thumb × 3 joints)
```

**Shoulder Joint**
- Dual-axis gimbal
- MG996R servos (2x)
- Ball bearing support
- Load: 5kg

**Arm Segments**
- Upper arm: 180mm
- Forearm: 160mm
- Material: PETG-CF tubes with TPU padding

**Hand Design (5 fingers)**
- Thumb: 3 DOF (oppose, flex, curl)
- Index: 3 DOF
- Middle: 3 DOF
- Ring: 3 DOF
- Pinky: 3 DOF
- **Total: 15 DOF per hand**

**Components:**
- arm_shoulder_base.stl
- arm_shoulder_pitch.stl
- arm_shoulder_roll.stl
- arm_upper_tube.stl
- arm_elbow_joint.stl
- arm_forearm_tube.stl
- arm_wrist_pitch.stl
- arm_wrist_yaw.stl
- arm_palm_base.stl
- finger_base.stl (×5)
- finger_segment_1.stl (×5)
- finger_segment_2.stl (×5)
- finger_tip.stl (×5, TPU)
- thumb_base.stl (opposable mount)

### 4. Leg Assemblies (STLs: leg_*.stl)

**Right & Left Leg (Mirror Design)**
```
Length: 550mm (hip to foot)
Weight: ~1.2kg each
DOF: 6
  - Hip: 3 (pitch, roll, yaw)
  - Knee: 1 (pitch)
  - Ankle: 2 (pitch, roll)
```

**Hip Joint**
- Triple-axis ball joint
- DS3218 servos (3x)
- Load: 10kg

**Leg Segments**
- Thigh: 220mm
- Shin: 200mm
- Material: Carbon fiber reinforced PETG

**Foot Design**
- Length: 150mm
- Width: 80mm
- 4x pressure sensors
- TPU sole (grip)
- Active ankle stabilization

**Components:**
- leg_hip_base.stl
- leg_hip_pitch.stl
- leg_hip_roll.stl
- leg_hip_yaw.stl
- leg_thigh_tube.stl
- leg_knee_joint.stl
- leg_shin_tube.stl
- leg_ankle_pitch.stl
- leg_ankle_roll.stl
- leg_foot_base.stl
- leg_foot_sole.stl (TPU)

### 5. Waist Joint (STLs: waist_*.stl)

**Torso-Leg Connection**
```
Rotation: ±90° yaw
Load: 15kg
Servo: MG996R (upgraded)
```

**Components:**
- waist_pelvis_upper.stl
- waist_pelvis_lower.stl
- waist_rotation_gear.stl
- waist_bearing_housing.stl

---

## ELECTRONICS STACK

### 1. Brain Compute (Cortex)

**Primary: Raspberry Pi 5 (8GB)**
```
Role: Main controller, AI inference, memory
OS: Ubuntu 24.04 LTS
Storage: 256GB NVMe SSD (M.2 HAT)
Cooling: Active cooler (official)
Power: 5V 5A USB-C
```

**AI Acceleration: Raspberry Pi AI HAT+**
```
Neural Accelerator: 13 TOPS
Models: ONNX, TensorFlow Lite
Power: 2W
Interface: PCIe (via GPIO)
```

**Connectivity:**
- WiFi 6 (onboard)
- Bluetooth 5 (onboard)
- 4G LTE HAT (optional)
- USB3 hub (4-port)

### 2. Distributed Nodes (Heart)

**Head Node: ESP32-S3-WROOM-1**
```
Role: Vision processing, audio I/O
Camera: ESP32-CAM (×4)
Audio: INMP441 (×4) + MAX98357A (×2)
Display: 1.3" OLED (status)
Power: 3.3V 500mA
```

**Torso Node: ESP32-S3**
```
Role: Balance, IMU, core sensors
IMU: BNO085 (9-DOF)
Pressure: BMP390 (barometer)
Temperature: DHT22 (×2)
Power: 3.3V 300mA
```

**Arm Nodes: ESP32-WROOM-32E (×2)**
```
Role: Servo control, tactile feedback
Servo Driver: PCA9685 (16ch)
Feedback: AS5600 magnetic encoders (×7)
Current sensing: INA219 (×7)
Power: 5V 10A per arm
```

**Leg Nodes: ESP32-WROOM-32E (×2)**
```
Role: Gait control, balance
Servo Driver: PCA9685 (16ch)
IMU: MPU6050 (×2, per leg)
Pressure sensors: FSR-402 (×4 per foot)
Power: 5V 15A per leg
```

**Power Node: ESP32-C3**
```
Role: Battery management, safety
BMS: BQ76930 (10S LiPo)
Charging: USB-C PD (100W)
Voltage monitoring: 24V rail
Current monitoring: INA228
Emergency cutoff: Relay (50A)
Power: 3.3V 100mA
```

### 3. Communication Bus

**CAN Bus 2.0B**
```
Controller: MCP2515 (×6 nodes)
Transceiver: TJA1051
Speed: 500kbps
Topology: Daisy chain
Termination: 120Ω at ends
```

**WiFi Mesh (Backup)**
```
Protocol: ESP-Mesh
Channel: 6 (2.4GHz)
Security: WPA3
Fallback: If CAN fails
```

### 4. Power Distribution

**24V Main Rail**
```
Battery: 6S LiPo 5000mAh (24V nominal)
Capacity: 120Wh
Runtime: ~2 hours (active)
        ~6 hours (standby)
```

**Buck Converters**
```
24V → 12V: 10A (servo rail)
24V → 5V: 20A (logic, Pi 5)
24V → 3.3V: 5A (MCUs, sensors)
```

**Power Budget**
```
Component        Power    Peak
─────────────────────────────
Pi 5 + AI HAT   15W      25W
Servos (25×)    100W     250W
ESP32 nodes     5W       8W
Sensors         3W       5W
Cameras (4×)    4W       6W
Audio           2W       5W
Misc            5W       10W
─────────────────────────────
Total           ~134W    ~309W
```

---

## SOFTWARE ARCHITECTURE

### 1. Firmware Stack

**Node Firmware (ESP32 - Arduino Framework)**
```cpp
// arm_node.ino
#include <CAN.h>
#include <ServoManager.h>
#include <SensorFusion.h>

class ArmNode {
private:
    ServoManager servos[7];
    CANBus can;
    SensorFusion imu;
    
public:
    void init() {
        // Initialize 7 servos
        // Setup CAN bus
        // Calibrate encoders
    }
    
    void loop() {
        // Read CAN commands
        // Update servo positions
        // Send telemetry
    }
};
```

**Control Loop: 100Hz**
- Servo position updates
- Sensor reading
- Safety checks
- CAN communication

### 2. Brain Software (Raspberry Pi 5)

**AOS-H1 Runtime**
```python
# aos_h1/runtime.py
class H1Runtime:
    def __init__(self):
        self.brain = Cortex()          # Main AI
        self.heart = HeartController() # Motor control
        self.stomach = PowerManager()  # Battery/safety
        self.body = Kinematics()       # IK/FK
        self.memory = EpisodicMemory() # ChromaDB
        
    def tick(self):
        # OODA loop
        observe = self.sense()
        orient = self.memory.retrieve(observe)
        decide = self.brain.decide(observe, orient)
        act = self.body.execute(decide)
        return act
```

**Agent Harness**
```python
# Agent can inhabit the body
class H1Agent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.runtime = H1Runtime()
        
    def perceive(self) -> Perception:
        """Get sensory data from body"""
        return self.runtime.sense()
    
    def act(self, action: Action) -> Result:
        """Execute action through body"""
        return self.runtime.execute(action)
    
    def learn(self, experience: Experience):
        """Store experience in memory"""
        self.runtime.memory.store(experience)
```

### 3. Control Systems

**Inverse Kinematics**
```python
def solve_ik(target_pos, joint_limits):
    """Compute joint angles for end-effector position"""
    # Jacobian-based iterative solver
    # Handles redundancy (7 DOF)
    # Respects joint limits
    pass
```

**Balance Control (ZMP)**
```python
def compute_zmp(forces, com_position):
    """Zero Moment Point for stability"""
    # Keep ZMP inside support polygon
    # Adjust ankle torques
    # Compensate with hip
    pass
```

**Gait Generation**
```python
def generate_walk(speed, direction):
    """Generate walking trajectory"""
    # COM trajectory (sinusoidal)
    # Foot placement (capture point)
    # Swing leg (Bezier curves)
    pass
```

### 4. Communication Protocol

**CAN Bus Frame Format**
```
ID: 11-bit
┌────────┬────────┬────────┐
│ Node   │ Type   │ Param  │
│ (4bit) │ (4bit) │ (3bit) │
└────────┴────────┴────────┘

Node IDs:
  0: Brain (Pi)
  1: Head
  2: Torso
  3: Left Arm
  4: Right Arm
  5: Left Leg
  6: Right Leg
  7: Power

Types:
  0: Heartbeat
  1: Position Cmd
  2: Position Rpt
  3: Sensor Data
  4: Safety Alert
  5: Debug Msg
```

---

## BILL OF MATERIALS

### Mechanical Components

| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| PETG-CF Filament (1kg) | 8 | $45 | $360 | Amazon |
| TPU Filament (1kg) | 2 | $35 | $70 | Amazon |
| Aluminum Tube 20×20mm (1m) | 4 | $12 | $48 | McMaster |
| Ball Bearing 608RS | 20 | $3 | $60 | Amazon |
| Ball Bearing 625RS | 12 | $2 | $24 | Amazon |
| Threaded Rod M8 (1m) | 2 | $8 | $16 | McMaster |
| Hex Bolts M3-M6 kit | 1 | $25 | $25 | Amazon |
| Springs (various) | 20 | $1 | $20 | Amazon |
| **Mechanical Subtotal** | | | **$623** | |

### Electronics Components

| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| Raspberry Pi 5 (8GB) | 1 | $80 | $80 | Pi Shop |
| Raspberry Pi AI HAT+ | 1 | $70 | $70 | Pi Shop |
| NVMe SSD 256GB | 1 | $35 | $35 | Amazon |
| ESP32-S3 DevKit | 2 | $12 | $24 | Amazon |
| ESP32-WROOM | 4 | $8 | $32 | Amazon |
| ESP32-C3 Mini | 1 | $5 | $5 | Amazon |
| PCA9685 Servo Driver | 6 | $12 | $72 | Adafruit |
| BNO085 IMU | 1 | $25 | $25 | Adafruit |
| MCP2515 CAN Module | 6 | $8 | $48 | Amazon |
| INA219 Current Sensor | 14 | $3 | $42 | Amazon |
| AS5600 Encoder | 25 | $4 | $100 | Amazon |
| ESP32-CAM | 4 | $8 | $32 | Amazon |
| INMP441 Mic | 4 | $4 | $16 | Amazon |
| MAX98357A Amp | 2 | $6 | $12 | Amazon |
| OLED 1.3" Display | 2 | $8 | $16 | Amazon |
| FSR-402 Pressure | 8 | $3 | $24 | Amazon |
| Buck Converter 24→12V | 2 | $12 | $24 | Amazon |
| Buck Converter 24→5V | 2 | $15 | $30 | Amazon |
| BMS 6S 100A | 1 | $45 | $45 | Amazon |
| Relays 24V | 2 | $5 | $10 | Amazon |
| Wire/Cables/Connectors | 1 | $50 | $50 | Amazon |
| PCB Prototype Boards | 10 | $5 | $50 | Amazon |
| **Electronics Subtotal** | | | **$824** | |

### Actuators

| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| DS3218 Digital Servo (20kg) | 12 | $18 | $216 | ServoCity |
| MG996R Metal Servo (10kg) | 10 | $12 | $120 | Amazon |
| SG90 Micro Servo (fingers) | 30 | $5 | $150 | Amazon |
| **Actuators Subtotal** | | | **$486** | |

### Power System

| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| 6S LiPo 5000mAh | 2 | $65 | $130 | HobbyKing |
| LiPo Charger B6AC | 1 | $55 | $55 | Amazon |
| XT90 Connectors | 10 | $3 | $30 | Amazon |
| Power Switch 50A | 2 | $8 | $16 | Amazon |
| Fuse Holder + Fuses | 5 | $4 | $20 | Amazon |
| **Power Subtotal** | | | **$251** | |

### Tools (One-time)

| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| 3D Printer (if needed) | 1 | $400 | $400 | Prusa |
| Soldering Iron | 1 | $50 | $50 | Amazon |
| Multimeter | 1 | $25 | $25 | Amazon |
| Crimping Tool | 1 | $30 | $30 | Amazon |
| Heat Gun | 1 | $20 | $20 | Amazon |
| Calipers | 1 | $15 | $15 | Amazon |
| **Tools Subtotal** | | | **$540** | |

### GRAND TOTAL

| Category | Cost |
|----------|------|
| Mechanical | $623 |
| Electronics | $824 |
| Actuators | $486 |
| Power | $251 |
| Tools (one-time) | $540 |
| **TOTAL** | **$2,224** |
| **Excluding Tools** | **$1,684** |
| **Core Build** | **$1,184** |

*Core Build = Mech + Elec + Actuators only (no power tools)*

---

## 3D PRINTING GUIDE

### Print Settings

**PETG-CF (Structural Parts)**
```
Layer Height: 0.2mm
Infill: 40% (gyroid)
Walls: 4
Top/Bottom: 4 layers
Temp: 250°C / 80°C bed
Speed: 50mm/s
Fan: 30%
Retraction: 4mm @ 45mm/s
```

**TPU (Flexible Parts - Fingers, Grips)**
```
Layer Height: 0.2mm
Infill: 25% (gyroid)
Walls: 3
Temp: 230°C / 60°C bed
Speed: 30mm/s
Fan: 0% (first 5 layers), 50% after
Retraction: 2mm @ 25mm/s
```

### Print Queue (Estimated Times)

| Assembly | Parts | Time | Filament |
|----------|-------|------|----------|
| Torso | 8 | 42h | 1.8kg PETG-CF |
| Head | 10 | 18h | 0.8kg PETG-CF |
| Right Arm | 25 | 56h | 2.2kg PETG-CF + 0.3kg TPU |
| Left Arm | 25 | 56h | 2.2kg PETG-CF + 0.3kg TPU |
| Right Leg | 15 | 48h | 2.0kg PETG-CF |
| Left Leg | 15 | 48h | 2.0kg PETG-CF |
| Waist | 4 | 12h | 0.5kg PETG-CF |
| **TOTAL** | **102** | **280h** | **11.8kg** |

*At 24h/day printing: ~12 days total*

### Post-Processing

1. **Remove supports** (tree supports recommended)
2. **Sand mating surfaces** (smooth fit)
3. **Tap threaded holes** (M3-M6)
4. **Install heat-set inserts** (where needed)
5. **Clean cooling ducts** (compressed air)

---

## ASSEMBLY INSTRUCTIONS

### Phase 1: Torso Core (Day 1-2)

1. **Print torso parts** (42h)
2. **Install Pi 5** in brain mount
3. **Mount AI HAT+**
4. **Install NVMe SSD**
5. **Wire CAN bus hub**
6. **Install battery bay**
7. **Mount cooling system**
8. **Test power distribution**

### Phase 2: Head Assembly (Day 3-4)

1. **Print head parts** (18h)
2. **Install cameras** (×4)
3. **Mount speakers**
4. **Install microphone array**
5. **Wire head node ESP32**
6. **Install LED eyes**
7. **Assemble neck mechanism**
8. **Test head movement**

### Phase 3: Arms (Day 5-9)

1. **Print arm parts** (112h total)
2. **Assemble shoulders** (dual axis)
3. **Build upper arms**
4. **Install elbow joints**
5. **Build forearms**
6. **Assemble wrists** (2-axis)
7. **Print hands** (fingers in TPU)
8. **Install 7 servos per arm**
9. **Wire arm nodes**
10. **Test range of motion**

### Phase 4: Legs (Day 10-13)

1. **Print leg parts** (96h total)
2. **Assemble hips** (3-axis)
3. **Build thighs**
4. **Install knees**
5. **Build shins**
6. **Assemble ankles** (2-axis)
7. **Build feet** with sensors
8. **Install 6 servos per leg**
9. **Wire leg nodes**
10. **Test stance**

### Phase 5: Integration (Day 14-15)

1. **Attach head to torso**
2. **Mount arms**
3. **Attach waist joint**
4. **Mount legs**
5. **Route all cables**
6. **Connect CAN bus**
7. **Power up system**
8. **Basic firmware upload**
9. **First boot sequence**

### Phase 6: Calibration (Day 16-17)

1. **Zero all joints**
2. **Calibrate IMUs**
3. **Set servo limits**
4. **Balance tuning**
5. **Gait calibration**
6. **Safety system tests**

---

## CALIBRATION & TESTING

### Joint Calibration

```python
# Set zero positions
for joint in all_joints:
    joint.home_position = current_position
    joint.save_to_eeprom()
```

### Balance Tuning

```python
# ZMP calibration
com_position = calculate_com()
zmp = calculate_zmp(pressure_sensors)
error = desired_zmp - zmp
correction = pid_controller(error)
```

### Safety Checks

- [ ] Emergency stop functional
- [ ] Current limits set
- [ ] Temperature monitoring active
- [ ] Joint limits enforced
- [ ] CAN bus heartbeat
- [ ] Battery low voltage cutoff
- [ ] Fall detection active

### Performance Tests

| Test | Target | Method |
|------|--------|--------|
| Stand still | 5 min | ZMP centered |
| Wave arms | 30 sec | No drift |
| Walk forward | 2m | Straight line |
| Turn 360° | <10s | In place |
| Pick up object | 1kg | Stable grasp |
| Stairs | 3 steps | No assistance |

---

## AGENT HARNESS INTEGRATION

### Agent SDK

```python
from aos_h1 import H1Robot, Action

class MyAgent:
    def __init__(self):
        self.body = H1Robot()
        
    def run(self):
        while True:
            perception = self.body.sense()
            decision = self.think(perception)
            self.body.act(decision)
            
    def think(self, perception):
        # Agent's decision logic
        if perception.ball_visible:
            return Action.pick_up(perception.ball_location)
        return Action.stand()

# Deploy agent to robot
agent = MyAgent()
agent.run()
```

### Cloud Connection

```python
# Agents can sync with cloud brain
from aos_h1.cloud import CloudSync

sync = CloudSync(agent_id="my-agent")
sync.upload_experiences()
sync.download_updates()
```

### Multi-Agent Coordination

```python
# Multiple agents can inhabit multiple H1s
from aos_h1.swarm import Swarm

swarm = Swarm([robot1, robot2, robot3])
swarm.coordinate_task("clean_room")
```

---

## DOCUMENTATION

### CAD Files

All STLs available in `/cad/` directory:
- Step files for editing
- STL files for printing
- BOM CSV for ordering

### Firmware

Located in `/firmware/`:
- Node firmware (Arduino)
- Brain software (Python)
- Update scripts

### Software

Located in `/software/`:
- ROS2 packages
- Simulation (Gazebo)
- Training environments

---

## LICENSE

**CERN Open Hardware License v2**

This documentation describes Open Hardware and is licensed under the CERN-OHL-S v2.

You may redistribute and modify this documentation under the terms of the CERN-OHL-S v2.

**Summary:**
- ✅ Commercial use allowed
- ✅ Modify and distribute
- ✅ Patent use granted
- ℹ️ Must include license and attribution
- ℹ️ Must share modifications

---

## SUPPORT

**Discord:** https://discord.gg/clawd  
**GitHub:** https://github.com/openclaw/aos-h1  
**Docs:** https://docs.openclaw.ai/h1  
**Email:** h1@openclaw.ai

---

## ROADMAP

### v1.0 (Current)
- Basic walking
- Object manipulation
- Voice commands
- Cloud connection

### v1.1 (Q2 2026)
- Dynamic balance
- Stair climbing
- Running (slow)
- Improved grasping

### v1.2 (Q3 2026)
- Outdoor navigation
- Autonomous charging
- Multi-agent coordination
- Learning from demonstration

### v2.0 (2027)
- Full-size (170cm)
- Hydraulic actuators
- Dexterous manipulation
- Human-speed locomotion

---

**"Building the body for AGI"**

*The AOS-H1 Project Team*  
*March 30, 2026*
