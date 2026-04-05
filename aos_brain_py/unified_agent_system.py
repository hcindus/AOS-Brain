#!/usr/bin/env python3
"""
Unified Brain System - Mylonen + R2 with Shared Organs

Both agents use:
- One Brain (7-region OODA)
- One Heart (ternary rhythm)  
- One Stomach (energy/metabolism)
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

sys.path.insert(0, str(Path(__file__).parent))

from brain.seven_region import SevenRegionBrain
from heart.ternary_heart import TernaryHeart, HeartState
from stomach.ternary_stomach import TernaryStomach, StomachState


class SharedOrgans:
    """Shared organ system for all agents."""
    
    def __init__(self):
        print("[SharedOrgans] Initializing...")
        
        # STOMACH - Shared energy
        self.stomach = TernaryStomach()
        print("  ✅ Stomach: HUNGRY/SATISFIED/FULL")
        
        # HEART - Shared rhythm
        self.heart = TernaryHeart()
        print("  ✅ Heart: REST/BALANCE/ACTIVE")
        
        # BRAIN - Shared cognition
        self.brain = SevenRegionBrain()
        print("  ✅ Brain: 7-region OODA")
        
        self.tick_count = 0
        print("[SharedOrgans] ✅ Ready")
    
    def cycle(self, agent_name: str, observation: str) -> Dict:
        """One organ cycle: Stomach -> Heart -> Brain -> Output"""
        self.tick_count += 1
        
        # 1. STOMACH - Digest energy
        stomach_output = self.stomach.digest()
        
        # 2. HEART - Generate rhythm
        heart_inputs = {
            "brain_arousal": 0.5,
            "safety": 0.8,
            "connection": 0.6,
            "stress": 0.2,
        }
        heart_output = self.heart.beat(heart_inputs)
        
        # 3. BRAIN - OODA cognition
        brain_input = {
            "text": f"[{agent_name}] {observation}",
            "source": agent_name,
            "heart_arousal": heart_output.get("heart_arousal", 0.5),
            "stomach_energy": stomach_output.get("energy_level", 0.5),
        }
        brain_output = self.brain.tick(brain_input)
        
        return {
            "tick": self.tick_count,
            "stomach": stomach_output,
            "heart": heart_output,
            "brain": brain_output,
        }


class MylonenAgent:
    """Mylonen - Scout Operations with shared organs."""
    
    def __init__(self, organs: SharedOrgans):
        self.name = "Mylonen"
        self.level = 2
        self.role = "Scout Operations"
        self.organs = organs
        self.position = [0, 0]
        self.mission_log = []
        
        print(f"[{self.name}] Connected to shared organs")
    
    def perceive(self, observation: str) -> Dict:
        """Mylonen perceives through shared organs."""
        result = self.organs.cycle(self.name, observation)
        
        # Mylonen interprets based on scout training
        brain = result["brain"]
        mode = brain.get("mode", "Unknown")
        
        response = f"[{self.name}] Scout analysis: {mode}"
        if "explore" in observation.lower():
            response += " | Terrain scanning..."
        elif "tool" in observation.lower():
            response += " | Equipment check..."
        elif "move" in observation.lower():
            self.position[0] += 1
            response += f" | Position: {self.position}"
        
        self.mission_log.append({
            "observation": observation,
            "mode": mode,
            "tick": result["tick"],
        })
        
        return {
            "agent": self.name,
            "response": response,
            "mode": mode,
            "position": self.position,
            "organs": result,
        }


class R2Agent:
    """R2 Droid - Astromech with shared organs."""
    
    def __init__(self, organs: SharedOrgans):
        self.name = "R2-D2"
        self.droid_type = "Astromech"
        self.organs = organs
        
        # Physical state
        self.dome_angle = 0
        self.tool_arm = "retracted"
        self.position = [0, 0]
        self.battery = 100.0
        self.holo_active = False
        
        print(f"[{self.name}] Connected to shared organs")
    
    def perceive(self, observation: str) -> Dict:
        """R2 perceives through shared organs."""
        result = self.organs.cycle(self.name, observation)
        
        # R2 interprets as astromech
        brain = result["brain"]
        action = brain.get("action", "observe")
        
        # Execute based on brain decision
        executed_action = self._execute(action, observation)
        
        return {
            "agent": self.name,
            "action": executed_action,
            "dome": self.dome_angle,
            "position": self.position,
            "battery": self.battery,
            "organs": result,
        }
    
    def _execute(self, action: str, context: str) -> str:
        """Execute physical action based on brain decision."""
        
        if action == "scan" or "scan" in context.lower():
            self.dome_angle = (self.dome_angle + 45) % 360
            self.battery -= 0.5
            return f"Rotated dome to {self.dome_angle}° | Scanned"
        
        elif action == "tool" or "tool" in context.lower():
            self.tool_arm = "extended"
            self.battery -= 2.0
            return f"Extended {self.tool_arm} | Tool ready"
        
        elif action == "move" or "move" in context.lower():
            self.position[0] += 1
            self.battery -= 1.0
            return f"Moved to {self.position}"
        
        elif action == "holo" or "holo" in context.lower():
            self.holo_active = True
            self.battery -= 3.0
            return f"Holo projector active"
        
        else:
            return f"Observing | Battery: {self.battery:.0f}%"


class UnifiedAgentSystem:
    """Mylonen + R2 sharing brain, heart, stomach."""
    
    def __init__(self):
        print("=" * 70)
        print("🫀🧠🤖 UNIFIED AGENT SYSTEM")
        print("Mylonen + R2 + Shared Brain + Heart + Stomach")
        print("=" * 70)
        print()
        
        # Create shared organs once
        self.organs = SharedOrgans()
        print()
        
        # Create agents with shared organs
        self.mylonen = MylonenAgent(self.organs)
        self.r2 = R2Agent(self.organs)
        
        print()
        print("=" * 70)
        print("✅ ALL AGENTS CONNECTED TO SHARED ORGANS")
        print("=" * 70)
        print()
    
    def run_mission(self, mission: str, steps: int = 10):
        """Run mission with both agents."""
        print(f"🚀 MISSION: {mission}")
        print(f"   Agents: Mylonen (Scout) + R2 (Astromech)")
        print(f"   Organs: Shared Brain + Heart + Stomach")
        print()
        
        for i in range(steps):
            tick = self.organs.tick_count + 1
            
            # Mylonen observes
            mylonen_obs = f"Step {i+1}: Scout reconnaissance"
            mylonen_result = self.mylonen.perceive(mylonen_obs)
            
            # R2 observes (different perspective, same organs)
            r2_obs = f"Step {i+1}: Technical assessment"
            r2_result = self.r2.perceive(r2_obs)
            
            # Get organ states
            heart_state = self.organs.heart.rhythm.state.name
            stomach_state = self.organs.stomach.state.name
            
            print(f"[Tick {tick:2d}] Heart: {heart_state:8s} | "
                  f"Stomach: {stomach_state:12s}")
            print(f"         Mylonen: {mylonen_result['response'][:40]}...")
            print(f"         R2:      {r2_result['action'][:40]}...")
            print()
            
            time.sleep(0.3)
        
        print("=" * 70)
        print("✅ MISSION COMPLETE")
        print("=" * 70)
        print()
        print("Final Status:")
        print(f"  Total ticks: {self.organs.tick_count}")
        print(f"  Mylonen position: {self.mylonen.position}")
        print(f"  R2 position: {self.r2.position}")
        print(f"  R2 battery: {self.r2.battery:.1f}%")
        print(f"  Brain mode: {mylonen_result['organs']['brain'].get('mode', 'Unknown')}")
        print()


def main():
    """Run unified system."""
    system = UnifiedAgentSystem()
    
    # Run test mission
    system.run_mission("Jordan Hostinger Deployment Support", steps=15)
    
    return system


if __name__ == "__main__":
    system = main()
