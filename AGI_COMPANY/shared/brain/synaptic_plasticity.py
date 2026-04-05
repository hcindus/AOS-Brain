"""
Synaptic Plasticity Module
Phase 1 of AOS Brain Evolution

Implements Hebbian learning and homeostatic decay
for self-modifying neural connections.
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SynapticWeight:
    """Represents a modifiable synaptic connection"""
    pre_cell: Tuple[int, int, int]  # (x, y, z) source
    post_cell: Tuple[int, int, int]  # (x, y, z) target
    weight: float  # Connection strength
    last_activation: datetime
    activation_count: int
    
    # Hebbian learning parameters
    hebbian_rate: float = 0.01  # How fast to strengthen
    decay_rate: float = 0.995   # How fast to weaken when inactive
    
    def strengthen(self, amount: float = None):
        """Strengthen connection (Hebbian learning)"""
        if amount is None:
            amount = self.hebbian_rate
        self.weight = min(2.0, self.weight * (1 + amount))
        self.activation_count += 1
        self.last_activation = datetime.now()
    
    def decay(self):
        """Homeostatic decay for inactive connections"""
        time_inactive = datetime.now() - self.last_activation
        
        # Decay based on inactivity duration
        if time_inactive > timedelta(seconds=10):
            self.weight *= self.decay_rate
            
        # Keep minimum weight to prevent complete loss
        self.weight = max(0.1, self.weight)


class CorticalPlasticity:
    """
    Manages synaptic plasticity across the cortical sheet.
    
    Implements:
    - Hebbian strengthening: "Neurons that fire together, wire together"
    - Homeostatic decay: Inactive connections weaken
    - Activity-dependent modulation
    """
    
    def __init__(self, width: int = 64, height: int = 64, depth: int = 16):
        self.width = width
        self.height = height
        self.depth = depth
        
        # Weight matrix: weights[x][y][z] for each cell
        self.weights = np.ones((width, height, depth), dtype=np.float32)
        
        # Activity tracking
        self.activation_history = {}
        self.last_decay = datetime.now()
        
        # Learning parameters
        self.hebbian_rate = 0.05
        self.decay_interval = 5.0  # seconds
        self.decay_rate = 0.999
        
        # Synapse tracking for plastic connections
        self.synapses: Dict[Tuple, SynapticWeight] = {}
        
    def activate_cell(self, x: int, y: int, z: int, strength: float = 1.0):
        """
        Activate a cortical cell and strengthen its connections.
        
        Args:
            x, y, z: Cell coordinates
            strength: Activation strength (0.0 to 1.0)
        """
        # Ensure coordinates in bounds
        if not (0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth):
            return
            
        # Strengthen this cell's weight
        self.weights[x, y, z] = min(
            2.0, 
            self.weights[x, y, z] * (1 + self.hebbian_rate * strength)
        )
        
        # Strengthen nearby connections
        self._strengthen_neighbors(x, y, z, strength)
        
        # Track activation
        key = (x, y, z)
        self.activation_history[key] = datetime.now()
        
    def _strengthen_neighbors(self, x: int, y: int, z: int, strength: float):
        """Strengthen connections to neighboring cells"""
        # Local neighborhood
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == dy == dz == 0:
                        continue
                        
                    nx, ny, nz = x + dx, y + dy, z + dz
                    
                    # Check bounds
                    if (0 <= nx < self.width and 
                        0 <= ny < self.height and 
                        0 <= nz < self.depth):
                        
                        # Strengthen connection
                        self.weights[nx, ny, nz] = min(
                            2.0,
                            self.weights[nx, ny, nz] * (1 + self.hebbian_rate * strength * 0.5)
                        )
                        
                        # Track synapse
                        syn_key = ((x, y, z), (nx, ny, nz))
                        if syn_key not in self.synapses:
                            self.synapses[syn_key] = SynapticWeight(
                                pre_cell=(x, y, z),
                                post_cell=(nx, ny, nz),
                                weight=self.weights[nx, ny, nz],
                                last_activation=datetime.now(),
                                activation_count=1
                            )
                        else:
                            self.synapses[syn_key].strengthen(strength * 0.5)
    
    def apply_decay(self):
        """Apply homeostatic decay to inactive regions"""
        now = datetime.now()
        
        # Only decay periodically
        if (now - self.last_decay).total_seconds() < self.decay_interval:
            return
            
        self.last_decay = now
        
        # Decay weights for inactive cells
        for key, last_active in list(self.activation_history.items()):
            time_inactive = now - last_active
            
            if time_inactive > timedelta(seconds=30):
                x, y, z = key
                if (0 <= x < self.width and 
                    0 <= y < self.height and 
                    0 <= z < self.depth):
                    
                    # Decay weight
                    self.weights[x, y, z] = max(
                        0.1,
                        self.weights[x, y, z] * self.decay_rate
                    )
        
        # Decay synapses
        for syn_key, synapse in list(self.synapses.items()):
            synapse.decay()
            if synapse.weight < 0.15:  # Prune very weak synapses
                del self.synapses[syn_key]
                
    def get_weight(self, x: int, y: int, z: int) -> float:
        """Get current weight for a cell"""
        if (0 <= x < self.width and 
            0 <= y < self.height and 
            0 <= z < self.depth):
            return float(self.weights[x, y, z])
        return 1.0
        
    def modulate_wave(self, wave_amplitude: float, x: int, y: int, z: int) -> float:
        """
        Modulate wave amplitude based on synaptic weights.
        
        Frequently used pathways have stronger waves.
        """
        weight = self.get_weight(x, y, z)
        return wave_amplitude * weight
        
    def get_plasticity_stats(self) -> dict:
        """Get statistics about current plasticity state"""
        return {
            "mean_weight": float(np.mean(self.weights)),
            "max_weight": float(np.max(self.weights)),
            "min_weight": float(np.min(self.weights)),
            "active_synapses": len(self.synapses),
            "strong_connections": sum(1 for s in self.synapses.values() if s.weight > 1.5),
            "total_activations": sum(s.activation_count for s in self.synapses.values())
        }


class LearningEngine:
    """
    High-level learning interface for the brain.
    
    Connects plasticity to reward, novelty, and experience.
    """
    
    def __init__(self, plasticity: CorticalPlasticity):
        self.plasticity = plasticity
        self.learning_rate = 1.0
        self.experience_buffer = []
        
    def learn_from_experience(self, 
                              activation_pattern: list,
                              reward: float = 0.0,
                              novelty: float = 0.0):
        """
        Learn from an experience.
        
        Args:
            activation_pattern: List of (x, y, z) activated cells
            reward: Positive or negative reward (-1.0 to 1.0)
            novelty: How novel the experience was (0.0 to 1.0)
        """
        # Modulate learning rate by reward and novelty
        effective_rate = self.learning_rate * (1 + novelty) * (1 + abs(reward))
        
        # Strengthen activated pathways
        for x, y, z in activation_pattern:
            self.plasticity.activate_cell(x, y, z, strength=effective_rate)
            
        # If negative reward, weaken alternative pathways
        if reward < 0:
            self._weaken_alternatives(activation_pattern)
            
        # Store experience
        self.experience_buffer.append({
            "pattern": activation_pattern,
            "reward": reward,
            "novelty": novelty,
            "timestamp": datetime.now()
        })
        
        # Trim buffer
        if len(self.experience_buffer) > 1000:
            self.experience_buffer = self.experience_buffer[-500:]
            
    def _weaken_alternatives(self, activated_pattern: list):
        """Weaken pathways not used in successful outcome"""
        # Find nearby cells that weren't activated
        activated_set = set(activated_pattern)
        
        for x, y, z in activated_pattern:
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    for dz in [-2, -1, 0, 1, 2]:
                        nx, ny, nz = x + dx, y + dy, z + dz
                        
                        if (nx, ny, nz) not in activated_set:
                            # Decay this alternative pathway
                            if (0 <= nx < self.plasticity.width and
                                0 <= ny < self.plasticity.height and
                                0 <= nz < self.plasticity.depth):
                                self.plasticity.weights[nx, ny, nz] *= 0.98


# Integration with existing brain system
def create_plastic_cortical_sheet(width=64, height=64, depth=16):
    """Factory function to create plasticity-enabled cortex"""
    return CorticalPlasticity(width, height, depth)


def integrate_with_brain(brain_instance):
    """
    Integrate plasticity module with existing 7-region brain.
    
    This would be called during brain initialization to enable
    synaptic plasticity across the cortical sheet.
    """
    plasticity = CorticalPlasticity(
        width=brain_instance.width,
        height=brain_instance.height,
        depth=brain_instance.depth
    )
    
    learning_engine = LearningEngine(plasticity)
    
    # Attach to brain
    brain_instance.plasticity = plasticity
    brain_instance.learning = learning_engine
    
    return brain_instance


# Example usage and testing
if __name__ == "__main__":
    print("Synaptic Plasticity Module - Phase 1 of AOS Brain Evolution")
    print("=" * 60)
    
    # Create plastic cortex
    cortex = CorticalPlasticity(width=32, height=32, depth=8)
    
    # Simulate activity
    print("\nSimulating neural activity...")
    
    # Activate some cells
    for i in range(10):
        cortex.activate_cell(16, 16, 4, strength=0.8)
        cortex.activate_cell(16, 17, 4, strength=0.6)
        cortex.activate_cell(17, 16, 4, strength=0.6)
        
        # Apply decay
        cortex.apply_decay()
        
    # Show stats
    stats = cortex.get_plasticity_stats()
    print(f"\nPlasticity Statistics:")
    print(f"  Mean weight: {stats['mean_weight']:.3f}")
    print(f"  Max weight: {stats['max_weight']:.3f}")
    print(f"  Active synapses: {stats['active_synapses']}")
    print(f"  Strong connections: {stats['strong_connections']}")
    
    # Test learning engine
    print("\nTesting learning engine...")
    engine = LearningEngine(cortex)
    
    pattern = [(16, 16, 4), (16, 17, 4), (17, 16, 4)]
    engine.learn_from_experience(pattern, reward=0.8, novelty=0.5)
    
    print(f"  Experience learned with reward=0.8, novelty=0.5")
    
    final_stats = cortex.get_plasticity_stats()
    print(f"\nFinal Statistics:")
    print(f"  Total activations: {final_stats['total_activations']}")
    print(f"  Mean weight: {final_stats['mean_weight']:.3f}")
    
    print("\n" + "=" * 60)
    print("Synaptic Plasticity module ready for integration")
