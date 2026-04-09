#!/usr/bin/env python3
"""
AOS TERNARY SYSTEM - DEPLOYED
Heart + Brain + Stomach (Unified)

Heart: 72 BPM, REST/BALANCE/ACTIVE, coherence, emotion
Brain: 7-region, Ollama-free, OODA loop
Stomach: HUNGRY/SATISFIED/FULL, digestion
"""

import sys
import time
import threading
from pathlib import Path

# Add paths
sys.path.insert(0, '/root/.aos/aos/aos_brain_py/heart')
sys.path.insert(0, '/root/.aos/aos/brain')
sys.path.insert(0, '/root/.aos/aos/stomach')

# Import components
from ternary_heart import TernaryHeart, HeartState
from aos_brain_v3 import AOSBrainv3
from ternary_stomach import TernaryStomach


class TernarySystem:
    """Complete Ternary Organism - Heart + Brain + Stomach"""
    
    def __init__(self):
        print("=" * 70)
        print("  AOS TERNARY SYSTEM")
        print("  Heart + Brain + Stomach")
        print("=" * 70)
        
        # Initialize all three systems
        print("\n[1/3] Initializing Heart (72 BPM, Ternary states)...")
        self.heart = TernaryHeart()
        
        print("[2/3] Initializing Brain (7-region, Ollama-free)...")
        self.brain = AOSBrainv3(
            state_path=Path.home() / ".aos" / "brain" / "state" / "ternary_brain_state.json"
        )
        
        print("[3/3] Initializing Stomach (Ternary digestion)...")
        self.stomach = TernaryStomach()
        
        # Control
        self.running = False
        self._threads = []
        
        print("\n" + "=" * 70)
        print("  All systems initialized")
        print("=" * 70)
    
    def _heart_loop(self):
        """Heart beat loop - provides rhythm to system"""
        while self.running:
            beat = self.heart.beat()
            
            # Calculate sleep time for next beat (60 / BPM)
            sleep_time = 60.0 / beat.rate
            
            # Every 30 beats, log status
            if self.heart.beat_count % 30 == 0:
                status = self.heart.get_status()
                print(f"\n[Heart] Beat {status['beat_count']}: {status['state']}, "
                      f"{status['rate']} BPM, energy={status['energy_level']:.2f}")
            
            time.sleep(sleep_time)
    
    def _brain_loop(self):
        """Brain OODA loop - cognition"""
        while self.running:
            try:
                self.brain.tick()
                
                # Get heart status to influence brain
                heart_status = self.heart.get_status()
                
                # Adjust brain based on heart
                if heart_status['state'] == 'active':
                    self.brain.limbic['reward'] = min(1.0, self.brain.limbic['reward'] + 0.05)
                elif heart_status['state'] == 'rest':
                    self.brain.limbic['reward'] = max(0.0, self.brain.limbic['reward'] - 0.02)
                
                # Log every 100 ticks
                if self.brain.tick_count % 100 == 0:
                    print(f"\n[Brain] Tick {self.brain.tick_count}, "
                          f"Memories: {self.brain.hippocampus.total_traces}, "
                          f"Phase: {self.brain.phase}")
                
                time.sleep(0.1)  # 10 ticks/second
                
            except Exception as e:
                print(f"[Brain] Error: {e}")
                time.sleep(0.1)
    
    def _stomach_loop(self):
        """Stomach digestion loop - provides energy"""
        while self.running:
            result = self.stomach.digest()
            
            # Feed energy to heart
            heart_status = self.heart.get_status()
            self.heart.energy_level = min(1.0, heart_status['energy_level'] + result.energy_produced * 0.1)
            
            # Every 20 cycles, log
            if self.stomach.cycle_count % 20 == 0:
                status = self.stomach.get_status()
                print(f"\n[Stomach] Cycle {status['cycle_count']}: {status['state']}, "
                      f"fullness={status['fullness']:.2f}, "
                      f"total_energy={status['total_energy']:.1f}")
            
            time.sleep(0.5)  # Digest every 500ms
    
    def start(self):
        """Start all systems"""
        print("\n[SYSTEM] Starting Ternary Organism...")
        self.running = True
        
        # Start heart
        print("[SYSTEM] Starting Heart...")
        heart_thread = threading.Thread(target=self._heart_loop, daemon=True)
        heart_thread.start()
        self._threads.append(heart_thread)
        time.sleep(1)
        
        # Start stomach
        print("[SYSTEM] Starting Stomach...")
        stomach_thread = threading.Thread(target=self._stomach_loop, daemon=True)
        stomach_thread.start()
        self._threads.append(stomach_thread)
        time.sleep(1)
        
        # Start brain (main thread)
        print("[SYSTEM] Starting Brain...")
        print("\n" + "=" * 70)
        print("  TERNARY SYSTEM OPERATIONAL")
        print("  Heart beating | Stomach digesting | Brain thinking")
        print("=" * 70)
        print("\nPress Ctrl+C to stop\n")
        
        try:
            self._brain_loop()
        except KeyboardInterrupt:
            pass
    
    def stop(self):
        """Stop all systems gracefully"""
        print("\n\n[SYSTEM] Stopping Ternary Organism...")
        self.running = False
        
        # Save all states
        self.brain._save_state()
        self.heart._save_state()
        self.stomach._save_state()
        
        # Wait for threads
        for t in self._threads:
            t.join(timeout=2.0)
        
        print("[SYSTEM] All systems stopped")
        print("=" * 70)
    
    def get_status(self) -> dict:
        """Get full system status"""
        return {
            "heart": self.heart.get_status(),
            "brain": {
                "tick": self.brain.tick_count,
                "memories": self.brain.hippocampus.total_traces,
                "phase": self.brain.phase
            },
            "stomach": self.stomach.get_status(),
            "running": self.running
        }


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  AOS TERNARY SYSTEM DEPLOYMENT")
    print("  2026-03-31 22:25 UTC")
    print("=" * 70)
    
    system = TernarySystem()
    
    try:
        system.start()
    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        system.stop()
        print("\n" + "=" * 70)
        print("  TERNARY SYSTEM COMPLETE")
        print("=" * 70)
