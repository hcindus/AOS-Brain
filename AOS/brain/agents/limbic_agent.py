class LimbicAgent:
    def __init__(self, cfg):
        self.cfg = cfg

    def evaluate(self, obs, ctx):
        return {
            "reward": 0.0, 
            "novelty": 0.0, 
            "mode": self.cfg.get("modes", {}).get("active_mode", "adaptive")
        }
