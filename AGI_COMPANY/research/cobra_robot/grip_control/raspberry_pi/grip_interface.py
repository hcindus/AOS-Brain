#!/usr/bin/env python3
"""
COBRA Robot - Grip Control Interface (Raspberry Pi)
Version: 1.0.0

High-level grip control with object detection integration
Communicates with Arduino Nano via I2C
"""

import smbus2
import time
import struct
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable
import threading

__version__ = "1.0.0"


class GripState(Enum):
    """Grip controller states"""
    IDLE = 0
    APPROACH = 1
    CONTACT = 2
    HOLDING = 3
    RELEASING = 4
    ERROR = 5


class GripMode(Enum):
    """Preset grip modes"""
    EGG = 0.5          # Fragile objects
    DELICATE = 1.0     # Electronics, glass
    MEDIUM = 2.0       # General objects
    FIRM = 5.0         # Heavy objects
    CUSTOM = 0.0       # User defined


@dataclass
class GripStatus:
    """Complete grip status from controller"""
    state: GripState
    force_left: float
    force_right: float
    actual_force: float
    target_force: float
    flex_left: float
    flex_right: float
    current: float
    touch_detected: bool
    servo_position: int
    timestamp: float


class CobraGripController:
    """
    High-level grip controller for COBRA robot
    
    Features:
    - Force-sensitive gripping with multiple modes
    - Slip detection and auto-compensation
    - Integration with object detection
    - Real-time feedback
    """
    
    # I2C configuration
    I2C_BUS = 1
    ARDUINO_ADDRESS = 0x42
    
    # Commands
    CMD_GRIP = 0x01
    CMD_RELEASE = 0x02
    CMD_SET_FORCE = 0x03
    CMD_GET_STATUS = 0x04
    
    # Safety limits
    MAX_FORCE = 10.0          # Newtons
    MIN_FORCE = 0.1           # Newtons
    STALL_CURRENT = 1.5       # Amps
    SLIP_THRESHOLD = 0.7      # 70% force drop
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"COBRA Grip Controller v{__version__} initializing...")
        
        # Initialize I2C
        try:
            self.bus = smbus2.SMBus(self.I2C_BUS)
            self.logger.info(f"I2C bus {self.I2C_BUS} initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize I2C: {e}")
            raise
        
        # State
        self._running = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._callbacks: list[Callable] = []
        self._current_status: Optional[GripStatus] = None
        self._lock = threading.Lock()
        
        # Grip parameters
        self._mode = GripMode.MEDIUM
        self._custom_force = 2.0
        
        # Slip detection
        self._slip_history: list[float] = []
        self._slip_window = 10
        
        self.logger.info("Grip controller ready")
    
    def _read_status(self) -> Optional[GripStatus]:
        """Read current status from Arduino"""
        try:
            # Request 22 bytes from Arduino
            data = self.bus.read_i2c_block_data(
                self.ARDUINO_ADDRESS, 
                self.CMD_GET_STATUS, 
                22
            )
            
            if len(data) < 22:
                return None
            
            # Unpack data
            state = GripState(data[0])
            
            # Force values (4 bytes float each)
            force_left = struct.unpack('f', bytes(data[1:5]))[0]
            force_right = struct.unpack('f', bytes(data[5:9]))[0]
            actual_force = struct.unpack('f', bytes(data[9:13]))[0]
            target_force = struct.unpack('f', bytes(data[13:17]))[0]
            
            # Flex sensors (1 byte, scaled 0-255)
            flex_left = data[17] / 255.0
            flex_right = data[18] / 255.0
            
            # Current (1 byte, scaled)
            current = data[19] / 50.0
            
            # Touch and position
            touch = data[20] == 1
            servo_pos = data[21]
            
            return GripStatus(
                state=state,
                force_left=force_left,
                force_right=force_right,
                actual_force=actual_force,
                target_force=target_force,
                flex_left=flex_left,
                flex_right=flex_right,
                current=current,
                touch_detected=touch,
                servo_position=servo_pos,
                timestamp=time.time()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to read status: {e}")
            return None
    
    def grip(self, mode: Optional[GripMode] = None, 
             custom_force: Optional[float] = None) -> bool:
        """
        Initiate grip sequence
        
        Args:
            mode: Predefined grip mode
            custom_force: Custom force in Newtons (if mode is CUSTOM)
            
        Returns:
            True if command sent successfully
        """
        if mode:
            self._mode = mode
            
        if mode == GripMode.CUSTOM and custom_force:
            self._custom_force = max(self.MIN_FORCE, 
                                    min(self.MAX_FORCE, custom_force))
        
        # Set target force
        target = self._get_target_force()
        self.set_target_force(target)
        
        # Send grip command
        try:
            self.bus.write_byte(self.ARDUINO_ADDRESS, self.CMD_GRIP)
            self.logger.info(f"Grip initiated: {self._mode.name} ({target:.2f}N)")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send grip command: {e}")
            return False
    
    def release(self) -> bool:
        """Release grip"""
        try:
            self.bus.write_byte(self.ARDUINO_ADDRESS, self.CMD_RELEASE)
            self.logger.info("Release initiated")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send release command: {e}")
            return False
    
    def set_target_force(self, force: float) -> bool:
        """
        Set target grip force
        
        Args:
            force: Target force in Newtons (0.1 to 10.0)
            
        Returns:
            True if command sent successfully
        """
        force = max(self.MIN_FORCE, min(self.MAX_FORCE, force))
        
        try:
            # Pack float as 4 bytes
            force_bytes = struct.pack('f', force)
            
            # Send command + 4 bytes
            data = [self.CMD_SET_FORCE] + list(force_bytes)
            self.bus.write_i2c_block_data(self.ARDUINO_ADDRESS, data[0], data[1:])
            
            self.logger.debug(f"Target force set to {force:.2f}N")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set force: {e}")
            return False
    
    def get_status(self) -> Optional[GripStatus]:
        """Get current grip status"""
        with self._lock:
            return self._current_status
    
    def is_holding(self) -> bool:
        """Check if currently holding an object"""
        status = self.get_status()
        return status is not None and status.state == GripState.HOLDING
    
    def is_idle(self) -> bool:
        """Check if gripper is idle"""
        status = self.get_status()
        return status is not None and status.state == GripState.IDLE
    
    def detect_slip(self) -> bool:
        """
        Detect if object is slipping
        
        Returns:
            True if slip detected
        """
        status = self.get_status()
        if not status or status.state != GripState.HOLDING:
            return False
        
        # Add to history
        self._slip_history.append(status.actual_force)
        if len(self._slip_history) > self._slip_window:
            self._slip_history.pop(0)
        
        # Need enough samples
        if len(self._slip_history) < 5:
            return False
        
        # Detect rapid force drop
        avg_force = sum(self._slip_history[:-2]) / len(self._slip_history[:-2])
        current = self._slip_history[-1]
        
        if current < avg_force * self.SLIP_THRESHOLD:
            self.logger.warning(f"Slip detected: {current:.2f}N < {avg_force:.2f}N")
            return True
        
        return False
    
    def wait_for_hold(self, timeout: float = 10.0) -> bool:
        """
        Wait until grip reaches HOLDING state
        
        Args:
            timeout: Maximum wait time in seconds
            
        Returns:
            True if holding, False if timeout or error
        """
        start = time.time()
        while time.time() - start < timeout:
            status = self.get_status()
            if status:
                if status.state == GripState.HOLDING:
                    return True
                if status.state == GripState.ERROR:
                    return False
            time.sleep(0.1)
        return False
    
    def start_monitoring(self, interval: float = 0.1):
        """
        Start background monitoring thread
        
        Args:
            interval: Polling interval in seconds
        """
        if self._running:
            return
        
        self._running = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self._monitor_thread.start()
        self.logger.info("Monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
        self.logger.info("Monitoring stopped")
    
    def register_callback(self, callback: Callable[[GripStatus], None]):
        """Register callback for status updates"""
        self._callbacks.append(callback)
    
    def _monitor_loop(self, interval: float):
        """Background monitoring thread"""
        while self._running:
            status = self._read_status()
            if status:
                with self._lock:
                    self._current_status = status
                
                # Check for slip
                self.detect_slip()
                
                # Notify callbacks
                for callback in self._callbacks:
                    try:
                        callback(status)
                    except Exception as e:
                        self.logger.error(f"Callback error: {e}")
            
            time.sleep(interval)
    
    def _get_target_force(self) -> float:
        """Get target force based on mode"""
        if self._mode == GripMode.CUSTOM:
            return self._custom_force
        return self._mode.value
    
    def close(self):
        """Clean shutdown"""
        self.stop_monitoring()
        self.release()
        self.bus.close()
        self.logger.info("Grip controller closed")


class ObjectAwareGripController(CobraGripController):
    """
    Extended controller with object detection integration
    Automatically selects grip mode based on detected object
    """
    
    def __init__(self):
        super().__init__()
        self.object_force_map = {
            'egg': GripMode.EGG,
            'glass': GripMode.DELICATE,
            'bottle': GripMode.MEDIUM,
            'book': GripMode.MEDIUM,
            'box': GripMode.FIRM,
            'ball': GripMode.MEDIUM,
        }
    
    def grip_object(self, object_type: str) -> bool:
        """
        Grip object with mode selected by type
        
        Args:
            object_type: Type of object (egg, glass, bottle, etc.)
            
        Returns:
            True if grip initiated
        """
        mode = self.object_force_map.get(object_type.lower(), GripMode.MEDIUM)
        self.logger.info(f"Detected '{object_type}' - using {mode.name} mode")
        return self.grip(mode=mode)
    
    def set_object_mode(self, object_type: str, mode: GripMode):
        """Configure grip mode for object type"""
        self.object_force_map[object_type.lower()] = mode


# Demo and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("COBRA Grip Controller Test")
    print("=" * 60)
    
    # Initialize controller
    controller = ObjectAwareGripController()
    controller.start_monitoring(interval=0.1)
    
    # Status callback
    def on_status(status: GripStatus):
        if status.state == GripState.HOLDING:
            print(f"\rHolding: {status.actual_force:.2f}N "
                  f"(target: {status.target_force:.2f}N)", end="")
    
    controller.register_callback(on_status)
    
    try:
        # Demo sequence
        print("\n1. Testing EGG grip...")
        controller.grip(mode=GripMode.EGG)
        if controller.wait_for_hold(timeout=5.0):
            print("\n   ✓ Holding egg")
            time.sleep(2)
            controller.release()
            time.sleep(1)
        
        print("\n2. Testing FIRM grip...")
        controller.grip(mode=GripMode.FIRM)
        if controller.wait_for_hold(timeout=5.0):
            print("\n   ✓ Firm grip active")
            time.sleep(2)
            controller.release()
            time.sleep(1)
        
        print("\n3. Testing object-aware grip...")
        controller.grip_object("egg")
        if controller.wait_for_hold(timeout=5.0):
            print("\n   ✓ Auto-selected egg mode")
            time.sleep(1)
            controller.release()
        
        print("\n4. Getting final status...")
        status = controller.get_status()
        if status:
            print(f"   State: {status.state.name}")
            print(f"   Force: {status.actual_force:.2f}N")
            print(f"   Touch: {'Yes' if status.touch_detected else 'No'}")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    finally:
        controller.close()
        print("\nTest complete")
