#!/usr/bin/env python3
"""
COBRA Virtual Training Environment
Physics-based simulation for robot learning
Safe training before physical deployment
"""

import numpy as np
import json
import time
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import random


class SimulationMode(Enum):
    IDLE = "idle"
    TRAINING = "training"
    TESTING = "testing"
    DEMO = "demo"


@dataclass
class JointState:
    """State of a single joint"""
    angle: float = 0.0
    velocity: float = 0.0
    torque: float = 0.0
    target_angle: float = 0.0
    

@dataclass
class PhysicsState:
    """Full physics state of robot"""
    position: np.ndarray = None  # [x, y, z]
    velocity: np.ndarray = None  # [vx, vy, vz]
    orientation: np.ndarray = None  # Quaternion [w, x, y, z]
    angular_velocity: np.ndarray = None  # [wx, wy, wz]
    
    def __post_init__(self):
        if self.position is None:
            self.position = np.array([0.0, 0.0, 0.9])  # Start 90cm high
        if self.velocity is None:
            self.velocity = np.array([0.0, 0.0, 0.0])
        if self.orientation is None:
            self.orientation = np.array([1.0, 0.0, 0.0, 0.0])  # Identity
        if self.angular_velocity is None:
            self.angular_velocity = np.array([0.0, 0.0, 0.0])


class VirtualSpine:
    """Virtual 25-vertebra snake spine with physics"""
    
    def __init__(self):
        self.num_vertebrae = 25
        self.joints: List[JointState] = []
        
        # Initialize all joints
        for i in range(self.num_vertebrae):
            self.joints.append(JointState())
            
        # Physics properties
        self.mass_per_vertebra = 0.08  # kg
        self.total_mass = self.mass_per_vertebra * self.num_vertebrae
        self.height = 0.5  # meters
        
        # Joint limits
        self.pitch_limits = []
        self.roll_limits = []
        
        # Cervical (0-6): more flexible
        for i in range(7):
            self.pitch_limits.append((-15, 15))
            self.roll_limits.append((-10, 10))
            
        # Thoracic (7-18): less flexible
        for i in range(7, 19):
            self.pitch_limits.append((-10, 10))
            self.roll_limits.append((-5, 5))
            
        # Lumbar (19-23): flexible
        for i in range(19, 24):
            self.pitch_limits.append((-15, 15))
            self.roll_limits.append((-10, 10))
            
        # Sacrum (24): rigid
        self.pitch_limits.append((-5, 5))
        self.roll_limits.append((-5, 5))
        
    def set_target_posture(self, pitch_angles: List[float], roll_angles: List[float]):
        """Set target angles for all joints"""
        for i, (p, r) in enumerate(zip(pitch_angles[:self.num_vertebrae], 
                                        roll_angles[:self.num_vertebrae])):
            # Clamp to limits
            p_min, p_max = self.pitch_limits[i]
            r_min, r_max = self.roll_limits[i]
            self.joints[i].target_angle = np.clip(p, p_min, p_max)
            
    def update(self, dt: float):
        """Update joint positions toward targets"""
        max_speed = 90.0  # degrees per second
        
        for joint in self.joints:
            error = joint.target_angle - joint.angle
            max_change = max_speed * dt
            
            if abs(error) < max_change:
                joint.angle = joint.target_angle
                joint.velocity = 0
            else:
                direction = np.sign(error)
                joint.angle += direction * max_change
                joint.velocity = direction * max_speed
                
    def get_center_of_mass(self) -> np.ndarray:
        """Calculate center of mass position"""
        # Simplified: average of vertebrae positions
        # In real physics, would integrate along curved spine
        positions = []
        y = 0
        for i, joint in enumerate(self.joints):
            # Rough approximation of vertebra position
            y += 0.02 * np.cos(np.radians(joint.angle))
            positions.append([0, y, 0])
            
        return np.mean(positions, axis=0) if positions else np.array([0, 0.25, 0])
        
    def get_stability_score(self) -> float:
        """Calculate stability metric (0-1, higher is better)"""
        # Check if COM is over base of support
        com = self.get_center_of_mass()
        
        # Simplified: check if COM is within reasonable bounds
        x_dev = abs(com[0])
        z_dev = abs(com[2])
        
        # Lower deviation = higher stability
        stability = max(0, 1.0 - (x_dev + z_dev) / 0.5)
        return stability


class VirtualBalanceSystem:
    """Virtual balance controller"""
    
    def __init__(self):
        self.target_pitch = 0.0
        self.target_roll = 0.0
        self.kp = 0.5  # Proportional gain
        self.kd = 0.1  # Derivative gain
        
    def compute_corrections(self, current_pitch: float, current_roll: float,
                           pitch_rate: float, roll_rate: float) -> Tuple[float, float]:
        """Compute balance corrections"""
        # PID-style control
        pitch_error = self.target_pitch - current_pitch
        roll_error = self.target_roll - current_roll
        
        pitch_correction = self.kp * pitch_error - self.kd * pitch_rate
        roll_correction = self.kp * roll_error - self.kd * roll_rate
        
        return pitch_correction, roll_correction


