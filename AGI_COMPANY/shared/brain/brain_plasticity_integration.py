"""
Synaptic Plasticity Integration Module
Connects Phase 1 plasticity to existing AOS Brain

This module bridges the new plasticity system with the
existing 7-region brain, enabling learning in real-time.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add shared brain to path
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/shared/brain')

try:
    from synaptic_plasticity import CorticalPlasticity, LearningEngine
except ImportError:
    print("Synaptic plasticity module not yet available")
    CorticalPlasticity = None
    LearningEngine = None


class BrainPlasticityBridge:
    """
    Bridges synaptic plasticity with the existing AOS brain.
    
    Monitors brain activity and applies plasticity updates.
    """
    
    def __init__(self, brain_state_path: str = "~/.aos/brain/state/brain_state.json"):
        self.brain_state_path = Path(brain_state_path).expanduser()
        
        # Initialize plasticity (64x64x16 default)
        if CorticalPlasticity:
            self.plasticity = CorticalPlasticity(width=64, height=64, depth=16)
            self.learning = LearningEngine(self.plasticity)
        else:
            self.plasticity = None
            self.learning = None
            
        # Track which regions are active
        self.active_regions = {}
        self.tick_count = 0
        
    def load_brain_state(self) -> Optional[Dict]:
        """Load current brain state from file"""
        try:
            if self.brain_state_path.exists():
                with open(self.brain_state_path) as f:
                    return json.load(f)
        except Exception as e:
            print(f"Could not load brain state: {e}")
        return None
        
    def map_region_to_coordinates(self, region: str, intensity: float) -> List[Tuple]:
        """
        Map brain regions to cortical coordinates.
        
        Regions and their approximate coordinates:
        - Thalamus: (32, 32, 8) - center
        - Hippocampus: (20, 20, 6) - memory
        - Limbic: (44, 20, 6) - emotion
        - PFC: (32, 44, 10) - planning
        - Basal: (32, 20, 4) - action
        - Cerebellum: (20, 44, 4) - coordination
        - Brainstem: (32, 32, 2) - regulation
        """
        region_coords = {
            "Thalamus": [(32, 32, 8)],
            "Hippocampus": [(20, 20, 6), (22, 22, 6)],
            "Limbic": [(44, 20, 6), (46, 22, 6)],
            "PFC": [(32, 44, 10), (34, 46, 10)],
            "Basal": [(32, 20, 4), (34, 22, 4)],
            "Cerebellum": [(20, 44, 4), (22, 46, 4)],
            "Brainstem": [(32, 32, 2), (34, 34, 2)],
        }
        
        # Get coordinates for region
        coords = region_coords.get(region, [(32, 32, 8)])
        
        # Spread activation based on intensity
        if intensity > 0.7:
            # Add surrounding cells
            spread = []
            for x, y, z in coords:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        for dz in [-1, 0, 1]:
                            spread.append((x+dx, y+dy, z+dz))
            coords = spread[:20]  # Limit spread
            
        return coords
        
    def process_tick(self):
        """
        Process one brain tick with plasticity.
        
        Called every tick to update synaptic weights
        based on current brain activity.
        """
        if not self.plasticity:
            return
            
        self.tick_count += 1
        
        # Load current state
        state = self.load_brain_state()
        if not state:
            return
            
        # Get active phase
        phase = state.get("phase", "Process")
        
        # Map phases to region activation
        phase_regions = {
            "Observe": ["Thalamus", "Hippocampus"],
            "Orient": ["Limbic", "PFC"],
            "Decide": ["PFC", "Basal"],
            "Act": ["Basal", "Cerebellum"],
            "Process": ["Thalamus", "Brainstem"],
        }
        
        active = phase_regions.get(phase, ["Thalamus"])
        
        # Activate plasticity for active regions
        for region in active:
            coords = self.map_region_to_coordinates(region, intensity=0.8)
            for x, y, z in coords:
                self.plasticity.activate_cell(x, y, z, strength=0.5)
                
        # Apply decay periodically
        if self.tick_count % 10 == 0:
            self.plasticity.apply_decay()
            
        # Get stats
        if self.tick_count % 100 == 0:
            stats = self.plasticity.get_plasticity_stats()
            self._log_plasticity_stats(stats)
            
    def _log_plasticity_stats(self, stats: Dict):
        """Log plasticity statistics"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tick": self.tick_count,
            "mean_weight": stats["mean_weight"],
            "max_weight": stats["max_weight"],
            "active_synapses": stats["active_synapses"],
            "strong_connections": stats["strong_connections"],
        }
        
        # Append to log
        log_path = Path("~/.aos/brain/logs/plasticity.log").expanduser()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
            
    def learn_from_outcome(self, 
                          pattern: List[str],
                          reward: float = 0.0,
                          novelty: float = 0.0):
        """
        Learn from an experience outcome.
        
        Args:
            pattern: List of regions activated
            reward: -1.0 to 1.0 (negative to positive)
            novelty: 0.0 to 1.0 (how new the experience)
        """
        if not self.learning:
            return
            
        # Convert region names to coordinates
        coord_pattern = []
        for region in pattern:
            coords = self.map_region_to_coordinates(region, intensity=0.8)
            coord_pattern.extend(coords)
            
        # Learn
        self.learning.learn_from_experience(
            coord_pattern,
            reward=reward,
            novelty=novelty
        )
        
    def get_plasticity_report(self) -> Dict:
        """Get current plasticity status for reporting"""
        if not self.plasticity:
            return {"status": "not_initialized"}
            
        stats = self.plasticity.get_plasticity_stats()
        
        return {
            "tick": self.tick_count,
            "mean_weight": round(stats["mean_weight"], 3),
            "max_weight": round(stats["max_weight"], 3),
            "active_synapses": stats["active_synapses"],
            "strong_connections": stats["strong_connections"],
            "total_activations": stats["total_activations"],
            "status": "active" if self.tick_count > 0 else "initializing"
        }


# Integration hook for existing brain loop
def integrate_plasticity_with_brain(brain_instance=None):
    """
    Main integration function.
    
    Call this during brain initialization to enable plasticity.
    
    Example:
        from brain_plasticity_integration import integrate_plasticity_with_brain
        
        # In your brain initialization
        brain = SevenRegionBrain()
        plasticity_bridge = integrate_plasticity_with_brain(brain)
        
        # In your tick loop
        while True:
            brain.tick()
            plasticity_bridge.process_tick()
    """
    bridge = BrainPlasticityBridge()
    
    # If brain instance provided, attach bridge
    if brain_instance:
        brain_instance.plasticity_bridge = bridge
        
    return bridge


# Standalone test
if __name__ == "__main__":
    print("Brain Plasticity Integration Module")
    print("=" * 50)
    
    # Create bridge
    bridge = BrainPlasticityBridge()
    
    # Simulate ticks
    print("\nSimulating 50 brain ticks...")
    for i in range(50):
        bridge.process_tick()
        
        # Occasionally learn from outcomes
        if i % 10 == 0:
            bridge.learn_from_outcome(
                pattern=["Thalamus", "PFC"],
                reward=0.5,
                novelty=0.3
            )
            
    # Report
    report = bridge.get_plasticity_report()
    print("\nPlasticity Report:")
    for key, value in report.items():
        print(f"  {key}: {value}")
        
    print("\n" + "=" * 50)
    print("Integration module ready")
    print("Import and use integrate_plasticity_with_brain()")
