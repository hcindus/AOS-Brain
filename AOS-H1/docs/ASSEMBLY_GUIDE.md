# AOS-H1 Assembly Guide
## Step-by-Step Construction Manual

**Version:** 1.0  
**Date:** March 30, 2026  
**Estimated Build Time:** 40-60 hours

---

## SAFETY FIRST

⚠️ **Before starting:**
- Read all instructions twice before acting
- Wear safety glasses when assembling
- Keep LiPo batteries away from metal objects
- Never short-circuit batteries
- Use ESD protection when handling electronics
- Have a fire extinguisher nearby for LiPo safety

---

## TOOLS REQUIRED

### Essential
- [ ] Phillips head screwdriver set
- [ ] Hex key set (metric)
- [ ] Needle-nose pliers
- [ ] Wire cutters/strippers
- [ ] Soldering iron (temperature controlled)
- [ ] Multimeter
- [ ] Heat gun (for heat shrink)

### Recommended
- [ ] Helping hands with magnifier
- [ ] Third hand tool
- [ ] Tweezers set (ESD safe)
- [ ] Calipers (digital)
- [ ] ESD wrist strap
- [ ] Work mat

---

## PHASE 1: 3D PRINTING (Days 1-12)

### Print Queue

**Week 1:**
- Day 1-2: Torso components (42 hours)
- Day 3-4: Head components (18 hours)
- Day 5-7: Right arm components (56 hours)

**Week 2:**
- Day 8-10: Left arm components (56 hours)
- Day 11-12: Leg components (96 hours total, print both simultaneously)

### Post-Processing Checklist

For each printed part:
- [ ] Remove supports carefully
- [ ] Sand mating surfaces smooth
- [ ] Clean out screw holes
- [ ] Install heat-set inserts (where marked)
- [ ] Test fit with mating parts
- [ ] Label part with masking tape

---

## PHASE 2: ELECTRONICS PREPARATION (Day 13-15)

### Step 2.1: Solder ESP32 Nodes (4 hours)

**Head Node (ESP32-S3):**
```
Pins to solder:
- GPIO 0-15: Camera connections
- GPIO 16-21: Audio I/O
- 3.3V, GND: Power
- UART TX/RX: CAN module
```

**Torso Node (ESP32-S3):**
```
Pins to solder:
- I2C SDA/SCL: IMU, sensors
- SPI: SD card, display
- GPIO: Emergency stop input
- CAN TX/RX: Bus communication
```

**Arm/Leg Nodes (ESP32 × 4):**
```
Pins to solder (each):
- GPIO 0-15: Servo PWM signals
- ADC pins: Current sensing
- I2C: AS5600 encoders
- UART: CAN module
```

**Power Node (ESP32-C3):**
```
Pins to solder:
- ADC: Battery voltage monitoring
- GPIO: Relay control
- I2C: BMS communication
- UART: Debug
```

### Step 2.2: Assemble CAN Bus Network (3 hours)

**Wiring Diagram:**
```
Pi 5 (Node 0) ←→ Head (1) ←→ Torso (2) ←→ L-Arm (3) ←→ R-Arm (4) ←→ L-Leg (5) ←→ R-Leg (6) ←→ Power (7)
     ↑_________ Termination 120Ω _________↓
```

**Instructions:**
1. Cut CAT5 cable to lengths needed
2. Strip ends, expose twisted pairs
3. Connect CAN_H (orange), CAN_L (orange/white)
4. Connect GND (blue), VCC (blue/white) - optional
5. Solder to MCP2515 modules
6. Test continuity with multimeter

### Step 2.3: Servo Wiring Harness (4 hours)

**Per Servo Connection:**
```
Servo Pin → PCA9685 Channel → ESP32 GPIO

Signal: Orange → PWM channel
Power+: Red → 5V/12V rail
GND: Brown → Common ground
```

**Build Harnesses:**
- Left arm: 7 servos → 1 PCA9685 → Node 3
- Right arm: 7 servos → 1 PCA9685 → Node 4
- Left leg: 6 servos → 1 PCA9685 → Node 5
- Right leg: 6 servos → 1 PCA9685 → Node 6
- Head: 2 servos → PCA9685 on Node 1
- Torso: 2 servos → PCA9685 on Node 2

---

## PHASE 3: TORSO ASSEMBLY (Day 16-17)

### Step 3.1: Install Brain (2 hours)

**Mount Pi 5:**
1. Install active cooler on Pi 5
2. Screw Pi 5 into torso_brain_mount
3. Connect NVMe SSD via M.2 HAT
4. Install AI HAT+ on GPIO header
5. Route USB-C power cable

**Install CAN Hub:**
1. Mount MCP2515 hub in torso
2. Connect Pi 5 to hub (SPI)
3. Route CAN bus to all body sections
4. Install 120Ω termination resistors

### Step 3.2: Power System (3 hours)

**Battery Bay:**
1. Mount torso_battery_mount
2. Install battery retention straps
3. Connect BMS to battery
4. Wire main power switch
5. Install emergency stop button

