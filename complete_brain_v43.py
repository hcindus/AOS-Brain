#!/usr/bin/env python3
"""
AOS COMPLETE BRAIN v4.3
Legacy + Ternary + Socket Interface + THYROID v1.2 (Endocrine) + Model Router

Components:
- SuperiorHeart (Ternary emotion)
- Stomach v2 (Information digestion)
- Intestine v2 (Distribution)
- 3D Cortex (Consciousness spatial processing)
- TracRay (Memory trajectories)
- Consciousness Layers (Con/Subcon/Uncon)
- QMD Loop (Ollama decisions via Model Router)
- MemoryBridge (Ollama embeddings)
- Voice Manager (TTS via Model Router)
- Vision Manager (Camera)
- Socket Server (Diagnostic interface)
- THYROID v1.2 (Endocrine-style regulation)
- Model Router (tinyllama for decisions, Mort_II for voice)

NEW in v4.3:
- Thyroid v1.2: Endocrine regulation (baseline → stimulate → auto-return)
- No "cough" - smooth hormonal decay back to baseline
- Stimulation-based (not promotion-based)
- Natural resource regulation like biological thyroid
"""

import sys
import time
import signal
import threading
import json
import socket
import os

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
from thyroid_v12 import AOSThyroidV12, ThyroidState
from model_router import AOSModelRouter

from ternary_interfaces import HeartBeatInput, BrainInput, HeartState


