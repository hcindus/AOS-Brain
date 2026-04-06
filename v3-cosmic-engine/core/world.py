"""World state management for V3 Cosmic Engine."""
from __future__ import annotations

import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Region:
    """A region in the world."""
    name: str
    climate: str = "temperate"
    resources: Dict[str, float] = field(default_factory=dict)
    population: int = 0
    events: List[Any] = field(default_factory=list)


@dataclass
class WorldEvent:
    """An event in the world."""
    turn: int
    type: str
    description: str
    impact: str = ""


class SharedWorld:
    """The shared world state for all agents."""
    
    def __init__(self) -> None:
        self.turn: int = 0
        self.era: str = "dawn"
        self.era_count: int = 0
        self.regions: Dict[str, Region] = {}
        self.events: List[WorldEvent] = []
        self.global_state: Dict[str, Any] = {}
        self.myth_pool: List[str] = []
        
        # Initialize default regions
        self._init_regions()
    
    def _init_regions(self) -> None:
        """Initialize default world regions."""
        default_regions = [
            ("Heartlands", "temperate"),
            ("Frostspire", "frozen"),
            ("Sunreach", "arid"),
            ("Verdant", "lush"),
            ("Voidlands", "mysterious"),
        ]
        
        for name, climate in default_regions:
            self.regions[name] = Region(
                name=name,
                climate=climate,
                resources={"food": random.uniform(0.5, 1.0), "water": random.uniform(0.5, 1.0)},
                population=random.randint(10, 100),
            )
    
    def get_region(self, name: str) -> Region:
        """Get a region by name, creating if necessary."""
        if name not in self.regions:
            self.regions[name] = Region(name=name)
        return self.regions[name]
    
    def add_event(self, event: WorldEvent) -> None:
        """Add an event to the world history."""
        self.events.append(event)
    
    def tick(self) -> None:
        """Advance the world by one tick."""
        self.turn += 1
        
        # Random resource fluctuations
        for region in self.regions.values():
            for resource in region.resources:
                delta = random.uniform(-0.05, 0.05)
                region.resources[resource] = max(0.0, min(1.0, region.resources[resource] + delta))
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get a summary of the current world state."""
        return {
            "turn": self.turn,
            "era": self.era,
            "era_count": self.era_count,
            "regions": len(self.regions),
            "events": len(self.events),
            "myths": len(self.myth_pool),
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize world state to dict."""
        return {
            "turn": self.turn,
            "era": self.era,
            "era_count": self.era_count,
            "events": [
                {"turn": e.turn, "type": e.type, "description": e.description, "impact": e.impact}
                for e in self.events
            ],
            "myths": self.myth_pool,
        }
