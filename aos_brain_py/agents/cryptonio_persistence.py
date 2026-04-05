#!/usr/bin/env python3
"""
The Great Cryptonio - Persistent Storage System.

Stores trade history, portfolio state, and analysis in vault so it doesn't forget.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any


class CryptonioPersistence:
    """Persistent storage for CryptoBot data."""
    
    def __init__(self, owner: str = "miles"):
        self.owner = owner
        self.vault_path = Path.home() / ".aos" / "vault" / "cryptonio"
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        # Files
        self.trades_file = self.vault_path / "trade_history.json"
        self.portfolio_file = self.vault_path / "portfolio.json"
        self.analysis_file = self.vault_path / "analysis_history.json"
        self.stats_file = self.vault_path / "performance_stats.json"
        
        # Initialize if not exists
        self._init_files()
    
    def _init_files(self):
        """Initialize storage files if they don't exist."""
        for file_path, default_data in [
            (self.trades_file, {"trades": [], "count": 0}),
            (self.portfolio_file, {"holdings": {}, "total_value_usd": 0.0, "positions": []}),
            (self.analysis_file, {"analyses": [], "count": 0}),
            (self.stats_file, {"total_trades": 0, "profitable_trades": 0, "total_profit_usd": 0.0}),
        ]:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
    
    def save_trade(self, trade: Dict):
        """Save trade to persistent storage."""
        data = self._load_json(self.trades_file)
        trade["timestamp"] = time.time()
        trade["id"] = f"trade_{int(time.time() * 1000)}"
        data["trades"].append(trade)
        data["count"] = len(data["trades"])
        self._save_json(self.trades_file, data)
        
        # Update stats
        self._update_stats(trade)
    
    def save_portfolio(self, portfolio: Dict):
        """Save portfolio state."""
        portfolio["last_updated"] = time.time()
        self._save_json(self.portfolio_file, portfolio)
    
    def save_analysis(self, analysis: Dict):
        """Save market analysis."""
        data = self._load_json(self.analysis_file)
        analysis["timestamp"] = time.time()
        analysis["id"] = f"analysis_{int(time.time() * 1000)}"
        data["analyses"].append(analysis)
        data["count"] = len(data["analyses"])
        # Keep last 1000 analyses
        if len(data["analyses"]) > 1000:
            data["analyses"] = data["analyses"][-1000:]
        self._save_json(self.analysis_file, data)
    
    def _update_stats(self, trade: Dict):
        """Update performance statistics."""
        stats = self._load_json(self.stats_file)
        stats["total_trades"] += 1
        
        # Check if profitable
        value = trade.get("value_usd", 0)
        if value > 0:
            stats["profitable_trades"] += 1
            stats["total_profit_usd"] += value
        
        stats["last_updated"] = time.time()
        self._save_json(self.stats_file, stats)
    
    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON from file."""
        try:
            with open(file_path) as f:
                return json.load(f)
        except:
            return {}
    
    def _save_json(self, file_path: Path, data: Dict):
        """Save JSON to file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_trade_history(self, limit: int = 100) -> List[Dict]:
        """Get trade history."""
        data = self._load_json(self.trades_file)
        trades = data.get("trades", [])
        return trades[-limit:] if trades else []
    
    def get_portfolio(self) -> Dict:
        """Get current portfolio."""
        return self._load_json(self.portfolio_file)
    
    def get_analysis_history(self, limit: int = 100) -> List[Dict]:
        """Get analysis history."""
        data = self._load_json(self.analysis_file)
        analyses = data.get("analyses", [])
        return analyses[-limit:] if analyses else []
    
    def get_stats(self) -> Dict:
        """Get performance statistics."""
        return self._load_json(self.stats_file)
    
    def get_summary(self) -> str:
        """Get storage summary."""
        trades = self._load_json(self.trades_file)
        portfolio = self._load_json(self.portfolio_file)
        analysis = self._load_json(self.analysis_file)
        stats = self._load_json(self.stats_file)
        
        return f"""💾 CRYPTONIO PERSISTENT STORAGE
═══════════════════════════════════════
Trades: {trades.get('count', 0)} stored
Analyses: {analysis.get('count', 0)} stored
Portfolio Holdings: {len(portfolio.get('holdings', {}))} assets
Total Profit: ${stats.get('total_profit_usd', 0):.2f} USD
Profitable Trades: {stats.get('profitable_trades', 0)} / {stats.get('total_trades', 0)}
═══════════════════════════════════════"""


def initialize_cryptonio_storage():
    """Initialize CryptoBot persistent storage."""
    print("=" * 70)
    print("💾 INITIALIZING CRYPTONIO PERSISTENT STORAGE")
    print("=" * 70)
    print()
    
    storage = CryptonioPersistence("miles")
    
    # Load existing data from original cryptonio if available
    aocros_cryptonio = Path("/root/.openclaw/workspace/aocros/agent_sandboxes/the-great-cryptonio")
    
    if aocros_cryptonio.exists():
        print("Found existing cryptonio data in aocros...")
        
        # Try to load existing trades/logs
        logs_dir = aocros_cryptonio / "logs"
        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.log"))
            print(f"  Found {len(log_files)} log files")
            # Could parse logs to restore history
    
    print()
    print(storage.get_summary())
    
    return storage


if __name__ == "__main__":
    storage = initialize_cryptonio_storage()
    print("\n✅ CryptoBot persistence initialized!")
    print("   Trade history, portfolio, and analysis will be remembered.")
