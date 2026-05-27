#!/usr/bin/env python3
"""
AOS SENSORY MEMORY v1.0
Persistent sensory patterns across sessions
Saves important patterns to disk and reloads on startup
"""

import numpy as np
import json
import socket
import time
import hashlib
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from pathlib import Path

class SensoryMemory:
    """
    Long-term storage for sensory patterns
    Persists across brain restarts
    """
    
    def __init__(self, brain_socket='/tmp/aos_brain.sock', 
                 agent_id="sensory_memory",
                 storage_path='/root/.aos/aos/sensory_memory'):
        self.brain_socket = brain_socket
        self.agent_id = agent_id
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Pattern storage
        self.patterns: Dict[str, Dict] = {}
        self.pattern_index = []
        
        # Load existing
        self._load_memory()
        
        print(f"[SensoryMemory] Initialized")
        print(f"  Storage: {self.storage_path}")
        print(f"  Patterns: {len(self.patterns)}")
    
    def _send(self, cmd, params):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.brain_socket)
            sock.sendall((json.dumps({'cmd': cmd, 'params': params}) + '\n').encode())
            data = sock.recv(4096)
            sock.close()
            return json.loads(data.decode()) if data else {}
        except:
            return {}
    
    def _load_memory(self):
        """Load saved patterns"""
        memory_file = self.storage_path / 'sensory_patterns.json'
        if memory_file.exists():
            try:
                with open(memory_file, 'r') as f:
                    data = json.load(f)
                    self.patterns = data.get('patterns', {})
                    self.pattern_index = data.get('index', [])
                print(f"  Loaded {len(self.patterns)} patterns from disk")
            except Exception as e:
                print(f"  Error loading: {e}")
    
    def _save_memory(self):
        """Save patterns to disk"""
        memory_file = self.storage_path / 'sensory_patterns.json'
        try:
            with open(memory_file, 'w') as f:
                json.dump({
                    'patterns': self.patterns,
                    'index': self.pattern_index,
                    'last_saved': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"[SensoryMemory] Save error: {e}")
    
    def _calculate_importance(self, features: Dict) -> float:
        """Calculate pattern importance score"""
        score = 0.0
        
        # Novelty - new patterns are important
        feature_hash = hashlib.md5(
            json.dumps(features, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        if feature_hash not in self.patterns:
            score += 0.3
        
        # Complexity - complex patterns carry more information
        if 'edge_complexity' in features:
            score += features['edge_complexity'] * 0.2
        if 'texture_variance' in features:
            score += features['texture_variance'] * 0.2
        
        # Trigger association - patterns that triggered reactions
        if 'triggered_actions' in features and features['triggered_actions']:
            score += 0.3
        
        return min(1.0, score)
    
    def store_pattern(self, modality: str, features: Dict, hotspots: List):
        """Store a sensory pattern if important"""
        importance = self._calculate_importance(features)
        
        if importance < 0.4:
            return False  # Not worth storing
        
        pattern_id = f"{modality}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.patterns)}"
        
        self.patterns[pattern_id] = {
            'modality': modality,
            'features': features,
            'hotspots': hotspots[:100],  # Store subset
            'importance': importance,
            'timestamp': datetime.now().isoformat(),
            'access_count': 0
        }
        
        self.pattern_index.append(pattern_id)
        
        # Prune if too many
        if len(self.patterns) > 1000:
            self._prune_old_patterns()
        
        # Save periodically
        if len(self.patterns) % 10 == 0:
            self._save_memory()
        
        return True
    
    def _prune_old_patterns(self):
        """Remove least important patterns"""
        sorted_patterns = sorted(
            self.patterns.items(),
            key=lambda x: (x[1]['importance'], x[1].get('access_count', 0)),
            reverse=True
        )
        
        # Keep top 800
        keep_ids = [p[0] for p in sorted_patterns[:800]]
        self.patterns = {k: v for k, v in self.patterns.items() if k in keep_ids}
        self.pattern_index = keep_ids
        
        print(f"[SensoryMemory] Pruned to {len(self.patterns)} patterns")
    
    def find_similar(self, features: Dict, modality: str = None) -> List[Dict]:
        """Find similar patterns in memory"""
        similar = []
        
        for pid, pattern in self.patterns.items():
            if modality and pattern['modality'] != modality:
                continue
            
            # Simple similarity check
            similarity = self._calculate_similarity(features, pattern['features'])
            
            if similarity > 0.7:
                similar.append({
                    'id': pid,
                    'similarity': similarity,
                    'data': pattern
                })
        
        return sorted(similar, key=lambda x: -x['similarity'])[:5]
    
    def _calculate_similarity(self, f1: Dict, f2: Dict) -> float:
        """Calculate feature similarity"""
        keys = set(f1.keys()) & set(f2.keys())
        if not keys:
            return 0.0
        
        diffs = []
        for k in keys:
            if isinstance(f1[k], (int, float)) and isinstance(f2[k], (int, float)):
                diffs.append(abs(f1[k] - f2[k]))
        
        if not diffs:
            return 0.0
        
        avg_diff = np.mean(diffs)
        return max(0, 1 - avg_diff)
    
    def replay_memory(self, count: int = 10):
        """Replay stored patterns back to brain"""
        print(f"\n[SensoryMemory] Replaying {count} patterns...")
        
        # Get most important patterns
        top_patterns = sorted(
            self.patterns.items(),
            key=lambda x: x[1]['importance'],
            reverse=True
        )[:count]
        
        self._send('cortex_register', {'agent_id': self.agent_id})
        
        for pid, pattern in top_patterns:
            hotspots = pattern['hotspots']
            
            self._send('cortex_write', {
                'agent_id': self.agent_id,
                'regions': list(range(8)),
                'activations': hotspots,
                'priority': pattern['importance'] * 0.8,
                'ephemeral': False
            })
            
            pattern['access_count'] = pattern.get('access_count', 0) + 1
            
            print(f"  Replayed {pattern['modality']} pattern "
                  f"({pattern['importance']:.2f} importance)")
            
            time.sleep(0.2)
        
        self._send('cortex_tick', {})
        print(f"[SensoryMemory] Replay complete")
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        modalities = {}
        for p in self.patterns.values():
            m = p['modality']
            modalities[m] = modalities.get(m, 0) + 1
        
        return {
            'total_patterns': len(self.patterns),
            'by_modality': modalities,
            'storage_path': str(self.storage_path)
        }

def main():
    memory = SensoryMemory()
    
    # Show stats
    print(f"\n[SensoryMemory] Stats:")
    stats = memory.get_stats()
    print(f"  Total: {stats['total_patterns']}")
    print(f"  By modality: {stats['by_modality']}")
    
    # Replay some memories
    if stats['total_patterns'] > 0:
        memory.replay_memory(count=5)
    
    # Demo store
    print("\n[SensoryMemory] Storing demo pattern...")
    features = {
        'edge_complexity': 0.8,
        'texture_variance': 0.7,
        'triggered_actions': ['alert']
    }
    hotspots = [[i, i, i, 1] for i in range(10)]
    memory.store_pattern('vision', features, hotspots)
    
    print(f"[SensoryMemory] Now {len(memory.patterns)} patterns stored")

if __name__ == "__main__":
    main()
