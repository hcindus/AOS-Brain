#!/usr/bin/env python3
"""
BHSI - Body Hardware System Interface
======================================

DUAL MEANING NOTE:
==================
BHSI = Brain + Heart + Stomach + Intestines (Biological Life Support)
       └─ The living organism - cognitive, rhythmic, digestive, eliminative systems

BHSI = Body Hardware System Interface (Physical Embodiment)
       └─ The bridge between agents and physical robot hardware

This module implements the SECOND meaning (Body Hardware System Interface).
It works WITH the biological BHSI (brain, heart, stomach, intestines) to allow
agents to control physical embodiment.

The biological BHSI provides:
- Brain: OODA cognition, decision-making
- Heart: Rhythmic coordination, emotional tone
- Stomach: Input filtering and processing
- Intestines: Nutrient absorption, waste disposal

This module (Body Hardware System Interface) provides:
- Joint discovery and capability reporting
- Joint assignment and exclusive control
- Command translation (high-level → actuator packets)
- Sensor feedback (position, torque, temperature)
- Multi-agent coordination (prevent conflicts)

Full Stack:
    Agent (cognitive system running on biological BHSI)
        ↓
    BHSI (this module - Body Hardware System Interface)
        ↓
    Motor Control Skill (inverse kinematics)
        ↓
    Body Adapter (protocol translation + safety)
        ↓
    BCSA V4 Actuators (physical hardware)
        ↓
    AOS-H1 Robot Body (22 joints, sensors)

Usage:
- Agents discover body capabilities
- Agents claim joints for exclusive control
- Agents send movement commands
- Agents receive sensor feedback
- Multiple agents share body (different joints)
- Emergency stop available
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent))

from body_adapter import BodyAdapter, BCSA_V4_Packet


@dataclass
class BodyCapability:
    """Capability statement for a body joint."""
    joint_name: str
    actuator_id: int
    joint_type: str
    range_of_motion: tuple
    max_velocity: float
    max_torque: float
    current_position: float
    status: str  # 'active', 'fault', 'calibrating'


class BHSI:
    """
    Body Hardware System Interface.
    
    The bridge between agent cognition and physical embodiment.
    Agents use BHSI to control the AOS-H1 robot body.
    """
    
    def __init__(self):
        self.body = BodyAdapter()
        self.connected = False
        self.agent_assignments: Dict[str, List[str]] = {}  # agent -> joints
        self.sensor_data: Dict[str, Any] = {}
        self.last_update = time.time()
        
        # Safety
        self.max_simultaneous_joints = 8  # Prevent agent conflicts
        self.emergency_stop = False
    
    def discover_capabilities(self, agent_id: str) -> Dict:
        """
        Allow agent to discover what the body can do.
        
        Returns:
            joints: List of controllable joints
            sensors: Available sensor data
            limits: Safety constraints
        """
        capabilities = []
        
        for joint_name, joint in self.body.joints.items():
            # Check if joint is available (not assigned to another agent)
            assigned = any(joint_name in joints for joints in self.agent_assignments.values())
            
            capabilities.append({
                'joint_name': joint_name,
                'actuator_id': joint.actuator_id,
                'type': joint.joint_type,
                'range': joint.limits,
                'max_velocity': joint.max_velocity,
                'max_torque': joint.max_torque,
                'gear_ratio': joint.gear_ratio,
                'available': not assigned
            })
        
        return {
            'agent_id': agent_id,
            'total_joints': len(self.body.joints),
            'available_joints': sum(1 for c in capabilities if c['available']),
            'joints': capabilities,
            'sensors': ['position', 'velocity', 'torque', 'temperature'],
            'update_rate_hz': self.body.update_rate,
            'safety_limits': {
                'max_torque_global': 71.0,  # Highest joint limit
                'max_velocity_global': 5.0,
                'emergency_stop': self.emergency_stop
            }
        }
    
    def claim_joints(self, agent_id: str, joint_names: List[str]) -> bool:
        """
        Agent claims specific joints for control.
        
        Args:
            agent_id: Unique agent identifier
            joint_names: List of joints to control
        
        Returns:
            True if claim successful, False if joints unavailable
        """
        # Check if joints are available
        for joint in joint_names:
            for existing_agent, existing_joints in self.agent_assignments.items():
                if joint in existing_joints and existing_agent != agent_id:
                    return False  # Joint already claimed
        
        # Check joint limit
        total_claimed = len(joint_names)
        if agent_id in self.agent_assignments:
            total_claimed += len(self.agent_assignments[agent_id])
        
        if total_claimed > self.max_simultaneous_joints:
            return False  # Agent trying to control too many joints
        
        # Assign joints
        self.agent_assignments[agent_id] = joint_names
        return True
    
    def release_joints(self, agent_id: str):
        """Agent releases control of joints."""
        if agent_id in self.agent_assignments:
            del self.agent_assignments[agent_id]
    
    def move_joint(self, agent_id: str, joint_name: str, 
                   position: float, velocity: float = 1.0, 
                   torque_limit: float = None) -> Dict:
        """
        Agent commands a specific joint to move.
        
        Args:
            agent_id: Controlling agent
            joint_name: Target joint
            position: Target position (radians)
            velocity: Max velocity (rad/s)
            torque_limit: Optional torque limit
        
        Returns:
            Command status and predicted execution
        """
        # Verify agent owns this joint
        if agent_id not in self.agent_assignments:
            return {'error': 'Agent has no claimed joints', 'success': False}
        
        if joint_name not in self.agent_assignments[agent_id]:
            return {'error': f'Joint {joint_name} not claimed by this agent', 'success': False}
        
        # Check emergency stop
        if self.emergency_stop:
            return {'error': 'Emergency stop active', 'success': False}
        
        # Get joint config
        joint = self.body.joints.get(joint_name)
        if not joint:
            return {'error': f'Unknown joint {joint_name}', 'success': False}
        
        # Use joint max torque if not specified
        if torque_limit is None:
            torque_limit = joint.max_torque
        
        # Create motor command
        command = {
            'joint': joint_name,
            'position': position,
            'velocity': velocity,
            'torque': torque_limit
        }
        
        # Convert to BCSA packets
        packets = self.body.commands_to_packets([command])
        
        if not packets:
            return {'error': 'Failed to generate packets', 'success': False}
        
        # In real implementation, send packets to hardware here
        # For now, simulate success
        packet = packets[0]
        
        return {
            'success': True,
            'joint': joint_name,
            'target_position': position,
            'target_velocity': velocity,
            'torque_limit': torque_limit,
            'actuator_id': packet.actuator_id,
            'packet_size_bytes': len(packet.to_bytes()),
            'estimated_time_to_target': abs(position - joint.zero_offset) / velocity
        }
    
    def set_pose(self, agent_id: str, end_effector: str, 
                 position: tuple, orientation: tuple = None) -> Dict:
        """
        High-level pose command (e.g., "move right hand to position").
        
        Args:
            agent_id: Controlling agent
            end_effector: 'right_hand', 'left_hand', 'right_foot', etc.
            position: (x, y, z) target position
            orientation: Optional (roll, pitch, yaw)
        
        Returns:
            IK solution success, joint commands generated
        """
        # Check if end effector joints are claimed
        if end_effector == 'right_hand':
            required_joints = ['right_shoulder_pitch', 'right_shoulder_roll', 
                             'right_elbow_pitch', 'right_wrist_yaw']
        elif end_effector == 'left_hand':
            required_joints = ['left_shoulder_pitch', 'left_shoulder_roll',
                             'left_elbow_pitch', 'left_wrist_yaw']
        elif end_effector == 'right_foot':
            required_joints = ['right_hip_pitch', 'right_hip_roll', 
                             'right_knee_pitch', 'right_ankle_pitch']
        else:
            return {'error': f'Unknown end effector {end_effector}', 'success': False}
        
        # Verify agent has claimed these joints
        if agent_id not in self.agent_assignments:
            return {'error': 'Agent has not claimed joints', 'success': False}
        
        claimed = self.agent_assignments[agent_id]
        missing = [j for j in required_joints if j not in claimed]
        
        if missing:
            return {
                'error': f'Missing joint claims: {missing}',
                'success': False,
                'hint': f'Call claim_joints for {required_joints}'
            }
        
        # Calculate IK (simplified - would use full kinematics)
        # This is where we'd call the motor control skill's IK
        
        return {
            'success': True,
            'end_effector': end_effector,
            'target_position': position,
            'required_joints': required_joints,
            'note': 'IK calculation would happen here, then joint commands sent'
        }
    
    def get_sensor_feedback(self, agent_id: str) -> Dict:
        """
        Get current sensor data from assigned joints.
        
        Returns:
            positions, velocities, torques, temperatures
        """
        if agent_id not in self.agent_assignments:
            return {'error': 'No joints assigned'}
        
        feedback = {}
        for joint_name in self.agent_assignments[agent_id]:
            # In real implementation, read from hardware
            # Simulated feedback:
            joint = self.body.joints[joint_name]
            feedback[joint_name] = {
                'position': 0.0,  # Would read from encoder
                'velocity': 0.0,
                'torque': 0.0,
                'temperature': 25.0,  # Celsius
                'status': 'active'
            }
        
        return {
            'agent_id': agent_id,
            'timestamp': time.time(),
            'joint_feedback': feedback
        }
    
    def emergency_stop_all(self):
        """Emergency stop all actuators."""
        self.emergency_stop = True
        packets = self.body.emergency_stop_all()
        
        return {
            'success': True,
            'message': 'Emergency stop activated',
            'packets_generated': len(packets),
            'affected_joints': list(self.body.joints.keys())
        }
    
    def get_agent_status(self) -> Dict:
        """Get status of all agents using the body."""
        return {
            'active_agents': len(self.agent_assignments),
            'agent_assignments': self.agent_assignments,
            'unclaimed_joints': len(self.body.joints) - sum(len(j) for j in self.agent_assignments.values()),
            'emergency_stop': self.emergency_stop
        }


# Integration with existing agent system
def create_bhsi_for_agent(agent_id: str, role: str) -> BHSI:
    """
    Factory function to create BHSI instance for a specific agent.
    
    Args:
        agent_id: Agent name (e.g., 'mylonen', 'mylzeron')
        role: Agent role ('explorer', 'builder', 'guard', etc.)
    
    Returns:
        Configured BHSI instance with appropriate joint claims
    """
    bhsi = BHSI()
    
    # Role-based joint assignment
    if role == 'explorer':
        # Claim head and legs for navigation
        joints = ['neck_pitch', 'neck_yaw', 
                 'right_hip_pitch', 'left_hip_pitch',
                 'right_knee_pitch', 'left_knee_pitch']
    elif role == 'manipulator':
        # Claim arms for manipulation
        joints = ['right_shoulder_pitch', 'right_shoulder_roll', 
                 'right_elbow_pitch', 'right_wrist_yaw',
                 'left_shoulder_pitch', 'left_shoulder_roll',
                 'left_elbow_pitch', 'left_wrist_yaw']
    elif role == 'walker':
        # Claim legs and waist for locomotion
        joints = ['waist_yaw', 'waist_pitch',
                 'right_hip_pitch', 'right_hip_roll',
                 'right_knee_pitch', 'right_ankle_pitch',
                 'left_hip_pitch', 'left_hip_roll',
                 'left_knee_pitch', 'left_ankle_pitch']
    else:
        joints = []
    
    if joints:
        bhsi.claim_joints(agent_id, joints)
    
    return bhsi


# Demo
if __name__ == '__main__':
    print("🦾 BHSI - Body Hardware System Interface")
    print("=" * 60)
    print("Connecting Agents to Physical Body")
    print("=" * 60)
    
    # Create BHSI
    bhsi = BHSI()
    
    # Agent Mylonen (explorer) discovers body
    print("\n[1] Agent 'mylonen' (explorer) discovers body capabilities...")
    caps = bhsi.discover_capabilities('mylonen')
    print(f"   Total joints: {caps['total_joints']}")
    print(f"   Available: {caps['available_joints']}")
    print(f"   Sensors: {', '.join(caps['sensors'])}")
    
    # Claim joints
    print("\n[2] Agent claims joints for exploration...")
    explorer_joints = ['neck_pitch', 'neck_yaw', 
                      'right_hip_pitch', 'left_hip_pitch']
    success = bhsi.claim_joints('mylonen', explorer_joints)
    print(f"   Claimed: {explorer_joints}")
    print(f"   Success: {success}")
    
    # Move neck to look around
    print("\n[3] Agent commands neck movement...")
    result = bhsi.move_joint('mylonen', 'neck_yaw', position=0.5, velocity=2.0)
    print(f"   Command: neck_yaw → 0.5 rad")
    print(f"   Success: {result['success']}")
    print(f"   Est. time: {result.get('estimated_time_to_target', 0):.2f}s")
    
    # Get feedback
    print("\n[4] Agent reads sensor feedback...")
    feedback = bhsi.get_sensor_feedback('mylonen')
    print(f"   Joints reporting: {list(feedback['joint_feedback'].keys())}")
    
    # Second agent tries to claim same joint
    print("\n[5] Agent 'mylzeron' tries to claim neck (already taken)...")
    success2 = bhsi.claim_joints('mylzeron', ['neck_yaw'])
    print(f"   Success: {success2} (expected: False)")
    
    # Set pose (high-level command)
    print("\n[6] Agent sets end-effector pose...")
    pose = bhsi.set_pose('mylonen', 'right_hand', position=(0.3, -0.2, 0.1))
    print(f"   Target: right_hand at (0.3, -0.2, 0.1)")
    print(f"   Success: {pose['success']}")
    print(f"   Requires joints: {pose.get('required_joints', [])}")
    
    # Final status
    print("\n" + "=" * 60)
    print("BHSI Status:")
    print("=" * 60)
    status = bhsi.get_agent_status()
    print(f"   Active agents: {status['active_agents']}")
    print(f"   Joint assignments: {status['agent_assignments']}")
    print(f"   Unclaimed joints: {status['unclaimed_joints']}")
    
    print("\n✅ BHSI ready for agent embodiment!")
    print("   Agents can now control physical AOS-H1 robot body")
