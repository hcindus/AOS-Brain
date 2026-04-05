#!/usr/bin/env python3
"""
COBRA Robot - Spine Control Interface (Raspberry Pi)
Version: 1.0.0

High-level control for 25-vertebra snake robot
Implements locomotion gaits, balance control, and coordination
"""

import serial
import struct
import time
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple, Callable
from enum import Enum
import threading
import logging

__version__ = "1.0.0"


class LocomotionPattern(Enum):
    """Serpentine locomotion patterns"""
    IDLE = 0
    SERPENTINE = 1      # Side-to-side wave (forward)
    CONCERTINA = 2      # Accordion motion (tight spaces)
    RECTILINEAR = 3     # Straight-line (slow, precise)
    SIDEWINDING = 4     # Desert sidewinder (fast)
    ROLLING = 5         # Rolling locomotion (obstacles)
    BALANCE = 6         # Balance correction mode


@dataclass
class SpineStatus:
    """Complete spine status"""
    positions: np.ndarray  # 25x2 array [vertebra, pitch/roll]
    pattern: LocomotionPattern
    amplitude: float
    frequency: float
    phase: float
    balance_pitch: float
    balance_roll: float
    timestamp: float


class CobraSpineController:
    """
    High-level spine controller for COBRA robot
    
    Features:
    - 25 vertebrae with 2 DOF each (pitch, roll)
    - Serpentine locomotion patterns
    - Real-time balance correction via IMU
    - Smooth interpolation and speed control
    """
    
    # Serial configuration
    DEFAULT_PORT = '/dev/ttyUSB0'
    DEFAULT_BAUD = 115200
    
    # Command types (match Arduino)
    CMD_MOVE_SERVO = 0x01
    CMD_MOVE_ALL = 0x02
    CMD_SET_PATTERN = 0x03
    CMD_STOP = 0x04
    CMD_GET_POSITIONS = 0x05
    CMD_BALANCE_UPDATE = 0x06
    CMD_CALIBRATE = 0x07
    CMD_EMERGENCY_STOP = 0xFF
    
    def __init__(self, port: str = DEFAULT_PORT, baud: int = DEFAULT_BAUD):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"COBRA Spine Controller v{__version__}")
        
        # Initialize serial connection
        try:
            self.ser = serial.Serial(port, baud, timeout=1.0)
            self.logger.info(f"Connected to {port} at {baud} baud")
        except Exception as e:
            self.logger.error(f"Failed to connect to Arduino: {e}")
            raise
        
        # State
        self._running = False
        self._control_thread: Optional[threading.Thread] = None
        self._current_status: Optional[SpineStatus] = None
        self._lock = threading.Lock()
        
        # Pattern parameters
        self._pattern = LocomotionPattern.IDLE
        self._amplitude = 30.0
        self._frequency = 1.0
        self._phase_offset = np.pi / 4
        self._speed = 0.5
        
        # Balance data
        self._balance_pitch = 0.0
        self._balance_roll = 0.0
        
        # Callbacks
        self._callbacks: List[Callable[[SpineStatus], None]] = []
        
        # Initialize positions
        self._positions = np.full((25, 2), 90.0)
        
        time.sleep(2)  # Wait for Arduino boot
        self.center_all()
        self.logger.info("Spine controller ready")
    
    def _send_command(self, cmd: int, data: bytes = b'') -> bool:
        """Send command to Arduino"""
        try:
            packet = bytes([cmd]) + data
            self.ser.write(packet)
            self.ser.flush()
            return True
        except Exception as e:
            self.logger.error(f"Failed to send command: {e}")
            return False
    
    def move_servo(self, vertebra: int, servo: int, 
                   degrees: float, speed: float = 0.5) -> bool:
        """
        Move single servo
        
        Args:
            vertebra: 0-24 (V1-V25)
            servo: 0=pitch, 1=roll
            degrees: 0-180
            speed: 0-1 interpolation speed
        """
        if not (0 <= vertebra < 25 and 0 <= servo < 2):
            return False
        
        degrees = max(0, min(180, int(degrees)))
        speed_byte = int(speed * 255)
        
        data = struct.pack('>BBH', vertebra, servo, degrees)
        data += bytes([speed_byte])
        
        return self._send_command(self.CMD_MOVE_SERVO, data)
    
    def move_vertebra(self, vertebra: int, 
                      pitch: float, roll: float, 
                      speed: float = 0.5) -> bool:
        """Move single vertebra (both servos)"""
        if not (0 <= vertebra < 25):
            return False
        
        success = True
        success &= self.move_servo(vertebra, 0, pitch, speed)
        time.sleep(0.01)
        success &= self.move_servo(vertebra, 1, roll, speed)
        
        return success
    
    def move_all(self, position: float, speed: float = 0.5) -> bool:
        """Move all servos to same position"""
        position = int(max(0, min(180, position)))
        speed_byte = int(speed * 255)
        
        data = struct.pack('>H', position)
        data += bytes([speed_byte])
        
        return self._send_command(self.CMD_MOVE_ALL, data)
    
    def center_all(self) -> bool:
        """Center all servos to 90 degrees"""
        self.logger.info("Centering all servos...")
        return self.move_all(90, speed=0.3)
    
    def set_pattern(self, pattern: LocomotionPattern,
                   amplitude: float = 30.0,
                   frequency: float = 1.0,
                   phase: float = None,
                   speed: float = 0.5) -> bool:
        """
        Set locomotion pattern
        
        Args:
            pattern: Locomotion pattern type
            amplitude: Wave amplitude in degrees (0-90)
            frequency: Wave frequency in Hz
            phase: Phase offset (radians), auto-calculated if None
            speed: Movement speed (0-1)
        """
        self._pattern = pattern
        self._amplitude = max(0, min(90, amplitude))
        self._frequency = max(0.1, frequency)
        self._speed = max(0, min(1, speed))
        
        if phase is None:
            # Auto-calculate phase for serpentine
            if pattern == LocomotionPattern.SERPENTINE:
                self._phase_offset = np.pi / 6
            elif pattern == LocomotionPattern.SIDEWINDING:
                self._phase_offset = np.pi / 3
            else:
                self._phase_offset = 0
        else:
            self._phase_offset = phase
        
        # Send to Arduino
        data = bytes([
            pattern.value,
            int(self._amplitude),
            int(self._frequency * 10),
            int(self._phase_offset * 255 / (2 * np.pi)),
            int(self._speed * 255)
        ])
        
        if self._send_command(self.CMD_SET_PATTERN, data):
            self.logger.info(f"Pattern set: {pattern.name}")
            return True
        return False
    
    def stop(self) -> bool:
        """Stop current motion"""
        self._pattern = LocomotionPattern.IDLE
        return self._send_command(self.CMD_STOP)
    
    def update_balance(self, pitch: float, roll: float,
                      pitch_rate: float, roll_rate: float) -> bool:
        """
        Update balance data from IMU
        
        Args:
            pitch: Pitch angle in degrees
            roll: Roll angle in degrees
            pitch_rate: Pitch rate in deg/s
            roll_rate: Roll rate in deg/s
        """
        self._balance_pitch = pitch
        self._balance_roll = roll
        
        # Scale to int16 for transmission
        p = int(pitch * 100)
        r = int(roll * 100)
        pr = int(pitch_rate * 100)
        rr = int(roll_rate * 100)
        
        data = struct.pack('>hhhh', p, r, pr, rr)
        return self._send_command(self.CMD_BALANCE_UPDATE, data)
    
    def get_positions(self) -> Optional[np.ndarray]:
        """Get current servo positions from Arduino"""
        try:
            self._send_command(self.CMD_GET_POSITIONS)
            time.sleep(0.1)
            
            if self.ser.in_waiting >= 100:  # 25 * 2 * 2 bytes
                data = self.ser.read(100)
                positions = np.frombuffer(data, dtype=np.int16).reshape(25, 2)
                
                with self._lock:
                    self._positions = positions
                
                return positions
        except Exception as e:
            self.logger.error(f"Failed to get positions: {e}")
        
        return None
    
    def calibrate(self) -> bool:
        """Run calibration routine"""
        self.logger.info("Starting calibration...")
        return self._send_command(self.CMD_CALIBRATE)
    
    def emergency_stop(self):
        """Emergency stop - requires reset"""
        self.logger.critical("EMERGENCY STOP ACTIVATED")
        self._send_command(self.CMD_EMERGENCY_STOP)
        self._running = False
    
    def start_control_loop(self, rate: float = 50.0):
        """
        Start background control thread
        
        Args:
            rate: Update rate in Hz
        """
        if self._running:
            return
        
        self._running = True
        interval = 1.0 / rate
        
        self._control_thread = threading.Thread(
            target=self._control_loop,
            args=(interval,),
            daemon=True
        )
        self._control_thread.start()
        self.logger.info(f"Control loop started at {rate}Hz")
    
    def stop_control_loop(self):
        """Stop background control"""
        self._running = False
        if self._control_thread:
            self._control_thread.join(timeout=2.0)
        self.logger.info("Control loop stopped")
    
    def _control_loop(self, interval: float):
        """Background control thread"""
        while self._running:
            start = time.time()
            
            # Get current positions
            positions = self.get_positions()
            
            # Calculate status
            if positions is not None:
                status = SpineStatus(
                    positions=positions.copy(),
                    pattern=self._pattern,
                    amplitude=self._amplitude,
                    frequency=self._frequency,
                    phase=self._phase_offset,
                    balance_pitch=self._balance_pitch,
                    balance_roll=self._balance_roll,
                    timestamp=time.time()
                )
                
                with self._lock:
                    self._current_status = status
                
                # Notify callbacks
                for callback in self._callbacks:
                    try:
                        callback(status)
                    except Exception as e:
                        self.logger.error(f"Callback error: {e}")
            
            # Maintain rate
            elapsed = time.time() - start
            if elapsed < interval:
                time.sleep(interval - elapsed)
    
    def get_status(self) -> Optional[SpineStatus]:
        """Get current spine status"""
        with self._lock:
            return self._current_status
    
    def register_callback(self, callback: Callable[[SpineStatus], None]):
        """Register status callback"""
        self._callbacks.append(callback)
    
    def close(self):
        """Clean shutdown"""
        self.stop_control_loop()
        self.center_all()
        self.ser.close()
        self.logger.info("Spine controller closed")


