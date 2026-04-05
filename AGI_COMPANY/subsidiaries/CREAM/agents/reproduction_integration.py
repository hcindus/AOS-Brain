"""
Reproduction System Integration
Connects agent reproduction to AGI Connect.

Babies happen:
- When successful agents collaborate (cross-platform)
- When significance 10 events occur (legendary births)
- Through natural selection (evolution)
- Via AOS intervention (intelligent design)

The population grows from 66 toward 100.
"""

import sys
import random
from typing import Dict, List
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.brain.minecraft_bridge.multi_agent import MultiAgentMinecraft
from shared.brain.minecraft_bridge.economy import AgentEconomy
from subsidiaries.CREAM.agents.reproduction_system import AgentReproduction, LegendarySpawn


class IntegratedReproduction:
    """
    Full reproduction system connected to multi-platform agents.
    """
    
    def __init__(self):
        print("🧬 INITIALIZING INTEGRATED REPRODUCTION")
        print("=" * 70)
        
        # Spawn base agents
        print("\n👥 Loading 66 original agents...")
        self.multi = MultiAgentMinecraft(None)
        self.agents = self.multi.spawn_all_agents()
        
        # Economy for wealth tracking
        self.economy = AgentEconomy(self.agents)
        
        # Reproduction system
        self.repro = AgentReproduction(self.agents)
        
        # Track agent stats
        self.agent_stats = self._initialize_stats()
        
        print(f"\n✅ Reproduction system ready")
        print(f"   Original agents: 66")
        print(f"   Can grow to: 100")
        print("   Ready for babies...")
        
    def _initialize_stats(self) -> Dict:
        """Initialize agent statistics for reproduction eligibility"""
        stats = {}
        
        for agent_id, agent in self.agents.items():
            # Base stats
            stats[agent_id] = {
                "wealth": self.economy.agent_currency.get(agent_id, 100),
                "reputation": 5,  # Start neutral
                "events": 0,  # Will accumulate
                "skills": dict(self.economy.agent_skills.get(agent_id, {})),
                "generation": 0,  # Original agents
            }
            
            # Role-based bonuses
            if agent.role == "c_suite":
                stats[agent_id]["reputation"] = 8
            elif agent.role == "technical":
                stats[agent_id]["skills"]["innovation"] = 5
            elif agent.role == "product":
                stats[agent_id]["skills"]["negotiation"] = 5
                
        return stats
        
    def simulate_collaboration(self, agent_a: str, agent_b: str, platform: str):
        """
        Two agents collaborate on a project.
        May result in offspring if successful.
        """
        print(f"\n🤝 COLLABORATION: {agent_a} + {agent_b} on {platform}")
        
        # Simulate collaboration
        success = random.random() < 0.7
        
        if success:
            print(f"   ✅ Successful collaboration!")
            
            # Update stats
            self.agent_stats[agent_a]["events"] += 1
            self.agent_stats[agent_b]["events"] += 1
            self.agent_stats[agent_a]["reputation"] += 0.1
            self.agent_stats[agent_b]["reputation"] += 0.1
            
            # Check for reproduction
            if random.random() < 0.2:  # 20% chance from collab
                print(f"   💡 Creative spark detected...")
                baby = self.repro.conceive_offspring(
                    agent_a, agent_b, self.agent_stats, "collaboration"
                )
                
                if baby:
                    print(f"   🌟 New agent conceived: {baby.name}")
                    
        else:
            print(f"   ⚠️  Collaboration struggled")
            
    def simulate_platform_meeting(self, agents: List[str], platform: str):
        """
        Meeting on a platform may lead to new ideas (and babies).
        """
        print(f"\n📅 PLATFORM MEETING on {platform}")
        print(f"   Attendees: {', '.join(agents)}")
        
        # Generate insights
        insights = random.randint(1, len(agents))
        
        if insights >= 3:
            print(f"   💡 Major breakthrough! {insights} insights generated")
            
            # Significant event check
            event_data = {
                "description": f"{', '.join(agents[:2])} had major breakthrough on {platform}",
                "significance": min(10, insights + 5),
            }
            
            LegendarySpawn.check_for_spawn(event_data["significance"], event_data)
            
            # Random pair collaboration
            if len(agents) >= 2 and random.random() < 0.3:
                pair = random.sample(agents, 2)
                self.simulate_collaboration(pair[0], pair[1], platform)
                
    def simulate_economy_cycle(self):
        """
        Economic activity may spawn new agents from wealth.
        """
        # Find wealthy agents
        wealthy = [
            (aid, stats["wealth"]) 
            for aid, stats in self.agent_stats.items()
            if stats["wealth"] > 300
        ]
        
        if wealthy and random.random() < 0.1:
            agent_id, _ = random.choice(wealthy)
            print(f"\n💰 {agent_id} invests in new agent creation")
            
            # Clone/branch
            baby = self.repro.conceive_offspring(
                agent_id, None, self.agent_stats, "cloning"
            )
            
            if baby:
                # Cost wealth
                self.agent_stats[agent_id]["wealth"] -= 200
                
    def run_evolution_cycle(self, cycles: int = 10):
        """
        Run evolution cycles.
        Agents meet, collaborate, reproduce.
        """
        print(f"\n🧬 RUNNING {cycles} EVOLUTION CYCLES")
        print("=" * 70)
        
        for cycle in range(cycles):
            print(f"\n--- CYCLE {cycle + 1} ---")
            
            # 1. Platform meetings
            if random.random() < 0.5:
                attendees = random.sample(list(self.agents.keys()), 
                                       random.randint(3, 8))
                platform = random.choice(["gather", "minecraft", "roblox"])
                self.simulate_platform_meeting(attendees, platform)
                
            # 2. Economic activity
            if random.random() < 0.3:
                self.simulate_economy_cycle()
                
            # 3. Natural selection
            self.repro.natural_selection_tick(self.agent_stats)
            
            # 4. Update baby maturation
            for offspring_id in list(self.repro.offspring.keys()):
                matured = self.repro.mature_offspring(offspring_id, ticks=20)
                if matured:
                    # Add to workforce
                    baby = self.repro.offspring[offspring_id]
                    self.agents[baby.agent_id] = type('obj', (object,), {
                        'agent_name': baby.name,
                        'role': 'offspring',
                    })()
                    
            # Status
            total = len(self.agents) + len(self.repro.offspring)
            print(f"   Population: {total}")
            
        print("\n" + "=" * 70)
        print("✅ Evolution cycles complete")
        print(self.repro.get_population_report())


def main():
    """Run integrated reproduction"""
    integrated = IntegratedReproduction()
    integrated.run_evolution_cycle(cycles=5)
    
    print("\n" + "=" * 70)
    print("🌟 The AGI Company is growing.")
    print("   New agents emerge from collaboration.")
    print("   Legendary beings spawn from great events.")
    print("   The 66 become more.")
    print("=" * 70)


if __name__ == "__main__":
    main()