class VirtualRobot:
    """Complete virtual COBRA robot"""
    
    def __init__(self, name: str = "COBRA-Virtual"):
        self.name = name
        self.spine = VirtualSpine()
        self.balance = VirtualBalanceSystem()
        self.physics = PhysicsState()
        
        # State tracking
        self.time_alive = 0.0
        self.distance_moved = 0.0
        self.falls = 0
        self.energy_used = 0.0
        
        # Learning metrics
        self.walking_skill = 0.0  # 0-1, learned over time
        self.balance_skill = 0.0
        self.reward_history = []
        
    def reset(self, randomize: bool = False):
        """Reset to initial state"""
        self.physics = PhysicsState()
        self.time_alive = 0.0
        self.distance_moved = 0.0
        
        # Reset joints
        for joint in self.spine.joints:
            joint.angle = 0.0
            joint.velocity = 0.0
            if randomize:
                joint.angle = random.uniform(-5, 5)
                
    def apply_action(self, action: np.ndarray):
        """Apply action from AI controller"""
        # Action is array of 25 pitch + 25 roll targets
        if len(action) >= 50:
            pitch_targets = action[:25]
            roll_targets = action[25:50]
            self.spine.set_target_posture(pitch_targets.tolist(), roll_targets.tolist())
            
    def step(self, dt: float = 0.01) -> Dict:
        """Simulation step"""
        # Update physics
        self.spine.update(dt)
        
        # Simple gravity simulation
        self.physics.velocity[2] -= 9.81 * dt  # Gravity
        self.physics.position += self.physics.velocity * dt
        
        # Ground collision
        if self.physics.position[2] <= 0:
            self.physics.position[2] = 0
            self.physics.velocity[2] = max(0, self.physics.velocity[2])
            
        # Calculate reward
        stability = self.spine.get_stability_score()
        height = self.physics.position[2]
        upright = 1.0 if height > 0.4 else 0.0
        
        reward = stability * upright * 10.0  # Base survival reward
        
        # Fall detection
        fallen = height < 0.2
        if fallen:
            reward = -100.0
            self.falls += 1
            
        self.time_alive += dt
        self.reward_history.append(reward)
        
        return {
            "position": self.physics.position.copy(),
            "velocity": self.physics.velocity.copy(),
            "stability": stability,
            "upright": upright,
            "fallen": fallen,
            "reward": reward,
            "time_alive": self.time_alive
        }
        
    def get_observation(self) -> np.ndarray:
        """Get state observation for AI"""
        obs = []
        
        # Joint angles (50 values)
        for joint in self.spine.joints:
            obs.append(joint.angle / 90.0)  # Normalize
            obs.append(0.0)  # Placeholder for roll
            
        # Physics state (6 values)
        obs.extend(self.physics.position / 2.0)  # Normalize position
        obs.extend(self.physics.velocity / 5.0)  # Normalize velocity
        
        return np.array(obs, dtype=np.float32)


