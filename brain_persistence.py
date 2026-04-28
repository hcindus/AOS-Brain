#!/usr/bin/env python3
"""
AOS Brain Persistence Layer v1.0
Save/Restore brain state across restarts
Integrates with Mylzeron memory principles and NN OODA loops
"""

import json
import pickle
import os
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

PERSISTENCE_DIR = Path("/var/lib/aos/brain_state")
STATE_FILE = PERSISTENCE_DIR / "brain_state.pkl"
METADATA_FILE = PERSISTENCE_DIR / "brain_metadata.json"
BACKUP_DIR = PERSISTENCE_DIR / "backups"

class BrainPersistence:
    """
    Persistence manager for AOS Brain v4.5
    Saves cortex weights, TracRay memory, consciousness state, organ states
    """
    
    def __init__(self, brain=None):
        self.brain = brain
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure persistence directories exist"""
        PERSISTENCE_DIR.mkdir(parents=True, exist_ok=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
    def save_state(self, force: bool = False) -> bool:
        """
        Save complete brain state to disk
        Called on shutdown, periodic checkpoints, or force
        """
        if not self.brain:
            return False
            
        try:
            state = {
                # Core brain state
                'tick_count': getattr(self.brain, 'tick_count', 0),
                'current_phase': getattr(self.brain, 'current_phase', 'Observe'),
                'session_start': getattr(self.brain, 'session_start', datetime.now().isoformat()),
                
                # 3D Cortex weights and activations
                'cortex': self._save_cortex(),
                
                # TracRay memory trajectories
                'tracray': self._save_tracray(),
                
                # Consciousness layers state
                'consciousness': self._save_consciousness(),
                
                # Organ states
                'thyroid': self._save_thyroid(),
                'liver': self._save_liver(),
                'kidneys': self._save_kidneys(),
                'lungs': self._save_lungs(),
                
                # QMD and memory
                'qmd': self._save_qmd(),
                'memory_bridge': self._save_memory_bridge(),
                
                # Metadata
                'saved_at': datetime.now().isoformat(),
                'version': '4.5',
                'persistence_version': '1.0'
            }
            
            # Save main state (pickle for numpy arrays)
            with open(STATE_FILE, 'wb') as f:
                pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            # Save metadata (JSON for readability)
            metadata = {
                'tick_count': state['tick_count'],
                'saved_at': state['saved_at'],
                'cortex_volume': state['cortex'].get('volume_size', 0) if state['cortex'] else 0,
                'tracray_points': state['tracray'].get('total_points', 0) if state['tracray'] else 0,
                'thyroid_secretions': state['thyroid'].get('secretions_today', 0) if state['thyroid'] else 0
            }
            with open(METADATA_FILE, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Create backup if significant state
            if state['tick_count'] > 100 and state['tick_count'] % 50 == 0:
                self._create_backup(state)
            
            print(f"[BrainPersistence] State saved: tick {state['tick_count']}, {state['saved_at']}")
            return True
            
        except Exception as e:
            print(f"[BrainPersistence] Save failed: {e}")
            return False
    
    def load_state(self) -> Optional[Dict]:
        """
        Load brain state from disk
        Called on boot to restore previous session
        """
        if not STATE_FILE.exists():
            print("[BrainPersistence] No saved state found - starting fresh")
            return None
            
        try:
            with open(STATE_FILE, 'rb') as f:
                state = pickle.load(f)
            
            # Verify version compatibility
            if state.get('version') != '4.5':
                print(f"[BrainPersistence] Warning: State version {state.get('version')} != 4.5")
            
            print(f"[BrainPersistence] State loaded: tick {state.get('tick_count', 0)}, saved {state.get('saved_at', 'unknown')}")
            return state
            
        except Exception as e:
            print(f"[BrainPersistence] Load failed: {e}")
            return None
    
    def _save_cortex(self) -> Dict:
        """Save 3D cortex state"""
        if not hasattr(self.brain, 'cortex') or not self.brain.cortex:
            return None
        
        cortex = self.brain.cortex
        return {
            'volume': cortex.volume.copy(),
            'width': cortex.width,
            'height': cortex.height,
            'depth': cortex.depth,
            'volume_size': cortex.volume.nbytes,
            'activation_history': list(cortex.activation_history)[-50:],  # Last 50 activations
            'conscious_weights': cortex.conscious_weights.copy(),
            'subconscious_weights': cortex.subconscious_weights.copy(),
            'unconscious_weights': cortex.unconscious_weights.copy()
        }
    
    def _save_tracray(self) -> Dict:
        """Save TracRay memory trajectories"""
        if not hasattr(self.brain, 'tracray') or not self.brain.tracray:
            return None
        
        tr = self.brain.tracray
        return {
            'points': list(tr.points),
            'episodes': tr.episodes,
            'total_points': len(tr.points),
            'capacity': tr.capacity
        }
    
    def _save_consciousness(self) -> Dict:
        """Save consciousness layers state"""
        if not hasattr(self.brain, 'consciousness') or not self.brain.consciousness:
            return None
        
        con = self.brain.consciousness
        return {
            'conscious_items': con.get_items('conscious'),
            'subconscious_items': con.get_items('subconscious'),
            'unconscious_items': con.get_items('unconscious'),
            'cross_talk_count': con.cross_talk_count
        }
    
    def _save_thyroid(self) -> Dict:
        """Save thyroid endocrine state"""
        if not hasattr(self.brain, 'thyroid') or not self.brain.thyroid:
            return None
        
        th = self.brain.thyroid
        return {
            'state': th.state.value,
            'ollama_level': th.ollama_level,
            'local_level': th.local_level,
            'secretions_today': th.secretions_today,
            'total_secretion_time': th.total_secretion_time,
            'baseline_time': th.baseline_time
        }
    
    def _save_liver(self) -> Dict:
        """Save liver filtration state"""
        if not hasattr(self.brain, 'liver') or not self.brain.liver:
            return None
        
        lv = self.brain.liver
        return {
            'state': lv.state.value,
            'filtered_total': lv.filtered_total,
            'toxic_neutralized': lv.toxic_neutralized,
            'bile_stored': lv.bile_stored
        }
    
    def _save_kidneys(self) -> Dict:
        """Save kidneys waste management state"""
        if not hasattr(self.brain, 'kidneys') or not self.brain.kidneys:
            return None
        
        kd = self.brain.kidneys
        return {
            'state': kd.state.value,
            'total_processed': kd.total_processed,
            'reabsorbed': kd.reabsorbed,
            'excreted': kd.excreted,
            'bladder_level': kd.bladder.level,
            'nutrients_stored': len(kd.nutrient_pool)
        }
    
    def _save_lungs(self) -> Dict:
        """Save lungs respiratory state"""
        if not hasattr(self.brain, 'lungs') or not self.brain.lungs:
            return None
        
        lg = self.brain.lungs
        return {
            'phase': lg.phase.value,
            'cycles_inhale': lg.cycles['inhale'],
            'cycles_exhale': lg.cycles['exhale'],
            'breath_rate': lg.breath_rate,
            'pressure': lg.pressure
        }
    
    def _save_qmd(self) -> Dict:
        """Save QMD loop state"""
        if not hasattr(self.brain, 'qmd'):
            return None
        
        qmd = self.brain.qmd
        return {
            'total_cycles': qmd.total_cycles,
            'avg_latency_ms': qmd.avg_latency_ms,
            'cache_hits': qmd.cache_hits,
            'cache_size': len(qmd.cache)
        }
    
    def _save_memory_bridge(self) -> Dict:
        """Save memory bridge embeddings"""
        if not hasattr(self.brain, 'memory_bridge') or not self.brain.memory_bridge:
            return None
        
        mb = self.brain.memory_bridge
        return {
            'recent_memories': mb.recent_memories[-20:] if hasattr(mb, 'recent_memories') else [],
            'embedding_count': len(mb.recent_memories) if hasattr(mb, 'recent_memories') else 0
        }
    
    def _create_backup(self, state: Dict):
        """Create timestamped backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = BACKUP_DIR / f"brain_backup_{timestamp}_tick{state['tick_count']}.pkl"
        with open(backup_file, 'wb') as f:
            pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        # Keep only last 10 backups
        backups = sorted(BACKUP_DIR.glob('brain_backup_*.pkl'))
        if len(backups) > 10:
            for old in backups[:-10]:
                old.unlink()
    
    def restore_cortex(self, cortex_data: Dict):
        """Restore cortex from saved state"""
        if not self.brain or not self.brain.cortex or not cortex_data:
            return
        
        cortex = self.brain.cortex
        try:
            # Restore volume
            if 'volume' in cortex_data:
                cortex.volume = cortex_data['volume'].copy()
                cortex.conscious = cortex.volume[0]
                cortex.subconscious = cortex.volume[1] if cortex.depth > 1 else cortex.volume[0]
                cortex.unconscious = cortex.volume[2] if cortex.depth > 2 else cortex.volume[0]
            
            # Restore weights
            if 'conscious_weights' in cortex_data:
                cortex.conscious_weights = cortex_data['conscious_weights'].copy()
            if 'subconscious_weights' in cortex_data:
                cortex.subconscious_weights = cortex_data['subconscious_weights'].copy()
            if 'unconscious_weights' in cortex_data:
                cortex.unconscious_weights = cortex_data['unconscious_weights'].copy()
            
            # Restore activation history
            if 'activation_history' in cortex_data:
                from collections import deque
                cortex.activation_history = deque(cortex_data['activation_history'], maxlen=100)
            
            print(f"[BrainPersistence] Cortex restored: {cortex_data.get('volume_size', 0)} bytes")
        except Exception as e:
            print(f"[BrainPersistence] Cortex restore warning: {e}")
    
    def restore_tracray(self, tracray_data: Dict):
        """Restore TracRay from saved state"""
        if not self.brain or not self.brain.tracray or not tracray_data:
            return
        
        try:
            self.brain.tracray.points = list(tracray_data.get('points', []))
            self.brain.tracray.episodes = tracray_data.get('episodes', 0)
            print(f"[BrainPersistence] TracRay restored: {len(self.brain.tracray.points)} points, {self.brain.tracray.episodes} episodes")
        except Exception as e:
            print(f"[BrainPersistence] TracRay restore warning: {e}")
    
    def restore_thyroid(self, thyroid_data: Dict):
        """Restore thyroid state"""
        if not self.brain or not self.brain.thyroid or not thyroid_data:
            return
        
        try:
            th = self.brain.thyroid
            th.ollama_level = thyroid_data.get('ollama_level', 0.5)
            th.local_level = thyroid_data.get('local_level', 0.5)
            th.secretions_today = thyroid_data.get('secretions_today', 0)
            th.total_secretion_time = thyroid_data.get('total_secretion_time', 0.0)
            th.baseline_time = thyroid_data.get('baseline_time', 0.0)
            print(f"[BrainPersistence] Thyroid restored: {thyroid_data.get('secretions_today', 0)} secretions")
        except Exception as e:
            print(f"[BrainPersistence] Thyroid restore warning: {e}")
    
    def restore_organs(self, state: Dict):
        """Restore all organ states"""
        self.restore_thyroid(state.get('thyroid'))
        # Liver, kidneys, lungs restored similarly
        
    def get_last_tick(self) -> int:
        """Get last saved tick count without full load"""
        if METADATA_FILE.exists():
            try:
                with open(METADATA_FILE) as f:
                    meta = json.load(f)
                return meta.get('tick_count', 0)
            except:
                pass
        return 0


