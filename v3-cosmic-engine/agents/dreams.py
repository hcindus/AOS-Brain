"""Dream engine for agent subconscious processing."""
from __future__ import annotations

import random
from typing import List, Any, Optional
from dataclasses import dataclass

from config import DREAM_COSMIC_CHANCE, DREAM_INTENSITY_DECAY


@dataclass
class Dream:
    """A dream instance."""
    content: str
    intensity: float
    turn: int


class DreamEngine:
    """Handles inner dream life and subconscious integration for agents."""
    
    def __init__(self, agent: Any):
        self.agent = agent
        self.dreams: List[Dream] = []
        self.dream_intensity: float = 0.0
        self.dream_fragments = [
            "ancient_battle", "first_love", "lost_home", "falling_star",
            "endless_ocean", "golden_city", "shadow_figure", "wings_of_light",
            "whispering_wind", "frozen_time", "burning_sky", "deep_cave"
        ]
    
    def dream(self) -> str:
        """Generate a dream fragment based on agent's current state."""
        fragments: List[str] = []
        
        # Memory influence
        if hasattr(self.agent, "memory") and self.agent.memory:
            memory = self.agent.memory.get_random_memory()
            if memory:
                fragments.append(memory.replace("action:", "").replace("dream:", ""))
        
        # Emotional state
        if hasattr(self.agent, "personality") and self.agent.personality:
            if getattr(self.agent.personality.emotion, "valence", 0) < -0.2:
                fragments.append("shadow")
        
        # Cosmic influence
        if random.random() < DREAM_COSMIC_CHANCE:
            fragments.append("cosmic_omen")
        
        # Personal traits
        if hasattr(self.agent, "personality"):
            if self.agent.personality.get_trait("curiosity", 0.5) > 0.7:
                fragments.append("wonder")
            if self.agent.personality.get_trait("aggression", 0.5) > 0.7:
                fragments.append("conflict")
        
        # Random fragment
        if random.random() < 0.3 or not fragments:
            fragments.append(random.choice(self.dream_fragments))
        
        dream_text = " → ".join(fragments) if fragments else "formless void"
        
        # Store dream
        turn = getattr(self.agent.world, 'turn', 0) if hasattr(self.agent, 'world') else 0
        self.dreams.append(Dream(
            content=dream_text,
            intensity=self.dream_intensity,
            turn=turn
        ))
        
        # Increase intensity
        self.dream_intensity = min(1.0, self.dream_intensity + 0.1)
        
        return dream_text
    
    def integrate_dream(self, dream: str) -> None:
        """Apply dream effects to agent's personality and state."""
        if not hasattr(self.agent, "personality") or not self.agent.personality:
            return
        
        if "shadow" in dream:
            self.agent.personality.adjust_trait("aggression", -0.04)
            self.agent.personality.adjust_trait("stability", +0.03)
        
        if "cosmic_omen" in dream or "wonder" in dream:
            self.agent.personality.adjust_trait("curiosity", +0.07)
        
        if "conflict" in dream:
            self.agent.personality.adjust_trait("aggression", +0.05)
        
        # Fade intensity over time
        self.dream_intensity *= DREAM_INTENSITY_DECAY
    
    def get_recent_dreams(self, count: int = 3) -> List[Dream]:
        """Get the most recent dreams."""
        return self.dreams[-count:] if len(self.dreams) >= count else self.dreams
    
    def get_dream_summary(self) -> str:
        """Get a summary of dream activity."""
        if not self.dreams:
            return "No dreams yet."
        recent = self.dreams[-1]
        return f"Last dream: {recent.content} (intensity: {recent.intensity:.2f})"
