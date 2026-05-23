#!/usr/bin/env python3
"""
AOS THYROID v1.2 - Endocrine Regulator
Acts like a biological thyroid gland - secretes LLM hormones when needed

Biological analogy:
- Thyroid normally at baseline (LOCAL mode, minimal resources)
- When stimulated (TSH/high importance), it secretes T3/T4 (switches to OLLAMA)
- After secretion pulse, returns to baseline (LOCAL)
- No "cough" - just smooth regulatory adjustment
"""

import time
import threading
import requests
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Optional


class ThyroidState(Enum):
    BASELINE = auto()     # LOCAL mode - minimal resource use
    SECRETING = auto()    # OLLAMA mode - active hormone production
    RECOVERING = auto()   # Transition back to baseline


@dataclass
class ThyroidHormone:
    """Like T3/T4 - the active hormone levels"""
    ollama_level: float    # 0.0 (none) to 1.0 (max)
    local_level: float     # Inverse of ollama_level
    last_secretion: float  # When last stimulated
    secretion_count: int   # How many times secreted today


class AOSThyroidV12:
    """
    Thyroid v1.2 - Endocrine-style regulation
    
    Like a thyroid gland:
    - Baseline: LOCAL mode (low T3/T4 = fast, cheap)
    - When stimulated: Secretes into OLLAMA (high T3/T4 = smart, slower)
    - Auto-returns to baseline after pulse (no cough, just natural decay)
    
    This is regulation, not reflex. Smooth, continuous, hormonal.
    """
    
    def __init__(self, 
                 qmd_loop=None,
                 baseline_timeout: float = 120.0,  # Return to baseline after 2 min
                 secretion_duration: float = 30.0):  # Stay open for 30s min
        self.qmd = qmd_loop
        self.baseline_timeout = baseline_timeout
        self.secretion_duration = secretion_duration
        
        # Hormone levels
        self.hormone = ThyroidHormone(
            ollama_level=0.0,      # Start at baseline (LOCAL)
            local_level=1.0,       # Full local capacity
            last_secretion=0.0,
            secretion_count=0
        )
        
        self.state = ThyroidState.BASELINE
        self.running = False
        self.monitor_thread = None
        
        # Statistics
        self.stats = {
            "secretions_today": 0,
            "total_secretion_time": 0.0,
            "baseline_time": 0.0
        }
        
        print(f"[Thyroid v1.2] Initialized - endocrine regulator")
        print(f"  Baseline: LOCAL mode (minimal resources)")
        print(f"  Secretion: OLLAMA mode (active when needed)")
        print(f"  Auto-return: {baseline_timeout}s after last stimulation")
    
    def start(self):
        """Start the thyroid monitor"""
        self.running = True
        self.monitor_thread = threading.Thread(target=self._regulate, daemon=True)
        self.monitor_thread.start()
        print(f"[Thyroid v1.2] Endocrine regulation active")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        print("[Thyroid v1.2] Regulation stopped")
    
    def _regulate(self):
        """Continuous regulation - like a gland adjusting hormone levels"""
        while self.running:
            try:
                self._adjust_hormones()
                self._apply_to_qmd()
                time.sleep(5)  # Check every 5 seconds
            except Exception as e:
                print(f"[Thyroid] Regulation error: {e}")
                time.sleep(5)
    
    def _adjust_hormones(self):
        """Adjust hormone levels based on time since last stimulation"""
        time_since = time.time() - self.hormone.last_secretion
        
        if self.state == ThyroidState.SECRETING:
            # Minimum secretion duration
            if time_since < self.secretion_duration:
                return  # Stay secreting
            
            # Check if we should return to baseline
            if time_since >= self.baseline_timeout:
                # Decay back to baseline
                decay_factor = 0.9  # Smooth decay
                self.hormone.ollama_level *= decay_factor
                self.hormone.local_level = 1.0 - self.hormone.ollama_level
                
                if self.hormone.ollama_level < 0.1:
                    # Fully returned to baseline
                    self.state = ThyroidState.BASELINE
                    self.hormone.ollama_level = 0.0
                    self.hormone.local_level = 1.0
                    print(f"\n[Thyroid v1.2] 📉 Baseline restored (hormone levels normalized)")
                    print(f"[Thyroid v1.2]    State: BASELINE → LOCAL mode")
    
    def _apply_to_qmd(self):
        """Apply current hormone levels to QMD"""
        if self.qmd:
            # Use OLLAMA when hormone level > 0.5
            self.qmd.use_ollama = (self.hormone.ollama_level > 0.5)
    
    def stimulate(self, importance: float = 0.5) -> bool:
        """
        Stimulate the thyroid to secrete OLLAMA hormone
        Like TSH stimulating the thyroid gland
        
        importance: 0.0-1.0, how much hormone to secrete
        Returns: True if now secreting, False if staying baseline
        """
        if importance < 0.7:
            # Not enough stimulation - stay at baseline
            return False
        
        # Stimulate!
        self.state = ThyroidState.SECRETING
        self.hormone.ollama_level = min(1.0, importance)
        self.hormone.local_level = 1.0 - self.hormone.ollama_level
        self.hormone.last_secretion = time.time()
        self.hormone.secretion_count += 1
        self.stats["secretions_today"] += 1
        
        print(f"\n[Thyroid v1.2] 📈 STIMULATED (importance: {importance:.2f})")
        print(f"[Thyroid v1.2]    OLLAMA hormone level: {self.hormone.ollama_level:.2f}")
        print(f"[Thyroid v1.2]    State: SECRETING → OLLAMA mode")
        
        return True
    
    def get_status(self) -> dict:
        """Current thyroid status"""
        time_since = time.time() - self.hormone.last_secretion if self.hormone.last_secretion > 0 else 999
        
        return {
            "state": self.state.name,
            "ollama_level": self.hormone.ollama_level,
            "local_level": self.hormone.local_level,
            "last_secretion_seconds_ago": time_since,
            "secretion_count_today": self.hormone.secretion_count,
            "baseline_timeout": self.baseline_timeout,
            **self.stats
        }


