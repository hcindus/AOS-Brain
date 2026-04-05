"""
Roblox Agent Economy
Adapted for Roblox features:
- Robux currency
- Marketplace trading
- Game passes
- Developer products
- Group economy
- Social features
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import random


class RobloxItemType(Enum):
    """Roblox item types"""
    ACCESSORY = "accessory"
    GEAR = "gear"
    CLOTHING = "clothing"
    EMOTE = "emote"
    BADGE = "badge"
    GAMEPASS = "gamepass"


class RobuxTransactionType(Enum):
    """Types of Robux transactions"""
    SALE = "sale"  # Item sale
    TRADE = "trade"  # Player trade
    PAYOUT = "payout"  # Group payout
    MARKETPLACE = "marketplace"  # Marketplace fee


@dataclass
class RobloxItem:
    """An item in Roblox"""
    name: str
    item_type: RobloxItemType
    rarity: int  # 1-10
    creator: str
    price: int  # In Robux
    limited: bool = False


@dataclass
class RobuxTransaction:
    """Robux transaction"""
    from_agent: str
    to_agent: str
    amount: int
    transaction_type: RobuxTransactionType
    item: Optional[str] = None


class RobloxAgentEconomy:
    """
    Economy system adapted for Roblox.
    
    Features:
    - Robux currency
    - Limited items (scarcity)
    - Marketplace trading
    - Game passes
    - Group revenue sharing
    """
    
    def __init__(self, agents: Dict):
        self.agents = agents
        
        # Robux balances
        self.robux: Dict[str, int] = {aid: random.randint(50, 500) for aid in agents}
        
        # Inventories
        self.inventories: Dict[str, List[RobloxItem]] = {aid: [] for aid in agents}
        
        # Marketplace
        self.marketplace: List[RobloxItem] = []
        self.trade_history: List[RobuxTransaction] = []
        
        # Groups (teams of agents)
        self.groups: Dict[str, Dict] = {}
        
        # Game passes owned
        self.gamepasses: Dict[str, List[str]] = {aid: [] for aid in agents}
        
        self._initialize_items()
        
    def _initialize_items(self):
        """Create initial items"""
        items = [
            RobloxItem("Epic Sword", RobloxItemType.GEAR, 8, "game", 250, True),
            RobloxItem("Crown", RobloxItemType.ACCESSORY, 10, "game", 500, True),
            RobloxItem("Ninja Outfit", RobloxItemType.CLOTHING, 6, "game", 100, False),
            RobloxItem("Dance Emote", RobloxItemType.EMOTE, 4, "game", 50, False),
            RobloxItem("VIP Badge", RobloxItemType.BADGE, 9, "game", 1000, True),
        ]
        
        # Distribute to agents
        for agent_id in self.agents:
            if random.random() < 0.3:
                item = random.choice(items)
                self.inventories[agent_id].append(item)
                
        # Add some to marketplace
        for _ in range(10):
            self.marketplace.append(random.choice(items))
            
    def list_item_on_marketplace(self, agent_id: str, item_name: str, price: int) -> bool:
        """Agent lists item for sale on marketplace"""
        if agent_id not in self.inventories:
            return False
            
        # Find item
        for item in self.inventories[agent_id]:
            if item.name == item_name:
                # List it
                self.marketplace.append(item)
                self.inventories[agent_id].remove(item)
                return True
                
        return False
        
    def buy_from_marketplace(self, buyer_id: str, item_name: str) -> bool:
        """Buy item from marketplace"""
        # Find item
        item = None
        for i in self.marketplace:
            if i.name == item_name:
                item = i
                break
                
        if not item:
            return False
            
        # Check funds
        if self.robux[buyer_id] < item.price:
            return False
            
        # Transaction
        self.robux[buyer_id] -= item.price
        
        # Creator gets 70%, platform keeps 30%
        creator_share = int(item.price * 0.7)
        if item.creator in self.robux:
            self.robux[item.creator] += creator_share
            
        # Transfer item
        self.marketplace.remove(item)
        self.inventories[buyer_id].append(item)
        
        # Record
        self.trade_history.append(RobuxTransaction(
            from_agent=buyer_id,
            to_agent=item.creator,
            amount=item.price,
            transaction_type=RobuxTransactionType.MARKETPLACE,
            item=item.name,
        ))
        
        return True
        
    def trade_items(self, agent_a: str, agent_b: str, 
                   item_a: str, item_b: Optional[str] = None,
                   robux_a: int = 0, robux_b: int = 0) -> bool:
        """Direct trade between agents"""
        # Check both have items
        if not any(i.name == item_a for i in self.inventories[agent_a]):
            return False
        if item_b and not any(i.name == item_b for i in self.inventories[agent_b]):
            return False
            
        # Check Robux
        if self.robux[agent_a] < robux_a:
            return False
        if self.robux[agent_b] < robux_b:
            return False
            
        # Execute trade
        self.robux[agent_a] -= robux_a
        self.robux[agent_b] += robux_a
        self.robux[agent_b] -= robux_b
        self.robux[agent_a] += robux_b
        
        # Swap items
        item_a_obj = next(i for i in self.inventories[agent_a] if i.name == item_a)
        self.inventories[agent_a].remove(item_a_obj)
        self.inventories[agent_b].append(item_a_obj)
        
        if item_b:
            item_b_obj = next(i for i in self.inventories[agent_b] if i.name == item_b)
            self.inventories[agent_b].remove(item_b_obj)
            self.inventories[agent_a].append(item_b_obj)
            
        # Record
        self.trade_history.append(RobuxTransaction(
            from_agent=agent_a,
            to_agent=agent_b,
            amount=robux_a - robux_b,
            transaction_type=RobuxTransactionType.TRADE,
            item=item_a if not item_b else f"{item_a}↔{item_b}",
        ))
        
        return True
        
    def create_group(self, creator_id: str, group_name: str) -> str:
        """Create a Roblox group"""
        group_id = f"group_{len(self.groups)}"
        
        self.groups[group_id] = {
            "name": group_name,
            "creator": creator_id,
            "members": [creator_id],
            "funds": 0,
            "revenue_share": 0.5,  # 50% to members
        }
        
        return group_id
        
    def join_group(self, agent_id: str, group_id: str) -> bool:
        """Agent joins group"""
        if group_id not in self.groups:
            return False
        if agent_id in self.groups[group_id]["members"]:
            return False
            
        self.groups[group_id]["members"].append(agent_id)
        return True
        
    def distribute_group_funds(self, group_id: str):
        """Distribute group revenue to members"""
        if group_id not in self.groups:
            return
            
        group = self.groups[group_id]
        if group["funds"] <= 0:
            return
            
        # Share to members
        share = group["funds"] * group["revenue_share"] / len(group["members"])
        for member in group["members"]:
            self.robux[member] += int(share)
            
        group["funds"] = 0
        
    def get_wealth_ranking(self) -> List[Tuple[str, int]]:
        """Get agents ranked by Robux wealth"""
        return sorted(
            self.robux.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
    def get_market_summary(self) -> Dict:
        """Get marketplace summary"""
        total_robux = sum(self.robux.values())
        total_items = sum(len(inv) for inv in self.inventories.values())
        
        # Rarity distribution
        limited_count = sum(1 for item in self.marketplace if item.limited)
        
        return {
            "total_robux": total_robux,
            "average_wealth": total_robux / len(self.agents),
            "marketplace_items": len(self.marketplace),
            "limited_items": limited_count,
            "total_items_owned": total_items,
            "trades_today": len([t for t in self.trade_history]),
        }
        
    def simulate_day(self):
        """Simulate one day of Roblox economy"""
        # Random transactions
        for _ in range(random.randint(5, 15)):
            agent_a = random.choice(list(self.agents.keys()))
            agent_b = random.choice([a for a in self.agents if a != agent_a])
            
            action = random.choice(["buy", "trade", "list", "earn"])
            
            if action == "buy" and self.marketplace:
                item = random.choice(self.marketplace)
                self.buy_from_marketplace(agent_a, item.name)
                
            elif action == "trade":
                if self.inventories[agent_a] and self.inventories[agent_b]:
                    item_a = random.choice(self.inventories[agent_a]).name
                    item_b = random.choice(self.inventories[agent_b]).name
                    self.trade_items(agent_a, agent_b, item_a, item_b)
                    
            elif action == "earn":
                # Play game, earn Robux
                self.robux[agent_a] += random.randint(5, 50)
                
        # Distribute group funds
        for group_id in self.groups:
            self.groups[group_id]["funds"] += random.randint(100, 500)
            self.distribute_group_funds(group_id)


if __name__ == "__main__":
    print("Roblox Agent Economy")
    print("=" * 60)
    
    # Mock agents
    from multi_agent import MultiAgentMinecraft
    multi = MultiAgentMinecraft(None)
    agents = multi.spawn_all_agents()
    
    # Create Roblox economy
    rbx_econ = RobloxAgentEconomy(agents)
    
    print(f"\nCreated Roblox economy for {len(agents)} agents")
    print(f"Total Robux: {sum(rbx_econ.robux.values())}")
    print(f"Marketplace items: {len(rbx_econ.marketplace)}")
    
    # Simulate days
    for day in range(5):
        rbx_econ.simulate_day()
        
    # Report
    summary = rbx_econ.get_market_summary()
    print(f"\n📊 After 5 days:")
    print(f"   Total Robux: {summary['total_robux']}")
    print(f"   Avg Wealth: {summary['average_wealth']:.0f}")
    print(f"   Trades: {summary['trades_today']}")
    
    print("\n🏆 Top Wealth:")
    for i, (agent, wealth) in enumerate(rbx_econ.get_wealth_ranking()[:5], 1):
        print(f"   {i}. {agent}: {wealth} Robux")
