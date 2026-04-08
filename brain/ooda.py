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
from memory_bridge import MemoryBridge
from memory_bootstrap import patch_hippocampus_for_resilience

class OODA:
    def __init__(self, cfg):
        self.cfg = cfg["brain"]
        
        # 1. Initialize Regions (Agents)
        self.thalamus = ThalamusAgent(self.cfg)
        self.hippo = HippocampusAgent(self.cfg)
        # Patch hippocampus for resilience
        self.hippo = patch_hippocampus_for_resilience(self.hippo)
        self.limbic = LimbicAgent(self.cfg)
        self.pfc = PFCAgent(self.cfg)
        self.cereb = CerebellumAgent(self.cfg)
        self.brainstem = BrainstemAgent(self.cfg)
        self.basal = BasalAgent(self.cfg)
        
        # 2. Initialize the 3-Tier Consciousness Architecture
        self.conscious = ConsciousLayer(self.pfc, self.cereb, self.brainstem)
        self.subconscious = SubconsciousLayer(self.hippo)
        self.unconscious = UnconsciousLayer(self.hippo, self.basal, self.limbic)
        
        # 3. Initialize Memory Bridge for workspace file integration
        self.memory_bridge = MemoryBridge()
        # Index files in background (don't block startup)
        import threading
        self._index_thread = threading.Thread(target=self.memory_bridge.index_memory_files, daemon=True)
        self._index_thread.start()
        
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
        
        # MEMORY BRIDGE: Query workspace memory on high novelty
        workspace_memory = None
        try:
            novelty = affect.get("novelty", 0.0)
            novelty_avg = affect.get("novelty_avg", 0.0)
            if self.memory_bridge.should_query_memory(novelty, novelty_avg):
                query_text = str(obs.get("input", obs))
                workspace_memory = self.memory_bridge.query(
                    query_text=query_text,
                    n_results=2,
                    novelty=novelty
                )
                # Inject memory into context for conscious layer
                if workspace_memory and workspace_memory.get("source_count", 0) > 0:
                    ctx["workspace_memory"] = workspace_memory
        except Exception as e:
            # Don't let memory bridge errors crash the brain
            print(f"[MemoryBridge] Query error: {e}")
        
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
        state = {
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
        }
        
        # Include workspace memory if retrieved
        if workspace_memory:
            state["workspace_memory"] = {
                "queried": True,
                "source_count": workspace_memory.get("source_count", 0),
                "results": [
                    {"source": r["source"], "relevance": r["relevance"], "text": r["text"][:200]}
                    for r in workspace_memory.get("results", [])
                ]
            }
        
        self.state_writer.write(state)
