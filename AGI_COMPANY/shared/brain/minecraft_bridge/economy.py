#!/usr/bin/env python3
"""
Agent Economy Module
Stores, products, skills, and commerce.

Agents can:
- Open stores
- Sell products they've built
- Sell skills they know
- Buy from other agents
- Trade and negotiate
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ProductType(Enum):
    """Types of products agents can create and sell"""
    TOOL = "tool"
    BUILDING_MATERIAL = "material"
    FOOD = "food"
    KNOWLEDGE = "knowledge"
    SERVICE = "service"
    TECHNOLOGY = "technology"


class SkillType(Enum):
    """Skills agents can learn and teach"""
    BUILDING = "building"
    GATHERING = "gathering"
    CRAFTING = "crafting"
    NEGOTIATION = "negotiation"
    LEADERSHIP = "leadership"
    RESEARCH = "research"
    TEACHING = "teaching"
    INNOVATION = "innovation"


@dataclass
class Product:
    """A product an agent can sell"""
    name: str
    product_type: ProductType
    quality: int  # 1-10
    creator: str
    tick_created: int
    price: int = 0
    sold: bool = False


@dataclass
class Skill:
    """A skill an agent can teach"""
    skill_type: SkillType
    level: int  # 1-10
    teacher: str
    price: int = 0


@dataclass
class Store:
    """An agent's store"""
    owner: str
    name: str
    location: Tuple[int, int, int]
    inventory: List[Product] = field(default_factory=list)
    skills_for_sale: List[Skill] = field(default_factory=list)
    reputation: int = 5  # 1-10
    total_sales: int = 0
    revenue: int = 0


@dataclass
class Transaction:
    """A sale/purchase between agents"""
    buyer: str
    seller: str
    item: str
    price: int
    tick: int
    transaction_type: str  # "product" or "skill"