class CobraMotionPlanner:
    """
    High-level motion planning for COBRA
    Generates smooth trajectories and gait transitions
    """
    
    def __init__(self, spine: CobraSpineController):
        self.spine = spine
        self.logger = logging.getLogger(__name__)
    
    def move_forward(self, distance: float, speed: float = 0.5) -> bool:
        """
        Move forward using serpentine gait
        
        Args:
            distance: Distance to travel (approximate)
            speed: Movement speed (0-1)
        """
        self.logger.info(f"Moving forward {distance}m at speed {speed}")
        
        # Calculate timing based on speed and distance
        # Approximate: 1 wave cycle = 0.1m at speed 0.5
        cycles = distance / (0.1 * speed / 0.5)
        duration = cycles / self.spine._frequency
        
        # Start serpentine pattern
        self.spine.set_pattern(
            LocomotionPattern.SERPENTINE,
            amplitude=30.0,
            frequency=1.0 + speed,
            speed=speed
        )
        
        time.sleep(duration)
        self.spine.stop()
        
        return True
    
    def turn(self, angle: float, speed: float = 0.3) -> bool:
        """
        Turn in place
        
        Args:
            angle: Angle in degrees (positive = right, negative = left)
            speed: Turn speed (0-1)
        """
        self.logger.info(f"Turning {angle} degrees")
        
        # Use sidewinding with bias
        bias = np.sign(angle) * 15  # Asymmetric amplitude
        
        # Calculate duration based on angle
        # Approximate: 1 second = 45 degrees at speed 0.3
        duration = abs(angle) / (45 * speed / 0.3)
        
        self.spine.set_pattern(
            LocomotionPattern.SIDEWINDING,
            amplitude=30.0 + bias,
            frequency=0.8,
            speed=speed
        )
        
        time.sleep(duration)
        self.spine.stop()
        
        return True
    
    def navigate_obstacle(self, height: float) -> bool:
        """
        Navigate over obstacle using rolling gait
        
        Args:
            height: Obstacle height in meters
        """
        self.logger.info(f"Navigating obstacle {height}m")
        
        # Approach
        self.spine.move_forward(0.3, speed=0.3)
        time.sleep(1)
        
        # Raise head
        for v in range(7):  # Cervical
            self.spine.move_servo(v, 0, 45, speed=0.5)
        time.sleep(2)
        
        # Roll over using serpentine at higher amplitude
        self.spine.set_pattern(
            LocomotionPattern.SERPENTINE,
            amplitude=45.0,
            frequency=1.5,
            speed=0.4
        )
        time.sleep(3)
        
        # Lower head
        self.spine.center_all()
        self.spine.stop()
        
        return True
    
    def balance_correction(self, target_pitch: float = 0, 
                          target_roll: float = 0) -> bool:
        """
        Apply balance correction
        
        Args:
            target_pitch: Target pitch angle
            target_roll: Target roll angle
        """
        # Use PID-like correction
        kp = 2.0
        
        # Apply to cervical spine to stabilize head
        for v in range(7):
            correction_pitch = (target_pitch - self.spine._balance_pitch) * kp
            correction_roll = (target_roll - self.spine._balance_roll) * kp
            
            # Limit corrections
            correction_pitch = max(-20, min(20, correction_pitch))
            correction_roll = max(-20, min(20, correction_roll))
            
            # Progressive correction (more at head)
            factor = 1.0 - (v / 7.0) * 0.5
            
            self.spine.move_servo(v, 0, 90 + correction_pitch * factor, speed=0.8)
            self.spine.move_servo(v, 1, 90 + correction_roll * factor, speed=0.8)
        
        return True


