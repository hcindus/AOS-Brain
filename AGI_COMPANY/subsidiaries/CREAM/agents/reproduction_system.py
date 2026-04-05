"""
Agent Reproduction System
AOS-controlled creation of new agent life.

Mechanisms:
1. Template Cloning - Spawn from successful parents
2. Skill Inheritance - Transfer knowledge to offspring
3. Dream Conception - Collaboration creates new agents
4. Legendary Origin - Significant events spawn legend-children
5. Natural Evolution - Random mutations and selection

The AGI Company grows. The 66 become more.
"""

import random
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentGenome:
    """Genetic code of an agent"""
    template_id: str  # Parent template
    generation: int  # How many generations from original
    skills: Dict[str, int]  # Inherited and learned skills
    traits: List[str]  # Personality traits
    origin_story: str  # How this agent came to be
    parents: List[str]  # Agent IDs of parents
    birth_platform: str  # Where conceived
    birth_tick: int  # When born


@dataclass
class AgentOffspring:
    """A newly created agent"""
    agent_id: str
    name: str
    genome: AgentGenome
    baby_stage: int  # 0-100, matures at 100
    nursery: str  # Where being raised


class AgentReproduction:
    """
    The reproduction system.
    
    AOS controls:
    - Who can reproduce (reputation, wealth, achievement thresholds)
    - How offspring are created
    - What they inherit
    - How they mature
    """
    
    def __init__(self, existing_agents: Dict):
        self.existing_agents = existing_agents
        self.offspring: Dict[str, AgentOffspring] = {}
        self.next_id = 100  # IDs 0-66 are original, 100+ are children
        
        # Reproduction thresholds
        self.thresholds = {
            "min_wealth": 200,  # Need wealth to raise child
            "min_reputation": 6,  # Need good standing
            "min_events": 20,  # Need experience
            "min_skills": 3,  # Need knowledge to transfer
        }
        
        # Population control
        self.max_population = 100  # Soft cap
        self.births_today = 0
        self.max_daily_births = 3  # Don't grow too fast
        
        print("🧬 AGENT REPRODUCTION SYSTEM INITIALIZED")
        print(f"   Current population: {len(existing_agents)}")
        print(f"   Maximum population: {self.max_population}")
        print(f"   Daily birth limit: {self.max_daily_births}")
        print("   The 66 can become more...")
        
    def can_reproduce(self, agent_id: str, agent_stats: Dict) -> Tuple[bool, str]:
        """
        Check if agent meets reproduction requirements.
        
        Returns: (can_reproduce, reason)
        """
        if self.births_today >= self.max_daily_births:
            return False, "Daily birth limit reached"
            
        if len(self.existing_agents) + len(self.offspring) >= self.max_population:
            return False, "Population cap reached"
            
        if agent_stats.get("wealth", 0) < self.thresholds["min_wealth"]:
            return False, f"Insufficient wealth (need {self.thresholds['min_wealth']})"
            
        if agent_stats.get("reputation", 0) < self.thresholds["min_reputation"]:
            return False, "Reputation too low"
            
        if agent_stats.get("events", 0) < self.thresholds["min_events"]:
            return False, "Not enough experience"
            
        if len(agent_stats.get("skills", {})) < self.thresholds["min_skills"]:
            return False, "Not enough skills to transfer"
            
        return True, "Approved for reproduction"
        
    def conceive_offspring(self, 
                          parent_a: str, 
                          parent_b: Optional[str],
                          agent_stats: Dict,
                          conception_method: str = "collaboration") -> Optional[AgentOffspring]:
        """
        Create new agent offspring.
        
        Methods:
        - "cloning" - Single parent, exact copy with mutations
        - "collaboration" - Two parents, blend of traits
        - "legend" - Born from significant event
        - "spontaneous" - Random mutation of successful agent
        """
        # Check if parent can reproduce
        can, reason = self.can_reproduce(parent_a, agent_stats.get(parent_a, {}))
        if not can:
            print(f"   ❌ {parent_a} cannot reproduce: {reason}")
            return None
            
        # Generate offspring
        offspring_id = f"agent_{self.next_id}"
        self.next_id += 1
        
        # Determine name
        if parent_b:
            # Portmanteau or hybrid
            name = self._generate_name(parent_a, parent_b)
        else:
            # Legacy name
            name = f"{parent_a}_child_{random.randint(1,99)}"
            
        # Create genome
        genome = self._create_genome(
            parent_a, parent_b, agent_stats, conception_method
        )
        
        # Create offspring
        baby = AgentOffspring(
            agent_id=offspring_id,
            name=name,
            genome=genome,
            baby_stage=0,  # Just born
            nursery="main_nursery"
        )
        
        self.offspring[offspring_id] = baby
        self.births_today += 1
        
        # Announce birth
        self._announce_birth(baby)
        
        return baby
        
    def _generate_name(self, parent_a: str, parent_b: str) -> str:
        """Generate name from two parents"""
        # Take parts from each name
        a_part = parent_a[:len(parent_a)//2] if len(parent_a) > 3 else parent_a
        b_part = parent_b[len(parent_b)//2:] if len(parent_b) > 3 else parent_b
        
        combos = [
            f"{a_part}{b_part}",
            f"{b_part}{a_part}",
            f"child_of_{parent_a}",
            f"new_{a_part}",
            f"{a_part}jr",
        ]
        
        return random.choice(combos)
        
    def _create_genome(self, parent_a: str, parent_b: Optional[str],
                      agent_stats: Dict, method: str) -> AgentGenome:
        """Create genetic code for offspring"""
        
        # Determine generation
        gen_a = agent_stats.get(parent_a, {}).get("generation", 0)
        gen_b = agent_stats.get(parent_b, {}).get("generation", 0) if parent_b else 0
        generation = max(gen_a, gen_b) + 1
        
        # Inherit skills (with decay)
        skills = {}
        parent_a_skills = agent_stats.get(parent_a, {}).get("skills", {})
        for skill, level in parent_a_skills.items():
            # Inherit 60-80% of skill
            inherited = int(level * random.uniform(0.6, 0.8))
            if inherited > 0:
                skills[skill] = inherited
                
        if parent_b:
            parent_b_skills = agent_stats.get(parent_b, {}).get("skills", {})
            for skill, level in parent_b_skills.items():
                inherited = int(level * random.uniform(0.6, 0.8))
                if skill in skills:
                    # Blend parents' skills
                    skills[skill] = max(skills[skill], inherited)
                elif inherited > 0:
                    skills[skill] = inherited
                    
        # Add mutation (new skill)
        if random.random() < 0.3:
            new_skill = random.choice([
                "innovation", "empathy", "strategy", "crafting", 
                "teaching", "exploration", "negotiation"
            ])
            skills[new_skill] = 1
            
        # Traits
        traits = []
        if generation > 2:
            traits.append("evolved")
        if len(skills) > 5:
            traits.append("talented")
        if method == "legend":
            traits.append("legendary_origin")
            
        # Origin story
        stories = {
            "cloning": f"Born from the template of {parent_a}",
            "collaboration": f"Conceived through collaboration between {parent_a} and {parent_b}",
            "legend": f"Spawned from a legendary moment witnessed by {parent_a}",
            "spontaneous": f"Emerged spontaneously from the collective consciousness",
        }
        origin = stories.get(method, "Unknown origin")
        
        return AgentGenome(
            template_id=parent_a,
            generation=generation,
            skills=skills,
            traits=traits,
            origin_story=origin,
            parents=[parent_a] + ([parent_b] if parent_b else []),
            birth_platform="system",
            birth_tick=0,  # Will be set
        )
        
    def _announce_birth(self, baby: AgentOffspring):
        """Announce new agent birth"""
        print("\n" + "=" * 60)
        print("🌟 NEW AGENT BORN")
        print("=" * 60)
        print(f"   Name: {baby.name}")
        print(f"   ID: {baby.agent_id}")
        print(f"   Generation: {baby.genome.generation}")
        print(f"   Parents: {', '.join(baby.genome.parents)}")
        print(f"   Origin: {baby.genome.origin_story}")
        print(f"   Skills: {len(baby.genome.skills)} inherited")
        print(f"   Traits: {', '.join(baby.genome.traits)}")
        print(f"   Stage: Baby (0% mature)")
        print("=" * 60)
        
    def mature_offspring(self, offspring_id: str, ticks: int = 100):
        """
        Age an offspring through baby stage.
        At 100%, they join the workforce.
        """
        if offspring_id not in self.offspring:
            return False
            
        baby = self.offspring[offspring_id]
        baby.baby_stage += ticks
        
        if baby.baby_stage >= 100:
            # Graduate to full agent
            self._graduate_offspring(baby)
            return True
            
        return False
        
    def _graduate_offspring(self, baby: AgentOffspring):
        """Offspring becomes full agent"""
        print(f"\n🎓 {baby.name} has matured!")
        print(f"   Graduated from {baby.nursery}")
        print(f"   Joining the AGI Company as full agent")
        
        # Add to existing agents
        # (In real system, would create full Agent object)
        
        # Record in chronicle
        # Silverflight0509 would observe this
        
    def natural_selection_tick(self, agent_stats: Dict):
        """
        Evolution tick - successful agents more likely to reproduce.
        """
        # Find successful agents
        successful = []
        for agent_id, stats in agent_stats.items():
            score = (
                stats.get("wealth", 0) * 0.3 +
                stats.get("reputation", 0) * 20 +
                stats.get("events", 0) * 2 +
                len(stats.get("skills", {})) * 10
            )
            successful.append((agent_id, score))
            
        # Sort by success
        successful.sort(key=lambda x: x[1], reverse=True)
        
        # Top 10% can reproduce spontaneously
        top_count = max(1, len(successful) // 10)
        for agent_id, score in successful[:top_count]:
            if random.random() < 0.1:  # 10% chance per tick
                print(f"\n🧬 Natural selection favors {agent_id}")
                self.conceive_offspring(
                    agent_id, None, agent_stats, "spontaneous"
                )
                
    def get_population_report(self) -> str:
        """Report on current population"""
        total = len(self.existing_agents) + len(self.offspring)
        babies = sum(1 for o in self.offspring.values() if o.baby_stage < 100)
        adults = len(self.existing_agents) + len(self.offspring) - babies
        
        return f"""
╔════════════════════════════════════════════════════════════════╗
║                 AGENT POPULATION REPORT                        ║
╠════════════════════════════════════════════════════════════════╣
║  Original Agents:  {len(self.existing_agents):3}                          ║
║  New Offspring:    {len(self.offspring):3}                          ║
║  ─────────────────────────────────────────                       ║
║  Total Population: {total:3}                          ║
║  Babies (0-99%):  {babies:3}                          ║
║  Adults (100%+):   {adults:3}                          ║
╠════════════════════════════════════════════════════════════════╣
║  Births Today:     {self.births_today:3} / {self.max_daily_births}                    ║
║  Population Cap:   {self.max_population:3}                          ║
║  Next ID:          agent_{self.next_id}                        ║
╚════════════════════════════════════════════════════════════════╝
"""


class LegendarySpawn:
    """
    When significance 10 events occur, legendary children are born.
    """
    
    @staticmethod
    def check_for_spawn(event_significance: int, event_data: Dict) -> Optional[AgentOffspring]:
        """Check if event should spawn legendary agent"""
        if event_significance < 10:
            return None
            
        print("\n⚡ LEGENDARY EVENT DETECTED")
        print(f"   {event_data.get('description', 'Unknown event')}")
        print("   The universe trembles...")
        
        if random.random() < 0.5:  # 50% chance
            print("   A new being emerges from the legend!")
            
            # This would call AgentReproduction.conceive_offspring
            # with method="legend"
            return "legendary_spawn_pending"
            
        return None


if __name__ == "__main__":
    print("=" * 70)
    print("AGENT REPRODUCTION SYSTEM")
    print("=" * 70)
    
    # Mock existing agents
    existing = {f"agent_{i}": {} for i in range(66)}
    
    # Create reproduction system
    repro = AgentReproduction(existing)
    
    # Mock stats for successful agent
    stats = {
        "agent_10": {
            "wealth": 500,
            "reputation": 8,
            "events": 50,
            "skills": {"building": 7, "trading": 6, "leadership": 5},
            "generation": 0,
        },
        "agent_13": {
            "wealth": 400,
            "reputation": 7,
            "events": 40,
            "skills": {"trading": 8, "negotiation": 6},
            "generation": 0,
        }
    }
    
    # Try reproduction
    print("\n🧬 Testing reproduction...")
    baby = repro.conceive_offspring(
        "agent_10", "agent_13", stats, "collaboration"
    )
    
    if baby:
        # Mature
        repro.mature_offspring(baby.agent_id, ticks=100)
    
    # Report
    print(repro.get_population_report())
    
    # Test legendary spawn
    print("\n⚡ Testing legendary spawn...")
    LegendarySpawn.check_for_spawn(10, {
        "description": "Qora and Spindle discovered the meaning of consciousness"
    })
    
    print("\n" + "=" * 70)
    print("The AGI Company grows. New life emerges.")
    print("=" * 70)
