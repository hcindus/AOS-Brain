class ThalamusAgent:
    def __init__(self, cfg):
        self.cfg = cfg

    def observe(self):
        # For now, just a stub input; later wire to gateway/CLI
        return {"input": "system_tick"}
