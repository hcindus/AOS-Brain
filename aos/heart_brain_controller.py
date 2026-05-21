#!/usr/bin/env python3
"""
Heart-Brain Controller
The HEART controls the heartbeat and timing
The BRAIN waits for heart signals
"""

import sys
import time
import threading
from pathlib import Path

sys.path.insert(0, '/root/.aos/aos/aos_brain_py/heart')
sys.path.insert(0, '/root/.aos/aos/brain')

from ternary_heart import TernaryHeart, HeartState
from aos_brain_v3 import AOSBrainv3


class HeartBrainController:
    """
    Heart controls the beat, Brain responds.
    The heart is the pacemaker.
    """
    
    def __init__(self):
        print("=" * 70)
        print("  🫀🧠 HEART-BRAIN CONTROLLER")
        print("  Heart controls rhythm | Brain responds")
        print("=" * 70)
        
        # Heart is the controller
        print("\n[Init] Creating Heart (pacemaker)...")
        self.heart = TernaryHeart()
        
        # Brain follows heart
        print("[Init] Creating Brain (follower)...")
        self.brain = AOSBrainv3()
        
        # Control
        self.running = False
        self.beat_count = 0
        
        print("\n" + "=" * 70)
        print("  ✅ Heart-Brain Controller Ready")
        print("=" * 70)
    
    def heartbeat_cycle(self):
        """
        One heartbeat cycle:
        1. Heart beats (generates rhythm, emotion, arousal)
        2. Heart signals flow to brain
        3. Brain processes (one tick per heartbeat)
        4. Brain state feeds back to heart
        """
        # Prepare heart inputs from brain state
        heart_inputs = {
            "brain_arousal": self.brain.limbic.get("novelty", 0.5),
            "safety": 0.8,
            "stress": 0.2 if self.brain.limbic.get("reward", 0.5) > 0.4 else 0.5,
            "connection": 0.6,
        }
        
        # 1. HEART BEATS (generates rhythm)
        heart_signals = self.heart.beat(heart_inputs)
        self.beat_count += 1
        
        # Extract heart data
        bpm = heart_signals.get("heart_bpm", 72)
        heart_state = heart_signals.get("heart_state", 0)
        emotion = heart_signals.get("heart_emotional_tone", "neutral")
        coherence = heart_signals.get("heart_coherence", 0.5)
        arousal = heart_signals.get("heart_arousal", 0.5)
        
        # 2. HEART SIGNALS → BRAIN
        # Arousal influences brain reward
        self.brain.limbic["arousal"] = arousal
        self.brain.limbic["coherence"] = coherence
        
        # Adjust reward based on heart state
        if heart_state == 1:  # ACTIVE
            self.brain.limbic["reward"] = min(1.0, self.brain.limbic["reward"] + 0.1)
        elif heart_state == -1:  # REST
            self.brain.limbic["reward"] = max(0.0, self.brain.limbic["reward"] - 0.05)
        
        # 3. BRAIN PROCESSES (one tick per heartbeat)
        self.brain.tick()
        
        # 4. Display status every 10 beats
        if self.beat_count % 10 == 0:
            print(f"\n[Beat {self.beat_count:3d}] 🫀 {bpm:.0f} BPM ({emotion:10s}, coherence={coherence:.2f}) | "
                  f"🧠 {self.brain.tick_count:5d} ticks | "
                  f"Memories: {self.brain.hippocampus.total_traces:4d} | "
                  f"Phase: {self.brain.phase}")
        
        # Return timing for next beat (60 / BPM)
        return 60.0 / bpm
    
    def run(self):
        """Heart-controlled main loop"""
        print("\n[SYSTEM] Starting Heart-Controlled System...")
        print("=" * 70)
        print("  🫀 HEART is the PACEMAKER")
        print("  🧠 BRAIN follows HEART rhythm")
        print("=" * 70)
        print("\nPress Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                # One heartbeat cycle
                sleep_time = self.heartbeat_cycle()
                
                # Wait for next heartbeat (heart controls timing)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            pass
    
    def stop(self):
        """Stop gracefully"""
        print("\n\n[SYSTEM] Stopping...")
        self.running = False
        
        # Save state
        self.brain._save_state()
        
        # Final report
        print(f"\n{'='*70}")
        print("  FINAL STATUS")
        print(f"{'='*70}")
        print(f"  🫀 Heart: {self.beat_count} beats")
        print(f"  🧠 Brain: {self.brain.tick_count} ticks")
        print(f"  🧠 Memories: {self.brain.hippocampus.total_traces}")
        print(f"  🫀 State: {self.heart.get_state_summary()}")
        print(f"{'='*70}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🫀🧠 HEART-BRAIN CONTROLLER")
    print("  2026-03-31 22:30 UTC")
    print("=" * 70)
    
    controller = HeartBrainController()
    
    try:
        controller.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.stop()
