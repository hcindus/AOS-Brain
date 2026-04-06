"""Agent archetypes for V3 Cosmic Engine."""
from __future__ import annotations

from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class ArchetypeTraits:
    """Trait modifiers for an archetype."""
    aggression: float = 0.0
    courage: float = 0.0
    curiosity: float = 0.0
    intuition: float = 0.0
    stability: float = 0.0
    patience: float = 0.0
    adaptability: float = 0.0
    freedom: float = 0.0


ARCHETYPES: Dict[str, ArchetypeTraits] = {
    "warrior": ArchetypeTraits(
        aggression=+0.3,
        courage=+0.4,
        stability=+0.1,
    ),
    "mystic": ArchetypeTraits(
        curiosity=+0.4,
        intuition=+0.3,
        adaptability=+0.1,
    ),
    "builder": ArchetypeTraits(
        stability=+0.3,
        patience=+0.4,
        aggression=-0.1,
    ),
    "wanderer": ArchetypeTraits(
        adaptability=+0.4,
        freedom=+0.3,
        curiosity=+0.2,
    ),
}


def get_archetype(name: str) -> ArchetypeTraits:
    """Get archetype traits by name."""
    return ARCHETYPES.get(name, ArchetypeTraits())


def get_all_archetypes() -> Dict[str, ArchetypeTraits]:
    """Get all available archetypes."""
    return ARCHETYPES.copy()
