#!/usr/bin/env python3
"""
AOS Ternary Stomach
Ternary state machine: HUNGRY / SATISFIED / FULL
Digests data/energy, feeds heart
"""

import time
import json
import threading
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


class StomachState(Enum):
    HUNGRY = "hungry"       # Needs input
    SATISFIED = "satisfied"  # Optimal level
    FULL = "full"           # Saturated, slow digestion


@dataclass
class DigestionResult:
    """Result of digestion"""
    timestamp: float
    input_amount: float
    energy_produced: float
    waste: float


class TernaryStomach:
    """
    Ternary Stomach - digestion and energy production
    States: HUNGRY -> SATISFIED -> FULL
    Feeds energy to heart
    """
    
    def __init__(self, state_path: Path = None):
        self.state_path = state_path or Path.home() / ".aos" / "stomach" / "state" / "stomach_state.json"
        
        # Ternary state
        self.state = StomachState.SATISFIED
        self.fullness = 0.5  # 0.0 to 1.0
        
        # Digestion metrics
        self.digestion_rate = 0.1  # per tick
        self.energy_efficiency = 0.7  # 70% conversion
        
        # Tracking
        self.total_digested = 0.0
        self.total_energy = 0.0
        self.cycle_count = 0
        
        # Threading
        self.running = False
        self._thread: threading.Thread = None
        
        # Load state
        self._load_state()
    
    def _load_state(self):
        """Load existing stomach state"""
        try:
            if self.state_path.exists():
                with open(self.state_path) as f:
                    data = json.load(f)
                    self.state = StomachState(data.get("state", "satisfied"))
                    self.fullness = data.get("fullness", 0.5)
                    self.total_digested = data.get("total_digested", 0.0)
                    self.total_energy = data.get("total_energy", 0.0)
                    print(f"[Stomach] Loaded state: {self.state.value}, fullness: {self.fullness:.2f}")
        except:
            pass
    
    def _save_state(self):
        """Save stomach state"""
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_path, 'w') as f:
                json.dump({
                    "state": self.state.value,
                    "fullness": self.fullness,
                    "total_digested": self.total_digested,
                    "total_energy": self.total_energy,
                    "timestamp": time.time()
                }, f, indent=2)
        except:
            pass
    
    def _ternary_transition(self):
        """Transition between ternary states based on fullness"""
        if self.fullness < 0.3:
            # Empty - transition to HUNGRY
            if self.state != StomachState.HUNGRY:
                print(f"[Stomach] Transitioning {self.state.value} -> HUNGRY (fullness: {self.fullness:.2f})")
                self.state = StomachState.HUNGRY
        elif self.fullness > 0.9:
            # Full - transition to FULL
            if self.state != StomachState.FULL:
                print(f"[Stomach] Transitioning {self.state.value} -> FULL (fullness: {self.fullness:.2f})")
                self.state = StomachState.FULL
        else:
            # Good level - SATISFIED
            if self.state != StomachState.SATISFIED:
                print(f"[Stomach] Transitioning {self.state.value} -> SATISFIED (fullness: {self.fullness:.2f})")
                self.state = StomachState.SATISFIED
    
    def digest(self, input_amount: float = 0.1) -> DigestionResult:
        """Process one digestion cycle"""
        # Update state
        self._ternary_transition()
        
        # Calculate digestion based on state
        if self.state == StomachState.FULL:
            # Slow digestion when full
            digest_amount = input_amount * 0.5
            self.fullness = min(1.0, self.fullness + input_amount * 0.1)
        elif self.state == StomachState.HUNGRY:
            # Fast digestion when hungry
            digest_amount = min(self.fullness, input_amount * 1.5)
            self.fullness += input_amount
        else:  # SATISFIED
            # Normal digestion
            digest_amount = min(self.fullness, input_amount)
            self.fullness = self.fullness - digest_amount + input_amount * 0.05
        
        self.fullness = max(0.0, min(1.0, self.fullness))
        
        # Convert to energy
        energy_produced = digest_amount * self.energy_efficiency
        waste = digest_amount - energy_produced
        
        # Update totals
        self.total_digested += digest_amount
        self.total_energy += energy_produced
        self.cycle_count += 1
        
        result = DigestionResult(
            timestamp=time.time(),
            input_amount=input_amount,
            energy_produced=energy_produced,
            waste=waste
        )
        
        # Save periodically
        if self.cycle_count % 10 == 0:
            self._save_state()
        
        return result
    
    def run(self):
        """Main stomach loop"""
        print(f"[Stomach] Starting Ternary Stomach")
        print(f"[Stomach] Initial state: {self.state.value}, fullness: {self.fullness:.2f}")
        
        while self.running:
            result = self.digest()
            
            # Log every 20 cycles
            if self.cycle_count % 20 == 0:
                print(f"[Stomach] Cycle {self.cycle_count}: {self.state.value}, "
                      f"fullness={self.fullness:.2f}, energy_produced={result.energy_produced:.3f}")
            
            time.sleep(0.5)  # Digest every 500ms
    
    def start(self) -> bool:
        """Start stomach in background thread"""
        if self.running:
            return True
        
        self.running = True
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()
        print(f"[Stomach] Started (PID: {self._thread.ident})")
        return True
    
    def stop(self):
        """Stop stomach"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        self._save_state()
        print("[Stomach] Stopped")
    
    def get_status(self) -> dict:
        """Get stomach status"""
        return {
            "state": self.state.value,
            "fullness": self.fullness,
            "total_digested": self.total_digested,
            "total_energy": self.total_energy,
            "cycle_count": self.cycle_count,
            "running": self.running
        }


if __name__ == "__main__":
    print("=" * 60)
    print("  AOS Ternary Stomach")
    print("  HUNGRY / SATISFIED / FULL")
    print("=" * 60)
    
    stomach = TernaryStomach()
    
    try:
        stomach.start()
        
        # Run for 60 seconds
        for i in range(6):
            time.sleep(10)
            status = stomach.get_status()
            print(f"\n[T+{i*10+10}s] Status: {status}")
    
    except KeyboardInterrupt:
        pass
    
    finally:
        stomach.stop()
        print("=" * 60)
        print("  Stomach stopped")
        print("=" * 60)
