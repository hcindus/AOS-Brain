#!/usr/bin/env python3
"""
AOS COMPLETE TERNARY SYSTEM
Heart + Stomach + Intestine + Brain

Full information digestion and distribution
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import time
import threading

from superior_heart import SuperiorHeart
from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from brain_v31 import AOSBrainV31

from ternary_interfaces import (
    HeartBeatInput, BrainInput, HeartState,
    DigestionInput, IntestineInput
)


class CompleteTernarySystem:
    """Complete organism: Heart + Stomach + Intestine + Brain"""
    
    def __init__(self):
        print("=" * 70)
        print("  🫀🍽️🧠 COMPLETE TERNARY SYSTEM")
        print("  Heart + Stomach + Intestine + Brain")
        print("=" * 70)
        
        # Initialize all organs
        print("\n[Organ 1/4] Creating Superior Heart...")
        self.heart = SuperiorHeart()
        
        print("[Organ 2/4] Creating Information Stomach...")
        self.stomach = InformationStomach(capacity=50)
        
        print("[Organ 3/4] Creating Information Intestine...")
        self.intestine = InformationIntestine()
        
        print("[Organ 4/4] Creating Brain v3.1...")
        self.brain = AOSBrainV31()
        
        # Metrics
        self.cycle_count = 0
        self.running = False
        
        print("\n" + "=" * 70)
        print("  ✅ All organs initialized")
        print("  Information Flow: Ingest → Digest → Distribute → Think")
        print("=" * 70)
    
    def ingest_information(self, source: str, content: str, priority: float = 0.5):
        """Feed information into the system"""
        self.stomach.ingest(source, content, priority)
    
    def system_cycle(self):
        """One complete system cycle"""
        self.cycle_count += 1
        
        # 1. STOMACH DIGESTS
        # Create digestion input
        stomach_inputs = DigestionInput(
            input_amount=0.1,
            heart_energy_demand=0.6,
            stress_level=0.2 if self.brain.limbic.get("reward", 0.5) > 0.4 else 0.5
        )
        
        stomach_output = self.stomach.digest(stomach_inputs)
        
        # 2. INTESTINE DISTRIBUTES
        # Get digested batch from stomach
        digested_batch = self.stomach.get_digested_batch(n=5)
        
        # Create mock stomach output with batch
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
        
        # 4. BRAIN THINKS (with energy from intestine)
        brain_inputs = BrainInput(
            heart_bpm=heart_output.bpm,
            heart_state=heart_output.state,
            heart_coherence=heart_output.coherence,
            heart_arousal=heart_output.arousal,
            emotional_tone=heart_output.emotional_tone,
            observation=f"Digestion cycle: stomach={stomach_output.state.value}, "
                         f"intestine distributed energy to brain={intestine_output.nutrients_to_brain:.2f}",
            observation_type="system"
        )
        
        brain_output = self.brain.tick(brain_inputs)
        
        # Display every 10 cycles
        if self.cycle_count % 10 == 0:
            print(f"\n[Cycle {self.cycle_count:3d}] "
                  f"🍽️  {stomach_output.state.value:10s} | "
                  f"🫀 {heart_output.bpm:.0f} BPM ({heart_output.emotional_tone:10s}) | "
                  f"🧠 {brain_output.tick_count:4d} ticks | "
                  f"Memories: {brain_output.memories_total:3d}")
        
        # Heart controls timing
        return 60.0 / heart_output.bpm
    
    def run(self, duration_seconds: int = 60):
        """Run complete system"""
        print(f"\n[SYSTEM] Starting for {duration_seconds}s...")
        print("=" * 70)
        print("  Information ingested → Digested → Distributed → Learned")
        print("=" * 70)
        print("\nPress Ctrl+C to stop\n")
        
        # Feed some initial information
        print("Feeding initial information...")
        self.ingest_information("api", "System status: CPU 45%, Memory 60%", 0.7)
        self.ingest_information("log", "User logged in successfully", 0.5)
        self.ingest_information("sensor", "Temperature: 72°F, Humidity: 45%", 0.4)
        self.ingest_information("file", '{"users": 150, "active": 42}', 0.6)
        self.ingest_information("api", "API call: /status returned 200", 0.5)
        
        start = time.time()
        
        try:
            while time.time() - start < duration_seconds:
                # Feed new information periodically
                if self.cycle_count % 20 == 0:
                    sources = ["api", "log", "sensor", "file", "user"]
                    contents = [
                        "System stable",
                        "Memory usage: 65%",
                        "Network latency: 23ms",
                        "Active users: 42",
                        "Cache hit rate: 87%"
                    ]
                    import random
                    self.ingest_information(
                        random.choice(sources),
                        random.choice(contents),
                        random.uniform(0.3, 0.7)
                    )
                
                sleep_time = self.system_cycle()
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            pass
    
    def stop(self):
        """Stop system"""
        print("\n\n[SYSTEM] Stopping...")
        
        self.brain.save_state()
        
        print(f"\n{'='*70}")
        print("  FINAL STATUS")
        print(f"{'='*70}")
        print(f"  🍽️  Stomach: {self.stomach.total_digested} items digested")
        print(f"  🫀 Heart: {self.heart.rhythm.beat_count} beats")
        print(f"  🧠 Brain: {self.brain.tick_count} ticks")
        print(f"         {self.brain.hippocampus.total_traces} memories")
        print(f"{'='*70}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🫀🍽️🧠 COMPLETE TERNARY SYSTEM")
    print("  Heart + Stomach + Intestine + Brain")
    print("  2026-03-31 22:55 UTC")
    print("=" * 70)
    
    system = CompleteTernarySystem()
    
    try:
        system.run(duration_seconds=60)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        system.stop()
