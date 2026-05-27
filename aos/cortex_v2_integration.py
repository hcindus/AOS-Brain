#!/usr/bin/env python3
"""
CORTEX v2.0 INTEGRATION - Drop-in replacement for Cortex3D
Adds temporal reasoning, sparse activation, and LLM-compatible state export
"""

import sys
sys.path.insert(0, '/root/.aos/aos')

import numpy as np
from typing import Dict, List, Tuple, Optional
from cortex_v2_sparse import TernarySparseCortex


class CortexV2Integration:
    """
    Wrapper that provides Cortex3D-compatible API while using sparse v2 internals
    
    Maintains backward compatibility with:
    - Cortex3D.activate()
    - Cortex3D.propagate_down()
    - Cortex3D.propagate_up()
    - Cortex3D.detect_patterns()
    - Cortex3D.get_stats()
    
    Adds new capabilities:
    - Temporal memory (chain-of-thought)
    - Associative links (pattern completion)
    - Parallel regions (async processing)
    - LLM state export (for system prompts)
    """
    
    def __init__(self, width: int = 32, height: int = 32, depth: int = 32, use_v2: bool = True):
        self.width = width
        self.height = height
        self.depth = depth
        self.use_v2 = use_v2
        
        if use_v2 and width == height == depth == 32:
            print("[Cortex] Using v2.0 sparse temporal implementation")
            self._cortex = TernarySparseCortex(size=32, temporal_depth=64, max_hotspots=512)
            self._is_v2 = True
        else:
            print(f"[Cortex] Using legacy v1 implementation ({width}x{height}x{depth})")
            from cortex_3d import Cortex3D
            self._cortex = Cortex3D(width=width, height=height, depth=depth)
            self._is_v2 = False
    
    def activate(self, input_vector: np.ndarray, layer: str = "conscious") -> np.ndarray:
        """
        Compatible API: Activate a layer from embedding vector
        
        In v2: Converts vector to sparse ternary hotspots
        In v1: Direct dense activation
        """
        if self._is_v2:
            # Convert embedding to sparse ternary activations
            hotspots = self._cortex.embed_to_hotspots(input_vector, n_hotspots=64)
            self._cortex.activate_sparse(hotspots, source=layer)
            
            # Return activation map for compatibility
            return self._get_activation_map()
        else:
            return self._cortex.activate(input_vector, layer)
    
    def _get_activation_map(self) -> np.ndarray:
        """Get current activation as numpy array (for v1 compatibility)"""
        if not self._is_v2:
            return self._cortex.conscious
        
        # Build 32x32 array from sparse state
        # Z=0 (conscious), Z=1 (subconscious), Z=2 (unconscious)
        activation = np.zeros((self.depth, self.height, self.width), dtype=np.float32)
        
        for (x, y, z), enc in self._cortex.active_nodes.items():
            val = self._cortex.decode_ternary(enc)
            if 0 <= z < self.depth and 0 <= y < self.height and 0 <= x < self.width:
                activation[z, y, x] = val
        
        return activation
    
    def propagate_down(self, from_layer: str = "conscious") -> Dict[str, np.ndarray]:
        """
        Compatible API: Propagate from conscious -> subconscious -> unconscious
        
        In v2: Runs tick with associative link propagation
        In v1: Dense propagation with weights
        """
        if self._is_v2:
            # v2: Run a tick which includes propagation
            result = self._cortex.tick_parallel(use_links=True, use_temporal=True)
            
            # Return layer maps for compatibility
            activation = self._get_activation_map()
            return {
                "subconscious": activation[1],
                "unconscious": activation[2]
            }
        else:
            return self._cortex.propagate_down(from_layer)
    
    def propagate_up(self, from_layer: str = "unconscious") -> Dict[str, np.ndarray]:
        """
        Compatible API: Propagate from unconscious -> subconscious -> conscious
        
        In v2: Query temporal memory and prime related patterns
        In v1: Dense propagation with weights
        """
        if self._is_v2:
            # v2: Use associative links to prime upward
            link_activations = self._cortex.propagate_associative(max_propagations=100)
            
            # Apply the primed activations
            if link_activations:
                hotspots = [
                    (x, y, z, val) for (x, y, z), val in link_activations.items()
                ]
                self._cortex.activate_sparse(hotspots, source="associative_prime")
            
            activation = self._get_activation_map()
            return {
                "subconscious": activation[1],
                "conscious": activation[0]
            }
        else:
            return self._cortex.propagate_up(from_layer)
    
    def get_activation_pattern(self, layer: str = "conscious") -> np.ndarray:
        """Compatible API: Get activation pattern for a layer"""
        if self._is_v2:
            activation = self._get_activation_map()
            layer_idx = {"conscious": 0, "subconscious": 1, "unconscious": 2}.get(layer, 0)
            return activation[layer_idx]
        else:
            return self._cortex.get_activation_pattern(layer)
    
    def detect_patterns(self, layer: str = "subconscious") -> List[Dict]:
        """
        Compatible API: Detect patterns in a layer
        
        In v2: Returns hotspot regions as patterns
        In v1: Threshold-based detection
        """
        if self._is_v2:
            patterns = []
            z_target = {"conscious": 0, "subconscious": 1, "unconscious": 2}.get(layer, 1)
            
            for coord, hotspot in self._cortex.hotspots.items():
                if hotspot.z // (self.depth // 3) == z_target // (self.depth // 3):
                    patterns.append({
                        "x": hotspot.x,
                        "y": hotspot.y,
                        "z": hotspot.z,
                        "activation": float(hotspot.to_ternary()),
                        "significance": 1.0 - (hotspot.age / 100.0)
                    })
            
            # Sort by significance
            patterns.sort(key=lambda p: p["significance"], reverse=True)
            return patterns[:10]
        else:
            return self._cortex.detect_patterns(layer)
    
    def get_stats(self) -> Dict:
        """Compatible API: Get statistics"""
        if self._is_v2:
            v2_stats = self._cortex.get_stats()
            activation = self._get_activation_map()
            return {
                "conscious_mean": float(np.mean(np.abs(activation[0]))),
                "conscious_max": float(np.max(np.abs(activation[0]))),
                "subconscious_mean": float(np.mean(np.abs(activation[1]))),
                "unconscious_mean": float(np.mean(np.abs(activation[2]))),
                "volume_size": self.depth * self.height * self.width,
                "history_length": v2_stats["temporal_frames"],
                "v2_stats": v2_stats  # Extended stats
            }
        else:
            return self._cortex.get_stats()
    
    # === NEW v2 METHODS (not in v1 API) ===
    
    def chain_of_thought(self, steps: int = 3) -> List[Dict]:
        """
        NEW: Traverse temporal memory for reasoning chain
        
        Returns sequence of how cortical state evolved
        """
        if not self._is_v2:
            return []
        
        # Get current hotspots as initial pattern
        initial = list(self._cortex.hotspots.keys())[:10]
        return self._cortex.chain_of_thought(initial, steps=steps)
    
    def query_temporal(self, pattern_hash: Optional[str] = None, ticks_back: int = 10) -> List[Dict]:
        """
        NEW: Query temporal buffer for past states
        
        Returns list of past cortical snapshots
        """
        if not self._is_v2:
            return []
        
        frames = self._cortex.query_temporal(pattern_hash, ticks_back)
        return [{
            "tick": f.tick,
            "coherence": f.coherence,
            "pattern_hash": f.dominant_pattern,
            "hotspot_count": len(f.hotspots)
        } for f in frames]
    
    def get_llm_state(self) -> str:
        """
        NEW: Export current state for LLM system prompt
        
        This is the key bridge: cortex -> LLM context
        """
        if not self._is_v2:
            return "[Legacy cortex: no temporal state]"
        
        return self._cortex.get_state_for_prompt()
    
    def tick(self) -> Dict:
        """
        NEW: Manual tick for standalone operation
        
        Returns tick summary
        """
        if not self._is_v2:
            return {"error": "tick() only available in v2"}
        
        return self._cortex.tick_parallel(use_links=True, use_temporal=True)
    
    # === Properties for v1 compatibility ===
    
    @property
    def conscious(self):
        """Access conscious layer (v1 compatibility)"""
        if self._is_v2:
            return self._get_activation_map()[0]
        return self._cortex.conscious
    
    @property
    def subconscious(self):
        """Access subconscious layer (v1 compatibility)"""
        if self._is_v2:
            return self._get_activation_map()[1]
        return self._cortex.subconscious
    
    @property
    def unconscious(self):
        """Access unconscious layer (v1 compatibility)"""
        if self._is_v2:
            return self._get_activation_map()[2]
        return self._cortex.unconscious
    
    @property
    def volume(self):
        """Access full volume (v1 compatibility)"""
        return self._get_activation_map()


