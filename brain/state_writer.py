import json
from pathlib import Path

class StateWriter:
    def __init__(self, path):
        self.path = Path(path).expanduser()

    def write(self, state: dict):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(state, f)
