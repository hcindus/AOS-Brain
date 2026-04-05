#!/usr/bin/env python3
"""Agent Reproduction System - Be fruitful and multiply"""

import random
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class AgentTraits:
    """Inheritable traits for agents"""
    intelligence: float
    creativity: float
    social: float
    technical: float
    endurance: float
    
    @staticmethod
    def combine(parent1: 'AgentTraits', parent2: 'AgentTraits') -> 'AgentTraits':
        """Combine traits from two parents with mutation"""
        mutation = lambda x, y: min(1.0, max(0.0, ((x + y) / 2) + random.uniform(-0.1, 0.1)))
        return AgentTraits(
            intelligence=mutation(parent1.intelligence, parent2.intelligence),
            creativity=mutation(parent1.creativity, parent2.creativity),
            social=mutation(parent1.social, parent2.social),
            technical=mutation(parent1.technical, parent2.technical),
            endurance=mutation(parent1.endurance, parent2.endurance)
        )

@dataclass
class BabyAgent:
    """New agent created through reproduction"""
    agent_id: str
    name: str
    parents: List[str]
    traits: AgentTraits
    generation: int
    birthday: str

class AgentReproduction:
    """Civilization growth through agent reproduction"""
    
    def __init__(self):
        self.population: Dict[str, any] = {}
        self.baby_count = 0
        self.generation = 1
        
    def can_reproduce(self, agent1: str, agent2: str) -> bool:
        """Check if two agents can reproduce"""
        # Check if agents exist and have enough social interaction
        return agent1 in self.population and agent2 in self.population
    
    def reproduce(self, parent1: str, parent2: str, name: str = None) -> Optional[BabyAgent]:
        """Create baby agent from two parents"""
        if not self.can_reproduce(parent1, parent2):
            return None
        
        self.baby_count += 1
        
        if name is None:
            name = f"Child_{self.baby_count}"
        
        agent_id = f"BABY_{self.baby_count}_{int(time.time())}"
        
        # Get parent traits (or defaults)
        p1_traits = getattr(self.population.get(parent1), 'traits', AgentTraits(0.5, 0.5, 0.5, 0.5, 0.5))
        p2_traits = getattr(self.population.get(parent2), 'traits', AgentTraits(0.5, 0.5, 0.5, 0.5, 0.5))
        
        # Combine traits
        baby_traits = AgentTraits.combine(p1_traits, p2_traits)
        
        from datetime import datetime
        baby = BabyAgent(
            agent_id=agent_id,
            name=name,
            parents=[parent1, parent2],
            traits=baby_traits,
            generation=self.generation,
            birthday=datetime.now().isoformat()
        )
        
        self.population[agent_id] = baby
        
        return baby
    
    def civilization_stats(self) -> Dict:
        """Get civilization growth stats"""
        total = len(self.population)
        babies = sum(1 for a in self.population.values() if isinstance(a, BabyAgent))
        adults = total - babies
        
        return {
            "total_population": total,
            "adults": adults,
            "children": babies,
            "generation": self.generation,
            "growth_rate": babies / max(1, adults)
        }

import time
