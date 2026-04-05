class UnconsciousLayer:
    def __init__(self, hippocampus, basal_ganglia, limbic):
        self.hippo = hippocampus
        self.basal = basal_ganglia
        self.limbic = limbic

    def evaluate_affect(self, obs, ctx):
        # Pass hippocampus reference for novelty calculation
        if hasattr(self.limbic, 'hippo') and self.limbic.hippo is None:
            self.limbic.hippo = self.hippo
        return self.limbic.evaluate(obs, ctx)

    def learn(self, trace):
        # Long term memory consolidation and habit reinforcement
        store_result = self.hippo.store(
            obs=trace.get("raw"), 
            plan=trace.get("meta", {}).get("plan"), 
            action=trace.get("meta", {}).get("actions"), 
            affect=trace.get("meta", {}).get("affect")
        )
        
        # Get novelty from store result for limbic update
        novelty = store_result.get("novelty", 0.0) if isinstance(store_result, dict) else 0.0
        
        # Update limbic with actual novelty
        if hasattr(self.limbic, 'novelty_history'):
            self.limbic.novelty_history.append(novelty)
            if len(self.limbic.novelty_history) > 100:
                self.limbic.novelty_history = self.limbic.novelty_history[-100:]
        
        self.basal.execute(trace.get("meta", {}).get("actions"), trace.get("meta", {}).get("affect"))
