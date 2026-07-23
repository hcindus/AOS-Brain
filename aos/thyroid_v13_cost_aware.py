#!/usr/bin/env python3
"""
AOS THYROID v1.3 - Cost-Aware Extension
Adds budget management to v1.2 endocrine regulator

NEW: Budget-aware mode switching
- Tracks API costs
- Auto-downgrades models when spend limits hit
- Emergency mode for budget exhaustion
"""

import time
import threading
from dataclasses import dataclass
from typing import Optional, Dict
from thyroid_v12 import AOSThyroidV12, ThyroidState, ThyroidHormone


@dataclass
class CostBudget:
    """Budget tracking for cost-aware thyroid"""
    daily_limit: float = 10.0      # $10/day default
    hourly_limit: float = 1.0      # $1/hour default
    spent_today: float = 0.0
    spent_this_hour: float = 0.0
    last_reset_day: float = 0.0
    last_reset_hour: float = 0.0
    
    # Cost tracking
    session_cost: float = 0.0      # Current session
    model_costs: Dict[str, float] = None
    
    def __post_init__(self):
        if self.model_costs is None:
            self.model_costs = {
                'tinyllama': 0.0001,    # $0.0001 per request
                'mort_ii': 0.01,        # $0.01 per request
                'nomic_embed': 0.0005,   # $0.0005 per request
            }
        self.last_reset_day = time.time()
        self.last_reset_hour = time.time()


class AOSThyroidV13(AOSThyroidV12):
    """
    Thyroid v1.3 - Cost-Aware Endocrine Regulator
    
    Extends v1.2 with budget management:
    - NORMAL: Standard endocrine regulation
    - CONSERVATIVE: Reduced OLLAMA usage when approaching limits
    - EMERGENCY: LOCAL only when budget exhausted
    """
    
    def __init__(self,
                 qmd_loop=None,
                 baseline_timeout: float = 120.0,
                 secretion_duration: float = 30.0,
                 daily_budget: float = 10.0,
                 hourly_budget: float = 1.0):
        
        super().__init__(qmd_loop, baseline_timeout, secretion_duration)
        
        # Budget management
        self.budget = CostBudget(
            daily_limit=daily_budget,
            hourly_limit=hourly_budget
        )
        
        # Mode thresholds (percentage of budget)
        self.conservative_threshold = 0.7   # 70% of budget = CONSERVATIVE
        self.emergency_threshold = 0.9       # 90% of budget = EMERGENCY
        
        # Current mode
        self.budget_mode = "NORMAL"
        
        print(f"\n[Thyroid v1.3] 💰 Cost-Aware extension active")
        print(f"    Daily budget: ${daily_budget:.2f}")
        print(f"    Hourly budget: ${hourly_budget:.2f}")
        print(f"    Conservative @ {self.conservative_threshold:.0%}")
        print(f"    Emergency @ {self.emergency_threshold:.0%}")
    
    def start(self):
        """Start thyroid and budget monitors"""
        super().start()
        self.budget_thread = threading.Thread(target=self._monitor_budget, daemon=True)
        self.budget_thread.start()
        print(f"[Thyroid v1.3] 💰 Budget monitoring active")
    
    def _monitor_budget(self):
        """Monitor budget and adjust mode"""
        while self.running:
            try:
                self._check_budget()
                self._apply_budget_mode()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"[Thyroid v1.3] Budget monitor error: {e}")
    
    def _check_budget(self):
        """Check current budget status and reset if needed"""
        now = time.time()
        
        # Reset daily budget
        if now - self.budget.last_reset_day >= 86400:  # 24 hours
            self.budget.spent_today = 0.0
            self.budget.last_reset_day = now
            self.budget.session_cost = 0.0
            print("[Thyroid v1.3] 💰 Daily budget reset")
        
        # Reset hourly budget
        if now - self.budget.last_reset_hour >= 3600:  # 1 hour
            self.budget.spent_this_hour = 0.0
            self.budget.last_reset_hour = now
    
    def _apply_budget_mode(self):
        """Apply budget constraints to thyroid mode"""
        daily_pct = self.budget.spent_today / self.budget.daily_limit
        hourly_pct = self.budget.spent_this_hour / self.budget.hourly_limit
        max_pct = max(daily_pct, hourly_pct)
        
        old_mode = self.budget_mode
        
        if max_pct >= self.emergency_threshold:
            self.budget_mode = "EMERGENCY"
            self.state = ThyroidState.BASELINE
        elif max_pct >= self.conservative_threshold:
            self.budget_mode = "CONSERVATIVE"
        else:
            self.budget_mode = "NORMAL"
        
        if old_mode != self.budget_mode:
            print(f"\n[Thyroid v1.3] 💰 Budget mode changed: {old_mode} → {self.budget_mode}")
            print(f"    Daily spend: ${self.budget.spent_today:.2f} / ${self.budget.daily_limit:.2f}")
            print(f"    Hourly spend: ${self.budget.spent_this_hour:.2f} / ${self.budget.hourly_limit:.2f}")
    
    def stimulate(self, importance: float = 0.5) -> bool:
        """
        Stimulate thyroid with budget awareness
        
        EMERGENCY: Always returns False (LOCAL only)
        CONSERVATIVE: Requires higher importance threshold
        NORMAL: Standard v1.2 behavior
        """
        if self.budget_mode == "EMERGENCY":
            print(f"\n[Thyroid v1.3] 🚨 EMERGENCY MODE - OLLAMA disabled (budget exhausted)")
            return False
        
        if self.budget_mode == "CONSERVATIVE":
            # Require higher importance in conservative mode
            adjusted_threshold = 0.85  # vs 0.7 in normal mode
            if importance < adjusted_threshold:
                print(f"\n[Thyroid v1.3] 💰 CONSERVATIVE MODE - Skipped (importance: {importance:.2f} < {adjusted_threshold:.2f})")
                return False
        
        # Normal stimulation (or conservative with high importance)
        return super().stimulate(importance)
    
    def record_cost(self, model: str, requests: int = 1):
        """Record API usage cost"""
        cost_per = self.budget.model_costs.get(model, 0.001)
        cost = cost_per * requests
        
        self.budget.spent_today += cost
        self.budget.spent_this_hour += cost
        self.budget.session_cost += cost
    
    def get_budget_status(self) -> dict:
        """Get current budget status"""
        daily_pct = self.budget.spent_today / self.budget.daily_limit
        hourly_pct = self.budget.spent_this_hour / self.budget.hourly_limit
        
        return {
            "budget_mode": self.budget_mode,
            "daily_spend": round(self.budget.spent_today, 4),
            "daily_limit": self.budget.daily_limit,
            "daily_remaining": round(self.budget.daily_limit - self.budget.spent_today, 4),
            "daily_pct": round(daily_pct * 100, 1),
            "hourly_spend": round(self.budget.spent_this_hour, 4),
            "hourly_limit": self.budget.hourly_limit,
            "hourly_remaining": round(self.budget.hourly_limit - self.budget.spent_this_hour, 4),
            "hourly_pct": round(hourly_pct * 100, 1),
            "session_cost": round(self.budget.session_cost, 4)
        }
    
    def get_status(self) -> dict:
        """Extended status with budget info"""
        status = super().get_status()
        status.update({
            "budget_mode": self.budget_mode,
            "budget": self.get_budget_status()
        })
        return status


