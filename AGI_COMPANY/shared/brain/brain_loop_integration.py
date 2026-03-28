"""
Brain Loop with Learning Integration
Main brain tick loop with all growth laws integrated.
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/shared/brain')

from learning import (
    step_sheet_with_plasticity,
    register_activation,
    self_organize_tracray,
    apply_reward_to_sheet,
    apply_reward_to_tracray,
    consolidate_memory,
    optimize_memory_palace,
    BrainDevelopment,
    CuriosityAgent,
    register_concept_use
)
from learning import tracray_organizer as org


class LearningBrainLoop:
    """
    Main brain loop with integrated learning.
    
    Usage:
        from brain_loop_integration import LearningBrainLoop
        
        brain = LearningBrainLoop(sheet, TRACRAY, memory_store, limbic)
        
        while True:
            brain.tick(input_signals)
    """
    
    def __init__(self, sheet, TRACRAY, memory_store, limbic_agent):
        self.sheet = sheet
        self.TRACRAY = TRACRAY
        self.memory_store = memory_store
        self.limbic = limbic_agent
        
        # Initialize learning components
        self.development = BrainDevelopment()
        self.curiosity = CuriosityAgent(TRACRAY, sheet)
        
        self.tick_count = 0
        self.dream_mode = False
        self.idle_mode = False
        
    def tick(self, input_signals=None, active_concepts=None):
        """
        Execute one brain tick with learning.
        
        Args:
            input_signals: Raw input (optional)
            active_concepts: Pre-computed active concepts (optional)
        """
        self.tick_count += 1
        
        # 1. Development stage configuration
        self.development.step()
        stage = self.development.configure(self.sheet, self.limbic)
        
        # 2. Process input → concepts
        if active_concepts is None and input_signals is not None:
            # This would call your existing wernicke/pfc processing
            active_concepts = self._process_input(input_signals)
            
        if active_concepts:
            register_concept_use(active_concepts)
            
        # 3. Limbic evaluation
        if active_concepts:
            valence = self.limbic.evaluate(active_concepts)
        else:
            valence = 0.0
            
        # 4. Reward-modulated learning params
        apply_reward_to_sheet(self.sheet, valence)
        apply_reward_to_tracray(valence, org)
        
        # 5. Cortical dynamics with plasticity
        step_sheet_with_plasticity(self.sheet)
        
        # 6. Tracray coactivation + self-organization
        if active_concepts:
            register_activation(active_concepts, valence)
            
        if self.dream_mode or (self.tick_count % 100 == 0):
            # Periodic reorganization
            self_organize_tracray(self.TRACRAY, steps=5)
            
        # 7. Memory trace + consolidation
        if active_concepts:
            trace = {
                "tick": self.tick_count,
                "concepts": active_concepts,
                "valence": valence,
                "novelty": getattr(self.limbic, 'novelty', lambda x: 0.5)(active_concepts),
                "stage": stage,
            }
            consolidate_memory(self.memory_store, trace, valence)
            
        # 8. Dream mode: optimize memory palace
        if self.dream_mode:
            clusters, portals = optimize_memory_palace(self.memory_store)
            # Pass to visualizer if available
            self._update_visualizer(clusters, portals)
            
        # 9. Curiosity when idle
        if self.idle_mode or (self.tick_count % 50 == 0 and not active_concepts):
            if self.curiosity.should_explore(novelty=0.8):
                explored = self.curiosity.act()
                if explored:
                    print(f"Curiosity explored: {explored}")
                    
        # Log progress
        if self.tick_count % 1000 == 0:
            self._log_status(stage, valence)
            
    def _process_input(self, input_signals):
        """Process raw input into concepts"""
        # This would integrate with existing wernicke/pfc
        # For now, return empty or simulated
        return []
        
    def _update_visualizer(self, clusters, portals):
        """Update visualizer with memory palace structure"""
        # Hook for visualizer
        pass
        
    def _log_status(self, stage, valence):
        """Log brain status"""
        stats = self.sheet.get_stats() if hasattr(self.sheet, 'get_stats') else {}
        print(f"Tick {self.tick_count}: Stage={stage}, Valence={valence:.2f}, "
              f"MeanWeight={stats.get('mean_weight', 0):.3f}")
              
    def enter_dream_mode(self):
        """Enter dream/sleep mode for consolidation"""
        self.dream_mode = True
        print("Entering dream mode...")
        
    def exit_dream_mode(self):
        """Exit dream mode"""
        self.dream_mode = False
        print("Exiting dream mode...")
        
    def set_idle_mode(self, idle):
        """Set idle mode (enables curiosity)"""
        self.idle_mode = idle


# Example integration
def integrate_with_existing_brain(existing_brain):
    """
    Wrap existing brain with learning.
    
    Args:
        existing_brain: Your current SevenRegionBrain instance
    """
    # Extract components from existing brain
    sheet = existing_brain.cortical_sheet if hasattr(existing_brain, 'cortical_sheet') else None
    tracray = existing_brain.tracray if hasattr(existing_brain, 'tracray') else {}
    memory = existing_brain.memory if hasattr(existing_brain, 'memory') else None
    limbic = existing_brain.limbic if hasattr(existing_brain, 'limbic') else None
    
    if not all([sheet, tracray, memory, limbic]):
        print("Warning: Missing components for learning integration")
        return None
        
    return LearningBrainLoop(sheet, tracray, memory, limbic)


if __name__ == "__main__":
    print("Brain Loop Integration Module")
    print("Import and use LearningBrainLoop to integrate learning into main brain")