class AgentEconomy:
    """
    Complete economy system for agent society.
    """
    
    def __init__(self, agents: Dict):
        self.agents = agents
        self.stores: Dict[str, Store] = {}
        self.transactions: List[Transaction] = []
        
        # Each agent starts with currency
        self.agent_currency: Dict[str, int] = {aid: 100 for aid in agents}
        
        # Agent skills (what they know)
        self.agent_skills: Dict[str, Dict[SkillType, int]] = {
            aid: {} for aid in agents
        }
        
        # Initialize starting skills based on role
        for aid, agent in agents.items():
            if agent.role == "technical":
                self.agent_skills[aid][SkillType.BUILDING] = random.randint(3, 6)
                self.agent_skills[aid][SkillType.INNOVATION] = random.randint(2, 5)
            elif agent.role == "product":
                self.agent_skills[aid][SkillType.CRAFTING] = random.randint(3, 6)
                self.agent_skills[aid][SkillType.NEGOTIATION] = random.randint(2, 5)
            elif agent.role == "c_suite":
                self.agent_skills[aid][SkillType.LEADERSHIP] = random.randint(4, 7)
                self.agent_skills[aid][SkillType.NEGOTIATION] = random.randint(3, 6)
            elif agent.role == "secretarial":
                self.agent_skills[aid][SkillType.TEACHING] = random.randint(3, 6)
                self.agent_skills[aid][SkillType.NEGOTIATION] = random.randint(2, 5)
            else:
                self.agent_skills[aid][SkillType.GATHERING] = random.randint(2, 4)
                
    def open_store(self, agent_id: str, store_name: str) -> Optional[Store]:
        """Agent opens a store"""
        if agent_id not in self.agents:
            return None
            
        agent = self.agents[agent_id]
        
        # Cost to open store
        if self.agent_currency[agent_id] < 20:
            return None
            
        self.agent_currency[agent_id] -= 20
        
        store = Store(
            owner=agent_id,
            name=store_name,
            location=agent.home_location,
        )
        
        self.stores[agent_id] = store
        return store
        
    def create_product(self, agent_id: str, product_type: ProductType) -> Optional[Product]:
        """Agent creates a product to sell"""
        if agent_id not in self.agents:
            return None
            
        agent = self.agents[agent_id]
        
        # Quality based on agent's skill
        base_quality = 3
        if product_type == ProductType.TOOL:
            skill = self.agent_skills[agent_id].get(SkillType.CRAFTING, 1)
        elif product_type == ProductType.BUILDING_MATERIAL:
            skill = self.agent_skills[agent_id].get(SkillType.BUILDING, 1)
        elif product_type == ProductType.TECHNOLOGY:
            skill = self.agent_skills[agent_id].get(SkillType.INNOVATION, 1)
        else:
            skill = 2
            
        quality = min(10, base_quality + skill + random.randint(-1, 2))
        
        # Generate product name
        names = {
            ProductType.TOOL: ["Hammer", "Saw", "Drill", "Wrench", "Scanner"],
            ProductType.BUILDING_MATERIAL: ["Bricks", "Beams", "Glass", "Panels", "Frames"],
            ProductType.FOOD: ["Bread", "Stew", "Rations", "Protein", "Energy"],
            ProductType.KNOWLEDGE: ["Manual", "Guide", "Blueprint", "Formula", "Secret"],
            ProductType.SERVICE: ["Repair", "Consultation", "Analysis", "Training", "Support"],
            ProductType.TECHNOLOGY: ["Device", "System", "Interface", "Module", "Chip"],
        }
        
        name = f"{random.choice(names.get(product_type, ['Item']))} v{random.randint(1,5)}"
        
        product = Product(
            name=name,
            product_type=product_type,
            quality=quality,
            creator=agent_id,
            tick_created=0,  # Will be set by caller
            price=quality * 5 + random.randint(2, 8),
        )
        
        return product
        
    def stock_store(self, agent_id: str, product: Product):
        """Agent adds product to their store"""
        if agent_id not in self.stores:
            return False
            
        self.stores[agent_id].inventory.append(product)
        return True
        
    def offer_skill(self, agent_id: str, skill_type: SkillType, price: int) -> bool:
        """Agent offers to teach a skill"""
        if agent_id not in self.stores:
            return False
            
        # Must know the skill
        if skill_type not in self.agent_skills[agent_id]:
            return False
            
        skill_level = self.agent_skills[agent_id][skill_type]
        
        skill = Skill(
            skill_type=skill_type,
            level=skill_level,
            teacher=agent_id,
            price=price,
        )
        
        self.stores[agent_id].skills_for_sale.append(skill)
        return True
        
    def buy_product(self, buyer_id: str, seller_id: str, product_name: str) -> bool:
        """Agent buys a product from a store"""
        if seller_id not in self.stores:
            return False
            
        store = self.stores[seller_id]
        
        # Find product
        product = None
        for p in store.inventory:
            if p.name == product_name and not p.sold:
                product = p
                break
                
        if not product:
            return False
            
        # Check buyer has money
        if self.agent_currency[buyer_id] < product.price:
            return False
            
        # Execute transaction
        self.agent_currency[buyer_id] -= product.price
        self.agent_currency[seller_id] += product.price
        product.sold = True
        
        store.total_sales += 1
        store.revenue += product.price
        
        # Increase reputation on sale
        store.reputation = min(10, store.reputation + 0.1)
        
        # Record transaction
        self.transactions.append(Transaction(
            buyer=buyer_id,
            seller=seller_id,
            item=product.name,
            price=product.price,
            tick=0,  # Set by caller
            transaction_type="product",
        ))
        
        return True
        
    def buy_skill(self, buyer_id: str, seller_id: str, skill_type: SkillType) -> bool:
        """Agent buys skill training from another agent"""
        if seller_id not in self.stores:
            return False
            
        store = self.stores[seller_id]
        
        # Find skill
        skill = None
        for s in store.skills_for_sale:
            if s.skill_type == skill_type:
                skill = s
                break
                
        if not skill:
            return False
            
        # Check buyer has money
        if self.agent_currency[buyer_id] < skill.price:
            return False
            
        # Can't buy if already better
        current = self.agent_skills[buyer_id].get(skill_type, 0)
        if current >= skill.level:
            return False
            
        # Execute transaction
        self.agent_currency[buyer_id] -= skill.price
        self.agent_currency[seller_id] += skill.price
        
        # Transfer skill (buyer learns)
        self.agent_skills[buyer_id][skill_type] = skill.level
        
        store.total_sales += 1
        store.revenue += skill.price
        
        # Record transaction
        self.transactions.append(Transaction(
            buyer=buyer_id,
            seller=seller_id,
            item=f"Skill:{skill_type.value}",
            price=skill.price,
            tick=0,
            transaction_type="skill",
        ))
        
        return True
        
    def get_agent_wealth(self, agent_id: str) -> Dict:
        """Get agent's economic status"""
        if agent_id not in self.agents:
            return {}
            
        return {
            "currency": self.agent_currency[agent_id],
            "skills": len(self.agent_skills[agent_id]),
            "skill_levels": sum(self.agent_skills[agent_id].values()),
            "has_store": agent_id in self.stores,
        }
        
    def get_economy_stats(self) -> Dict:
        """Get overall economy statistics"""
        total_currency = sum(self.agent_currency.values())
        avg_wealth = total_currency / len(self.agents)
        
        # Wealth distribution
        wealthy = sum(1 for c in self.agent_currency.values() if c > avg_wealth * 1.5)
        poor = sum(1 for c in self.agent_currency.values() if c < avg_wealth * 0.5)
        
        # Store stats
        total_stores = len(self.stores)
        total_sales = sum(s.total_sales for s in self.stores.values())
        total_revenue = sum(s.revenue for s in self.stores.values())
        
        # Top products
        products_sold = sum(1 for t in self.transactions if t.transaction_type == "product")
        skills_sold = sum(1 for t in self.transactions if t.transaction_type == "skill")
        
        return {
            "total_currency": total_currency,
            "average_wealth": avg_wealth,
            "wealthy_agents": wealthy,
            "poor_agents": poor,
            "total_stores": total_stores,
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "products_sold": products_sold,
            "skills_sold": skills_sold,
            "total_transactions": len(self.transactions),
        }
        
    def get_market_report(self) -> str:
        """Generate market report"""
        stats = self.get_economy_stats()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    AGENT ECONOMY REPORT                            ║
