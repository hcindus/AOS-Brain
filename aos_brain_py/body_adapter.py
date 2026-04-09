#!/usr/bin/env python3
"""
Body Adapter - AOS to BCSA V4 Hardware Bridge

Translates high-level motor commands from brain into
low-level BCSA V4 actuator instructions.

Architecture:
    Motor Control Skill (position, velocity, torque targets)
        ↓
    Body Adapter (protocol translation, safety limits, calibration)
        ↓
    BCSA V4 API (CAN bus / EtherCAT packets)
        ↓
    Physical Actuators (motion)
"""

import time
import json
import struct
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BCSACommandType(Enum):
    POSITION = 0x01
    VELOCITY = 0x02
    TORQUE = 0x03
    IMPEDANCE = 0x04
    ENABLE = 0x10
    DISABLE = 0x11
    ZERO = 0x12


@dataclass
class BCSA_V4_Packet:
    """Binary packet format for BCSA V4 actuator."""
    
    actuator_id: int      # 1 byte: Joint ID (0-255)
    command_type: int     # 1 byte: Command type
    data: bytes          # 6 bytes: Command data
    crc: int = 0         # 1 byte: CRC checksum
    
    def to_bytes(self) -> bytes:
        """Convert to BCSA V4 binary format."""
        packet = struct.pack('BB', self.actuator_id, self.command_type)
        packet += self.data.ljust(6, b'\x00')[:6]
        # Calculate CRC (simplified - real CRC would be more complex)
        self.crc = sum(packet) % 256
        packet += struct.pack('B', self.crc)
        return packet
    
    @classmethod
    def from_commands(cls, actuator_id: int, target_position: float, 
                     target_velocity: float, torque_limit: float,
                     kp: float = 100.0, kd: float = 10.0) -> 'BCSA_V4_Packet':
        """Create packet from motor commands."""
        # Scale to integer values (BCSA V4 uses fixed-point)
        pos_int = int(target_position * 1000)  # radians * 1000
        vel_int = int(target_velocity * 100)   # rad/s * 100
        torque_int = int(torque_limit * 100)  # Nm * 100
        kp_int = int(kp)
        kd_int = int(kd)
        
        # Pack into 6 bytes (simplified - real protocol more complex)
        data = struct.pack('<hh', pos_int, vel_int)  # 4 bytes
        data += struct.pack('BB', min(torque_int, 255), min(kp_int, 255))  # 2 bytes
        
        return cls(
            actuator_id=actuator_id,
            command_type=BCSACommandType.POSITION.value,
            data=data
        )


@dataclass
class JointConfig:
    """Configuration for a single joint/actuator."""
    name: str
    actuator_id: int
    joint_type: str  # 'revolute', 'prismatic', 'fixed'
    limits: Tuple[float, float]  # (min, max) in radians
    max_velocity: float  # rad/s
    max_torque: float   # Nm
    gear_ratio: float
    zero_offset: float = 0.0  # Calibration offset
    
    # BCSA V4 specific
    bcsa_model: str = "BCSA_107"  # Actuator model
    bcsa_reduction: int = 19      # Gear reduction ratio


