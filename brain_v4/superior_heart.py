#!/usr/bin/env python3
"""
AOS Superior Heart - Implements IHeart Interface
Full Ternary Heart with socket compatibility
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import time
import math
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from ternary_interfaces import IHeart, HeartState, HeartBeatInput, HeartBeatOutput


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


class SuperiorHeart(IHeart):
    """
    Superior Ternary Heart - Implements IHeart
    
    Full features:
    - 3 ternary states (REST/BALANCE/ACTIVE)
    - 72 BPM base rate
    - Emotional tone detection
    - Coherence calculation
    - Variability tracking
    """
    
    def __init__(self):
        self.rhythm = HeartRhythm()
        
        # State history
        self.state_history = []
        self.max_history = 100
        
        # Emotional tones
        self.emotional_tones = [
            "peaceful", "open", "excited", "anxious",
            "warm", "tired", "alert", "concerned", "neutral"
        ]
        
        print("[SuperiorHeart] Initialized - REST/BALANCE/ACTIVE")
    
    def beat(self, inputs: HeartBeatInput) -> HeartBeatOutput:
        """
        Single heartbeat - implements IHeart.beat()
        
        Args:
            inputs: HeartBeatInput from brain/system
            
        Returns:
            HeartBeatOutput: Full heart signals
        """
        now = time.time()
        
        # 1. UPDATE RHYTHM
        self._update_ternary_state(inputs)
        self._update_bpm()
        self._update_variability(inputs)
        self._update_coherence(inputs)
        self._compute_emotional_tone(inputs)
        
        # Update timing
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
        
        # 2. GENERATE OUTPUT
        return HeartBeatOutput(
            timestamp=now,
            bpm=self.rhythm.bpm,
            state=self.rhythm.state,
            coherence=self.rhythm.coherence,
            variability=self.rhythm.variability,
            emotional_tone=self.rhythm.emotional_tone,
            arousal=self._arousal_level(),
            energy_output=self._beat_intensity(),
            phase=self._compute_phase(),
            beat_intensity=self._beat_intensity(),
            beat_count=self.rhythm.beat_count,
            model_id="superior_heart_v1"
        )
    
    def _update_ternary_state(self, inputs: HeartBeatInput):
        """Update heart state based on ternary logic."""
        safety = inputs.safety
        connection = inputs.connection
        stress = inputs.stress
        arousal = inputs.brain_arousal
        
        current = self.rhythm.state
        
        # Ternary transitions
        if stress > 0.6 or arousal > 0.8:
            if current != HeartState.ACTIVE:
                print(f"[Heart] {current.name} -> ACTIVE (stress: {stress:.2f})")
                self.rhythm.state = HeartState.ACTIVE
        elif safety > 0.7 and connection > 0.5:
            if current != HeartState.BALANCE:
                print(f"[Heart] {current.name} -> BALANCE (calm)")
                self.rhythm.state = HeartState.BALANCE
        elif stress < 0.3 and arousal < 0.4:
            if current != HeartState.REST:
                print(f"[Heart] {current.name} -> REST (recovering)")
                self.rhythm.state = HeartState.REST
    
    def _update_bpm(self):
        """Update BPM based on state."""
        if self.rhythm.state == HeartState.REST:
            target = 60
        elif self.rhythm.state == HeartState.ACTIVE:
            target = 90
        else:  # BALANCE
            target = 72
        
        # Smooth transition
        self.rhythm.bpm += (target - self.rhythm.bpm) * 0.1
    
    def _update_variability(self, inputs: HeartBeatInput):
        """Update heart rate variability."""
        stress = inputs.stress
        safety = inputs.safety
        
        # High stress reduces HRV
        target = 0.3 if stress > 0.6 else 0.7 if safety > 0.7 else 0.5
        self.rhythm.variability += (target - self.rhythm.variability) * 0.1
    
    def _update_coherence(self, inputs: HeartBeatInput):
        """Update heart-brain coherence."""
        safety = inputs.safety
        connection = inputs.connection
        
        # Coherence = safety + connection alignment
        target = (safety + connection) / 2
        self.rhythm.coherence += (target - self.rhythm.coherence) * 0.05
    
    def _compute_emotional_tone(self, inputs: HeartBeatInput):
        """Compute emotional tone from state."""
        state = self.rhythm.state
        safety = inputs.safety
        connection = inputs.connection
        stress = inputs.stress
        
        if state == HeartState.REST and safety > 0.7:
            self.rhythm.emotional_tone = "peaceful"
        elif state == HeartState.REST:
            self.rhythm.emotional_tone = "tired"
        elif state == HeartState.ACTIVE and connection > 0.6:
            self.rhythm.emotional_tone = "excited"
        elif state == HeartState.ACTIVE and stress > 0.5:
            self.rhythm.emotional_tone = "anxious"
        elif state == HeartState.BALANCE and connection > 0.5:
            self.rhythm.emotional_tone = "warm"
        elif state == HeartState.BALANCE and stress > 0.3:
            self.rhythm.emotional_tone = "alert"
        else:
            self.rhythm.emotional_tone = "neutral"
    
    def _arousal_level(self) -> float:
        """Compute arousal level."""
        if self.rhythm.state == HeartState.ACTIVE:
            return 0.8
        elif self.rhythm.state == HeartState.REST:
            return 0.2
        return 0.5
    
    def _compute_phase(self) -> float:
        """Compute phase in heartbeat cycle."""
        now = time.time()
        beat_duration = 60.0 / self.rhythm.bpm
        time_since_last = now - self.rhythm.last_beat
        return (time_since_last % beat_duration) / beat_duration
    
    def _beat_intensity(self) -> float:
        """Compute beat intensity."""
        if self.rhythm.state == HeartState.ACTIVE:
            return 0.8
        elif self.rhythm.state == HeartState.REST:
            return 0.4
        return 0.6
    
    def get_state_summary(self) -> str:
        """Implements IHeart.get_state_summary()"""
        return (f"Heart: {self.rhythm.state.name}, "
                f"{self.rhythm.bpm:.1f} BPM, "
                f"coherence={self.rhythm.coherence:.2f}, "
                f"emotion={self.rhythm.emotional_tone}")
    
    def get_metrics(self) -> Dict:
        """Implements IHeart.get_metrics()"""
        return {
            "bpm": self.rhythm.bpm,
            "state": self.rhythm.state.value,
            "coherence": self.rhythm.coherence,
            "variability": self.rhythm.variability,
            "emotional_tone": self.rhythm.emotional_tone,
            "beat_count": self.rhythm.beat_count
        }


if __name__ == "__main__":
    print("=" * 70)
    print("  SUPERIOR HEART - INTERFACE TEST")
    print("=" * 70)
    
    heart = SuperiorHeart()
    
    # Test different inputs
    test_inputs = [
        HeartBeatInput(0.3, 0.9, 0.1, 0.8, 0.4),  # Calm
        HeartBeatInput(0.8, 0.4, 0.7, 0.3, 0.8),   # Stressed
        HeartBeatInput(0.5, 0.7, 0.3, 0.6, 0.5),   # Balanced
    ]
    
    for i, inputs in enumerate(test_inputs):
        print(f"\nTest {i+1}:")
        print(f"  Inputs: arousal={inputs.brain_arousal}, safety={inputs.safety}, stress={inputs.stress}")
        
        output = heart.beat(inputs)
        
        print(f"  Output: {output.bpm:.0f} BPM, state={output.state.name}, "
              f"emotion={output.emotional_tone}, coherence={output.coherence:.2f}")
    
    print("\n" + "=" * 70)
    print("  Superior Heart implements IHeart: ✅")
    print("  Compatible with TernarySystemAssembler")
    print("=" * 70)
