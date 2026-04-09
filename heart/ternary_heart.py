#!/usr/bin/env python3
"""
AOS Ternary Heart
Ternary state machine: REST / BALANCE / ACTIVE
30 BPM rhythmic beating
Feeds energy to brain
"""

import time
import json
import threading
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


class HeartState(Enum):
    REST = "rest"       # Low energy, recovery
    BALANCE = "balance" # Steady state
    ACTIVE = "active"   # High energy output


@dataclass
class HeartBeat:
    """Single heartbeat data"""
    timestamp: float
    state: HeartState
    rate: int  # BPM
    energy_output: float


class TernaryHeart:
    """
    Ternary Heart - rhythmic energy pump
    States: REST <-> BALANCE <-> ACTIVE
    Default: 30 BPM
    """
    
    def __init__(self, state_path: Path = None):
        self.state_path = state_path or Path.home() / ".aos" / "heart" / "state" / "heart_state.json"
        
        # Ternary state
        self.state = HeartState.BALANCE
        self.energy_level = 0.5  # 0.0 to 1.0
        
        # Heart rate (default 30 BPM)
        self.base_rate = 30
        self.current_rate = 30
        
        # Beat tracking
        self.beat_count = 0
        self.last_beat = time.time()
        self.beat_history = []
        
        # Energy distribution
        self.brain_allocation = 0.6
        self.system_allocation = 0.4
        
        # Threading
        self.running = False
        self._thread: threading.Thread = None
        
        # Load state
        self._load_state()
    
    def _load_state(self):
        """Load existing heart state"""
        try:
            if self.state_path.exists():
                with open(self.state_path) as f:
                    data = json.load(f)
                    self.state = HeartState(data.get("state", "balance"))
                    self.beat_count = data.get("beat_count", 0)
                    self.energy_level = data.get("energy_level", 0.5)
                    print(f"[Heart] Loaded state: {self.state.value}, beats: {self.beat_count}")
        except:
            pass
    
    def _save_state(self):
        """Save heart state"""
        try:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_path, 'w') as f:
                json.dump({
                    "state": self.state.value,
                    "beat_count": self.beat_count,
                    "energy_level": self.energy_level,
                    "rate": self.current_rate,
                    "timestamp": time.time()
                }, f, indent=2)
        except:
            pass
    
    def _ternary_transition(self):
        """Transition between ternary states based on energy level"""
        if self.energy_level < 0.3:
            # Low energy - transition to REST
            if self.state != HeartState.REST:
                print(f"[Heart] Transitioning {self.state.value} -> REST (energy: {self.energy_level:.2f})")
                self.state = HeartState.REST
        elif self.energy_level > 0.8:
            # High energy - transition to ACTIVE
            if self.state != HeartState.ACTIVE:
                print(f"[Heart] Transitioning {self.state.value} -> ACTIVE (energy: {self.energy_level:.2f})")
                self.state = HeartState.ACTIVE
        else:
            # Medium energy - BALANCE
            if self.state != HeartState.BALANCE:
                print(f"[Heart] Transitioning {self.state.value} -> BALANCE (energy: {self.energy_level:.2f})")
                self.state = HeartState.BALANCE
    
    def _calculate_rate(self) -> int:
        """Calculate current heart rate based on state"""
        if self.state == HeartState.REST:
            return max(20, self.base_rate - 10)  # Slower
        elif self.state == HeartState.ACTIVE:
            return min(60, self.base_rate + 20)  # Faster
        else:  # BALANCE
            return self.base_rate
    
    def beat(self) -> HeartBeat:
        """Generate single heartbeat"""
        # Update state
        self._ternary_transition()
        self.current_rate = self._calculate_rate()
        
        # Calculate energy output
        if self.state == HeartState.REST:
            energy_out = 0.3
            self.energy_level = min(1.0, self.energy_level + 0.05)  # Recover
        elif self.state == HeartState.ACTIVE:
            energy_out = 0.8
            self.energy_level = max(0.0, self.energy_level - 0.03)  # Consume
        else:  # BALANCE
            energy_out = 0.5
            self.energy_level += 0.01  # Slight gain
            self.energy_level = max(0.0, min(1.0, self.energy_level))
        
        # Create beat
        beat = HeartBeat(
            timestamp=time.time(),
            state=self.state,
            rate=self.current_rate,
            energy_output=energy_out
        )
        
        self.beat_count += 1
        self.last_beat = time.time()
        self.beat_history.append(beat)
        
        # Trim history
        if len(self.beat_history) > 100:
            self.beat_history = self.beat_history[-50:]
        
        # Save periodically
        if self.beat_count % 10 == 0:
            self._save_state()
        
        return beat
    
    def run(self):
        """Main heart loop - beats at current rate"""
        print(f"[Heart] Starting Ternary Heart at {self.base_rate} BPM")
        print(f"[Heart] Initial state: {self.state.value}")
        
        while self.running:
            beat = self.beat()
            
            # Calculate sleep time for next beat
            sleep_time = 60.0 / beat.rate
            
            # Log every 30 beats
            if self.beat_count % 30 == 0:
                print(f"[Heart] Beat {self.beat_count}: {beat.state.value}, "
                      f"{beat.rate} BPM, energy={self.energy_level:.2f}")
            
            time.sleep(sleep_time)
    
    def start(self) -> bool:
        """Start heart in background thread"""
        if self.running:
            return True
        
        self.running = True
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()
        print(f"[Heart] Started (PID: {self._thread.ident})")
        return True
    
    def stop(self):
        """Stop heart"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        self._save_state()
        print("[Heart] Stopped")
    
    def get_status(self) -> dict:
        """Get heart status"""
        return {
            "state": self.state.value,
            "beat_count": self.beat_count,
            "rate": self.current_rate,
            "energy_level": self.energy_level,
            "running": self.running
        }


if __name__ == "__main__":
    print("=" * 60)
    print("  AOS Ternary Heart")
    print("  REST / BALANCE / ACTIVE")
    print("=" * 60)
    
    heart = TernaryHeart()
    
    try:
        heart.start()
        
        # Run for 60 seconds
        for i in range(6):
            time.sleep(10)
            status = heart.get_status()
            print(f"\n[T+{i*10+10}s] Status: {status}")
    
    except KeyboardInterrupt:
        pass
    
    finally:
        heart.stop()
        print("=" * 60)
        print("  Heart stopped")
        print("=" * 60)