# Test
def test_thyroid_v12():
    """Test Thyroid v1.2 - endocrine style"""
    print("=" * 70)
    print("  🫁 THYROID v1.2 - Endocrine Regulator Test")
    print("=" * 70)
    
    # Mock QMD
    class MockQMD:
        def __init__(self):
            self.use_ollama = False
    
    mock_qmd = MockQMD()
    thyroid = AOSThyroidV12(qmd_loop=mock_qmd, baseline_timeout=10.0, secretion_duration=5.0)
    
    print("\n[1] Starting...")
    thyroid.start()
    print(f"\n   Initial: {thyroid.get_status()}")
    
    print("\n[2] Baseline for 3 seconds...")
    time.sleep(3)
    print(f"   Still baseline: {thyroid.state.name}")
    
    print("\n[3] Stimulating (importance=0.9)...")
    stimulated = thyroid.stimulate(importance=0.9)
    print(f"   Stimulated: {stimulated}")
    print(f"   QMD use_ollama: {mock_qmd.use_ollama}")
    
    print("\n[4] Waiting for secretion period (5s)...")
    time.sleep(6)
    print(f"   Still secreting: {thyroid.state.name}")
    print(f"   OLLAMA level: {thyroid.hormone.ollama_level:.2f}")
    
    print("\n[5] Waiting for baseline return (5s more)...")
    time.sleep(5)
    print(f"   Now: {thyroid.state.name}")
    print(f"   QMD use_ollama: {mock_qmd.use_ollama}")
    
    print("\n[6] Final status:")
    status = thyroid.get_status()
    for k, v in status.items():
        print(f"   {k}: {v}")
    
    print("\n[7] Stopping...")
    thyroid.stop()
    
    print("\n" + "=" * 70)
    print("  ✅ Thyroid v1.2 Test Complete")
    print("=" * 70)
    print("\n  Summary:")
    print("    • Baseline: LOCAL mode (default, minimal resources)")
    print("    • Stimulation: Opens to OLLAMA when needed")
    print("    • Auto-return: Smooth decay back to baseline")
    print("    • No cough - just endocrine regulation")


if __name__ == "__main__":
    test_thyroid_v12()
