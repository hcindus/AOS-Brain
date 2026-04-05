"""
Growth Laws Module
Implements the "growth laws" of the AOS brain - how it actually changes itself.

This module provides concrete, implementable algorithms for:
- Synaptic plasticity on cortical sheet
- Tracray self-organization
- Reward-based learning
- Memory palace optimization
- Developmental stages
- Curiosity-driven exploration

Based on research: Brain Evolution - From Mechanical to Living Intelligence
"""

import math
import random
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
import numpy as np


@dataclass
class GrowthConfig:
    """Configuration for brain growth parameters"""
    # Plasticity rates
    lr_up: float = 0.01          # Learning rate up (strengthening)
    lr_down: float = 0.001     # Learning rate down (decay)
    
    # Tracray organization
    attract_lr: float = 0.05     # Attraction learning rate
    repel_lr: float = 0.01     # Repulsion learning rate
    
    # Reward modulation
    reward_boost: float = 2.0    # How much reward boosts learning
    punishment_penalty: float = 0.5  # How much punishment reduces learning
    
    # Development stages
    infant_steps: int = 10_000
    child_steps: int = 100_000
    adolescent_steps: int = 1_000_000
    
    # Curiosity
    novelty_threshold: float = 0.7
    exploration_rate: float = 0.1


class TernaryCorticalSheet3D:
    """
    3D cortical sheet with ternary neurons (-1, 0, +1) and plastic weights.
    
    Each cell has:
    - state ∈ {-1, 0, +1}
    - weight ∈ ℝ (how easy it is to activate)
    """
    
    def __init__(self, nx: int = 64, ny: int = 64, nz: int = 16, config: Optional[GrowthConfig] = None):
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.size = nx * ny * nz
        
        self.config = config or GrowthConfig()
        
        # Initialize states and weights
        self.state = [0] * self.size  # -1, 0, +1
        self.weight = [0.5] * self.size  # Start neutral
        self.activation_count = [0] * self.size
        
        # Activation history for decay
        self.last_activation = [datetime.now()] * self.size
        
    def _idx(self, x: int, y: int, z: int) -> int:
        """Convert 3D coordinates to 1D index"""
        return x + y * self.nx + z * self.nx * self.ny
        
    def _coords(self, idx: int) -> Tuple[int, int, int]:
        """Convert 1D index to 3D coordinates"""
        z = idx // (self.nx * self.ny)
        remainder = idx % (self.nx * self.ny)
        y = remainder // self.nx
        x = remainder % self.nx
        return x, y, z
        
    def _neighbors(self, idx: int) -> List[int]:
        """Get neighboring cell indices"""
        x, y, z = self._coords(idx)
        neighbors = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == dy == dz == 0:
                        continue
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < self.nx and 0 <= ny < self.ny and 0 <= nz < self.nz:
                        neighbors.append(self._idx(nx, ny, nz))
                        
        return neighbors
        
    def _threshold(self, idx: int) -> float:
        """Calculate activation threshold based on weight"""
        base = 1.0
        # Higher weight = lower threshold (easier to activate)
        return max(0.1, base - 0.3 * (self.weight[idx] - 0.5))
        
    def step(self):
        """
        Execute one step of cortical dynamics with plasticity.
        """
        new_state = [0] * self.size
        
        for idx in range(self.size):
            neighbors = self._neighbors(idx)
            
            # Calculate excitation from neighbors
            excitation = sum(
                self.state[n] * self.weight[n] 
                for n in neighbors
            )
            
            # Apply threshold
            threshold = self._threshold(idx)
            
            if excitation > threshold:
                new_state[idx] = 1
                self.activation_count[idx] += 1
                self.last_activation[idx] = datetime.now()
            elif excitation < -threshold:
                new_state[idx] = -1
            else:
                new_state[idx] = 0
                
        # Update plasticity based on new states
        self._update_plasticity(new_state)
        
        self.state = new_state
        
    def _update_plasticity(self, new_state: List[int]):
        """
        Update synaptic weights based on activation.
        
        Hebbian learning: active cells strengthen
        Homeostatic decay: inactive cells weaken
        """
        for idx, v in enumerate(new_state):
            if v == 1:
                # Strengthen: move toward 1.0
                self.weight[idx] += self.config.lr_up * (1.0 - self.weight[idx])
            else:
                # Decay: move toward 0.1 (minimum)
                self.weight[idx] -= self.config.lr_down * (self.weight[idx] - 0.1)
                
        # Clamp weights
        for idx in range(self.size):
            self.weight[idx] = max(0.1, min(1.0, self.weight[idx]))
            
    def excite_region(self, x: int, y: int, z: int, radius: int = 2):
        """Excite a region of the sheet"""
        center_idx = self._idx(x, y, z)
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < self.nx and 0 <= ny < self.ny and 0 <= nz < self.nz:
                        idx = self._idx(nx, ny, nz)
                        self.state[idx] = 1
                        self.activation_count[idx] += 1
                        self.weight[idx] = min(1.0, self.weight[idx] + 0.05)
                        
    def get_active_regions(self) -> List[Tuple[int, int, int]]:
        """Get coordinates of currently active cells"""
        active = []
        for idx, s in enumerate(self.state):
            if s == 1:
                active.append(self._coords(idx))
        return active
        
    def get_stats(self) -> Dict:
        """Get plasticity statistics"""
        return {
            "mean_weight": sum(self.weight) / len(self.weight),
            "max_weight": max(self.weight),
            "min_weight": min(self.weight),
            "mean_activations": sum(self.activation_count) / len(self.activation_count),
            "total_active": sum(1 for s in self.state if s == 1),
        }


