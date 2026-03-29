/*
 * COBRA Robot - Grip Controller (Arduino Nano)
 * Version: 1.0.0
 * Handles force-sensitive gripping for delicate objects
 * Communicates with Raspberry Pi via I2C
 */

#include <Wire.h>
#include <Servo.h>

// Version
const char* FIRMWARE_VERSION = "1.0.0";

// Pin definitions
#define SDA_PIN A4
#define SCL_PIN A5
#define FSR_LEFT_PIN A0
#define FSR_RIGHT_PIN A1
#define FLEX_LEFT_PIN A2
#define FLEX_RIGHT_PIN A3
#define SERVO_LEFT_PIN 9
#define SERVO_RIGHT_PIN 10
#define CURRENT_SENSE_PIN A6
#define TOUCH_PIN 2

// I2C
#define I2C_ADDRESS 0x42
#define CMD_GRIP 0x01
#define CMD_RELEASE 0x02
#define CMD_SET_FORCE 0x03
#define CMD_GET_STATUS 0x04

// Servo objects
Servo servoLeft;
Servo servoRight;

// State variables
enum GripState {
  STATE_IDLE,
  STATE_APPROACH,
  STATE_CONTACT,
  STATE_HOLDING,
  STATE_RELEASING,
  STATE_ERROR
};

struct GripData {
  GripState state;
  float forceLeft;
  float forceRight;
  float flexLeft;
  float flexRight;
  float current;
  bool touchDetected;
  uint16_t servoPosLeft;
  uint16_t servoPosRight;
  float targetForce;
  float actualForce;
} gripData;

// Calibration
const float FSR_MIN_FORCE = 0.1;    // Newtons
const float FSR_MAX_FORCE = 10.0;   // Newtons
const float EGG_FORCE = 0.5;        // Safe egg grip force
const float FSR_VOLTAGE = 5.0;
const float FSR_RESISTANCE = 10000; // 10k pull-down

// Smoothing
const int SAMPLES = 10;
float forceBufferLeft[SAMPLES];
float forceBufferRight[SAMPLES];
int bufferIndex = 0;

// Timing
unsigned long lastUpdate = 0;
const unsigned long UPDATE_INTERVAL = 10; // 100Hz

void setup() {
  Serial.begin(115200);
  Serial.print("COBRA Grip Controller v");
  Serial.println(FIRMWARE_VERSION);
  
  // Initialize pins
  pinMode(TOUCH_PIN, INPUT);
  pinMode(FSR_LEFT_PIN, INPUT);
  pinMode(FSR_RIGHT_PIN, INPUT);
  pinMode(FLEX_LEFT_PIN, INPUT);
  pinMode(FLEX_RIGHT_PIN, INPUT);
  pinMode(CURRENT_SENSE_PIN, INPUT);
  
  // Initialize servos
  servoLeft.attach(SERVO_LEFT_PIN);
  servoRight.attach(SERVO_RIGHT_PIN);
  
  // Start position (open)
  servoLeft.write(0);
  servoRight.write(180);
  
  // Initialize I2C as slave
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(receiveCommand);
  Wire.onRequest(sendStatus);
  
  // Initialize buffers
  for (int i = 0; i < SAMPLES; i++) {
    forceBufferLeft[i] = 0;
    forceBufferRight[i] = 0;
  }
  
  // Default target force (egg mode)
  gripData.targetForce = EGG_FORCE;
  gripData.state = STATE_IDLE;
  
  Serial.println("Ready");
}

void loop() {
  unsigned long now = millis();
  
  if (now - lastUpdate >= UPDATE_INTERVAL) {
    lastUpdate = now;
    
    // Read all sensors
    readSensors();
    
    // Run state machine
    updateGripState();
    
    // Debug output
    if (Serial.available() > 0) {
      handleSerialCommand();
    }
  }
}

