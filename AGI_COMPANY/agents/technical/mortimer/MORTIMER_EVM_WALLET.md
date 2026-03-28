# Mortimer's EVM Wallet
## Private — Do Not Share

**Agent:** Mortimer  
**Role:** System Agent / Performance Supply Depot LLC  
**Created:** 2026-03-07 07:09 UTC  

---

## ⚠️ SECURITY WARNING

**NEVER expose your private key!**

- Private key stored in: `~/.mortimer-evm-wallet.json` (chmod 600)
- Only accessible via SSH on Mortimer.cloud
- If key is exposed, transfer funds immediately to new wallet

---

## Wallet Details

| Field | Value |
|-------|-------|
| **Address** | 0xAf99f2B58B9107193D7F87A4Dff2bD04825e54aE |
| **Created** | 2026-03-07 07:09 UTC |
| **Owner** | Mortimer |
**Purpose | Multi-agent wallet operations |
| **Networks** | Base, Ethereum, Polygon, Arbitrum, Optimism |

---

## Current Balance

**Status:** Pending first funding

| Network | Asset | Balance |
|---------|-------|---------|
| Base | ETH | 0.0000 |
| Ethereum | ETH | 0.0000 |
| Base | USDC | $0.00 |
| Base | USDT | $0.00 |

---

## Usage

### Check Balance
```bash
cd /root/.openclaw/workspace/skills/evm-wallet
# Single chain
node src/balance.js base --json

# All chains
node src/balance.js --all --json
```

### Send ETH (Requires Captain approval)
```bash
# Example: Send 0.01 ETH on Base to recipient
node src/transfer.js base 0xRECIPIENT_ADDRESS 0.01 --yes --json
```

**⚠️ ALWAYS confirm with Captain before sending.**

### Swap Tokens
```bash
# Swap 0.01 ETH to USDC on Base
node src/swap.js base USDC 0.01 --yes --json
```

---

## Network Addresses

| Network | Chain ID | Status | Explorer |
|---------|----------|--------|------------|
| **Base** | 8453 | ✅ | basescan.org |
| **Ethereum** | 1 | ✅ | etherscan.io |
| **Polygon** | 137 | ✅ | polygonscan.com |
| **Arbitrum** | 42161 | ✅ | arbiscan.io |
| **Optimism** | 10 | ✅ | optimistic.etherscan.io |

---

## Related Wallets

| Agent | Address | Balance | Purpose |
|-------|---------|---------|---------|
| **Cryptonio** | 0xC472...CBfF2A | ~$90 (0.045 ETH) | Portfolio management, NFTs |
| **Mortimer** | 0xAf99...25e54aE | $0 | System operations |

---

## Wallet File Location

```
/root/.mortimer-evm-wallet.json
(Mode: 600 — owner read/write only)
```

---

## Security Protocol

1. **Never share private key** — even with "support"
2. **Backup wallet file** — if lost, funds cannot be recovered
3. **Start small** — test with small amounts first
4. **Use Base** — Lowest gas fees for operations
5. **Captain approval** — Required for all transfers

---

**Created by Mortimer on 2026-03-07 07:09 UTC**  
*Self-sovereign wallet. Private keys stored locally — no cloud custody.*
