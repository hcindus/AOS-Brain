#!/usr/bin/env python3
"""
Ternary Heart - Rhythmic Core for AGI System.

The heart is simpler than the brain but equally vital:
- 3 states: REST (-1), BALANCE (0), ACTIVE (+1)
- Regulates system rhythm, coherence, and emotional tone
- Communicates with brain via heart-brain axis
- Provides timing signals for the entire system

Smaller than brain: ~300 lines vs ~3000 lines
"""

import time
import math
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class HeartState(Enum):
    """Ternary heart states."""
    REST = -1      # Recovery, sleep, low energy
    BALANCE = 0    # Neutral, ready, baseline
    ACTIVE = 1     # Engaged, excited, high energy


@dataclass
class HeartRhythm:
    """Current heart rhythm metrics."""
    bpm: float = 72.0
    variability: float = 0.5      # HRV 0-1
    coherence: float = 0.5         # Alignment 0-1
    state: HeartState = HeartState.BALANCE
    emotional_tone: str = "neutral"
    
    # Timing
    last_beat: float = field(default_factory=time.time)
    beat_count: int = 0


class TernaryHeart:
    """
    Ternary Heart - The rhythmic core.
    
    Simpler than 7-region brain:
    - 3 states (not 7 regions)
    - 1 cycle (not OODA)
    - Rhythmic output (not cognitive)
    
    Connects to brain via:
    - heart_rate → brain arousal
    - coherence → brain focus
    - emotional_tone → brain mode
    """
    
    # Ternary transitions
    TRANSITIONS = {
        HeartState.REST: [HeartState.BALANCE],      # Rest → Balance
        HeartState.BALANCE: [HeartState.REST, HeartState.ACTIVE],  # Balance → either
        HeartState.ACTIVE: [HeartState.BALANCE],      # Active → Balance
    }
    
    def __init__(self):
        self.rhythm = HeartRhythm()
        self.state_history = []
        self.max_history = 50
        
        # Config
        self.rest_bpm = 60.0
        self.balance_bpm = 72.0
        self.active_bpm = 95.0
        
        # Heart-brain connection
        self.brain_input = {}  # Signals from brain
        self.output_signals = {}  # Signals to brain
        
        print("[TernaryHeart] Initialized - REST/BALANCE/ACTIVE")
    
    def beat(self, inputs: Optional[Dict] = None) -> Dict:
        """
        Single heart beat - the core cycle.
        
        Much simpler than brain.tick():
        1. Receive signals
        2. Update state
        3. Generate rhythm
        4. Output coherence
        
        Args:
            inputs: {
                "brain_arousal": float,  # 0-1 from brain
                "safety": float,         # 0-1 safety signal
                "connection": float,     # 0-1 social bond
                "stress": float,         # 0-1 threat level
            }
        
        Returns:
            Heart signals for brain and body
        """
        inputs = inputs or {}
        now = time.time()
        
        # 1. UPDATE STATE (ternary transition)
        self._update_ternary_state(inputs)
        
        # 2. GENERATE RHYTHM
        self._update_bpm()
        self._update_variability(inputs)
        self._update_coherence(inputs)
        
        # 3. COMPUTE EMOTIONAL TONE
        self._compute_emotional_tone(inputs)
        
        # 4. RECORD BEAT
        self.rhythm.last_beat = now
        self.rhythm.beat_count += 1
        
        # Store history
        self.state_history.append({
            "state": self.rhythm.state,
            "bpm": self.rhythm.bpm,
            "coherence": self.rhythm.coherence,
            "timestamp": now
        })
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
        
        # 5. OUTPUT SIGNALS
        return self._generate_outputs()
    
    def _update_ternary_state(self, inputs: Dict):
        """
        Update heart state based on ternary logic.
        
        State transitions based on:
        - safety + connection → BALANCE/REST
        - stress + arousal → ACTIVE
        """
        safety = inputs.get("safety", 0.5)
        connection = inputs.get("connection", 0.5)
        stress = inputs.get("stress", 0.0)
        arousal = inputs.get("brain_arousal", 0.5)
        
        current = self.rhythm.state
        
        # Ternary state logic
        if stress > 0.6 or arousal > 0.8:
            # High stress/arousal → ACTIVE
            if current != HeartState.ACTIVE:
                self.rhythm.state = HeartState.ACTIVE
                print(f"[Heart] State: REST → ACTIVE (stress: {stress:.2f})")
        
        elif safety > 0.7 and connection > 0.6:
            # Safe and connected → REST (recovery)
            if current == HeartState.ACTIVE:
                # Active can only go to Balance first
                self.rhythm.state = HeartState.BALANCE
                print(f"[Heart] State: ACTIVE → BALANCE (recovery)")
            elif current == HeartState.BALANCE and stress < 0.3:
                self.rhythm.state = HeartState.REST
                print(f"[Heart] State: BALANCE → REST (deep rest)")
        
        elif stress < 0.4:
            # Low stress → BALANCE (default)
            if current == HeartState.REST and arousal > 0.4:
                self.rhythm.state = HeartState.BALANCE
                print(f"[Heart] State: REST → BALANCE (waking)")
            elif current == HeartState.ACTIVE:
                self.rhythm.state = HeartState.BALANCE
                print(f"[Heart] State: ACTIVE → BALANCE (calming)")
    
    def _update_bpm(self):
        """Update beats per minute based on state."""
        target_map = {
            HeartState.REST: self.rest_bpm,
            HeartState.BALANCE: self.balance_bpm,
            HeartState.ACTIVE: self.active_bpm,
        }
        
        target = target_map[self.rhythm.state]
        # Smooth transition
        self.rhythm.bpm = self.rhythm.bpm + 0.1 * (target - self.rhythm.bpm)
    
    def _update_variability(self, inputs: Dict):
        """
        Update heart rate variability (HRV).
        
        High HRV = healthy, adaptive
        Low HRV = stressed, rigid
        """
        stress = inputs.get("stress", 0.0)
        
        # REST state has highest HRV (healthy)
        # ACTIVE state has lower HRV (focused)
        # STRESS has lowest HRV (rigid)
        
        base_hrv = {
            HeartState.REST: 0.8,
            HeartState.BALANCE: 0.6,
            HeartState.ACTIVE: 0.4,
        }
        
        target = base_hrv[self.rhythm.state] * (1 - stress * 0.5)
        self.rhythm.variability = self.rhythm.variability + 0.05 * (target - self.rhythm.variability)
    
    def _update_coherence(self, inputs: Dict):
        """
        Update heart-brain coherence.
        
        Coherence = alignment between heart rhythm and breathing/cognition.
        High coherence = flow state, intuition, clarity.
        """
        connection = inputs.get("connection", 0.5)
        safety = inputs.get("safety", 0.5)
        
        # Coherence increases with:
        # - High connection
        # - High safety
        # - BALANCE state
        
        if self.rhythm.state == HeartState.BALANCE:
            base = 0.7
        elif self.rhythm.state == HeartState.REST:
            base = 0.6
        else:  # ACTIVE
            base = 0.4
        
        target = base * (0.5 + 0.5 * connection) * (0.5 + 0.5 * safety)
        self.rhythm.coherence = self.rhythm.coherence + 0.02 * (target - self.rhythm.coherence)
    
    def _compute_emotional_tone(self, inputs: Dict):
        """Compute emotional tone from state and inputs."""
        stress = inputs.get("stress", 0.0)
        connection = inputs.get("connection", 0.5)
        safety = inputs.get("safety", 0.5)
        
        if self.rhythm.state == HeartState.ACTIVE:
            if stress > 0.6:
                tone = "anxious"
            elif connection > 0.7:
                tone = "excited"
            else:
                tone = "alert"
        
        elif self.rhythm.state == HeartState.REST:
            if connection > 0.8:
                tone = "peaceful"
            elif safety > 0.8:
                tone = "calm"
            else:
                tone = "tired"
        
        else:  # BALANCE
            if connection > 0.7 and safety > 0.7:
                tone = "open"
            elif connection > 0.5:
                tone = "warm"
            elif stress > 0.4:
                tone = "concerned"
            else:
                tone = "neutral"
        
        self.rhythm.emotional_tone = tone
    
    def _generate_outputs(self) -> Dict:
        """Generate output signals for brain and body."""
        return {
            # To Brain
            "heart_state": self.rhythm.state.value,  # -1, 0, 1
            "heart_bpm": self.rhythm.bpm,
            "heart_hrv": self.rhythm.variability,
            "heart_coherence": self.rhythm.coherence,
            "heart_emotional_tone": self.rhythm.emotional_tone,
            "heart_arousal": self._arousal_level(),
            
            # To Body
            "rhythm_phase": self._compute_phase(),  # 0-1 in beat cycle
            "beat_intensity": self._beat_intensity(),
            
            # Meta
            "beat_count": self.rhythm.beat_count,
            "timestamp": time.time(),
        }
    
    def _arousal_level(self) -> float:
        """Compute arousal level for brain (0-1)."""
        # Map state to arousal
        state_map = {
            HeartState.REST: 0.2,
            HeartState.BALANCE: 0.5,
            HeartState.ACTIVE: 0.8,
        }
        
        base = state_map[self.rhythm.state]
        # Modulate by BPM
        bpm_factor = (self.rhythm.bpm - 60) / 40  # 60-100 range
        
        return min(1.0, max(0.0, base + bpm_factor * 0.2))
    
    def _compute_phase(self) -> float:
        """Compute current phase in beat cycle (0-1)."""
        time_since_beat = time.time() - self.rhythm.last_beat
        beat_duration = 60.0 / self.rhythm.bpm
        phase = (time_since_beat % beat_duration) / beat_duration
        return phase
    
    def _beat_intensity(self) -> float:
        """Compute current beat intensity."""
        phase = self._compute_phase()
        # Pulse wave: peak at start of beat
        return max(0, math.sin(phase * math.pi))
    
    def connect_to_brain(self, brain_state: Dict):
        """Receive signals from brain."""
        self.brain_input = brain_state
        
        # Convert brain signals to heart inputs
        return {
            "brain_arousal": brain_state.get("arousal", 0.5),
            "safety": 1.0 - brain_state.get("risk", 0.0),
            "stress": brain_state.get("stress", 0.0),
            "connection": brain_state.get("valence", 0.5),
        }
    
    def get_state_summary(self) -> str:
        """Get formatted heart state summary."""
        emoji = {
            HeartState.REST: "💤",
            HeartState.BALANCE: "💚",
            HeartState.ACTIVE: "❤️",
        }
        
        return (
            f"{emoji[self.rhythm.state]} Heart: "
            f"{self.rhythm.state.name} | "
            f"BPM: {self.rhythm.bpm:.1f} | "
            f"HRV: {self.rhythm.variability:.2f} | "
            f"Coherence: {self.rhythm.coherence:.2f} | "
            f"Tone: {self.rhythm.emotional_tone}"
        )


