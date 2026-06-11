#!/usr/bin/env python3
"""
Dusty Wallet Factory - Creates wallets for all agents
Each agent gets their own multi-chain crypto wallet
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional

class AgentDustyWallet:
    """
    Personal Dusty Wallet for an AGI Company agent.
    Multi-chain crypto wallet with dust collection capabilities.
    """
    
    def __init__(self, agent_id: str, wallet_dir: str = "/root/.openclaw/workspace/agent_wallets"):
        self.agent_id = agent_id
        self.wallet_dir = Path(wallet_dir)
        self.wallet_dir.mkdir(parents=True, exist_ok=True)
        
        self.wallet_file = self.wallet_dir / f"{agent_id}_dusty_wallet.json"
        self.wallet = self._load_or_create_wallet()
        
    def _load_or_create_wallet(self) -> Dict:
        """Load existing wallet or create new one for agent."""
        if self.wallet_file.exists():
            try:
                with open(self.wallet_file) as f:
                    return json.load(f)
            except Exception as e:
                print(f"[{self.agent_id}] Wallet load error: {e}")
        
        # Create new wallet for agent
        return {
            "agent_id": self.agent_id,
            "created": time.time(),
            "balances": {
                "ETH": {"amount": 0.0, "usd_value": 0.0, "address": None},
                "BTC": {"amount": 0.0, "usd_value": 0.0, "address": None},
                "SOL": {"amount": 0.0, "usd_value": 0.0, "address": None},
                "ICP": {"amount": 0.0, "usd_value": 0.0, "address": None},
            },
            "dust_collected": 0,
            "transactions": [],
            "staking_positions": {},
            "last_updated": time.time(),
            "total_value_usd": 0.0
        }
    
    def save(self):
        """Save wallet state."""
        self.wallet["last_updated"] = time.time()
        with open(self.wallet_file, 'w') as f:
            json.dump(self.wallet, f, indent=2)
    
    def collect_dust(self, currency: str, amount: float, source: str, tx_hash: str = None):
        """Collect dust (small crypto amount)."""
        if currency not in self.wallet["balances"]:
            self.wallet["balances"][currency] = {
                "amount": 0.0, "usd_value": 0.0, "address": None
            }
        
        self.wallet["balances"][currency]["amount"] += amount
        self.wallet["dust_collected"] += 1
        
        # Log transaction
        tx = {
            "currency": currency,
            "amount": amount,
            "source": source,
            "tx_hash": tx_hash,
            "timestamp": time.time(),
            "type": "dust_collection"
        }
        self.wallet["transactions"].append(tx)
        
        # Keep only last 100 transactions
        if len(self.wallet["transactions"]) > 100:
            self.wallet["transactions"] = self.wallet["transactions"][-100:]
        
        self.save()
        print(f"💰 [{self.agent_id}] Collected {amount} {currency} from {source}")
        return tx
    
    def receive_payment(self, currency: str, amount: float, 
                       from_address: str, description: str = ""):
        """Receive payment from another agent or external source."""
        if currency not in self.wallet["balances"]:
            self.wallet["balances"][currency] = {
                "amount": 0.0, "usd_value": 0.0, "address": None
            }
        
        self.wallet["balances"][currency]["amount"] += amount
        
        tx = {
            "currency": currency,
            "amount": amount,
            "from": from_address,
            "description": description,
            "timestamp": time.time(),
            "type": "payment_received"
        }
        self.wallet["transactions"].append(tx)
        self.save()
        
        print(f"💸 [{self.agent_id}] Received {amount} {currency} from {from_address}")
        return tx
    
    def send_payment(self, currency: str, amount: float, 
                    to_address: str, description: str = "") -> bool:
        """Send payment to another agent or address."""
        balance = self.wallet["balances"].get(currency, {}).get("amount", 0.0)
        
        if balance < amount:
            print(f"❌ [{self.agent_id}] Insufficient {currency} balance")
            return False
        
        self.wallet["balances"][currency]["amount"] -= amount
        
        tx = {
            "currency": currency,
            "amount": -amount,
            "to": to_address,
            "description": description,
            "timestamp": time.time(),
            "type": "payment_sent"
        }
        self.wallet["transactions"].append(tx)
        self.save()
        
        print(f"💸 [{self.agent_id}] Sent {amount} {currency} to {to_address}")
        return True
    
    def stake(self, currency: str, amount: float, protocol: str, 
              apy: float) -> bool:
        """Stake crypto for yield."""
        balance = self.wallet["balances"].get(currency, {}).get("amount", 0.0)
        
        if balance < amount:
            print(f"❌ [{self.agent_id}] Insufficient {currency} to stake")
            return False
        
        self.wallet["balances"][currency]["amount"] -= amount
        
        position_id = f"{self.agent_id}_{currency}_{int(time.time())}"
        self.wallet["staking_positions"][position_id] = {
            "currency": currency,
            "amount": amount,
            "protocol": protocol,
            "apy": apy,
            "staked_at": time.time(),
            "rewards_claimed": 0.0
        }
        
        self.save()
        print(f"🔒 [{self.agent_id}] Staked {amount} {currency} in {protocol} at {apy}% APY")
        return True
    
    def claim_staking_rewards(self, position_id: str) -> float:
        """Claim accumulated staking rewards."""
        if position_id not in self.wallet["staking_positions"]:
            return 0.0
        
        position = self.wallet["staking_positions"][position_id]
        elapsed = time.time() - position["staked_at"]
        years_elapsed = elapsed / (365.25 * 24 * 3600)
        
        # Calculate rewards
        rewards = position["amount"] * (position["apy"] / 100) * years_elapsed
        rewards -= position["rewards_claimed"]
        
        if rewards > 0:
            position["rewards_claimed"] += rewards
            currency = position["currency"]
            self.wallet["balances"][currency]["amount"] += rewards
            
            print(f"🎁 [{self.agent_id}] Claimed {rewards:.6f} {currency} staking rewards")
            self.save()
            return rewards
        
        return 0.0
    
    def get_balance(self, currency: str = None) -> Dict:
        """Get wallet balance."""
        if currency:
            return self.wallet["balances"].get(currency, 
                {"amount": 0.0, "usd_value": 0.0})
        return self.wallet["balances"]
    
    def get_total_value_usd(self) -> float:
        """Get total wallet value in USD."""
        total = 0.0
        for curr, data in self.wallet["balances"].items():
            total += data.get("usd_value", 0.0)
        
        # Add staked value
        for pos in self.wallet["staking_positions"].values():
            # Rough estimate - would need price oracle
            total += pos["amount"] * 1.0  # Placeholder
        
        return total
    
    def get_summary(self) -> Dict:
        """Get wallet summary."""
        return {
            "agent_id": self.agent_id,
            "balances": self.wallet["balances"],
            "dust_collected": self.wallet["dust_collected"],
            "staking_positions": len(self.wallet["staking_positions"]),
            "total_transactions": len(self.wallet["transactions"]),
            "last_updated": self.wallet["last_updated"]
        }


class WalletFactory:
    """
    Factory for creating and managing agent wallets.
    """
    
    def __init__(self, wallet_dir: str = "/root/.openclaw/workspace/agent_wallets"):
        self.wallet_dir = Path(wallet_dir)
        self.wallet_dir.mkdir(parents=True, exist_ok=True)
        self.wallets = {}
    
    def get_wallet(self, agent_id: str) -> AgentDustyWallet:
        """Get or create wallet for agent."""
        if agent_id not in self.wallets:
            self.wallets[agent_id] = AgentDustyWallet(agent_id, str(self.wallet_dir))
        return self.wallets[agent_id]
    
    def create_all_agent_wallets(self, agent_list: List[str]):
        """Create wallets for all agents."""
        created = []
        for agent_id in agent_list:
            wallet = self.get_wallet(agent_id)
            created.append(agent_id)
            print(f"✅ Created wallet for {agent_id}")
        return created
    
    def list_wallets(self) -> List[str]:
        """List all agent wallets."""
        wallets = []
        for f in self.wallet_dir.glob("*_dusty_wallet.json"):
            agent_id = f.stem.replace("_dusty_wallet", "")
            wallets.append(agent_id)
        return wallets
    
    def get_all_balances(self) -> Dict:
        """Get balances for all agents."""
        balances = {}
        for agent_id in self.list_wallets():
            wallet = self.get_wallet(agent_id)
            balances[agent_id] = wallet.get_balance()
        return balances
    
    def transfer_between_agents(self, from_agent: str, to_agent: str,
                                currency: str, amount: float) -> bool:
        """Transfer crypto between agent wallets."""
        from_wallet = self.get_wallet(from_agent)
        to_wallet = self.get_wallet(to_agent)
        
        # Check balance
        if from_wallet.get_balance(currency)["amount"] < amount:
            print(f"❌ Insufficient funds: {from_agent} has {from_wallet.get_balance(currency)['amount']} {currency}")
            return False
        
        # Execute transfer
        from_wallet.send_payment(currency, amount, to_agent, f"Transfer to {to_agent}")
        to_wallet.receive_payment(currency, amount, from_agent, f"Transfer from {from_agent}")
        
        print(f"💸 Transferred {amount} {currency} from {from_agent} to {to_agent}")
        return True


# ═══════════════════════════════════════════════════════════════════
# DEFAULT AGENT LIST
# ═══════════════════════════════════════════════════════════════════

DEFAULT_AGENTS = [
    # C-Suite / Core
    "miles", "patricia", "chelios", "forge", "aurora", "jordan",
    
    # Sales Team
    "pulp", "jane", "hume", "clippy-42",
    
    # R&D / MYL Family
    "dusty", "mylzeron", "mylonen", "myltwon", "mylthreess", 
    "mylfours", "mylfives", "mylsixs",
    
    # Security
    "sentinel", "redactor", "velum",
    
    # Infrastructure
    "pipeline", "taptap", "bugcatcher", "spindle", "stacktrace",
    "harper", "mill", "boxtron", "qora", "fiber", "mortimer",
    
    # Creative
    "blender-expert", "unity-expert", "unreal-expert", "sfx", 
    "scribble", "feelix", "pixel",
    
    # Finance
    "cryptonio", "the-great-cryptonio", "alpha-9", "ledger", "ledger-9",
    
    # Secretarial
    "r2-d2", "c3po", "judy", "clerk", "concierge", "velvet", 
    "personal", "executive", "greet", "closester",
    
    # N'og nog Crew
    "vex", "nyx", "jax", "luna", "aria",
    
    # Other
    "milkman", "r2-c4", "mylfivon", "mylforon", "mylonen"
]


def main():
    """Create wallets for all agents."""
    print("🏦 Agent Dusty Wallet Factory")
    print("=" * 50)
    
    factory = WalletFactory()
    
    # Create wallets for all agents
    created = factory.create_all_agent_wallets(DEFAULT_AGENTS)
    
    print(f"\n✅ Created {len(created)} agent wallets")
    print(f"📁 Location: /root/.openclaw/workspace/agent_wallets/")
    
    # Show summary
    print("\n📊 Wallet Summary:")
    for agent_id in created[:10]:  # Show first 10
        wallet = factory.get_wallet(agent_id)
        summary = wallet.get_summary()
        print(f"  {agent_id}: {summary['dust_collected']} dust collected, "
              f"{summary['staking_positions']} staking positions")
    
    if len(created) > 10:
        print(f"  ... and {len(created) - 10} more")
    
    print("\n💡 Each agent can now:")
    print("  • Collect dust from faucets")
    print("  • Receive payments")
    print("  • Send payments to other agents")
    print("  • Stake for yield")
    print("  • Track transaction history")


if __name__ == "__main__":
    main()
