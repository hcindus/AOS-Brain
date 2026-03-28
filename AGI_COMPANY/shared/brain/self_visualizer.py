"""
Self-Visualization Module
The brain visualizing its own growth and development.

This allows the brain to:
- See concept movement trails over time
- Visualize its own neurochemical state
- Watch memory clusters form
- Observe stage transitions
- Meta-cognitive self-awareness
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from collections import defaultdict


class BrainSelfVisualizer:
    """
    Allows the brain to visualize itself.
    
    Creates representations of:
    - Concept trajectories through Tracray space
    - Neurochemical state over time
    - Memory palace structure
    - Developmental stage transitions
    """
    
    def __init__(self, log_dir: str = "~/.aos/brain/logs/growth"):
        self.log_dir = Path(log_dir).expanduser()
        
        # Concept history for trails
        self.concept_history = defaultdict(list)  # concept -> [(tick, coord), ...]
        
        # Neurochemical history
        self.neurochem_history = []
        
        # Stage transitions
        self.stage_history = []
        
        # Current view state
        self.current_tick = 0
        self.view_mode = "concepts"  # concepts, neurochem, memory, development
        
    def load_growth_data(self, last_n: int = 1000):
        """Load recent growth logs"""
        log_files = sorted(self.log_dir.glob("brain_*.json"))
        
        for log_file in log_files[-last_n:]:
            with open(log_file) as f:
                data = json.load(f)
                self._process_log_entry(data)
                
    def _process_log_entry(self, data: Dict):
        """Process a single log entry"""
        tick = data.get("step", 0)
        
        # Track concept positions
        tracray = data.get("tracray", {})
        coords = tracray.get("coords", {})
        
        for concept, coord in coords.items():
            self.concept_history[concept].append({
                "tick": tick,
                "coord": coord,
            })
            
        # Track neurochemistry
        neurochem = data.get("neurochem", {})
        if neurochem:
            self.neurochem_history.append({
                "tick": tick,
                **neurochem,
            })
            
        # Track stages
        stage = data.get("stage")
        if stage:
            if not self.stage_history or self.stage_history[-1]["stage"] != stage:
                self.stage_history.append({
                    "tick": tick,
                    "stage": stage,
                })
                
    def get_concept_trajectory(self, concept: str, sample_rate: int = 10) -> List[Dict]:
        """
        Get movement trail for a concept.
        
        Args:
            concept: Concept name
            sample_rate: Sample every N points
            
        Returns:
            List of {tick, x, y, z, intensity}
        """
        history = self.concept_history.get(concept, [])
        
        if not history:
            return []
            
        trajectory = []
        for i, entry in enumerate(history[::sample_rate]):
            x, y, z = entry["coord"]
            
            # Calculate intensity based on recency
            age = self.current_tick - entry["tick"]
            intensity = max(0.1, 1.0 - (age / 10000))
            
            trajectory.append({
                "tick": entry["tick"],
                "x": x,
                "y": y,
                "z": z,
                "intensity": intensity,
                "age": age,
            })
            
        return trajectory
        
    def get_all_concept_positions(self, tick: int = -1) -> Dict[str, Dict]:
        """
        Get all concept positions at a specific time.
        
        Args:
            tick: Time point (-1 for latest)
            
        Returns:
            Dict mapping concept to position + metadata
        """
        if tick == -1:
            tick = self.current_tick
            
        positions = {}
        
        for concept, history in self.concept_history.items():
            # Find closest entry to requested tick
            closest = None
            closest_dist = float('inf')
            
            for entry in history:
                dist = abs(entry["tick"] - tick)
                if dist < closest_dist:
                    closest_dist = dist
                    closest = entry
                    
            if closest:
                x, y, z = closest["coord"]
                
                # Calculate visit importance
                visit_count = len(history)
                importance = min(1.0, math.log(1 + visit_count) / 5)
                
                # Calculate velocity (movement rate)
                velocity = 0.0
                if len(history) > 1:
                    prev = history[-2]
                    dx = x - prev["coord"][0]
                    dy = y - prev["coord"][1]
                    dz = z - prev["coord"][2]
                    velocity = math.sqrt(dx*dx + dy*dy + dz*dz)
                    
                positions[concept] = {
                    "x": x,
                    "y": y,
                    "z": z,
                    "importance": importance,
                    "visit_count": visit_count,
                    "velocity": velocity,
                    "tick": closest["tick"],
                }
                
        return positions
        
    def get_neurochem_trajectory(self, chemical: str = "dopamine", 
                                   window: int = 100) -> List[Dict]:
        """Get trajectory of a specific neurochemical"""
        trajectory = []
        
        for entry in self.neurochem_history[-window:]:
            value = entry.get(chemical, 0)
            trajectory.append({
                "tick": entry["tick"],
                "value": value,
            })
            
        return trajectory
        
    def get_stage_timeline(self) -> List[Dict]:
        """Get developmental stage transitions"""
        return self.stage_history
        
    def generate_self_report(self) -> str:
        """Generate a report of the brain's own development"""
        report = []
        report.append("=" * 60)
        report.append("BRAIN SELF-VISUALIZATION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Developmental progress
        report.append("📈 Developmental Progress:")
        if self.stage_history:
            for transition in self.stage_history:
                report.append(f"  Step {transition['tick']:,}: {transition['stage']}")
        report.append("")
        
        # Concept statistics
        report.append(f"🧠 Concept Statistics ({len(self.concept_history)} concepts):")
        
        # Top 5 most visited concepts
        by_visits = sorted(
            self.concept_history.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:5]
        
        for concept, history in by_visits:
            report.append(f"  {concept:15} - {len(history):4} visits")
            
            # Show trajectory if moved significantly
            if len(history) >= 2:
                first = history[0]["coord"]
                last = history[-1]["coord"]
                dx = last[0] - first[0]
                dy = last[1] - first[1]
                dz = last[2] - first[2]
                distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                report.append(f"                  drifted {distance:.2f} units")
                
        report.append("")
        
        # Neurochemistry summary
        if self.neurochem_history:
            report.append("🧪 Neurochemistry Summary:")
            recent = self.neurochem_history[-10:]
            
            for chem in ["dopamine", "serotonin", "acetylcholine", "norepinephrine"]:
                values = [entry.get(chem, 0) for entry in recent]
                if values:
                    avg = sum(values) / len(values)
                    report.append(f"  {chem:15} avg: {avg:+.3f}")
                    
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
        
    def render_ascii_concept_map(self, tick: int = -1, width: int = 60, height: int = 20):
        """
        Render ASCII visualization of concept positions.
        
        Shows:
        - Concept positions (projected to 2D)
        - Intensity = visit count
        - Recent movement trails
        """
        positions = self.get_all_concept_positions(tick)
        
        if not positions:
            print("No concept data available")
            return
            
        # Find bounds
        xs = [p["x"] for p in positions.values()]
        ys = [p["y"] for p in positions.values()]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Create grid
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Place concepts
        chars = " ░▒▓█"  # Intensity levels
        
        for concept, pos in positions.items():
            # Map to grid
            gx = int((pos["x"] - min_x) / (max_x - min_x) * (width - 1))
            gy = int((pos["y"] - min_y) / (max_y - min_y) * (height - 1))
            
            # Calculate intensity
            intensity = int(pos["importance"] * (len(chars) - 1))
            
            grid[height - 1 - gy][gx] = chars[intensity]
            
        # Print
        print(f"\nConcept Map (Step {tick if tick > 0 else 'latest'}):")
        print("-" * width)
        for row in grid:
            print("".join(row))
        print("-" * width)
        print(f"Legend: █=high importance ░=low importance")
        
    def render_ascii_neurochem_timeline(self, width: int = 60, height: int = 10):
        """Render ASCII timeline of neurochemistry"""
        if not self.neurochem_history:
            print("No neurochemical data available")
            return
            
        chemicals = ["dopamine", "serotonin", "acetylcholine", "norepinephrine"]
        symbols = {"dopamine": "D", "serotonin": "S", "acetylcholine": "A", "norepinephrine": "N"}
        
        print(f"\nNeurochemical Timeline (last {width} samples):")
        print("-" * width)
        
        for chem in chemicals:
            trajectory = self.get_neurochem_trajectory(chem, window=width)
            
            if not trajectory:
                continue
                
            values = [t["value"] for t in trajectory]
            min_v, max_v = min(values), max(values)
            
            if max_v == min_v:
                continue
                
            line = []
            for val in values:
                normalized = (val - min_v) / (max_v - min_v)
                row = int(normalized * (height - 1))
                line.append(row)
                
            # Draw line
            grid = [[" " for _ in range(len(line))] for _ in range(height)]
            for i, row in enumerate(line):
                grid[height - 1 - row][i] = symbols[chem]
                
            print(f"{chem[:3]}: ", end="")
            for row in grid:
                print("".join(row))
                
        print("-" * width)
        
    def export_for_3d_visualizer(self, filepath: str):
        """
        Export data in format for 3D visualizer.
        
        Creates JSON with:
        - concept positions with trails
        - neurochem states
        - stage transitions
        """
        export_data = {
            "export_time": datetime.now().isoformat(),
            "current_tick": self.current_tick,
            "concepts": {},
            "neurochem_trajectories": {},
            "stage_timeline": self.stage_history,
        }
        
        # Export concept trails
        for concept, history in self.concept_history.items():
            export_data["concepts"][concept] = {
                "trail": [
                    {
                        "tick": h["tick"],
                        "x": h["coord"][0],
                        "y": h["coord"][1],
                        "z": h["coord"][2],
                    }
                    for h in history
                ],
                "current_position": history[-1]["coord"] if history else (0, 0, 0),
                "visit_count": len(history),
            }
            
        # Export neurochem
        for chem in ["dopamine", "serotonin", "acetylcholine", "norepinephrine"]:
            export_data["neurochem_trajectories"][chem] = [
                {
                    "tick": entry["tick"],
                    "value": entry.get(chem, 0),
                }
                for entry in self.neurochem_history
            ]
            
        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=2)
            
        print(f"Exported to {filepath}")


