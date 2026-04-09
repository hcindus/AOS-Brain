#!/usr/bin/env python3
"""
AOS TERNARY SYSTEM - UNIFIED DEPLOYMENT
Superior Heart + Brain v3.1 via Standardized Interfaces

Socket-compatible architecture for future assembly
"""

import sys
import time

sys.path.insert(0, '/root/.aos/aos')

from superior_heart import SuperiorHeart
from brain_v31 import AOSBrainV31
from ternary_interfaces import (
    HeartBeatInput, BrainInput, HeartState,
    TernarySystemAssembler
)


class UnifiedTernarySystem:
    """Heart + Brain with standardized socket interface"""
    
    def __init__(self):
        print("=" * 70)
        print("  🫀🧠 AOS TERNARY SYSTEM - UNIFIED")
        print("  Superior Heart + Brain v3.1")
        print("  Standardized Interface Socket")
        print("=" * 70)
        
        # Create organs via standardized interface
        print("\n[Socket 1/2] Creating Superior Heart...")
        self.heart = SuperiorHeart()
        print(f"  Heart: {self.heart.rhythm.bpm} BPM, {self.heart.rhythm.state.name}")
        
        print("[Socket 2/2] Creating Brain v3.1...")
        self.brain = AOSBrainV31()
        print(f"  Brain: {self.brain.tick_count} ticks")
        
        # Metrics
        self.beat_count = 0
        
        print("\n" + "=" * 70)
        print("  ✅ Standardized Sockets Connected")
        print("  Heart Output → Brain Input")
        print("  Brain Output → Heart Input")
        print("=" * 70)
    
    def heartbeat_cycle(self):
        """One heartbeat cycle with standardized interface"""
        # Prepare Heart Input (from Brain state)
        heart_input = HeartBeatInput(
            brain_arousal=self.brain.limbic.get("arousal", 0.5),
            safety=0.8,
            stress=0.2 if self.brain.limbic.get("reward", 0.5) > 0.4 else 0.5,
            connection=0.6,
            cognitive_load=0.5,
            brain_state=self.brain.phase,
            limbic_reward=self.brain.limbic.get("reward", 0.5)
        )
        
        # HEART BEATS (Socket: HeartOutput)
        heart_output = self.heart.beat(heart_input)
        self.beat_count += 1
        
        # Prepare Brain Input (from Heart output)
        brain_input = BrainInput(
            heart_bpm=heart_output.bpm,
            heart_state=heart_output.state,
            heart_coherence=heart_output.coherence,
            heart_arousal=heart_output.arousal,
            emotional_tone=heart_output.emotional_tone,
            observation=f"Heart: {heart_output.bpm:.0f} BPM, {heart_output.emotional_tone}, coherence={heart_output.coherence:.2f}",
            observation_type="heart_signal"
        )
        
        # BRAIN THINKS (Socket: BrainOutput)
        brain_output = self.brain.tick(brain_input)
        
        # Display every 10 beats
        if self.beat_count % 10 == 0:
            print(f"\n[Beat {self.beat_count:3d}] 🫀 {heart_output.bpm:.0f} BPM ({heart_output.emotional_tone:10s}, coherence={heart_output.coherence:.2f}) | "
                  f"🧠 {brain_output.tick_count:5d} ticks | "
                  f"Memories: {brain_output.memories_total:4d} | "
                  f"Action: {brain_output.action_type} | "
                  f"Phase: {brain_output.phase}")
        
        # Heart controls timing
        return 60.0 / heart_output.bpm
    
    def run(self, duration_seconds: int = 60):
        """Run unified system"""
        print(f"\n[SYSTEM] Starting Ternary System for {duration_seconds}s...")
        print("=" * 70)
        print("  🫀 Heart beats → 🧠 Brain thinks → 🧠 Memories form")
        print("  Standardized sockets: HeartOutput → BrainInput")
        print("=" * 70)
        print("\nPress Ctrl+C to stop\n")
        
        start = time.time()
        
        try:
            while time.time() - start < duration_seconds:
                sleep_time = self.heartbeat_cycle()
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            pass
    
    def stop(self):
        """Stop gracefully"""
        print("\n\n[SYSTEM] Stopping...")
        
        self.brain.save_state()
        
        print(f"\n{'='*70}")
        print("  FINAL STATUS")
        print(f"{'='*70}")
        print(f"  🫀 Heart: {self.beat_count} beats")
        print(f"         {self.heart.get_state_summary()}")
        print(f"  🧠 Brain: {self.brain.tick_count} ticks")
        print(f"         {self.brain.hippocampus.total_traces} memories")
        print(f"         Phase: {self.brain.phase}")
        print(f"{'='*70}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🫀🧠 UNIFIED TERNARY SYSTEM")
    print("  Superior Heart + Brain v3.1")
    print("  2026-03-31 22:42 UTC")
    print("=" * 70)
    
    system = UnifiedTernarySystem()
    
    try:
        system.run(duration_seconds=120)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        system.stop()
