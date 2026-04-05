/*
 * COBRA Robot - Spine Controller (Arduino Nano)
 * Version: 1.0.0
 * 
 * Controls 25 vertebrae with 50 servos via PCA9685
 * Implements serpentine locomotion patterns
 * Communicates with Raspberry Pi via I2C/UART
 */

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <EEPROM.h>

// Version
const char* FIRMWARE_VERSION = "1.0.0";
const uint16_t VERSION_EEPROM_ADDR = 0;

// PCA9685 servo controllers
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x40); // V1-V16
Adafruit_PWMServoDriver pwm2 = Adafruit_PWMServoDriver(0x41); // V17-V25

// Configuration
#define SERVO_MIN_PULSE 150  // 0 degrees
#define SERVO_MAX_PULSE 600  // 180 degrees
#define SERVO_FREQ 50        // 50Hz for MG90S
#define NUM_VERTEBRAE 25
#define SERVOS_PER_VERTEBRA 2  // Pitch + Roll

// Servo mapping: vertebra -> (pwm controller, channel)
struct ServoMapping {
  uint8_t pwmNum;    // 1 or 2
  uint8_t channel;   // 0-15
};

ServoMapping servoMap[NUM_VERTEBRAE][2]; // [vertebra][0=pitch,1=roll]

// Current servo positions (degrees)
int16_t servoPositions[NUM_VERTEBRAE][2];

// Target positions for interpolation
int16_t targetPositions[NUM_VERTEBRAE][2];
float currentSpeeds[NUM_VERTEBRAE][2];

// Movement parameters
struct MovementParams {
  float amplitude;      // 0-90 degrees
  float frequency;        // Hz
  float phase;           // Phase offset
  float speed;           // Movement speed
  uint8_t waveType;      // 0=sin, 1=triangle, 2=square
};

MovementParams currentParams = {
  .amplitude = 30.0,
  .frequency = 1.0,
  .phase = 0.0,
  .speed = 0.5,
  .waveType = 0
};

// Balance control from IMU
struct BalanceData {
  float pitch;
  float roll;
  float pitchRate;
  float rollRate;
  bool valid;
};

BalanceData balance = {0, 0, 0, 0, false};

// Command types
#define CMD_MOVE_SERVO 0x01
#define CMD_MOVE_ALL 0x02
#define CMD_SET_PATTERN 0x03
#define CMD_STOP 0x04
#define CMD_GET_POSITIONS 0x05
#define CMD_BALANCE_UPDATE 0x06
#define CMD_CALIBRATE 0x07
#define CMD_EMERGENCY_STOP 0xFF

// Timing
unsigned long lastUpdate = 0;
const unsigned long UPDATE_INTERVAL = 20; // 50Hz update rate
unsigned long lastPatternUpdate = 0;

// Pattern generation
uint8_t currentPattern = 0;
float patternPhase = 0;

void setup() {
  Serial.begin(115200);
  Serial.print("COBRA Spine Controller v");
  Serial.println(FIRMWARE_VERSION);
  
  // Initialize I2C
  Wire.begin();
  Wire.setClock(400000); // 400kHz
  
  // Initialize servo controllers
  pwm1.begin();
  pwm1.setOscillatorFrequency(27000000);
  pwm1.setPWMFreq(SERVO_FREQ);
  
  pwm2.begin();
  pwm2.setOscillatorFrequency(27000000);
  pwm2.setPWMFreq(SERVO_FREQ);
  
  delay(100);
  
  // Initialize servo mapping
  initServoMapping();
  
  // Load calibration from EEPROM
  loadCalibration();
  
  // Set all servos to center position
  centerAllServos();
  
  Serial.println("Spine controller ready");
  Serial.println("Waiting for commands...");
}

void loop() {
  unsigned long now = millis();
  
  // Handle serial commands
  if (Serial.available() > 0) {
    handleSerialCommand();
  }
  
  // Update servos at fixed rate
  if (now - lastUpdate >= UPDATE_INTERVAL) {
    lastUpdate = now;
    
    // Update pattern movement
    updatePattern();
    
    // Interpolate to targets
    interpolateServos();
    
    // Apply balance corrections
    applyBalance();
    
    // Write to servos
    writeServos();
  }
}