class BrainSocketServer:
    """Unix socket server for diagnostic interface"""
    
    def __init__(self, brain, socket_path='/tmp/aos_brain.sock'):
        self.brain = brain
        self.socket_path = socket_path
        self.running = False
        self.server_thread = None
        
        if os.path.exists(socket_path):
            try:
                os.remove(socket_path)
            except:
                pass
    
    def start(self):
        """Start the socket server in a thread"""
        self.running = True
        self.server_thread = threading.Thread(target=self._serve, daemon=True)
        self.server_thread.start()
        print(f"[Socket Server] Started on {self.socket_path}")
    
    def stop(self):
        """Stop the socket server"""
        self.running = False
        if os.path.exists(self.socket_path):
            try:
                os.remove(self.socket_path)
            except:
                pass
    
    def _serve(self):
        """Serve socket requests"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(self.socket_path)
            sock.listen(5)
            sock.settimeout(1.0)
            
            while self.running:
                try:
                    conn, addr = sock.accept()
                    self._handle_connection(conn)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"[Socket Server] Error: {e}")
        except Exception as e:
            print(f"[Socket Server] Fatal error: {e}")
        finally:
            sock.close()
    
    def _handle_connection(self, conn):
        """Handle a single connection"""
        try:
            conn.settimeout(5.0)
            
            data = b''
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b'\n' in data:
                    break
            
            if not data:
                return
            
            request = json.loads(data.decode().strip())
            cmd = request.get('cmd')
            response = self._execute_command(cmd, request.get('params', {}))
            conn.sendall(json.dumps(response).encode())
            
        except Exception as e:
            try:
                conn.sendall(json.dumps({'error': str(e)}).encode())
            except:
                pass
        finally:
            conn.close()
    
    def _execute_command(self, cmd: str, params: dict) -> dict:
        """Execute a brain command"""
        if cmd == 'status':
            status = self.brain.get_status()
            status['thyroid'] = self.brain.thyroid.get_status() if self.brain.thyroid else None
            return status
        elif cmd == 'ping':
            return {'pong': True, 'tick': self.brain.tick_count}
        elif cmd == 'pause':
            self.brain.paused = True
            return {'success': True, 'state': 'paused'}
        elif cmd == 'resume':
            self.brain.paused = False
            return {'success': True, 'state': 'resumed'}
        elif cmd == 'get_phase':
            return {'phase': self.brain.current_phase}
        elif cmd == 'get_heart':
            if hasattr(self.brain, 'heart') and self.brain.heart:
                return {
                    'bpm': self.brain.heart.rhythm.bpm,
                    'state': str(self.brain.heart.rhythm.state)
                }
            return {'error': 'Heart not available'}
        elif cmd == 'thyroid':
            if self.brain.thyroid:
                return self.brain.thyroid.get_status()
            return {'error': 'Thyroid not available'}
        elif cmd == 'router':
            if self.brain.router:
                return {
                    'models': self.brain.router.MODELS,
                    'stats': self.brain.router.get_stats()
                }
            return {'error': 'Router not available'}
        elif cmd == 'decide':
            # Direct decision via router
            context = params.get('context', {})
            if self.brain.router:
                action, confidence = self.brain.router.decide(context)
                return {'action': action, 'confidence': confidence}
            return {'error': 'Router not available'}
        elif cmd == 'speak':
            # Direct voice via router
            message = params.get('message', '')
            context = params.get('context', {})
            if self.brain.router:
                response = self.brain.router.speak(message, context)
                return {'response': response}
            return {'error': 'Router not available'}
        elif cmd == 'stimulate':
            # Stimulate thyroid (v1.2 style)
            importance = params.get('importance', 0.8)
            if self.brain.thyroid:
                stimulated = self.brain.thyroid.stimulate(importance=importance)
                return {'stimulated': stimulated, 'state': self.brain.thyroid.state.name}
            return {'error': 'Thyroid not available'}
        else:
            return {'error': f'Unknown command: {cmd}'}


class CompleteBrainV43:
    """
    Fully integrated brain with ALL features + Thyroid v1.2 + Model Router
    """
    
    def __init__(self, test_mode=False):
        print("=" * 70)
        print("  🧠 COMPLETE BRAIN v4.3")
        print("  Legacy + Ternary + Socket + THYROID v1.2 (Endocrine) + Model Router")
        print("=" * 70)
        
        self.test_mode = test_mode
        
        # Core organs
        print("\n[Core 1/4] Superior Heart...")
        self.heart = SuperiorHeart()
        
        print("[Core 2/4] Stomach v2...")
        self.stomach = InformationStomach(capacity=100)
        
        print("[Core 3/4] Intestine v2...")
        self.intestine = InformationIntestine()
        
        print("[Core 4/4] Brain v3.1...")
        self.brain = AOSBrainV31()
        
        # Legacy components
        print("\n[Legacy 1/5] 3D Cortex...")
        self.cortex = Cortex3D(width=32, height=32, depth=3)
        
        print("[Legacy 2/5] TracRay...")
        self.tracray = TracRay(capacity=5000)
        
        print("[Legacy 3/5] Consciousness Layers...")
        self.consciousness = ConsciousnessManager()
        
        print("[Legacy 4/5] QMD Loop (tinyllama-ready)...")
        self.qmd = QMDLoop(use_ollama=False)  # Thyroid will manage
        
        print("[Legacy 5/5] MemoryBridge...")
        self.memory_bridge = MemoryBridge()
        
        # Model Router
        print("\n[NEW v4.2] Model Router...")
        self.router = AOSModelRouter()
        
        # NEW: Thyroid v1.2 (endocrine style)
        print("[NEW v4.3] Thyroid v1.2 (endocrine regulation)...")
        self.thyroid = AOSThyroidV12(
            qmd_loop=self.qmd,
            baseline_timeout=120.0,  # Return to baseline after 2 min
            secretion_duration=30.0  # Minimum 30s secretion
        )
        
        # Sensory
        print("\n[Sensory 1/2] Voice Interface...")
        self.voice = VoiceInterface()
        
        print("[Sensory 2/2] Vision Interface...")
        self.vision = VisionInterface()
        
        # Socket server
        print("\n[Interface] Socket Server...")
        self.socket_server = BrainSocketServer(self)
        
        # State
        self.tick_count = 0
        self.running = True
        self.paused = False
        self.current_phase = "Initialize"
        
        # Signals
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("\n" + "=" * 70)
        print("  ✅ ALL SYSTEMS INITIALIZED")
        print("=" * 70)
        
        # Announce via router (uses Mort_II)
        announcement = self.router.speak(
            "Complete Brain v4.3 initialized with Thyroid v1.2 endocrine regulation",
            {"situation": "startup"}
        )
        print(f"\n[Voice] {announcement[:60]}...")
    
    def _signal_handler(self, signum, frame):
        print(f"\n[SYSTEM] Signal {signum} received")
        self.running = False
    
    def _get_visual_input(self) -> str:
        """Get visual observation"""
        observation = self.vision.observe()
        return observation if observation else "No visual input"
    
    def _process_cortex(self, observation: str, phase: str) -> dict:
        """Process through 3D Cortex"""
        import numpy as np
        encoded = np.random.randn(1024) * 0.1
        self.cortex.activate(encoded, "conscious")
        self.cortex.propagate_down("conscious")
        patterns = self.cortex.detect_patterns("subconscious")
        
        return {
            "conscious_activation": float(np.mean(self.cortex.conscious)),
            "subconscious_activation": float(np.mean(self.cortex.subconscious)),
            "patterns_detected": len(patterns)
        }
    
    def system_cycle(self):
        """One complete cycle"""
        if self.paused:
            time.sleep(0.1)
            return 0.1
        
        self.tick_count += 1
        
        # 1. Visual input
        visual_observation = self._get_visual_input()
        
        # 2. Stomach ingestion
        self.stomach.ingest("vision", visual_observation, priority=0.4)
        
        # 3. Consciousness processing
        self.consciousness.perceive(visual_observation, intensity=0.7)
        self.consciousness.consolidate()
        
        # 4. Stomach digestion
        from ternary_interfaces import DigestionInput, IntestineInput
        
        stomach_inputs = DigestionInput(
            input_amount=0.1,
            heart_energy_demand=0.6,
            stress_level=0.2
        )
        stomach_output = self.stomach.digest(stomach_inputs)
        
        # 5. Intestine distribution
        digested_batch = self.stomach.get_digested_batch(n=5)
        stomach_output.__dict__['digested_queue'] = digested_batch
        
        intestine_inputs = IntestineInput(
            from_stomach=stomach_output,
            heart_needs=0.6,
            brain_needs=0.8,
            system_needs=0.3
        )
        intestine_output = self.intestine.process(intestine_inputs)
        self.heart.rhythm.bpm += intestine_output.nutrients_to_heart * 0.1
        
        # 6. Heart beat
        heart_inputs = HeartBeatInput(
            brain_arousal=0.5,
            safety=0.8,
            stress=0.2,
            connection=0.6,
            cognitive_load=0.5
        )
        heart_output = self.heart.beat(heart_inputs)
        
        # 7. Cortex processing
        cortex_result = self._process_cortex(visual_observation, "Observe")
        
        # 8. Brain tick
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
        self.current_phase = brain_output.phase
        
        # 9. QMD decision (via Router when secreting)
        qmd_context = {
            "phase": brain_output.phase,
            "observation": visual_observation,
            "limbic": {
                "novelty": brain_output.novelty,
                "reward": brain_output.reward
            }
        }
        
        # Check thyroid state - use Router when SECRETING (OLLAMA mode)
        if self.thyroid.state == ThyroidState.SECRETING:
            try:
                action, confidence = self.router.decide(qmd_context)
                qmd_result = {
                    "action": action.lower(),
                    "confidence": confidence,
                    "reasoning": "model_router",
                    "model": self.router.MODELS['decision']
                }
            except Exception as e:
                # Router failed, use QMD local fallback
                qmd_result = self.qmd.cycle(qmd_context, memory_bridge=self.memory_bridge)
        else:
            # BASELINE mode - use QMD directly (LOCAL)
            qmd_result = self.qmd.cycle(qmd_context, memory_bridge=self.memory_bridge)
        
        # 10. TracRay record
        self.tracray.record(
            tick=self.tick_count,
            phase=brain_output.phase,
            limbic={"novelty": brain_output.novelty, "reward": brain_output.reward},
            observation=visual_observation,
            action=qmd_result.get("action", "unknown")
        )
        
        # Display status
        if self.tick_count % 50 == 0:
            summary = self.consciousness.get_layer_summary()
            thyroid_state = self.thyroid.state.name
            hormone_level = self.thyroid.hormone.ollama_level
            router_model = self.router.MODELS['decision'] if thyroid_state == "SECRETING" else "local"
            
            print(f"\n[Cycle {self.tick_count:5d}] "
                  f"🫀 {heart_output.bpm:.0f} BPM | "
                  f"🧠 {brain_output.phase:8s} | "
                  f"🎛️  {qmd_result.get('action', 'unknown'):10s} ({qmd_result.get('confidence', 0):.2f}) | "
                  f"🫁 {thyroid_state:10s} ({hormone_level:.1f}) | "
                  f"Con:{summary['conscious']['active_items']}/"
                  f"Sub:{summary['subconscious']['active_items']}")
        
        # Save periodically
        if self.tick_count % 100 == 0:
            self.brain.save_state()
            self.tracray.end_episode(f"tick_{self.tick_count}")
        
        return 60.0 / heart_output.bpm
    
    def get_status(self) -> dict:
        """Get complete system status"""
        thyroid_status = self.thyroid.get_status() if self.thyroid else None
        
        return {
            "version": "4.3",
            "tick": self.tick_count,
            "phase": self.current_phase,
            "cortex": self.cortex.get_stats(),
            "tracray": self.tracray.get_stats(),
            "qmd": self.qmd.get_stats(),
            "consciousness": self.consciousness.get_layer_summary(),
            "thyroid": thyroid_status,
            "router": {
                "models": self.router.MODELS if self.router else None,
                "stats": self.router.get_stats() if self.router else None
            },
            "components_active": 12
        }
    
    def run(self):
        """Run complete system"""
        print("\n[SYSTEM] Complete Brain v4.3 running...")
        
        # Start thyroid monitor (endocrine regulation)
        self.thyroid.start()
        
        # Start socket server
        self.socket_server.start()
        
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            try:
                sleep_time = self.system_cycle()
                time.sleep(sleep_time)
            except Exception as e:
                print(f"[SYSTEM] Error: {e}")
                time.sleep(1)
        
        print("\n[SYSTEM] Shutting down...")
        self.socket_server.stop()
        self.thyroid.stop()
        self.brain.save_state()
        
        status = self.get_status()
        print(f"[SYSTEM] Final: {status['tick']} ticks")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🧠 COMPLETE BRAIN v4.3")
    print("  Thyroid v1.2 (Endocrine) + Model Router + tinyllama/Mort_II")
    print("=" * 70)
    
    brain = CompleteBrainV43()
    
    try:
        brain.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("=" * 70)
        print("  Complete Brain v4.3 Finished")
        print("=" * 70)
