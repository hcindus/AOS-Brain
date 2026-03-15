class UnconsciousLayer:
    def __init__(self, hippocampus, basal_ganglia, limbic):
        self.hippo = hippocampus
        self.basal = basal_ganglia
        self.limbic = limbic

    def evaluate_affect(self, obs, ctx):
        return self.limbic.evaluate(obs, ctx)

    def learn(self, trace):
        # Long term memory consolidation and habit reinforcement
        self.hippo.store(
            obs=trace.get("raw"), 
            plan=trace.get("meta", {}).get("plan"), 
            action=trace.get("meta", {}).get("actions"), 
            affect=trace.get("meta", {}).get("affect")
        )
        self.basal.execute(trace.get("meta", {}).get("actions"), trace.get("meta", {}).get("affect"))