void initServoMapping() {
  // V1-V16 on PWM1
  for (int v = 0; v < 16; v++) {
    servoMap[v][0] = {1, (uint8_t)(v * 2)};     // Pitch
    servoMap[v][1] = {1, (uint8_t)(v * 2 + 1)}; // Roll
  }
  
  // V17-V25 on PWM2
  for (int v = 16; v < NUM_VERTEBRAE; v++) {
    int idx = v - 16;
    servoMap[v][0] = {2, (uint8_t)(idx * 2)};     // Pitch
    servoMap[v][1] = {2, (uint8_t)(idx * 2 + 1)}; // Roll
  }
  
  // Initialize positions
  for (int v = 0; v < NUM_VERTEBRAE; v++) {
    for (int s = 0; s < 2; s++) {
      servoPositions[v][s] = 90;
      targetPositions[v][s] = 90;
      currentSpeeds[v][s] = 0;
    }
  }
}

void centerAllServos() {
  Serial.println("Centering all servos...");
  for (int v = 0; v < NUM_VERTEBRAE; v++) {
    for (int s = 0; s < 2; s++) {
      setServoPosition(v, s, 90);
    }
  }
  delay(500);
  Serial.println("Servos centered");
}

void setServoPosition(uint8_t vertebra, uint8_t servo, int16_t degrees) {
  // Constrain to valid range
  degrees = constrain(degrees, 0, 180);
  
  // Map to pulse
  uint16_t pulse = map(degrees, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE);
  
  // Write to appropriate PWM controller
  ServoMapping &mapping = servoMap[vertebra][servo];
  if (mapping.pwmNum == 1) {
    pwm1.setPWM(mapping.channel, 0, pulse);
  } else {
    pwm2.setPWM(mapping.channel, 0, pulse);
  }
  
  servoPositions[vertebra][servo] = degrees;
}

void moveServo(uint8_t vertebra, uint8_t servo, int16_t degrees, float speed) {
  if (vertebra >= NUM_VERTEBRAE || servo >= 2) return;
  
  targetPositions[vertebra][servo] = constrain(degrees, 0, 180);
  currentSpeeds[vertebra][servo] = speed;
}

void interpolateServos() {
  for (int v = 0; v < NUM_VERTEBRAE; v++) {
    for (int s = 0; s < 2; s++) {
      int16_t current = servoPositions[v][s];
      int16_t target = targetPositions[v][s];
      
      if (current != target) {
        int16_t diff = target - current;
        int16_t step = (int16_t)(diff * currentSpeeds[v][s]);
        
        // Minimum step
        if (abs(step) < 1) step = (diff > 0) ? 1 : -1;
        
        int16_t newPos = current + step;
        
        // Check if reached target
        if ((diff > 0 && newPos >= target) || (diff < 0 && newPos <= target)) {
          newPos = target;
        }
        
        servoPositions[v][s] = newPos;
      }
    }
  }
}

void writeServos() {
  for (int v = 0; v < NUM_VERTEBRAE; v++) {
    for (int s = 0; s < 2; s++) {
      setServoPosition(v, s, servoPositions[v][s]);
    }
  }
}

void updatePattern() {
  if (currentPattern == 0) return; // No pattern
  
  unsigned long now = millis();
  float dt = (now - lastPatternUpdate) / 1000.0;
  lastPatternUpdate = now;
  
  // Update phase
  patternPhase += currentParams.frequency * dt * 2 * PI;
  if (patternPhase > 2 * PI) patternPhase -= 2 * PI;
  
  // Generate wave based on pattern type
  for (int v = 0; v < NUM_VERTEBRAE; v++) {
    float phaseOffset = (float)v / NUM_VERTEBRAE * currentParams.phase;
    float angle = patternPhase + phaseOffset;
    
    float waveValue = 0;
    switch (currentParams.waveType) {
      case 0: // Sine
        waveValue = sin(angle);
        break;
      case 1: // Triangle
        waveValue = 2.0 / PI * asin(sin(angle));
        break;
      case 2: // Square
        waveValue = (sin(angle) >= 0) ? 1.0 : -1.0;
        break;
    }
    
    int16_t pitchPos = 90 + (int16_t)(waveValue * currentParams.amplitude);
    targetPositions[v][0] = pitchPos;
    currentSpeeds[v][0] = currentParams.speed;
  }
}

void applyBalance() {
  if (!balance.valid) return;
  
  // Apply balance corrections to base servos
  // Cervical (V1-V7): Counter head movement
  int16_t pitchCorrection = (int16_t)(-balance.pitch * 2);
  int16_t rollCorrection = (int16_t)(-balance.roll * 2);
  
  for (int v = 0; v < 7; v++) {
    targetPositions[v][0] += pitchCorrection;
    targetPositions[v][1] += rollCorrection;
  }
}

