"""
Neurochemistry Module
Neuromodulators that affect brain behavior.

- Dopamine: reward, motivation, learning
- Serotonin: mood, patience, stability
- Acetylcholine: attention, focus, plasticity
- Norepinephrine: alertness, threat, urgency
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class NeurochemicalState:
    """Current neurochemical levels"""
    dopamine: float = 0.0
    serotonin: float = 0.0
    acetylcholine: float = 0.0
    norepinephrine: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "dopamine": round(self.dopamine, 3),
            "serotonin": round(self.serotonin, 3),
            "acetylcholine": round(self.acetylcholine, 3),
            "norepinephrine": round(self.norepinephrine, 3),
        }


class Neurochemistry:
    """
    Manages brain neuromodulators.
    
    These chemicals modulate:
    - Learning rates (dopamine, acetylcholine)
    - Mood stability (serotonin)
    - Alertness and threat response (norepinephrine)
    """
    
    def __init__(self):
        self.state = NeurochemicalState()
        
        # Decay rates (how fast chemicals return to baseline)
        self.decay_rates = {
            "dopamine": 0.95,
            "serotonin": 0.99,
            "acetylcholine": 0.90,
            "norepinephrine": 0.93,
        }
        
    def update(self, valence: float = 0.0, novelty: float = 0.0, threat: float = 0.0):
        """
        Update neurochemical levels based on experience.
        
        Args:
            valence: -1.0 to 1.0 (negative to positive)
            novelty: 0.0 to 1.0 (familiar to novel)
            threat: 0.0 to 1.0 (safe to dangerous)
        """
        # Dopamine: reward + novelty
        self.state.dopamine += 0.5 * valence + 0.3 * novelty
        
        # Serotonin: slow baseline mood
        self.state.serotonin += 0.01 * valence - 0.001 * abs(threat)
        
        # Acetylcholine: attention to novelty
        self.state.acetylcholine = 0.5 * novelty
        
        # Norepinephrine: threat/urgency (with decay)
        self.state.norepinephrine = max(
            self.state.norepinephrine * 0.9,
            threat
        )
        
        # Apply decay and clamp
        self._apply_decay()
        self._clamp()
        
    def _apply_decay(self):
        """Apply natural decay to all chemicals"""
        self.state.dopamine *= self.decay_rates["dopamine"]
        self.state.serotonin *= self.decay_rates["serotonin"]
        self.state.acetylcholine *= self.decay_rates["acetylcholine"]
        self.state.norepinephrine *= self.decay_rates["norepinephrine"]
        
    def _clamp(self):
        """Clamp all values to [-1, 1]"""
        self.state.dopamine = max(-1.0, min(1.0, self.state.dopamine))
        self.state.serotonin = max(-1.0, min(1.0, self.state.serotonin))
        self.state.acetylcholine = max(-1.0, min(1.0, self.state.acetylcholine))
        self.state.norepinephrine = max(-1.0, min(1.0, self.state.norepinephrine))
        
    def get_learning_modulators(self) -> Dict:
        """
        Get factors to modulate learning.
        
        Returns:
            Dict with learning rate multipliers
        """
        # Dopamine boosts learning
        lr_up_boost = 1.0 + max(0, self.state.dopamine) * 2.0
        
        # Acetylcholine increases plasticity when high
        plasticity_boost = 1.0 + self.state.acetylcholine * 1.5
        
        # Serotonin smooths (reduces extremes)
        stability = 1.0 - abs(self.state.serotonin) * 0.3
        
        # Norepinephrine narrows focus under threat
        focus = 1.0 + self.state.norepinephrine * 0.5
        
        return {
            "lr_up_multiplier": lr_up_boost,
            "plasticity_multiplier": plasticity_boost,
            "stability": stability,
            "focus_multiplier": focus,
        }
        
    def get_mood(self) -> str:
        """Get current mood based on neurochemistry"""
        if self.state.serotonin > 0.5:
            return "calm_happy"
        elif self.state.serotonin < -0.5:
            return "anxious"
        elif self.state.dopamine > 0.5:
            return "motivated"
        elif self.state.norepinephrine > 0.5:
            return "alert"
        elif self.state.acetylcholine > 0.5:
            return "focused"
        return "neutral"
        
    def should_consolidate_memory(self) -> bool:
        """Check if conditions favor memory consolidation"""
        # High dopamine + low norepinephrine = good for learning
        return (self.state.dopamine > 0.2 and 
                self.state.norepinephrine < 0.3)
                
    def get_state(self) -> NeurochemicalState:
        """Get current state"""
        return self.state
        
    def reset(self):
        """Reset to baseline"""
        self.state = NeurochemicalState()


if __name__ == "__main__":
    print("Neurochemistry Module")
    print("=" * 50)
    
    neuro = Neurochemistry()
    
    # Test different experiences
    test_cases = [
        ("neutral", 0.0, 0.0, 0.0),
        ("positive_reward", 0.8, 0.2, 0.0),
        ("novel_discovery", 0.3, 0.9, 0.0),
        ("threat", -0.5, 0.3, 0.9),
        ("focused_learning", 0.2, 0.6, 0.0),
    ]
    
    for name, valence, novelty, threat in test_cases:
        neuro.reset()
        
        # Simulate multiple updates
        for _ in range(10):
            neuro.update(valence, novelty, threat)
            
        print(f"\n{name}:")
        print(f"  Input: valence={valence}, novelty={novelty}, threat={threat}")
        print(f"  State: {neuro.state.to_dict()}")
        print(f"  Mood: {neuro.get_mood()}")
        print(f"  Modulators: {neuro.get_learning_modulators()}")
        
    print("\n" + "=" * 50)
    print("Neurochemistry module ready")
