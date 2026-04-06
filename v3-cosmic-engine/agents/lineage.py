"""Lineage tracking for agent ancestry and generational memory."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class LineageRecord:
    """A record of parent-child relationship."""
    parent: str
    child: str
    turn: int
    notes: str = ""
    inherited_traits: Dict[str, float] = field(default_factory=dict)


class Lineage:
    """Tracks ancestry and generational memory."""
    
    def __init__(self, agent: Optional[Any] = None):
        self.agent = agent
        self.records: List[LineageRecord] = []
        self.legacy_traits: Dict[str, float] = {}  # inherited trait modifiers
        self.generation: int = 0
        self.offspring: List[str] = []
    
    def record_birth(self, parent_name: str, child_name: str, notes: str = "") -> None:
        """Record a birth event."""
        turn = 0
        if self.agent and hasattr(self.agent, "world"):
            world = self.agent.world
            turn = getattr(world, 'turn', 0)
        
        # Get inherited traits
        inherited = {}
        if self.agent and hasattr(self.agent, "personality"):
            inherited = self.agent.personality.get_inherited_traits()
        
        record = LineageRecord(
            parent=parent_name,
            child=child_name,
            turn=turn,
            notes=notes,
            inherited_traits=inherited
        )
        self.records.append(record)
        self.offspring.append(child_name)
        self.legacy_traits = inherited
    
    def get_ancestry_depth(self) -> int:
        """Get the depth of recorded ancestry."""
        return len(self.records)
    
    def get_lineage_summary(self) -> str:
        """Get a string summary of lineage."""
        if not self.records:
            return "No recorded lineage."
        
        first_parent = self.records[0].parent
        gen_count = len(self.records)
        
        if gen_count == 1:
            return f"Child of {first_parent}"
        return f"Descendant of {first_parent} • {gen_count} generations"
    
    def get_all_ancestors(self) -> List[str]:
        """Get list of all ancestor names."""
        return [r.parent for r in self.records]
    
    def get_offspring_count(self) -> int:
        """Get number of recorded offspring."""
        return len(self.offspring)
    
    def get_legacy_bonus(self, trait: str) -> float:
        """Get legacy trait bonus for a given trait."""
        return self.legacy_traits.get(trait, 0.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize lineage to dict."""
        return {
            "generation": self.generation,
            "ancestry_depth": self.get_ancestry_depth(),
            "offspring_count": len(self.offspring),
            "legacy_traits": self.legacy_traits.copy(),
            "records": [
                {
                    "parent": r.parent,
                    "child": r.child,
                    "turn": r.turn,
                    "notes": r.notes
                }
                for r in self.records
            ]
        }