**Power Distribution:**
1. Mount buck converters
2. Connect 24V → 12V (servos)
3. Connect 24V → 5V (logic/Pi 5)
4. Connect 24V → 3.3V (MCUs)
5. Wire current sensors (INA219)

**Test:**
- [ ] Check all voltages with multimeter
- [ ] Test emergency stop
- [ ] Verify current sensors reading

### Step 3.3: Cooling System (1 hour)

1. Mount 120mm fan in torso
2. Connect PWM control to Node 2
3. Install air intake filter
4. Route exhaust through back panel
5. Test fan operation

---

## PHASE 4: HEAD ASSEMBLY (Day 18-19)

### Step 4.1: Install Sensors (2 hours)

**Camera Array:**
1. Mount 4x ESP32-CAM modules
2. Wire to Head Node (ESP32-S3)
3. Route USB cables through neck
4. Test each camera

**Audio System:**
1. Install INMP441 microphones
2. Mount MAX98357A amplifiers
3. Install speakers in head_speaker_enclosures
4. Wire to Head Node I2S pins

**Display:**
1. Mount 1.3" OLED in forehead
2. Wire I2C to Head Node
3. Test display output

### Step 4.2: Neck Mechanism (2 hours)

**Assemble Gimbal:**
1. Mount head_neck_base to torso
2. Install pan servo (MG996R)
3. Install tilt servo (MG996R)
4. Connect head_skull_main
5. Test range of motion

**Wiring:**
1. Route all head cables through neck
2. Use slip-ring connector (optional)
3. Leave service loop for movement
4. Secure with cable ties

### Step 4.3: Face Assembly (1 hour)

1. Install RGB LEDs (eyes)
2. Mount head_face_panel
3. Connect LED controller
4. Test eye expressions

---

## PHASE 5: ARM ASSEMBLY (Day 20-24)

### Step 5.1: Shoulder Joint (Right Arm) (4 hours)

**Build Dual-Axis Gimbal:**
1. Mount arm_shoulder_base to torso bracket
2. Install pitch axis servo (DS3218)
3. Install roll axis servo (DS3218)
4. Test both axes independently
5. Calibrate neutral position

**Calibration:**
```python
# Set zero positions
shoulder_pitch.set_angle(90)  # Horizontal
shoulder_roll.set_angle(90)   # Neutral
```

### Step 5.2: Upper Arm (3 hours)

1. Connect arm_upper_tube to shoulder
2. Install upper arm twist servo
3. Wire AS5600 encoder
4. Mount current sensor
5. Route cables through tube

### Step 5.3: Elbow (2 hours)

1. Assemble arm_elbow_joint
2. Install elbow servo (DS3218)
3. Connect forearm
4. Test 0-135° range

### Step 5.4: Forearm & Wrist (3 hours)

1. Build arm_forearm_tube
2. Install forearm twist servo
3. Assemble 2-axis wrist
   - Install pitch servo
   - Install yaw servo
4. Test full wrist range

### Step 5.5: Hand Assembly (4 hours)

**Palm:**
1. Mount arm_palm_base
2. Install 5 servo mounts

**Fingers (×4):**
For each finger:
1. Assemble finger_base
2. Connect segment_1
3. Connect segment_2
4. Install tip (TPU)
5. Mount servo in palm
6. Connect tendon/wire

**Thumb:**
1. Assemble thumb_base (opposable mount)
2. Build thumb segments
3. Mount opposing to fingers
4. Connect servo

**Test:**
- [ ] Each finger curls independently
- [ ] Thumb opposes properly
- [ ] Full fist position achievable

### Step 5.6: Wiring & Testing (2 hours)

1. Connect all servos to PCA9685
2. Wire encoders to Node 3
3. Install current sensors
4. Upload arm_node firmware
5. Test all 7 DOF

**Repeat for Left Arm (Days 22-24)**

---

## PHASE 6: LEG ASSEMBLY (Day 25-30)

### Step 6.1: Hip Joint (Right Leg) (4 hours)

**Build Triple-Axis Hip:**
1. Mount leg_hip_base to waist
2. Install pitch servo (DS3218)
3. Install roll servo (DS3218)
4. Install yaw servo (DS3218)
5. Test all three axes

### Step 6.2: Thigh & Knee (3 hours)

1. Assemble leg_thigh_tube
2. Install thigh IMU (MPU6050)
3. Build leg_knee_joint
4. Install knee servo
5. Test 0-135° range

### Step 6.3: Shin & Ankle (3 hours)

1. Assemble leg_shin_tube
2. Install shin IMU
3. Build ankle (2-axis)
4. Install pitch & roll servos
5. Test ankle range

### Step 6.4: Foot (2 hours)

1. Assemble leg_foot_base
2. Mount 4x FSR pressure sensors
3. Install leg_foot_sole (TPU)
4. Wire sensors to Node 5
5. Test pressure readings

### Step 6.5: Wiring & Testing (2 hours)

