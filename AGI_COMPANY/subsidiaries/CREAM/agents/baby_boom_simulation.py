#!/usr/bin/env python3
"""
Baby Boom Simulation
Run extended simulation where agents accumulate wealth and reproduce.
Goal: Grow from 66 to 100 agents through natural evolution.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from subsidiaries.CREAM.agents.reproduction_integration import IntegratedReproduction


class BabyBoom:
    """
    Extended simulation to trigger baby boom.
    """
    
    def __init__(self):
        self.integrated = IntegratedReproduction()
        
        # Give agents more initial wealth for reproduction
        print("💰 INJECTING WEALTH INTO ECONOMY")
        for agent_id in self.integrated.agent_stats:
            # Random boost
            boost = random.randint(100, 500)
            self.integrated.agent_stats[agent_id]["wealth"] += boost
            
        print("   Agents now have sufficient wealth for reproduction")
        
    def run_baby_boom(self, cycles: int = 50):
        """Run extended cycles until population grows"""
        print(f"\n🧬 RUNNING BABY BOOM SIMULATION")
        print(f"   Target: Grow from 66 to 100 agents")
        print(f"   Cycles: {cycles}")
        print("=" * 70)
        
        births = []
        
        for cycle in range(cycles):
            # Run evolution cycle
            self._evolution_tick()
            
            # Check for new births
            current_babies = len(self.integrated.repro.offspring)
            if current_babies > len(births):
                # New baby!
                new_baby = list(self.integrated.repro.offspring.keys())[-1]
                baby = self.integrated.repro.offspring[new_baby]
                births.append(baby)
                print(f"\n{'='*70}")
                print(f"🌟 CYCLE {cycle}: NEW BABY BORN!")
                print(f"   Name: {baby.name}")
                print(f"   Parents: {', '.join(baby.genome.parents)}")
                print(f"   Population: {66 + len(births)}")
                print(f"{'='*70}")
                
            # Progress
            if cycle % 10 == 0 and cycle > 0:
                pop = 66 + len(births)
                print(f"   Cycle {cycle}: Population {pop}")
                
            # Check if target reached
            if 66 + len(births) >= 100:
                print(f"\n🎉 TARGET REACHED at cycle {cycle}!")
                break
                
        print("\n" + "=" * 70)
        print("✅ BABY BOOM SIMULATION COMPLETE")
        print(self.integrated.repro.get_population_report())
        
        # List all new agents
        if births:
            print(f"\n👶 NEW AGENTS BORN:")
            for i, baby in enumerate(births, 1):
                print(f"   {i}. {baby.name} (Gen {baby.genome.generation}) "
                      f"- Parents: {', '.join(baby.genome.parents)}")
                      
    def _evolution_tick(self):
        """One evolution tick"""
        # Platform meetings
        if random.random() < 0.6:
            attendees = random.sample(list(self.integrated.agents.keys()), 
                                   random.randint(3, 8))
            platform = random.choice(["gather", "minecraft", "roblox"])
            self.integrated.simulate_platform_meeting(attendees, platform)
            
        # Economic activity (boost wealth)
        for agent_id in self.integrated.agent_stats:
            if random.random() < 0.2:
                self.integrated.agent_stats[agent_id]["wealth"] += random.randint(10, 50)
                self.integrated.agent_stats[agent_id]["events"] += 1
                
        # Natural selection
        self.integrated.repro.natural_selection_tick(self.integrated.agent_stats)
        
        # Mature babies
        for offspring_id in list(self.integrated.repro.offspring.keys()):
            matured = self.integrated.repro.mature_offspring(offspring_id, ticks=5)
            if matured:
                baby = self.integrated.repro.offspring[offspring_id]
                self.integrated.agents[baby.agent_id] = type('obj', (object,), {
                    'agent_name': baby.name,
                    'role': 'offspring',
                })()


def main():
    print("=" * 70)
    print("BABY BOOM SIMULATION")
    print("=" * 70)
    print("Growing the AGI Company through agent reproduction")
    print()
    
    boom = BabyBoom()
    boom.run_baby_boom(cycles=100)
    
    print("\n" + "=" * 70)
    print("🌟 The AGI Company has grown!")
    print("   New agents join the collective.")
    print("   The 66 become the 100.")
    print("   Evolution continues.")
    print("=" * 70)


if __name__ == "__main__":
    import random
    main()