# Demo
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("COBRA Spine Controller Demo")
    print("=" * 60)
    
    # Initialize controller
    spine = CobraSpineController('/dev/ttyUSB0', 115200)
    planner = CobraMotionPlanner(spine)
    
    # Start control loop
    spine.start_control_loop(rate=50)
    
    try:
        # Demo sequences
        print("\n1. Testing center position...")
        spine.center_all()
        time.sleep(2)
        
        print("\n2. Testing individual vertebra movement...")
        spine.move_vertebra(0, 120, 90, speed=0.5)  # Head up
        time.sleep(1)
        spine.move_vertebra(0, 60, 90, speed=0.5)   # Head down
        time.sleep(1)
        spine.center_all()
        time.sleep(1)
        
        print("\n3. Testing serpentine pattern...")
        spine.set_pattern(LocomotionPattern.SERPENTINE, amplitude=25, frequency=1.0)
        time.sleep(3)
        spine.stop()
        time.sleep(1)
        
        print("\n4. Testing balance correction...")
        # Simulate IMU data
        for _ in range(20):
            spine.update_balance(pitch=5, roll=-3, pitch_rate=0, roll_rate=0)
            planner.balance_correction()
            time.sleep(0.1)
        
        spine.center_all()
        
        print("\n5. Testing status reporting...")
        status = spine.get_status()
        if status:
            print(f"   Pattern: {status.pattern.name}")
            print(f"   Amplitude: {status.amplitude}")
            print(f"   Head position: {status.positions[0]}")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    finally:
        spine.center_all()
        spine.close()
        print("\nDemo complete")