void handleSerialCommand() {
  uint8_t cmd = Serial.read();
  
  switch (cmd) {
    case CMD_MOVE_SERVO:
      {
        // Format: [cmd] [vertebra] [servo] [degrees_high] [degrees_low] [speed]
        if (Serial.available() >= 5) {
          uint8_t v = Serial.read();
          uint8_t s = Serial.read();
          int16_t deg = (Serial.read() << 8) | Serial.read();
          float speed = Serial.read() / 255.0;
          moveServo(v, s, deg, speed);
        }
      }
      break;
      
    case CMD_MOVE_ALL:
      {
        // Move all servos to same position
        if (Serial.available() >= 3) {
          int16_t deg = (Serial.read() << 8) | Serial.read();
          float speed = Serial.read() / 255.0;
          for (int v = 0; v < NUM_VERTEBRAE; v++) {
            for (int s = 0; s < 2; s++) {
              moveServo(v, s, deg, speed);
            }
          }
        }
      }
      break;
      
    case CMD_SET_PATTERN:
      {
        if (Serial.available() >= 5) {
          currentPattern = Serial.read();
          currentParams.amplitude = Serial.read();
          currentParams.frequency = Serial.read() / 10.0;
          currentParams.phase = Serial.read() * 2 * PI / 255.0;
          currentParams.speed = Serial.read() / 255.0;
          lastPatternUpdate = millis();
          Serial.print("Pattern set: ");
          Serial.println(currentPattern);
        }
      }
      break;
      
    case CMD_STOP:
      currentPattern = 0;
      for (int v = 0; v < NUM_VERTEBRAE; v++) {
        targetPositions[v][0] = servoPositions[v][0];
        targetPositions[v][1] = servoPositions[v][1];
      }
      Serial.println("Stopped");
      break;
      
    case CMD_GET_POSITIONS:
      // Send back all positions
      Serial.write((uint8_t*)servoPositions, NUM_VERTEBRAE * 2 * sizeof(int16_t));
      break;
      
    case CMD_BALANCE_UPDATE:
      {
        if (Serial.available() >= 8) {
          int16_t pitch = (Serial.read() << 8) | Serial.read();
          int16_t roll = (Serial.read() << 8) | Serial.read();
          int16_t pitchRate = (Serial.read() << 8) | Serial.read();
          int16_t rollRate = (Serial.read() << 8) | Serial.read();
          
          balance.pitch = pitch / 100.0;
          balance.roll = roll / 100.0;
          balance.pitchRate = pitchRate / 100.0;
          balance.rollRate = rollRate / 100.0;
          balance.valid = true;
        }
      }
      break;
      
    case CMD_CALIBRATE:
      centerAllServos();
      saveCalibration();
      break;
      
    case CMD_EMERGENCY_STOP:
      emergencyStop();
      break;
      
    default:
      Serial.print("Unknown command: ");
      Serial.println(cmd);
  }
}

void emergencyStop() {
  // Disable all PWM outputs
  pwm1.setPWMFreq(0);
  pwm2.setPWMFreq(0);
  
  Serial.println("EMERGENCY STOP");
  
  // Hang here until reset
  while (true) {
    delay(1000);
  }
}

void saveCalibration() {
  // Save current positions as center
  EEPROM.write(VERSION_EEPROM_ADDR, 1); // Calibration valid flag
  
  for (int v = 0; v < NUM_VERTEBRAE; v++) {
    for (int s = 0; s < 2; s++) {
      int addr = VERSION_EEPROM_ADDR + 1 + v * 4 + s * 2;
      EEPROM.write(addr, servoPositions[v][s] >> 8);
      EEPROM.write(addr + 1, servoPositions[v][s] & 0xFF);
    }
  }
  
  Serial.println("Calibration saved");
}

void loadCalibration() {
  uint8_t valid = EEPROM.read(VERSION_EEPROM_ADDR);
  if (valid != 1) {
    Serial.println("No calibration found, using defaults");
    return;
  }
  
  for (int v = 0; v < NUM_VERTEBRAE; v++) {
    for (int s = 0; s < 2; s++) {
      int addr = VERSION_EEPROM_ADDR + 1 + v * 4 + s * 2;
      int16_t pos = (EEPROM.read(addr) << 8) | EEPROM.read(addr + 1);
      servoPositions[v][s] = pos;
      targetPositions[v][s] = pos;
    }
  }
  
  Serial.println("Calibration loaded");
}