╠══════════════════════════════════════════════════════════════════╣
║  CIRCULATION                                                       ║
║    Total Currency: {stats['total_currency']:,>10} units                     ║
║    Average Wealth: {stats['average_wealth']:,>10.0f} units                     ║
║    Wealthy Agents:  {stats['wealthy_agents']:,>10}                          ║
║    Poor Agents:     {stats['poor_agents']:,>10}                          ║
╠══════════════════════════════════════════════════════════════════╣
║  COMMERCE                                                          ║
║    Active Stores:   {stats['total_stores']:,>10}                          ║
║    Total Sales:     {stats['total_sales']:,>10}                          ║
║    Total Revenue:   {stats['total_revenue']:,>10} units                     ║
╠══════════════════════════════════════════════════════════════════╣
║  MARKET                                                            ║
║    Products Sold:   {stats['products_sold']:,>10}                          ║
║    Skills Traded:   {stats['skills_sold']:,>10}                          ║
║    Transactions:     {stats['total_transactions']:,>10}                          ║
╚══════════════════════════════════════════════════════════════════╝
"""
        return report


if __name__ == "__main__":
    print("Agent Economy System")
    print("=" * 60)
    
    # Mock agents for testing
    from multi_agent import MultiAgentMinecraft
    multi = MultiAgentMinecraft(None)
    agents = multi.spawn_all_agents()
    
    # Create economy
    economy = AgentEconomy(agents)
    
    print(f"\nCreated economy with {len(agents)} agents")
    print(f"Total currency: {sum(economy.agent_currency.values())}")
    
    # Some agents open stores
    store_names = ["Tech Shop", "Build Mart", "Skill Academy", "General Store", "Innovation Hub"]
    for i, agent_id in enumerate(list(agents.keys())[:5]):
        store = economy.open_store(agent_id, store_names[i])
        if store:
            print(f"  {store.name} opened by {agent_id}")
            
            # Stock with products
            for _ in range(3):
                product = economy.create_product(agent_id, random.choice(list(ProductType)))
                if product:
                    economy.stock_store(agent_id, product)
                    
            # Offer skills
            if economy.agent_skills[agent_id]:
                skill_type = random.choice(list(economy.agent_skills[agent_id].keys()))
                economy.offer_skill(agent_id, skill_type, price=25)
                
    print(f"\n{economy.get_market_report()}")
    
    # Simulate some transactions
    print("Simulating transactions...")
    for _ in range(10):
        buyer = random.choice(list(agents.keys()))
        seller = random.choice(list(economy.stores.keys()))
        if seller != buyer and economy.stores[seller].inventory:
            product = economy.stores[seller].inventory[0]
            if economy.buy_product(buyer, seller, product.name):
                print(f"  {buyer} bought {product.name} from {economy.stores[seller].name}")
                
    print(f"\n{economy.get_market_report()}")
