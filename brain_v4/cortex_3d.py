#!/usr/bin/env python3
"""
3D Cortex - Multi-Dimensional Neural Processing
Ported from legacy brain architecture
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque


@dataclass
class CortexLayer:
    """3D neural layer"""
    x: int  # Spatial X
    y: int  # Spatial Y
    z: int  # Depth/Abstraction
    activation: np.ndarray
    connections: List[Tuple[int, int, int]]  # Connected coordinates


class Cortex3D:
    """
    3D Cortex for multi-dimensional neural processing
    
    Dimensions:
    - X: Input space (sensory/observation)
    - Y: Processing space (pattern recognition)
    - Z: Abstraction depth (consciousness level)
    
    Layer 0 (Z=0): Raw sensory input (Conscious)
    Layer 1 (Z=1): Pattern recognition (Subconscious)  
    Layer 2 (Z=2): Deep abstraction (Unconscious)
    """
    
    def __init__(self, width: int = 64, height: int = 64, depth: int = 3):
        self.width = width
        self.height = height
        self.depth = depth
        
        # 3D neural volume
        self.volume = np.zeros((depth, height, width), dtype=np.float32)
        
        # Layer activations
        self.conscious = self.volume[0]  # Z=0
        self.subconscious = self.volume[1]  # Z=1
        self.unconscious = self.volume[2]  # Z=2
        
        # Processing history
        self.activation_history = deque(maxlen=100)
        
        # Weights for inter-layer propagation
        self.conscious_weights = np.random.randn(height, width) * 0.1
        self.subconscious_weights = np.random.randn(height, width) * 0.1
        self.unconscious_weights = np.random.randn(height, width) * 0.1
        
        print(f"[3DCortex] Initialized {depth}x{height}x{width} neural volume")
    
    def activate(self, input_vector: np.ndarray, layer: str = "conscious") -> np.ndarray:
        """Activate a specific layer"""
        layer_idx = {"conscious": 0, "subconscious": 1, "unconscious": 2}.get(layer, 0)
        
        # Reshape input to match layer dimensions
        if len(input_vector) != self.width * self.height:
            input_vector = np.resize(input_vector, self.width * self.height)
        
        input_2d = input_vector.reshape(self.height, self.width)
        
        # Apply activation with sigmoid
        activated = 1 / (1 + np.exp(-input_2d))
        
        self.volume[layer_idx] = activated
        self.activation_history.append({
            "layer": layer,
            "mean_activation": float(np.mean(activated)),
            "max_activation": float(np.max(activated))
        })
        
        return activated
    
    def propagate_down(self, from_layer: str = "conscious") -> Dict[str, np.ndarray]:
        """Propagate activation from conscious -> subconscious -> unconscious"""
        results = {}
        
        if from_layer == "conscious":
            # Conscious -> Subconscious
            propagated = np.tanh(self.conscious * self.conscious_weights)
            self.subconscious = (self.subconscious * 0.7 + propagated * 0.3)
            results["subconscious"] = self.subconscious.copy()
            
            # Subconscious -> Unconscious
            propagated = np.tanh(self.subconscious * self.subconscious_weights)
            self.unconscious = (self.unconscious * 0.9 + propagated * 0.1)
            results["unconscious"] = self.unconscious.copy()
            
        elif from_layer == "subconscious":
            propagated = np.tanh(self.subconscious * self.subconscious_weights)
            self.unconscious = (self.unconscious * 0.9 + propagated * 0.1)
            results["unconscious"] = self.unconscious.copy()
        
        return results
    
    def propagate_up(self, from_layer: str = "unconscious") -> Dict[str, np.ndarray]:
        """Propagate activation from unconscious -> subconscious -> conscious (intuition)"""
        results = {}
        
        if from_layer == "unconscious":
            # Unconscious patterns bubble up
            propagated = np.tanh(self.unconscious * self.unconscious_weights)
            self.subconscious = np.maximum(self.subconscious, propagated * 0.3)
            results["subconscious"] = self.subconscious.copy()
            
            # Subconscious patterns to conscious
            propagated = np.tanh(self.subconscious * self.subconscious_weights)
            self.conscious = np.maximum(self.conscious, propagated * 0.2)
            results["conscious"] = self.conscious.copy()
        
        return results
    
    def get_activation_pattern(self, layer: str = "conscious") -> np.ndarray:
        """Get current activation pattern"""
        layer_idx = {"conscious": 0, "subconscious": 1, "unconscious": 2}.get(layer, 0)
        return self.volume[layer_idx].copy()
    
    def detect_patterns(self, layer: str = "subconscious") -> List[Dict]:
        """Detect emerging patterns in a layer"""
        layer_idx = {"conscious": 0, "subconscious": 1, "unconscious": 2}.get(layer, 1)
        activations = self.volume[layer_idx]
        
        # Find high-activation regions
        threshold = np.mean(activations) + np.std(activations)
        high_activation = activations > threshold
        
        patterns = []
        for i in range(self.height):
            for j in range(self.width):
                if high_activation[i, j]:
                    patterns.append({
                        "x": j,
                        "y": i,
                        "activation": float(activations[i, j]),
                        "significance": float(activations[i, j] / threshold)
                    })
        
        # Sort by activation
        patterns.sort(key=lambda x: x["activation"], reverse=True)
        return patterns[:10]  # Top 10 patterns
    
    def get_stats(self) -> Dict:
        """Get cortex statistics"""
        return {
            "conscious_mean": float(np.mean(self.conscious)),
            "conscious_max": float(np.max(self.conscious)),
            "subconscious_mean": float(np.mean(self.subconscious)),
            "unconscious_mean": float(np.mean(self.unconscious)),
            "volume_size": self.depth * self.height * self.width,
            "history_length": len(self.activation_history)
        }


if __name__ == "__main__":
    print("=" * 70)
    print("  3D CORTEX TEST")
    print("=" * 70)
    
    cortex = Cortex3D(width=32, height=32, depth=3)
    
    # Test activation
    test_input = np.random.randn(1024)
    cortex.activate(test_input, "conscious")
    
    # Propagate down
    print("\n[Propagation] Conscious -> Subconscious -> Unconscious")
    results = cortex.propagate_down("conscious")
    print(f"  Subconscious mean: {np.mean(results['subconscious']):.3f}")
    print(f"  Unconscious mean: {np.mean(results['unconscious']):.3f}")
    
    # Detect patterns
    print("\n[Pattern Detection]")
    patterns = cortex.detect_patterns("subconscious")
    print(f"  Found {len(patterns)} significant patterns")
    if patterns:
        print(f"  Top: activation={patterns[0]['activation']:.3f} at ({patterns[0]['x']}, {patterns[0]['y']})")
    
    print("\n" + "=" * 70)
