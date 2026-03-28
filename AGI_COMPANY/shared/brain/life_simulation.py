"""
Life Simulation - Complete Brain Development
Simulates a brain growing from infant to adult.

Usage:
    python life_simulation.py --ticks 10000 --visualize
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/shared/brain')

from growth_laws import GrowingBrain, TernaryCorticalSheet3D
from life_curriculum import LifeCurriculum, DayNightCycle
from neurochemistry import Neurochemistry
from growth_logger import GrowthLogger, SimpleVisualizer
from learning import (
    BrainDevelopment,
    CuriosityAgent,
    register_concept_use,
    register_activation,
    self_organize_tracray,
    apply_reward_to_sheet,
    apply_reward_to_tracray,
    consolidate_memory,
    optimize_memory_palace,
)
from learning import tracray_organizer as org


class LifeSimulator:
    """
    Complete life simulation for the AOS brain.
    
    Simulates:
    - Developmental stages (infant → adult)
    - Day/night cycles (learning → consolidation)
    - Neuromodulators affecting behavior
    - Growth logging and visualization
    """
    
    def __init__(self, 
                 total_ticks: int = 100_000,
                 day_length: int = 1000,
                 night_length: int = 500,
                 log_interval: int = 100):
        
        print("🌱 Initializing Life Simulation...")
        
        self.total_ticks = total_ticks
        self.log_interval = log_interval
        
        # Initialize brain components
        self.sheet = TernaryCorticalSheet3D(nx=32, ny=32, nz=8)
        self.TRACRAY = {"concepts": {}}
        self.memory_store = type('obj', (object,), {
            'traces': [],
            'cluster_count': 0,
            'add_trace': lambda **kwargs: self.memory_store.traces.append(kwargs),
        })()
        
        # Initialize learning systems
        self.curriculum = LifeCurriculum()
        self.day_night = DayNightCycle(day_length, night_length)
        self.neurochem = Neurochemistry()
        self.development = BrainDevelopment()
        self.curiosity = CuriosityAgent(self.TRACRAY, self.sheet)
        self.logger = GrowthLogger()
        
        # Simulation state
        self.tick = 0
        self.concepts_learned = set()
        
        # Seed initial concepts
        self._seed_concepts()
        
        print(f"   Brain initialized: {len(self.TRACRAY['concepts'])} seed concepts")
        print(f"   Curriculum: {len(self.curriculum.STAGES)} stages")
        print(f"   Simulation: {total_ticks:,} ticks")
        
    def _seed_concepts(self):
        """Seed initial concepts in Tracray"""
        seed = {
            "milk": {"coord": (16, 16, 4)},
            "warm": {"coord": (16, 20, 4)},
            "soft": {"coord": (20, 16, 4)},
            "light": {"coord": (20, 20, 4)},
            "sound": {"coord": (12, 16, 4)},
            "mother": {"coord": (16, 12, 4)},
        }
        self.TRACRAY["concepts"] = seed
        
    def _get_limbic_valence(self, concepts: list) -> float:
        """Simulate limbic evaluation"""
        # Simple simulation: positive for known concepts
        valence = 0.3
        
        for concept in concepts:
            if concept in self.concepts_learned:
                valence += 0.1  # Familiar = good
            else:
                valence += 0.2  # Novel = exciting
                
        return min(1.0, max(-1.0, valence))
        
    def _get_novelty(self, concepts: list) -> float:
        """Calculate novelty"""
        if not concepts:
            return 0.0
            
        novel_count = sum(1 for c in concepts if c not in self.concepts_learned)
        return novel_count / len(concepts)
        
    def _get_threat(self, concepts: list) -> float:
        """Simulate threat detection"""
        threat_words = ["loud", "dark", "cold", "pain", "scary"]
        if any(w in concepts for w in threat_words):
            return 0.5
        return 0.0
        
    def run_tick(self):
        """Execute one tick of life simulation"""
        self.tick += 1
        
        # Update day/night cycle
        time_of_day = self.day_night.tick()
        is_night = (time_of_day == "night")
        
        # Update development
        self.development.step()
        stage = self.development.configure(self.sheet, type('obj', (object,), {'novelty_gain': 1.0})())
        
        # Generate curriculum input
        input_data = self.curriculum.generate_input(self.tick)
        concepts = input_data["concepts"]
        
        # Track learned concepts
        for c in concepts:
            self.concepts_learned.add(c)
            
        # Evaluate experience
        valence = self._get_limbic_valence(concepts)
        novelty = self._get_novelty(concepts)
        threat = self._get_threat(concepts)
        
        # Update neurochemistry
        self.neurochem.update(valence, novelty, threat)
        
        # Apply reward modulation
        apply_reward_to_sheet(self.sheet, valence)
        apply_reward_to_tracray(valence, org)
        
        # Register concept usage
        register_concept_use(concepts)
        register_activation(concepts, valence)
        
        # Cortical dynamics with plasticity
        from learning.plasticity import step_sheet_with_plasticity
        step_sheet_with_plasticity(self.sheet)
        
        # Memory trace
        trace = {
            "tick": self.tick,
            "concepts": concepts,
            "valence": valence,
            "novelty": novelty,
            "stage": stage,
        }
        
        # Consolidate if conditions right
        if self.neurochem.should_consolidate_memory():
            consolidate_memory(self.memory_store, trace, valence)
            
        # Night: reorganization and dream
        if is_night:
            self_organize_tracray(self.TRACRAY, steps=3)
            
            # Occasional memory palace optimization
            if self.tick % 1000 == 0:
                clusters, portals = optimize_memory_palace(self.memory_store)
                self.memory_store.cluster_count = len(clusters)
                
        # Day: curiosity when idle
        elif not is_night and self.tick % 50 == 0:
            if self.curiosity.should_explore(novelty):
                explored = self.curiosity.act()
                
        # Log state
        if self.tick % self.log_interval == 0:
            self.logger.log_brain_state(
                self.tick,
                self.TRACRAY,
                self.sheet,
                self.memory_store,
                self.neurochem,
                self.development,
                self.curriculum,
            )
            
    def run(self, visualize: bool = False):
        """
        Run complete life simulation.
        
        Args:
            visualize: Show progress visualization
        """
        print(f"\n🚀 Starting Life Simulation...")
        print(f"   Target: {self.total_ticks:,} ticks")
        print(f"   From infant to {self.total_ticks / 1_000_000:.2f}M tick adult")
        print()
        
        viz = SimpleVisualizer(self.logger) if visualize else None
        
        # Main simulation loop
        for i in range(self.total_ticks):
            self.run_tick()
            
            # Progress updates
            if self.tick % 10_000 == 0:
                stage = self.development.get_stage()
                neuro = self.neurochem.state
                print(f"   Tick {self.tick:,} | Stage: {stage:12} | "
                      f"Dopamine: {neuro.dopamine:+.2f} | "
                      f"Concepts: {len(self.concepts_learned):4}")
                      
                if viz:
                    viz.print_concept_map()
                    
        # Final report
        print(f"\n✅ Simulation Complete!")
        print(f"   Total ticks: {self.tick:,}")
        print(f"   Final stage: {self.development.get_stage()}")
        print(f"   Concepts learned: {len(self.concepts_learned)}")
        print(f"   Memory traces: {len(self.memory_store.traces)}")
        
        # Generate report
        report = self.logger.generate_growth_report()
        print("\n" + report)
        
        if viz:
            print("\n📊 Growth Charts:")
            viz.print_growth_chart("mean_weight")
            viz.print_growth_chart("max_weight")
            


def main():
    parser = argparse.ArgumentParser(description="AOS Brain Life Simulation")
    parser.add_argument("--ticks", type=int, default=10_000,
                       help="Total simulation ticks")
    parser.add_argument("--day-length", type=int, default=1000,
                       help="Day cycle length")
    parser.add_argument("--night-length", type=int, default=500,
                       help="Night cycle length")
    parser.add_argument("--log-interval", type=int, default=100,
                       help="Logging interval")
    parser.add_argument("--visualize", action="store_true",
                       help="Enable visualization")
    
    args = parser.parse_args()
    
    # Run simulation
    sim = LifeSimulator(
        total_ticks=args.ticks,
        day_length=args.day_length,
        night_length=args.night_length,
        log_interval=args.log_interval,
    )
    
    sim.run(visualize=args.visualize)


if __name__ == "__main__":
    main()
