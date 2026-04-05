# core/cortical_sheet.py
"""
3D Ternary Cortical Sheet with wave propagation, Hebbian learning, and gating.
"""

import numpy as np
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class SheetSummary:
    """Summary of cortical sheet state."""
    pos_count: int = 0
    neg_count: int = 0
    zero_count: int = 0
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    energy: float = 0.0
    coherence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pos_count": self.pos_count,
            "neg_count": self.neg_count,
            "zero_count": self.zero_count,
            "center": list(self.center),
            "energy": self.energy,
            "coherence": self.coherence,
        }


class TernaryCorticalSheet3D:
    """
    3D grid of ternary neurons (-1, 0, +1).
    
    Features:
    - Wave propagation through local connectivity
    - Hebbian weight learning
    - Ternary gating (+1/0/-1) for attention control
    - Coherence measurement
    """
    
    # 6-neighbor connectivity (von Neumann neighborhood)
    NEIGHBORS = [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    ]
    
    def __init__(self, nx: int = 12, ny: int = 12, nz: int = 6):
        """
        Initialize 3D cortical sheet.
        
        Args:
            nx, ny, nz: Dimensions of the sheet
        """
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.size = nx * ny * nz
        
        # Initialize states and weights
        self.state = np.zeros((nx, ny, nz), dtype=np.int8)
        self.next_state = np.zeros((nx, ny, nz), dtype=np.int8)
        self.weight = np.ones((nx, ny, nz), dtype=np.float32)
        
        # Activity history for coherence
        self.history = []
        self.max_history = 10
    
    def excite_region(self, cx: int, cy: int, cz: int, radius: int, value: int = 1):
        """Excite a spherical region to given value."""
        for x in range(max(0, cx - radius), min(self.nx, cx + radius + 1)):
            for y in range(max(0, cy - radius), min(self.ny, cy + radius + 1)):
                for z in range(max(0, cz - radius), min(self.nz, cz + radius + 1)):
                    dx, dy, dz = x - cx, y - cy, z - cz
                    if dx*dx + dy*dy + dz*dz <= radius*radius:
                        self.state[x, y, z] = value
    
    def inhibit_region(self, cx: int, cy: int, cz: int, radius: int):
        """Inhibit (set to -1) a spherical region."""
        self.excite_region(cx, cy, cz, radius, -1)
    
    def clear_region(self, cx: int, cy: int, cz: int, radius: int):
        """Clear (set to 0) a spherical region."""
        self.excite_region(cx, cy, cz, radius, 0)
    
    def step_wave(self, decay: float = 0.9):
        """
        Propagate waves through the sheet.
        
        Each cell updates based on:
        - Self contribution (weighted)
        - Neighbor contributions
        - Decay factor
        """
        for x in range(self.nx):
            for y in range(self.ny):
                for z in range(self.nz):
                    # Self contribution with weight
                    idx = (x, y, z)
                    s = self.weight[idx] * self.state[idx]
                    
                    # Neighbor contributions
                    for dx, dy, dz in self.NEIGHBORS:
                        nx, ny_, nz_ = x + dx, y + dy, z + dz
                        if 0 <= nx < self.nx and 0 <= ny_ < self.ny and 0 <= nz_ < self.nz:
                            s += 0.5 * self.state[nx, ny_, nz_]
                    
                    # Apply decay
                    s *= decay
                    
                    # Ternary activation
                    if s > 0.3:
                        self.next_state[idx] = 1
                    elif s < -0.3:
                        self.next_state[idx] = -1
                    else:
                        self.next_state[idx] = 0
        
        # Swap states
        self.state, self.next_state = self.next_state, self.state
        
        # Update history
        self.history.append(self.state.copy())
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def step_wave_gated(self, gate_state: int, decay_pos: float = 0.95, decay_neutral: float = 0.85):
        """
        Gated wave propagation.
        
        Args:
            gate_state: +1 (facilitate), 0 (normal), -1 (suppress)
        """
        if gate_state == -1:
            # Full suppression
            self.state.fill(0)
            return
        
        decay = decay_pos if gate_state == 1 else decay_neutral
        self.step_wave(decay)
    
    def hebbian_update(self, eta: float = 0.01):
        """
        Hebbian learning: strengthen weights for active neurons.
        
        "Neurons that fire together, wire together"
        """
        active_mask = self.state != 0
        self.weight[active_mask] += eta * self.state[active_mask]
        
        # Clamp weights
        self.weight = np.clip(self.weight, -5.0, 5.0)
    
    def consolidate(self):
        """Strengthen persistent patterns (memory consolidation)."""
        active_mask = self.state != 0
        self.weight[active_mask] *= 1.05
        self.weight = np.clip(self.weight, -10.0, 10.0)
    
    def summarize(self) -> SheetSummary:
        """Generate summary statistics."""
        s = SheetSummary()
        
        s.pos_count = int(np.sum(self.state == 1))
        s.neg_count = int(np.sum(self.state == -1))
        s.zero_count = int(np.sum(self.state == 0))
        
        # Center of mass for positive activations
        pos_indices = np.argwhere(self.state == 1)
        if len(pos_indices) > 0:
            s.center = tuple(pos_indices.mean(axis=0))
        
        # Total energy
        s.energy = float(np.sum(np.abs(self.state)))
        
        # Coherence (how synchronized)
        s.coherence = self._calculate_coherence()
        
        return s
    
    def _calculate_coherence(self) -> float:
        """Calculate coherence (synchronization) of the sheet."""
        if len(self.history) < 2:
            return 0.0
        
        # Compare current state to previous
        prev = self.history[-2] if len(self.history) >= 2 else self.state
        similarity = np.mean(self.state == prev)
        return float(similarity)
    
    def seed_from_concept(self, coord: Tuple[int, int, int], intensity: float = 1.0):
        """Seed activity at a concept's coordinate."""
        x, y, z = coord
        radius = int(2 * intensity)
        self.excite_region(x, y, z, radius, 1)
    
    def get_active_regions(self) -> list:
        """Get list of active (non-zero) coordinates."""
        return [(int(x), int(y), int(z)) 
                for x, y, z in np.argwhere(self.state != 0)]
