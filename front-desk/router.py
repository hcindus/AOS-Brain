"""Routing table — turn a classified intent into an agent destination."""
import yaml
import os


class Router:
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), "config.yaml")))
        self.table = cfg["routing"]

    def route(self, intent):
        """intent (str) -> list of agent names."""
        i = (intent or "").strip().lower()
        # normalize synonyms
        if i in ("sales", "quote", "order", "purchase", "buy"):
            return self.table.get("sales", ["pulp", "jane"])
        if i in ("hr", "hiring", "job", "employment"):
            return self.table.get("hr", ["feelix"])
        if i in ("legal", "compliance", "contract"):
            return self.table.get("legal", ["redactor"])
        if i in ("security", "threat", "breach"):
            return self.table.get("security", ["sentinel"])
        if i in ("support", "repair", "help", "broken", "technician"):
            return self.table.get("support", ["fiber", "boxtron"])
        if i in ("logistics", "shipping", "delivery"):
            return self.table.get("logistics", ["boxtron"])
        return self.table.get("catch_all", ["clippy-42"])
