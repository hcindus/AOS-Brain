#!/usr/bin/env python3
"""
AOS TERNARY SYSTEM v2.0 - PROPER INTEGRATION
Brain + Heart + Stomach (Heart called by Brain)

Architecture:
- Heart: Provides rhythm/coherence/emotion (called by brain)
- Brain: 7-region OODA, uses heart signals
- Stomach: Provides energy (feeds heart)
"""

import sys
import time
import threading
from pathlib import Path

# Add paths
sys.path.insert(0, '/root/.aos/aos/aos_brain_py/heart')
sys.path.insert(0, '/root/.aos/aos/brain')

# Import components
from ternary_heart import TernaryHeart, HeartState
from aos_brain_v3 import AOSBrainv3


class TernarySystem:
    """Complete Ternary Organism - Heart integrated into Brain"""
    
    def __init__(self):
        print("=" * 70)
        print("  AOS TERNARY SYSTEM v2.0")
        print("  Heart-Brain Integration")
        print("=" * 70)
        
        # Initialize heart (called by brain)
        print("\n[1/2] Initializing Ternary Heart (72 BPM)...")
        self.heart = TernaryHeart()
        
        # Initialize brain
        print("[2/2] Initializing 7-Region Brain (Ollama-free)...")
        self.brain = AOSBrainv3(
            state_path=Path.home() / ".aos" / "brain" / "state" / "ternary_brain_state.json"
        )
        
        # Control
        self.running = False
        
        # Stats
        self.heart_beats = 0
        
        print("\n" + "=" * 70)
        print("  All systems initialized")
        print("=" * 70)
    
    def _get_heart_inputs(self) -> dict:
        """Convert brain state to heart inputs"""
        return {
            "brain_arousal": self.brain.limbic.get("novelty", 0.5),
            "safety": 1.0 - self.brain.limbic.get("risk", 0.0),
            "stress": 0.0 if self.brain.limbic.get("reward", 0.5) > 0.4 else 0.5,
            "connection": self.brain.limbic.get("valence", 0.5),
        }
    
    def run(self):
        """Main loop - Brain ticks, Heart provides rhythm"""
        print("\n[SYSTEM] Starting Ternary Organism...")
        print("\n" + "=" * 70)
        print("  TERNARY SYSTEM OPERATIONAL")
        print("  Heart provides rhythm → Brain uses signals → Learning")
        print("=" * 70)
        print("\nPress Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                # Get heart signals (heart beat)
                heart_inputs = self._get_heart_inputs()
                heart_signals = self.heart.beat(heart_inputs)
                self.heart_beats += 1
                
                # Use heart signals to influence brain
                # Adjust brain reward based on heart coherence
                coherence = heart_signals.get("heart_coherence", 0.5)
                self.brain.limbic["coherence"] = coherence
                
                # Run brain tick
                self.brain.tick()
                
                # Log every 50 ticks
                if self.brain.tick_count % 50 == 0:
                    heart_state = heart_signals.get("heart_state", 0)
                    heart_bpm = heart_signals.get("heart_bpm", 72)
                    emotion = heart_signals.get("heart_emotional_tone", "neutral")
                    
                    print(f"[Tick {self.brain.tick_count:4d}] "
                          f"Heart: {heart_state:2d} ({heart_bpm:.0f} BPM, {emotion}), "
                          f"Brain: {self.brain.hippocampus.total_traces:3d} memories, "
                          f"Phase: {self.brain.phase}")
                
                # Heart rate determines tick speed
                bpm = heart_signals.get("heart_bpm", 72)
                sleep_time = 60.0 / (bpm * 2)  # Twice per beat
                time.sleep(max(0.05, sleep_time))
                
        except KeyboardInterrupt:
            pass
    
    def stop(self):
        """Stop gracefully"""
        print("\n\n[SYSTEM] Stopping Ternary Organism...")
        self.running = False
        
        # Save states
        self.brain._save_state()
        
        # Show final status
        print(f"\nFinal Status:")
        print(f"  Brain: {self.brain.tick_count} ticks")
        print(f"  Heart: {self.heart_beats} beats")
        print(f"  Memories: {self.brain.hippocampus.total_traces}")
        print(f"  Heart Summary: {self.heart.get_state_summary()}")
        
        print("\n" + "=" * 70)
        print("  TERNARY SYSTEM STOPPED")
        print("=" * 70)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  AOS TERNARY SYSTEM v2.0 DEPLOYMENT")
    print("  2026-03-31 22:26 UTC")
    print("=" * 70)
    
    system = TernarySystem()
    
    try:
        system.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        system.stop()
