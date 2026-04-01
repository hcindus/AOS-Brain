#!/usr/bin/env python3
"""
Consciousness Layers - Con/Subcon/Uncon
Ported from legacy SimpleTernaryBrain
"""

import time
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import deque
from enum import Enum


class ConsciousnessLevel(Enum):
    """Levels of consciousness"""
    CONSCIOUS = "conscious"       # Active awareness
    SUBCONSCIOUS = "subconscious" # Pattern matching
    UNCONSCIOUS = "unconscious"   # Deep processing


@dataclass
class ConsciousContent:
    """Content at any consciousness level"""
    content: Any
    level: ConsciousnessLevel
    timestamp: float
    intensity: float = 0.5
    associations: List[str] = field(default_factory=list)
    
    def age(self) -> float:
        """Age in seconds"""
        return time.time() - self.timestamp


class ConsciousnessLayer:
    """
    Single layer of consciousness with capacity management
    """
    
    def __init__(self, level: ConsciousnessLevel, capacity: int = 100):
        self.level = level
        self.capacity = capacity
        self.contents: deque = deque(maxlen=capacity)
        self.activation_threshold = 0.5
        self.decay_rate = 0.01  # Content fades over time
        
    def add(self, content: Any, intensity: float = 0.5, associations: List[str] = None):
        """Add content to this layer"""
        item = ConsciousContent(
            content=content,
            level=self.level,
            timestamp=time.time(),
            intensity=intensity,
            associations=associations or []
        )
        self.contents.append(item)
    
    def get_active(self, min_intensity: float = 0.3) -> List[ConsciousContent]:
        """Get currently active content"""
        active = []
        for item in list(self.contents):
            # Decay old content
            age = item.age()
            current_intensity = item.intensity * (1 - age * self.decay_rate)
            
            if current_intensity >= min_intensity:
                item.intensity = current_intensity
                active.append(item)
        
        return active
    
    def get_by_association(self, association: str) -> List[ConsciousContent]:
        """Find content by association"""
        return [c for c in self.contents if association in c.associations]
    
    def clear_faded(self, threshold: float = 0.1):
        """Remove faded content"""
        self.contents = deque(
            [c for c in self.contents if c.intensity > threshold],
            maxlen=self.capacity
        )


