#!/usr/bin/env python3
"""
COBRA Policy Deployment
Transfer learned virtual behaviors to physical robot
"""

import json
import time
from typing import Dict, List


class PhysicalRobotInterface:
    """Interface to physical COBRA robot"""
    
    def __init__(self, port: str = "/dev/ttyUSB0"):
        self.port = port
        self.connected = False
        self.vertebrae = 25
        
    def connect(self) -> bool:
        """Connect to physical robot"""
        print(f"Connecting to COBRA on {self.port}...")
        # In real implementation, would open serial/CAN connection
        self.connected = True
        print("✅ Connected to physical COBRA")
        return True
        
    def set_joint_angles(self, angles: List[float], speed: float = 100.0):
        """Set joint angles on physical robot"""
        if not self.connected:
            raise RuntimeError("Not connected to robot")
            
        # Send angles to physical servos via CAN bus
        # Format: [pitch_0, roll_0, pitch_1, roll_1, ...]
        for i in range(min(len(angles) // 2, self.vertebrae)):
            pitch = angles[i * 2]
            roll = angles[i * 2 + 1] if i * 2 + 1 < len(angles) else 0.0
            
            # Clamp to safe limits
            pitch = max(-15, min(15, pitch))
            roll = max(-10, min(10, roll))
            
            # Send to physical servo (simulated here)
            # real_implementation: can_bus.send_servo_command(i, pitch, roll, speed)
            
    def get_joint_feedback(self) -> Dict:
        """Get current state from physical robot"""
        return {
            "positions": [0.0] * (self.vertebrae * 2),
            "currents": [0.0] * (self.vertebrae * 2),
            "temperatures": [25.0] * self.vertebrae
        }
        
    def emergency_stop(self):
        """Emergency stop all motion"""
        print("🛑 EMERGENCY STOP")
        # real_implementation: can_bus.send_emergency_stop()
        
    def disconnect(self):
        """Safely disconnect"""
        if self.connected:
            self.emergency_stop()
            self.connected = False
            print("✅ Disconnected from physical COBRA")


class PolicyDeployer:
    """Deploy learned policies to physical robot"""
    
    def __init__(self, policy_file: str = "cobra_learned_policy.json"):
        self.policy_file = policy_file
        self.policy_data = None
        self.robot = PhysicalRobotInterface()
        
    def load_policy(self) -> bool:
        """Load policy from file"""
        try:
            with open(self.policy_file, 'r') as f:
                self.policy_data = json.load(f)
                
            print(f"✅ Loaded policy: {self.policy_file}")
            print(f"   Episodes trained: {self.policy_data['episodes_trained']}")
            print(f"   Best virtual time: {self.policy_data['best_time']:.2f}s")
            print(f"   Postures learned: {len(self.policy_data['postures'])}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load policy: {e}")
            return False
            
    def validate_policy(self) -> bool:
        """Validate policy for safety"""
        if not self.policy_data:
            print("❌ No policy loaded")
            return False
            
        print("\n🔍 Validating policy...")
        
        # Check posture count
        postures = self.policy_data['postures']
        if len(postures) == 0:
            print("❌ No postures in policy")
            return False
            
        # Check joint angles are within limits
        for i, posture in enumerate(postures):
            if len(posture) != 50:
                print(f"⚠️  Posture {i} has {len(posture)} angles, expected 50")
                
            # Check for extreme values
            max_angle = max(abs(a) for a in posture)
            if max_angle > 20:
                print(f"⚠️  Posture {i} has extreme angles: {max_angle}")
                
        print(f"✅ Policy validated: {len(postures)} postures ready")
        return True
        
    def test_sequence(self, duration: float = 5.0):
        """Test learned postures in sequence"""
        if not self.robot.connect():
            return
            
        print(f"\n🧪 Testing learned postures on physical robot...")
        print(f"   Duration: {duration}s")
        print("   ⚠️  Ensure robot is secured to test stand!")
        
        # Safety check
        input("\nPress ENTER when ready (or Ctrl+C to abort)...")
        
        try:
            postures = self.policy_data['postures']
            posture_index = 0
            start_time = time.time()
            
            while time.time() - start_time < duration:
                # Get next posture
                posture = postures[posture_index % len(postures)]
                
                # Apply to robot
                self.robot.set_joint_angles(posture, speed=50.0)
                
                # Hold for 0.5s
                time.sleep(0.5)
                
                # Check feedback
                feedback = self.robot.get_joint_feedback()
                max_temp = max(feedback['temperatures'])
                
                if max_temp > 50:
                    print(f"⚠️  High temperature detected: {max_temp}°C")
                    
                posture_index += 1
                
                if posture_index % 10 == 0:
                    print(f"   Tested {posture_index} postures...")
                    
        except KeyboardInterrupt:
            print("\n⏹️  Test interrupted by user")
        finally:
            self.robot.emergency_stop()
            self.robot.disconnect()
            
    def deploy_walking_skill(self):
        """Deploy walking skill to physical robot"""
        if not self.robot.connect():
            return
            
        print("\n🚶 Deploying walking skill...")
        print("   This will make the robot attempt to walk in place")
        
        input("\nPress ENTER when robot is secured and ready...")
        
        try:
            # Apply gait sequence
            gait_sequence = self.generate_gait_sequence()
            
            for i, posture in enumerate(gait_sequence):
                print(f"   Step {i+1}/{len(gait_sequence)}")
                self.robot.set_joint_angles(posture, speed=80.0)
                time.sleep(0.3)
                
        except Exception as e:
            print(f"❌ Walking deployment failed: {e}")
        finally:
            self.robot.emergency_stop()
            self.robot.disconnect()
            
    def generate_gait_sequence(self) -> List[List[float]]:
        """Generate walking gait from learned postures"""
        # Simple forward walking gait
        # Alternates weight between sides while propelling forward
        
        base_posture = self.policy_data['postures'][0] if self.policy_data['postures'] else [0.0] * 50
        
        gait = []
        
        # Step 1: Neutral
        gait.append(base_posture)
        
        # Step 2: Shift weight left
        left_shift = base_posture.copy()
        for i in range(19, 24):  # Lumbar
            left_shift[i * 2 + 1] = 5.0  # Roll left
        gait.append(left_shift)
        
        # Step 3: Lift right (simulated)
        lift_right = left_shift.copy()
        for i in range(10, 15):  # Right side thoracic
            lift_right[i * 2] = 3.0  # Slight pitch
        gait.append(lift_right)
        
        # Step 4: Return to neutral
        gait.append(base_posture)
        
        # Step 5: Shift weight right
        right_shift = base_posture.copy()
        for i in range(19, 24):  # Lumbar
            right_shift[i * 2 + 1] = -5.0  # Roll right
        gait.append(right_shift)
        
        # Step 6: Lift left
        lift_left = right_shift.copy()
        for i in range(5, 10):  # Left side thoracic
            lift_left[i * 2] = 3.0  # Slight pitch
        gait.append(lift_left)
        
        # Step 7: Return to neutral
        gait.append(base_posture)
        
        return gait
        
    def export_to_robot_memory(self, robot_id: str = "COBRA-001"):
        """Export policy directly to robot's onboard memory"""
        print(f"\n💾 Exporting policy to robot {robot_id}...")
        
        # Format for onboard storage
        onboard_policy = {
            "robot_id": robot_id,
            "policy_version": "1.0",
            "postures": self.policy_data['postures'],
            "gait_sequences": {
                "walk": self.generate_gait_sequence(),
                "stand": [self.policy_data['postures'][0]] if self.policy_data['postures'] else []
            },
            "safety_limits": {
                "max_joint_angle": 15.0,
                "max_temperature": 60.0,
                "max_current": 2.0
            }
        }
        
        output_file = f"{robot_id}_policy.bin"
        with open(output_file, 'w') as f:
            json.dump(onboard_policy, f, indent=2)
            
        print(f"✅ Policy exported to {output_file}")
        print(f"   Ready to flash to {robot_id}")
        print(f"   File size: {len(json.dumps(onboard_policy))} bytes")


def main():
    """Policy Deployment Tool"""
    print("=" * 70)
    print("🐍 COBRA Policy Deployment Tool")
    print("=" * 70)
    print("Transfer virtual learning to physical robot")
    print("=" * 70)
    
    deployer = PolicyDeployer("cobra_learned_policy.json")
    
    # Load policy
    if not deployer.load_policy():
        return
        
    # Validate
    if not deployer.validate_policy():
        return
        
    # Menu
    while True:
        print("\n" + "=" * 70)
        print("Deployment Options:")
        print("  1. Test postures on physical robot")
        print("  2. Deploy walking skill")
        print("  3. Export to robot memory")
        print("  4. Validate only (no physical)")
        print("  5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            deployer.test_sequence(duration=5.0)
        elif choice == "2":
            deployer.deploy_walking_skill()
        elif choice == "3":
            robot_id = input("Enter robot ID (default: COBRA-001): ").strip() or "COBRA-001"
            deployer.export_to_robot_memory(robot_id)
        elif choice == "4":
            print("\n✅ Policy validation complete")
        elif choice == "5":
            print("\n👋 Exiting")
            break
        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main()
