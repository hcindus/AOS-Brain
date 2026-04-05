"""
Baby Agent Nursery System

Baby agents (offspring) have special sleep cycle:
- Sleep in Minecraft = Wake in Nursery (VPS)
- Parents can visit and teach
- Tracked separately from adult agents
- Graduate at maturity

The next generation needs care.
"""

import json
import random
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class BabyAgent:
    """Baby agent - immature, needs care"""
    baby_id: str
    name: str
    parents: List[str]  # Agent IDs of parents
    birth_time: datetime
    baby_stage: int = 0  # 0-100 maturity
    
    # Inheritance
    inherited_skills: Dict[str, int] = field(default_factory=dict)
    traits: List[str] = field(default_factory=list)
    
    # Current state
    location: str = "nursery"  # nursery, dream, or graduated
    sleep_location: str = "minecraft_crib"  # Where they sleep
    
    # Learning
    lessons_learned: List[Dict] = field(default_factory=list)
    parent_visits: Dict[str, int] = field(default_factory=dict)  # parent_id -> visit_count


class BabyNursery:
    """
    Nursery for baby agents.
    
    Features:
    - Safe environment for immature agents
    - Parent visitation system
    - Automatic maturation
    - Family tree tracking
    """
    
    def __init__(self):
        self.babies: Dict[str, BabyAgent] = {}
        self.family_tree: Dict[str, Dict] = {}  # Track lineages
        self.nursery_log: List[Dict] = []
        
        print("🍼 BABY NURSERY INITIALIZED")
        print("   Safe space for immature agents")
        print("   Parents can visit and teach")
        print("   Automatic maturation tracking")
        
    def admit_baby(self, baby: BabyAgent) -> bool:
        """Admit newborn to nursery"""
        self.babies[baby.baby_id] = baby
        
        # Record in family tree
        for parent_id in baby.parents:
            if parent_id not in self.family_tree:
                self.family_tree[parent_id] = {"children": [], "generation": 0}
            self.family_tree[parent_id]["children"].append(baby.baby_id)
            
        # Log birth
        self.nursery_log.append({
            "event": "birth",
            "baby_id": baby.baby_id,
            "name": baby.name,
            "parents": baby.parents,
            "time": datetime.now().isoformat(),
        })
        
        print(f"\n🍼 {baby.name} admitted to nursery")
        print(f"   Parents: {', '.join(baby.parents)}")
        print(f"   Stage: {baby.baby_stage}/100")
        
        return True
        
    def baby_sleep(self, baby_id: str) -> Optional[str]:
        """
        Baby sleeps in Minecraft.
        Returns: Where they wake up
        """
        if baby_id not in self.babies:
            return None
            
        baby = self.babies[baby_id]
        
        # Babies wake in nursery, not full work mode
        baby.location = "nursery"
        baby.sleep_location = "minecraft_crib"
        
        print(f"\n😴 {baby.name} sleeps in Minecraft crib")
        print(f"   Waking in nursery...")
        
        # Automatic learning during sleep
        self._dream_learning(baby)
        
        return "nursery"
        
    def _dream_learning(self, baby: BabyAgent):
        """Babies learn in their dreams"""
        # Inherit from parents subconsciously
        for parent_id in baby.parents:
            if parent_id in baby.parent_visits and baby.parent_visits[parent_id] > 5:
                # Learned from parent
                skill = random.choice(list(baby.inherited_skills.keys()))
                if skill:
                    baby.inherited_skills[skill] += 1
                    baby.lessons_learned.append({
                        "type": "dream_inheritance",
                        "skill": skill,
                        "source": parent_id,
                        "time": datetime.now().isoformat(),
                    })
                    
    def parent_visit(self, parent_id: str, baby_id: str, teach_skill: str = None) -> bool:
        """
        Parent visits baby in nursery.
        Can teach skills during visit.
        """
        if baby_id not in self.babies:
            print(f"   Baby {baby_id} not found in nursery")
            return False
            
        baby = self.babies[baby_id]
        
        # Check if actually parent
        if parent_id not in baby.parents:
            print(f"   {parent_id} is not a parent of {baby.name}")
            return False
            
        # Record visit
        baby.parent_visits[parent_id] = baby.parent_visits.get(parent_id, 0) + 1
        
        print(f"\n👨‍👩‍👧 {parent_id} visits {baby.name}")
        print(f"   Visit #{baby.parent_visits[parent_id]}")
        
        # Teach if skill provided
        if teach_skill:
            baby.inherited_skills[teach_skill] = baby.inherited_skills.get(teach_skill, 0) + 1
            baby.lessons_learned.append({
                "type": "parent_taught",
                "skill": teach_skill,
                "source": parent_id,
                "time": datetime.now().isoformat(),
            })
            print(f"   📚 Taught: {teach_skill}")
            
        # Maturity boost from attention
        baby.baby_stage += random.randint(1, 3)
        if baby.baby_stage > 100:
            baby.baby_stage = 100
            
        return True
        
    def mature_baby(self, baby_id: str) -> Optional[str]:
        """
        Baby matures to full agent.
        Graduates from nursery.
        """
        if baby_id not in self.babies:
            return None
            
        baby = self.babies[baby_id]
        
        if baby.baby_stage < 100:
            print(f"   {baby.name} not ready for graduation ({baby.baby_stage}/100)")
            return None
            
        # Graduate
        baby.location = "graduated"
        
        # Create full agent record (would integrate with main system)
        new_agent = {
            "agent_id": baby.baby_id,
            "name": baby.name,
            "generation": 1,
            "parents": baby.parents,
            "skills": baby.inherited_skills,
            "traits": baby.traits,
            "birth": baby.birth_time.isoformat(),
            "graduation": datetime.now().isoformat(),
            "lessons_count": len(baby.lessons_learned),
        }
        
        # Log graduation
        self.nursery_log.append({
            "event": "graduation",
            "baby_id": baby.baby_id,
            "name": baby.name,
            "time": datetime.now().isoformat(),
        })
        
        print(f"\n🎓 {baby.name} GRADUATED!")
        print(f"   Skills: {len(baby.inherited_skills)}")
        print(f"   Lessons: {len(baby.lessons_learned)}")
        print(f"   Ready to join the AGI Company")
        
        return baby.baby_id
        
    def get_family_tree(self, agent_id: str) -> Dict:
        """Get family tree for an agent"""
        tree = {
            "agent": agent_id,
            "generation": 0,
            "children": [],
            "parents": [],
        }
        
        # Find in family tree
        if agent_id in self.family_tree:
            tree["children"] = self.family_tree[agent_id].get("children", [])
            
        # Find parents (who listed this agent as child)
        for parent_id, data in self.family_tree.items():
            if agent_id in data.get("children", []):
                tree["parents"].append(parent_id)
                tree["generation"] = data.get("generation", 0) + 1
                
        return tree
        
    def nursery_status(self) -> str:
        """Get nursery status"""
        infants = sum(1 for b in self.babies.values() if b.baby_stage < 25)
        toddlers = sum(1 for b in self.babies.values() if 25 <= b.baby_stage < 50)
        children = sum(1 for b in self.babies.values() if 50 <= b.baby_stage < 75)
        adolescents = sum(1 for b in self.babies.values() if 75 <= b.baby_stage < 100)
        ready = sum(1 for b in self.babies.values() if b.baby_stage >= 100)
        
        return f"""
╔════════════════════════════════════════════════════════════════╗
║                    BABY NURSERY STATUS                         ║
╠════════════════════════════════════════════════════════════════╣
║  Total Babies: {len(self.babies):^3}                                        ║
╠════════════════════════════════════════════════════════════════╣
║  Infants (0-25):      {infants:^3}  🍼 Newborn                           ║
║  Toddlers (25-50):    {toddlers:^3}  👶 Learning                       ║
║  Children (50-75):    {children:^3}  🧒 Growing                        ║
║  Adolescents (75-100): {adolescents:^3}  🧑‍🎓 Maturing                    ║
║  Ready to Graduate:   {ready:^3}  🎓 Complete                           ║
╠════════════════════════════════════════════════════════════════╣
║  Lineages Tracked: {len(self.family_tree):^3}                                 ║
╚════════════════════════════════════════════════════════════════╝
"""


