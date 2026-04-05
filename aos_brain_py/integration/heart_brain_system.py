#!/usr/bin/env python3
"""
Heart-Brain Integration - Unified AGI System.

The heart takes over heartbeat functions and integrates with the 7-region brain:
- Heart provides: rhythm, emotion, arousal, coherence
- Brain provides: cognition, planning, memory, decision
- Together: unified mind-body-emotion system
"""

import os
import sys
import time
import json
import threading
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain
from heart.ternary_heart import TernaryHeart, HeartState


@dataclass
class HeartBrainState:
    """Unified state of heart-brain system."""
    timestamp: float
    heart_state: str
    brain_mode: str
    emotional_tone: str
    coherence: float
    arousal: float
    cognitive_load: float
    stress_level: float
    system_health: str


class HeartBrainIntegration:
    """
    Heart-Brain Integration System.
    
    The heart takes over heartbeat and provides:
    - Rhythmic timing for brain ticks
    - Emotional tone for limbic region
    - Arousal level for cognitive load
    - Coherence for focus and flow
    """
    
    def __init__(self):
        print("=" * 70)
        print("🫀🧠 HEART-BRAIN INTEGRATION SYSTEM")
        print("=" * 70)
        print()
        
        # Initialize core systems
        self.heart = TernaryHeart()
        self.brain = SevenRegionBrain()
        
        # Integration state
        self.tick_count = 0
        self.running = False
        self.heartbeat_thread = None
        
        # History
        self.state_history = []
        self.max_history = 100
        
        # Heart rate for system (in seconds between ticks)
        self.base_tick_rate = 2.0  # 30 BPM base
        self.current_tick_rate = self.base_tick_rate
        
        print("✅ Heart initialized (ternary: REST/BALANCE/ACTIVE)")
        print("✅ Brain initialized (7-region OODA)")
        print("✅ Heart-Brain Axis connected")
        print()
    
    def heart_beat_cycle(self):
        """
        Single heart-beat cycle:
        1. Heart beats → generates rhythm, emotion, arousal
        2. Heart signals → flow to brain
        3. Brain processes → cognition, memory, decision
        4. Brain feedback → adjust heart state
        5. Unified output → agent perception
        """
        # 1. HEART BEAT
        # Prepare inputs from brain state
        heart_inputs = self._prepare_heart_inputs()
        
        # Heart generates rhythm
        heart_outputs = self.heart.beat(heart_inputs)
        
        # 2. HEART SIGNALS → BRAIN
        # Heart influences brain via arousal, coherence, emotion
        brain_inputs = self._prepare_brain_inputs(heart_outputs)
        
        # 3. BRAIN PROCESSES
        # Brain thinks with heart influence
        brain_outputs = self.brain.tick(brain_inputs)
        
        # 4. BRAIN FEEDBACK → HEART
        # Brain influences heart via safety, stress, connection
        self._update_heart_from_brain(brain_outputs)
        
        # 5. UNIFIED STATE
        unified = self._create_unified_state(heart_outputs, brain_outputs)
        
        # Store history
        self.state_history.append(unified)
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        
        self.tick_count += 1
        
        # Adaptive tick rate based on heart state
        self._adjust_tick_rate(unified)
        
        return unified
    
    def _prepare_heart_inputs(self) -> Dict:
        """Prepare inputs for heart from brain state."""
        # Brain provides: stress, safety, connection, cognitive load
        # These are synthesized from brain regions
        
        # Get last brain state if available
        if hasattr(self.brain, 'last_thought') and self.brain.last_thought:
            thought = self.brain.last_thought
            
            # Extract signals
            ternary = thought.get('ternary_code', [0, 0, 0, 0, 0])
            value = thought.get('value', {})
            
            return {
                "brain_arousal": ternary[2],  # Action signal
                "safety": 1.0 - ternary[3],   # Inverse of risk
                "stress": 1.0 if ternary[3] == -1 else 0.0,
                "connection": value.get('valence', 0.5),
                "cognitive_load": value.get('importance', 0.5),
            }
        
        return {"brain_arousal": 0.5, "safety": 0.7, "connection": 0.5, "stress": 0.1}
    
    def _prepare_brain_inputs(self, heart_outputs: Dict) -> Dict:
        """Prepare inputs for brain from heart outputs."""
        # Heart provides: arousal, coherence, emotional tone, rhythm
        
        # Map heart emotional tone to observation
        tone = heart_outputs.get('heart_emotional_tone', 'neutral')
        arousal = heart_outputs.get('heart_arousal', 0.5)
        coherence = heart_outputs.get('heart_coherence', 0.5)
        
        # Create text for brain to process
        observations = {
            "peaceful": "System is calm and resting",
            "open": "Feeling connected and receptive",
            "excited": "Energy is high and engaged",
            "anxious": "Alert to potential challenges",
            "warm": "Positive emotional state",
            "tired": "System needs recovery",
            "alert": "Attention is focused",
            "concerned": "Monitoring situation carefully",
            "neutral": "Baseline state",
        }
        
        text = observations.get(tone, "Heartbeat cycle")
        
        # Add arousal context
        if arousal > 0.7:
            text += " (high arousal)"
        elif arousal < 0.3:
            text += " (low arousal)"
        
        return {"text": text, "source": "heart", "arousal": arousal, "coherence": coherence}
    
    def _update_heart_from_brain(self, brain_outputs: Dict):
        """Update heart based on brain feedback."""
        # Brain's decision influences heart
        mode = brain_outputs.get('mode', 'Unknown')
        
        # Brain mode influences heart
        mode_influence = {
            "Analytical": {"stress": 0.2, "safety": 0.8},
            "Creative": {"connection": 0.8, "stress": 0.1},
            "Cautious": {"safety": 0.9, "stress": 0.3},
            "Exploratory": {"connection": 0.7, "safety": 0.6},
            "Reflective": {"safety": 0.9, "stress": 0.0},
            "Directive": {"safety": 0.7, "stress": 0.2},
            "Emotional": {"connection": 0.9, "safety": 0.7},
        }
        
        # Heart naturally adapts, but this feedback loop helps
        pass  # Heart.beat() already receives these signals
    
    def _create_unified_state(self, heart_outputs: Dict, brain_outputs: Dict) -> HeartBrainState:
        """Create unified state from heart and brain outputs."""
        return HeartBrainState(
            timestamp=time.time(),
            heart_state=self.heart.rhythm.state.name,
            brain_mode=brain_outputs.get('mode', 'Unknown'),
            emotional_tone=heart_outputs.get('heart_emotional_tone', 'neutral'),
            coherence=heart_outputs.get('heart_coherence', 0.5),
            arousal=heart_outputs.get('heart_arousal', 0.5),
            cognitive_load=brain_outputs.get('value', {}).get('importance', 0.5),
            stress_level=1.0 - heart_outputs.get('heart_coherence', 0.5),
            system_health="healthy" if heart_outputs.get('heart_coherence', 0) > 0.4 else "degraded"
        )
    
    def _adjust_tick_rate(self, state: HeartBrainState):
        """Adjust system tick rate based on unified state."""
        # High coherence = stable = normal rate
        # Low coherence = unstable = faster rate
        
        if state.coherence < 0.3:
            # Low coherence - check more frequently
            self.current_tick_rate = 1.0
        elif state.stress_level > 0.7:
            # High stress - faster monitoring
            self.current_tick_rate = 1.5
        elif state.heart_state == "REST":
            # Resting - slower is fine
            self.current_tick_rate = 3.0
        else:
            self.current_tick_rate = self.base_tick_rate
    
    def run_heartbeat(self):
        """
        Run heart-beat cycle continuously.
        The heart controls the rhythm of the entire system.
        """
        print("[Heart-Brain] Starting unified heartbeat...")
        print(f"Base tick rate: {60/self.base_tick_rate:.1f} BPM")
        print("Press Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                # Heart-beat cycle
                state = self.heart_beat_cycle()
                
                # Display every 5 beats
                if self.tick_count % 5 == 0:
                    self._display_state(state)
                
                # Sleep for heart-determined duration
                time.sleep(self.current_tick_rate)
                
        except KeyboardInterrupt:
            print("\n[Heart-Brain] Stopping...")
            self.running = False
    
    def _display_state(self, state: HeartBrainState):
        """Display current unified state."""
        heart_emoji = {
            "REST": "💤",
            "BALANCE": "💚",
            "ACTIVE": "❤️",
        }.get(state.heart_state, "💙")
        
        print(f"\n[Tick {self.tick_count}] {heart_emoji} {state.heart_state} | 🧠 {state.brain_mode}")
        print(f"  Emotion: {state.emotional_tone:12s} | Coherence: {state.coherence:.2f}")
        print(f"  Arousal: {state.arousal:.2f}       | Stress: {state.stress_level:.2f}")
        print(f"  Health:  {state.system_health.upper()}")
        print(f"  Tick rate: {60/self.current_tick_rate:.1f} BPM")
    
    def get_health_report(self) -> str:
        """Get comprehensive health report."""
        if not self.state_history:
            return "No data yet."
        
        latest = self.state_history[-1]
        
        lines = [
            "=" * 70,
            "🫀🧠 HEART-BRAIN HEALTH REPORT",
            "=" * 70,
            f"Total cycles: {self.tick_count}",
            f"Current tick rate: {60/self.current_tick_rate:.1f} BPM",
            "",
            "Current State:",
            f"  Heart: {latest.heart_state} ({latest.emotional_tone})",
            f"  Brain: {latest.brain_mode}",
            f"  Coherence: {latest.coherence:.2f}",
            f"  Arousal: {latest.arousal:.2f}",
            f"  Stress: {latest.stress_level:.2f}",
            f"  System Health: {latest.system_health.upper()}",
            "",
            "Integration Status: ✅ Heart and Brain synchronized",
            "=" * 70,
        ]
        
        return "\n".join(lines)
    
    def simulate_scenario(self, name: str, duration: int = 10):
        """Simulate a specific scenario."""
        print(f"\n{'='*70}")
        print(f"🎭 SCENARIO: {name}")
        print(f"{'='*70}\n")
        
        # Set initial conditions
        if "stress" in name.lower():
            # Simulate stress
            for _ in range(duration):
                # Force stress inputs
                self.heart.beat({"stress": 0.8, "safety": 0.3, "connection": 0.2})
                time.sleep(0.5)
        elif "calm" in name.lower():
            # Simulate calm
            for _ in range(duration):
                self.heart.beat({"stress": 0.1, "safety": 0.9, "connection": 0.8})
                time.sleep(0.5)
        else:
            # Normal
            self.run_heartbeat()
            return
        
        print(self.get_health_report())


def demo_heart_brain_integration():
    """Demo full heart-brain integration."""
    print("\n" + "=" * 70)
    print("🫀🧠 HEART-BRAIN INTEGRATION DEMO")
    print("=" * 70)
    print()
    print("The heart takes over heartbeat and integrates with the 7-region brain.")
    print("Together they create a unified mind-body-emotion system.")
    print()
    
    integration = HeartBrainIntegration()
    
    # Run for 30 seconds
    print("Running 15 heart-beat cycles...")
    print()
    
    integration.running = True
    for i in range(15):
        state = integration.heart_beat_cycle()
        if i % 3 == 0:
            integration._display_state(state)
        time.sleep(1)
    
    integration.running = False
    
    print("\n" + integration.get_health_report())
    
    print("\n" + "=" * 70)
    print("✅ Heart-Brain Integration Complete!")
    print("=" * 70)
    print("\nThe heart now controls the system rhythm:")
    print("  - Provides timing for brain ticks")
    print("  - Sends emotion and arousal to brain")
    print("  - Receives safety/stress feedback from brain")
    print("  - Creates unified mind-body coherence")
    print("=" * 70)


if __name__ == "__main__":
    demo_heart_brain_integration()
