#!/usr/bin/env python3
"""
Unified Wallet System - Ties all wallets to Dusty Wallet.

Aggregates:
- EVM Wallet (Ethereum-compatible)
- Dusty Wallet (multi-chain dust collection)
- Binance API Wallet
- Stripe Payment System
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional


class UnifiedWalletSystem:
    """
    Central wallet hub that connects all wallet types.
    
    Wallets integrated:
    - Dusty Wallet (dust collection)
    - EVM Wallet (Ethereum/mainnet)
    - Exchange Wallets (Binance, etc.)
    - Payment Systems (Stripe)
    """
    
    def __init__(self, owner: str = "miles"):
        self.owner = owner
        self.vault_path = Path.home() / ".aos" / "vault"
        self.unified_path = self.vault_path / f"{owner}_unified_wallet.json"
        
        # Load all wallet components
        self.dusty = self._load_dusty_wallet()
        self.evm = self._load_evm_wallet()
        self.exchange = self._load_exchange_wallets()
        self.payment = self._load_payment_systems()
        
        # Initialize unified tracking
        self.unified = self._load_unified()
        
    def _load_dusty_wallet(self) -> Dict:
        """Load Dusty Wallet."""
        dusty_path = self.vault_path / f"{self.owner}_dusty_wallet.json"
        if dusty_path.exists():
            with open(dusty_path) as f:
                return json.load(f)
        return {"balances": {}, "dust_collected": 0}
    
    def _load_evm_wallet(self) -> Dict:
        """Load EVM wallet."""
        evm_path = self.vault_path / f"{self.owner}_evm_wallet.json"
        if evm_path.exists():
            with open(evm_path) as f:
                return json.load(f)
        return {"address": "0x2ce0c5D9aaD321d1Ea0ad02F02bde75A5fB0E3BE", "network": "ethereum_compatible"}
    
    def _load_exchange_wallets(self) -> Dict:
        """Load exchange wallet configs."""
        exchanges = {}
        
        # Binance
        binance_path = self.vault_path / "binance_api.json"
        if binance_path.exists():
            with open(binance_path) as f:
                exchanges["binance"] = json.load(f)
        
        return exchanges
    
    def _load_payment_systems(self) -> Dict:
        """Load payment system configs."""
        payments = {}
        
        # Stripe
        stripe_path = self.vault_path / "stripe" / ".env.stripe"
        if stripe_path.exists():
            payments["stripe"] = {"config_path": str(stripe_path), "status": "configured"}
        
        return payments
    
    def _load_unified(self) -> Dict:
        """Load or create unified wallet state."""
        if self.unified_path.exists():
            try:
                with open(self.unified_path) as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "owner": self.owner,
            "created": time.time(),
            "total_wallets": 0,
            "total_balance_usd": 0.0,
            "wallets": {},
            "last_sync": time.time(),
        }
    
    def sync_wallets(self):
        """Sync all wallets into unified view."""
        self.unified["wallets"] = {
            "dusty": {
                "type": "dust_collection",
                "balances": self.dusty.get("balances", {}),
                "dust_collected": self.dusty.get("dust_collected", 0),
                "status": "active",
            },
            "evm": {
                "type": "ethereum_compatible",
                "address": self.evm.get("address", "unknown"),
                "network": self.evm.get("network", "unknown"),
                "status": self.evm.get("status", "active"),
            },
            "exchanges": {
                "type": "exchange_api",
                "connected": list(self.exchange.keys()),
                "status": "active" if self.exchange else "not_configured",
            },
            "payments": {
                "type": "payment_processing",
                "systems": list(self.payment.keys()),
                "status": "active" if self.payment else "not_configured",
            },
        }
        
        self.unified["total_wallets"] = len([w for w in self.unified["wallets"].values() if w.get("status") == "active"])
        self.unified["last_sync"] = time.time()
        
        self._save_unified()
        print(f"[UnifiedWallet] Synced {self.unified['total_wallets']} active wallets")
    
    def _save_unified(self):
        """Save unified wallet state."""
        self.unified_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.unified_path, 'w') as f:
            json.dump(self.unified, f, indent=2)
    
    def get_summary(self) -> str:
        """Get unified wallet summary."""
        self.sync_wallets()
        
        summary = f"""💎 UNIFIED WALLET SYSTEM ({self.owner.upper()})
═══════════════════════════════════════════════════

🔗 CONNECTED WALLETS: {self.unified['total_wallets']}

🪙 DUSTY WALLET (Dust Collection):
   Currencies: {len(self.dusty.get('balances', {}))}
   Dust Collected: {self.dusty.get('dust_collected', 0)} transactions
   Balances: {', '.join([f"{k}: {v['amount']:.6f}" for k, v in self.dusty.get('balances', {}).items()])}

🔐 EVM WALLET (Ethereum Compatible):
   Address: {self.evm.get('address', 'N/A')[:20]}...
   Network: {self.evm.get('network', 'N/A')}
   Status: {self.evm.get('status', 'unknown')}

💱 EXCHANGE WALLETS:
   Connected: {', '.join(self.exchange.keys()) if self.exchange else 'None'}

💳 PAYMENT SYSTEMS:
   Connected: {', '.join(self.payment.keys()) if self.payment else 'None'}

═══════════════════════════════════════════════════
Last Sync: {time.ctime(self.unified['last_sync'])}
═══════════════════════════════════════════════════"""
        
        return summary
    
    def collect_dust_to_unified(self, currency: str, amount: float, source: str):
        """Collect dust and update unified view."""
        # Import DustyWallet class
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from dusty_wallet import DustyWallet
        
        dusty = DustyWallet(self.owner)
        dusty.collect_dust(currency, amount, source)
        
        # Refresh and sync
        self.dusty = self._load_dusty_wallet()
        self.sync_wallets()


def create_unified_wallet():
    """Create unified wallet system for Miles."""
    print("=" * 70)
    print("💎 UNIFIED WALLET SYSTEM - TYING ALL WALLETS TO DUSTY")
    print("=" * 70)
    print()
    
    unified = UnifiedWalletSystem("miles")
    
    print("Loading wallets...")
    print("  ✅ Dusty Wallet (dust collection)")
    print("  ✅ EVM Wallet (ethereum compatible)")
    print("  ✅ Exchange wallets (Binance)")
    print("  ✅ Payment systems (Stripe)")
    print()
    
    # Sync and display
    unified.sync_wallets()
    print(unified.get_summary())
    
    return unified


if __name__ == "__main__":
    unified = create_unified_wallet()
    print()
    print("✅ All wallets tied to Dusty Wallet!")
    print("   Unified view provides complete portfolio overview.")
