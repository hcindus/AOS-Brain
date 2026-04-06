"""Agent personality and behavior system."""
from __future__ import annotations

import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from agents.archetype import ArchetypeTraits, get_archetype


@dataclass
class EmotionState:
    """Current emotional state of an agent."""
    valence: float = 0.0  # -1.0 (negative) to +1.0 (positive)
    arousal: float = 0.5  # 0.0 (calm) to 1.0 (excited)
    dominance: float = 0.5  # 0.0 (submissive) to 1.0 (dominant)
    
    def update(self, delta_valence: float = 0.0, delta_arousal: float = 0.0) -> None:
        """Update emotional state with deltas, clamping to valid range."""
        self.valence = max(-1.0, min(1.0, self.valence + delta_valence))
        self.arousal = max(0.0, min(1.0, self.arousal + delta_arousal))


class Personality:
    """Agent personality traits and their management."""
    
    TRAIT_NAMES = ["aggression", "courage", "curiosity", "intuition", 
                   "stability", "patience", "adaptability", "freedom"]
    
    def __init__(self, archetype: Optional[str] = None):
        self.traits: Dict[str, float] = {trait: 0.5 for trait in self.TRAIT_NAMES}
        self.emotion = EmotionState()
        self.archetype = archetype
        
        # Apply archetype modifiers
        if archetype:
            self._apply_archetype(archetype)
    
    def _apply_archetype(self, archetype_name: str) -> None:
        """Apply archetype trait modifiers."""
        modifiers = get_archetype(archetype_name)
        
        for trait_name in self.TRAIT_NAMES:
            modifier = getattr(modifiers, trait_name, 0.0)
            if trait_name in self.traits:
                self.traits[trait_name] = max(0.0, min(1.0, 
                    self.traits[trait_name] + modifier))
    
    def get_trait(self, trait: str, default: float = 0.5) -> float:
        """Get a trait value."""
        return self.traits.get(trait, default)
    
    def adjust_trait(self, trait: str, delta: float) -> None:
        """Adjust a trait by delta, clamping to [0, 1]."""
        if trait in self.traits:
            self.traits[trait] = max(0.0, min(1.0, self.traits[trait] + delta))
    
    def get_inherited_traits(self) -> Dict[str, float]:
        """Get traits to pass to offspring (slightly mutated)."""
        inherited = {}
        for trait, value in self.traits.items():
            # Small random mutation
            mutation = random.uniform(-0.05, 0.05)
            inherited[trait] = max(0.0, min(1.0, value + mutation))
        return inherited
    
    def get_dominant_traits(self, n: int = 3) -> List[tuple]:
        """Get the top N dominant traits."""
        sorted_traits = sorted(self.traits.items(), key=lambda x: x[1], reverse=True)
        return sorted_traits[:n]
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize personality to dict."""
        return {
            "archetype": self.archetype,
            "traits": self.traits.copy(),
            "emotion": {
                "valence": self.emotion.valence,
                "arousal": self.emotion.arousal,
                "dominance": self.emotion.dominance,
            }
        }


class Memory:
    """Agent memory system."""
    
    def __init__(self):
        self.short_term: List[str] = []
        self.graph: Dict[str, List[str]] = {}  # Memory graph for dream influence
        self.max_short_term = 10
    
    def add(self, memory: str) -> None:
        """Add a memory."""
        self.short_term.append(memory)
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)
        
        # Update memory graph
        if memory not in self.graph:
            self.graph[memory] = []
    
    def get_recent(self, count: int = 3) -> List[str]:
        """Get recent memories."""
        return self.short_term[-count:] if len(self.short_term) >= count else self.short_term
    
    def get_random_memory(self) -> Optional[str]:
        """Get a random memory from the graph."""
        if self.graph:
            return random.choice(list(self.graph.keys()))
        return None


class Agent:
    """A cosmic agent with personality, dreams, and lineage."""
    
    def __init__(self, name: str, world: Any):
        self.name = name
        self.world = world
        self.active: bool = True
        
        # Core systems
        self.archetype: Optional[str] = None
        self.personality = Personality()
        self.memory = Memory()
        
        # Attached cosmic systems (set externally)
        self.dream_engine: Optional[Any] = None
        self.lineage: Optional[Any] = None
        
        # State
        self.age: int = 0
        self.energy: float = 1.0
        self.location: str = "Heartlands"
    
    def tick(self) -> None:
        """Execute one agent tick."""
        self.age += 1
        
        # Dream processing
        if self.dream_engine and random.random() < 0.1:  # 10% chance to dream
            dream = self.dream_engine.dream()
            self.dream_engine.integrate_dream(dream)
            self.memory.add(f"dream:{dream}")
        
        # Energy decay/recovery
        self.energy = max(0.0, min(1.0, self.energy - 0.01 + random.uniform(0, 0.02)))
        
        # Random action based on personality
        if random.random() < 0.05:  # 5% chance of notable action
            self._perform_action()
    
    def _perform_action(self) -> None:
        """Perform a random action based on personality."""
        actions = []
        
        if self.personality.get_trait("curiosity") > 0.6:
            actions.append("explores")
        if self.personality.get_trait("aggression") > 0.6:
            actions.append("challenges")
        if self.personality.get_trait("stability") > 0.6:
            actions.append("builds")
        
        if actions:
            action = random.choice(actions)
            self.memory.add(f"action:{action}")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current agent state."""
        return {
            "name": self.name,
            "archetype": self.archetype,
            "age": self.age,
            "energy": self.energy,
            "location": self.location,
            "active": self.active,
        }
    
    def __repr__(self) -> str:
        return f"Agent({self.name}, archetype={self.archetype})"
