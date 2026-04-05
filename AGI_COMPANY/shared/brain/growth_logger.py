"""
Growth Logger Module
Log and visualize brain development over time.
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class GrowthLogger:
    """
    Logs brain development snapshots.
    
    Creates time-series data for visualizing growth.
    """
    
    def __init__(self, log_dir: str = "~/.aos/brain/logs/growth"):
        self.log_dir = Path(log_dir).expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.step_count = 0
        self.last_log_step = 0
        self.log_interval = 100  # Log every N steps
        
    def log_brain_state(self, 
                         step: int,
                         TRACRAY: Dict,
                         sheet,
                         memory_store,
                         neurochem,
                         dev,
                         curriculum):
        """
        Log complete brain state.
        
        Args:
            step: Current tick
            TRACRAY: Tracray lexicon
            sheet: Cortical sheet
            memory_store: Memory store
            neurochem: Neurochemistry object
            dev: BrainDevelopment object
            curriculum: LifeCurriculum object
        """
        self.step_count = step
        
        # Only log periodically
        if step - self.last_log_step < self.log_interval:
            return
            
        self.last_log_step = step
        
        # Gather data
        data = {
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "stage": dev.get_stage() if hasattr(dev, 'get_stage') else "unknown",
            "age_steps": getattr(dev, 'age_steps', step),
            
            # Tracray snapshot
            "tracray": {
                "concept_count": len(TRACRAY.get("concepts", {})),
                "coords": {
                    name: spec.get("coord", (0, 0, 0))
                    for name, spec in list(TRACRAY.get("concepts", {}).items())[:20]  # Sample
                },
            },
            
            # Sheet statistics
            "sheet": {
                "mean_weight": sum(sheet.weight) / len(sheet.weight) if hasattr(sheet, 'weight') else 0.5,
                "max_weight": max(sheet.weight) if hasattr(sheet, 'weight') else 1.0,
                "min_weight": min(sheet.weight) if hasattr(sheet, 'weight') else 0.1,
                "active_fraction": sum(1 for v in sheet.state if v == 1) / len(sheet.state) if hasattr(sheet, 'state') else 0,
            },
            
            # Memory statistics
            "memory": {
                "trace_count": len(getattr(memory_store, 'traces', [])),
                "cluster_count": getattr(memory_store, 'cluster_count', 0),
            },
            
            # Neurochemistry
            "neurochem": neurochem.state.to_dict() if hasattr(neurochem, 'state') else {},
            
            # Curriculum
            "curriculum": curriculum.get_curriculum_stats() if hasattr(curriculum, 'get_curriculum_stats') else {},
        }
        
        # Write to file
        log_file = self.log_dir / f"brain_{step:08d}.json"
        with open(log_file, "w") as f:
            json.dump(data, f, indent=2)
            
    def get_growth_history(self, last_n: int = 100) -> List[Dict]:
        """
        Get recent growth history.
        
        Args:
            last_n: Number of recent logs to retrieve
            
        Returns:
            List of brain state dicts
        """
        log_files = sorted(self.log_dir.glob("brain_*.json"))
        
        history = []
        for log_file in log_files[-last_n:]:
            with open(log_file) as f:
                history.append(json.load(f))
                
        return history
        
    def get_development_timeline(self) -> Dict:
        """
        Get complete development timeline.
        
        Returns:
            Dict with stage transitions and metrics
        """
        history = self.get_growth_history(last_n=10000)
        
        if not history:
            return {"status": "no_data"}
            
        timeline = {
            "total_steps": history[-1]["step"] - history[0]["step"],
            "stage_transitions": [],
            "mean_weight_trajectory": [],
            "neurochem_trajectory": {
                "dopamine": [],
                "serotonin": [],
            },
        }
        
        prev_stage = None
        for entry in history:
            stage = entry.get("stage")
            if stage != prev_stage:
                timeline["stage_transitions"].append({
                    "step": entry["step"],
                    "from": prev_stage,
                    "to": stage,
                })
                prev_stage = stage
                
            timeline["mean_weight_trajectory"].append({
                "step": entry["step"],
                "weight": entry.get("sheet", {}).get("mean_weight", 0),
            })
            
            neurochem = entry.get("neurochem", {})
            timeline["neurochem_trajectory"]["dopamine"].append({
                "step": entry["step"],
                "value": neurochem.get("dopamine", 0),
            })
            
        return timeline
        
    def generate_growth_report(self) -> str:
        """Generate a text report of growth"""
        timeline = self.get_development_timeline()
        
        if timeline.get("status") == "no_data":
            return "No growth data available yet."
            
        report = []
        report.append("=" * 60)
        report.append("BRAIN GROWTH REPORT")
        report.append("=" * 60)
        report.append(f"Total steps: {timeline['total_steps']:,}")
        report.append(f"Stage transitions: {len(timeline['stage_transitions'])}")
        report.append("")
        
        for transition in timeline["stage_transitions"]:
            report.append(f"  Step {transition['step']:,}: {transition['from']} → {transition['to']}")
            
        if timeline["mean_weight_trajectory"]:
            first = timeline["mean_weight_trajectory"][0]["weight"]
            last = timeline["mean_weight_trajectory"][-1]["weight"]
            report.append("")
            report.append(f"Mean synaptic weight: {first:.3f} → {last:.3f}")
            
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


class SimpleVisualizer:
    """
    Simple text-based growth visualizer.
    
    For full 3D visualization, use the log files with external tools.
    """
    
    def __init__(self, logger: GrowthLogger):
        self.logger = logger
        
    def print_concept_map(self, step: int = -1):
        """Print ASCII concept map"""
        history = self.logger.get_growth_history(last_n=1)
        
        if not history:
            print("No data available")
            return
            
        data = history[0] if step == -1 else None
        
        # Find closest step
        for h in self.logger.get_growth_history(last_n=100):
            if h["step"] >= step:
                data = h
                break
                
        if not data:
            print(f"No data for step {step}")
            return
            
        print(f"\nConcept Map at Step {data['step']:,}:")
        print("-" * 40)
        
        coords = data.get("tracray", {}).get("coords", {})
        for name, (x, y, z) in list(coords.items())[:10]:
            print(f"  {name:15} @ ({x:6.2f}, {y:6.2f}, {z:6.2f})")
            
    def print_growth_chart(self, metric: str = "mean_weight", width: int = 60):
        """Print ASCII growth chart"""
        history = self.logger.get_growth_history(last_n=50)
        
        if not history:
            print("No data available")
            return
            
        values = [h.get("sheet", {}).get(metric, 0) for h in history]
        
        if not values:
            print(f"No {metric} data available")
            return
            
        min_val = min(values)
        max_val = max(values)
        
        if max_val == min_val:
            print(f"No variation in {metric}")
            return
            
        print(f"\n{metric} over last {len(values)} logs:")
        print("-" * width)
        
        for i, val in enumerate(values):
            normalized = (val - min_val) / (max_val - min_val)
            bar_length = int(normalized * (width - 20))
            bar = "█" * bar_length
            step = history[i]["step"]
            print(f"{step:8} │{bar:50} {val:.3f}")
            

if __name__ == "__main__":
    print("Growth Logger Module")
    print("=" * 50)
    
    # Create logger
    logger = GrowthLogger(log_dir="/tmp/test_growth")
    
    # Simulate some logs
    print("\nSimulating brain growth logs...")
    
    class MockSheet:
        def __init__(self):
            self.weight = [0.5] * 1000
            self.state = [0] * 1000
            
    class MockNeurochem:
        def __init__(self):
            self.state = type('obj', (object,), {
                'to_dict': lambda: {'dopamine': 0.5, 'serotonin': 0.3}
            })()
            
    for step in range(0, 1000, 100):
        # Simulate weight growth
        sheet = MockSheet()
        for i in range(len(sheet.weight)):
            sheet.weight[i] = 0.5 + (step / 1000) * 0.3
            
        neuro = MockNeurochem()
        
        logger.log_brain_state(
            step=step,
            TRACRAY={"concepts": {"milk": {"coord": (10, 10, 4)}}},
            sheet=sheet,
            memory_store=type('obj', (object,), {'traces': []})(),
            neurochem=neuro,
            dev=type('obj', (object,), {'get_stage': lambda: 'infant'})(),
            curriculum=type('obj', (object,), {'get_curriculum_stats': lambda: {}})(),
        )
        
    print(f"\nLogged {len(list(logger.log_dir.glob('*.json')))} snapshots")
    
    # Generate report
    print("\n" + logger.generate_growth_report())
    
    # Visualize
    viz = SimpleVisualizer(logger)
    viz.print_concept_map()
    viz.print_growth_chart()
    
    print("\n" + "=" * 50)
    print("Growth logger ready")
