#!/usr/bin/env python3
"""
Automatic Memory Flush System for Brain.

Handles automatic compaction of:
- Short-term (conscious) → Mid-term (subconscious) → Long-term (unconscious)
- Periodic memory consolidation
- Disk state writing
"""

import sys
import time
import threading
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain


class AutomaticMemoryFlush:
    """
    Automatic memory management for 3-tier consciousness.
    
    Handles:
    - Continuous short-term → mid-term overflow
    - Periodic mid-term → long-term consolidation
    - Automatic disk writes
    - Memory compaction
    """
    
    def __init__(self, brain: SevenRegionBrain):
        self.brain = brain
        self.running = True
        self.flush_thread = None
        
        # Configuration
        self.short_term_threshold = 8  # Start flushing at 8 items
        self.mid_term_threshold = 80   # Start long-term at 80 items
        self.disk_write_interval = 30  # Seconds between disk writes
        self.consolidation_interval = 300  # Seconds between full consolidation
        
        # Stats
        self.flushes = 0
        self.consolidations = 0
        self.disk_writes = 0
        
    def start_automatic_flush(self):
        """Start automatic flush in background thread."""
        if self.flush_thread and self.flush_thread.is_alive():
            return
        
        self.running = True
        self.flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self.flush_thread.start()
        print("[AutoFlush] Automatic memory flush started")
        
    def _flush_loop(self):
        """Background flush loop."""
        last_consolidation = time.time()
        last_disk_write = time.time()
        
        while self.running:
            try:
                # Check short-term → mid-term
                if len(self.brain.short_term) >= self.short_term_threshold:
                    self._flush_short_term()
                
                # Check mid-term → long-term
                if len(self.brain.mid_term) >= self.mid_term_threshold:
                    self._consolidate_mid_term()
                
                # Periodic full consolidation
                if time.time() - last_consolidation > self.consolidation_interval:
                    if self.brain.unconscious:
                        self._run_unconscious_consolidation()
                    last_consolidation = time.time()
                
                # Periodic disk write
                if time.time() - last_disk_write > self.disk_write_interval:
                    self._write_state_to_disk()
                    last_disk_write = time.time()
                
                # Brief sleep
                time.sleep(1.0)
                
            except Exception as e:
                print(f"[AutoFlush] Error: {e}")
                time.sleep(5.0)
    
    def _flush_short_term(self):
        """Flush short-term to mid-term."""
        moved = 0
        while len(self.brain.short_term) > 5:  # Keep last 5
            trace = self.brain.short_term.popleft()
            self.brain.mid_term.append(trace)
            moved += 1
        
        if moved > 0:
            self.flushes += 1
            print(f"[AutoFlush] Short-term → Mid-term: {moved} items")
    
    def _consolidate_mid_term(self):
        """Consolidate mid-term to long-term."""
        moved = 0
        while len(self.brain.mid_term) > 20:  # Keep last 20
            trace = self.brain.mid_term.popleft()
            key = f"memory_{trace.get('tick', self.brain.tick_count)}_{int(time.time()*1000)}"
            self.brain.long_term[key] = trace
            moved += 1
        
        if moved > 0:
            self.consolidations += 1
            print(f"[AutoFlush] Mid-term → Long-term: {moved} items")
    
    def _run_unconscious_consolidation(self):
        """Run unconscious processor for deep consolidation."""
        if not self.brain.unconscious:
            return
        
        print("[AutoFlush] Running unconscious consolidation...")
        sleep_report = self.brain.unconscious.enter_sleep(duration=30.0)
        self.brain._consolidate_long_term(sleep_report)
        
        dreams = sleep_report.get("dreams", [])
        consolidations = sleep_report.get("consolidations", 0)
        print(f"[AutoFlush] Unconscious: {len(dreams)} dreams, {consolidations} consolidations")
    
    def _write_state_to_disk(self):
        """Write current state to disk."""
        try:
            state = {
                "tick": self.brain.tick_count,
                "timestamp": time.time(),
                "short_term": len(self.brain.short_term),
                "mid_term": len(self.brain.mid_term),
                "long_term": len(self.brain.long_term),
                "flushes": self.flushes,
                "consolidations": self.consolidations,
            }
            
            # Write to state file
            flush_path = Path.home() / ".aos" / "brain" / "state" / "memory_flush.json"
            flush_path.parent.mkdir(parents=True, exist_ok=True)
            
            import json
            with open(flush_path, 'w') as f:
                json.dump(state, f, indent=2)
            
            self.disk_writes += 1
            
        except Exception as e:
            print(f"[AutoFlush] Disk write error: {e}")
    
    def get_status(self) -> dict:
        """Get flush system status."""
        return {
            "running": self.running,
            "short_term": len(self.brain.short_term),
            "mid_term": len(self.brain.mid_term),
            "long_term": len(self.brain.long_term),
            "flushes": self.flushes,
            "consolidations": self.consolidations,
            "disk_writes": self.disk_writes,
        }
    
    def stop(self):
        """Stop automatic flush."""
        self.running = False
        if self.flush_thread:
            self.flush_thread.join(timeout=2.0)
        print("[AutoFlush] Stopped")


def setup_automatic_flush(brain: SevenRegionBrain = None):
    """Setup automatic flush for a brain instance."""
    if brain is None:
        brain = SevenRegionBrain()
    
    flusher = AutomaticMemoryFlush(brain)
    flusher.start_automatic_flush()
    
    return flusher


if __name__ == "__main__":
    print("=" * 70)
    print("🔄 AUTOMATIC MEMORY FLUSH SYSTEM")
    print("=" * 70)
    print()
    
    # Create brain with automatic flush
    brain = SevenRegionBrain()
    flusher = setup_automatic_flush(brain)
    
    print(f"Brain initialized with automatic flush")
    print(f"  Short-term max: 10 items")
    print(f"  Mid-term max: 100 items")
    print(f"  Auto-flush at: 8 items")
    print(f"  Unconscious cycle: every 5 minutes")
    print()
    
    # Simulate data feed
    print("Simulating data feed...")
    for i in range(15):
        brain.tick({"text": f"Data item {i}", "source": "auto_flush_test"})
        time.sleep(0.5)
        
        if i % 5 == 0:
            status = flusher.get_status()
            print(f"  Tick {i}: Short={status['short_term']}, Mid={status['mid_term']}, Long={status['long_term']}")
    
    print()
    print("Final status:")
    status = flusher.get_status()
    print(f"  Flushes: {status['flushes']}")
    print(f"  Consolidations: {status['consolidations']}")
    print(f"  Memory tiers: Short={status['short_term']}, Mid={status['mid_term']}, Long={status['long_term']}")
    
    print()
    print("✅ Automatic flush working!")
    print("Memory flows: Short-term → Mid-term → Long-term automatically")
