#!/usr/bin/env python3
"""
AOS Ternary Daemon - Persistent Complete System
Runs continuously as background service
"""

import sys
import time
import signal
from pathlib import Path

sys.path.insert(0, '/root/.aos/aos')

from superior_heart import SuperiorHeart
from stomach_v2 import InformationStomach
from intestine_v2 import InformationIntestine
from brain_v31 import AOSBrainV31

from ternary_interfaces import HeartBeatInput, BrainInput, DigestionInput, IntestineInput


class TernaryDaemon:
    """Persistent Ternary System Daemon"""
    
    def __init__(self):
        self.running = False
        self.cycle_count = 0
        
        # Initialize organs
        print("[Daemon] Initializing Complete Ternary System...")
        self.heart = SuperiorHeart()
        self.stomach = InformationStomach(capacity=100)
        self.intestine = InformationIntestine()
        self.brain = AOSBrainV31()
        
        # Signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("[Daemon] All organs initialized")
        
        # Load state if exists
        self._load_state()
    
    def _load_state(self):
        """Load previous state"""
        state_file = Path.home() / ".aos" / "ternary_state.json"
        try:
            if state_file.exists():
                import json
                with open(state_file) as f:
                    data = json.load(f)
                    self.cycle_count = data.get("cycles", 0)
                    print(f"[Daemon] Resumed from cycle {self.cycle_count}")
        except:
            pass
    
    def _save_state(self):
        """Save current state"""
        state_file = Path.home() / ".aos" / "ternary_state.json"
        try:
            import json
            with open(state_file, 'w') as f:
                json.dump({
                    "cycles": self.cycle_count,
                    "heart_beats": self.heart.rhythm.beat_count,
                    "brain_ticks": self.brain.tick_count,
                    "memories": self.brain.hippocampus.total_traces,
                    "stomach_digested": self.stomach.total_digested,
                    "timestamp": time.time()
                }, f)
        except:
            pass
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n[Daemon] Received signal {signum}, shutting down...")
        self.running = False
    
    def ingest_information(self, source: str, content: str, priority: float = 0.5):
        """Feed information into stomach"""
        self.stomach.ingest(source, content, priority)
    
    def cycle(self):
        """One complete system cycle"""
        self.cycle_count += 1
        
        # 1. STOMACH DIGESTS
        stomach_output = self.stomach.digest()
        
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
        self.heart.rhythm.bpm += intestine_output.nutrients_to_heart * 0.05
        self.heart.rhythm.bpm = max(60, min(100, self.heart.rhythm.bpm))
        
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
            observation=f"Cycle {self.cycle_count}: digestion={stomach_output.state.value}, heart={heart_output.bpm:.0f}BPM",
            observation_type="system"
        )
        brain_output = self.brain.tick(brain_inputs)
        
        # Log every 50 cycles
        if self.cycle_count % 50 == 0:
            print(f"[Cycle {self.cycle_count:5d}] 🍽️ {stomach_output.state.value:10s} | "
                  f"🫀 {heart_output.bpm:.0f} BPM ({heart_output.emotional_tone:10s}) | "
                  f"🧠 {brain_output.tick_count:5d} ticks | Memories: {brain_output.memories_total:4d}")
        
        # Save state every 100 cycles
        if self.cycle_count % 100 == 0:
            self._save_state()
        
        return 60.0 / heart_output.bpm
    
    def run(self):
        """Main daemon loop"""
        print("[Daemon] Starting Ternary System...")
        print("[Daemon] Press Ctrl+C to stop")
        
        self.running = True
        
        # Feed initial information
        self.ingest_information("system", "Ternary daemon started", 0.9)
        self.ingest_information("config", "Heart-B-Stomach-Intestine-Brain connected", 0.8)
        
        # Information sources
        info_sources = [
            ("api", "API call received", 0.6),
            ("log", "System stable", 0.4),
            ("sensor", "Temperature normal", 0.3),
            ("user", "User interaction", 0.7),
            ("file", "Data processed", 0.5),
        ]
        info_idx = 0
        
        try:
            while self.running:
                # Feed information periodically
                if self.cycle_count % 30 == 0:
                    source, content, priority = info_sources[info_idx % len(info_sources)]
                    self.ingest_information(source, content, priority)
                    info_idx += 1
                
                # Run cycle
                sleep_time = self.cycle()
                time.sleep(sleep_time)
                
        except Exception as e:
            print(f"[Daemon] Error: {e}")
        finally:
            self._shutdown()
    
    def _shutdown(self):
        """Graceful shutdown"""
        print("\n[Daemon] Shutting down...")
        self._save_state()
        self.brain.save_state()
        
        status = self._get_status()
        print(f"\n[Daemon] Final Status:")
        print(f"  Cycles: {status['cycles']}")
        print(f"  Heart: {status['heart_beats']} beats")
        print(f"  Brain: {status['brain_ticks']} ticks")
        print(f"  Memories: {status['memories']}")
        print(f"  Digested: {status['digested']} items")
        print("[Daemon] Stopped")
    
    def _get_status(self) -> dict:
        """Get system status"""
        return {
            "cycles": self.cycle_count,
            "heart_beats": self.heart.rhythm.beat_count,
            "brain_ticks": self.brain.tick_count,
            "memories": self.brain.hippocampus.total_traces,
            "digested": self.stomach.total_digested
        }


if __name__ == "__main__":
    print("=" * 70)
    print("  🫀🍽️🧠 TERNARY DAEMON")
    print("  Persistent Complete System")
    print("=" * 70)
    
    daemon = TernaryDaemon()
    daemon.run()
