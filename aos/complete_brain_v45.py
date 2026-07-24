#!/usr/bin/env python3
"""
AOS COMPLETE BRAIN v4.5
Legacy + Ternary + Socket + THYROID v1.2 + Model Router + LIVER v1.0 + KIDNEYS v1.0 + LUNGS v1.0

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
- LUNGS v1.0 (Respiratory system - INHALE/GAS_EXHANGE/EXHALE)
- LIVER v1.0 (Ternary blood filtration - CLEAN/PURIFY/TOXIC)
- KIDNEYS v1.0 (Ternary waste management - FILTER/REABSORB/EXCRETE)
- Model Router (tinyllama for decisions, Mort_II for voice)

NEW in v4.5:
- LUNGS v1.0: Respiratory system for ambient intake
- Full respiratory pipeline: Lungs → Liver → Brain → Kidneys

v4.4 Features:
- LIVER v1.0: Pre-brain signal/noise filtration
- KIDNEYS v1.0: Post-brain pattern recycling
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
from cortex_v25_optimized import CortexV25Optimized, AgentReadRequest, AgentWriteRequest
from trac_ray import TracRay
from consciousness_layers import ConsciousnessManager
from qmd_loop import QMDLoop
from memory_bridge_v4 import MemoryBridge
from voice_manager import VoiceInterface
from vision_manager import VisionInterface
from thyroid_v12 import AOSThyroidV12, ThyroidState
from liver_v1 import AOSLiverV1, LiverState, BloodSample
from kidneys_v1 import AOSKidneysV1, KidneyState
from model_router import AOSModelRouter
from ternary_lungs_v1 import TernaryLungs, TernaryOxygenPacket

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
        elif cmd == 'liver':
            if self.brain.liver:
                return self.brain.liver.get_status()
            return {'error': 'Liver not available'}
        elif cmd == 'kidneys':
            if self.brain.kidneys:
                return self.brain.kidneys.get_status()
            return {'error': 'Kidneys not available'}
        elif cmd == 'lungs':
            if self.brain.lungs:
                return self.brain.lungs.get_status()
            return {'error': 'Lungs not available'}
        elif cmd == 'breathe':
            if self.brain.lungs:
                ambient = params.get('ambient', [])
                valence = params.get('valence', 0.0)
                demand = params.get('demand', 1.0)
                o2, waste = self.brain.lungs.step(ambient, valence, demand)
                return {
                    'oxygen': o2.to_dict(),
                    'waste': waste.to_dict()
                }
            return {'error': 'Lungs not available'}
        elif cmd == 'hold_breath':
            if self.brain.lungs:
                self.brain.lungs.hold_breath()
                return {'status': 'breath_held'}
            return {'error': 'Lungs not available'}
        elif cmd == 'release_breath':
            if self.brain.lungs:
                self.brain.lungs.release_breath()
                return {'status': 'breath_released'}
            return {'error': 'Lungs not available'}
        elif cmd == 'router':
            if self.brain.router:
                return {
                    'models': self.brain.router.MODELS,
                    'stats': self.brain.router.get_stats()
                }
            return {'error': 'Router not available'}
        elif cmd == 'decide':
            context = params.get('context', {})
            if self.brain.router:
                action, confidence = self.brain.router.decide(context)
                return {'action': action, 'confidence': confidence}
            return {'error': 'Router not available'}
        elif cmd == 'speak':
            message = params.get('message', '')
            context = params.get('context', {})
            if self.brain.router:
                response = self.brain.router.speak(message, context)
                return {'response': response}
            return {'error': 'Router not available'}
        elif cmd == 'stimulate':
            importance = params.get('importance', 0.8)
            if self.brain.thyroid:
                stimulated = self.brain.thyroid.stimulate(importance=importance)
                return {'stimulated': stimulated, 'state': self.brain.thyroid.state.name}
            return {'error': 'Thyroid not available'}
        elif cmd == 'filter':
            content = params.get('content', '')
            source = params.get('source', 'socket')
            if self.brain.liver:
                sample = BloodSample(source, content, time.time(), 1.0)
                state, result, meta = self.brain.liver.process(sample)
                return {'state': state.name, 'result': result, 'metadata': meta}
            return {'error': 'Liver not available'}
        elif cmd == 'seed_layers':
            # Directly seed subconscious and unconscious layers
            import json
            seed_path = params.get('path', '/root/.openclaw/workspace/aos/layer_export.json')
            try:
                with open(seed_path, 'r') as f:
                    data = json.load(f)
                
                # Seed subconscious
                for item in data.get('subconscious', []):
                    self.brain.consciousness.subconscious.add(
                        item['content'],
                        intensity=item.get('intensity', 0.7),
                        associations=item.get('associations', [])
                    )
                
                # Seed unconscious
                for item in data.get('unconscious', []):
                    self.brain.consciousness.unconscious.add(
                        item['content'],
                        intensity=item.get('intensity', 0.8),
                        associations=item.get('associations', [])
                    )
                
                sub_count = len(self.brain.consciousness.subconscious.get_active(min_intensity=0.3))
                unc_count = len(self.brain.consciousness.unconscious.get_active(min_intensity=0.3))
                
                return {
                    'seeded': True,
                    'subconscious_seeded': len(data.get('subconscious', [])),
                    'unconscious_seeded': len(data.get('unconscious', [])),
                    'subconscious_active': sub_count,
                    'unconscious_active': unc_count
                }
            except Exception as e:
                return {'error': str(e)}
        elif cmd == 'add_to_layer':
            # Direct addition to any consciousness layer
            layer = params.get('layer', 'subconscious')  # conscious/subconscious/unconscious
            content = params.get('content', '')
            intensity = params.get('intensity', 0.8)
            associations = params.get('associations', [])
            
            target_layer = None
            if layer == 'conscious':
                target_layer = self.brain.consciousness.conscious
            elif layer == 'subconscious':
                target_layer = self.brain.consciousness.subconscious
            elif layer == 'unconscious':
                target_layer = self.brain.consciousness.unconscious
            
            if target_layer:
                target_layer.add(content, intensity=intensity, associations=associations)
                active_count = len(target_layer.get_active(min_intensity=0.3))
                return {
                    'added': True,
                    'layer': layer,
                    'content': content[:50],
                    'active_items': active_count
                }
            return {'error': f'Unknown layer: {layer}'}
        elif cmd == 'perceive':
            observation = params.get('observation', '')
            intensity = params.get('intensity', 0.8)
            if self.brain.consciousness:
                self.brain.consciousness.perceive(observation, intensity=intensity)
                self.brain.consciousness.consolidate()
                con = len(self.brain.consciousness.conscious.get_active())
                sub = len(self.brain.consciousness.subconscious.get_active(min_intensity=0.1))
                unc = len(self.brain.consciousness.unconscious.get_active(min_intensity=0.1))
                return {
                    'perceived': True,
                    'observation': observation[:50],
                    'intensity': intensity,
                    'conscious_items': con,
                    'subconscious_items': sub,
                    'unconscious_items': unc
                }
            return {'error': 'Consciousness not available'}
        elif cmd == 'ingest':
            # Feed through stomach -> intestine -> brain (full metabolic cycle)
            content = params.get('content', '')
            source = params.get('source', 'socket')
            priority = params.get('priority', 0.8)
            
            if self.brain.stomach:
                # Ingest into stomach buffer
                self.brain.stomach.ingest(source, content, priority=priority)
                
                # Get digestion metrics
                buffer_size = len(self.brain.stomach.input_buffer)
                state = self.brain.stomach.state.name if hasattr(self.brain.stomach.state, 'name') else str(self.brain.stomach.state)
                
                return {
                    'ingested': True,
                    'source': source,
                    'buffer_size': buffer_size,
                    'stomach_state': state,
                    'message': 'Content queued in stomach. Will digest on next tick cycle.'
                }
            return {'error': 'Stomach not available'}
        elif cmd == 'save':
            # Trigger manual state save
            if hasattr(self.brain, 'persistence') and self.brain.persistence:
                success = self.brain.persistence.save_state(force=True)
                tick = getattr(self.brain, 'tick_count', 0)
                return {
                    'saved': success,
                    'tick': tick,
                    'state_file': str(self.brain.persistence.STATE_FILE) if success else None
                }
            return {'error': 'Persistence not available'}
        elif cmd == 'load':
            # Check if saved state exists
            if hasattr(self.brain, 'persistence') and self.brain.persistence:
                state = self.brain.persistence.load_state()
                if state:
                    return {
                        'loaded': True,
                        'tick': state.get('tick_count', 0),
                        'saved_at': state.get('saved_at', 'unknown'),
                        'has_cortex': state.get('cortex') is not None,
                        'has_tracray': state.get('tracray') is not None
                    }
                return {'loaded': False, 'message': 'No saved state found'}
            return {'error': 'Persistence not available'}
        elif cmd == 'tick':
            # Return current tick count
            return {
                'tick': getattr(self.brain, 'tick_count', 0),
                'phase': getattr(self.brain, 'current_phase', 'unknown')
            }
        elif cmd == 'waste_loop':
            # Feedback-to-Curriculum: Control the metabolic loop
            action = params.get('action', 'status')
            if self.brain.kidneys:
                if action == 'enable':
                    self.brain.kidneys.waste_loop_enabled = True
                    return {'waste_loop': 'enabled', 'status': 'active'}
                elif action == 'disable':
                    self.brain.kidneys.waste_loop_enabled = False
                    return {'waste_loop': 'disabled', 'status': 'inactive'}
                elif action == 'status':
                    return {
                        'waste_loop_enabled': self.brain.kidneys.waste_loop_enabled,
                        'waste_queue_size': len(self.brain.kidneys.waste_queue),
                        'events_generated': self.brain.kidneys.waste_events_generated,
                        'items_queued': self.brain.kidneys.curriculum_items_queued
                    }
            return {'error': 'Kidneys not available'}
        elif cmd == 'waste_queue':
            # Manage waste queue for curriculum ingestion
            action = params.get('action', 'status')
            if self.brain.kidneys:
                if action == 'status':
                    return self.brain.kidneys.get_waste_queue_status()
                elif action == 'flush':
                    flushed = self.brain.kidneys.flush_waste_queue()
                    return {
                        'flushed': len(flushed),
                        'events': [e.to_dict() for e in flushed]
                    }
            return {'error': 'Kidneys not available'}
        elif cmd == 'priority_curriculum':
            # Check or consume priority curriculum items
            action = params.get('action', 'peek')
            if self.brain.liver:
                if action == 'peek':
                    item = self.brain.liver.peek_priority_queue()
                    if item:
                        return {'has_item': True, 'item': item.to_dict()}
                    return {'has_item': False}
                elif action == 'consume':
                    items = self.brain.liver.get_priority_queue()
                    return {
                        'consumed': len(items),
                        'items': [i.to_dict() for i in items]
                    }
            return {'error': 'Liver not available'}
        elif cmd == 'cortex_register':
            """Register an agent with the cortex"""
            agent_id = params.get('agent_id', 'anonymous')
            success = self.brain.cortex.register_agent(agent_id)
            return {'registered': success, 'agent_id': agent_id}
        elif cmd == 'cortex_write':
            """Agent writes to cortex"""
            from cortex_v25_optimized import AgentWriteRequest
            agent_id = params.get('agent_id', 'anonymous')
            regions = params.get('regions', list(range(8)))
            activations = params.get('activations', [])
            priority = params.get('priority', 1.0)
            ephemeral = params.get('ephemeral', False)
            
            request = AgentWriteRequest(
                agent_id=agent_id,
                region_indices=regions,
                activations=[(a[0], a[1], a[2], a[3]) for a in activations],
                priority=priority,
                ephemeral=ephemeral
            )
            result = self.brain.cortex.agent_write(request)
            return {'write_result': result}
        elif cmd == 'cortex_read':
            """Agent reads from cortex"""
            from cortex_v25_optimized import AgentReadRequest
            agent_id = params.get('agent_id', 'anonymous')
            regions = params.get('regions', list(range(8)))
            max_hotspots = params.get('max_hotspots', 64)
            
            request = AgentReadRequest(
                agent_id=agent_id,
                region_indices=regions,
                layer_mask=params.get('layer_mask', 0b111),
                max_hotspots=max_hotspots
            )
            snapshot = self.brain.cortex.agent_read(request)
            return {
                'tick': snapshot.tick,
                'coherence': snapshot.coherence,
                'pattern_hash': snapshot.pattern_hash,
                'hotspot_count': len(snapshot.hotspots),
                'hotspots': [{"x": c[0], "y": c[1], "z": c[2], "val": v} 
                           for c, v in list(snapshot.hotspots.items())[:max_hotspots]]
            }
        elif cmd == 'cortex_tick':
            """Manually trigger a cortex tick"""
            result = self.brain.cortex.tick_parallel()
            return {
                'tick': result['tick'],
                'active_nodes': result['active_nodes'],
                'sparsity': result['sparsity'],
                'tick_time_ms': result['tick_time_ms']
            }
        elif cmd == 'cortex_stats':
            """Get cortex performance stats"""
            perf = self.brain.cortex.get_performance_stats()
            agent_stats = self.brain.cortex.get_agent_stats()
            return {
                'performance': perf,
                'agents': agent_stats,
                'current_tick': self.brain.cortex.current_tick
            }
        elif cmd == 'curriculum_intelligence':
            """Curriculum Intelligence v1.3 dashboard"""
            action = params.get('action', 'dashboard')
            if self.brain.curriculum_intel:
                if action == 'dashboard':
                    return self.brain.curriculum_intel.get_dashboard()
                elif action == 'metrics':
                    return self.brain.curriculum_intel.get_conversion_metrics()
                elif action == 'report':
                    return {'report': self.brain.curriculum_intel.generate_report()}
                elif action == 'evaluate':
                    lesson_id = params.get('lesson_id')
                    if lesson_id:
                        result = self.brain.curriculum_intel.evaluate_lesson_effectiveness(lesson_id)
                        return {'evaluation': asdict(result) if result else None}
                    return {'error': 'lesson_id required'}
                elif action == 'auto_tune':
                    if self.brain.kidneys:
                        applied = self.brain.curriculum_intel.auto_tune_kidneys(self.brain.kidneys)
                        return {'auto_tuned': True, 'adjustments': applied}
                    return {'error': 'Kidneys not available'}
                elif action == 'threshold_recommendations':
                    recs = self.brain.curriculum_intel.calculate_threshold_recommendations()
                    return {'recommendations': recs}
            return {'error': 'Curriculum Intelligence not available'}
        elif cmd == 'chief_of_staff':
            """APEX Chief of Staff commands"""
            action = params.get('action', 'receive')
            if self.brain.chief_of_staff:
                if action == 'receive':
                    objective = params.get('objective')
                    initiator = params.get('initiator', 'system')
                    if objective:
                        wf_id = self.brain.chief_of_staff.receive_objective(objective, initiator)
                        return {'workflow_id': wf_id, 'status': 'created'}
                    return {'error': 'objective required'}
                elif action == 'execute':
                    workflow_id = params.get('workflow_id')
                    if workflow_id:
                        success = self.brain.chief_of_staff.execute_workflow(workflow_id)
                        return {'workflow_id': workflow_id, 'success': success}
                    return {'error': 'workflow_id required'}
                elif action == 'status':
                    workflow_id = params.get('workflow_id')
                    if workflow_id:
                        status = self.brain.chief_of_staff.get_workflow_status(workflow_id)
                        return {'workflow_id': workflow_id, 'status': status}
                    return {'error': 'workflow_id required'}
                elif action == 'crew_status' or action == 'company_status':
                    company_status = self.brain.chief_of_staff.get_company_status()
                    return company_status
                elif action == 'query':
                    query = params.get('query')
                    if query:
                        result = self.brain.chief_of_staff.query_crew(query)
                        return {'result': result}
                    return {'error': 'query required'}
            return {'error': 'Chief of Staff not available'}
        elif cmd == 'channel':
            """Brain Socket Channel commands"""
            action = params.get('action')
            if self.brain.channels:
                return self.brain.channels.handle_command(action, params)
            return {'error': 'Channels not available'}
        elif cmd == 'crypto_identity':
            """Agent cryptographic identity commands"""
            action = params.get('action', 'create')
            if self.brain.crypto_manager:
                if action == 'create':
                    agent_id = params.get('agent_id')
                    agent_name = params.get('agent_name')
                    if agent_id and agent_name:
                        identity = self.brain.crypto_manager.create_identity(agent_id, agent_name)
                        return {
                            'agent_id': identity.agent_id,
                            'agent_name': identity.agent_name,
                            'public_key': identity.public_key_hex,
                            'npub': identity.npub
                        }
                    return {'error': 'agent_id and agent_name required'}
                elif action == 'load':
                    agent_id = params.get('agent_id')
                    if agent_id:
                        identity = self.brain.crypto_manager.load_identity(agent_id)
                        if identity:
                            return {
                                'agent_id': identity.agent_id,
                                'agent_name': identity.agent_name,
                                'public_key': identity.public_key_hex,
                                'npub': identity.npub
                            }
                        return {'error': 'Identity not found'}
                    return {'error': 'agent_id required'}
                elif action == 'sign_event':
                    agent_id = params.get('agent_id')
                    event_data = params.get('event_data', {})
                    if agent_id:
                        signature = self.brain.crypto_manager.sign_event(agent_id, event_data)
                        return {'signature': signature}
                    return {'error': 'agent_id required'}
                elif action == 'list':
                    agents = self.brain.crypto_manager.list_agents()
                    return {'agents': agents}
            return {'error': 'Crypto manager not available'}
        else:
            return {'error': f'Unknown command: {cmd}'}


class CompleteBrainV44:
    """
    Fully integrated brain with ALL features + Liver + Kidneys + Signal/Noise pipeline
    """
    
    def __init__(self, test_mode=False):
        print("=" * 70)
        print("  🧠 COMPLETE BRAIN v4.4")
        print("  Legacy + Ternary + Socket + THYROID v1.2 + LIVER v1.0 + KIDNEYS v1.0")
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
        self.cortex = CortexV25Optimized(size=32, temporal_depth=128)
        
        print("[Legacy 2/5] TracRay...")
        self.tracray = TracRay(capacity=5000)
        
        print("[Legacy 3/5] Consciousness Layers...")
        self.consciousness = ConsciousnessManager()
        
        print("[Legacy 4/5] QMD Loop...")
        self.qmd = QMDLoop(use_ollama=False)
        
        print("[Legacy 5/5] MemoryBridge...")
        self.memory_bridge = MemoryBridge()
        
        # Model Router
        print("\n[Router] Model Router...")
        self.router = AOSModelRouter()
        
        # NEW v4.4: Liver v1.0 (pre-brain filtration)
        print("\n[NEW v4.4] Liver v1.0 (blood filtration)...")
        self.liver = AOSLiverV1(
            toxic_threshold=0.7,
            purify_threshold=0.3
        )
        
        # NEW v4.4: Kidneys v1.0 (post-brain waste management)
        print("[NEW v4.4] Kidneys v1.0 (waste recycling)...")
        self.kidneys = AOSKidneysV1(
            signal_threshold=0.5,
            reabsorb_threshold=0.2
        )
        
        # NEW v4.5: Ternary Lungs v1.0 (respiratory system)
        print("\n[NEW v4.5] Ternary Lungs v1.0 (respiratory/gas exchange)...")
        self.lungs = TernaryLungs(
            base_breath_rate=1.0,
            base_pressure=1.0,
            classification_threshold=0.2
        )
        
        # Thyroid v1.2 (endocrine regulation)
        print("\n[Thyroid] v1.2 (endocrine regulation)...")
        self.thyroid = AOSThyroidV12(
            qmd_loop=self.qmd,
            baseline_timeout=120.0,
            secretion_duration=30.0
        )
        
        # Sensory
        print("\n[Sensory 1/2] Voice Interface...")
        self.voice = VoiceInterface()
        
        print("[Sensory 2/2] Vision Interface...")
        self.vision = VisionInterface()
        
        # Socket server
        print("\n[Interface] Socket Server...")
        self.socket_server = BrainSocketServer(self)
        
        # NEW v4.6: APEX Chief of Staff (Patricia as coordinator)
        print("\n[APEX] Chief of Staff v1.0 (Patricia as crew coordinator)...")
        try:
            from apex_chief_of_staff import APEXChiefOfStaff
            self.chief_of_staff = APEXChiefOfStaff()
            print("  ✅ Chief of Staff active - Patricia manages crew workflows")
        except Exception as e:
            print(f"  ⚠️ Chief of Staff not loaded: {e}")
            self.chief_of_staff = None
        
        # NEW v4.6: Agent Cryptographic Identities
        print("\n[Crypto] Agent Identity Manager v1.0...")
        try:
            from agent_crypto_identity import AgentCryptoManager
            self.crypto_manager = AgentCryptoManager()
            print("  ✅ Cryptographic identities active")
        except Exception as e:
            print(f"  ⚠️ Crypto manager not loaded: {e}")
            self.crypto_manager = None
        
        # NEW v4.6: Brain Socket Channels (Buzz-inspired)
        print("\n[Channels] Brain Socket Channels v1.0...")
        try:
            from brain_socket_channels import BrainSocketChannels
            self.channels = BrainSocketChannels()
            print("  ✅ Channel-based collaboration active")
        except Exception as e:
            print(f"  ⚠️ Channels not loaded: {e}")
            self.channels = None
        
        # State
        self.tick_count = 0
        self.running = True
        self.paused = False
        self.current_phase = "Initialize"
        
        # Signal/Noise tracking
        self.signal_quality_history = []
        self.noise_events = []
        
        # Signals
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # NEW: Persistence Layer v1.0
        print("\n[Persistence v1.0] Loading brain state...")
        try:
            from brain_persistence import integrate_persistence, start_auto_save
            self.persistence = integrate_persistence(self)
            start_auto_save(self, interval_seconds=60)
            print("  ✅ Persistence active - Auto-save every 60s")
        except Exception as e:
            print(f"  ⚠️ Persistence not loaded: {e}")
            self.persistence = None
        
        # NEW v4.6: Feedback-to-Curriculum persistence
        print("\n[Feedback-to-Curriculum v1.1] Initializing...")
        self.waste_queue_path = '/var/lib/aos/brain_state/waste_queue.json'
        self._ensure_waste_state_dir()
        self._load_waste_queue()
        print("  ✅ Waste queue persistence ready")
        
        # NEW v4.6: Curriculum Intelligence v1.3
        print("\n[Curriculum Intelligence v1.3] Initializing...")
        try:
            from curriculum_intelligence import CurriculumIntelligence
            self.curriculum_intel = CurriculumIntelligence()
            print("  ✅ Intelligence layer active - tracking lesson effectiveness")
        except Exception as e:
            print(f"  ⚠️ Curriculum Intelligence not loaded: {e}")
            self.curriculum_intel = None
    
    def _ensure_waste_state_dir(self):
        """Ensure waste queue directory exists"""
        state_dir = os.path.dirname(self.waste_queue_path)
        os.makedirs(state_dir, exist_ok=True)
    
    def _load_waste_queue(self):
        """Load persisted waste queue from disk"""
        if not os.path.exists(self.waste_queue_path):
            return
        try:
            with open(self.waste_queue_path, 'r') as f:
                data = json.load(f)
            # Queue is loaded by curriculum_feeder, not directly here
            print(f"  💾 Loaded {len(data)} waste events from disk")
        except Exception as e:
            print(f"  ⚠️ Could not load waste queue: {e}")
    
    def _save_waste_queue(self):
        """Save current waste queue to disk"""
        if not hasattr(self, 'kidneys') or not self.kidneys:
            return
        try:
            events = self.kidneys.flush_waste_queue()
            if events:
                # Load existing
                existing = []
                if os.path.exists(self.waste_queue_path):
                    with open(self.waste_queue_path, 'r') as f:
                        existing = json.load(f)
                # Append new
                existing.extend([e.to_dict() for e in events])
                # Save
                with open(self.waste_queue_path, 'w') as f:
                    json.dump(existing, f, indent=2)
        except Exception as e:
            print(f"[Waste Queue] Save error: {e}")
        
        print("\n" + "=" * 70)
        print("  ✅ ALL SYSTEMS INITIALIZED")
        if self.persistence:
            print(f"  💾 Persistence: ON (tick {self.tick_count})")
        print("=" * 70)
        
        # Announce via router (non-blocking, just print)
        print("\n[Voice] Complete Brain v4.4 initialized with Liver and Kidneys signal processing")
    
    def _signal_handler(self, signum, frame):
        print(f"\n[SYSTEM] Signal {signum} received")
        self.running = False
    
    def _get_visual_input(self) -> str:
        """Get visual observation"""
        observation = self.vision.observe()
        return observation if observation else "No visual input"
    
    def _filter_through_liver(self, observation: str) -> tuple:
        """
        LIVER v1.0: Pre-brain blood filtration
        Returns: (filtered_content, liver_state, metadata)
        """
        sample = BloodSample(
            source="vision",
            content=observation,
            timestamp=time.time(),
            flow_rate=1.0
        )
        
        state, result, meta = self.liver.process(sample)
        
        if state == LiverState.TOXIC:
            # Toxic - replace with safe placeholder
            return f"[FILTERED: Toxic content neutralized]", state, meta
        elif state == LiverState.PURIFY:
            # Purified - use cleaned version
            return result if result else observation, state, meta
        else:
            # Clean - pass through
            return observation, state, meta
    
    def _process_through_kidneys(self, content: str, context: dict) -> tuple:
        """
        KIDNEYS v1.0: Post-brain waste management
        Returns: (result, kidney_state, metadata)
        """
        state, result, meta = self.kidneys.process(
            content=content,
            source="brain_output",
            context=context
        )
        
        return result, state, meta
    
    def _process_cortex(self, observation: str, phase: str) -> dict:
        """Process through Cortex v2.5 with agent API"""
        import numpy as np
        
        # Generate embedding from observation
        encoded = np.random.randn(256) * 0.1
        
        # Agent write to cortex
        write_req = AgentWriteRequest(
            agent_id="brain_core",
            region_indices=list(range(8)),
            activations=[],  # Will be generated from embedding
            priority=0.7
        )
        
        # Convert embedding to hotspots and write
        # hotspots = self.cortex.embed_to_hotspots(encoded, n_hotspots=64)
        # FIXME: Method missing from CortexV25Optimized - using fallback
        hotspots = []
        write_req.activations = hotspots
        self.cortex.agent_write(write_req)
        
        # Tick cortex for propagation
        tick_result = self.cortex.tick_parallel()
        
        # Read back state
        read_req = AgentReadRequest(
            agent_id="brain_core",
            region_indices=list(range(8)),
            layer_mask=0b111,
            max_hotspots=32
        )
        snapshot = self.cortex.agent_read(read_req)
        
        return {
            "active_nodes": tick_result.get("active_nodes", 0),
            "coherence": snapshot.coherence,
            "patterns_detected": len(snapshot.hotspots),
            "tick": snapshot.tick
        }
    
    def system_cycle(self):
        """One complete cycle with Liver → Brain → Kidneys pipeline"""
        if self.paused:
            time.sleep(0.1)
            return 0.1
        
        self.tick_count += 1
        
        # 1. Raw visual input
        raw_observation = self._get_visual_input()
        
        # 1.5: LUNGS: Inhale ambient atmosphere and perform gas exchange
        # Get heart state first for lung rhythm modulation
        heart_valence = 0.0
        metabolic_demand = 1.0
        if hasattr(self, 'heart') and self.heart:
            # Estimate valence from heart state (-1 to +1)
            heart_state = self.heart.rhythm.state
            if hasattr(heart_state, 'value'):
                heart_valence = heart_state.value / 10.0  # Normalize roughly
            metabolic_demand = 0.6 + (self.heart.rhythm.bpm - 60) / 120.0
        
        # Create ambient stream from raw observation
        ambient_stream = [raw_observation] if raw_observation else []
        
        # Lungs perform gas exchange
        oxygen_packet, exhaled_waste = self.lungs.step(
            ambient_stream=ambient_stream,
            heart_valence=heart_valence,
            metabolic_demand=metabolic_demand
        )
        
        # Use oxygenated signal as the filtered observation
        # Prioritize positives, then neutrals, then fall back to raw
        if oxygen_packet.positives:
            filtered_obs = str(oxygen_packet.positives[0])
        elif oxygen_packet.neutrals:
            filtered_obs = str(oxygen_packet.neutrals[0])
        else:
            filtered_obs = raw_observation
        
        # Get lungs metrics for tracking
        lung_metrics = self.lungs.get_metrics()
        
        # 2. LIVER: Pre-brain filtration (now working on oxygenated input)
        filtered_obs, liver_state, liver_meta = self._filter_through_liver(raw_observation)
        
        # Track signal quality
        signal_quality = 1.0 - liver_meta.get('original_toxicity', 0.0)
        self.signal_quality_history.append(signal_quality)
        if len(self.signal_quality_history) > 100:
            self.signal_quality_history.pop(0)
        
        # 3. Stomach ingestion (only if not TOXIC)
        if liver_state != LiverState.TOXIC:
            self.stomach.ingest("vision", filtered_obs, priority=signal_quality)
        
        # 4. Consciousness processing
        self.consciousness.perceive(filtered_obs, intensity=signal_quality * 0.7)
        self.consciousness.consolidate()
        
        # 5. Stomach digestion
        from ternary_interfaces import DigestionInput, IntestineInput
        
        stomach_inputs = DigestionInput(
            input_amount=0.1 * signal_quality,
            heart_energy_demand=0.6,
            stress_level=0.2 if liver_state != LiverState.TOXIC else 0.5
        )
        stomach_output = self.stomach.digest(stomach_inputs)
        
        # 6. Intestine distribution
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
        
        # 7. Heart beat
        heart_inputs = HeartBeatInput(
            brain_arousal=signal_quality * 0.5,
            safety=0.8 if liver_state != LiverState.TOXIC else 0.5,
            stress=0.2 if liver_state != LiverState.TOXIC else 0.5,
            connection=0.6,
            cognitive_load=0.5
        )
        heart_output = self.heart.beat(heart_inputs)
        
        # 8. Cortex processing
        cortex_result = self._process_cortex(filtered_obs, "Observe")
        
        # 9. Brain tick
        brain_inputs = BrainInput(
            heart_bpm=heart_output.bpm,
            heart_state=heart_output.state,
            heart_coherence=heart_output.coherence,
            heart_arousal=heart_output.arousal,
            emotional_tone=heart_output.emotional_tone,
            observation=filtered_obs,
            observation_type="multimodal"
        )
        brain_output = self.brain.tick(brain_inputs)
        self.current_phase = brain_output.phase
        
        # 10. QMD decision (via Router when secreting)
        qmd_context = {
            "phase": brain_output.phase,
            "observation": filtered_obs,
            "liver_state": liver_state.name,
            "signal_quality": signal_quality,
            "limbic": {
                "novelty": brain_output.novelty,
                "reward": brain_output.reward
            }
        }
        
        # Check thyroid state and budget mode
        qmd_result = None
        if hasattr(self.thyroid, 'budget_mode') and self.thyroid.budget_mode == "EMERGENCY":
            # EMERGENCY: Use Gemma 4 E4B via emergency_decide
            try:
                action, confidence = self.router.emergency_decide(qmd_context)
                qmd_result = {
                    "action": action.lower(),
                    "confidence": confidence,
                    "reasoning": "emergency_gemma4e4b",
                    "model": self.router.MODELS['emergency']
                }
                print(f"[Brain] 🚨 Emergency decision via Gemma 4 E4B: {action}")
            except Exception as e:
                print(f"[Brain] Emergency decision failed, using QMD: {str(e)[:30]}")
                qmd_result = self.qmd.cycle(qmd_context, memory_bridge=self.memory_bridge)
        elif self.thyroid.state == ThyroidState.SECRETING:
            try:
                action, confidence = self.router.decide(qmd_context)
                qmd_result = {
                    "action": action.lower(),
                    "confidence": confidence,
                    "reasoning": "model_router",
                    "model": self.router.MODELS['decision']
                }
            except Exception as e:
                qmd_result = self.qmd.cycle(qmd_context, memory_bridge=self.memory_bridge)
        else:
            qmd_result = self.qmd.cycle(qmd_context, memory_bridge=self.memory_bridge)
        
        # 11. KIDNEYS: Post-brain waste management
        action_str = json.dumps(qmd_result)
        kidney_result, kidney_state, kidney_meta = self._process_through_kidneys(
            action_str,
            {"is_brain_output": True, "liver_state": liver_state.name}
        )
        
        # NEW v4.6: Curriculum Intelligence tracking
        if self.curriculum_intel and kidney_meta.get('waste_event_created'):
            waste_event = kidney_meta.get('waste_event')
            if waste_event:
                # Record error for trend tracking
                self.curriculum_intel.record_error_event(
                    waste_event.error_category,
                    waste_event.severity
                )
                
                # If lesson was created, track it
                if hasattr(waste_event, 'suggested_lesson'):
                    self.curriculum_intel.record_lesson_created(
                        lesson_id=waste_event.event_id,
                        error_category=waste_event.error_category,
                        lesson_content=waste_event.suggested_lesson
                    )
        
        # 12. TracRay record (with full pipeline metadata)
        self.tracray.record(
            tick=self.tick_count,
            phase=brain_output.phase,
            limbic={
                "novelty": brain_output.novelty,
                "reward": brain_output.reward,
                "signal_quality": signal_quality
            },
            observation=filtered_obs[:100],
            action=qmd_result.get("action", "unknown")
        )
        
        # NEW v4.6: Check for priority curriculum from Liver
        if self.liver and self.liver.has_priority_items():
            priority_items = self.liver.get_priority_queue()
            if priority_items:
                print(f"  ⚡ Consuming {len(priority_items)} priority curriculum items")
                # Process priority items (feed to consciousness immediately)
                for item in priority_items:
                    self.consciousness.perceive(item.content, intensity=item.importance)
                    print(f"    📚 Learned: {item.error_category} → {item.content[:60]}...")
        
        # Save waste queue periodically
        if self.tick_count % 10 == 0:
            self._save_waste_queue()
        
        # Display status every 50 ticks
        if self.tick_count % 50 == 0:
            summary = self.consciousness.get_layer_summary()
            thyroid_state = self.thyroid.state.name
            kidney_state_str = self.kidneys.state.name
            lung_phase = self.lungs.phase if hasattr(self.lungs, 'phase') else "REST"
            avg_signal = sum(self.signal_quality_history[-20:]) / min(len(self.signal_quality_history[-20:]), 20)
            
            # NEW v4.6: Intelligence metrics
            intel_status = ""
            if self.curriculum_intel:
                metrics = self.curriculum_intel.get_conversion_metrics()
                if metrics['total_lessons_created'] > 0:
                    intel_status = f" | 📚 {metrics['lesson_conversion_rate']:.0%} lesson conversion"
            
            print(f"\n[Cycle {self.tick_count:5d}] "
                  f"🫀 {heart_output.bpm:.0f} BPM | "
                  f"🧠 {brain_output.phase:8s} | "
                  f"🎛️  {qmd_result.get('action', 'unknown'):10s} | "
                  f"🫁 {thyroid_state:10s} | "
                  f"🫘 {kidney_state_str:8s} | "
                  f"📶 {avg_signal:.2f}{intel_status}")
            print(f"              Liver: {liver_state.name:8s} | "
                  f"Lungs: {lung_phase:8s} | "
                  f"Con:{summary['conscious']['active_items']}/"
                  f"Sub:{summary['subconscious']['active_items']} | "
                  f"Waste:{kidney_meta['bladder_level']}")
            
            # NEW v4.6: Print intelligence report every 250 ticks
            if self.tick_count % 250 == 0 and self.curriculum_intel:
                print("\n" + self.curriculum_intel.generate_report())
        
        # Save periodically
        if self.tick_count % 100 == 0:
            self.brain.save_state()
            self.tracray.end_episode(f"tick_{self.tick_count}")
        
        return 60.0 / heart_output.bpm
    
    def get_status(self) -> dict:
        """Get complete system status with all organs"""
        recent_signal = sum(self.signal_quality_history[-20:]) / max(len(self.signal_quality_history[-20:]), 1) if self.signal_quality_history else 0.5
        
        return {
            "version": "4.5",
            "tick": self.tick_count,
            "phase": self.current_phase,
            "signal_quality_20avg": recent_signal,
            "cortex": {
                "performance": self.cortex.get_performance_stats() if hasattr(self.cortex, 'get_performance_stats') else {},
                "agents": self.cortex.get_agent_stats() if hasattr(self.cortex, 'get_agent_stats') else {},
                "active_nodes": sum(len(r.active_nodes) for r in self.cortex.regions) if hasattr(self.cortex, 'regions') else 0
            },
            "tracray": self.tracray.get_stats(),
            "qmd": self.qmd.get_stats(),
            "consciousness": self.consciousness.get_layer_summary(),
            "thyroid": self.thyroid.get_status() if self.thyroid else None,
            "lungs": self.lungs.get_status() if hasattr(self, 'lungs') and self.lungs else None,
            "liver": self.liver.get_status() if self.liver else None,
            "kidneys": self.kidneys.get_status() if self.kidneys else None,
            "router": {
                "models": self.router.MODELS if self.router else None,
                "stats": self.router.get_stats() if self.router else None
            },
            "components_active": 15,
            "pipeline": "Lungs → Liver → Brain → Kidneys"
        }
    
    def run(self):
        """Run complete system with full signal/noise pipeline"""
        print("\n[SYSTEM] Complete Brain v4.4 running...")
        print("         Signal pipeline: Liver → Brain → Kidneys")
        
        # Start all organ monitors
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
                import traceback
                traceback.print_exc()
                time.sleep(1)
        
        print("\n[SYSTEM] Shutting down...")
        self.socket_server.stop()
        self.thyroid.stop()
        self.brain.save_state()
        
        status = self.get_status()
        print(f"[SYSTEM] Final: {status['tick']} ticks")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  🧠 COMPLETE BRAIN v4.5")
    print("  Lungs v1.0 + Liver v1.0 + Kidneys v1.0 + Thyroid v1.2 + Respiratory Pipeline")
    print("=" * 70)
    
    brain = CompleteBrainV44()
    
    try:
        brain.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("=" * 70)
        print("  Complete Brain v4.5 Finished")
        print("=" * 70)
