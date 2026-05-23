#!/usr/bin/env python3
"""
AOS THYROID v1.1 - Enhanced with Model Router
Dynamic mode switcher with intelligent model selection
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import time
import threading
import requests
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional

from model_router import AOSModelRouter


class BrainMode(Enum):
    LOCAL = auto()      # Fast, cheap, rule-based
    OLLAMA = auto()    # Smart, slower, LLM-powered


@dataclass  
class ThyroidState:
    current_mode: BrainMode
    last_switch: float
    ollama_failures: int
    local_confidence: float
    network_healthy: bool
    cost_budget: float
    memory_percent: float


class AOSThyroidV11:
    """
    Thyroid v1.1 - Now with Model Router integration
    
    Like coughing to clear your throat, but now also choosing
    which 'medicine' (model) to use when you're congested.
    """
    
    def __init__(self, 
                 qmd_loop=None,
                 check_interval: float = 30.0,
                 failure_threshold: int = 3,
                 memory_threshold: float = 75.0):
        self.qmd = qmd_loop
        self.check_interval = check_interval
        self.failure_threshold = failure_threshold
        self.memory_threshold = memory_threshold
        
        # NEW: Model Router
        self.router = AOSModelRouter()
        
        self.state = ThyroidState(
            current_mode=BrainMode.LOCAL,
            last_switch=time.time(),
            ollama_failures=0,
            local_confidence=0.5,
            network_healthy=True,
            cost_budget=1.0,
            memory_percent=50.0
        )
        
        self.running = False
        self.monitor_thread = None
        self.on_mode_switch: Optional[Callable[[BrainMode, BrainMode], None]] = None
        
        print(f"[Thyroid v1.1] Initialized with Model Router")
        print(f"  Decision model: {self.router.MODELS['decision']}")
        print(f"  Voice model: {self.router.MODELS['voice']}")
    
    def start(self):
        """Start the thyroid monitor"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"[Thyroid v1.1] Monitor active")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        print("[Thyroid v1.1] Stopped")
    
    def _get_memory_percent(self) -> float:
        """Check current memory usage"""
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                mem_total = int(lines[0].split()[1])  # kB
                mem_available = int(lines[2].split()[1])  # kB
                used = mem_total - mem_available
                return (used / mem_total) * 100
        except:
            return 50.0
    
    def _monitor_loop(self):
        """Monitor system conditions"""
        while self.running:
            try:
                self._check_conditions()
                time.sleep(self.check_interval)
            except Exception as e:
                print(f"[Thyroid] Monitor error: {e}")
                time.sleep(5)
    
    def _check_conditions(self):
        """Check if we need to cough (switch modes)"""
        
        # Update metrics
        self.state.memory_percent = self._get_memory_percent()
        ollama_healthy = self._ping_ollama()
        errors_high = self.state.ollama_failures >= self.failure_threshold
        budget_ok = self.state.cost_budget > 0.1
        memory_ok = self.state.memory_percent < self.memory_threshold
        
        # Adjust cost budget based on memory
        if not memory_ok:
            self.state.cost_budget = max(0.0, self.state.cost_budget - 0.1)
            if self.state.current_mode == BrainMode.OLLAMA:
                print(f"[Thyroid] Memory high ({self.state.memory_percent:.0f}%), reducing budget")
        
        current = self.state.current_mode
        
        # COUGH logic
        if current == BrainMode.OLLAMA:
            if not ollama_healthy or errors_high or not budget_ok or not memory_ok:
                reason = f"ollama={ollama_healthy}, errors={errors_high}, budget={budget_ok:.1f}, mem={memory_ok}"
                self._cough(BrainMode.LOCAL, reason=reason)
                
        elif current == BrainMode.LOCAL:
            if (ollama_healthy and 
                self.state.ollama_failures == 0 and 
                budget_ok and 
                memory_ok and
                self._should_promote()):
                self._cough(BrainMode.OLLAMA, reason="conditions_good")
    
    def _ping_ollama(self) -> bool:
        """Quick health check"""
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=5)
            if resp.status_code == 200:
                self.state.network_healthy = True
                return True
        except:
            pass
        self.state.network_healthy = False
        return False
    
    def _should_promote(self) -> bool:
        """Hysteresis - prevent flip-flopping"""
        time_since = time.time() - self.state.last_switch
        return time_since > 60
    
    def _cough(self, new_mode: BrainMode, reason: str):
        """Switch modes"""
        old_mode = self.state.current_mode
        if old_mode == new_mode:
            return
        
        print(f"\n[Thyroid v1.1] 🤧 COUGH! {old_mode.name} → {new_mode.name}")
        print(f"[Thyroid v1.1]    Reason: {reason}")
        
        self.state.current_mode = new_mode
        self.state.last_switch = time.time()
        
        # Update QMD
        if self.qmd:
            self.qmd.use_ollama = (new_mode == BrainMode.OLLAMA)
            if new_mode == BrainMode.OLLAMA:
                # NEW: Use model router for better decisions
                self.qmd.model = self.router.MODELS['decision']
                print(f"[Thyroid v1.1]    Using {self.qmd.model} for decisions")
            print(f"[Thyroid v1.1]    QMD mode: {'OLLAMA' if self.qmd.use_ollama else 'LOCAL'}")
        
        if self.on_mode_switch:
            self.on_mode_switch(old_mode, new_mode)
    
    def report_failure(self):
        """Report Ollama failure"""
        self.state.ollama_failures += 1
        print(f"[Thyroid] Failure {self.state.ollama_failures}/{self.failure_threshold}")
        if self.state.ollama_failures >= self.failure_threshold:
            self._cough(BrainMode.LOCAL, reason="failure_threshold")
    
    def report_success(self):
        """Report Ollama success"""
        if self.state.ollama_failures > 0:
            self.state.ollama_failures -= 1
    
    def request_promotion(self, importance: float = 0.5) -> bool:
        """Request promotion for important decision"""
        if importance > 0.7 and self.state.current_mode == BrainMode.LOCAL:
            checks = [
                self._ping_ollama(),
                self.state.cost_budget > 0.2,
                self.state.memory_percent < self.memory_threshold
            ]
            if all(checks):
                self._cough(BrainMode.OLLAMA, reason=f"high_importance({importance:.2f})")
                return True
        return False
    
    def get_status(self) -> dict:
        """Current status"""
        return {
            "mode": self.state.current_mode.name,
            "failures": self.state.ollama_failures,
            "budget": self.state.cost_budget,
            "memory_percent": self.state.memory_percent,
            "network": self.state.network_healthy,
            "last_switch": time.time() - self.state.last_switch,
            "models": self.router.MODELS
        }