class TracrayOrganizer:
    """
    Self-organizing semantic map.
    
    Concepts move, cluster, and reorganize based on co-activation.
    """
    
    def __init__(self, tracray_lexicon: Dict, config: Optional[GrowthConfig] = None):
        self.tracray = tracray_lexicon
        self.config = config or GrowthConfig()
        
        # Track co-activation counts
        self.coactivation = defaultdict(lambda: defaultdict(int))
        
        # Concept visit counts (for familiarity)
        self.visit_count = defaultdict(int)
        
    def register_activation(self, active_concepts: List[str], valence: float = 0.0):
        """
        Register that concepts co-activated together.
        
        Args:
            active_concepts: List of concept names that were active
            valence: Emotional valence (-1.0 to 1.0)
        """
        # Update coactivation matrix
        for i in range(len(active_concepts)):
            for j in range(i + 1, len(active_concepts)):
                a, b = active_concepts[i], active_concepts[j]
                
                # Scale by valence magnitude
                boost = int(abs(valence) * 2) + 1
                self.coactivation[a][b] += boost
                self.coactivation[b][a] += boost
                
        # Update visit counts
        for concept in active_concepts:
            self.visit_count[concept] += 1
            
    def self_organize(self, steps: int = 1):
        """
        Move concepts based on co-activation patterns.
        
        - Frequently co-activating concepts pull together
        - Rarely co-activating concepts push apart
        """
        for _ in range(steps):
            for name, spec in self.tracray["concepts"].items():
                if "coord" not in spec:
                    continue
                    
                x, y, z = spec["coord"]
                fx = fy = fz = 0.0
                
                # Attraction to co-activated concepts
                for other, count in self.coactivation[name].items():
                    if count < 1 or other not in self.tracray["concepts"]:
                        continue
                        
                    ox, oy, oz = self.tracray["concepts"][other]["coord"]
                    dx, dy, dz = ox - x, oy - y, oz - z
                    dist = max(0.1, math.sqrt(dx*dx + dy*dy + dz*dz))
                    
                    # Stronger attraction for more co-activation
                    strength = self.config.attract_lr * (count / (1.0 + dist))
                    fx += strength * dx / dist
                    fy += strength * dy / dist
                    fz += strength * dz / dist
                    
                # Mild repulsion from all others
                for other, ospec in self.tracray["concepts"].items():
                    if other == name or "coord" not in ospec:
                        continue
                    ox, oy, oz = ospec["coord"]
                    dx, dy, dz = ox - x, oy - y, oz - z
                    dist2 = dx*dx + dy*dy + dz*dz
                    if dist2 < 1.0:
                        strength = self.config.repel_lr / max(0.1, dist2)
                        fx -= strength * dx
                        fy -= strength * dy
                        fz -= strength * dz
                        
                # Update position
                spec["coord"] = (x + fx, y + fy, z + fz)
                
    def curiosity_score(self, concept: str) -> float:
        """
        Calculate curiosity score for a concept.
        
        Higher score = more novel/less familiar = more curious.
        """
        v = self.visit_count[concept]
        if v == 0:
            return 1.0
        return 1.0 / (1.0 + math.log(1 + v))
        
    def pick_curiosity_target(self, top_k: int = 10) -> Optional[str]:
        """Pick a concept to explore based on curiosity"""
        scores = []
        for name in self.tracray["concepts"].keys():
            score = self.curiosity_score(name)
            scores.append((score, name))
            
        scores.sort(reverse=True)
        
        if not scores:
            return None
            
        # Pick from top-k with some randomness
        top = scores[:min(top_k, len(scores))]
        return random.choice(top)[1]
        
    def get_clustered_concepts(self, threshold: int = 5) -> List[List[str]]:
        """Get concepts clustered by co-activation"""
        clusters = []
        concepts = list(self.tracray["concepts"].keys())
        visited = set()
        
        for concept in concepts:
            if concept in visited:
                continue
                
            # BFS to find cluster
            cluster = []
            queue = [concept]
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                cluster.append(current)
                
                # Add strongly co-activated neighbors
                for other, count in self.coactivation[current].items():
                    if count >= threshold and other not in visited:
                        queue.append(other)
                        
            if cluster:
                clusters.append(cluster)
                
        return clusters