class BodyAdapter:
    """
    Body Adapter - Translates brain commands to BCSA V4 hardware.
    
    Responsibilities:
    1. Protocol translation (brain JSON → BCSA binary)
    2. Safety limits (enforce joint limits, max torque/velocity)
    3. Calibration (zero positions, gear ratios)
    4. Real-time feedback (position, torque, temperature)
    """
    
    def __init__(self):
        self.joints: Dict[str, JointConfig] = {}
        self._init_aos_h1_joints()
        
        # Communication
        self.connected = False
        self.last_update = time.time()
        self.update_rate = 60  # Hz (typical for humanoids)
        
        # Safety
        self.emergency_stop = False
        self.temperature_limits = {
            'motor': 80.0,   # Celsius
            'driver': 70.0
        }
        
        # Statistics
        self.packets_sent = 0
        self.errors = 0
    
    def _init_aos_h1_joints(self):
        """Initialize AOS-H1 humanoid joint configuration."""
        
        # Head (2 DOF)
        self.joints['neck_pitch'] = JointConfig(
            name='neck_pitch', actuator_id=0,
            joint_type='revolute', limits=(-0.5, 0.5),
            max_velocity=2.0, max_torque=5.0, gear_ratio=19,
            bcsa_model='BCSA_107', bcsa_reduction=19
        )
        self.joints['neck_yaw'] = JointConfig(
            name='neck_yaw', actuator_id=1,
            joint_type='revolute', limits=(-1.0, 1.0),
            max_velocity=2.0, max_torque=5.0, gear_ratio=19
        )
        
        # Right Arm (4 DOF) - Higher torque for lifting
        self.joints['right_shoulder_pitch'] = JointConfig(
            name='right_shoulder_pitch', actuator_id=10,
            joint_type='revolute', limits=(-1.5, 1.5),
            max_velocity=3.0, max_torque=30.0, gear_ratio=39,
            bcsa_model='BCSA_107', bcsa_reduction=39
        )
        self.joints['right_shoulder_roll'] = JointConfig(
            name='right_shoulder_roll', actuator_id=11,
            joint_type='revolute', limits=(-0.5, 2.0),
            max_velocity=3.0, max_torque=30.0, gear_ratio=39
        )
        self.joints['right_elbow_pitch'] = JointConfig(
            name='right_elbow_pitch', actuator_id=12,
            joint_type='revolute', limits=(-2.5, 0),
            max_velocity=4.0, max_torque=23.0, gear_ratio=29,
            bcsa_model='BCSA_107', bcsa_reduction=29
        )
        self.joints['right_wrist_yaw'] = JointConfig(
            name='right_wrist_yaw', actuator_id=13,
            joint_type='revolute', limits=(-1.0, 1.0),
            max_velocity=5.0, max_torque=10.0, gear_ratio=11,
            bcsa_model='BCSA_107', bcsa_reduction=11
        )
        
        # Left Arm (4 DOF)
        self.joints['left_shoulder_pitch'] = JointConfig(
            name='left_shoulder_pitch', actuator_id=20,
            joint_type='revolute', limits=(-1.5, 1.5),
            max_velocity=3.0, max_torque=30.0, gear_ratio=39
        )
        self.joints['left_shoulder_roll'] = JointConfig(
            name='left_shoulder_roll', actuator_id=21,
            joint_type='revolute', limits=(-2.0, 0.5),
            max_velocity=3.0, max_torque=30.0, gear_ratio=39
        )
        self.joints['left_elbow_pitch'] = JointConfig(
            name='left_elbow_pitch', actuator_id=22,
            joint_type='revolute', limits=(-2.5, 0),
            max_velocity=4.0, max_torque=23.0, gear_ratio=29
        )
        self.joints['left_wrist_yaw'] = JointConfig(
            name='left_wrist_yaw', actuator_id=23,
            joint_type='revolute', limits=(-1.0, 1.0),
            max_velocity=5.0, max_torque=10.0, gear_ratio=11
        )
        
        # Torso (2 DOF)
        self.joints['waist_yaw'] = JointConfig(
            name='waist_yaw', actuator_id=30,
            joint_type='revolute', limits=(-1.0, 1.0),
            max_velocity=1.5, max_torque=40.0, gear_ratio=49,
            bcsa_model='BCSA_107', bcsa_reduction=49
        )
        self.joints['waist_pitch'] = JointConfig(
            name='waist_pitch', actuator_id=31,
            joint_type='revolute', limits=(-0.3, 0.3),
            max_velocity=1.5, max_torque=40.0, gear_ratio=49
        )
        
        # Right Leg (5 DOF) - High torque for walking
        self.joints['right_hip_pitch'] = JointConfig(
            name='right_hip_pitch', actuator_id=40,
            joint_type='revolute', limits=(-1.5, 1.5),
            max_velocity=3.0, max_torque=71.0, gear_ratio=49,
            bcsa_model='BCSA_107', bcsa_reduction=49
        )
        self.joints['right_hip_roll'] = JointConfig(
            name='right_hip_roll', actuator_id=41,
            joint_type='revolute', limits=(-0.5, 0.5),
            max_velocity=3.0, max_torque=48.0, gear_ratio=39
        )
        self.joints['right_knee_pitch'] = JointConfig(
            name='right_knee_pitch', actuator_id=42,
            joint_type='revolute', limits=(-2.5, 0),
            max_velocity=4.0, max_torque=71.0, gear_ratio=49
        )
        self.joints['right_ankle_pitch'] = JointConfig(
            name='right_ankle_pitch', actuator_id=43,
            joint_type='revolute', limits=(-0.8, 0.8),
            max_velocity=3.0, max_torque=40.0, gear_ratio=39
        )
        self.joints['right_ankle_roll'] = JointConfig(
            name='right_ankle_roll', actuator_id=44,
            joint_type='revolute', limits=(-0.5, 0.5),
            max_velocity=3.0, max_torque=30.0, gear_ratio=29
        )
        
        # Left Leg (5 DOF)
        self.joints['left_hip_pitch'] = JointConfig(
            name='left_hip_pitch', actuator_id=50,
            joint_type='revolute', limits=(-1.5, 1.5),
            max_velocity=3.0, max_torque=71.0, gear_ratio=49
        )
        self.joints['left_hip_roll'] = JointConfig(
            name='left_hip_roll', actuator_id=51,
            joint_type='revolute', limits=(-0.5, 0.5),
            max_velocity=3.0, max_torque=48.0, gear_ratio=39
        )
        self.joints['left_knee_pitch'] = JointConfig(
            name='left_knee_pitch', actuator_id=52,
            joint_type='revolute', limits=(-2.5, 0),
            max_velocity=4.0, max_torque=71.0, gear_ratio=49
        )
        self.joints['left_ankle_pitch'] = JointConfig(
            name='left_ankle_pitch', actuator_id=53,
            joint_type='revolute', limits=(-0.8, 0.8),
            max_velocity=3.0, max_torque=40.0, gear_ratio=39
        )
        self.joints['left_ankle_roll'] = JointConfig(
            name='left_ankle_roll', actuator_id=54,
            joint_type='revolute', limits=(-0.5, 0.5),
            max_velocity=3.0, max_torque=30.0, gear_ratio=29
        )
    
    def commands_to_packets(self, motor_commands: List[Dict]) -> List[BCSA_V4_Packet]:
        """
        Convert motor control commands to BCSA V4 packets.
        
        Args:
            motor_commands: List of {joint, position, velocity, torque}
        
        Returns:
            List of BCSA V4 packets ready to send
        """
        packets = []
        
        for cmd in motor_commands:
            joint_name = cmd.get('joint')
            if joint_name not in self.joints:
                self.errors += 1
                continue
            
            joint = self.joints[joint_name]
            
            # Apply safety limits
            position = self._clamp(cmd.get('position', 0), joint.limits)
            velocity = self._clamp(cmd.get('velocity', 0), 
                                  (-joint.max_velocity, joint.max_velocity))
            torque = self._clamp(cmd.get('torque', 0),
                               (-joint.max_torque, joint.max_torque))
            
            # Apply gear ratio (motor side vs output side)
            motor_position = position * joint.gear_ratio
            motor_velocity = velocity * joint.gear_ratio
            motor_torque = torque / joint.gear_ratio
            
            # Create packet
            packet = BCSA_V4_Packet.from_commands(
                actuator_id=joint.actuator_id,
                target_position=motor_position,
                target_velocity=motor_velocity,
                torque_limit=abs(motor_torque),
                kp=100.0,  # Position gain
                kd=10.0    # Velocity gain
            )
            
            packets.append(packet)
        
        return packets
    
    def _clamp(self, value: float, limits: Tuple[float, float]) -> float:
        """Clamp value to limits."""
        return max(limits[0], min(limits[1], value))
    
    def emergency_stop_all(self) -> List[BCSA_V4_Packet]:
        """Generate emergency stop packets for all joints."""
        packets = []
        for joint in self.joints.values():
            packet = BCSA_V4_Packet(
                actuator_id=joint.actuator_id,
                command_type=BCSACommandType.DISABLE.value,
                data=b'\x00\x00\x00\x00\x00\x00'
            )
            packets.append(packet)
        
        self.emergency_stop = True
        return packets
    
    def zero_all_joints(self) -> List[BCSA_V4_Packet]:
        """Zero all joints (calibration)."""
        packets = []
        for joint in self.joints.values():
            packet = BCSA_V4_Packet(
                actuator_id=joint.actuator_id,
                command_type=BCSACommandType.ZERO.value,
                data=b'\x00\x00\x00\x00\x00\x00'
            )
            packets.append(packet)
        
        return packets
    
    def get_joint_status(self, joint_name: str) -> Optional[Dict]:
        """Get joint configuration and limits."""
        if joint_name not in self.joints:
            return None
        
        joint = self.joints[joint_name]
        return {
            'name': joint.name,
            'actuator_id': joint.actuator_id,
            'limits': joint.limits,
            'max_velocity': joint.max_velocity,
            'max_torque': joint.max_torque,
            'gear_ratio': joint.gear_ratio,
            'bcsa_model': joint.bcsa_model
        }
    
    def get_actuator_map(self) -> Dict[int, str]:
        """Get mapping of actuator IDs to joint names."""
        return {joint.actuator_id: name for name, joint in self.joints.items()}
    
    def get_stats(self) -> Dict:
        """Get adapter statistics."""
        return {
            'joints_configured': len(self.joints),
            'packets_sent': self.packets_sent,
            'errors': self.errors,
            'emergency_stop': self.emergency_stop,
            'update_rate': self.update_rate
        }