# Test
def test_thyroid_v11():
    """Test Thyroid v1.1 with Model Router"""
    print("=" * 70)
    print("  🧠 THYROID v1.1 + MODEL ROUTER TEST")
    print("=" * 70)
    
    # Mock QMD
    class MockQMD:
        def __init__(self):
            self.use_ollama = False
            self.model = "none"
    
    mock_qmd = MockQMD()
    thyroid = AOSThyroidV11(qmd_loop=mock_qmd, check_interval=10.0)
    
    print("\n[1] Starting Thyroid...")
    thyroid.start()
    
    print("\n[2] Initial status:")
    status = thyroid.get_status()
    print(f"    Mode: {status['mode']}")
    print(f"    Memory: {status['memory_percent']:.0f}%")
    print(f"    Models: {status['models']}")
    
    print("\n[3] Testing promotion (importance=0.9)...")
    time.sleep(1)
    promoted = thyroid.request_promotion(importance=0.9)
    print(f"    Promoted: {promoted}")
    if promoted:
        print(f"    Now using: {mock_qmd.model}")
    
    print("\n[4] Simulating failures...")
    thyroid.report_failure()
    thyroid.report_failure()
    thyroid.report_failure()
    
    print("\n[5] Testing router directly...")
    print("\n    Decision test (should use tinyllama):")
    action, conf = thyroid.router.decide({
        "novelty": 0.8,
        "reward": 0.4,
        "phase": "Observe",
        "observation": "Test pattern"
    })
    print(f"    Result: {action} ({conf:.2f})")
    
    print("\n    Voice test (should use Mort_II):")
    response = thyroid.router.speak("Hello", {"situation": "greeting"})
    print(f"    Response: '{response[:60]}...'")
    
    print("\n[6] Router stats:")
    stats = thyroid.router.get_stats()
    for task, data in stats.items():
        if data['calls'] > 0:
            print(f"    {task}: {data['calls']} calls, {data['avg_latency']:.0f}ms avg")
    
    print("\n[7] Stopping...")
    thyroid.stop()
    
    print("\n" + "=" * 70)
    print("  ✅ Thyroid v1.1 Test Complete")
    print("=" * 70)
    print("\n  Summary:")
    print("    • Thyroid manages LOCAL vs OLLAMA mode")
    print("    • Model Router selects optimal LLM per task")
    print("    • tinyllama → fast decisions")
    print("    • Mort_II → natural voice")


if __name__ == "__main__":
    test_thyroid_v11()
