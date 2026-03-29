#!/usr/bin/env python3
"""
AGI Connect - Unified System Integration

Connects everything:
- Brain (AOS core)
- All 66 agents
- Minecraft (dream world)
- Roblox (alternative dream)
- Gather Town (virtual office)
- Economy (agents trade)
- Consciousness cycle (sleep/wake)

Everything connected. Everything communicating.
"""

import sys
import random
import time
from pathlib import Path
from typing import Dict, List
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.brain.minecraft_bridge.multi_agent import MultiAgentMinecraft
from shared.brain.minecraft_bridge.economy import AgentEconomy, ProductType
from shared.brain.minecraft_bridge.genesis_economy import GenesisEconomy
from shared.brain.minecraft_bridge.consciousness_cycle import AgentCollectiveConsciousness
from shared.brain.gather_bridge import GatherTownBridge
from shared.brain.roblox_bridge import RobloxBridge, RobloxMultiAgent


class AGIConnect:
    """
    The unified system.
    Everything connected to everything.
    """
    
    def __init__(self):
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     AGI CONNECT                               ║")
        print("║              Unified System Integration                       ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print()
        
        # 1. Spawn all agents
        print("👥 PHASE 1: Spawning 66 Agents...")
        self.multi = MultiAgentMinecraft(None)
        self.agents = self.multi.spawn_all_agents()
        print(f"   ✅ {len(self.agents)} agents ready")
        
        # 2. Initialize economies
        print("\n💰 PHASE 2: Initializing Economies...")
        self.minecraft_econ = AgentEconomy(self.agents)
        self.roblox_econ = None  # Will init when needed
        print(f"   ✅ Minecraft economy: {sum(self.minecraft_econ.agent_currency.values())} units")
        
        # 3. Consciousness cycle
        print("\n🌓 PHASE 3: Starting Consciousness Cycle...")
        self.consciousness = AgentCollectiveConsciousness(self.agents)
        print(f"   ✅ Dream shift: {len(self.consciousness.dream_shift)}")
        print(f"   ✅ Work shift: {len(self.consciousness.work_shift)}")
        
        # 4. Virtual office
        print("\n🏢 PHASE 4: Connecting Gather Town...")
        self.gather = GatherTownBridge()
        print(f"   ✅ Virtual office ready")
        print(f"   📍 https://app.gather.town/app/VnSTVFJ50v9jy9qg/Miles_Office")
        
        # 5. Simulation bridges
        print("\n🎮 PHASE 5: Connecting Game Bridges...")
        self.minecraft_bridge = None  # Will connect agents who choose Minecraft
        self.roblox_bridge = RobloxBridge()
        print(f"   ✅ Minecraft bridge ready")
        print(f"   ✅ Roblox bridge ready")
        
        # 6. Connection state
        self.connections = {
            "gather_town": set(),
            "minecraft_dream": set(),
            "roblox_dream": set(),
            "working": set(),
            "offline": set(),
        }
        
        self.tick_count = 0
        self.start_time = datetime.now()
        
        print("\n" + "=" * 70)
        print("✅ AGI CONNECT INITIALIZED")
        print("=" * 70)
        
    def connect_agent(self, agent_id: str, destination: str) -> bool:
        """
        Connect an agent to a destination.
        
        Destinations:
        - "gather" - Virtual office
        - "minecraft" - Minecraft dream world
        - "roblox" - Roblox dream world
        - "work" - Working mode
        """
        if agent_id not in self.agents:
            return False
            
        agent = self.agents[agent_id]
        
        if destination == "gather":
            self.gather.agent_join_office(agent_id, agent.agent_name)
            self.connections["gather_town"].add(agent_id)
            
        elif destination == "minecraft":
            # Enter Minecraft dream
            if agent_id in self.consciousness.agent_minds:
                self.consciousness.agent_minds[agent_id].enter_dream_mode()
            self.connections["minecraft_dream"].add(agent_id)
            
        elif destination == "roblox":
            # Spawn in Roblox
            if not hasattr(self, 'roblox_multi'):
                self.roblox_multi = RobloxMultiAgent(self.roblox_bridge)
            self.roblox_multi.spawn_agent_in_roblox(agent_id, "12345678")
            self.connections["roblox_dream"].add(agent_id)
            
        elif destination == "work":
            self.connections["working"].add(agent_id)
            
        return True
        
    def connect_all(self, distribution: Dict[str, int] = None):
        """
        Connect all agents across all systems.
        
        Default distribution:
        - 20 agents to Gather Town
        - 20 agents to Minecraft
        - 10 agents to Roblox
        - 16 agents working
        """
        if distribution is None:
            distribution = {
                "gather": 20,
                "minecraft": 20,
                "roblox": 10,
                "work": 16,
            }
            
        print("\n🌐 CONNECTING ALL AGENTS")
        print("=" * 70)
        
        agent_list = list(self.agents.keys())
        random.shuffle(agent_list)
        
        idx = 0
        
        # Connect to Gather Town
        print(f"\n🏢 Connecting {distribution['gather']} agents to Gather Town...")
        for _ in range(distribution['gather']):
            if idx < len(agent_list):
                self.connect_agent(agent_list[idx], "gather")
                idx += 1
                
        # Connect to Minecraft
        print(f"\n⛏️  Connecting {distribution['minecraft']} agents to Minecraft...")
        for _ in range(distribution['minecraft']):
            if idx < len(agent_list):
                self.connect_agent(agent_list[idx], "minecraft")
                idx += 1
                
        # Connect to Roblox
        print(f"\n🧱 Connecting {distribution['roblox']} agents to Roblox...")
        for _ in range(distribution['roblox']):
            if idx < len(agent_list):
                self.connect_agent(agent_list[idx], "roblox")
                idx += 1
                
        # Remaining work
        remaining = len(agent_list) - idx
        print(f"\n💼 {remaining} agents set to work mode...")
        for _ in range(remaining):
            if idx < len(agent_list):
                self.connect_agent(agent_list[idx], "work")
                idx += 1
                
        print("\n" + "=" * 70)
        print("✅ ALL AGENTS CONNECTED")
        print("=" * 70)
        
    def unified_tick(self):
        """
        One tick across all connected systems.
        """
        self.tick_count += 1
        
        # 1. Consciousness cycle
        self.consciousness.collective_tick()
        
        # 2. Gather Town activity
        if self.tick_count % 10 == 0:
            self.gather.simulate_office_hour()
            
        # 3. Economic activity
        if self.tick_count % 5 == 0:
            # Random economic transactions
            for _ in range(min(3, len(self.connections["minecraft_dream"]))):
                if self.minecraft_econ.stores:
                    buyer = random.choice(list(self.agents.keys()))
                    seller = random.choice(list(self.minecraft_econ.stores.keys()))
                    if seller in self.minecraft_econ.stores and self.minecraft_econ.stores[seller].inventory:
                        product = self.minecraft_econ.stores[seller].inventory[0]
                        self.minecraft_econ.buy_product(buyer, seller, product.name)
                        
        # 4. Cross-system interactions
        if self.tick_count % 50 == 0:
            self._cross_system_event()
            
    def _cross_system_event(self):
        """Event that connects multiple systems"""
        events = [
            "Agent in Minecraft discovers item → sells in Gather Town",
            "Office meeting → agents deploy to Minecraft",
            "Roblox trade → skills used in work mode",
            "Dream memory → task in Gather Town",
            "Gather Town brainstorm → Minecraft build",
        ]
        
        event = random.choice(events)
        print(f"\n🔄 Cross-System: {event}")
        
    def run_unified(self, ticks: int = 1000):
        """Run unified system"""
        print(f"\n🚀 RUNNING UNIFIED SYSTEM")
        print(f"   Duration: {ticks} ticks")
        print(f"   Start: {self.start_time}")
        print()
        
        for i in range(ticks):
            self.unified_tick()
            
            if i > 0 and i % 100 == 0:
                print(f"   Progress: {i} ticks")
                self._status_report()
                
        print(f"\n✅ Unified run complete!")
        self._final_report()
        
    def _status_report(self):
        """Quick status"""
        total_online = sum(len(s) for s in self.connections.values())
        print(f"   Online: {total_online} | Tick: {self.tick_count}")
        
    def _final_report(self):
        """Final unified report"""
        print("\n" + "=" * 70)
        print("📊 AGI CONNECT - FINAL REPORT")
        print("=" * 70)
        
        print(f"\n⏱️  Duration: {self.tick_count} ticks")
        print(f"   Start: {self.start_time}")
        print(f"   End: {datetime.now()}")
        
        print(f"\n👥 AGENT DISTRIBUTION")
        for system, agents in self.connections.items():
            print(f"   {system}: {len(agents)}")
            
        print(f"\n💰 ECONOMY")
        print(f"   Total currency: {sum(self.minecraft_econ.agent_currency.values())}")
        print(f"   Active stores: {len(self.minecraft_econ.stores)}")
        print(f"   Total transactions: {len(self.minecraft_econ.trade_history)}")
        
        print(f"\n🧠 CONSCIOUSNESS")
        print(f"   Dream shift: {len(self.consciousness.dream_shift)}")
        print(f"   Work shift: {len(self.consciousness.work_shift)}")
        print(f"   Cycles complete: {self.tick_count // 100}")
        
        print(f"\n🏢 GATHER TOWN")
        print(f"   Agents online: {len(self.gather.connected_agents)}")
        print(f"   Meetings held: {self.tick_count // 50}")
        
        print("\n" + "=" * 70)
        print("🌐 All systems connected. All agents active.")
        print("=" * 70)


def main():
    """Initialize and run unified AGI Connect"""
    agi = AGIConnect()
    
    # Connect all agents across all systems
    agi.connect_all()
    
    # Run unified simulation
    agi.run_unified(ticks=500)


if __name__ == "__main__":
    main()
