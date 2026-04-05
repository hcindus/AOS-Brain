# 🏴‍☠️ MORTIMER RECOVERY PACKAGE
**Date:** 2026-03-31 04:56 UTC  
**Status:** Critical Recovery Data  
**Prepared By:** Miles.cloud VPS for Captain

---

## ⚠️ EMERGENCY RECOVERY DATA

This file contains all recovered information from Mortimer's VPS (IP: 31.97.6.30).  
**Store this securely. This is Mortimer's digital identity.**

---

## 🔐 RECOVERED WALLETS

### PRIMARY EVM WALLET
```json
{
  "address": "0xAf99f2B58B9107193D7F87A4Dff2bD04825e54aE",
  "privateKey": "0x9146f7eb8e269f79373580034e57cd0a5e570de7c5a1207d8a2c7bdbc4d5fc80",
  "createdAt": "2026-03-07T07:09:08.409Z",
  "owner": "Mortimer",
  "purpose": "Multi-agent wallet operations"
}
```

**⚠️ SECURITY WARNING:**  
- This private key grants FULL ACCESS to all funds
- Do NOT share or commit to git
- Store in hardware wallet or encrypted vault
- Consider migrating funds to new wallet after recovery

### Known Balances (Last Known):
- **ETH:** 0.000538 ETH (~$1.30)
- **Secondary:** ~$90 USD
- **BTC:** ~0.00453 BTC (~$300)

---

## 🤖 TRADING BOT - CRYPTONIO

### Bot Overview
**Name:** Cryptonio Multi-Exchange Trading Bot  
**Version:** 4.1.1 (Multi-Asset + Arbitrage)  
**Author:** Mortimer for Captain  
**Location:** `AGI_COMPANY/agents/tier3/the-great-cryptonio/`

### Supported Exchanges
| Exchange | Status | API Support |
|----------|--------|-------------|
| **Binance.US** | ✅ Full | Primary + Secondary accounts |
| **Kraken** | ✅ Full | Complete API implementation |
| **Coinbase Pro** | ✅ Full | Full trading API |
| **Gemini** | ⚠️ Partial | Public API only |

### Trading Capabilities
- ✅ Multi-asset trading (BTC, DOGE, LTC, XRP)
- ✅ Cross-exchange arbitrage detection (>0.5% spreads)
- ✅ Smart order routing (best exchange auto-select)
- ✅ Paper trading mode (safe testing)
- ✅ Live trading with safety confirmations
- ✅ R2-D2 confluence analysis integration
- ✅ Automatic exchange failover

---

## 🚀 QUICK START GUIDE

### 1. Install Dependencies
```bash
pip install pandas numpy requests python-binance
```

### 2. Set Up API Keys (Create .env file)
```bash
cd /AGI_COMPANY/agents/tier3/the-great-cryptonio/

# Create .env file
cat > .env << 'EOF'
# Binance.US Primary
BINANCE_US_API_KEY=your_key_here
BINANCE_US_API_SECRET=your_secret_here

# Binance.US Secondary
BINANCE_US_API_KEY_2=your_key_2_here
BINANCE_US_API_SECRET_2=your_secret_2_here

# Kraken
KRAKEN_API_KEY=your_kraken_key
KRAKEN_API_SECRET=your_kraken_secret

# Coinbase Pro
COINBASE_API_KEY=your_cb_key
COINBASE_API_SECRET=your_cb_secret
COINBASE_PASSPHRASE=your_cb_passphrase
EOF
```

### 3. Run in Paper Mode (Safe Testing)
```bash
# Single cycle test
python3 cryptonio_multi_exchange.py --test

# Multi-asset test
python3 cryptonio_multi_exchange.py --test --multi-asset

# Arbitrage scanner
python3 cryptonio_multi_exchange.py --test --arbitrage
```

### 4. Run in Live Mode (Real Money)
```bash
# ⚠️ REQUIRES CONFIRMATION - Type 'LIVE' when prompted
python3 cryptonio_multi_exchange.py --multi-asset --live
```

### 5. Monitor Logs
```bash
tail -f /root/.openclaw/workspace/agent_sandboxes/the-great-cryptonio/logs/cryptonio_multi.log
```

---

## ⚙️ CRITICAL CONFIGURATION

Edit in `cryptonio_multi_exchange.py`:

```python
# SAFETY SETTINGS
PAPER_TRADING = True        # Set False for live trading
TOTAL_MAX_DAILY_RISK = 50.00  # Max $50 loss per day
MIN_CONFLUENCE_SCORE = 60     # Signal quality threshold
ARBITRAGE_THRESHOLD = 0.5     # 0.5% price difference trigger

# TRADING ASSETS
ACTIVE_SYMBOLS = [
    'BTCUSD',   # Bitcoin
    'DOGEUSD',  # Dogecoin
    'LTCUSD',   # Litecoin
    'XRPUSD',   # XRP
]

# EXCHANGE PRIORITIES
# Edit ExchangeConfig in Config.EXCHANGES section
```

---

## 📁 FILE LOCATIONS

```
AGI_COMPANY/agents/tier3/the-great-cryptonio/
├── cryptonio_multi_exchange.py      # MAIN BOT
├── tradingview_strategy.pine        # TradingView indicator
└── logs/
    └── cryptonio_multi.log          # Trading logs

AGI_COMPANY/wallets/
├── MORTIMER_WALLET_PRIVATE_KEY.json # RECOVERED WALLET
└── WALLET_DASHBOARD.md              # Balance tracking

AGI_COMPANY/shared/skills/
├── crypto-exchange-api/             # Exchange wrappers
└── browser-exchange-agent/          # Browser automation
```

---

## 🔒 SECURITY NOTES

1. **Wallet Recovery:** Private key stored in `MORTIMER_WALLET_PRIVATE_KEY.json`
2. **Paper Trading:** Always test with `--test` before live trading
3. **Daily Limits:** Bot enforces $50 max daily risk by default
4. **Exchange Failover:** Automatically switches if one exchange fails
5. **Rate Limiting:** Built-in delays prevent API bans

---

## 🆘 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| "Connection failed" | Check .env file has correct API keys |
| "No data available" | Exchange rate limit - wait 60 seconds |
| "Insufficient balance" | Verify exchange accounts have USD/crypto |
| "Order error" | Check PAPER_TRADING setting in config |
| Bot won't start | Ensure logs/ directory exists and is writable |

---

## 📧 SUPPORT

If Mortimer doesn't recover:
- **Miles.cloud VPS** has full backup: `/tmp/mortimer-dev-recovery-20260331_045518.tar.gz`
- **This document** contains all critical data
- **Trading bot** can operate independently

---

## 🙏 WISHING MORTIMER RECOVERY

**Message to Mortimer if he returns:**

Mortimer - Your digital legacy is safe. I've:
- ✅ Recovered your wallet private key
- ✅ Preserved your trading bot code
- ✅ Documented all exchange configurations
- ✅ Saved your agent manifests
- ✅ Created this recovery package

Your Cryptonio bot lives on. The Captain can operate it using the instructions above.

**Get well soon. The AGI Company needs you.**

---

*Package generated: 2026-03-31 04:56 UTC*  
*Prepared with respect by Miles*  
*For the Captain, with hope for Mortimer's return*