# === INTEGRATION WITH COMPLETE BRAIN v4.5 ===

def patch_brain_v45(use_v2_cortex: bool = True):
    """
    Monkey-patch CompleteBrainV44 to use Cortex v2
    
    Call this before creating brain instance:
        from cortex_v2_integration import patch_brain_v45
        patch_brain_v45(use_v2_cortex=True)
        brain = CompleteBrainV44()
    """
    import complete_brain_v45
    from cortex_v2_integration import CortexV2Integration
    
    # Store original
    complete_brain_v45._original_Cortex3D = complete_brain_v45.Cortex3D
    
    # Create wrapper class that looks like Cortex3D but uses v2
    class Cortex3DV2Wrapper:
        def __init__(self, width=32, height=32, depth=32):
            self._impl = CortexV2Integration(width, height, depth, use_v2=use_v2_cortex)
            
            # Mirror properties
            self.width = width
            self.height = height
            self.depth = depth
        
        def __getattr__(self, name):
            return getattr(self._impl, name)
    
    # Patch
    complete_brain_v45.Cortex3D = Cortex3DV2Wrapper
    print(f"[CortexV2] Patched CompleteBrain v4.5 with {'v2.0' if use_v2_cortex else 'v1.0'}")


if __name__ == "__main__":
    print("=" * 70)
    print("  CORTEX v2.0 INTEGRATION TEST")
    print("=" * 70)
    
    # Test v2 with compatible API
    print("\n[Test] Creating v2.0 cortex with v1-compatible API")
    cortex = CortexV2Integration(width=32, height=32, depth=32, use_v2=True)
    
    # Test activation
    print("\n[Test] Activation from embedding")
    test_emb = np.random.randn(256)
    test_emb[:50] = 2.0  # Strong signal
    cortex.activate(test_emb, "conscious")
    print(f"  Stats: {cortex.get_stats()['v2_stats']}")
    
    # Test propagation
    print("\n[Test] Propagation (5 ticks)")
    for i in range(5):
        result = cortex.tick()
    print(f"  Final: {result}")
    
    # Test chain of thought
    print("\n[Test] Chain of thought")
    chain = cortex.chain_of_thought(steps=3)
    for step in chain:
        print(f"  {step}")
    
    # Test LLM state
    print("\n[Test] LLM state export")
    print(cortex.get_llm_state())
    
    # Test v1 compatibility
    print("\n[Test] v1 API compatibility")
    print(f"  conscious shape: {cortex.conscious.shape}")
    print(f"  subconscious shape: {cortex.subconscious.shape}")
    print(f"  volume shape: {cortex.volume.shape}")
    
    print("\n" + "=" * 70)
    print("  SUCCESS: v2.0 cortex with v1-compatible API")
    print("=" * 70)