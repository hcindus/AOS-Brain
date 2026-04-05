import time
from pathlib import Path
import yaml

from ooda import OODA

CONFIG_PATH = Path.home() / ".aos" / "config" / "brain.yaml"

def load_config():
    # Make sure we don't crash if config is missing during initial run in workspace
    if not CONFIG_PATH.exists():
        # Fallback to local config if running from workspace without installing
        local_cfg = Path(__file__).parent.parent / "config" / "brain.yaml"
        if local_cfg.exists():
            with open(local_cfg, "r") as f:
                return yaml.safe_load(f)
    
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def main():
    cfg = load_config()
    ooda = OODA(cfg)
    print("AOS brain starting (NN–OODA loop)...")

    tick_ms = cfg["brain"]["ooda"]["tick_interval_ms"]
    while True:
        ooda.tick()
        time.sleep(tick_ms / 1000.0)

if __name__ == "__main__":
    main()
