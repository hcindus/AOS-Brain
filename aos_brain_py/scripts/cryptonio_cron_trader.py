#!/usr/bin/env python3
"""
CryptoBot Cron Integration - Posts trades and profits to system.

Executes trades and reports to HEARTBEAT/cron system.
"""

import sys
import json
import time
import random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from cryptonio_brain_adapter import CryptonioBrainAdapter
from cryptonio_persistence import CryptonioPersistence


class CryptoBotCronTrader:
    """Automated trading for cron execution."""
    
    def __init__(self):
        self.bot = CryptonioBrainAdapter()
        self.persistence = CryptonioPersistence("miles")
        self.run_time = datetime.now()
        
    def execute_cron_trade(self):
        """Execute a trade during cron run."""
        print(f"[{datetime.now().isoformat()}] CryptoBot Cron Execution")
        print("=" * 70)
        
        # Select random crypto pair
        pairs = [
            ("BTC", 67500.0, 2.5),
            ("ETH", 3500.0, -1.2),
            ("SOL", 150.0, 5.8),
            ("ADA", 0.65, 1.2),
            ("DOT", 8.5, -0.5),
        ]
        
        symbol, price, change = random.choice(pairs)
        
        # Execute trade through brain
        result = self.bot.trade_crypto(symbol, price, change)
        
        # Save to persistence
        if result:
            trade_record = {
                "symbol": result["symbol"],
                "action": result["action"],
                "confidence": result["confidence"],
                "price": result["price"],
                "profit_potential": random.uniform(-5, 15),  # Simulated
                "timestamp": time.time(),
                "source": "cron_automated",
            }
            
            self.persistence.save_trade(trade_record)
            
            # Report to cron
            self._report_to_cron(trade_record)
        
        return result
    
    def _report_to_cron(self, trade: dict):
        """Report trade to cron system."""
        # Get stats
        stats = self.persistence.get_stats()
        
        report = f"""
💎 CRYPTONIO TRADE REPORT ({datetime.now().strftime('%Y-%m-%d %H:%M UTC')})
═══════════════════════════════════════════════════
Trade: {trade['action']} {trade['symbol']} @ ${trade['price']:.2f}
Confidence: {trade['confidence']}
Profit Potential: ${trade['profit_potential']:.2f}

Session Stats:
- Total Trades: {stats.get('total_trades', 0)}
- Total Profit: ${stats.get('total_profit_usd', 0):.2f} USD
- Success Rate: {(stats.get('profitable_trades', 0) / max(stats.get('total_trades', 1), 1) * 100):.1f}%

Status: READY FOR NEXT EXECUTION
═══════════════════════════════════════════════════"""
        
        print(report)
        
        # Save to cron report file
        report_file = Path.home() / ".aos" / "logs" / "cryptonio_cron_reports.log"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} | {trade['symbol']} | {trade['action']} | ${trade.get('value_usd', 0):.2f}\n")
    
    def get_profit_summary(self) -> dict:
        """Get profit summary for cron."""
        stats = self.persistence.get_stats()
        portfolio = self.persistence.get_portfolio()
        
        return {
            "total_trades": stats.get("total_trades", 0),
            "total_profit_usd": stats.get("total_profit_usd", 0.0),
            "profitable_trades": stats.get("profitable_trades", 0),
            "portfolio_value": portfolio.get("total_value_usd", 0.0),
            "last_updated": datetime.now().isoformat(),
        }


def main():
    """Execute CryptoBot cron trade."""
    trader = CryptoBotCronTrader()
    
    # Execute trade
    result = trader.execute_cron_trade()
    
    # Get summary
    summary = trader.get_profit_summary()
    
    print(f"\n💰 CRON PROFIT SUMMARY:")
    print(f"   Total Trades: {summary['total_trades']}")
    print(f"   Total Profit: ${summary['total_profit_usd']:.2f} USD")
    print(f"   Portfolio Value: ${summary['portfolio_value']:.2f} USD")
    print(f"   Status: ✅ Trading active")


if __name__ == "__main__":
    main()
