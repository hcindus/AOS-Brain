"""Cosmology, cosmic events, and myth generation for V3 Cosmic Engine."""
from __future__ import annotations

import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from config import COSMIC_EVENT_CHANCE, ERA_MIN_LENGTH, ERA_MAX_LENGTH


@dataclass
class CosmicEvent:
    """A cosmic event in the simulation."""
    type: str
    turn: int
    description: str
    impact: str = ""
    era: str = ""


class Cosmology:
    """Handles creation myth and overarching cosmic narrative."""
    
    def __init__(self, world: Any):
        self.world = world
        self.creation_myth: str = ""
        self.events: List[CosmicEvent] = []
        self.omens: List[str] = []
        self.prophecies: List[str] = []
    
    def generate_creation_myth(self) -> None:
        """Generate a flavorful, expandable creation myth based on world state."""
        region = self.world.get_region("Heartlands")
        climate = region.climate if hasattr(region, "climate") else "unknown"
        
        self.creation_myth = (
            f"In the primordial {climate} era, the world awoke from the silence between storms. "
            f"From the void rose the First Flame, and with it came the song of becoming."
        )
        
        # Add to world myth pool
        if hasattr(self.world, 'myth_pool'):
            self.world.myth_pool.append(self.creation_myth)
    
    def record_event(self, event_type: str, description: str, impact: str = "") -> None:
        """Record a cosmic event."""
        event = CosmicEvent(
            type=event_type,
            turn=self.world.turn if hasattr(self.world, "turn") else 0,
            description=description,
            impact=impact,
            era=getattr(self.world, 'era', 'unknown'),
        )
        self.events.append(event)
        self.world.add_event(event)
    
    def add_prophecy(self, prophecy: str) -> None:
        """Add a prophecy to the cosmic narrative."""
        self.prophecies.append(prophecy)
    
    def get_recent_events(self, count: int = 5) -> List[CosmicEvent]:
        """Get the most recent cosmic events."""
        return self.events[-count:] if len(self.events) >= count else self.events


class CosmicEvents:
    """Manages random cosmic events with proper integration."""
    
    EVENT_TYPES = ["solar_eclipse", "comet", "prophecy", "divine_sign", "void_whisper"]
    
    def __init__(self, world: Any, cosmology: Cosmology):
        self.world = world
        self.cosmology = cosmology
    
    def tick(self) -> None:
        """Called once per world tick. Low probability of major cosmic events."""
        if random.random() < COSMIC_EVENT_CHANCE:
            event_type = random.choice(self.EVENT_TYPES)
            
            descriptions = {
                "solar_eclipse": "The sun was swallowed by shadow for a full cycle.",
                "comet": "A blazing herald streaked across the heavens.",
                "prophecy": "Ancient words echoed in the dreams of the wise.",
                "divine_sign": "The stars aligned in a pattern unseen for aeons.",
                "void_whisper": "A silence fell that carried voices from beyond the veil."
            }
            
            impacts = {
                "solar_eclipse": "Morale shifted across the Heartlands.",
                "comet": "Scholars and mystics gathered to interpret the omen.",
                "prophecy": "New cults began to form in remote regions.",
                "divine_sign": "Faith surged among the faithful.",
                "void_whisper": "Some agents reported strange dreams."
            }
            
            self.cosmology.record_event(
                event_type=event_type,
                description=descriptions[event_type],
                impact=impacts[event_type]
            )
    
    def trigger_event(self, event_type: str) -> None:
        """Manually trigger a specific cosmic event."""
        if event_type in self.EVENT_TYPES:
            descriptions = {
                "solar_eclipse": "The sun was swallowed by shadow for a full cycle.",
                "comet": "A blazing herald streaked across the heavens.",
                "prophecy": "Ancient words echoed in the dreams of the wise.",
                "divine_sign": "The stars aligned in a pattern unseen for aeons.",
                "void_whisper": "A silence fell that carried voices from beyond the veil."
            }
            
            impacts = {
                "solar_eclipse": "Morale shifted across the Heartlands.",
                "comet": "Scholars and mystics gathered to interpret the omen.",
                "prophecy": "New cults began to form in remote regions.",
                "divine_sign": "Faith surged among the faithful.",
                "void_whisper": "Some agents reported strange dreams."
            }
            
            self.cosmology.record_event(
                event_type=event_type,
                description=descriptions[event_type],
                impact=impacts[event_type]
            )


class EraEngine:
    """Manages cosmic eras and their transitions."""
    
    ERAS = [
        ("dawn", "The world awakens"),
        ("golden_age", "Prosperity spreads"),
        ("trials", "Challenges arise"),
        ("twilight", "The age fades"),
        ("renewal", "A new cycle begins"),
    ]
    
    def __init__(self, world: Any):
        self.world = world
        self.era_index: int = 0
        self.era_duration: int = 0
        self.max_era_duration: int = random.randint(ERA_MIN_LENGTH, ERA_MAX_LENGTH)
        self._set_era(0)
    
    def _set_era(self, index: int) -> None:
        """Set the current era."""
        if 0 <= index < len(self.ERAS):
            self.era_index = index
            era_name, era_desc = self.ERAS[index]
            self.world.era = era_name
            if hasattr(self.world, 'era_count'):
                self.world.era_count = index
            self.era_duration = 0
            self.max_era_duration = random.randint(ERA_MIN_LENGTH, ERA_MAX_LENGTH)
    
    def tick(self) -> None:
        """Advance era timing, potentially triggering transition."""
        self.era_duration += 1
        
        if self.era_duration >= self.max_era_duration:
            self._transition_era()
    
    def _transition_era(self) -> None:
        """Transition to the next era."""
        next_index = (self.era_index + 1) % len(self.ERAS)
        old_era = self.ERAS[self.era_index][0]
        new_era = self.ERAS[next_index][0]
        
        self._set_era(next_index)
        
        # Record the transition as a cosmic event if cosmology exists
        if hasattr(self.world, 'events'):
            from core.world import WorldEvent
            self.world.events.append(WorldEvent(
                turn=self.world.turn,
                type="era_transition",
                description=f"The {old_era} fades. The {new_era} begins.",
                impact="The world shifts to a new cosmic phase."
            ))
    
    def get_era_progress(self) -> float:
        """Get current era progress (0.0 to 1.0)."""
        if self.max_era_duration > 0:
            return self.era_duration / self.max_era_duration
        return 0.0
    
    def get_era_info(self) -> Dict[str, Any]:
        """Get information about the current era."""
        era_name, era_desc = self.ERAS[self.era_index]
        return {
            "name": era_name,
            "description": era_desc,
            "duration": self.era_duration,
            "max_duration": self.max_era_duration,
            "progress": self.get_era_progress(),
        }
