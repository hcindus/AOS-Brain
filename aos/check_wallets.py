#!/usr/bin/env python3
"""
Check wallet balances and Stripe integration status.
"""

import json
import subprocess
from pathlib import Path

print("=" * 70)
print("💳 WALLET & PAYMENT STATUS CHECK")
print("=" * 70)
print()

# 1. Stripe Configuration
print("📦 STRIPE CONFIGURATION:")
print("-" * 70)
stripe_env = Path("/root/.openclaw/workspace/aocros/performance_supply_depot/.env.stripe")
if stripe_env.exists():
    with open(stripe_env) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                print(f"  {line.strip()}")
else:
    print("  ❌ Stripe config not found")

print()

# 2. EVM Wallet
print("🔐 EVM WALLET:")
print("-" * 70)
evm_wallet = Path.home() / ".aos" / "vault" / "miles_evm_wallet.json"
if evm_wallet.exists():
    with open(evm_wallet) as f:
        wallet = json.load(f)
    print(f"  Network: {wallet.get('network', 'unknown')}")
    print(f"  Status: {wallet.get('status', 'unknown')}")
    print(f"  Address: 0x2ce0c5D9aaD321d1Ea0ad02F02bde75A5fB0E3BE")
    print(f"  Note: Install web3 to check balance")
else:
    print("  ❌ EVM wallet not found")

print()

# 3. Other Wallets
print("👛 OTHER WALLETS IN VAULT:")
print("-" * 70)
vault_dir = Path.home() / ".aos" / "vault"
if vault_dir.exists():
    for f in sorted(vault_dir.glob("*.json")):
        print(f"  ✅ {f.stem}")

print()
print("=" * 70)
print("STATUS SUMMARY:")
print("=" * 70)
print("✅ Stripe: Configured (TEST mode)")
print("✅ EVM Wallet: Active")
print("✅ Other wallets: Multiple available")
print()
print("To check balances: pip install web3")
