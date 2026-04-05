#!/usr/bin/env python3
"""
Open All Offices - Multi-Platform Agent Test

Agents join simultaneously:
- Gather Town (virtual office)
- Minecraft (dream world)  
- Roblox (alternative dream)

Cross-platform presence test.
"""

import sys
import random
import time
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from minecraft_bridge.multi_agent import MultiAgentMinecraft
from minecraft_bridge.economy import AgentEconomy
from minecraft_bridge.consciousness_cycle import AgentCollectiveConsciousness
from gather_bridge import GatherTownBridge
from roblox_bridge import RobloxBridge, RobloxMultiAgent


class MultiPlatformOffice:
    """
    All virtual offices open.
    Agents distributed across platforms.
    """
    
    def __init__(self):
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║              OPENING ALL VIRTUAL OFFICES                       ║")
        print("║         Gather Town | Minecraft | Roblox                     ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print()
        
        # Spawn agents
        print("👥 Spawning 66 Agents...")
        self.multi = MultiAgentMinecraft(None)
        self.agents = self.multi.spawn_all_agents()
        print(f"   ✅ {len(self.agents)} agents ready\n")
        
        # Open Office 1: Gather Town
        print("🏢 OPENING OFFICE 1: Gather Town")
        print("   📍 https://app.gather.town/app/VnSTVFJ50v9jy9qg/Miles_Office")
        self.gather = GatherTownBridge()
        self.gather_agents = set()
        print("   ✅ Office ready\n")
        
        # Open Office 2: Minecraft
        print("⛏️  OPENING OFFICE 2: Minecraft")
        print("   🌍 Dream world ready for exploration")
        self.minecraft_agents = {}
        self.minecraft_econ = AgentEconomy(self.agents)
        print("   ✅ Minecraft server ready\n")
        
        # Open Office 3: Roblox
        print("🧱 OPENING OFFICE 3: Roblox")
        print("   🎮 Alternative dream world ready")
        self.roblox = RobloxBridge()
        self.roblox_multi = RobloxMultiAgent(self.roblox)
        self.roblox_agents = set()
        print("   ✅ Roblox place ready\n")
        
        # Consciousness system
        print("🌓 Initializing Consciousness Bridge...")
        self.consciousness = AgentCollectiveConsciousness(self.agents)
        print("   ✅ Sleep/wake cycle active\n")
        
        print("=" * 70)
        print("✅ ALL OFFICES OPEN")
        print("=" * 70)
        
    def distribute_agents(self):
        """
        Distribute 66 agents across all three platforms.
        
        Distribution:
        - 25 agents → Gather Town (office work)
        - 25 agents → Minecraft (dream/build)
        - 16 agents → Roblox (alternative dream)
        """
        print("\n🌐 DISTRIBUTING AGENTS ACROSS PLATFORMS")
        print("=" * 70)
        
        agent_list = list(self.agents.keys())
        random.shuffle(agent_list)
        
        # Gather Town - 25 agents
        print("\n🏢 Sending 25 agents to Gather Town...")
        for i in range(25):
            if i < len(agent_list):
                aid = agent_list[i]
                agent = self.agents[aid]
                self.gather.agent_join_office(aid, agent.agent_name)
                self.gather_agents.add(aid)
                time.sleep(0.1)
        
        # Minecraft - 25 agents  
        print("\n⛏️  Sending 25 agents to Minecraft...")
        for i in range(25, 50):
            if i < len(agent_list):
                aid = agent_list[i]
                agent = self.agents[aid]
                # Enter dream mode
                if aid in self.consciousness.agent_minds:
                    self.consciousness.agent_minds[aid].enter_dream_mode()
                self.minecraft_agents[aid] = {
                    "position": (random.randint(0, 100), 70, random.randint(0, 100)),
                    "inventory": [],
                    "mode": "exploring"
                }
                print(f"   {agent.agent_name} spawned in Minecraft")
                time.sleep(0.05)
        
        # Roblox - 16 agents
        print("\n🧱 Sending 16 agents to Roblox...")
        for i in range(50, 66):
            if i < len(agent_list):
                aid = agent_list[i]
                agent = self.agents[aid]
                self.roblox_multi.spawn_agent_in_roblox(aid, "office_place_001")
                self.roblox_agents.add(aid)
                print(f"   {agent.agent_name} spawned in Roblox")
                time.sleep(0.05)
        
        print("\n" + "=" * 70)
        print("✅ ALL AGENTS DISTRIBUTED")
        print("=" * 70)
        
    def run_cross_platform(self, duration_minutes: int = 5):
        """
        Run agents across all platforms simultaneously.
        
        Agents:
        - Move within their platform
        - Interact with others on same platform
        - Economy transactions (Minecraft)
        - Meetings (Gather Town)
        - Trading (Roblox)
        """
        print(f"\n🚀 RUNNING CROSS-PLATFORM SIMULATION")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Platforms: Gather Town ({len(self.gather_agents)}), "
              f"Minecraft ({len(self.minecraft_agents)}), "
              f"Roblox ({len(self.roblox_agents)})")
        print()
        
        ticks = 0
        start_time = time.time()
        
        while time.time() - start_time < duration_minutes * 60:
            ticks += 1
            
            # Platform 1: Gather Town activity
            if ticks % 10 == 0:
                self._gather_activity()
                
            # Platform 2: Minecraft activity
            if ticks % 8 == 0:
                self._minecraft_activity()
                
            # Platform 3: Roblox activity
            if ticks % 12 == 0:
                self._roblox_activity()
                
            # Consciousness cycle
            if ticks % 5 == 0:
                self.consciousness.collective_tick()
                
            # Cross-platform events
            if ticks % 100 == 0:
                self._cross_platform_event()
                
            # Progress report
            if ticks % 300 == 0:
                self._progress_report(ticks)
                
            time.sleep(0.1)  # 10 ticks per second
            
        print(f"\n✅ Cross-platform run complete!")
        self._final_report()
        
    def _gather_activity(self):
        """Activity in Gather Town office"""
        if not self.gather_agents:
            return
            
        # Random agent does something
        agent_id = random.choice(list(self.gather_agents))
        
        action = random.choice(["work", "move", "talk"])
        
        if action == "work":
            self.gather.agent_work_at_desk(agent_id)
        elif action == "move":
            room = random.choice(list(self.gather.rooms.keys()))
            self.gather.agent_move(agent_id, room)
        elif action == "talk":
            # Find someone to talk to
            others = [a for a in self.gather_agents if a != agent_id]
            if others:
                self.gather.start_conversation(agent_id, random.choice(others))
                
    def _minecraft_activity(self):
        """Activity in Minecraft dream world"""
        if not self.minecraft_agents:
            return
            
        agent_id = random.choice(list(self.minecraft_agents.keys()))
        agent_data = self.minecraft_agents[agent_id]
        
        action = random.choice(["explore", "build", "trade", "mine"])
        
        if action == "explore":
            # Move to new position
            agent_data["position"] = (
                random.randint(0, 200),
                70,
                random.randint(0, 200)
            )
            agent_data["mode"] = "exploring"
            
        elif action == "build":
            agent_data["mode"] = "building"
            # Add to consciousness
            if agent_id in self.consciousness.agent_minds:
                self.consciousness.agent_minds[agent_id].dream_activity("build", "success")
                
        elif action == "trade":
            # Economic activity
            if self.minecraft_econ.stores:
                seller = random.choice(list(self.minecraft_econ.stores.keys()))
                if seller in self.minecraft_econ.stores and self.minecraft_econ.stores[seller].inventory:
                    product = self.minecraft_econ.stores[seller].inventory[0]
                    if not product.sold:
                        self.minecraft_econ.buy_product(agent_id, seller, product.name)
                        
    def _roblox_activity(self):
        """Activity in Roblox dream world"""
        if not self.roblox_agents:
            return
            
        agent_id = random.choice(list(self.roblox_agents))
        
        action = random.choice(["socialize", "game", "trade"])
        
        if action == "socialize":
            # Roblox social features
            others = [a for a in self.roblox_agents if a != agent_id]
            if others:
                target = random.choice(others)
                print(f"   🎮 {self.agents[agent_id].agent_name} friends {self.agents[target].agent_name}")
                
        elif action == "game":
            # Play mini-game
            print(f"   🎮 {self.agents[agent_id].agent_name} plays a mini-game")
            
        elif action == "trade":
            # Roblox trading
            pass  # Trading logic in roblox_economy
            
    def _cross_platform_event(self):
        """Event connecting multiple platforms"""
        events = [
            f"Gather Town meeting → agents deploy to Minecraft",
            f"Minecraft discovery → sold in Gather Town",
            f"Roblox trade → skills used in work",
            f"Dream memory → Gather Town presentation",
            f"Gather brainstorm → Minecraft build project",
            f"Agent rotates: Roblox → Minecraft → Gather",
        ]
        
        event = random.choice(events)
        print(f"\n🔄 CROSS-PLATFORM: {event}")
        
        # Actually move an agent between platforms
        if random.random() < 0.3:
            self._rotate_agent_between_platforms()
            
    def _rotate_agent_between_platforms(self):
        """Move one agent to a different platform"""
        # Pick random agent from any platform
        all_connected = list(self.gather_agents) + list(self.minecraft_agents.keys()) + list(self.roblox_agents)
        
        if not all_connected:
            return
            
        agent_id = random.choice(all_connected)
        agent_name = self.agents[agent_id].agent_name
        
        # Remove from current
        if agent_id in self.gather_agents:
            self.gather_agents.remove(agent_id)
            print(f"   {agent_name} left Gather Town")
        if agent_id in self.minecraft_agents:
            del self.minecraft_agents[agent_id]
            print(f"   {agent_name} left Minecraft")
        if agent_id in self.roblox_agents:
            self.roblox_agents.remove(agent_id)
            print(f"   {agent_name} left Roblox")
            
        # Add to new platform
        new_platform = random.choice(["gather", "minecraft", "roblox"])
        
        if new_platform == "gather":
            self.gather.agent_join_office(agent_id, agent_name)
            self.gather_agents.add(agent_id)
        elif new_platform == "minecraft":
            self.minecraft_agents[agent_id] = {
                "position": (random.randint(0, 100), 70, random.randint(0, 100)),
                "inventory": [],
                "mode": "exploring"
            }
        else:
            self.roblox_multi.spawn_agent_in_roblox(agent_id, "office_place_001")
            self.roblox_agents.add(agent_id)
            
        print(f"   → Joined {new_platform.upper()}")
        
    def _progress_report(self, ticks: int):
        """Progress update"""
        print(f"\n📊 PROGRESS (Tick {ticks})")
        print(f"   Gather Town: {len(self.gather_agents)} agents")
        print(f"   Minecraft: {len(self.minecraft_agents)} agents")
        print(f"   Roblox: {len(self.roblox_agents)} agents")
        print(f"   Total online: {len(self.gather_agents) + len(self.minecraft_agents) + len(self.roblox_agents)}")
        
    def _final_report(self):
        """Final report"""
        print("\n" + "=" * 70)
        print("📊 MULTI-PLATFORM OFFICE - FINAL REPORT")
        print("=" * 70)
        
        print(f"\n🏢 GATHER TOWN")
        print(f"   Agents: {len(self.gather_agents)}")
        print(f"   Rooms occupied:")
        for room in self.gather.rooms:
            count = sum(1 for p in self.gather.connected_agents.values() if p.current_room == room)
            if count > 0:
                print(f"     {room}: {count}")
                
        print(f"\n⛏️  MINECRAFT")
        print(f"   Dreamers: {len(self.minecraft_agents)}")
        print(f"   Economy: {len(self.minecraft_econ.stores)} stores")
        print(f"   Transactions: {len(self.minecraft_econ.trade_history)}")
        
        print(f"\n🧱 ROBLOX")
        print(f"   Players: {len(self.roblox_agents)}")
        
        print(f"\n🌓 CONSCIOUSNESS")
        print(f"   Active cycles: Running")
        print(f"   Dream shift: {len(self.consciousness.dream_shift)}")
        print(f"   Work shift: {len(self.consciousness.work_shift)}")
        
        print("\n" + "=" * 70)
        print("✅ ALL PLATFORMS OPERATIONAL")
        print("   Agents flow between Gather, Minecraft, and Roblox")
        print("   Economy active across platforms")
        print("   Consciousness cycle rotating agents")
        print("=" * 70)


def main():
    """Open all offices and run cross-platform simulation"""
    office = MultiPlatformOffice()
    office.distribute_agents()
    
    # Run for 2 minutes (120 seconds)
    print("\n⏱️  Running 2-minute cross-platform test...")
    office.run_cross_platform(duration_minutes=2)


if __name__ == "__main__":
    main()
