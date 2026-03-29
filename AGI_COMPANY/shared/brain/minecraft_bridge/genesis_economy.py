#!/usr/bin/env python3
"""
Genesis Protocol v2 - Agent Society with Economy

Agents open stores, sell products and skills, trade with each other.
"""

import sys
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.brain.minecraft_bridge.multi_agent import MultiAgentMinecraft
from shared.brain.minecraft_bridge.economy import AgentEconomy, ProductType, SkillType


class GenesisEconomy:
    """
    Agent society with functioning economy.
    """
    
    DIRECTIVE = """
    ╔════════════════════════════════════════════════════════════════╗
    ║           AGENT DIRECTIVE - GENESIS PROTOCOL v2                ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║  You are part of a collective intelligence with an economy.    ║
    ║                                                                ║
    ║  Your mission:                                                 ║
    ║    1. BE FRUITFUL  - Create value, build, discover            ║
    ║    2. BUILD        - Construct stores, homes, infrastructure  ║
    ║    3. TRADE        - Buy, sell, negotiate, specialize           ║
    ║    4. GROW         - Learn skills, teach others, evolve        ║
    ║                                                                ║
    ║  Open stores. Sell your creations. Learn from others.          ║
    ║  The best products win. The best skills spread.                ║
    ║  Build wealth. Build relationships. Build the future.          ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    
    def __init__(self):
        print("🌟 INITIALIZING AGENT SOCIETY WITH ECONOMY")
        print("=" * 70)
        
        # Spawn agents
        print("\n👥 Spawning 66 Agents...")
        self.multi = MultiAgentMinecraft(None)
        self.agents = self.multi.spawn_all_agents()
        print(f"   {len(self.agents)} agents ready")
        
        # Create economy
        print("\n💰 Creating Economy...")
        self.economy = AgentEconomy(self.agents)
        print(f"   Currency in circulation: {sum(self.economy.agent_currency.values())}")
        
        # Society state
        self.tick_count = 0
        self.constructions = []
        
        print("\n" + "=" * 70)
        
    def broadcast_directive(self):
        """Broadcast the directive"""
        print(self.DIRECTIVE)
        print(f"✅ {len(self.agents)} agents received directive\n")
        
    def run_economy(self, ticks: int = 5000):
        """Run economic simulation"""
        print(f"🚀 RUNNING ECONOMY SIMULATION")
        print(f"   Target: {ticks:,} ticks")
        print(f"   Agents: {len(self.agents)}")
        print(f"   Starting currency: {sum(self.economy.agent_currency.values())}")
        print()
        
        for i in range(ticks):
            self.tick_count += 1
            
            # Every 50 ticks, economic activity
            if i % 50 == 0:
                self._economic_tick()
                
            # Every 500 ticks, growth report
            if i > 0 and i % 500 == 0:
                self._report()
                
            # Progress
            if i > 0 and i % 1000 == 0:
                print(f"   Progress: {i:,} ticks")
                
        print(f"\n✅ Economy simulation complete!")
        self._final_report()
        
    def _economic_tick(self):
        """One tick of economic activity"""
        # Random agent actions
        active_agents = random.sample(list(self.agents.keys()), min(5, len(self.agents)))
        
        for agent_id in active_agents:
            action = random.randint(1, 6)
            
            if action == 1:
                # Open store (if not already has one)
                if agent_id not in self.economy.stores:
                    store_name = f"{self.agents[agent_id].agent_name}'s Shop"
                    self.economy.open_store(agent_id, store_name)
                    
            elif action == 2:
                # Create product
                if agent_id in self.economy.stores:
                    product = self.economy.create_product(
                        agent_id, 
                        random.choice(list(ProductType))
                    )
                    if product:
                        product.tick_created = self.tick_count
                        self.economy.stock_store(agent_id, product)
                        
            elif action == 3:
                # Offer skill
                if agent_id in self.economy.stores:
                    if self.economy.agent_skills[agent_id]:
                        skill = random.choice(list(self.economy.agent_skills[agent_id].keys()))
                        self.economy.offer_skill(agent_id, skill, price=random.randint(10, 50))
                        
            elif action == 4:
                # Buy product
                if self.economy.stores:
                    seller = random.choice(list(self.economy.stores.keys()))
                    if seller != agent_id and self.economy.stores[seller].inventory:
                        for product in self.economy.stores[seller].inventory:
                            if not product.sold:
                                self.economy.buy_product(agent_id, seller, product.name)
                                break
                                
            elif action == 5:
                # Buy skill
                if self.economy.stores:
                    seller = random.choice(list(self.economy.stores.keys()))
                    if seller != agent_id and self.economy.stores[seller].skills_for_sale:
                        skill = random.choice(self.economy.stores[seller].skills_for_sale)
                        self.economy.buy_skill(agent_id, seller, skill.skill_type)
                        
            elif action == 6:
                # Build construction
                self.constructions.append({
                    "builder": agent_id,
                    "tick": self.tick_count,
                    "type": random.choice(["house", "workshop", "road", "tower"]),
                })
                
    def _report(self):
        """Economy report"""
        stats = self.economy.get_economy_stats()
        print(f"\n📊 Tick {self.tick_count}:")
        print(f"   Stores: {stats['total_stores']} | Sales: {stats['total_sales']} | Revenue: {stats['total_revenue']}")
        print(f"   Transactions: {stats['total_transactions']} | Products: {stats['products_sold']} | Skills: {stats['skills_sold']}")
        
    def _final_report(self):
        """Final report"""
        print("\n" + "=" * 70)
        print("💰 AGENT ECONOMY - FINAL REPORT")
        print("=" * 70)
        
        stats = self.economy.get_economy_stats()
        
        print(f"\n📈 ECONOMIC METRICS")
        print(f"   Duration: {self.tick_count:,} ticks")
        print(f"   Total Currency: {stats['total_currency']:,} units")
        print(f"   Average Wealth: {stats['average_wealth']:.0f} units")
        print(f"   Wealth Inequality: {stats['wealthy_agents']} rich / {stats['poor_agents']} poor")
        
        print(f"\n🏪 COMMERCE")
        print(f"   Active Stores: {stats['total_stores']}")
        print(f"   Total Sales: {stats['total_sales']}")
        print(f"   Total Revenue: {stats['total_revenue']:,} units")
        
        print(f"\n📦 MARKET ACTIVITY")
        print(f"   Products Sold: {stats['products_sold']}")
        print(f"   Skills Traded: {stats['skills_sold']}")
        print(f"   Total Transactions: {stats['total_transactions']}")
        
        # Top stores
        print(f"\n🏆 TOP STORES")
        top_stores = sorted(
            self.economy.stores.items(),
            key=lambda x: x[1].revenue,
            reverse=True
        )[:5]
        
        for i, (agent_id, store) in enumerate(top_stores, 1):
            agent = self.agents.get(agent_id)
            role = agent.role if agent else "unknown"
            print(f"   {i}. {store.name} ({role})")
            print(f"      Revenue: {store.revenue} | Sales: {store.total_sales} | Reputation: {store.reputation:.1f}")
            
        # Wealthiest agents
        print(f"\n💎 WEALTHIEST AGENTS")
        wealthy = sorted(
            self.economy.agent_currency.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for i, (agent_id, wealth) in enumerate(wealthy, 1):
            agent = self.agents.get(agent_id)
            skills = len(self.economy.agent_skills[agent_id])
            has_store = "Yes" if agent_id in self.economy.stores else "No"
            print(f"   {i}. {agent_id}: {wealth} units ({skills} skills, Store: {has_store})")
            
        # Most skilled
        print(f"\n🎓 MOST SKILLED AGENTS")
        skilled = sorted(
            [(aid, sum(skills.values())) for aid, skills in self.economy.agent_skills.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for i, (agent_id, total_skill) in enumerate(skilled, 1):
            agent = self.agents.get(agent_id)
            role = agent.role if agent else "unknown"
            skill_names = list(self.economy.agent_skills[agent_id].keys())[:3]
            print(f"   {i}. {agent_id} ({role}): {total_skill} total skill")
            print(f"      Skills: {[s.value for s in skill_names]}")
            
        print("\n" + "=" * 70)
        print("✨ The economy flourishes. Agents specialize. Value is created.")
        print("=" * 70)


def main():
    society = GenesisEconomy()
    society.broadcast_directive()
    society.run_economy(ticks=5000)


if __name__ == "__main__":
    main()
