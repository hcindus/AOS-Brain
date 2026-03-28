#!/usr/bin/env python3
"""
Rationed API Manager - Limit API calls for cost control
Tracks usage and enforces quotas
"""

import json
import time
from pathlib import Path
from typing import Optional, Dict

class RationedAPIManager:
    """
    Manages API call rationing.
    
    Features:
    - Daily/hourly quotas
    - Per-agent tracking
    - Automatic fallback to local brain
    - Cost estimation
    """
    
    def __init__(self, daily_limit: int = 100):
        self.daily_limit = daily_limit
        self.usage_file = Path.home() / ".aos" / "vault" / "api_usage.json"
        self.usage_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize usage
        self.usage = self._load_usage()
        
    def _load_usage(self) -> Dict:
        """Load usage tracking."""
        if self.usage_file.exists():
            with open(self.usage_file) as f:
                return json.load(f)
        return {
            "daily_calls": 0,
            "total_calls": 0,
            "last_reset": time.time(),
            "by_agent": {}
        }
    
    def _save_usage(self):
        """Save usage tracking."""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f, indent=2)
    
    def can_make_call(self, agent: str) -> bool:
        """Check if call is allowed under ration."""
        # Reset daily count if needed
        if time.time() - self.usage.get("last_reset", 0) > 86400:
            self.usage["daily_calls"] = 0
            self.usage["last_reset"] = time.time()
        
        if self.usage["daily_calls"] >= self.daily_limit:
            print(f"[RationedAPI] Daily limit reached ({self.daily_limit})")
            print(f"[RationedAPI] Using local brain fallback")
            return False
        
        return True
    
    def record_call(self, agent: str, tokens: int = 0):
        """Record API call."""
        self.usage["daily_calls"] += 1
        self.usage["total_calls"] += 1
        
        if agent not in self.usage["by_agent"]:
            self.usage["by_agent"][agent] = {"calls": 0, "tokens": 0}
        
        self.usage["by_agent"][agent]["calls"] += 1
        self.usage["by_agent"][agent]["tokens"] += tokens
        
        self._save_usage()
    
    def get_status(self) -> Dict:
        """Get ration status."""
        remaining = self.daily_limit - self.usage.get("daily_calls", 0)
        return {
            "daily_limit": self.daily_limit,
            "daily_calls": self.usage.get("daily_calls", 0),
            "remaining": remaining,
            "total_calls": self.usage.get("total_calls", 0),
            "by_agent": self.usage.get("by_agent", {})
        }
    
    def print_status(self):
        """Print current ration status."""
        status = self.get_status()
        print(f"[RationedAPI] Daily: {status['daily_calls']}/{status['daily_limit']} calls")
        print(f"[RationedAPI] Remaining: {status['remaining']} calls today")
        print(f"[RationedAPI] Total: {status['total_calls']} calls")
        
        if status['by_agent']:
            print(f"[RationedAPI] By agent:")
            for agent, data in status['by_agent'].items():
                print(f"  - {agent}: {data['calls']} calls")


# Global ration manager
_ration_manager = None

def get_ration_manager(daily_limit: int = 100) -> RationedAPIManager:
    """Get singleton ration manager."""
    global _ration_manager
    if _ration_manager is None:
        _ration_manager = RationedAPIManager(daily_limit)
    return _ration_manager


if __name__ == "__main__":
    rm = get_ration_manager(daily_limit=50)
    rm.print_status()
