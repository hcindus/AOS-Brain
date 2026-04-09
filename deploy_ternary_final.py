#!/usr/bin/env python3
"""
AOS TERNARY SYSTEM - FINAL DEPLOYMENT
Brain v3.0 (Ollama-free) + Ternary Heart (72 BPM)

Complete working integration.
"""

import sys
import time
import threading
from pathlib import Path

# Add paths
sys.path.insert(0, '/root/.aos/aos/aos_brain_py/heart')
sys.path.insert(0, '/root/.aos/aos/brain')

from ternary_heart import TernaryHeart, HeartState
from aos_brain_v3 import AOSBrainv3


class TernarySystem:
    """Complete Ternary Organism - Working Integration"""
    
    def __init__(self):
        print("=" * 70)
        print("  🫀🧠 AOS TERNARY SYSTEM")
        print("  Brain v3.0 + Ternary Heart")
        print("=" * 70)
        
        # Initialize heart
        print("\n[1/2] Initializing Ternary Heart...")
        self.heart = TernaryHeart()
        
        # Initialize brain (Ollama-free)
        print("[2/2] Initializing Brain v3.0...")
        self.brain = AOSBrainv3()
        
        # Control
        self.running = False
        self.tick_count = 0
        
        print("\n" + "=" * 70)
        print("  All systems ready")
        print("=" * 70)
    
    def run(self):
        """Main loop - Heart provides rhythm, Brain provides cognition"""
        print("\n[SYSTEM] Starting Ternary Organism...")
        print("\n" + "=" * 70)
        print("  🫀 Heart beats → 🧠 Brain thinks → 🧠 Memories form")
        print("=" * 70)
        print("\nPress Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                # Heart beat - provides rhythm and emotion
                heart_inputs = {
                    "brain_arousal": self.brain.limbic.get("novelty", 0.5),
                    "safety": 0.8,
                    "stress": 0.2,
                    "connection": 0.6
                }
                
                heart_outputs = self.heart.beat(heart_inputs)
                
                # Brain tick - cognition
                self.brain.tick()
                self.tick_count += 1
                
                # Display every 50 ticks
                if self.tick_count % 50 == 0:
                    heart_bpm = heart_outputs.get("heart_bpm", 72)
                    heart_state = heart_outputs.get("heart_state", 0)
                    emotion = heart_outputs.get("heart_emotional_tone", "neutral")
                    coherence = heart_outputs.get("heart_coherence", 0.5)
                    
                    print(f"[Tick {self.brain.tick_count:5d}] "
                          f"🫀 {heart_state:2d} ({heart_bpm:.0f} BPM, {emotion:10s}, coherence={coherence:.2f}) | "
                          f"🧠 {self.brain.hippocampus.total_traces:4d} memories | "
                          f"Phase: {self.brain.phase}")
                
                # Heart rate determines timing (60 / BPM seconds)
                sleep_time = 60.0 / 72.0  # ~0.83 seconds per beat
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            pass
    
    def stop(self):
        """Stop gracefully"""
        print("\n\n[SYSTEM] Stopping...")
        self.running = False
        
        # Save brain state
        self.brain._save_state()
        
        # Final status
        print(f"\n{'='*70}")
        print("  FINAL STATUS")
        print(f"{'='*70}")
        print(f"  Brain: {self.brain.tick_count} ticks")
        print(f"  Memories: {self.brain.hippocampus.total_traces}")
        print(f"  Heart: {self.heart.rhythm.beat_count} beats")
        print(f"  Heart Summary: {self.heart.get_state_summary()}")
        print(f"{'='*70}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🫀🧠 AOS TERNARY SYSTEM DEPLOYMENT")
    print("  2026-03-31 22:30 UTC")
    print("=" * 70)
    
    system = TernarySystem()
    
    try:
        system.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        system.stop()
