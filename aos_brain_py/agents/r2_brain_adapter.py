#!/usr/bin/env python3
"""
R2 Droid Brain Adapter - Connect R2 droid to 7-Region Brain with OODA loop.

R2 Droid: Astromech platform with full brain integration
- Receives commands from brain
- Reports sensor data to brain
- Has its own heart rhythm
- Connected to stomach for power management

This makes R2 an intelligent agent, not just a remote-controlled robot.
"""

import sys
import json
import time
import threading
from pathlib import Path
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain
from heart.ternary_heart import TernaryHeart, HeartState
from stomach.ternary_stomach import TernaryStomach, StomachState


@dataclass
class R2SensorData:
    """Sensor readings from R2."""
    dome_angle: int = 0
    position: List[int] = field(default_factory=lambda: [0, 0])
    battery: float = 100.0
    holo_active: bool = False
    tool_arm: str = "retracted"
    audio_detected: bool = False
    motion_detected: bool = False
    obstacles: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


class R2BrainAdapter:
    """
    R2 Droid with full brain, heart, and stomach integration.
    
    R2 is now an intelligent agent that:
    - Perceives through sensors (thalamus)
    - Decides via OODA loop (PFC + basal ganglia)
    - Acts through motors (cerebellum coordination)
    - Feels via heart (emotion, rhythm)
    - Energizes via stomach (power, metabolism)
    """
    
    def __init__(self, name: str = "R2"):
        self.name = name
        self.droid_id = f"{name.lower()}_unit"
        
        # Core organ systems
        print(f"[{name}] Initializing organ systems...")
        
        # STOMACH - Energy metabolism
        self.stomach = TernaryStomach()
        print(f"  ✅ Stomach: HUNGRY/SATISFIED/FULL")
        
        # HEART - Rhythm and emotion
        self.heart = TernaryHeart()
        print(f"  ✅ Heart: REST/BALANCE/ACTIVE")
        
        # BRAIN - 7-region OODA cognition
        self.brain = SevenRegionBrain()
        print(f"  ✅ Brain: 7-region OODA")
        
        # R2 Physical state
        self.sensors = R2SensorData()
        self.action_log = []
        
        # Running state
        self.running = False
        self.tick_count = 0
        self.last_heartbeat = time.time()
        
        # Connect stomach → heart → brain
        self._connect_organs()
        
        print(f"[{name}] ✅ Fully integrated: Stomach + Heart + Brain")
        print(f"[{name}] OODA Loop: Observe → Orient → Decide → Act")
        print()
    
    def _connect_organs(self):
        """Connect the three organ systems into unified mind-body."""
        # Stomach feeds energy to heart
        # Heart provides rhythm to brain
        # Brain provides safety/stress feedback to heart
        # All coordinated for unified operation
        pass  # Connection happens during tick cycle
    
    def tick(self, mission: str = "") -> Dict:
        """
        Single OODA loop cycle for R2.
        
        OODA: Observe → Orient → Decide → Act
        """
        self.tick_count += 1
        
        # === O - OBSERVE (Thalamus) ===
        # Gather sensory data
        observation = self._gather_observations(mission)
        
        # === O - ORIENT (Hippocampus + Limbic) ===
        # Process in context of memory and emotion
        # Heart provides emotional tone
        heart_beat = self.heart.beat({
            "brain_arousal": 0.5,
            "safety": 0.8,
            "stress": 0.2,
        })
        
        # Stomach provides energy level
        stomach_state = self.stomach.digest({
            "content": f"mission_{mission}",
            "complexity": 0.3,
            "nutrition": 0.5,
        })
        
        # === D - DECIDE (PFC + Basal Ganglia) ===
        # Brain processes observation with emotion/energy context
        brain_input = {
            "text": f"R2 mission: {mission}. Sensors: {observation}",
            "source": "r2_sensors",
            "energy": stomach_state.get("energy_output", 0.5),
            "emotion": heart_beat.get("emotional_tone", "neutral"),
        }
        
        decision = self.brain.tick(brain_input)
        
        # === A - ACT (Cerebellum + Motor Cortex) ===
        # Execute the decision
        action = self._execute_decision(decision)
        
        # Log the cycle
        self.action_log.append({
            "tick": self.tick_count,
            "mission": mission,
            "observation": observation,
            "heart_state": heart_beat.get("state"),
            "stomach_state": stomach_state.get("state"),
            "decision": decision.get("action"),
            "action": action,
        })
        
        return {
            "tick": self.tick_count,
            "ooda_complete": True,
            "observation": observation,
            "heart": heart_beat,
            "stomach": stomach_state,
            "decision": decision,
            "action": action,
        }
    
    def _gather_observations(self, mission: str) -> Dict:
        """Gather sensor data (simulated or real)."""
        return {
            "position": self.sensors.position,
            "dome_angle": self.sensors.dome_angle,
            "battery": self.sensors.battery,
            "obstacles": self.sensors.obstacles,
            "mission": mission,
        }
    
    def _execute_decision(self, decision: Dict) -> str:
        """Execute the decided action."""
        action_type = decision.get("action", "observe")
        
        actions = {
            "scan": self._action_scan,
            "move": self._action_move,
            "tool": self._action_tool,
            "holo": self._action_holo,
            "dome": self._action_dome,
            "observe": self._action_observe,
        }
        
        action_fn = actions.get(action_type, self._action_observe)
        return action_fn(decision)
    
    def _action_scan(self, decision: Dict) -> str:
        """Execute scan action."""
        self.sensors.dome_angle = (self.sensors.dome_angle + 45) % 360
        self.sensors.battery -= 0.5
        return f"Scanned surroundings, dome at {self.sensors.dome_angle}°"
    
    def _action_move(self, decision: Dict) -> str:
        """Execute movement."""
        direction = decision.get("metadata", {}).get("direction", [1, 0])
        self.sensors.position[0] += direction[0]
        self.sensors.position[1] += direction[1]
        self.sensors.battery -= 1.0
        return f"Moved to position {self.sensors.position}"
    
    def _action_tool(self, decision: Dict) -> str:
        """Execute tool action."""
        tool = decision.get("metadata", {}).get("tool", "scanner")
        self.sensors.tool_arm = tool
        self.sensors.battery -= 2.0
        return f"Extended {tool} arm"
    
    def _action_holo(self, decision: Dict) -> str:
        """Execute holo projection."""
        message = decision.get("metadata", {}).get("message", "Stand by")
        self.sensors.holo_active = True
        self.sensors.battery -= 3.0
        return f"Projected hologram: '{message}'"
    
    def _action_dome(self, decision: Dict) -> str:
        """Execute dome rotation."""
        angle = decision.get("metadata", {}).get("angle", 90)
        self.sensors.dome_angle = angle
        self.sensors.battery -= 0.3
        return f"Rotated dome to {angle}°"
    
    def _action_observe(self, decision: Dict) -> str:
        """Default observe action."""
        return "Observing environment"
    
    def run_mission(self, mission: str, steps: int = 5) -> List[Dict]:
        """Run a complete mission with OODA loop."""
        print(f"[{self.name}] 🚀 Starting mission: {mission}")
        print(f"[{self.name}] Organ integration: Stomach → Heart → Brain → Action")
        print()
        
        results = []
        for i in range(steps):
            result = self.tick(mission)
            results.append(result)
            
            # Print status
            heart = result["heart"]
            stomach = result["stomach"]
            action = result["action"]
            
            print(f"[Tick {result['tick']}] Heart: {heart.get('state')} | "
                  f"Stomach: {stomach.get('state')} | Action: {action[:30]}...")
            
            # Wait for heart rhythm
            time.sleep(0.5)
        
        print()
        print(f"[{self.name}] ✅ Mission complete")
        print(f"  Total ticks: {self.tick_count}")
        print(f"  Final battery: {self.sensors.battery:.1f}%")
        print(f"  Final position: {self.sensors.position}")
        
        return results
    
    def get_status(self) -> Dict:
        """Get full R2 status."""
        return {
            "name": self.name,
            "tick_count": self.tick_count,
            "battery": self.sensors.battery,
            "position": self.sensors.position,
            "dome_angle": self.sensors.dome_angle,
            "heart_state": self.heart.rhythm.state.name,
            "stomach_state": self.stomach.state.name,
            "brain_mode": "adaptive",
            "organs": ["stomach", "heart", "brain"],
        }


# Singleton for shared access
_r2_instance = None

def get_r2_brain(name: str = "R2") -> R2BrainAdapter:
    """Get or create R2 with brain integration."""
    global _r2_instance
    if _r2_instance is None:
        _r2_instance = R2BrainAdapter(name)
    return _r2_instance


if __name__ == "__main__":
    print("=" * 70)
    print("R2 DROID - FULL ORGAN INTEGRATION TEST")
    print("=" * 70)
    print()
    
    # Create R2 with full brain
    r2 = R2BrainAdapter("R2-D2")
    
    # Run test mission
    results = r2.run_mission("Hostinger deployment support", steps=10)
    
    print()
    print("Final Status:")
    print(json.dumps(r2.get_status(), indent=2))