# Demo
if __name__ == '__main__':
    print("🦾 Body Adapter - AOS to BCSA V4 Bridge")
    print("=" * 60)
    
    adapter = BodyAdapter()
    
    print(f"\nConfigured Joints: {len(adapter.joints)}")
    print("\nHigh-Torque Joints (Legs/Arms):")
    for name, joint in adapter.joints.items():
        if joint.max_torque >= 30:
            print(f"  {name}: {joint.max_torque}Nm max, {joint.gear_ratio}:1 gear")
    
    # Demo command translation
    print("\n" + "=" * 60)
    print("Command Translation Demo")
    print("=" * 60)
    
    motor_commands = [
        {'joint': 'right_shoulder_pitch', 'position': 0.5, 'velocity': 1.0, 'torque': 10.0},
        {'joint': 'right_elbow_pitch', 'position': -1.0, 'velocity': 2.0, 'torque': 5.0},
        {'joint': 'right_hip_pitch', 'position': 0.3, 'velocity': 1.5, 'torque': 40.0},
    ]
    
    print(f"\nInput Commands:")
    for cmd in motor_commands:
        print(f"  {cmd['joint']}: pos={cmd['position']:.2f}rad, vel={cmd['velocity']:.1f}rad/s, torque={cmd['torque']:.1f}Nm")
    
    packets = adapter.commands_to_packets(motor_commands)
    
    print(f"\nOutput BCSA V4 Packets: {len(packets)}")
    for i, packet in enumerate(packets):
        print(f"  Packet {i+1}: ID={packet.actuator_id}, Type={packet.command_type}, "
              f"Data={packet.data.hex()}, CRC={packet.crc}")
    
    print(f"\nAdapter Stats: {adapter.get_stats()}")
    print("\n✅ Body Adapter ready for BCSA V4 integration!")
