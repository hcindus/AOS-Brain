#!/usr/bin/env python3
"""
Humanoid Robot - Body Map and Kinematic Model
Version: 1.0.0

This module provides the internal body representation that allows
the AOS Brain to understand its own physical structure.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable
from enum import Enum
import json

__version__ = "1.0.0"


class JointType(Enum):
    REVOLUTE = "revolute"  # Rotation around axis
    PRISMATIC = "prismatic"  # Linear translation
    SPHERICAL = "spherical"  # Ball joint (3 DOF)
    FIXED = "fixed"


@dataclass
class Joint:
    """Represents a single joint in the kinematic chain"""
    name: str
    joint_type: JointType
    parent_link: str
    child_link: str
    axis: np.ndarray = field(default_factory=lambda: np.array([0, 0, 1]))
    limits: Tuple[float, float] = (-180.0, 180.0)  # degrees
    max_velocity: float = 180.0  # degrees/s
    max_torque: float = 10.0  # Nm
    home_position: float = 0.0
    current_position: float = 0.0
    compliance: float = 0.0  # 0=rigid, 1=fully compliant
    
    def is_at_limit(self) -> bool:
        """Check if joint is at mechanical limit"""
        return self.current_position <= self.limits[0] or \
               self.current_position >= self.limits[1]
    
    def get_center(self) -> float:
        """Get center of motion range"""
        return (self.limits[0] + self.limits[1]) / 2


@dataclass
class Link:
    """Represents a rigid body link"""
    name: str
    parent_joint: str
    length: float  # meters
    mass: float  # kg
    center_of_mass: np.ndarray = field(default_factory=lambda: np.array([0, 0, 0]))
    inertia_tensor: np.ndarray = field(default_factory=lambda: np.eye(3))
    visual_mesh: Optional[str] = None
    collision_mesh: Optional[str] = None


@dataclass
class BodyCapability:
    """Describes what a body part can do"""
    joint_name: str
    max_force: float  # Maximum safe force output
    preferred_range: Tuple[float, float]  # Comfortable operating range
    fatigue_factor: float  # Accumulated stress indicator
    health_status: float = 1.0  # 1.0 = perfect, 0.0 = failed
    temperature: float = 25.0  # Celsius


class HumanoidBodyMap:
    """
    Complete body schema for the humanoid robot.
    
    Provides:
    - Forward/inverse kinematics
    - Self-model for motor planning
    - Proprioceptive integration
    - Capability mapping
    """
    
    def __init__(self):
        self.joints: Dict[str, Joint] = {}
        self.links: Dict[str, Link] = {}
        self.capabilities: Dict[str, BodyCapability] = {}
        self.joint_order: List[str] = []  # Ordered chain from base to tip
        
        self._build_standard_humanoid()
        self._compute_capabilities()
    
    def _build_standard_humanoid(self):
        """Build standard 47-DOF humanoid structure"""
        
        # === PELVIS (Base) ===
        self._add_joint("pelvis_yaw", JointType.REVOLUTE, "world", "pelvis",
                       axis=[0, 0, 1], limits=[-90, 90])
        
        # === SPINE ===
        self._add_joint("spine_yaw", JointType.REVOLUTE, "pelvis", "torso_lower",
                       axis=[0, 0, 1], limits=[-30, 30])
        self._add_joint("spine_pitch", JointType.REVOLUTE, "torso_lower", "torso_upper",
                       axis=[0, 1, 0], limits=[-30, 30])
        self._add_joint("spine_roll", JointType.REVOLUTE, "torso_upper", "torso_top",
                       axis=[1, 0, 0], limits=[-20, 20])
        
        # === NECK ===
        self._add_joint("neck_yaw", JointType.REVOLUTE, "torso_top", "neck_base",
                       axis=[0, 0, 1], limits=[-90, 90])
        self._add_joint("neck_pitch", JointType.REVOLUTE, "neck_base", "neck_mid",
                       axis=[0, 1, 0], limits=[-45, 45])
        self._add_joint("neck_roll", JointType.REVOLUTE, "neck_mid", "head",
                       axis=[1, 0, 0], limits=[-30, 30])
        
        # === RIGHT ARM ===
        self._add_joint("r_shoulder_pitch", JointType.REVOLUTE, "torso_top", "r_upper_arm",
                       axis=[0, 1, 0], limits=[-180, 90])
        self._add_joint("r_shoulder_roll", JointType.REVOLUTE, "r_upper_arm", "r_shoulder",
                       axis=[1, 0, 0], limits=[0, 180])
        self._add_joint("r_shoulder_yaw", JointType.REVOLUTE, "r_shoulder", "r_shoulder_rot",
                       axis=[0, 0, 1], limits=[-90, 90])
        self._add_joint("r_elbow_flex", JointType.REVOLUTE, "r_shoulder_rot", "r_forearm",
                       axis=[0, 1, 0], limits=[0, 150])
        self._add_joint("r_forearm_roll", JointType.REVOLUTE, "r_forearm", "r_wrist_base",
                       axis=[1, 0, 0], limits=[-90, 90])
        self._add_joint("r_wrist_pitch", JointType.REVOLUTE, "r_wrist_base", "r_wrist",
                       axis=[0, 1, 0], limits=[-45, 45])
        self._add_joint("r_wrist_yaw", JointType.REVOLUTE, "r_wrist", "r_hand_base",
                       axis=[0, 0, 1], limits=[-90, 90])
        
        # === RIGHT HAND ===
        self._build_hand("r")
        
        # === LEFT ARM (mirrored) ===
        self._add_joint("l_shoulder_pitch", JointType.REVOLUTE, "torso_top", "l_upper_arm",
                       axis=[0, 1, 0], limits=[-180, 90])
        self._add_joint("l_shoulder_roll", JointType.REVOLUTE, "l_upper_arm", "l_shoulder",
                       axis=[1, 0, 0], limits=[-180, 0])  # Mirror
        self._add_joint("l_shoulder_yaw", JointType.REVOLUTE, "l_shoulder", "l_shoulder_rot",
                       axis=[0, 0, 1], limits=[-90, 90])
        self._add_joint("l_elbow_flex", JointType.REVOLUTE, "l_shoulder_rot", "l_forearm",
                       axis=[0, 1, 0], limits=[0, 150])
        self._add_joint("l_forearm_roll", JointType.REVOLUTE, "l_forearm", "l_wrist_base",
                       axis=[1, 0, 0], limits=[-90, 90])
        self._add_joint("l_wrist_pitch", JointType.REVOLUTE, "l_wrist_base", "l_wrist",
                       axis=[0, 1, 0], limits=[-45, 45])
        self._add_joint("l_wrist_yaw", JointType.REVOLUTE, "l_wrist", "l_hand_base",
                       axis=[0, 0, 1], limits=[-90, 90])
        
        # === LEFT HAND ===
        self._build_hand("l")
        
        # === RIGHT LEG ===
        self._add_joint("r_hip_yaw", JointType.REVOLUTE, "pelvis", "r_hip",
                       axis=[0, 0, 1], limits=[-45, 45])
        self._add_joint("r_hip_roll", JointType.REVOLUTE, "r_hip", "r_hip_abduct",
                       axis=[1, 0, 0], limits=[-45, 45])
        self._add_joint("r_hip_pitch", JointType.REVOLUTE, "r_hip_abduct", "r_thigh",
                       axis=[0, 1, 0], limits=[-90, 90])
        self._add_joint("r_knee_flex", JointType.REVOLUTE, "r_thigh", "r_shin",
                       axis=[0, 1, 0], limits=[0, 150])
        self._add_joint("r_ankle_pitch", JointType.REVOLUTE, "r_shin", "r_ankle",
                       axis=[0, 1, 0], limits=[-30, 45])
        self._add_joint("r_ankle_roll", JointType.REVOLUTE, "r_ankle", "r_foot",
                       axis=[1, 0, 0], limits=[-20, 20])
        
        # === LEFT LEG (mirrored) ===
        self._add_joint("l_hip_yaw", JointType.REVOLUTE, "pelvis", "l_hip",
                       axis=[0, 0, 1], limits=[-45, 45])
        self._add_joint("l_hip_roll", JointType.REVOLUTE, "l_hip", "l_hip_abduct",
                       axis=[1, 0, 0], limits=[-45, 45])
        self._add_joint("l_hip_pitch", JointType.REVOLUTE, "l_hip_abduct", "l_thigh",
                       axis=[0, 1, 0], limits=[-90, 90])
        self._add_joint("l_knee_flex", JointType.REVOLUTE, "l_thigh", "l_shin",
                       axis=[0, 1, 0], limits=[0, 150])
        self._add_joint("l_ankle_pitch", JointType.REVOLUTE, "l_shin", "l_ankle",
                       axis=[0, 1, 0], limits=[-30, 45])
        self._add_joint("l_ankle_roll", JointType.REVOLUTE, "l_ankle", "l_foot",
                       axis=[1, 0, 0], limits=[-20, 20])
        
        # Build link structure
        self._build_links()
    
    def _build_hand(self, side: str):
        """Build 15-DOF hand structure"""
        prefix = f"{side}_"
        base = f"{prefix}hand_base"
        
        # Thumb
        self._add_joint(f"{prefix}thumb_cmc_yaw", JointType.REVOLUTE, base, f"{prefix}thumb_proximal",
                       axis=[0, 0, 1], limits=[-30, 60])
        self._add_joint(f"{prefix}thumb_cmc_pitch", JointType.REVOLUTE, f"{prefix}thumb_proximal", 
                       f"{prefix}thumb_mid",
                       axis=[0, 1, 0], limits=[0, 90])
        self._add_joint(f"{prefix}thumb_mcp", JointType.REVOLUTE, f"{prefix}thumb_mid",
                       f"{prefix}thumb_distal",
                       axis=[0, 1, 0], limits=[0, 90])
        
        # Fingers (index, middle, ring, little)
        for finger in ["index", "middle", "ring", "little"]:
            self._add_joint(f"{prefix}{finger}_mcp_yaw", JointType.REVOLUTE, base,
                           f"{prefix}{finger}_proximal",
                           axis=[0, 0, 1], limits=[-15, 15])
            self._add_joint(f"{prefix}{finger}_mcp_pitch", JointType.REVOLUTE,
                           f"{prefix}{finger}_proximal", f"{prefix}{finger}_mid",
                           axis=[0, 1, 0], limits=[0, 90])
            self._add_joint(f"{prefix}{finger}_pip", JointType.REVOLUTE,
                           f"{prefix}{finger}_mid", f"{prefix}{finger}_distal",
                           axis=[0, 1, 0], limits=[0, 110])
    
    def _add_joint(self, name: str, jtype: JointType, parent: str, child: str,
                   axis: List[float], limits: Tuple[float, float]):
        """Add a joint to the body map"""
        self.joints[name] = Joint(
            name=name,
            joint_type=jtype,
            parent_link=parent,
            child_link=child,
            axis=np.array(axis),
            limits=limits
        )
        self.joint_order.append(name)
    
    def _build_links(self):
        """Build link inertial properties"""
        # Simplified masses and lengths
        link_specs = {
            "pelvis": (0.15, 15.0),  # length, mass
            "torso_lower": (0.20, 8.0),
            "torso_upper": (0.25, 10.0),
            "torso_top": (0.10, 5.0),
            "head": (0.20, 4.0),
            "r_upper_arm": (0.30, 2.5),
            "r_forearm": (0.25, 2.0),
            "r_hand": (0.10, 0.8),
            "r_thigh": (0.40, 8.0),
            "r_shin": (0.40, 5.0),
            "r_foot": (0.25, 1.5),
        }
        
        for name, (length, mass) in link_specs.items():
            parent_joint = None
            for j in self.joints.values():
                if j.child_link == name:
                    parent_joint = j.name
                    break
            
            self.links[name] = Link(
                name=name,
                parent_joint=parent_joint or "fixed",
                length=length,
                mass=mass,
                center_of_mass=np.array([length/2, 0, 0])
            )
    
    def _compute_capabilities(self):
        """Compute capability map for each joint"""
        for name, joint in self.joints.items():
            # Set capability based on joint location
            if "hip" in name or "knee" in name:
                max_force = 200.0  # High torque
                preferred = (-30, 30)
            elif "shoulder" in name or "elbow" in name:
                max_force = 50.0
                preferred = (-45, 45)
            elif "hand" in name or "finger" in name or "thumb" in name:
                max_force = 5.0
                preferred = (0, 60)
            else:
                max_force = 20.0
                preferred = joint.limits
            
            self.capabilities[name] = BodyCapability(
                joint_name=name,
                max_force=max_force,
                preferred_range=preferred,
                fatigue_factor=0.0,
                health_status=1.0,
                temperature=25.0
            )
    
    def get_joint(self, name: str) -> Optional[Joint]:
        """Get joint by name"""
        return self.joints.get(name)
    
    def get_chain(self, from_joint: str, to_joint: str) -> List[str]:
        """Get kinematic chain between two joints"""
        # Find common ancestor
        from_chain = [from_joint]
        to_chain = [to_joint]
        
        # Build parent chains
        current = from_joint
        while current in self.joints:
            parent = self.joints[current].parent_link
            if parent == "world":
                break
            for j in self.joints.values():
                if j.child_link == parent:
                    from_chain.append(j.name)
                    current = j.name
                    break
            else:
                break
        
        current = to_joint
        while current in self.joints:
            parent = self.joints[current].parent_link
            if parent == "world":
                break
            for j in self.joints.values():
                if j.child_link == parent:
                    to_chain.append(j.name)
                    current = j.name
                    break
            else:
                break
        
        # Find intersection
        for i, j1 in enumerate(from_chain):
            for j2 in to_chain:
                if j1 == j2:
                    return from_chain[:i+1] + to_chain[:to_chain.index(j2)][::-1]
        
        return []
    
    def get_reach(self, hand: str = "r_hand") -> float:
        """Calculate maximum reach for given hand"""
        if hand == "r_hand":
            chain = self.get_chain("pelvis_yaw", "r_wrist_yaw")
        else:
            chain = self.get_chain("pelvis_yaw", "l_wrist_yaw")
        
        total_reach = 0.0
        for joint_name in chain:
            if joint_name in self.joints:
                child = self.joints[joint_name].child_link
                if child in self.links:
                    total_reach += self.links[child].length
        
        return total_reach
    
    def is_pose_valid(self, joint_positions: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Check if a pose is within joint limits and capabilities"""
        violations = []
        
        for name, angle in joint_positions.items():
            if name not in self.joints:
                violations.append(f"Unknown joint: {name}")
                continue
            
            joint = self.joints[name]
            cap = self.capabilities[name]
            
            # Check limits
            if angle < joint.limits[0] or angle > joint.limits[1]:
                violations.append(f"{name}: angle {angle} outside limits {joint.limits}")
            
            # Check capability
            if angle < cap.preferred_range[0] or angle > cap.preferred_range[1]:
                violations.append(f"{name}: angle {angle} outside preferred range {cap.preferred_range}")
            
            # Check health
            if cap.health_status < 0.5:
                violations.append(f"{name}: joint degraded (health={cap.health_status:.2f})")
        
        return len(violations) == 0, violations
    
    def get_comfort_score(self, joint_positions: Dict[str, float]) -> float:
        """Calculate how comfortable/natural a pose is (0-1)"""
        total_score = 0.0
        count = 0
        
        for name, angle in joint_positions.items():
            if name not in self.joints or name not in self.capabilities:
                continue
            
            cap = self.capabilities[name]
            center = (cap.preferred_range[0] + cap.preferred_range[1]) / 2
            range_size = cap.preferred_range[1] - cap.preferred_range[0]
            
            # Gaussian-like score centered on preferred range
            deviation = abs(angle - center)
            score = max(0, 1 - (deviation / (range_size / 2))**2)
            
            total_score += score
            count += 1
        
        return total_score / count if count > 0 else 0.0
    
    def update_from_proprioception(self, sensor_data: Dict[str, float]):
        """Update body map from actual sensor readings"""
        for name, position in sensor_data.items():
            if name in self.joints:
                self.joints[name].current_position = position
    
    def export_urdf(self, filename: str = "humanoid.urdf"):
        """Export to URDF format for ROS/Gazebo"""
        # Simplified URDF export
        urdf = ['<?xml version="1.0"?>',
                '<robot name="prometheus_humanoid">',
                '  <material name="body">',
                '    <color rgba="0.8 0.8 0.8 1"/>',
                '  </material>']
        
        for link in self.links.values():
            urdf.append(f'  <link name="{link.name}">')
            urdf.append(f'    <visual>')
            urdf.append(f'      <geometry><box size="{link.length} 0.1 0.1"/></geometry>')
            urdf.append(f'      <material name="body"/>')
            urdf.append(f'    </visual>')
            urdf.append(f'  </link>')
        
        for joint in self.joints.values():
            if joint.joint_type == JointType.FIXED:
                continue
            urdf.append(f'  <joint name="{joint.name}" type="revolute">')
            urdf.append(f'    <parent link="{joint.parent_link}"/>')
            urdf.append(f'    <child link="{joint.child_link}"/>')
            urdf.append(f'    <axis xyz="{" ".join(map(str, joint.axis))}"/>')
            urdf.append(f'    <limit lower="{np.radians(joint.limits[0])}" upper="{np.radians(joint.limits[1])}"/>')
            urdf.append(f'  </joint>')
        
        urdf.append('</robot>')
        
        with open(filename, 'w') as f:
            f.write('\n'.join(urdf))
    
    def print_summary(self):
        """Print body map summary"""
        print("=" * 60)
        print("HUMANOID BODY MAP SUMMARY")
        print("=" * 60)
        print(f"Total Joints: {len(self.joints)}")
        print(f"Total Links: {len(self.links)}")
        print(f"Total Mass: {sum(l.mass for l in self.links.values()):.1f} kg")
        print(f"Right Hand Reach: {self.get_reach('r_hand'):.2f} m")
        print(f"Left Hand Reach: {self.get_reach('l_hand'):.2f} m")
        
        # Group by region
        regions = {
            "Head": ["neck"],
            "Torso": ["spine", "pelvis"],
            "Right Arm": ["r_shoulder", "r_elbow", "r_wrist"],
            "Left Arm": ["l_shoulder", "l_elbow", "l_wrist"],
            "Right Leg": ["r_hip", "r_knee", "r_ankle"],
            "Left Leg": ["l_hip", "l_knee", "l_ankle"],
        }
        
        print("\nJoint Distribution:")
        for region, keywords in regions.items():
            count = sum(1 for j in self.joints if any(k in j for k in keywords))
            print(f"  {region}: {count} DOF")
        
        print(f"\nHands: 30 DOF (15 per hand)")
        print("=" * 60)


# Demo
if __name__ == "__main__":
    body = HumanoidBodyMap()
    body.print_summary()
    
    # Test pose validation
    test_pose = {
        "r_shoulder_pitch": 90,
        "r_shoulder_roll": 45,
        "r_elbow_flex": 90,
    }
    
    valid, violations = body.is_pose_valid(test_pose)
    print(f"\nTest pose valid: {valid}")
    if violations:
        print("Violations:", violations)
    
    comfort = body.get_comfort_score(test_pose)
    print(f"Comfort score: {comfort:.2f}")