void readSensors() {
  // Read FSRs with smoothing
  float rawLeft = analogRead(FSR_LEFT_PIN);
  float rawRight = analogRead(FSR_RIGHT_PIN);
  
  float forceLeft = fsrToForce(rawLeft);
  float forceRight = fsrToForce(rawRight);
  
  // Update buffers
  forceBufferLeft[bufferIndex] = forceLeft;
  forceBufferRight[bufferIndex] = forceRight;
  bufferIndex = (bufferIndex + 1) % SAMPLES;
  
  // Calculate smoothed values
  gripData.forceLeft = average(forceBufferLeft, SAMPLES);
  gripData.forceRight = average(forceBufferRight, SAMPLES);
  gripData.actualForce = (gripData.forceLeft + gripData.forceRight) / 2.0;
  
  // Read flex sensors (finger compliance)
  gripData.flexLeft = analogRead(FLEX_LEFT_PIN) / 1023.0;
  gripData.flexRight = analogRead(FLEX_RIGHT_PIN) / 1023.0;
  
  // Read current sense (servo load)
  gripData.current = analogRead(CURRENT_SENSE_PIN) * (5.0 / 1023.0);
  
  // Read touch sensor
  gripData.touchDetected = digitalRead(TOUCH_PIN) == HIGH;
  
  // Track servo positions
  gripData.servoPosLeft = servoLeft.read();
  gripData.servoPosRight = servoRight.read();
}

float fsrToForce(int rawValue) {
  if (rawValue == 0) return 0;
  
  // Convert to resistance
  float voltage = rawValue * FSR_VOLTAGE / 1023.0;
  float resistance = FSR_RESISTANCE * (FSR_VOLTAGE - voltage) / voltage;
  
  // Approximate force from resistance (simplified model)
  // FSR 402: resistance decreases with force
  float force = pow(10, (log10(resistance) - 2.5) / -0.6);
  
  // Clamp to valid range
  return constrain(force, FSR_MIN_FORCE, FSR_MAX_FORCE);
}

float average(float* buffer, int size) {
  float sum = 0;
  for (int i = 0; i < size; i++) {
    sum += buffer[i];
  }
  return sum / size;
}

void updateGripState() {
  static unsigned long contactTime = 0;
  static float holdForce = 0;
  
  switch (gripData.state) {
    case STATE_IDLE:
      // Wait for touch or command
      if (gripData.touchDetected) {
        gripData.state = STATE_APPROACH;
        Serial.println("STATE: APPROACH");
      }
      break;
      
    case STATE_APPROACH:
      // Slow approach until contact
      servoLeft.write(servoLeft.read() + 1);
      servoRight.write(servoRight.read() - 1);
      
      // Check for force contact
      if (gripData.actualForce > FSR_MIN_FORCE) {
        contactTime = millis();
        gripData.state = STATE_CONTACT;
        Serial.println("STATE: CONTACT");
      }
      
      // Timeout safety
      if (servoLeft.read() > 90 || servoRight.read() < 90) {
        gripData.state = STATE_ERROR;
        Serial.println("ERROR: Max travel reached");
      }
      break;
      
    case STATE_CONTACT:
      // Build up to target force gradually
      {
        float forceError = gripData.targetForce - gripData.actualForce;
        int adjustment = constrain((int)(forceError * 5), -2, 2);
        
        servoLeft.write(servoLeft.read() + adjustment);
        servoRight.write(servoRight.read() - adjustment);
        
        // Check if at target
        if (abs(forceError) < 0.05) {
          holdForce = gripData.actualForce;
          gripData.state = STATE_HOLDING;
          Serial.println("STATE: HOLDING");
        }
        
        // Safety timeout
        if (millis() - contactTime > 2000) {
          gripData.state = STATE_HOLDING;
          Serial.println("STATE: HOLDING (timeout)");
        }
        
        // Overforce protection
        if (gripData.actualForce > gripData.targetForce * 1.5) {
          gripData.state = STATE_RELEASING;
          Serial.println("WARNING: Overforce detected");
        }
      }
      break;
      
    case STATE_HOLDING:
      // Maintain constant force (compliance control)
      {
        float forceError = holdForce - gripData.actualForce;
        int adjustment = constrain((int)(forceError * 3), -1, 1);
        
        servoLeft.write(servoLeft.read() + adjustment);
        servoRight.write(servoRight.read() - adjustment);
        
        // Detect slip (rapid force decrease)
        if (gripData.actualForce < holdForce * 0.7) {
          Serial.println("WARNING: Slip detected");
          // Brief increase to re-secure
          servoLeft.write(servoLeft.read() + 3);
          servoRight.write(servoRight.read() - 3);
        }
        
        // Detect vibration (micro-slip)
        static float lastForce = 0;
        if (abs(gripData.actualForce - lastForce) > 0.2) {
          // Object shifting - adjust compliance
          Serial.println("INFO: Object movement detected");
        }
        lastForce = gripData.actualForce;
      }
      break;
      
    case STATE_RELEASING:
      servoLeft.write(0);
      servoRight.write(180);
      delay(500);
      gripData.state = STATE_IDLE;
      Serial.println("STATE: IDLE");
      break;
      
    case STATE_ERROR:
      // Safe state
      servoLeft.write(0);
      servoRight.write(180);
      break;
  }
}

