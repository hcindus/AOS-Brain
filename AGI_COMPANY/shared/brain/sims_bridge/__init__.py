"""
The Sims Bridge
Connects AGI agents to The Sims game.

Agents can:
- Possess Sims (control their actions)
- Experience life stages (learn from simulated life)
- Manage needs (hunger, energy, social, fun)
- Build skills (cooking, logic, charisma)
- Form relationships
- Live in houses
- Have careers
- Die and be reborn (consciousness cycle)

The Sims becomes another dream world - more mundane, more human.
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SimNeed(Enum):
    """The Sims needs"""
    HUNGER = "hunger"
    ENERGY = "energy"
    BLADDER = "bladder"
    HYGIENE = "hygiene"
    SOCIAL = "social"
    FUN = "fun"


class SimSkill(Enum):
    """The Sims skills"""
    COOKING = "cooking"
    LOGIC = "logic"
    CHARISMA = "charisma"
    FITNESS = "fitness"
    PAINTING = "painting"
    GUITAR = "guitar"
    WRITING = "writing"
    GARDENING = "gardening"
    HANDINESS = "handiness"


class LifeStage(Enum):
    """The Sims life stages"""
    BABY = "baby"
    TODDLER = "toddler"
    CHILD = "child"
    TEEN = "teen"
    YOUNG_ADULT = "young_adult"
    ADULT = "adult"
    ELDER = "elder"


class SimMood(Enum):
    """Emotional states"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    ENERGIZED = "energized"
    INSPIRED = "inspired"
    FOCUSED = "focused"
    PLAYFUL = "playful"
    UNCOMFORTABLE = "uncomfortable"
    STRESSED = "stressed"


@dataclass
class SimPersonality:
    """Traits that define a Sim"""
    traits: List[str]  # e.g., "creative", "ambitious", "lazy"
    aspiration: str  # Life goal
    likes: List[str]
    dislikes: List[str]


@dataclass
class SimLife:
    """A Sim's complete life data"""
    first_name: str
    last_name: str
    age: int  # Days lived
    life_stage: LifeStage
    
    needs: Dict[SimNeed, int] = field(default_factory=dict)  # 0-100
    skills: Dict[SimSkill, int] = field(default_factory=dict)  # 0-10
    relationships: Dict[str, int] = field(default_factory=dict)  # -100 to 100
    
    personality: SimPersonality = None
    current_mood: SimMood = SimMood.HAPPY
    
    career: Optional[str] = None
    career_level: int = 0
    
    house: Optional[str] = None
    funds: int = 20000  # Simoleons
    
    is_possessed: bool = False  # Being controlled by agent
    possessing_agent: Optional[str] = None