class RewardModulator:
    """
    Modulates learning based on reward/valence signals.
    
    Dopamine-like reinforcement learning.
    """
    
    def __init__(self, config: Optional[GrowthConfig] = None):
        self.config = config or GrowthConfig()
        self.valence_history = []
        
    def apply_reward_to_sheet(self, sheet: TernaryCorticalSheet3D, valence: float):
        """
        Modulate plasticity rates based on valence.
        
        Positive valence -> faster strengthening
        Negative valence -> faster decay
        """
        self.valence_history.append(valence)
        
        if valence > 0:
            # Positive: boost learning
            sheet.config.lr_up = self.config.lr_up * self.config.reward_boost
            sheet.config.lr_down = self.config.lr_down * 0.5
        elif valence < 0:
            # Negative: reduce learning, increase decay
            sheet.config.lr_up = self.config.lr_up * self.config.punishment_penalty
            sheet.config.lr_down = self.config.lr_down * 2.0
        else:
            # Neutral: reset to baseline
            sheet.config.lr_up = self.config.lr_up
            sheet.config.lr_down = self.config.lr_down
            
    def apply_reward_to_tracray(self, organizer: TracrayOrganizer, valence: float):
        """Modulate Tracray organization rates"""
        if valence > 0:
            organizer.config.attract_lr = self.config.attract_lr * self.config.reward_boost
            organizer.config.repel_lr = self.config.repel_lr * 0.5
        elif valence < 0:
            organizer.config.attract_lr = self.config.attract_lr * self.config.punishment_penalty
            organizer.config.repel_lr = self.config.repel_lr * 2.0
        else:
            organizer.config.attract_lr = self.config.attract_lr
            organizer.config.repel_lr = self.config.repel_lr
            
    def get_average_valence(self, window: int = 100) -> float:
        """Get average recent valence"""
        if not self.valence_history:
            return 0.0
        recent = self.valence_history[-window:]
        return sum(recent) / len(recent)