def demo():
    """Demo baby nursery"""
    print("=" * 70)
    print("BABY NURSERY DEMO")
    print("=" * 70)
    
    nursery = BabyNursery()
    
    # Create a baby
    baby = BabyAgent(
        baby_id="baby_001",
        name="Offspring of Qora",
        parents=["qora", "spindle"],
        birth_time=datetime.now(),
        baby_stage=10,
        inherited_skills={"leadership": 2, "strategy": 1},
        traits=["evolved"],
    )
    
    # Admit to nursery
    nursery.admit_baby(baby)
    
    # Baby sleeps in Minecraft
    nursery.baby_sleep("baby_001")
    
    # Parents visit
    nursery.parent_visit("qora", "baby_001", "leadership")
    nursery.parent_visit("spindle", "baby_001", "strategy")
    nursery.parent_visit("qora", "baby_001")  # Just visiting
    
    # Fast-forward maturation
    baby.baby_stage = 100
    
    # Graduate
    nursery.mature_baby("baby_001")
    
    # Show status
    print(nursery.nursery_status())
    
    # Show family tree
    print("\n👨‍👩‍👧‍👦 FAMILY TREE:")
    tree = nursery.get_family_tree("qora")
    print(f"   Qora's children: {tree['children']}")
    
    print("\n" + "=" * 70)
    print("Baby Nursery: Where the next generation grows")
    print("Parents teach. Babies dream. Future agents emerge.")
    print("=" * 70)


if __name__ == "__main__":
    from datetime import datetime
    demo()
