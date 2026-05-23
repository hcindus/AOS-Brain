#!/usr/bin/env python3
"""
AOS ENHANCED TERNARY SYSTEM
Heart + Stomach + Intestine + Brain + Voice + Vision + STT

SUPERIOR PRODUCT - All features from previous brains integrated
"""

import sys
import time
import signal
import threading

sys.path.insert(0, '/root/.aos/aos')

from superior_heart import SuperiorHeart
from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from brain_v31 import AOSBrainV31
from voice_manager import VoiceInterface
from vision_manager import VisionInterface

from ternary_interfaces import (
    HeartBeatInput, BrainInput, HeartState,
    DigestionInput, IntestineInput
)


class EnhancedTernarySystem:
    """Complete organism with ALL features from previous brains"""
    
    def __init__(self):
        print("=" * 70)
        print("  🫀🍽️🧠🎙️👁️ ENHANCED TERNARY SYSTEM")
        print("  Heart + Stomach + Intestine + Brain + Voice + Vision")
        print("=" * 70)
        print("  SUPERIOR PRODUCT - All legacy features integrated")
        print("=" * 70)
        
        # Core organs
        print("\n[Core 1/4] Superior Heart...")
        self.heart = SuperiorHeart()
        
        print("[Core 2/4] Information Stomach...")
        self.stomach = InformationStomach(capacity=100)
        
        print("[Core 3/4] Information Intestine...")
        self.intestine = InformationIntestine()
        
        print("[Core 4/4] Brain v3.1...")
        self.brain = AOSBrainV31()
        
        # Sensory/Motor (ported from legacy)
        print("\n[Sensory 1/2] Voice Interface (ElevenLabs)...")
        self.voice = VoiceInterface()
        
        print("[Sensory 2/2] Vision Interface (Camera)...")
        self.vision = VisionInterface()
        
        # State
        self.cycle_count = 0
        self.running = True
        
        # Announcements
        self.last_announcement = 0
        
        # Signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("\n" + "=" * 70)
        print("  ✅ All systems initialized")
        print("=" * 70)
        
        # Initial announcement
        self.voice.announce("Enhanced Ternary System initialized", priority="high")
    
    def _signal_handler(self, signum, frame):
        print(f"\n[SYSTEM] Signal {signum} received, shutting down...")
        self.voice.announce("System shutting down", priority="high")
        self.running = False
    
    def _get_visual_input(self) -> str:
        """Get visual observation"""
        observation = self.vision.observe()
        return observation if observation else "No visual input"
    
    def _announce_status(self, cycle: int, heart_bpm: float, 
                         heart_emotion: str, memories: int):
        """Announce status via voice"""
        # Only announce every 500 cycles
        if cycle - self.last_announcement < 500:
            return
        
        self.last_announcement = cycle
        
        message = f"System status: {heart_bpm:.0f} beats per minute, {memories} memories formed"
        self.voice.announce(message, priority="normal")
    
    def system_cycle(self):
        """One complete enhanced cycle"""
        self.cycle_count += 1
        
        # 1. Get visual input
        visual_observation = self._get_visual_input()
        self.stomach.ingest("vision", visual_observation, priority=0.4)
        
        # 2. STOMACH DIGESTS (information + visual)
        stomach_inputs = DigestionInput(
            input_amount=0.1,
            heart_energy_demand=0.6,
            stress_level=0.2 if self.brain.limbic.get("reward", 0.5) > 0.4 else 0.5
        )
        stomach_output = self.stomach.digest(stomach_inputs)
        
        # 3. INTESTINE DISTRIBUTES
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
        
        # 4. HEART BEATS
        heart_inputs = HeartBeatInput(
            brain_arousal=self.brain.limbic.get("arousal", 0.5),
            safety=0.8,
            stress=0.2,
            connection=0.6,
            cognitive_load=0.5
        )
        heart_output = self.heart.beat(heart_inputs)
        
        # 5. BRAIN THINKS (with voice and vision)
        brain_inputs = BrainInput(
            heart_bpm=heart_output.bpm,
            heart_state=heart_output.state,
            heart_coherence=heart_output.coherence,
            heart_arousal=heart_output.arousal,
            emotional_tone=heart_output.emotional_tone,
            observation=visual_observation,
            observation_type="multimodal"
        )
        brain_output = self.brain.tick(brain_inputs)
        
        # 6. Voice announcement (periodic)
        self._announce_status(
            self.cycle_count,
            heart_output.bpm,
            heart_output.emotional_tone,
            brain_output.memories_total
        )
        
        # Display every 100 cycles
        if self.cycle_count % 100 == 0:
            print(f"\n[Cycle {self.cycle_count:5d}] "
                  f"🍽️ {stomach_output.state.value:10s} | "
                  f"🫀 {heart_output.bpm:.0f} BPM ({heart_output.emotional_tone:10s}) | "
                  f"🧠 {brain_output.tick_count:5d} ticks | "
                  f"👁️  {visual_observation[:30]}...")
        
        # Save periodically
        if self.cycle_count % 500 == 0:
            self.brain.save_state()
        
        return 60.0 / heart_output.bpm
    
    def run(self):
        """Run enhanced system continuously"""
        print("\n[SYSTEM] Enhanced Ternary System starting...")
        self.voice.announce("Enhanced system operational", priority="high")
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            try:
                sleep_time = self.system_cycle()
                time.sleep(sleep_time)
            except Exception as e:
                print(f"[SYSTEM] Error: {e}")
                time.sleep(1)
        
        # Cleanup
        print("\n[SYSTEM] Shutting down...")
        self.voice.announce("System offline", priority="high")
        self.brain.save_state()
        print(f"[SYSTEM] Final: {self.brain.tick_count} ticks, {self.brain.hippocampus.total_traces} memories")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🫀🍽️🧠🎙️👁️ ENHANCED TERNARY SYSTEM")
    print("  Complete feature set from legacy brains")
    print("  2026-03-31 23:30 UTC")
    print("=" * 70)
    
    system = EnhancedTernarySystem()
    
    try:
        system.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        print("=" * 70)
        print("  Enhanced Ternary System Complete")
        print("=" * 70)
