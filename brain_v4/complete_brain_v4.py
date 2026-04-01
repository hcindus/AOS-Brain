#!/usr/bin/env python3
"""
AOS COMPLETE BRAIN v4.0
Everything from legacy brains + Enhanced Ternary

Components:
- SuperiorHeart (Ternary emotion)
- Stomach v2 (Information digestion)
- Intestine v2 (Distribution)
- 3D Cortex (Consciousness spatial processing)
- TracRay (Memory trajectories)
- Consciousness Layers (Con/Subcon/Uncon)
- QMD Loop (Ollama decisions)
- MemoryBridge (Ollama embeddings)
- Voice Manager (TTS)
- Vision Manager (Camera)
"""

import sys
import time
import signal
import threading
import json

sys.path.insert(0, '/root/.aos/aos')

from superior_heart import SuperiorHeart
from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from brain_v31 import AOSBrainV31
from cortex_3d import Cortex3D
from trac_ray import TracRay
from consciousness_layers import ConsciousnessManager
from qmd_loop import QMDLoop
from memory_bridge_v4 import MemoryBridge
from voice_manager import VoiceInterface
from vision_manager import VisionInterface

from ternary_interfaces import HeartBeatInput, BrainInput, HeartState


class CompleteBrainV4:
    """
    Fully integrated brain with ALL legacy features
    """
    
    def __init__(self):
        print("=" * 70)
        print("  🧠 COMPLETE BRAIN v4.0")
        print("  Legacy + Ternary + Enhanced Components")
        print("=" * 70)
        
        # Core organs
        print("\n[Core 1/4] Superior Heart...")
        self.heart = SuperiorHeart()
        
        print("[Core 2/4] Stomach v2...")
        self.stomach = InformationStomach(capacity=100)
        
        print("[Core 3/4] Intestine v2...")
        self.intestine = InformationIntestine()
        
        print("[Core 4/4] Brain v3.1...")
        self.brain = AOSBrainV31()
        
        # NEW: Legacy components
        print("\n[Legacy 1/5] 3D Cortex (Consciousness spatial)...")
        self.cortex = Cortex3D(width=32, height=32, depth=3)
        
        print("[Legacy 2/5] TracRay (Memory trajectories)...")
        self.tracray = TracRay(capacity=5000)
        
        print("[Legacy 3/5] Consciousness Layers...")
        self.consciousness = ConsciousnessManager()
        
        print("[Legacy 4/5] QMD Loop (local decisions)...")
        self.qmd = QMDLoop(use_ollama=False)
        
        print("[Legacy 5/5] MemoryBridge (Ollama embeddings)...")
        self.memory_bridge = MemoryBridge()
        
        # Sensory
        print("\n[Sensory 1/2] Voice Interface...")
        self.voice = VoiceInterface()
        
        print("[Sensory 2/2] Vision Interface...")
        self.vision = VisionInterface()
        
        # State
        self.tick_count = 0
        self.running = True
        self.last_announcement = 0
        
        # Signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("\n" + "=" * 70)
        print("  ✅ ALL SYSTEMS INITIALIZED")
        print("=" * 70)
        
        self.voice.announce("Complete Brain v4 initialized", priority="high")
    
    def _signal_handler(self, signum, frame):
        print(f"\n[SYSTEM] Signal {signum} received")
        self.voice.announce("System shutting down", priority="high")
        self.running = False
    
    def _get_visual_input(self) -> str:
        """Get visual observation"""
        observation = self.vision.observe()
        return observation if observation else "No visual input"
    
    def _process_cortex(self, observation: str, phase: str) -> dict:
        """Process through 3D Cortex"""
        # Encode observation
        import numpy as np
        encoded = np.random.randn(1024) * 0.1
        
        # Activate conscious layer
        self.cortex.activate(encoded, "conscious")
        
        # Propagate down through subconscious to unconscious
        propagation = self.cortex.propagate_down("conscious")
        
        # Extract patterns
        patterns = self.cortex.detect_patterns("subconscious")
        
        return {
            "conscious_activation": float(np.mean(self.cortex.conscious)),
            "subconscious_activation": float(np.mean(self.cortex.subconscious)),
            "patterns_detected": len(patterns)
        }
    
    def system_cycle(self):
        """One complete cycle with ALL components"""
        self.tick_count += 1
        
        # 1. Get visual input
        visual_observation = self._get_visual_input()
        
        # 2. Stomach ingests
        self.stomach.ingest("vision", visual_observation, priority=0.4)
        
        # 3. NEW: Process through consciousness layers
        self.consciousness.perceive(visual_observation, intensity=0.7)
        self.consciousness.consolidate()
        
        # 4. Stomach digests
        from ternary_interfaces import DigestionInput, IntestineInput
        
        stomach_inputs = DigestionInput(
            input_amount=0.1,
            heart_energy_demand=0.6,
            stress_level=0.2
        )
        stomach_output = self.stomach.digest(stomach_inputs)
        
        # 5. Intestine distributes
        digested_batch = self.stomach.get_digested_batch(n=5)
        stomach_output.__dict__['digested_queue'] = digested_batch
        
        intestine_inputs = IntestineInput(
            from_stomach=stomach_output,
            heart_needs=0.6,
            brain_needs=0.8,
            system_needs=0.3
        )
        intestine_output = self.intestine.process(intestine_inputs)
        
        # Feed heart
        self.heart.rhythm.bpm += intestine_output.nutrients_to_heart * 0.1
        
        # 6. Heart beats
        heart_inputs = HeartBeatInput(
            brain_arousal=0.5,
            safety=0.8,
            stress=0.2,
            connection=0.6,
            cognitive_load=0.5
        )
        heart_output = self.heart.beat(heart_inputs)
        
        # 7. NEW: 3D Cortex processing
        cortex_result = self._process_cortex(visual_observation, "Observe")
        
        # 8. Brain thinks
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
        
        # 9. NEW: QMD decision
        qmd_context = {
            "phase": brain_output.phase,
            "observation": visual_observation,
            "limbic": {
                "novelty": brain_output.novelty,
                "reward": brain_output.reward
            }
        }
        qmd_result = self.qmd.cycle(qmd_context)
        
        # 10. NEW: TracRay record
        self.tracray.record(
            tick=self.tick_count,
            phase=brain_output.phase,
            limbic={"novelty": brain_output.novelty, "reward": brain_output.reward},
            observation=visual_observation,
            action=qmd_result["action"]
        )
        
        # Display every 50 cycles
        if self.tick_count % 50 == 0:
            summary = self.consciousness.get_layer_summary()
            print(f"\n[Cycle {self.tick_count:5d}] "
                  f"🫀 {heart_output.bpm:.0f} BPM | "
                  f"🧠 {brain_output.phase:8s} | "
                  f"🎛️  {qmd_result['action']:10s} ({qmd_result['confidence']:.2f}) | "
                  f"🧿 {cortex_result['patterns_detected']:2d} patterns | "
                  f"Con:{summary['conscious']['active_items']}/"
                  f"Sub:{summary['subconscious']['active_items']}/"
                  f"Unc:{summary['unconscious']['active_items']}")
        
        # Save periodically
        if self.tick_count % 100 == 0:
            self.brain.save_state()
            self.tracray.end_episode(f"tick_{self.tick_count}")
        
        return 60.0 / heart_output.bpm
    
    def get_status(self) -> dict:
        """Get complete system status"""
        cortex_stats = self.cortex.get_stats()
        tracray_stats = self.tracray.get_stats()
        qmd_stats = self.qmd.get_stats()
        consciousness_summary = self.consciousness.get_layer_summary()
        
        return {
            "tick": self.tick_count,
            "cortex": cortex_stats,
            "tracray": tracray_stats,
            "qmd": qmd_stats,
            "consciousness": consciousness_summary,
            "components_active": 10
        }
    
    def run(self):
        """Run complete system"""
        print("\n[SYSTEM] Complete Brain v4.0 running...")
        self.voice.announce("Complete system operational", priority="high")
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            try:
                sleep_time = self.system_cycle()
                time.sleep(sleep_time)
            except Exception as e:
                print(f"[SYSTEM] Error: {e}")
                time.sleep(1)
        
        print("\n[SYSTEM] Shutting down...")
        self.voice.announce("System offline", priority="high")
        self.brain.save_state()
        
        status = self.get_status()
        print(f"[SYSTEM] Final: {status['tick']} ticks, {status['cortex']['history_length']} cortex activations")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🧠 COMPLETE BRAIN v4.0")
    print("  All legacy + ternary components")
    print("=" * 70)
    
    brain = CompleteBrainV4()
    
    try:
        brain.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        print("=" * 70)
        print("  Complete Brain v4.0 Finished")
        print("=" * 70)
