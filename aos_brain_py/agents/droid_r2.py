#!/usr/bin/env python3
"""
R2 Droid Integration - Astromech platform interface.
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))


class R2DroidInterface:
    """R2 Astromech Droid - Physical platform for agent operations."""
    
    def __init__(self):
        self.name = "R2"
        self.type = "Astromech"
        self.status = "online"
        self.battery_level = 94.0
        self.position = {"x": 0, "y": 0, "theta": 0}
        
        # Hardware components
        self.dome_rotation = 0  # degrees
        self.holo_projector = False
        self.tool_arm = None
        
        # Sensors
        self.sensors = {
            "proximity": [],
            "camera": [],
            "audio": []
        }
        
    def move_forward(self, distance: float = 1.0):
        """Move forward by distance units."""
        self.position["x"] += distance * self.position["theta"]
        self.battery_level -= 0.5
        return {"action": "move_forward", "distance": distance, "position": self.position}
    
    def rotate_dome(self, degrees: float):
        """Rotate dome for scanning."""
        self.dome_rotation = (self.dome_rotation + degrees) % 360
        return {"action": "dome_rotate", "degrees": degrees, "total": self.dome_rotation}
    
    def deploy_tool(self, tool_type: str):
        """Deploy a tool arm."""
        self.tool_arm = tool_type
        self.battery_level -= 1.0
        return {"action": "tool_deploy", "tool": tool_type}
    
    def scan_environment(self):
        """Scan surroundings."""
        self.sensors["proximity"] = ["clear", "obstacle_at_2m", "clear"]
        return {"action": "scan", "readings": self.sensors}
    
    def play_audio(self, sound: str):
        """Play sound effect."""
        return {"action": "audio", "sound": sound}
    
    def get_status(self) -> dict:
        """Return current droid status."""
        return {
            "name": self.name,
            "type": self.type,
            "status": self.status,
            "battery": f"{self.battery_level:.1f}%",
            "position": self.position,
            "dome": self.dome_rotation,
            "tool": self.tool_arm
        }


class MylonenR2Mission:
    """Joint mission with Mylonen and R2."""
    
    def __init__(self):
        from agents.mylonen_adapter import MylonenAdapter
        
        self.mylonen = MylonenAdapter()
        self.r2 = R2DroidInterface()
        self.mission_log = []
        
    def run_reconnaissance(self):
        """Run reconnaissance mission."""
        print("\n[MISSION] Reconnaissance")
        
        # Mylonen processes objective
        self.mylonen.process("Reconnaissance: scan area, identify obstacles", "mission")
        
        # R2 executes
        self.r2.move_forward(2.0)
        scan = self.r2.scan_environment()
        self.r2.rotate_dome(45)
        
        print(f"  ✓ R2 scanned: {scan['readings']['proximity']}")
        print(f"  ✓ Dome rotated to {self.r2.dome_rotation}°")
        
        self.mission_log.append({"type": "recon", "result": scan})
        
    def run_tool_deployment(self):
        """Run tool deployment mission."""
        print("\n[MISSION] Tool Deployment")
        
        # Mylonen decides tool needed
        self.mylonen.process("Deploy soldering arm for repair", "mission")
        
        # R2 deploys
        result = self.r2.deploy_tool("soldering")
        self.r2.play_audio("beep_boop")
        
        print(f"  ✓ Deployed: {result['tool']}")
        print(f"  ✓ Audio: beep_boop")
        
        self.mission_log.append({"type": "tool", "result": result})
        
    def run_navigation(self):
        """Run navigation mission."""
        print("\n[MISSION] Navigation")
        
        # Mylonen plans route
        self.mylonen.process("Navigate to target avoiding obstacles", "mission")
        
        # R2 executes movement
        moves = []
        for i in range(3):
            move = self.r2.move_forward(1.0)
            moves.append(move)
            time.sleep(0.1)
        
        print(f"  ✓ Executed {len(moves)} moves")
        print(f"  ✓ Final position: {self.r2.position}")
        
        self.mission_log.append({"type": "nav", "moves": len(moves)})
        
    def get_status(self):
        """Return mission status."""
        return {
            "mylonen": self.mylonen.get_status(),
            "r2": self.r2.get_status(),
            "missions_completed": len(self.mission_log),
            "log": self.mission_log
        }


def deploy_test_subjects():
    """Deploy both test subjects."""
    print("=" * 70)
    print("🚀 DEPLOYING TEST SUBJECTS")
    print("=" * 70)
    
    mission = MylonenR2Mission()
    
    print(f"\n🤖 MYLONEN")
    print(f"  Name: {mission.mylonen.name}")
    print(f"  Level: {mission.mylonen.level}")
    print(f"  Role: {mission.mylonen.role}")
    print(f"  Brain ticks: {mission.mylonen.brain.tick_count}")
    
    print(f"\n🛸 R2 DROID")
    print(f"  Name: {mission.r2.name}")
    print(f"  Type: {mission.r2.type}")
    print(f"  Battery: {mission.r2.battery_level:.0f}%")
    print(f"  Position: {mission.r2.position}")
    
    print("\n" + "=" * 70)
    print("RUNNING MISSIONS")
    print("=" * 70)
    
    # Run all missions
    mission.run_reconnaissance()
    mission.run_tool_deployment()
    mission.run_navigation()
    
    print("\n" + "=" * 70)
    print("✅ DEPLOYMENT COMPLETE")
    print("=" * 70)
    
    status = mission.get_status()
    print(f"\nMission Summary:")
    print(f"  Missions completed: {status['missions_completed']}")
    print(f"  Mylonen brain ticks: {status['mylonen']['brain_tick']}")
    print(f"  R2 battery: {status['r2']['battery']}")
    print(f"  R2 final position: {status['r2']['position']}")
    
    return mission


if __name__ == "__main__":
    deploy_test_subjects()
