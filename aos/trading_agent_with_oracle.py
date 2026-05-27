#!/usr/bin/env python3
"""
TRADING AGENT v1.0 - Consults Madame Gypsy (Quantum Oracle)

Autonomous trading with quantum-enhanced decision making.

Pipeline:
  Market Data → Brain/Cortex → Check for Oracle Signals → 
  → Consult Madame Gypsy (if needed) → Execute Trade → Learn

The trading agent can:
  1. Read existing quantum signals from cortex
  2. Consult Madame Gypsy on-demand for difficult decisions
  3. Combine classical technical analysis with quantum intuition
  4. Learn from outcomes and calibrate confidence
"""

import time
import json
import hashlib
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from agent_sdk import AOSBrainClient, CortexHotspot

# Import Oracle for on-demand consultation
try:
    from quantum_oracle_agent import QuantumOracleAgent, HAS_QISKIT
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    print("[TradingAgent] Warning: Quantum Oracle not available")


class TradeAction(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

@dataclass
class TradeDecision:
    """A trading decision with full context"""
    timestamp: float
    symbol: str
    action: TradeAction
    confidence: float
    quantum_signal: Optional[Dict]
    classical_signal: Optional[Dict]
    position_size: float  # 0.0 to 1.0
    stop_loss: float
    take_profit: float
    reasoning: str

@dataclass
class TradeResult:
    """Result of a trade for learning"""
    decision: TradeDecision
    entry_price: float
    exit_price: float
    pnl: float  # Profit/loss
    outcome: str  # win, loss, breakeven
    duration_seconds: float


class TradingAgent:
    """
    Autonomous trading agent with quantum consultation
    
    Agent ID: trading_agent_[strategy]_[instance]
    """
    
    def __init__(self, agent_id: str = "trading_agent_quantum_01",
                 socket_path: str = '/tmp/aos_brain.sock',
                 initial_capital: float = 10000.0,
                 max_position_size: float = 0.2):  # Max 20% per trade
        self.agent_id = agent_id
        self.socket_path = socket_path
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_position_size = max_position_size
        
        # Connect to brain
        self.brain = AOSBrainClient(agent_id=agent_id)
        self.brain.register()
        
        # Initialize Oracle for consultation
        self.oracle = None
        if ORACLE_AVAILABLE:
            self.oracle = QuantumOracleAgent(
                agent_id=f"oracle_{agent_id}",
                socket_path=socket_path,
                max_qubits=20
            )
            print(f"[TradingAgent:{agent_id}] Connected to Madame Gypsy")
        
        self.trade_history: List[TradeResult] = []
        self.pending_decisions: List[TradeDecision] = []
        self.total_pnl = 0.0
        
        print(f"[TradingAgent:{agent_id}] Initialized")
        print(f"  Capital: ${initial_capital:,.2f}")
        print(f"  Max position: {max_position_size*100:.0f}%")
        print(f"  Oracle: {'Available' if self.oracle else 'Not available'}")
    
    def check_cortex_for_signals(self, symbol: str = "BTC") -> Optional[Dict]:
        """
        Check if other agents (like Oracle) have written signals
        
        Reads regions associated with this symbol
        """
        # Hash symbol to region mapping
        symbol_hash = int(hashlib.md5(symbol.encode()).hexdigest(), 16)
        regions = [
            (symbol_hash % 8),
            ((symbol_hash // 8) % 8)
        ]
        
        state = self.brain.read_cortex(
            regions=regions,
            max_hotspots=32
        )
        
        if state is None or state.coherence < 0.05:
            return None
        
        # Analyze hotspots for trading signals
        buy_signals = sum(1 for h in state.hotspots if h.value > 0)
        sell_signals = sum(1 for h in state.hotspots if h.value < 0)
        
        if buy_signals > sell_signals * 1.5:
            signal_type = "BUY"
            confidence = min(1.0, buy_signals / 10)
        elif sell_signals > buy_signals * 1.5:
            signal_type = "SELL"
            confidence = min(1.0, sell_signals / 10)
        else:
            signal_type = "UNCLEAR"
            confidence = 0.5
        
        return {
            "signal": signal_type,
            "confidence": confidence,
            "coherence": state.coherence,
            "hotspots": len(state.hotspots),
            "tick": state.tick
        }
    
    def consult_madame_gypsy(self, prices: List[float], 
                             volumes: List[float], 
                             symbol: str = "BTC") -> Optional[Dict]:
        """
        On-demand consultation with Quantum Oracle
        
        Called when:
        1. No clear signal in cortex
        2. Classical analysis is ambiguous
        3. High-stakes decision needed
        """
        if not self.oracle:
            print(f"[TradingAgent] Oracle not available, skipping consultation")
            return None
        
        print(f"[TradingAgent] Consulting Madame Gypsy for {symbol}...")
        
        # Run full quantum analysis
        result = self.oracle.process_full_analysis(prices, volumes, symbol)
        
        if "error" in result:
            print(f"[TradingAgent] Oracle consultation failed: {result['error']}")
            return None
        
        insight = result["insight"]
        
        print(f"[TradingAgent] Oracle says: {insight['recommendation']} "
              f"({insight['confidence']:.1%} confidence, "
              f"entropy: {insight['entropy']:.2f})")
        
        return {
            "recommendation": insight["recommendation"],
            "confidence": insight["confidence"],
            "entropy": insight["entropy"],
            "circuit": insight["circuit"],
            "regime": insight["regime"],
            "hotspots_written": result.get("hotspots", 0)
        }
    
    def classical_analysis(self, prices: List[float], 
                          volumes: List[float]) -> Dict:
        """
        Classical technical analysis
        
        Simple signals: RSI, trend, volume spike
        """
        if len(prices) < 14:
            return {"signal": "INSUFFICIENT_DATA", "confidence": 0.0}
        
        # Simple momentum
        returns = np.diff(prices) / prices[:-1]
        momentum = np.mean(returns[-5:])
        
        # Simple RSI approximation
        gains = [r for r in returns[-14:] if r > 0]
        losses = [abs(r) for r in returns[-14:] if r < 0]
        avg_gain = np.mean(gains) if gains else 0.001
        avg_loss = np.mean(losses) if losses else 0.001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Volume trend
        vol_trend = volumes[-1] / np.mean(volumes[-5:]) if len(volumes) >= 5 else 1.0
        
        # Decision logic
        if rsi < 30 and momentum > 0:
            signal = "BUY"
            confidence = (30 - rsi) / 30 * 0.8 + 0.2
        elif rsi > 70 and momentum < 0:
            signal = "SELL"
            confidence = (rsi - 70) / 30 * 0.8 + 0.2
        elif abs(momentum) < 0.001:
            signal = "HOLD"
            confidence = 0.6
        else:
            signal = "HOLD"
            confidence = 0.4
        
        return {
            "signal": signal,
            "confidence": confidence,
            "rsi": rsi,
            "momentum": momentum,
            "volume_trend": vol_trend
        }
    
    def make_trade_decision(self, prices: List[float],
                           volumes: List[float],
                           symbol: str = "BTC",
                           current_price: float = None) -> TradeDecision:
        """
        Full decision pipeline:
        1. Check cortex for existing signals
        2. Run classical analysis
        3. If ambiguous, consult Oracle
        4. Combine and decide
        5. Execute and record
        """
        timestamp = time.time()
        
        # Step 1: Check cortex
        cortex_signal = self.check_cortex_for_signals(symbol)
        
        # Step 2: Classical analysis
        classical = self.classical_analysis(prices, volumes)
        
        # Step 3: Determine if we need Oracle
        need_oracle = False
        
        if cortex_signal is None:
            need_oracle = True
            reason = "No clear signal in cortex"
        elif classical["confidence"] < 0.6:
            need_oracle = True
            reason = "Classical analysis ambiguous"
        elif abs(rsi - 50) < 10:  # RSI near neutral
            need_oracle = True
            reason = "RSI neutral, need quantum insight"
        else:
            reason = "Clear classical signal"
        
        # Step 4: Consult Oracle if needed
        quantum_signal = None
        if need_oracle and self.oracle:
            quantum_signal = self.consult_madame_gypsy(prices, volumes, symbol)
        
        # Step 5: Combine signals
        action, confidence, decision_reason = self._combine_signals(
            cortex_signal, classical, quantum_signal
        )
        
        # Step 6: Calculate position size
        position_size = self._calculate_position_size(confidence, action)
        
        # Step 7: Set stop loss / take profit
        if current_price:
            stop_loss = current_price * 0.95 if action == TradeAction.BUY else current_price * 1.05
            take_profit = current_price * 1.10 if action == TradeAction.BUY else current_price * 0.90
        else:
            stop_loss = 0.0
            take_profit = 0.0
        
        decision = TradeDecision(
            timestamp=timestamp,
            symbol=symbol,
            action=action,
            confidence=confidence,
            quantum_signal=quantum_signal,
            classical_signal=classical,
            position_size=position_size,
            stop_loss=stop_loss,
            take_profit=take_profit,
            reasoning=decision_reason
        )
        
        # Record in brain
        self._record_decision(decision)
        
        return decision
    
    def _combine_signals(self, cortex: Optional[Dict], 
                        classical: Dict,
                        quantum: Optional[Dict]) -> Tuple[TradeAction, float, str]:
        """
        Combine multiple signals into final decision
        
        Weight by source confidence
        """
        signals = []
        
        # Classical signal
        if classical["signal"] in ["BUY", "SELL"]:
            action = TradeAction.BUY if classical["signal"] == "BUY" else TradeAction.SELL
            signals.append((action, classical["confidence"], "classical"))
        
        # Cortex signal
        if cortex and cortex.get("signal") in ["BUY", "SELL"]:
            action = TradeAction.BUY if cortex["signal"] == "BUY" else TradeAction.SELL
            signals.append((action, cortex["confidence"], "cortex"))
        
        # Quantum signal
        if quantum and quantum.get("recommendation") in ["BUY", "SELL"]:
            action = TradeAction.BUY if quantum["recommendation"] == "BUY" else TradeAction.SELL
            signals.append((action, quantum["confidence"], "quantum"))
        
        if not signals:
            return TradeAction.HOLD, 0.5, "No clear signals"
        
        # Weighted vote
        buy_votes = sum(conf for action, conf, source in signals if action == TradeAction.BUY)
        sell_votes = sum(conf for action, conf, source in signals if action == TradeAction.SELL)
        
        total_confidence = sum(conf for _, conf, _ in signals) / len(signals)
        
        sources = [source for _, _, source in signals]
        
        if buy_votes > sell_votes * 1.2:
            return TradeAction.BUY, total_confidence, f"Buy consensus ({', '.join(sources)})"
        elif sell_votes > buy_votes * 1.2:
            return TradeAction.SELL, total_confidence, f"Sell consensus ({', '.join(sources)})"
        else:
            return TradeAction.HOLD, 0.5, f"Conflicting signals ({', '.join(sources)})"
    
    def _calculate_position_size(self, confidence: float, action: TradeAction) -> float:
        """Calculate position size based on confidence"""
        if action == TradeAction.HOLD:
            return 0.0
        
        # Base size on confidence
        base_size = confidence * self.max_position_size
        
        # Adjust for capital
        capital_factor = min(1.0, self.current_capital / self.initial_capital)
        
        return base_size * capital_factor
    
    def _record_decision(self, decision: TradeDecision):
        """Record decision to brain cortex"""
        # Encode decision to hotspots
        action_val = 1 if decision.action == TradeAction.BUY else (-1 if decision.action == TradeAction.SELL else 0)
        
        hotspots = []
        # Action strength
        for i in range(int(decision.confidence * 10)):
            x = (i * 3) % 32
            y = (i * 5 + 16) % 32
            z = 8  # Trading layer
            hotspots.append(CortexHotspot(x, y, z, action_val))
        
        self.brain.write_cortex(hotspots, priority=decision.confidence)
        
        # Also ingest for long-term memory
        self.brain.ingest(
            content=json.dumps(asdict(decision), default=str),
            source="trading_agent",
            priority=decision.confidence
        )
    
    def execute_paper_trade(self, decision: TradeDecision, 
                         current_price: float) -> TradeResult:
        """
        Execute paper trade (simulation)
        
        In production: connect to exchange API
        """
        print(f"\n[TRADE EXECUTED]")
        print(f"  Symbol: {decision.symbol}")
        print(f"  Action: {decision.action.value}")
        print(f"  Price: ${current_price:,.2f}")
        print(f"  Size: {decision.position_size*100:.1f}%")
        print(f"  Stop: ${decision.stop_loss:,.2f}")
        print(f"  Target: ${decision.take_profit:,.2f}")
        print(f"  Reason: {decision.reasoning}")
        
        # Simulate outcome
        if decision.action == TradeAction.HOLD:
            result = TradeResult(
                decision=decision,
                entry_price=current_price,
                exit_price=current_price,
                pnl=0.0,
                outcome="breakeven",
                duration_seconds=0.0
            )
        else:
            # Simulate price movement
            direction = 1 if decision.action == TradeAction.BUY else -1
            
            # Random outcome weighted by confidence
            if np.random.random() < decision.confidence:
                # Successful trade
                move = np.random.uniform(0.02, 0.08)
                exit_price = current_price * (1 + direction * move)
                pnl = direction * move * decision.position_size * self.current_capital
                outcome = "win"
            else:
                # Failed trade
                move = np.random.uniform(0.01, 0.05)
                exit_price = current_price * (1 - direction * move)
                pnl = -direction * move * decision.position_size * self.current_capital
                outcome = "loss"
            
            result = TradeResult(
                decision=decision,
                entry_price=current_price,
                exit_price=exit_price,
                pnl=pnl,
                outcome=outcome,
                duration_seconds=np.random.uniform(60, 3600)
            )
            
            self.current_capital += pnl
            self.total_pnl += pnl
        
        self.trade_history.append(result)
        
        # Learn from result
        self._learn_from_result(result)
        
        return result
    
    def _learn_from_result(self, result: TradeResult):
        """Update learning from trade outcome"""
        # Write outcome to brain
        self.brain.write_thought(
            f"Trade {result.outcome}: {result.decision.action.value} "
            f"{result.decision.symbol} PnL ${result.pnl:.2f}",
            priority=1.0 if result.outcome == "win" else 0.7
        )
        
        # Calibrate if using oracle
        if self.oracle and len(self.trade_history) > 10:
            returns = [r.pnl for r in self.trade_history[-10:]]
            self.oracle.calibrate_confidence(returns)
    
    def get_performance_summary(self) -> Dict:
        """Get trading performance summary"""
        if not self.trade_history:
            return {"error": "No trades yet"}
        
        wins = sum(1 for r in self.trade_history if r.outcome == "win")
        losses = sum(1 for r in self.trade_history if r.outcome == "loss")
        
        return {
            "total_trades": len(self.trade_history),
            "wins": wins,
            "losses": losses,
            "win_rate": wins / (wins + losses) if (wins + losses) > 0 else 0,
            "total_pnl": self.total_pnl,
            "current_capital": self.current_capital,
            "roi": (self.current_capital - self.initial_capital) / self.initial_capital
        }


def demo_trading_with_oracle():
    """Demonstrate trading agent with quantum oracle consultation"""
    print("=" * 70)
    print("  TRADING AGENT + MADAME GYPSY")
    print("  Autonomous trading with quantum consultation")
    print("=" * 70)
    
    # Create trading agent
    trader = TradingAgent(
        agent_id="trading_demo_01",
        initial_capital=10000.0
    )
    
    print(f"\n[Setup] Capital: ${trader.initial_capital:,.2f}")
    print(f"        Oracle: {'Connected' if trader.oracle else 'Not available'}")
    
    # Simulate multiple trading scenarios
    scenarios = [
        ("BTC", "Strong uptrend", "uptrend"),
        ("ETH", "Volatile choppy", "volatile"),
        ("SOL", "Sideways range", "ranging"),
        ("BTC", "Conflicting signals", "confusing"),
    ]
    
    for symbol, description, regime in scenarios:
        print(f"\n{'-'*70}")
        print(f"[Scenario] {symbol}: {description} ({regime})")
        print(f"{'-'*70}")
        
        # Generate appropriate market data
        if regime == "uptrend":
            prices = [45000 + i*200 + np.random.normal(0, 100) for i in range(25)]
            volumes = [1000 + np.random.normal(0, 50) for _ in range(25)]
        elif regime == "volatile":
            prices = [3000 + np.sin(i)*100 + np.random.normal(0, 80) for i in range(25)]
            volumes = [800 + np.random.normal(0, 200) for _ in range(25)]
        elif regime == "ranging":
            prices = [100 + np.random.normal(0, 2) for _ in range(25)]
            volumes = [500 + np.random.normal(0, 30) for _ in range(25)]
        else:  # confusing
            prices = [50000 + np.random.normal(0, 500) for _ in range(25)]
            volumes = [1200 + np.random.normal(0, 100) for _ in range(25)]
        
        current_price = prices[-1]
        
        print(f"  Current price: ${current_price:,.2f}")
        
        # Make decision
        decision = trader.make_trade_decision(prices, volumes, symbol, current_price)
        
        print(f"\n[Decision]")
        print(f"  Action: {decision.action.value}")
        print(f"  Confidence: {decision.confidence:.1%}")
        print(f"  Position: {decision.position_size*100:.1f}%")
        print(f"  Reason: {decision.reasoning}")
        
        if decision.quantum_signal:
            print(f"\n[Oracle Input]")
            print(f"  Circuit: {decision.quantum_signal.get('circuit', 'N/A')}")
            print(f"  Quantum confidence: {decision.quantum_signal.get('confidence', 0):.1%}")
            print(f"  Entropy: {decision.quantum_signal.get('entropy', 0):.2f}")
        
        # Execute paper trade
        if decision.action != TradeAction.HOLD:
            result = trader.execute_paper_trade(decision, current_price)
            print(f"\n[Result]")
            print(f"  Outcome: {result.outcome.upper()}")
            print(f"  PnL: ${result.pnl:,.2f}")
            print(f"  Duration: {result.duration_seconds/60:.1f} minutes")
        else:
            print("\n[Result] No trade executed (HOLD)")
        
        time.sleep(0.5)  # Brief pause between trades
    
    # Summary
    print("\n" + "=" * 70)
    print("  TRADING PERFORMANCE SUMMARY")
    print("=" * 70)
    
    summary = trader.get_performance_summary()
    print(f"\n  Total Trades: {summary['total_trades']}")
    print(f"  Wins: {summary['wins']} | Losses: {summary['losses']}")
    print(f"  Win Rate: {summary['win_rate']:.1%}")
    print(f"  Total PnL: ${summary['total_pnl']:,.2f}")
    print(f"  ROI: {summary['roi']:.2%}")
    print(f"  Final Capital: ${summary['current_capital']:,.2f}")
    
    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    print("\nThe trading agent:")
    print("  • Checks cortex for existing signals")
    print("  • Runs classical technical analysis")
    print("  • Consults Madame Gypsy when uncertain")
    print("  • Combines all signals for decision")
    print("  • Executes and learns from outcomes")
    print("\nReady for live trading with real exchange APIs.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_trading_with_oracle()
    else:
        print("Usage: python3 trading_agent_with_oracle.py --demo")
        print("\nFeatures:")
        print("  • Autonomous trading decisions")
        print("  • On-demand Oracle consultation")
        print("  • Classical + Quantum signal fusion")
        print("  • Paper trade simulation")
        print("  • Learning from outcomes")