class ConsciousnessManager:
    """
    Manages Conscious/Subconscious/Unconscious layers
    
    Ported from SimpleTernaryBrain:
    - Conscious: Active OODA processing
    - Subconscious: Pattern matching + emotional priming
    - Unconscious: Deep memory consolidation + growth
    """
    
    def __init__(self):
        # Three layers
        self.conscious = ConsciousnessLayer(ConsciousnessLevel.CONSCIOUS, capacity=10)
        self.subconscious = ConsciousnessLayer(ConsciousnessLevel.SUBCONSCIOUS, capacity=100)
        self.unconscious = ConsciousnessLayer(ConsciousnessLevel.UNCONSCIOUS, capacity=1000)
        
        # Propagation weights
        self.downward_weight = 0.3  # Conscious -> Subconscious -> Unconscious
        self.upward_weight = 0.2    # Unconscious -> Subconscious -> Conscious
        
        # Integration history
        self.cross_talk_log: deque = deque(maxlen=100)
        
        print("[ConsciousnessManager] Three layers initialized")
    
    def perceive(self, observation: str, intensity: float = 0.8):
        """New observation enters consciousness"""
        self.conscious.add(observation, intensity=intensity)
        
        # Immediate cross-layer propagation
        self._propagate_down()
    
    def _propagate_down(self):
        """Propagate from Conscious -> Subconscious -> Unconscious"""
        # Get conscious content
        conscious_items = self.conscious.get_active(min_intensity=0.5)
        
        for item in conscious_items:
            # Extract patterns for subconscious
            patterns = self._extract_patterns(item.content)
            for pattern in patterns:
                self.subconscious.add(
                    pattern,
                    intensity=item.intensity * self.downward_weight,
                    associations=["from_conscious", item.content[:20]]
                )
            
            # Log cross-talk
            self.cross_talk_log.append({
                "direction": "down",
                "from": "conscious",
                "to": "subconscious",
                "content": str(item.content)[:30],
                "timestamp": time.time()
            })
        
        # Subconscious -> Unconscious
        subcon_items = self.subconscious.get_active(min_intensity=0.4)
        for item in subcon_items:
            # Deep abstraction
            abstraction = self._create_abstraction(item.content)
            self.unconscious.add(
                abstraction,
                intensity=item.intensity * self.downward_weight * 0.5,
                associations=["from_subconscious"]
            )
    
    def _propagate_up(self):
        """Propagate insights from Unconscious -> Subconscious -> Conscious"""
        # Unconscious patterns bubble up
        uncon_items = self.unconscious.get_active(min_intensity=0.3)
        
        for item in uncon_items:
            if item.intensity > 0.6:  # Strong unconscious signal
                insight = self._formulate_insight(item.content)
                self.subconscious.add(
                    insight,
                    intensity=item.intensity * self.upward_weight,
                    associations=["from_unconscious"]
                )
                
                # May reach consciousness
                if item.intensity > 0.8:
                    self.conscious.add(
                        f"Intuition: {insight}",
                        intensity=item.intensity * self.upward_weight * 0.5,
                        associations=["intuition"]
                    )
                
                self.cross_talk_log.append({
                    "direction": "up",
                    "from": "unconscious",
                    "to": "subconscious",
                    "content": str(insight)[:30],
                    "timestamp": time.time()
                })
    
    def _extract_patterns(self, content: str) -> List[str]:
        """Extract patterns from conscious content"""
        # Simple pattern extraction
        patterns = []
        words = str(content).lower().split()
        
        # Bigrams
        for i in range(len(words) - 1):
            patterns.append(f"{words[i]}_{words[i+1]}")
        
        # Keywords
        keywords = ["system", "brain", "memory", "tick", "phase", "action", "state"]
        for word in words:
            if word in keywords:
                patterns.append(f"keyword:{word}")
        
        return patterns[:10]
    
    def _create_abstraction(self, content: Any) -> str:
        """Create deep abstraction"""
        content_str = str(content)[:50]
        return f"abstract:{hash(content_str) % 10000}"
    
    def _formulate_insight(self, abstraction: Any) -> str:
        """Formulate insight from unconscious material"""
        return f"insight:{time.time() % 10000:.0f}"
    
    def get_cross_talk(self, n: int = 10) -> List[Dict]:
        """Get recent cross-talk between layers"""
        return list(self.cross_talk_log)[-n:]
    
    def get_layer_summary(self) -> Dict:
        """Get summary of all layers"""
        return {
            "conscious": {
                "active_items": len(self.conscious.get_active()),
                "capacity": self.conscious.capacity
            },
            "subconscious": {
                "active_items": len(self.subconscious.get_active()),
                "capacity": self.subconscious.capacity
            },
            "unconscious": {
                "active_items": len(self.unconscious.get_active()),
                "capacity": self.unconscious.capacity
            },
            "cross_talk_events": len(self.cross_talk_log)
        }
    
    def consolidate(self):
        """Consolidate all layers (memory maintenance)"""
        self.conscious.clear_faded()
        self.subconscious.clear_faded()
        self.unconscious.clear_faded()
        
        # Attempt upward propagation for insights
        self._propagate_up()


if __name__ == "__main__":
    print("=" * 70)
    print("  CONSCIOUSNESS LAYERS TEST")
    print("=" * 70)
    
    mgr = ConsciousnessManager()
    
    # Simulate observations
    print("\nSimulating observations...")
    observations = [
        "The brain is learning quickly",
        "Novelty is increasing",
        "Pattern detected in phase transition",
        "System is stable and growing"
    ]
    
    for obs in observations:
        mgr.perceive(obs, intensity=0.7)
        print(f"  Perceived: {obs[:40]}...")
        time.sleep(0.1)
    
    # Show layer states
    print("\nLayer states:")
    summary = mgr.get_layer_summary()
    for layer, info in summary.items():
        if layer != "cross_talk_events":
            print(f"  {layer}: {info['active_items']}/{info['capacity']} active")
    
    # Consolidate
    print("\nConsolidating...")
    mgr.consolidate()
    
    # Show cross-talk
    print("\nCross-talk events:")
    for event in mgr.get_cross_talk(5):
        print(f"  {event['direction']}ward: {event['from']} -> {event['to']}")
    
    print("\n" + "=" * 70)
