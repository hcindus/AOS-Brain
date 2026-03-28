"""
Minecraft Brain Integration
Connects AOS brain to Minecraft for embodied learning.
"""

import sys
from typing import Dict, Optional
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from observer import MinecraftObserver
from actor import MinecraftActor
from growth_laws import GrowingBrain
from self_visualizer import BrainSelfVisualizer, DevelopmentMode


class MinecraftBrainIntegration:
    """
    Complete integration: Brain plays Minecraft, learns, visualizes itself.
    
    Creates a feedback loop:
    1. Observe Minecraft world → concepts
    2. Brain processes → actions
    3. Execute in Minecraft → new observations
    4. Learn from experience → growth
    5. Visualize self → meta-awareness
    """
    
    def __init__(self, 
                 brain: GrowingBrain,
                 observer: Optional[MinecraftObserver] = None,
                 actor: Optional[MinecraftActor] = None):
        self.brain = brain
        self.observer = observer or MinecraftObserver()
        self.actor = actor or MinecraftActor()
        self.visualizer = BrainSelfVisualizer()
        self.dev_mode = DevelopmentMode(brain)
        
        # Learning state
        self.tick_count = 0
        self.experiences = []
        self.is_sleeping = False
        
        # Memory palace mapping
        self.location_memories = {}  # (x,y,z) → memory_cluster
        
    def tick(self):
        """
        Execute one tick of brain-in-minecraft.
        
        Full loop:
        1. Observe world
        2. Convert to brain concepts
        3. Brain processes
        4. Decide actions
        5. Execute
        6. Learn from outcome
        """
        self.tick_count += 1
        
        # 1. OBSERVE
        observation = self.observer.observe()
        if not observation:
            return
            
        # 2. TRANSLATE to brain concepts
        concept_data = self.observer.to_concepts(observation)
        concepts = concept_data["concepts"]
        valence = concept_data["valence"]
        threat = concept_data["threat"]
        novelty = concept_data["novelty"]
        position = concept_data["position"]
        
        # Get neurochemical reward
        neuro = self.observer.get_reward_signal(observation)
        
        # 3. BRAIN PROCESSING
        # Update neurochemistry
        self.brain.neurochem.update(valence, novelty, threat)
        
        # Brain tick with learning
        self.brain.tick(
            input_signals=observation,
            active_concepts=concepts,
        )
        
        # 4. DECIDE ACTIONS
        # Priority 1: React to immediate threats
        if threat > 0.5:
            action = {"type": "flee", "priority": 10}
            
        # Priority 2: Curiosity when safe
        elif self.brain.curiosity.should_explore(novelty):
            action = self.actor.from_brain_concepts(
                concepts + ["explore"], 
                intensity=novelty
            )
            
        # Priority 3: Goal-directed from concepts
        else:
            action = self.actor.from_brain_concepts(concepts)
            
        # Priority 4: Cortical activation
        if not action:
            # Get active region from sheet
            active = self.brain.sheet.get_active_regions()
            if active:
                action = self.actor.from_cortical_activation(
                    active[0], 
                    (0, 1, 0)  # Forward bias
                )
                
        # 5. EXECUTE
        if action:
            success = self.actor.execute(action)
            
            # Record experience
            experience = {
                "tick": self.tick_count,
                "concepts": concepts,
                "action": action,
                "valence": valence,
                "neurochem": neuro,
                "position": position,
                "success": success,
            }
            self.experiences.append(experience)
            
        # 6. MEMORY PALACE
        # Map this location to memory
        loc_key = (int(position[0]), int(position[1]), int(position[2]))
        if loc_key not in self.location_memories:
            self.location_memories[loc_key] = {
                "first_seen": self.tick_count,
                "concepts": concepts,
                "visits": 0,
            }
        self.location_memories[loc_key]["visits"] += 1
        
        # 7. DREAM MODE (sleep in bed)
        if self.is_sleeping or ("sleep" in concepts and valence > 0.3):
            self._enter_dream_mode()
            
        # 8. SELF-VISUALIZATION
        if self.tick_count % 100 == 0:
            self._update_visualization()
            
        # 9. DEVELOPMENT MODE
        if self.dev_mode.active:
            self.dev_mode.on_tick(self.tick_count)
            
    def _enter_dream_mode(self):
        """Enter dream/sleep mode for consolidation"""
        if not self.is_sleeping:
            print("💤 Entering dream mode...")
            self.is_sleeping = True
            self.brain.enter_dream_mode()
            
        # During sleep:
        # - Replay recent experiences
        # - Reorganize Tracray
        # - Optimize memory palace
        # - Consolidate memories
        
        recent = self.experiences[-50:]
        for exp in recent:
            # Replay
            self.brain.learning.learn_from_experience(
                exp["concepts"],
                exp["valence"],
                novelty=0.3,
            )
            
        # Reorganize
        from learning import self_organize_tracray
        self_organize_tracray(self.brain.TRACRAY, steps=10)
        
        # Optimize memory palace
        clusters, portals = optimize_memory_palace(self.brain.memory_store)
        
        # Wake up after processing
        if len(self.experiences) % 200 == 0:
            print("☀️ Waking up from dream mode")
            self.is_sleeping = False
            self.brain.exit_dream_mode()
            
    def _update_visualization(self):
        """Update self-visualization"""
        # Log current state
        self.brain.logger.log_brain_state(
            self.tick_count,
            self.brain.TRACRAY,
            self.brain.sheet,
            self.brain.memory_store,
            self.brain.neurochem,
            self.brain.development,
            self.brain.curriculum,
        )
        
        # Development mode visualization
        if self.tick_count % 1000 == 0:
            viz = self.visualizer
            viz.current_tick = self.tick_count
            viz.load_growth_data(last_n=100)
            
            # ASCII visualization
            viz.render_ascii_concept_map()
            viz.render_ascii_neurochem_timeline()
            
            # Report
            report = viz.generate_self_report()
            print(report)
            
    def run_life(self, ticks: int = 10000, development_mode: bool = False):
        """
        Run complete life simulation in Minecraft.
        
        Args:
            ticks: Number of ticks to simulate
            development_mode: Enable development visualization
        """
        if development_mode:
            self.dev_mode.activate()
            
        print(f"🎮 Starting Minecraft Life Simulation")
        print(f"   Ticks: {ticks:,}")
        print(f"   Development mode: {development_mode}")
        print()
        
        for i in range(ticks):
            self.tick()
            
            # Progress
            if i % 1000 == 0 and i > 0:
                status = self.brain.get_status()
                print(f"   Tick {i:,} | Stage: {status['stage']} | "
                      f"Weight: {status.get('cortical_stats', {}).get('mean_weight', 0):.3f}")
                      
        print(f"\n✅ Life simulation complete!")
        print(f"   Total ticks: {self.tick_count:,}")
        print(f"   Experiences: {len(self.experiences):,}")
        print(f"   Locations mapped: {len(self.location_memories)}")
        
        # Final report
        print(self.visualizer.generate_self_report())


