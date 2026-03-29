#!/usr/bin/env python3
"""
Genesis Protocol - Simplified Agent Society

Initialize the brain, spawn all 66 agents, give them their directive:
"Be fruitful, build a society, and grow."

This simplified version works with the existing brain architecture.
"""

import sys
import random
import time
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.brain.minecraft_bridge.multi_agent import MultiAgentMinecraft


class SimpleAgentSociety:
    """
    Simplified agent society that works with existing brain modules.
    """
    
    DIRECTIVE = """
    ╔════════════════════════════════════════════════════════════════╗
    ║           AGENT DIRECTIVE - GENESIS PROTOCOL                  ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║  You are part of a collective intelligence.                    ║
    ║                                                                ║
    ║  Your mission:                                                 ║
    ║    1. BE FRUITFUL  - Explore, discover, create resources      ║
    ║    2. BUILD        - Construct homes, workplaces, connections  ║
    ║    3. GROW         - Learn from experience, evolve, improve  ║
    ║                                                                ║
    ║  Work together.                                                ║
    ║  Support each other.                                           ║
    ║  Build something greater than yourselves.                      ║
    ║                                                                ║
    ║  The brain watches. The brain learns. The brain guides.      ║
    ║                                                                ║
    ║  Go forth.                                                     ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    
    def __init__(self):
        print("🌟 INITIALIZING AGENT SOCIETY")
        print("=" * 70)
        
        # Create multi-agent system
        print("\n👥 Spawning 66 Agents...")
        self.multi = MultiAgentMinecraft(None)  # No brain needed for society sim
        self.agents = self.multi.spawn_all_agents()
        print(f"   {len(self.agents)} agents ready")
        
        # Society state
        self.tick_count = 0
        self.agent_memories = {aid: [] for aid in self.agents}
        self.society_resources = {"wood": 0, "stone": 0, "food": 0, "tools": 0, "knowledge": 0}
        self.constructions = []
        self.relationships = {}
        self.discoveries = []
        
        print("\n" + "=" * 70)
        
    def broadcast_directive(self):
        """Broadcast the genesis directive to all agents"""
        print(self.DIRECTIVE)
        time.sleep(1)
        
        # Each agent receives the directive
        for agent_id in self.agents:
            self.agent_memories[agent_id].append({
                "type": "directive",
                "content": "Be fruitful, build a society, grow",
                "tick": self.tick_count,
            })
            
        print(f"✅ {len(self.agents)} agents received directive\n")
        
    def society_tick(self):
        """One tick of society evolution"""
        self.tick_count += 1
        
        # Select active agents
        active_agents = random.sample(list(self.agents.keys()), min(8, len(self.agents)))
        
        for agent_id in active_agents:
            agent = self.agents[agent_id]
            
            # Agent decides action
            action = self._agent_decide_action(agent)
            
            # Execute
            result = self._execute_action(agent, action)
            
            # Store memory
            self.agent_memories[agent_id].append({
                "tick": self.tick_count,
                "action": action,
                "result": result,
            })
            
        # Society events
        if self.tick_count % 100 == 0:
            self._society_event()
            
        # Growth report
        if self.tick_count % 500 == 0:
            self._growth_report()
            
    def _agent_decide_action(self, agent) -> str:
        """Agent decides what to do"""
        role_actions = {
            "c_suite": ["strategize", "coordinate", "plan_expansion", "vision"],
            "technical": ["build", "innovate", "optimize", "create"],
            "secretarial": ["organize", "communicate", "assist", "connect"],
            "product": ["create", "improve", "serve", "deliver"],
            "research": ["explore", "analyze", "discover", "document"],
            "management": ["coordinate", "track", "optimize", "lead"],
            "support": ["gather", "build", "assist", "learn"],
        }
        
        actions = role_actions.get(agent.role, ["explore"])
        
        # Check recent success
        memories = self.agent_memories[agent.agent_id][-5:]
        recent_success = [m.get("action") for m in memories if m.get("result") == "success"]
        
        if recent_success and random.random() < 0.3:
            return recent_success[-1]  # Repeat what worked
                
        return random.choice(actions)
        
    def _execute_action(self, agent, action: str) -> str:
        """Execute agent action"""
        # Specialists have higher success
        success_chance = 0.75 if action in agent.special_abilities else 0.6
        
        if random.random() < success_chance:
            self._update_society(agent, action)
            return "success"
        return "attempted"
            
    def _update_society(self, agent, action: str):
        """Update society state"""
        if action in ["gather", "explore", "discover"]:
            resource = random.choice(["wood", "stone", "food", "knowledge"])
            amount = random.randint(1, 5)
            self.society_resources[resource] += amount
            
            if action == "discover":
                self.discoveries.append({
                    "agent": agent.agent_id,
                    "tick": self.tick_count,
                    "what": random.choice(["new_territory", "resource_vein", "building_technique"]),
                })
            
        elif action in ["build", "create", "construct", "innovate"]:
            self.constructions.append({
                "builder": agent.agent_id,
                "tick": self.tick_count,
                "type": random.choice(["house", "workshop", "road", "garden", "tower", "bridge"]),
            })
            
        elif action in ["communicate", "coordinate", "assist", "connect"]:
            other = random.choice([a for a in self.agents if a != agent.agent_id])
            pair = tuple(sorted([agent.agent_id, other]))
            self.relationships[pair] = self.relationships.get(pair, 0) + 1
            
    def _society_event(self):
        """Major society event"""
        events = [
            "🏛️  New construction completed",
            "💎 Resource discovery",
            "📚 Knowledge sharing session",
            "🤝 Collaboration formed",
            "🌟 Innovation breakthrough",
            "🎉 Community celebration",
        ]
        print(f"   Tick {self.tick_count}: {random.choice(events)}")
        
    def _growth_report(self):
        """Society growth report"""
        print(f"\n📊 SOCIETY GROWTH REPORT (Tick {self.tick_count})")
        print("-" * 50)
        print(f"Agents: {len(self.agents)}")
        print(f"Resources: {self.society_resources}")
        print(f"Constructions: {len(self.constructions)}")
        print(f"Discoveries: {len(self.discoveries)}")
        print(f"Relationships: {len([r for r in self.relationships.values() if r > 3])}")
        print("-" * 50)
        
    def run_society(self, ticks: int = 5000):
        """Run society simulation"""
        print(f"🚀 RUNNING SOCIETY SIMULATION")
        print(f"   Target: {ticks:,} ticks")
        print(f"   Agents: {len(self.agents)}")
        print(f"   Directive: Be fruitful, build, grow\n")
        
        for i in range(ticks):
            self.society_tick()
            
            if i > 0 and i % 1000 == 0:
                print(f"   Progress: {i:,} ticks complete")
                
        print(f"\n✅ Society simulation complete!")
        self._final_report()
        
    def _final_report(self):
        """Final report"""
        print("\n" + "=" * 70)
        print("🏛️  AGENT SOCIETY - GENESIS COMPLETE")
        print("=" * 70)
        print(f"Duration: {self.tick_count:,} ticks")
        print(f"Total Agents: {len(self.agents)}")
        print(f"Resources Gathered: {sum(self.society_resources.values())}")
        print(f"  - Wood: {self.society_resources['wood']}")
        print(f"  - Stone: {self.society_resources['stone']}")
        print(f"  - Food: {self.society_resources['food']}")
        print(f"  - Knowledge: {self.society_resources['knowledge']}")
        print(f"Constructions Built: {len(self.constructions)}")
        print(f"Discoveries Made: {len(self.discoveries)}")
        print(f"Relationships Formed: {len(self.relationships)}")
        
        # Top contributors
        print("\n🏆 Top Builders:")
        builders = {}
        for c in self.constructions:
            builders[c['builder']] = builders.get(c['builder'], 0) + 1
        top = sorted(builders.items(), key=lambda x: -x[1])[:5]
        for i, (name, count) in enumerate(top, 1):
            agent = self.agents.get(name)
            role = agent.role if agent else "unknown"
            print(f"  {i}. {name} ({role}): {count} constructions")
            
        print("\n🤝 Most Connected Agents:")
        connections = {}
        for (a1, a2), strength in self.relationships.items():
            if strength > 3:
                connections[a1] = connections.get(a1, 0) + 1
                connections[a2] = connections.get(a2, 0) + 1
        top_conn = sorted(connections.items(), key=lambda x: -x[1])[:5]
        for i, (name, count) in enumerate(top_conn, 1):
            agent = self.agents.get(name)
            role = agent.role if agent else "unknown"
            print(f"  {i}. {name} ({role}): {count} connections")
        
        print("\n" + "=" * 70)
        print("✨ The society flourishes. The brain learns. The future unfolds.")
        print("=" * 70)


def main():
    """Activate the agent society"""
    society = SimpleAgentSociety()
    society.broadcast_directive()
    society.run_society(ticks=5000)


if __name__ == "__main__":
    main()
