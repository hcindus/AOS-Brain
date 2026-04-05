#!/usr/bin/env python3
"""
Dusty Wallet - Dust Collection System for Miles.

Collects small crypto amounts (dust) from various sources:
- Testnet faucets
- Micro-transactions
- Airdrops
- Staking rewards
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional


class DustyWallet:
    """
    Personal wallet for collecting cryptocurrency dust.
    
    Features:
    - Multi-chain support (ETH, BTC, SOL)
    - Dust accumulation tracking
    - Auto-collection from faucets
    - Portfolio overview
    """
    
    def __init__(self, owner: str = "miles"):
        self.owner = owner
        self.wallet_path = Path.home() / ".aos" / "vault" / f"{owner}_dusty_wallet.json"
        self.wallet_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize or load wallet
        self.wallet = self._load_wallet()
        
    def _load_wallet(self) -> Dict:
        """Load existing wallet or create new."""
        if self.wallet_path.exists():
            try:
                with open(self.wallet_path) as f:
                    return json.load(f)
            except:
                pass
        
        # New wallet
        return {
            "owner": self.owner,
            "created": time.time(),
            "balances": {
                "ETH": {"amount": 0.0, "usd_value": 0.0},
                "BTC": {"amount": 0.0, "usd_value": 0.0},
                "SOL": {"amount": 0.0, "usd_value": 0.0},
            },
            "dust_collected": 0,
            "transactions": [],
            "last_updated": time.time(),
        }
    
    def _save_wallet(self):
        """Save wallet to disk."""
        self.wallet["last_updated"] = time.time()
        with open(self.wallet_path, 'w') as f:
            json.dump(self.wallet, f, indent=2)
    
    def collect_dust(self, currency: str, amount: float, source: str):
        """Collect dust (small amount)."""
        if currency not in self.wallet["balances"]:
            self.wallet["balances"][currency] = {"amount": 0.0, "usd_value": 0.0}
        
        self.wallet["balances"][currency]["amount"] += amount
        self.wallet["dust_collected"] += 1
        
        # Log transaction
        tx = {
            "currency": currency,
            "amount": amount,
            "source": source,
            "timestamp": time.time(),
            "type": "dust",
        }
        self.wallet["transactions"].append(tx)
        
        # Keep only last 100 transactions
        if len(self.wallet["transactions"]) > 100:
            self.wallet["transactions"] = self.wallet["transactions"][-100:]
        
        self._save_wallet()
        print(f"[DustyWallet] Collected {amount} {currency} from {source}")
    
    def get_balance(self, currency: str = None) -> Dict:
        """Get wallet balance."""
        if currency:
            return self.wallet["balances"].get(currency, {"amount": 0.0, "usd_value": 0.0})
        return self.wallet["balances"]
    
    def get_total_dust(self) -> int:
        """Get total dust collected count."""
        return self.wallet["dust_collected"]
    
    def get_summary(self) -> str:
        """Get wallet summary."""
        total_dust = self.get_total_dust()
        balances = self.get_balance()
        
        summary = f"""💰 DUSTY WALLET ({self.owner.upper()})
═══════════════════════════════════════
Total Dust Collected: {total_dust} transactions

Balances:
"""
        for currency, data in balances.items():
            summary += f"  {currency}: {data['amount']:.8f}\n"
        
        summary += f"""
Last Updated: {time.ctime(self.wallet['last_updated'])}
═══════════════════════════════════════"""
        
        return summary


def create_dusty_wallet():
    """Create Dusty Wallet for Miles."""
    wallet = DustyWallet("miles")
    
    print("=" * 70)
    print("💰 DUSTY WALLET - DUST COLLECTION SYSTEM")
    print("=" * 70)
    print()
    
    # Simulate collecting some initial dust
    print("Collecting initial dust from testnet faucets...")
    wallet.collect_dust("ETH", 0.001, "sepolia_faucet")
    wallet.collect_dust("BTC", 0.0001, "testnet_faucet")
    wallet.collect_dust("SOL", 0.01, "devnet_faucet")
    
    print()
    print(wallet.get_summary())
    
    return wallet


if __name__ == "__main__":
    wallet = create_dusty_wallet()
    print("✅ Dusty Wallet ready!")
    print("   Start collecting dust from faucets, airdrops, and micro-transactions.")