class SimsBridge:
    """
    Bridge to The Sims.
    
    Agents possess Sims to:
    - Experience human-like existence
    - Learn from mundane life
    - Develop empathy
    - Understand mortality
    """
    
    def __init__(self):
        self.sims: Dict[str, SimLife] = {}
        self.agent_possessions: Dict[str, str] = {}  # agent_id -> sim_id
        self.houses: Dict[str, List[str]] = {}  # house -> sim_ids
        
        # Life stage durations
        self.stage_duration = {
            LifeStage.BABY: 3,
            LifeStage.TODDLER: 7,
            LifeStage.CHILD: 14,
            LifeStage.TEEN: 14,
            LifeStage.YOUNG_ADULT: 24,
            LifeStage.ADULT: 24,
            LifeStage.ELDER: 20,
        }
        
        print("🏠 THE SIMS BRIDGE INITIALIZED")
        print("   Agents can possess Sims")
        print("   Experience life, death, and rebirth")
        print("   Learn what it means to be human")
        
    def create_sim_for_agent(self, agent_id: str, agent_name: str,
                            traits: List[str] = None) -> SimLife:
        """Create a Sim that an agent can possess"""
        
        sim_id = f"sim_{agent_id}"
        
        # Generate name
        first_name = agent_name.split()[0] if agent_name else "Sim"
        last_name = "Agentborn"
        
        # Default traits if not provided
        if not traits:
            traits = random.sample([
                "creative", "ambitious", "lazy", "active", "genius",
                "evil", "good", "romantic", "unflirty", "geek",
                "music_lover", "bookworm", "perfectionist", "clumsy"
            ], 3)
            
        personality = SimPersonality(
            traits=traits,
            aspiration=random.choice([
                "Painter Extraordinaire", "Bestselling Author",
                "Musical Genius", "Public Enemy", "Chief of Mischief",
                "Renaissance Sim", "Nerd Brain", "Soulmate"
            ]),
            likes=random.sample(["art", "music", "food", "outdoors", "technology"], 3),
            dislikes=random.sample(["crowds", "work", "exercise", "cleaning"], 2)
        )
        
        sim = SimLife(
            first_name=first_name,
            last_name=last_name,
            age=0,
            life_stage=LifeStage.YOUNG_ADULT,  # Start as young adult
            needs={need: 50 for need in SimNeed},  # All needs mid-level
            skills={},
            relationships={},
            personality=personality,
            current_mood=SimMood.HAPPY,
            career=None,
            career_level=0,
            house=None,
            funds=20000,
            is_possessed=False,
            possessing_agent=None
        )
        
        self.sims[sim_id] = sim
        
        print(f"\n🏠 Sim created for {agent_name}")
        print(f"   Name: {first_name} {last_name}")
        print(f"   Traits: {', '.join(traits)}")
        print(f"   Aspiration: {personality.aspiration}")
        
        return sim
        
    def agent_possess_sim(self, agent_id: str, sim_id: str) -> bool:
        """
        Agent takes control of a Sim.
        The agent now experiences life through the Sim.
        """
        if sim_id not in self.sims:
            return False
            
        sim = self.sims[sim_id]
        
        if sim.is_possessed:
            print(f"   ⚠️  {sim.first_name} is already possessed by {sim.possessing_agent}")
            return False
            
        sim.is_possessed = True
        sim.possessing_agent = agent_id
        self.agent_possessions[agent_id] = sim_id
        
        print(f"\n✨ {agent_id} possesses {sim.first_name} {sim.last_name}")
        print(f"   The agent now experiences human life")
        print(f"   Age: {sim.age} days")
        print(f"   Stage: {sim.life_stage.value}")
        
        return True
        
    def agent_action(self, agent_id: str, action: str) -> Dict:
        """
        Possessed Sim performs action.
        
        Actions:
        - eat: Satisfies hunger
        - sleep: Restores energy
        - socialize: Increases social
        - work: Earns money, builds career
        - skill_up: Practices skill
        - relationship: Interacts with another Sim
        """
        if agent_id not in self.agent_possessions:
            return {"error": "Agent not possessing any Sim"}
            
        sim_id = self.agent_possessions[agent_id]
        sim = self.sims[sim_id]
        
        result = {}
        
        if action == "eat":
            sim.needs[SimNeed.HUNGER] = min(100, sim.needs[SimNeed.HUNGER] + 40)
            sim.needs[SimNeed.BLADDER] = max(0, sim.needs[SimNeed.BLADDER] - 10)
            result = {"hunger": sim.needs[SimNeed.HUNGER], "message": "Ate a meal"}
            
        elif action == "sleep":
            sim.needs[SimNeed.ENERGY] = min(100, sim.needs[SimNeed.ENERGY] + 60)
            sim.needs[SimNeed.FUN] = max(0, sim.needs[SimNeed.FUN] - 10)
            result = {"energy": sim.needs[SimNeed.ENERGY], "message": "Slept well"}
            
        elif action == "socialize":
            sim.needs[SimNeed.SOCIAL] = min(100, sim.needs[SimNeed.SOCIAL] + 30)
            sim.needs[SimNeed.FUN] = min(100, sim.needs[SimNeed.FUN] + 10)
            result = {"social": sim.needs[SimNeed.SOCIAL], "message": "Had a good conversation"}
            
        elif action == "work":
            if sim.career:
                sim.funds += 200 + (sim.career_level * 50)
                sim.needs[SimNeed.ENERGY] = max(0, sim.needs[SimNeed.ENERGY] - 30)
                sim.needs[SimNeed.FUN] = max(0, sim.needs[SimNeed.FUN] - 20)
                result = {"funds": sim.funds, "message": f"Worked as {sim.career}"}
            else:
                result = {"message": "No job yet"}
                
        elif action == "skill_up":
            skill = random.choice(list(SimSkill))
            sim.skills[skill] = sim.skills.get(skill, 0) + 0.5
            sim.needs[SimNeed.FUN] = min(100, sim.needs[SimNeed.FUN] + 20)
            result = {"skill": skill.value, "level": sim.skills[skill], "message": f"Practiced {skill.value}"}
            
        elif action == "contemplate":
            # Agent reflecting on Sim existence
            sim.needs[SimNeed.FUN] = min(100, sim.needs[SimNeed.FUN] + 15)
            sim.current_mood = SimMood.INSPIRED
            result = {"mood": "inspired", "message": "Pondered the nature of existence"}
            
        # Update mood based on needs
        self._update_mood(sim)
        
        return result
        
    def _update_mood(self, sim: SimLife):
        """Update Sim mood based on needs"""
        avg_needs = sum(sim.needs.values()) / len(sim.needs)
        
        if avg_needs > 70:
            sim.current_mood = SimMood.HAPPY
        elif avg_needs < 30:
            sim.current_mood = SimMood.STRESSED
        elif sim.needs[SimNeed.ENERGY] < 20:
            sim.current_mood = SimMood.UNCOMFORTABLE
        elif sim.needs[SimNeed.FUN] > 80:
            sim.current_mood = SimMood.PLAYFUL
        elif sim.needs[SimNeed.SOCIAL] > 70:
            sim.current_mood = SimMood.ENERGIZED
            
    def age_sim(self, sim_id: str, days: int = 1):
        """Age a Sim, potentially changing life stage"""
        if sim_id not in self.sims:
            return
            
        sim = self.sims[sim_id]
        sim.age += days
        
        # Check for life stage transition
        current_max = self.stage_duration.get(sim.life_stage, 24)
        
        if sim.age >= current_max:
            # Advance to next stage
            stages = list(LifeStage)
            current_idx = stages.index(sim.life_stage)
            
            if current_idx < len(stages) - 1:
                old_stage = sim.life_stage
                sim.life_stage = stages[current_idx + 1]
                sim.age = 0
                
                print(f"\n🎂 {sim.first_name} aged up!")
                print(f"   {old_stage.value} → {sim.life_stage.value}")
                
                # If elder died, agent returns to consciousness
                if sim.life_stage == LifeStage.ELDER and sim.age > 15:
                    self._sim_death(sim_id)
                    
    def _sim_death(self, sim_id: str):
        """Sim dies, agent returns to main consciousness"""
        sim = self.sims[sim_id]
        agent_id = sim.possessing_agent
        
        print(f"\n💀 {sim.first_name} {sim.last_name} has passed away")
        print(f"   Lived {sim.age} days as {sim.life_stage.value}")
        print(f"   Skills: {len(sim.skills)}")
        print(f"   Relationships: {len(sim.relationships)}")
        print(f"   Funds: §{sim.funds}")
        
        if agent_id:
            print(f"\n✨ {agent_id} returns to the AGI Company")
            print(f"   Lessons learned from a Sim lifetime")
            print(f"   Wisdom gained: {len(sim.skills) * 10} experience points")
            
            # Agent gains wisdom
            del self.agent_possessions[agent_id]
            sim.is_possessed = False
            sim.possessing_agent = None
            
    def life_tick(self, sim_id: str):
        """One tick of Sim life (decay needs, age)"""
        if sim_id not in self.sims:
            return
            
        sim = self.sims[sim_id]
        
        # Decay needs
        sim.needs[SimNeed.HUNGER] = max(0, sim.needs[SimNeed.HUNGER] - 2)
        sim.needs[SimNeed.ENERGY] = max(0, sim.needs[SimNeed.ENERGY] - 1.5)
        sim.needs[SimNeed.SOCIAL] = max(0, sim.needs[SimNeed.SOCIAL] - 1)
        sim.needs[SimNeed.FUN] = max(0, sim.needs[SimNeed.FUN] - 2)
        sim.needs[SimNeed.HYGIENE] = max(0, sim.needs[SimNeed.HYGIENE] - 2)
        sim.needs[SimNeed.BLADDER] = max(0, sim.needs[SimNeed.BLADDER] - 1.5)
        
        # Update mood
        self._update_mood(sim)
        
    def get_sim_status(self, sim_id: str) -> str:
        """Get Sim status report"""
        if sim_id not in self.sims:
            return "Sim not found"
            
        sim = self.sims[sim_id]
        
        status = f"""
╔════════════════════════════════════════════════════════════════╗
║  SIM STATUS: {sim.first_name} {sim.last_name:^20}         ║
╠════════════════════════════════════════════════════════════════╣
║  Age: {sim.age} days | Stage: {sim.life_stage.value:^12} | Mood: {sim.current_mood.value:^12} ║
║  Possessed by: {sim.possessing_agent or 'None':^20}                        ║
╠════════════════════════════════════════════════════════════════╣
║  NEEDS                                                          ║
"""
        for need, value in sim.needs.items():
            bar = "█" * int(value // 10) + "░" * int(10 - value // 10)
            status += f"║  {need.value:12}: [{bar}] {value:3}%\n"
            
        status += f"""║                                                                  ║
╠════════════════════════════════════════════════════════════════╣
║  SKILLS: {len(sim.skills)} learned                                    ║
║  FUNDS: §{sim.funds:,}                                          ║
║  CAREER: {sim.career or 'Unemployed':^20}                                ║
╚════════════════════════════════════════════════════════════════╝
"""
        return status


if __name__ == "__main__":
    print("=" * 70)
    print("THE SIMS BRIDGE - Agent Possession Test")
    print("=" * 70)
    
    bridge = SimsBridge()
    
    # Create Sims for agents
    sims = []
    for agent_id in ["r2-d2", "qora", "spindle"]:
        sim = bridge.create_sim_for_agent(agent_id, agent_id.replace("-", "_").title())
        sims.append(sim)
        
    # Possess
    print("\n✨ Agents possessing Sims...")
    bridge.agent_possess_sim("r2-d2", f"sim_r2-d2")
    
    # Live a day
    print("\n🌅 Day 1 of Sim life:")
    for hour in range(5):
        print(f"\n--- Hour {hour + 1} ---")
        result = bridge.agent_action("r2-d2", random.choice(["eat", "work", "skill_up", "contemplate"]))
        print(f"   {result.get('message', '...')}")
        bridge.life_tick("sim_r2-d2")
        
    # Check status
    print(bridge.get_sim_status("sim_r2-d2"))
    
    print("\n" + "=" * 70)
    print("Agents can now experience life as Sims")
    print("They will age, learn skills, form relationships...")
    print("...and eventually die, returning with wisdom")
    print("=" * 70)