class BrainDevelopment:
    """
    Simulates developmental stages like a child growing up.
    """
    
    def __init__(self, config: Optional[GrowthConfig] = None):
        self.config = config or GrowthConfig()
        self.age_steps = 0
        
    def step(self):
        """Increment age"""
        self.age_steps += 1
        
    def get_stage(self) -> str:
        """Get current developmental stage"""
        if self.age_steps < self.config.infant_steps:
            return "infant"
        elif self.age_steps < self.config.child_steps:
            return "child"
        elif self.age_steps < self.config.adolescent_steps:
            return "adolescent"
        return "adult"
        
    def configure_brain(self, 
                        sheet: TernaryCorticalSheet3D, 
                        organizer: TracrayOrganizer,
                        modulator: RewardModulator):
        """
        Configure brain parameters based on developmental stage.
        
        Infant: Fast learning, high novelty
        Child: Moderate learning, exploration
        Adolescent: Balanced learning
        Adult: Conservative learning
        """
        stage = self.get_stage()
        
        if stage == "infant":
            # Rapid learning, high plasticity
            sheet.config.lr_up = 0.05
            sheet.config.lr_down = 0.0001
            organizer.config.attract_lr = 0.08
            organizer.config.repel_lr = 0.005
            modulator.config.reward_boost = 3.0
            
        elif stage == "child":
            # Moderate learning, exploration
            sheet.config.lr_up = 0.02
            sheet.config.lr_down = 0.0005
            organizer.config.attract_lr = 0.06
            organizer.config.repel_lr = 0.008
            modulator.config.reward_boost = 2.0
            
        elif stage == "adolescent":
            # Balanced learning
            sheet.config.lr_up = 0.01
            sheet.config.lr_down = 0.001
            organizer.config.attract_lr = 0.05
            organizer.config.repel_lr = 0.01
            modulator.config.reward_boost = 1.5
            
        else:  # adult
            # Conservative learning
            sheet.config.lr_up = 0.005
            sheet.config.lr_down = 0.002
            organizer.config.attract_lr = 0.03
            organizer.config.repel_lr = 0.015
            modulator.config.reward_boost = 1.2
            
        return stage
        
    def get_stats(self) -> Dict:
        """Get developmental statistics"""
        return {
            "age_steps": self.age_steps,
            "stage": self.get_stage(),
            "progress_to_next": self._progress_to_next(),
        }
        
    def _progress_to_next(self) -> float:
        """Get progress percentage to next stage"""
        if self.age_steps < self.config.infant_steps:
            return self.age_steps / self.config.infant_steps
        elif self.age_steps < self.config.child_steps:
            return (self.age_steps - self.config.infant_steps) / (self.config.child_steps - self.config.infant_steps)
        elif self.age_steps < self.config.adolescent_steps:
            return (self.age_steps - self.config.child_steps) / (self.config.adolescent_steps - self.config.child_steps)
        return 1.0


class CuriosityAgent:
    """
    Curiosity-driven exploration agent.
    
    Seeks novel, uncertain, or prediction-error-rich states.
    """
    
    def __init__(self, 
                 organizer: TracrayOrganizer,
                 sheet: TernaryCorticalSheet3D,
                 config: Optional[GrowthConfig] = None):
        self.organizer = organizer
        self.sheet = sheet
        self.config = config or GrowthConfig()
        
    def act(self) -> Optional[str]:
        """
        Execute curiosity-driven action.
        
        Returns: Name of concept explored, or None
        """
        # Pick curiosity target
        target_name = self.organizer.pick_curiosity_target(top_k=10)
        
        if not target_name:
            return None
            
        # Get coordinates
        if target_name not in self.organizer.tracray["concepts"]:
            return None
            
        spec = self.organizer.tracray["concepts"][target_name]
        if "coord" not in spec:
            return None
            
        x, y, z = spec["coord"]
        
        # Excite that region
        self.sheet.excite_region(int(x), int(y), int(z), radius=2)
        
        # Register as visited
        self.organizer.visit_count[target_name] += 1
        
        return target_name
        
    def should_explore(self, current_novelty: float) -> bool:
        """
        Decide whether to explore vs exploit.
        
        Higher novelty -> more likely to explore
        """
        threshold = self.config.novelty_threshold
        return current_novelty > threshold or random.random() < self.config.exploration_rate


