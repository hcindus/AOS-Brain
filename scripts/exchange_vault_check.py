#!/usr/bin/env python3
"""
Heartbeat Exchange Balance Checker.

Shows current exchange vault status for HEARTBEAT.md
"""

from pathlib import Path

def check_exchange_vault():
    """Check exchange vault and return status."""
    vault_path = Path.home() / ".aos" / "vault"
    
    exchanges = {
        "Binance US": vault_path / "binance",
        "Gemini": vault_path / "gemini", 
        "Coinbase": vault_path / "coinbase",
        "Kraken": vault_path / "cryptonio" / "trade_history.json",
    }
    
    status = []
    total_accounts = 0
    
    for name, path in exchanges.items():
        if path.exists():
            if path.is_dir():
                accounts = len(list(path.glob("*.env")))
                status.append(f"{name}: {accounts} account(s)")
                total_accounts += accounts
            else:
                status.append(f"{name}: ✓ (has trade history)")
                total_accounts += 1
    
    return {
        "total_accounts": total_accounts,
        "details": " | ".join(status),
        "status": "READY" if total_accounts >= 4 else "INCOMPLETE"
    }

if __name__ == "__main__":
    result = check_exchange_vault()
    print(f"Exchange Vault: {result['total_accounts']} accounts [{result['details']}]")
    print(f"Status: {result['status']} for trading")