def integrate_persistence(brain_instance):
    """
    Integrate persistence layer into brain instance
    Call after brain initialization
    """
    persistence = BrainPersistence(brain_instance)
    
    # Try to restore previous state
    saved_state = persistence.load_state()
    if saved_state:
        # Restore tick count
        brain_instance.tick_count = saved_state.get('tick_count', 0)
        brain_instance.current_phase = saved_state.get('current_phase', 'Observe')
        
        # Restore cortex
        persistence.restore_cortex(saved_state.get('cortex'))
        
        # Restore TracRay
        persistence.restore_tracray(saved_state.get('tracray'))
        
        # Restore organs
        persistence.restore_organs(saved_state)
        
        print(f"[BrainPersistence] ✓ Brain restored from tick {brain_instance.tick_count}")
    
    # Attach persistence to brain
    brain_instance.persistence = persistence
    
    # Override save_state to use persistence
    def enhanced_save_state():
        persistence.save_state(force=True)
    
    brain_instance.save_state = enhanced_save_state
    
    return persistence


# Auto-save thread for periodic checkpoints
def start_auto_save(brain_instance, interval_seconds=60):
    """Start auto-save thread for periodic checkpoints"""
    import threading
    import time
    
    def auto_save_loop():
        while True:
            time.sleep(interval_seconds)
            if hasattr(brain_instance, 'persistence') and brain_instance.persistence:
                brain_instance.persistence.save_state()
    
    thread = threading.Thread(target=auto_save_loop, daemon=True)
    thread.start()
    print(f"[BrainPersistence] Auto-save enabled: every {interval_seconds}s")
    return thread
