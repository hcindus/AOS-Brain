#!/usr/bin/env python3
"""
AOS TERNARY SYSTEM - PERSISTENT SERVICE
Runs continuously as systemd service
"""

import sys
import time
import signal

sys.path.insert(0, '/root/.aos/aos')

from superior_heart import SuperiorHeart
from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from brain_v31 import AOSBrainV31

from ternary_interfaces import (
    HeartBeatInput, BrainInput, HeartState,
    DigestionInput, IntestineInput
)


class PersistentTernarySystem:
    """Continuous running ternary system"""
    
    def __init__(self):
        print("[TernarySystem] Initializing...")
        
        self.heart = SuperiorHeart()
        self.stomach = InformationStomach(capacity=100)
        self.intestine = InformationIntestine()
        self.brain = AOSBrainV31()
        
        self.cycle_count = 0
        self.running = True
        
        # Signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("[TernarySystem] All organs ready")
    
    def _signal_handler(self, signum, frame):
        print(f"\n[TernarySystem] Received signal {signum}, shutting down...")
        self.running = False
    
    def _feed_system(self):
        """Feed information periodically"""
        import random
        sources = ["api", "log", "sensor", "file", "user", "system"]
        contents = [
            "System status: CPU 45%, Memory 60%",
            "User activity detected",
            "Network latency: 23ms",
            "Cache hit rate: 87%",
            "Heartbeat received",
            "Memory allocation: stable",
            "Process cycle complete",
            "Information ingested"
        ]
        
        self.stomach.ingest(
            random.choice(sources),
            random.choice(contents),
            random.uniform(0.3, 0.7)
        )
    
    def system_cycle(self):
        """One complete cycle"""
        self.cycle_count += 1
        
        # Feed information periodically
        if self.cycle_count % 50 == 0:
            self._feed_system()
        
        # 1. STOMACH DIGESTS
        stomach_inputs = DigestionInput(
            input_amount=0.1,
            heart_energy_demand=0.6,
            stress_level=0.2 if self.brain.limbic.get("reward", 0.5) > 0.4 else 0.5
        )
        stomach_output = self.stomach.digest(stomach_inputs)
        
        # 2. INTESTINE DISTRIBUTES
        digested_batch = self.stomach.get_digested_batch(n=5)
        stomach_output.__dict__['digested_queue'] = digested_batch
        
        intestine_inputs = IntestineInput(
            from_stomach=stomach_output,
            heart_needs=0.6,
            brain_needs=0.8,
            system_needs=0.3
        )
        intestine_output = self.intestine.process(intestine_inputs)
        
        # Feed energy to heart
        self.heart.rhythm.bpm += intestine_output.nutrients_to_heart * 0.1
        
        # 3. HEART BEATS
        heart_inputs = HeartBeatInput(
            brain_arousal=self.brain.limbic.get("arousal", 0.5),
            safety=0.8,
            stress=0.2,
            connection=0.6,
            cognitive_load=0.5
        )
        heart_output = self.heart.beat(heart_inputs)
        
        # 4. BRAIN THINKS
        brain_inputs = BrainInput(
            heart_bpm=heart_output.bpm,
            heart_state=heart_output.state,
            heart_coherence=heart_output.coherence,
            heart_arousal=heart_output.arousal,
            emotional_tone=heart_output.emotional_tone,
            observation=f"Cycle {self.cycle_count}: digestion={stomach_output.state.value}",
            observation_type="system"
        )
        brain_output = self.brain.tick(brain_inputs)
        
        # Log every 100 cycles
        if self.cycle_count % 100 == 0:
            print(f"[Cycle {self.cycle_count:5d}] 🍽️ {stomach_output.state.value:10s} | "
                  f"🫀 {heart_output.bpm:.0f} BPM ({heart_output.emotional_tone:10s}) | "
                  f"🧠 {brain_output.tick_count:5d} ticks | "
                  f"Memories: {brain_output.memories_total:4d}")
        
        # Save state periodically
        if self.cycle_count % 500 == 0:
            self.brain.save_state()
        
        return 60.0 / heart_output.bpm
    
    def run(self):
        """Run continuously"""
        print("[TernarySystem] Starting continuous operation...")
        print("[TernarySystem] Press Ctrl+C or send SIGTERM to stop")
        
        while self.running:
            try:
                sleep_time = self.system_cycle()
                time.sleep(sleep_time)
            except Exception as e:
                print(f"[TernarySystem] Error: {e}")
                time.sleep(1)
        
        # Cleanup
        print("\n[TernarySystem] Shutting down...")
        self.brain.save_state()
        print(f"[TernarySystem] Final: {self.brain.tick_count} ticks, {self.brain.hippocampus.total_traces} memories")


if __name__ == "__main__":
    system = PersistentTernarySystem()
    system.run()
