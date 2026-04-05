class ConsciousLayer:
    def __init__(self, pfc, cerebellum, brainstem):
        self.pfc = pfc
        self.cerebellum = cerebellum
        self.brainstem = brainstem

    def decide(self, goal, context, affect):
        plan = self.pfc.plan(goal, context, affect)
        actions = self.cerebellum.format(plan)
        safe = self.brainstem.enforce(actions, goal, context, affect)
        return {"plan": plan, "actions": safe}