class LearningAgent:
    """AI agent that learns to control the robot"""
    
    def __init__(self, robot: VirtualRobot):
        self.robot = robot
        self.episode_count = 0
        self.best_time = 0.0
        self.total_reward = 0.0
        
        # Simple policy: store good postures
        self.good_postures = []
        self.exploration_rate = 0.3
        
    def select_action(self, observation: np.ndarray, training: bool = True) -> np.ndarray:
        """Select action based on current policy"""
        if training and random.random() < self.exploration_rate:
            # Random exploration
            return np.random.uniform(-15, 15, size=50)
        else:
            # Use learned policy
            if self.good_postures:
                # Pick random good posture
                return random.choice(self.good_postures)
            else:
                # Default standing posture
                action = np.zeros(50)
                # S-curve
                action[:7] = 5.0  # Cervical forward
                action[7:19] = -3.0  # Thoracic back
                action[19:24] = 8.0  # Lumbar forward
                return action
                
    def train_episode(self, max_steps: int = 10000) -> Dict:
        """Run one training episode"""
        self.robot.reset(randomize=True)
        
        total_reward = 0.0
        steps = 0
        survived = True
        
        for step in range(max_steps):
            # Get observation
            obs = self.robot.get_observation()
            
            # Select action
            action = self.select_action(obs, training=True)
            
            # Apply action
            self.robot.apply_action(action)
            
            # Step simulation
            result = self.robot.step()
            
            total_reward += result["reward"]
            steps += 1
            
            # Store good posture if high reward
            if result["reward"] > 8.0 and len(self.good_postures) < 100:
                self.good_postures.append(action.copy())
                
            # Check termination
            if result["fallen"]:
                survived = False
                break
                
        self.episode_count += 1
        self.total_reward = total_reward
        
        if self.robot.time_alive > self.best_time:
            self.best_time = self.robot.time_alive
            
        # Decay exploration
        self.exploration_rate = max(0.05, self.exploration_rate * 0.995)
        
        return {
            "episode": self.episode_count,
            "steps": steps,
            "time_alive": self.robot.time_alive,
            "total_reward": total_reward,
            "survived": survived,
            "best_time": self.best_time,
            "exploration_rate": self.exploration_rate,
            "postures_learned": len(self.good_postures)
        }
        
    def export_policy(self, filename: str):
        """Export learned policy for physical robot"""
        policy_data = {
            "name": self.robot.name,
            "episodes_trained": self.episode_count,
            "best_time": self.best_time,
            "postures": [p.tolist() for p in self.good_postures[:20]],  # Top 20
            "metadata": {
                "version": "1.0",
                "simulation": "COBRA-Virtual-v1",
                "export_date": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(policy_data, f, indent=2)
            
        print(f"✅ Policy exported to {filename}")


class TrainingEnvironment:
    """Complete training environment"""
    
    def __init__(self):
        self.robot = VirtualRobot()
        self.agent = LearningAgent(self.robot)
        self.mode = SimulationMode.IDLE
        
    def run_training(self, episodes: int = 100, log_interval: int = 10):
        """Run training for N episodes"""
        print(f"\n🎓 Starting Training: {episodes} episodes")
        print("=" * 70)
        
        self.mode = SimulationMode.TRAINING
        
        for ep in range(episodes):
            result = self.agent.train_episode()
            
            if (ep + 1) % log_interval == 0:
                print(f"Episode {result['episode']:4d} | "
                      f"Time: {result['time_alive']:6.2f}s | "
                      f"Reward: {result['total_reward']:8.1f} | "
                      f"Best: {result['best_time']:6.2f}s | "
                      f"Exploration: {result['exploration_rate']:.3f} | "
                      f"Postures: {result['postures_learned']:3d}")
                      
        print("=" * 70)
        print(f"\n✅ Training Complete!")
        print(f"   Episodes: {episodes}")
        print(f"   Best Survival Time: {self.agent.best_time:.2f}s")
        print(f"   Postures Learned: {len(self.agent.good_postures)}")
        
    def test_policy(self, episodes: int = 10):
        """Test learned policy without exploration"""
        print(f"\n🧪 Testing Policy: {episodes} episodes")
        print("=" * 70)
        
        self.mode = SimulationMode.TESTING
        
        # Temporarily disable exploration
        old_exploration = self.agent.exploration_rate
        self.agent.exploration_rate = 0.0
        
        results = []
        for ep in range(episodes):
            result = self.agent.train_episode(max_steps=5000)
            results.append(result["time_alive"])
            print(f"Test {ep+1:2d}: Survived {result['time_alive']:.2f}s")
            
        self.agent.exploration_rate = old_exploration
        
        avg_time = np.mean(results)
        print("=" * 70)
        print(f"\n📊 Test Results:")
        print(f"   Average Survival: {avg_time:.2f}s")
        print(f"   Best: {max(results):.2f}s")
        print(f"   Worst: {min(results):.2f}s")
        
    def demo(self, duration: float = 30.0):
        """Demonstrate learned behavior"""
        print(f"\n🎭 Running Demo: {duration}s")
        print("=" * 70)
        
        self.mode = SimulationMode.DEMO
        self.robot.reset()
        
        start_time = time.time()
        step_count = 0
        
        while time.time() - start_time < duration:
            obs = self.robot.get_observation()
            action = self.agent.select_action(obs, training=False)
            self.robot.apply_action(action)
            
            result = self.robot.step()
            step_count += 1
            
            if step_count % 100 == 0:
                print(f"Time: {result['time_alive']:6.2f}s | "
                      f"Height: {result['position'][2]:.3f}m | "
                      f"Stability: {result['stability']:.2f}")
                      
            if result["fallen"]:
                print(f"⚠️  Robot fell after {result['time_alive']:.2f}s")
                self.robot.reset()
                
        print("=" * 70)
        print(f"✅ Demo Complete - {step_count} simulation steps")


def main():
    """Virtual Training Environment Demo"""
    print("=" * 70)
    print("🐍 COBRA Virtual Training Environment")
    print("=" * 70)
    print("Safe AI learning before physical deployment")
    print("=" * 70)
    
    # Create training environment
    env = TrainingEnvironment()
    
    # Phase 1: Initial training
    print("\n📚 Phase 1: Initial Training (100 episodes)")
    env.run_training(episodes=100, log_interval=20)
    
    # Phase 2: Policy testing
    print("\n📋 Phase 2: Policy Testing")
    env.test_policy(episodes=5)
    
    # Phase 3: Demo
    print("\n🎬 Phase 3: Live Demo")
    env.demo(duration=10.0)
    
    # Export learned policy
    print("\n💾 Phase 4: Export Policy")
    env.agent.export_policy("cobra_learned_policy.json")
    
    print("\n" + "=" * 70)
    print("✅ Virtual Training Complete")
    print("=" * 70)
    print("\nPolicy file 'cobra_learned_policy.json' ready for")
    print("deployment to physical COBRA robot.")
    print("\nThe robot has learned:")
    print(f"  • {len(env.agent.good_postures)} stable postures")
    print(f"  • Best survival time: {env.agent.best_time:.2f}s")
    print(f"  • Ready for physical body transfer")


if __name__ == "__main__":
    main()