1. Connect all leg servos
2. Wire IMUs and sensors
3. Upload leg_node firmware
4. Test all 6 DOF
5. Verify balance when standing

**Repeat for Left Leg (Days 28-30)**

---

## PHASE 7: INTEGRATION (Day 31-33)

### Step 7.1: Waist Assembly (2 hours)

1. Mount waist_pelvis_upper to torso
2. Install rotation servo (MG996R)
3. Connect waist_pelvis_lower
4. Attach leg assemblies
5. Test rotation

### Step 7.2: Full Wiring (4 hours)

**Route Cables:**
1. Head → Torso (through neck)
2. Arms → Torso (through shoulders)
3. Legs → Torso (through waist)
4. Keep power and signal separate
5. Use cable management sleeve

**Connect Power:**
1. Main battery → BMS → Switch
2. Switch → Distribution board
3. Test all voltages
4. Verify emergency stop

### Step 7.3: Close Panels (1 hour)

1. Install torso_back_panel
2. Install torso_front_panel
3. Secure with screws
4. Label access points

---

## PHASE 8: SOFTWARE SETUP (Day 34-36)

### Step 8.1: Brain Setup (3 hours)

**Install OS:**
```bash
# On Pi 5
sudo apt update
sudo apt install -y python3-pip git
pip3 install numpy pandas canopen

# Install AOS-H1 software
git clone https://github.com/openclaw/aos-h1.git
cd aos-h1
pip3 install -e .
```

**Configure CAN:**
```bash
# Enable SPI for MCP2515
sudo nano /boot/config.txt
# Add: dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
sudo reboot
```

### Step 8.2: Node Firmware (3 hours)

**Upload to each ESP32:**
```bash
# Using Arduino IDE or PlatformIO
cd firmware/nodes/

# Head node
pio run -t upload -e head_node

# Arm nodes
pio run -t upload -e arm_node_left
pio run -t upload -t upload -e arm_node_right

# Leg nodes
pio run -t upload -e leg_node_left
pio run -t upload -e leg_node_right
```

### Step 8.3: Calibration (3 hours)

**Joint Zeroing:**
```python
from aos_h1 import H1Robot

robot = H1Robot()
robot.calibrate_all_joints()
robot.save_calibration("calibration.json")
```

**IMU Calibration:**
```
1. Place robot on level surface
2. Run imu_calibrate.py
3. Follow prompts for each axis
4. Save calibration data
```

---

## PHASE 9: TESTING (Day 37-40)

### Basic Tests

**Power-On Test:**
- [ ] All systems boot
- [ ] No smoke/smell
- [ ] Voltages in range
- [ ] CAN bus active

**Communication Test:**
- [ ] Ping all nodes
- [ ] Read sensor data
- [ ] Control servos individually

**Joint Tests:**
- [ ] Each joint moves smoothly
- [ ] No binding or noise
- [ ] Full range achievable
- [ ] Encoders reading

**Safety Tests:**
- [ ] Emergency stop works
- [ ] Current limits enforced
- [ ] Temperature sensors reading
- [ ] Battery protection active

### Functional Tests

**Head:**
- [ ] Pan 180°
- [ ] Tilt ±45°
- [ ] All cameras work
- [ ] Audio in/out
- [ ] Eyes display colors

**Arms:**
- [ ] Reach full extension
- [ ] Touch opposite shoulder
- [ ] Full hand curl
- [ ] Thumb opposition

**Legs:**
- [ ] Stand upright (static)
- [ ] Shift weight side-to-side
- [ ] Bend knees
- [ ] Lift each foot

### Performance Tests

**Stability:**
- [ ] Stand for 5 minutes
- [ ] Balance on one foot (assisted)
- [ ] Recover from light push

**Motion:**
- [ ] Wave arms
- [ ] Turn head
- [ ] Crouch/stand
- [ ] (Later) Walk forward

---

## TROUBLESHOOTING

### Servo Not Responding
1. Check power connection
2. Verify signal wire
3. Test with servo tester
4. Check PCA9685 channel

### CAN Bus Errors
1. Check termination resistors
2. Verify wiring continuity
3. Check MCP2515 power
4. Verify bit rate (500kbps)

### IMU Drift
1. Recalibrate
2. Check for magnetic interference
3. Verify mounting (isolated)
4. Update fusion algorithm

### Power Issues
1. Check battery voltage
2. Verify BMS function
3. Check buck converter output
4. Measure current draw

---

## NEXT STEPS

After successful assembly:

1. **Software Development**
   - Install agent harness
   - Connect to cloud brain
   - Train walking gait

2. **Testing**
   - Walking on flat ground
   - Stair climbing
   - Object manipulation

3. **Improvements**
   - Upgrade servos as needed
   - Add skin/shell
   - Improve appearance

---

## SUPPORT

**Discord:** https://discord.gg/clawd  
**GitHub:** https://github.com/openclaw/aos-h1  
**Docs:** https://docs.openclaw.ai/h1/assembly

---

**Document Version:** 1.0  
**Last Updated:** March 30, 2026
