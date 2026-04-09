#!/usr/bin/env python3
"""
Debug script to test brain components
"""

import sys
sys.path.insert(0, '.')

print("=" * 60)
print("AOS Brain Component Debug")
print("=" * 60)

# Test 1: Config loading
print("\n[1] Testing config loading...")
try:
    from pathlib import Path
    import yaml
    
    CONFIG_PATH = Path.home() / ".aos" / "config" / "brain.yaml"
    
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            cfg = yaml.safe_load(f)
        print(f"✅ Config loaded: {CONFIG_PATH}")
        print(f"    Tick interval: {cfg['brain']['ooda']['tick_interval_ms']}ms")
    else:
        print(f"⚠️  Config not found at {CONFIG_PATH}, trying fallback...")
        local_cfg = Path(__file__).parent / "config" / "brain.yaml"
        if local_cfg.exists():
            with open(local_cfg, "r") as f:
                cfg = yaml.safe_load(f)
            print(f"✅ Fallback config loaded")
        else:
            print(f"❌ No config found")
            cfg = None
except Exception as e:
    print(f"❌ Config error: {e}")
    import traceback
    traceback.print_exc()
    cfg = None

# Test 2: Import OODA
print("\n[2] Testing OODA import...")
try:
    from ooda import OODA
    print("✅ OODA imported")
except Exception as e:
    print(f"❌ OODA import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Initialize OODA
print("\n[3] Testing OODA initialization...")
try:
    if cfg:
        ooda = OODA(cfg)
        print("✅ OODA initialized")
        print(f"    Thalamus: {type(ooda.thalamus).__name__}")
        print(f"    Hippocampus: {type(ooda.hippo).__name__}")
        print(f"    Using ChromaDB: {ooda.hippo.using_chroma}")
        print(f"    Memory count: {ooda.hippo.total_traces}")
    else:
        print("❌ Cannot initialize without config")
except Exception as e:
    print(f"❌ OODA init failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Run a tick
print("\n[4] Testing OODA tick...")
try:
    if cfg:
        ooda.tick()
        print("✅ Tick executed successfully")
        
        # Check state
        import json
        state_path = Path("~/.aos/brain/state/brain_state.json").expanduser()
        if state_path.exists():
            with open(state_path) as f:
                state = json.load(f)
            print(f"    State tick: {state.get('tick')}")
            print(f"    Memory clusters: {state.get('memory_nn', {}).get('clusters')}")
            print(f"    Novelty: {state.get('limbic', {}).get('novelty')}")
        else:
            print("⚠️  State file not created yet")
    else:
        print("❌ Cannot tick without config")
except Exception as e:
    print(f"❌ Tick failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Debug complete")
print("=" * 60)
