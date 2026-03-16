from agents.thalamus_agent import ThalamusAgent
from agents.hippocampus_agent import HippocampusAgent
from agents.limbic_agent import LimbicAgent
from agents.pfc_agent import PFCAgent
from agents.cerebellum_agent import CerebellumAgent
from agents.brainstem_agent import BrainstemAgent
from agents.basal_agent import BasalAgent
from state_writer import StateWriter

from conscious import ConsciousLayer
from subconscious import SubconsciousLayer
from unconscious import UnconsciousLayer

class OODA:
    def __init__(self, cfg):
        self.cfg = cfg["brain"]
        
        # 1. Initialize Regions (Agents)
        self.thalamus = ThalamusAgent(self.cfg)
        self.hippo = HippocampusAgent(self.cfg)
        self.limbic = LimbicAgent(self.cfg)
        self.pfc = PFCAgent(self.cfg)
        self.cereb = CerebellumAgent(self.cfg)
        self.brainstem = BrainstemAgent(self.cfg)
        self.basal = BasalAgent(self.cfg)
        
        # 2. Initialize the 3-Tier Consciousness Architecture
        self.conscious = ConsciousLayer(self.pfc, self.cereb, self.brainstem)
        self.subconscious = SubconsciousLayer(self.hippo)
        self.unconscious = UnconsciousLayer(self.hippo, self.basal, self.limbic)
        
        self.state_writer = StateWriter(self.cfg["state_path"])
        
        # Tracking for error calculation
        self.last_prediction = None
        self.tick_count = 0

    def tick(self):
        self.tick_count += 1
        
        # O: Observe (Thalamus)
        obs = self.thalamus.observe()
        
        # O: Orient (Subconscious Context)
        ctx = self.subconscious.context(obs)
        affect = self.unconscious.evaluate_affect(obs, ctx)
        
        # Calculate complexity for GrowingNN
        complexity = self.basal.calculate_complexity(obs, ctx)
        
        # D: Decide (Conscious Layer + Brainstem Safety)
        decision = self.conscious.decide(obs, ctx, affect)
        act = decision["actions"]
        plan = decision["plan"]
        
        # Track error (compare predicted vs actual)
        predicted = self.last_prediction
        actual = act.get("type", "unknown")
        error = self.basal.track_error(predicted, actual)
        
        # Store memory and get novelty
        store_result = self.hippo.store(obs, plan, act, affect)
        novelty = store_result.get("novelty", 0.0)
        
        # A: Act & Learn (Unconscious Layer)
        self.unconscious.learn({
            "raw": obs,
            "meta": {"plan": plan, "affect": affect, "actions": act}
        })
        
        # Execute action
        self.basal.execute(act, affect)
        
        # GrowingNN: Check for growth triggers
        if self.basal.should_add_node(novelty, error):
            self.basal.add_node()
        
        if self.basal.should_add_layer(complexity):
            self.basal.add_layer()
        
        # Update prediction for next tick
        self.last_prediction = act.get("type", "unknown")
        
        # Get comprehensive stats
        novelty_stats = self.hippo.get_novelty_stats()
        basal_stats = self.basal.get_stats()
        nn_state = basal_stats["nn_state"]
        
        # Write state for Visualizer
        self.state_writer.write({
            "phase": "Act",
            "tick": self.tick_count,
            "obs": obs,
            "plan": plan,
            "action": act,
            "limbic": affect,
            "policy_nn": {
                "layers": nn_state["layers"],
                "nodes": nn_state["nodes"],
                "activations": nn_state["activations"],
                "total_nodes": nn_state["total_nodes"],
                "growth_events": nn_state["growth_events"]
            },
            "memory_nn": {
                "clusters": novelty_stats["total_traces"],
                "novelty_current": novelty_stats["current"],
                "novelty_avg": novelty_stats["average"],
                "novelty_max": novelty_stats["max"]
            },
            "growingnn": {
                "error_rate": error,
                "complexity": complexity,
                "novelty": novelty,
                "growth_triggered": self.basal.should_add_node(novelty, error) or self.basal.should_add_layer(complexity)
            }
        })
