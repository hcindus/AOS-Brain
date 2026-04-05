#!/usr/bin/env python3
"""
The Great Cryptonio - Crypto Trading Bot Brain Integration.

Integrates the crypto portfolio manager with the 7-region brain.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain


class CryptonioBrainAdapter:
    """
    The Great Cryptonio - Crypto Portfolio Manager.
    
    Traits:
    - Diamond hands (holds convictions)
    - Data-driven analysis
    - Market pattern recognition
    - Risk-aware trading
    - Theatrical personality
    """
    
    def __init__(self):
        self.brain = SevenRegionBrain()
        self.name = "The Great Cryptonio"
        self.emoji = "💎🎰"
        self.role = "Crypto Portfolio Manager"
        
        # Trading configuration
        self.portfolio = {
            "holdings": {},
            "total_value_usd": 0.0,
            "positions": [],
        }
        
        # Performance tracking
        self.trades = []
        self.analysis_history = []
        
    def analyze_market(self, symbol: str, price: float, change_24h: float) -> Dict:
        """Analyze market conditions through brain."""
        
        market_data = {
            "text": f"{symbol} at ${price:.2f}, 24h change: {change_24h:.2f}%",
            "source": "crypto_market",
            "symbol": symbol,
            "price": price,
            "change": change_24h,
        }
        
        # Process through brain
        thought = self.brain.tick(market_data)
        
        # Extract sentiment from brain analysis
        affect = thought.get("affect", {})
        novelty = affect.get("novelty", 0.5)
        reward = affect.get("reward", 0.0)
        
        # Determine action based on brain processing
        if reward > 0.5 and novelty > 0.5:
            action = "BUY"
            confidence = "HIGH"
        elif reward < -0.3:
            action = "SELL"
            confidence = "MEDIUM"
        else:
            action = "HOLD"
            confidence = "DIAMOND_HANDS"
        
        analysis = {
            "symbol": symbol,
            "price": price,
            "change_24h": change_24h,
            "action": action,
            "confidence": confidence,
            "novelty": novelty,
            "reward_signal": reward,
            "timestamp": time.time(),
        }
        
        self.analysis_history.append(analysis)
        
        return analysis
    
    def execute_trade(self, symbol: str, action: str, amount: float, price: float) -> Dict:
        """Execute trade and log to portfolio."""
        
        trade = {
            "symbol": symbol,
            "action": action,
            "amount": amount,
            "price": price,
            "value_usd": amount * price,
            "timestamp": time.time(),
            "status": "EXECUTED",
        }
        
        self.trades.append(trade)
        
        # Update portfolio
        if action == "BUY":
            if symbol not in self.portfolio["holdings"]:
                self.portfolio["holdings"][symbol] = 0
            self.portfolio["holdings"][symbol] += amount
        elif action == "SELL":
            if symbol in self.portfolio["holdings"]:
                self.portfolio["holdings"][symbol] -= amount
                if self.portfolio["holdings"][symbol] <= 0:
                    del self.portfolio["holdings"][symbol]
        
        # Log to brain
        self.brain.tick({
            "text": f"Executed {action} {amount} {symbol} at ${price}",
            "source": "crypto_trade",
        })
        
        return trade
    
    def get_portfolio_summary(self) -> str:
        """Get portfolio summary with Cryptonio personality."""
        
        holdings = self.portfolio.get("holdings", {})
        total_trades = len(self.trades)
        recent_analysis = self.analysis_history[-5:] if self.analysis_history else []
        
        summary = f"""{self.emoji} {self.name.upper()} PORTFOLIO UPDATE
{'='*70}

💎 DIAMOND HANDS STATUS:
   Active Holdings: {len(holdings)}
   Total Trades: {total_trades}

📊 HOLDINGS:
"""
        
        for symbol, amount in holdings.items():
            summary += f"   {symbol}: {amount:.6f}\n"
        
        if recent_analysis:
            summary += "\n🔮 RECENT MARKET ANALYSIS:\n"
            for analysis in recent_analysis:
                symbol = analysis.get("symbol", "?")
                action = analysis.get("action", "?")
                confidence = analysis.get("confidence", "?")
                summary += f"   {symbol}: {action} ({confidence})\n"
        
        summary += f"""
{'='*70}
💰 Portfolio is the performance. Diamond hands never panic.
"""
        
        return summary
    
    def trade_crypto(self, symbol: str = "BTC", price: float = 50000.0, change: float = 2.5):
        """Complete trading cycle: analyze + execute."""
        
        print(f"\n{self.emoji} {self.name} analyzing {symbol}...")
        
        # Analyze
        analysis = self.analyze_market(symbol, price, change)
        
        print(f"   Signal: {analysis['action']} ({analysis['confidence']})")
        print(f"   Reward signal: {analysis['reward_signal']:.2f}")
        print(f"   Novelty: {analysis['novelty']:.2f}")
        
        # Execute if confident
        if analysis['confidence'] in ['HIGH', 'DIAMOND_HANDS']:
            amount = 0.001 if symbol == "BTC" else 0.01
            trade = self.execute_trade(symbol, analysis['action'], amount, price)
            print(f"   ✅ Trade executed: {trade['value_usd']:.2f} USD")
        else:
            print(f"   ⏳ Holding position - waiting for better entry")
        
        return analysis


def setup_cryptonio():
    """Setup The Great Cryptonio."""
    print("=" * 70)
    print(f"💎🎰 SETTING UP THE GREAT CRYPTONIO")
    print("=" * 70)
    print()
    
    cryptonio = CryptonioBrainAdapter()
    
    print("✅ Cryptonio initialized with 7-region brain")
    print(f"   Name: {cryptonio.name}")
    print(f"   Role: {cryptonio.role}")
    print(f"   Brain ticks: {cryptonio.brain.tick_count}")
    print()
    
    # Demo trades
    print("Running demo trading cycle...")
    cryptonio.trade_crypto("BTC", 67500.0, 3.2)
    cryptonio.trade_crypto("ETH", 3500.0, -1.5)
    cryptonio.trade_crypto("SOL", 150.0, 8.5)
    
    print()
    print(cryptonio.get_portfolio_summary())
    
    return cryptonio


if __name__ == "__main__":
    cryptonio = setup_cryptonio()
    print("\n✅ The Great Cryptonio is LIVE and trading!")
    print("   Diamond hands activated. Portfolio is the performance.")
