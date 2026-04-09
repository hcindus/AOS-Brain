#!/usr/bin/env python3
"""
Minimal Brain - No blocking components
Ensures logic flows and grows
"""

import time
import json
from pathlib import Path

# Minimal state
state = {
    "tick": 0,
    "timestamp": time.time(),
    "phase": "Observe",
    "mode": "Minimal",
    "limbic": {"novelty": 0.8, "reward": 0.3},
    "memory_nn": {"clusters": 0},
    "policy_nn": {"layers": 3, "nodes": [8, 12, 40]}
}

STATE_PATH = Path.home() / ".aos" / "brain" / "state" / "brain_state.json"

def save_state():
    """Save current state to file"""
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)

def tick():
    """Minimal OODA tick"""
    global state
    
    state["tick"] += 1
    state["timestamp"] = time.time()
    
    # Cycle through phases
    phases = ["Observe", "Orient", "Decide", "Act"]
    current_idx = phases.index(state["phase"]) if state["phase"] in phases else 0
    state["phase"] = phases[(current_idx + 1) % len(phases)]
    
    # Simulate memory formation
    if state["tick"] % 10 == 0:
        state["memory_nn"]["clusters"] += 1
        print(f"[Brain] Tick {state['tick']}, Memories: {state['memory_nn']['clusters']}")
    
    # Simulate GrowingNN growth
    if state["tick"] % 50 == 0 and len(state["policy_nn"]["nodes"]) > 0:
        # Add node to output layer
        state["policy_nn"]["nodes"][-1] += 1
        print(f"[Brain] GrowingNN expanded: {state['policy_nn']['nodes'][-1]} nodes")
    
    save_state()

print("=" * 60)
print("MINIMAL BRAIN - Logic Flowing and Growing")
print("=" * 60)

# Load existing state if available
try:
    if STATE_PATH.exists():
        with open(STATE_PATH) as f:
            loaded = json.load(f)
            state["tick"] = loaded.get("tick", 0)
            state["memory_nn"]["clusters"] = loaded.get("memory_nn", {}).get("clusters", 0)
            print(f"Resumed from tick {state['tick']}")
except:
    pass

print(f"Starting from tick {state['tick']}")
print("Press Ctrl+C to stop")
print("=" * 60)

try:
    while True:
        tick()
        time.sleep(0.1)  # 10 ticks/second
except KeyboardInterrupt:
    print("\nBrain stopped")
    save_state()