# Development mode integration
class DevelopmentMode:
    """
    Special operating mode for observing development.
    
    Can be activated to:
    - Slow down processing
    - Enable detailed logging
    - Activate visualization
    - Pause at stage transitions
    """
    
    def __init__(self, brain):
        self.brain = brain
        self.visualizer = BrainSelfVisualizer()
        self.active = False
        self.pause_on_stage_change = True
        
    def activate(self):
        """Enter development observation mode"""
        self.active = True
        print("🔬 Entering Development Mode")
        print("   Brain will observe its own growth")
        
    def deactivate(self):
        """Exit development mode"""
        self.active = False
        print("⚡ Resuming normal operation")
        
    def on_tick(self, tick: int):
        """Called every tick when in development mode"""
        if not self.active:
            return
            
        self.visualizer.current_tick = tick
        
        # Periodic visualization
        if tick % 1000 == 0:
            self.visualizer.load_growth_data(last_n=100)
            
            # Show concept map
            self.visualizer.render_ascii_concept_map()
            
            # Show neurochem
            self.visualizer.render_ascii_neurochem_timeline()
            
            # Show report
            print(self.visualizer.generate_self_report())
            
        # Check for stage transition
        current_stage = self.brain.development.get_stage() if hasattr(self.brain, 'development') else None


if __name__ == "__main__":
    print("Brain Self-Visualization Module")
    print("=" * 60)
    
    # Create visualizer
    viz = BrainSelfVisualizer()
    
    # Load sample data if available
    viz.load_growth_data(last_n=100)
    
    if viz.concept_history:
        print("\nLoaded concept history:")
        print(f"  {len(viz.concept_history)} concepts tracked")
        
        # Show trajectories
        for concept in list(viz.concept_history.keys())[:3]:
            trajectory = viz.get_concept_trajectory(concept)
            print(f"\n  {concept}: {len(trajectory)} positions recorded")
            
        # Render map
        viz.render_ascii_concept_map()
        
        # Show report
        print(viz.generate_self_report())
    else:
        print("\nNo growth data found.")
        print("Run life_simulation.py first to generate data.")
        
    print("\n" + "=" * 60)
    print("Self-visualization ready")