class GrowingBrain:
    """
    Complete growing brain system.
    
    Integrates all growth laws into a unified system.
    """
    
    def __init__(self, 
                 tracray_lexicon: Optional[Dict] = None,
                 nx: int = 64, ny: int = 64, nz: int = 16):
        self.config = GrowthConfig()
        
        # Initialize components
        self.sheet = TernaryCorticalSheet3D(nx, ny, nz, self.config)
        
        if tracray_lexicon is None:
            tracray_lexicon = {"concepts": {}}
        self.organizer = TracrayOrganizer(tracray_lexicon, self.config)
        self.modulator = RewardModulator(self.config)
        self.development = BrainDevelopment(self.config)
        self.curiosity = CuriosityAgent(self.organizer, self.sheet, self.config)
        
        # Tracking
        self.tick_count = 0
        self.active_concepts_history = []
        
    def tick(self, valence: float = 0.0, active_concepts: Optional[List[str]] = None):
        """
        Execute one brain tick with growth.
        
        Args:
            valence: Emotional valence (-1.0 to 1.0)
            active_concepts: List of active concept names
        """
        self.tick_count += 1
        
        # Apply reward modulation
        self.modulator.apply_reward_to_sheet(self.sheet, valence)
        self.modulator.apply_reward_to_tracray(self.organizer, valence)
        
        # Step cortical sheet
        self.sheet.step()
        
        # Register concept activations
        if active_concepts:
            self.organizer.register_activation(active_concepts, valence)
            self.active_concepts_history.append((self.tick_count, active_concepts))
            
        # Periodic self-organization
        if self.tick_count % 100 == 0:
            self.organizer.self_organize(steps=1)
            
        # Developmental changes
        self.development.step()
        stage = self.development.configure_brain(
            self.sheet, self.organizer, self.modulator
        )
        
        # Curiosity-driven exploration when idle
        if self.tick_count % 50 == 0 and (not active_concepts or valence == 0):
            if self.curiosity.should_explore(novelty=0.8):
                self.curiosity.act()
                
    def get_status(self) -> Dict:
        """Get complete brain status"""
        return {
            "tick": self.tick_count,
            "stage": self.development.get_stage(),
            "cortical_stats": self.sheet.get_stats(),
            "development_stats": self.development.get_stats(),
            "avg_valence": self.modulator.get_average_valence(),
            "clusters": len(self.organizer.get_clustered_concepts()),
        }
        
    def simulate_growth(self, ticks: int = 1000):
        """Simulate brain growth over many ticks"""
        print(f"Simulating {ticks} ticks of brain growth...")
        
        for i in range(ticks):
            # Simulate varying valence
            valence = math.sin(i / 100) * 0.5  # Oscillating valence
            
            # Simulate random concept activations
            concepts = list(self.organizer.tracray["concepts"].keys())
            if concepts:
                active = random.sample(concepts, min(3, len(concepts)))
            else:
                active = []
                
            self.tick(valence=valence, active_concepts=active)
            
            if i % 100 == 0:
                status = self.get_status()
                print(f"  Tick {i}: Stage={status['stage']}, "
                      f"MeanWeight={status['cortical_stats']['mean_weight']:.3f}")
                      
        print(f"\nGrowth simulation complete after {ticks} ticks")
        print(f"Final stage: {self.development.get_stage()}")


# Example usage
if __name__ == "__main__":
    print("Growth Laws Module - Brain Evolution")
    print("=" * 50)
    
    # Create growing brain
    brain = GrowingBrain(nx=32, ny=32, nz=8)
    
    # Add some initial concepts
    brain.organizer.tracray["concepts"] = {
        "milk": {"coord": (16, 16, 4)},
        "dairy": {"coord": (16, 20, 4)},
        "cheese": {"coord": (20, 16, 4)},
        "farm": {"coord": (24, 24, 4)},
    }
    
    # Simulate growth
    brain.simulate_growth(ticks=500)
    
    # Final status
    print("\nFinal Brain Status:")
    for key, value in brain.get_status().items():
        print(f"  {key}: {value}")
        
    print("\n" + "=" * 50)
    print("Growth laws module ready for integration")