# Test
def test_thyroid_v13():
    """Test Cost-Aware Thyroid v1.3"""
    print("\n" + "=" * 70)
    print("  🫁 THYROID v1.3 - Cost-Aware Test")
    print("=" * 70)
    
    class MockQMD:
        def __init__(self):
            self.use_ollama = False
    
    mock_qmd = MockQMD()
    thyroid = AOSThyroidV13(
        qmd_loop=mock_qmd,
        baseline_timeout=10.0,
        secretion_duration=5.0,
        daily_budget=10.0,
        hourly_budget=1.0
    )
    
    print("\n[1] Starting cost-aware thyroid...")
    thyroid.start()
    print(f"   Budget mode: {thyroid.budget_mode}")
    
    print("\n[2] Normal stimulation...")
    stimulated = thyroid.stimulate(importance=0.9)
    print(f"   Stimulated: {stimulated}")
    
    print("\n[3] Simulating high cost (EMERGENCY mode)...")
    thyroid.budget.spent_today = 9.5  # 95% of budget
    thyroid._apply_budget_mode()
    print(f"   Budget mode: {thyroid.budget_mode}")
    
    print("\n[4] Attempt stimulation in EMERGENCY mode...")
    stimulated = thyroid.stimulate(importance=0.9)
    print(f"   Stimulated: {stimulated} (should be False)")
    
    print("\n[5] Budget status:")
    budget = thyroid.get_budget_status()
    for k, v in budget.items():
        print(f"   {k}: {v}")
    
    print("\n[6] Stopping...")
    thyroid.stop()
    
    print("\n" + "=" * 70)
    print("  ✅ Thyroid v1.3 Cost-Aware Test Complete")
    print("=" * 70)


if __name__ == "__main__":
    test_thyroid_v13()