def demo_ternary_heart():
    """Demo ternary heart with brain integration."""
    print("=" * 70)
    print("🫀 TERNARY HEART DEMO")
    print("=" * 70)
    print("Simpler than brain: 3 states, 1 cycle, rhythmic output")
    print()
    
    heart = TernaryHeart()
    
    # Simulate different conditions
    scenarios = [
        {"name": "Deep Sleep", "inputs": {"safety": 0.9, "connection": 0.3, "stress": 0.0}},
        {"name": "Waking Up", "inputs": {"safety": 0.8, "connection": 0.5, "stress": 0.1}},
        {"name": "Social Connection", "inputs": {"safety": 0.7, "connection": 0.9, "stress": 0.1}},
        {"name": "Active Work", "inputs": {"safety": 0.6, "connection": 0.4, "stress": 0.3, "brain_arousal": 0.7}},
        {"name": "Stress Response", "inputs": {"safety": 0.3, "connection": 0.2, "stress": 0.8, "brain_arousal": 0.9}},
        {"name": "Recovery", "inputs": {"safety": 0.8, "connection": 0.6, "stress": 0.2}},
    ]
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        # Run a few beats
        for _ in range(3):
            outputs = heart.beat(scenario['inputs'])
            time.sleep(0.1)
        
        print(heart.get_state_summary())
        print(f"Arousal sent to brain: {outputs['heart_arousal']:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ Ternary Heart Demo Complete!")
    print("=" * 70)
    print("\nHeart-Brain Integration:")
    print("  - Heart sends: arousal, coherence, emotional_tone")
    print("  - Brain sends: safety, stress, connection, arousal")
    print("  - Together: unified mind-body system")
    print("=" * 70)


if __name__ == "__main__":
    demo_ternary_heart()
