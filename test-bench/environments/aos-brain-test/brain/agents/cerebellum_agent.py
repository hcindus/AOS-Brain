class CerebellumAgent:
    def __init__(self, cfg):
        self.cfg = cfg

    def format(self, plan):
        return {"type": "noop", "plan": plan}