def create_minecraft_brain():
    """
    Factory: Create brain optimized for Minecraft.
    
    Returns:
        GrowingBrain configured for embodied learning
    """
    # Seed with Minecraft-relevant concepts
    initial_tracray = {
        "concepts": {
            # Resources
            "wood": {"coord": (10, 10, 4)},
            "stone": {"coord": (15, 10, 4)},
            "coal": {"coord": (20, 10, 4)},
            "iron": {"coord": (25, 10, 4)},
            "diamond": {"coord": (30, 10, 4)},
            
            # Danger
            "zombie": {"coord": (10, 5, 4)},
            "skeleton": {"coord": (15, 5, 4)},
            "creeper": {"coord": (20, 5, 4)},
            "lava": {"coord": (25, 5, 4)},
            "fall": {"coord": (30, 5, 4)},
            
            # Needs
            "hunger": {"coord": (10, 15, 4)},
            "shelter": {"coord": (15, 15, 4)},
            "safety": {"coord": (20, 15, 4)},
            
            # Actions
            "mine": {"coord": (25, 15, 4)},
            "craft": {"coord": (30, 15, 4)},
            "build": {"coord": (35, 15, 4)},
            "explore": {"coord": (40, 15, 4)},
            
            # Time
            "day": {"coord": (10, 20, 4)},
            "night": {"coord": (15, 20, 4)},
        }
    }
    
    brain = GrowingBrain(
        tracray_lexicon=initial_tracray,
        nx=64, ny=64, nz=16,
    )
    
    return brain


if __name__ == "__main__":
    print("Minecraft Brain Integration")
    print("=" * 60)
    
    # Create brain for Minecraft
    brain = create_minecraft_brain()
    
    # Create integration
    integration = MinecraftBrainIntegration(brain)
    
    # Run life in Minecraft
    integration.run_life(ticks=5000, development_mode=True)
    
    print("\n" + "=" * 60)
    print("Integration ready - brain can now play Minecraft")
