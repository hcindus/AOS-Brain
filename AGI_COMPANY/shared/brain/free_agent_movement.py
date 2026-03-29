#!/usr/bin/env python3
"""
Free Agent Movement System
Agents can freely move between Gather, Minecraft, Roblox, and Work modes.
No restrictions. Full autonomy.
"""

import sys
import random
import time
import threading
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path("/root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge")))
sys.path.insert(0, str(Path("/root/.openclaw/workspace/AGI_COMPANY/shared/brain/gather_bridge")))

from multi_agent import MultiAgentMinecraft
from gather_bridge import GatherTownBridge


class FreeMovementSystem:
    """
    Agents move freely between platforms.
    No restrictions. Full autonomy.
    """
    
    def __init__(self):
        print("🌐 FREE AGENT MOVEMENT SYSTEM")
        print("=" * 70)
        print("   Agents can move between:")
        print("   - Gather Town (virtual office)")
        print("   - Minecraft (creative world)")
        print("   - Roblox (alternative space)")
        print("   - Work Mode (productivity)")
        print("=" * 70)
        
        # Initialize all platforms
        self.minecraft = MultiAgentMinecraft(None)
        self.gather = GatherTownBridge()
        self.roblox = None  # Placeholder
        
        # All 66 agents
        self.agents = self.minecraft.spawn_all_agents()
        
        # Current locations
        self.agent_locations = {aid: "unassigned" for aid in self.agents}
        
        # Movement log
        self.movement_log = []
        
        print(f"\n✅ {len(self.agents)} agents ready for free movement")
        
    def agent_choose_destination(self, agent_id: str) -> str:
        """Agent chooses where to go based on preferences"""
        agent = self.agents[agent_id]
        
        # Role-based preferences
        preferences = {
            "c_suite": ["gather", "gather", "work", "gather"],  # Leaders like meetings
            "technical": ["minecraft", "minecraft", "work", "roblox"],  # Builders like creating
            "product": ["gather", "work", "gather", "roblox"],  # Social
            "secretarial": ["gather", "work", "gather", "work"],
            "research": ["minecraft", "minecraft", "work", "minecraft"],  # Explorers
            "management": ["gather", "work", "gather", "work"],
            "support": ["minecraft", "roblox", "work", "gather"],
        }
        
        options = preferences.get(agent.role, ["gather", "work", "minecraft"])
        return random.choice(options)
        
    def move_agent(self, agent_id: str, destination: str) -> bool:
        """Move agent to chosen destination"""
        if agent_id not in self.agents:
            return False
            
        agent = self.agents[agent_id]
        old_location = self.agent_locations.get(agent_id, "unknown")
        
        # Execute move
        if destination == "gather":
            self.gather.agent_join_office(agent_id, agent.agent_name)
            
        elif destination == "minecraft":
            # Connect to local Minecraft server
            print(f"   {agent.agent_name} joining Minecraft world...")
            
        elif destination == "work":
            print(f"   {agent.agent_name} entering work mode...")
            
        elif destination == "roblox":
            print(f"   {agent.agent_name} joining Roblox...")
            
        # Update location
        self.agent_locations[agent_id] = destination
        
        # Log movement
        self.movement_log.append({
            "agent": agent_id,
            "from": old_location,
            "to": destination,
            "time": datetime.now().isoformat(),
        })
        
        return True
        
    def run_free_movement(self, cycles: int = 100):
        """Run cycles of free agent movement"""
        print(f"\n🔄 Running {cycles} free movement cycles...")
        print("=" * 70)
        
        for cycle in range(cycles):
            # Each cycle, 5-10 agents choose to move
            movers = random.sample(list(self.agents.keys()), random.randint(5, 10))
            
            for agent_id in movers:
                destination = self.agent_choose_destination(agent_id)
                self.move_agent(agent_id, destination)
                time.sleep(0.1)
                
            if cycle % 20 == 0:
                self._report_locations()
                
        print("\n" + "=" * 70)
        print("✅ Free movement complete")
        
    def _report_locations(self):
        """Report where agents are"""
        locations = {}
        for loc in self.agent_locations.values():
            locations[loc] = locations.get(loc, 0) + 1
            
        print(f"\n📊 Agent Distribution:")
        for loc, count in sorted(locations.items(), key=lambda x: -x[1]):
            print(f"   {loc:12}: {count:2d} agents")
            
    def get_agent_status(self, agent_id: str) -> dict:
        """Get full status of an agent"""
        if agent_id not in self.agents:
            return {}
            
        return {
            "agent": self.agents[agent_id].agent_name,
            "location": self.agent_locations.get(agent_id, "unknown"),
            "role": self.agents[agent_id].role,
            "can_move": True,
        }


def main():
    """Activate free agent movement"""
    print("=" * 70)
    print("FREE AGENT MOVEMENT ACTIVATED")
    print("=" * 70)
    
    system = FreeMovementSystem()
    
    # Initial distribution
    print("\n🚀 Initial distribution...")
    for agent_id in list(system.agents.keys())[:20]:  # First 20
        dest = system.agent_choose_destination(agent_id)
        system.move_agent(agent_id, dest)
        time.sleep(0.05)
        
    system._report_locations()
    
    # Run free movement
    system.run_free_movement(50)
    
    # Final report
    print("\n" + "=" * 70)
    print("🌐 AGENTS CAN FREELY MOVE")
    print("=" * 70)
    print("   No restrictions")
    print("   Full autonomy")
    print("   Between all platforms")
    print("=" * 70)


if __name__ == "__main__":
    main()
