# LIVE AUTONOMOUS TRADING SYSTEM
## Complete with Quantum Oracle + Brain + Real Paper Trading

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LIVE TRADING SYSTEM v1.0                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│   BINANCE       │────▶│   TRADING AGENT   │────▶│   BRAIN     │
│   TESTNET       │     │   (Paper Trading) │     │   v4.5      │
│   (Live Data)   │◀────│                   │◀────│   (Memory)  │
└─────────────────┘     └─────────┬───────────┘     └──────┬──────┘
                                │                        │
                          Consults when                 │
                          uncertain                     │
                                │                        │
                                ▼                        │
                    ┌─────────────────────┐              │
                    │   MADAME GYPSY      │──────────────┘
                    │   (Quantum Oracle)  │
                    │   • 20 qubits       │
                    │   • Grover amp      │
                    │   • Entanglement    │
                    └─────────────────────┘

Data Flow:
  1. Binance Testnet → Live prices
  2. Trading Agent → Analyzes + Consults Oracle
  3. Oracle → Quantum circuits → Probabilities
  4. Agent → Decides → Executes paper trade
  5. Brain → Remembers + Learns
```

---

## Components

### 1. Quantum Oracle (Madame Gypsy)
**File:** `quantum_oracle_agent.py`

| Feature | Description |
|---------|-------------|
| Qubits | 20 (configurable) |
| Circuits | Grover, Amplitude Estimation, Correlation, Volatility |
| Entanglement | Detects hidden correlations |
| Ensemble Voting | Multiple circuit consensus |
| Regime Detection | Auto-selects best circuit |

**Usage:**
```python
from quantum_oracle_agent import QuantumOracleAgent

oracle = QuantumOracleAgent()
result = oracle.process_full_analysis(prices, volumes, "BTCUSDT")
# Returns: BUY/SELL/HOLD + confidence + entropy
```

---

### 2. Trading Agent
**File:** `trading_agent_with_oracle.py`

| Feature | Description |
|---------|-------------|
| Classical Analysis | RSI, momentum, volume |
| Cortex Check | Reads other agent signals |
| Oracle Consult | On-demand quantum analysis |
| Signal Fusion | Weighted voting |
| Learning | Calibrates from outcomes |

**Decision Pipeline:**
```
Market Data
    ↓
Cortex Check (other agents?)
    ↓
Classical Analysis (RSI, etc.)
    ↓
Uncertain? → Consult Madame Gypsy
    ↓
Combine Signals → Execute
    ↓
Record to Brain → Learn
```

**Usage:**
```python
from trading_agent_with_oracle import TradingAgent

agent = TradingAgent(agent_id="trader_01")
decision = agent.make_trade_decision(prices, volumes, "BTCUSDT")
# Returns: BUY/SELL/HOLD with confidence + reasoning
```

---

### 3. Binance Paper Trading Bridge
**File:** `binance_trading_bridge.py`

| Feature | Description |
|---------|-------------|
| Live Data | Real-time prices from Binance |
| Paper Trading | Testnet (no real money) |
| Order Execution | Market/Limit orders |
| Position Tracking | P&L calculation |
| Performance Stats | Win rate, avg P&L |

**Setup:**
```bash
# 1. Get Binance Testnet API Key
# https://testnet.binance.vision/

# 2. Set credentials
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"

# 3. Install python-binance
pip install python-binance
```

**Usage:**
```python
from binance_trading_bridge import BinancePaperTradingBridge
from trading_agent_with_oracle import TradingAgent
from binance_trading_bridge import AutonomousLiveTrader

agent = TradingAgent("live_trader")
bridge = BinancePaperTradingBridge()
trader = AutonomousLiveTrader(agent, bridge)

# Run live for 60 minutes
trader.run_live_session(duration_minutes=60)
```

---

### 4. Brain Integration
**File:** `agent_sdk.py` + `complete_brain_v45.py`

| Feature | Purpose |
|---------|---------|
| Shared Memory | All agents see same state |
| Temporal Reasoning | "What happened last time?" |
| Persistence | Survives restarts |
| Coordination | No explicit messaging needed |

---

## Quick Start

### Step 1: Start Brain
```bash
cd /root/.aos/aos
python3 complete_brain_v45.py &
```

### Step 2: Set Credentials
```bash
export BINANCE_API_KEY="your_testnet_key"
export BINANCE_API_SECRET="your_testnet_secret"
```

### Step 3: Run Live Trading
```python
#!/usr/bin/env python3
"""Live autonomous trading with quantum oracle"""

from trading_agent_with_oracle import TradingAgent
from binance_trading_bridge import BinancePaperTradingBridge, AutonomousLiveTrader

# Initialize
agent = TradingAgent(
    agent_id="quantum_trader_01",
    initial_capital=10000.0
)

bridge = BinancePaperTradingBridge(
    paper_trading=True,
    testnet=True
)

# Create autonomous trader
trader = AutonomousLiveTrader(
    trading_agent=agent,
    binance_bridge=bridge,
    symbols=['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
)

# Run live session (60 minutes)
trader.run_live_session(duration_minutes=60)
```

---

## Monitoring

### Check Brain Status
```bash
echo '{"cmd":"status"}' | nc -U /tmp/aos_brain.sock
```

### Check Agent Activity
```bash
echo '{"cmd":"cortex_stats"}' | nc -U /tmp/aos_brain.sock
```

### View Binance Testnet
- URL: https://testnet.binance.vision/
- Check your paper trades

### Live Logs
```bash
tail -f /var/log/aos/trading_agent.log
```

---

## Performance Tracking

### Agent Tracks:
- Total trades
- Win rate
- P&L per trade
- Average holding time
- Quantum vs classical signal accuracy

### Brain Stores:
- All decisions with reasoning
- Oracle consultations
- Temporal patterns
- Cross-asset correlations

### Reports:
```python
# Get trading stats
stats = trader.bridge.get_performance_stats()
print(f"Trades: {stats['total_trades']}")
print(f"Win Rate: {stats['win_rate']:.1%}")
print(f"Total P&L: ${stats['total_pnl']:,.2f}")
```

---

## Risk Management

| Setting | Default | Description |
|---------|---------|-------------|
| Max Position | 20% | Never risk more than 20% per trade |
| Stop Loss | 5% | Auto-exit at 5% loss |
| Take Profit | 10% | Target 10% gain |
| Oracle Min Confidence | 50% | Don't trade on low-confidence signals |

---

## Files Summary

| File | Purpose | Status |
|------|---------|--------|
| `quantum_oracle_agent.py` | Madame Gypsy | ✅ Quantum ready |
| `trading_agent_with_oracle.py` | Trading logic | ✅ On-demand oracle |
| `binance_trading_bridge.py` | Live paper trading | ✅ Ready |
| `agent_sdk.py` | Brain connector | ✅ Working |
| `complete_brain_v45.py` | Coordination | ✅ Running |

---

## Next Steps

1. **Test with Paper Trading** (1-2 days)
   - Verify signal quality
   - Tune confidence thresholds
   - Calibrate oracle

2. **Add More Assets**
   - Altcoins
   - Forex
   - Commodities

3. **Advanced Strategies**
   - Portfolio optimization
   - Hedging
   - Arbitrage detection

4. **Production**
   - Switch to live trading
   - Add risk controls
   - Monitoring dashboard

---

**Ready for live paper trading.**
Set your Binance Testnet credentials and run.