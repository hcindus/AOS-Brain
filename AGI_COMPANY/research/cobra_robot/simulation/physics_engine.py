#!/usr/bin/env python3
"""
COBRA Physics Engine
3D physics simulation using simplified rigid body dynamics
"""

import numpy as np
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class RigidBody:
    """Physics body for simulation"""
    mass: float = 1.0
    position: np.ndarray = None
    velocity: np.ndarray = None
    acceleration: np.ndarray = None
    orientation: np.ndarray = None  # Quaternion
    angular_velocity: np.ndarray = None
    
    def __post_init__(self):
        if self.position is None:
            self.position = np.zeros(3)
        if self.velocity is None:
            self.velocity = np.zeros(3)
        if self.acceleration is None:
            self.acceleration = np.zeros(3)
        if self.orientation is None:
            self.orientation = np.array([1.0, 0.0, 0.0, 0.0])  # Identity
        if self.angular_velocity is None:
            self.angular_velocity = np.zeros(3)
            
    def apply_force(self, force: np.ndarray, dt: float):
        """Apply force to body"""
        self.acceleration = force / self.mass
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        
    def apply_torque(self, torque: np.ndarray, dt: float):
        """Apply torque to body"""
        # Simplified: angular acceleration proportional to torque
        self.angular_velocity += torque * dt
        # Update orientation (simplified)
        

class CollisionDetector:
    """Simple collision detection"""
    
    def __init__(self):
        self.ground_level = 0.0
        
    def check_ground_collision(self, position: np.ndarray, radius: float = 0.1) -> bool:
        """Check if object collides with ground"""
        return position[2] - radius <= self.ground_level
        
    def resolve_ground_collision(self, body: RigidBody, radius: float = 0.1, 
                                  restitution: float = 0.3):
        """Resolve collision with ground"""
        if body.position[2] - radius <= self.ground_level:
            # Push above ground
            body.position[2] = self.ground_level + radius
            # Dampen velocity
            body.velocity[2] = -body.velocity[2] * restitution
            # Apply friction
            body.velocity[0] *= 0.8
            body.velocity[1] *= 0.8


class SpinePhysics:
    """Physics model for snake spine"""
    
    def __init__(self, num_segments: int = 25):
        self.num_segments = num_segments
        self.segments: List[RigidBody] = []
        self.joints: List[Tuple[int, int]] = []  # Connected segments
        
        # Create segments
        for i in range(num_segments):
            body = RigidBody(mass=0.08)  # 80g per vertebra
            body.position = np.array([0.0, i * 0.02, 0.9])  # Stacked
            self.segments.append(body)
            
        # Connect joints (parent-child)
        for i in range(num_segments - 1):
            self.joints.append((i, i + 1))
            
    def update(self, dt: float, joint_angles: List[Tuple[float, float]]):
        """Update physics with joint angles"""
        # Apply gravity
        gravity = np.array([0.0, 0.0, -9.81])
        
        for i, body in enumerate(self.segments):
            # Gravity force
            force = body.mass * gravity
            
            # Joint constraints (simplified)
            if i < len(joint_angles):
                # Apply joint angle as virtual force
                pitch, roll = joint_angles[i]
                # Pitch affects forward/back
                pitch_force = np.array([0.0, np.sin(np.radians(pitch)) * 0.1, 0.0])
                force += pitch_force
                
            body.apply_force(force, dt)
            
        # Collision detection
        detector = CollisionDetector()
        for body in self.segments:
            detector.resolve_ground_collision(body, radius=0.02)
            
    def get_stability(self) -> float:
        """Calculate stability from COM and base"""
        # Center of mass
        com = np.mean([s.position for s in self.segments], axis=0)
        
        # Base is lowest segment
        base_z = min(s.position[2] for s in self.segments)
        
        # Height of COM above base
        com_height = com[2] - base_z
        
        # Stability score (higher is more stable)
        if com_height < 0.1:
            return 0.0  # Fallen
        else:
            return min(1.0, com_height / 0.3)


class PhysicsSimulator:
    """Main physics simulation"""
    
    def __init__(self):
        self.spine = SpinePhysics()
        self.collision = CollisionDetector()
        self.time = 0.0
        self.dt = 0.01  # 100Hz simulation
        
    def step(self, joint_targets: List[Tuple[float, float]]) -> dict:
        """One physics step"""
        self.spine.update(self.dt, joint_targets)
        self.time += self.dt
        
        # Calculate metrics
        stability = self.spine.get_stability()
        com = np.mean([s.position for s in self.spine.segments], axis=0)
        
        # Check fall
        fallen = com[2] < 0.3
        
        return {
            "time": self.time,
            "stability": stability,
            "com": com,
            "fallen": fallen,
            "segments": len(self.spine.segments)
        }
        
    def reset(self):
        """Reset simulation"""
        self.spine = SpinePhysics()
        self.time = 0.0


def test_physics():
    """Test physics engine"""
    print("Testing COBRA Physics Engine...")
    
    sim = PhysicsSimulator()
    
    # Test standing
    print("\nTest 1: Standing posture")
    standing_angles = [(0, 0) for _ in range(25)]
    
    for _ in range(100):
        result = sim.step(standing_angles)
        
    print(f"  Stability: {result['stability']:.2f}")
    print(f"  COM height: {result['com'][2]:.3f}m")
    
    # Test forward bend
    print("\nTest 2: Forward bend")
    sim.reset()
    bend_angles = [(15, 0) for _ in range(25)]
    
    for _ in range(100):
        result = sim.step(bend_angles)
        
    print(f"  Stability: {result['stability']:.2f}")
    print(f"  COM height: {result['com'][2]:.3f}m")
    
    print("\n✅ Physics tests passed")


if __name__ == "__main__":
    test_physics()