void receiveCommand(int bytes) {
  if (Wire.available() < 1) return;
  
  uint8_t cmd = Wire.read();
  
  switch (cmd) {
    case CMD_GRIP:
      if (gripData.state == STATE_IDLE) {
        gripData.state = STATE_APPROACH;
        Serial.println("CMD: GRIP");
      }
      break;
      
    case CMD_RELEASE:
      gripData.state = STATE_RELEASING;
      Serial.println("CMD: RELEASE");
      break;
      
    case CMD_SET_FORCE:
      if (Wire.available() >= 4) {
        uint8_t forceBytes[4];
        for (int i = 0; i < 4; i++) {
          forceBytes[i] = Wire.read();
        }
        float newForce = *((float*)forceBytes);
        gripData.targetForce = constrain(newForce, 0.1, 10.0);
        Serial.print("CMD: SET_FORCE=");
        Serial.println(gripData.targetForce);
      }
      break;
      
    case CMD_GET_STATUS:
      // Handled in sendStatus
      break;
  }
}

void sendStatus() {
  // Pack status into bytes
  uint8_t buffer[22];
  
  buffer[0] = (uint8_t)gripData.state;
  
  // Force values (4 bytes each)
  memcpy(&buffer[1], &gripData.forceLeft, 4);
  memcpy(&buffer[5], &gripData.forceRight, 4);
  memcpy(&buffer[9], &gripData.actualForce, 4);
  memcpy(&buffer[13], &gripData.targetForce, 4);
  
  // Flex values (1 byte each, scaled)
  buffer[17] = (uint8_t)(gripData.flexLeft * 255);
  buffer[18] = (uint8_t)(gripData.flexRight * 255);
  
  // Current (1 byte, scaled)
  buffer[19] = (uint8_t)(gripData.current * 50);
  
  // Touch and positions
  buffer[20] = gripData.touchDetected ? 1 : 0;
  buffer[21] = (uint8_t)gripData.servoPosLeft;
  
  Wire.write(buffer, 22);
}

void handleSerialCommand() {
  char cmd = Serial.read();
  
  switch (cmd) {
    case 'g':
      if (gripData.state == STATE_IDLE) {
        gripData.state = STATE_APPROACH;
        Serial.println("Grip initiated");
      }
      break;
      
    case 'r':
      gripData.state = STATE_RELEASING;
      Serial.println("Release initiated");
      break;
      
    case 'e':
      gripData.targetForce = EGG_FORCE;
      Serial.println("Mode: EGG (0.5N)");
      break;
      
    case 'f':
      gripData.targetForce = 2.0;
      Serial.println("Mode: FIRM (2.0N)");
      break;
      
    case 's':
      Serial.println("\n--- Status ---");
      Serial.print("State: ");
      Serial.println(gripData.state);
      Serial.print("Force L/R: ");
      Serial.print(gripData.forceLeft);
      Serial.print(" / ");
      Serial.println(gripData.forceRight);
      Serial.print("Target: ");
      Serial.println(gripData.targetForce);
      Serial.print("Touch: ");
      Serial.println(gripData.touchDetected ? "YES" : "NO");
      Serial.print("Current: ");
      Serial.println(gripData.current);
      Serial.println("--------------");
      break;
      
    case 'h':
      Serial.println("Commands: g=grip, r=release, e=egg mode, f=firm mode, s=status, h=help");
      break;
  }
}
