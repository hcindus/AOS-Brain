#!/usr/bin/env python3
"""
AOS Ternary System - Complete Organism
Brain + Heart + Stomach integrated

Ternary States:
- Brain: Observe/Orient/Decide/Act
- Heart: REST/BALANCE/ACTIVE (30 BPM)
- Stomach: HUNGRY/SATISFIED/FULL
"""

import sys
import time
import threading
from pathlib import Path

# Add paths
sys.path.insert(0, '/root/.aos/aos/brain')
sys.path.insert(0, '/root/.aos/aos/heart')
sys.path.insert(0, '/root/.aos/aos/stomach')

from aos_brain_v3 import AOSBrainv3
from ternary_heart import TernaryHeart
from ternary_stomach import TernaryStomach


class TernaryOrganism:
    """
    Complete AOS Ternary Organism
    All three systems working together
    """
    
    def __init__(self):
        print("[TernarySystem] Initializing complete organism...")
        
        # Initialize all three systems
        self.brain = AOSBrainv3()
        self.heart = TernaryHeart()
        self.stomach = TernaryStomach()
        
        # Integration thread
        self.running = False
        self._integration_thread: threading.Thread = None
        
        print("[TernarySystem] All systems initialized")
    
    def _integration_loop(self):
        """
        Integration loop - coordinates brain, heart, stomach
        """
        while self.running:
            # Get heart status
            heart_status = self.heart.get_status()
            
            # Feed heart energy from stomach
            stomach_status = self.stomach.get_status()
            
            # Adjust brain based on heart state
            if heart_status["state"] == "active":
                # High energy - brain can work harder
                self.brain.limbic["reward"] = min(1.0, self.brain.limbic["reward"] + 0.1)
            elif heart_status["state"] == "rest":
                # Low energy - conserve
                self.brain.limbic["reward"] = max(0.0, self.brain.limbic["reward"] - 0.05)
            
            # Log system status every 10 cycles
            if self.brain.tick_count % 100 == 0 and self.brain.tick_count > 0:
                print(f"\n[TernarySystem] Status at tick {self.brain.tick_count}:")
                print(f"  Brain: {self.brain.tick_count} ticks, {self.brain.hippocampus.total_traces} memories")
                print(f"  Heart: {heart_status['beat_count']} beats, {heart_status['state']}, {heart_status['rate']} BPM")
                print(f"  Stomach: {stomach_status['cycle_count']} cycles, {stomach_status['state']}, fullness={stomach_status['fullness']:.2f}")
            
            time.sleep(0.1)
    
    def start(self):
        """Start all systems"""
        print("[TernarySystem] Starting complete organism...")
        print("=" * 60)
        
        # Start heart
        self.heart.start()
        time.sleep(0.5)
        
        # Start stomach
        self.stomach.start()
        time.sleep(0.5)
        
        # Start integration
        self.running = True
        self._integration_thread = threading.Thread(target=self._integration_loop, daemon=True)
        self._integration_thread.start()
        
        print("[TernarySystem] Heart beating")
        print("[TernarySystem] Stomach digesting")
        print("[TernarySystem] Brain thinking")
        print("[TernarySystem] Integration active")
        print("=" * 60)
        
        # Run brain in main thread
        self.brain.run(duration_seconds=300)  # Run for 5 minutes
    
    def stop(self):
        """Stop all systems"""
        print("\n[TernarySystem] Stopping organism...")
        self.running = False
        
        self.brain._save_state()
        self.heart.stop()
        self.stomach.stop()
        
        if self._integration_thread:
            self._integration_thread.join(timeout=2.0)
        
        print("[TernarySystem] Organism stopped")


if __name__ == "__main__":
    print("=" * 60)
    print("  AOS TERNARY SYSTEM")
    print("  Complete Organism: Brain + Heart + Stomach")
    print("  REST/BALANCE/ACTIVE | HUNGRY/SATISFIED/FULL")
    print("=" * 60)
    
    organism = TernaryOrganism()
    
    try:
        organism.start()
    except KeyboardInterrupt:
        pass
    finally:
        organism.stop()
        print("=" * 60)
        print("  Ternary System Complete")
        print("=" * 60)
