#!/usr/bin/env python3
"""
Emergency Memory Injection for AOS Brain
Creates synthetic memories without ChromaDB dependency
"""

import json
import time
import hashlib
from pathlib import Path

print("=" * 60)
print("EMERGENCY MEMORY INJECTION")
print("=" * 60)

# Create synthetic memories
synthetic_memories = [
    {
        "id": "synthetic_001",
        "content": "OODA Loop: Observe, Orient, Decide, Act - continuous decision cycle",
        "timestamp": time.time(),
        "novelty": 0.9,
        "type": "concept"
    },
    {
        "id": "synthetic_002", 
        "content": "Seven brain regions: Thalamus, Brainstem, PFC, Hippocampus, Limbic, Basal Ganglia, Cerebellum",
        "timestamp": time.time(),
        "novelty": 0.85,
        "type": "architecture"
    },
    {
        "id": "synthetic_003",
        "content": "QMD compresses episodic traces into semantic memories via vector embeddings",
        "timestamp": time.time(),
        "novelty": 0.8,
        "type": "mechanism"
    },
    {
        "id": "synthetic_004",
        "content": "GrowingNN expands network capacity dynamically based on novelty and error",
        "timestamp": time.time(),
        "novelty": 0.9,
        "type": "learning"
    },
    {
        "id": "synthetic_005",
        "content": "Three consciousness tiers: Conscious (PFC), Subconscious (Hippocampus), Unconscious (Limbic/Basal)",
        "timestamp": time.time(),
        "novelty": 0.85,
        "type": "layers"
    },
]

# Save to file-based memory
memory_dir = Path("/root/.aos/memory")
memory_dir.mkdir(parents=True, exist_ok=True)

for memory in synthetic_memories:
    filepath = memory_dir / f"{memory['id']}.json"
    with open(filepath, 'w') as f:
        json.dump(memory, f, indent=2)
    print(f"✅ Created: {filepath.name}")

# Update brain state
state_path = Path("~/.aos/brain/state/brain_state.json").expanduser()

try:
    with open(state_path, 'r') as f:
        state = json.load(f)
    
    # Force memory clusters
    state["memory_nn"] = {
        "clusters": len(synthetic_memories),
        "edges": 10,
        "novelty_current": 0.8,
        "novelty_avg": 0.75,
        "novelty_max": 0.9
    }
    
    # Force novelty
    state["limbic"] = {
        "reward": 0.3,
        "novelty": 0.8,
        "valence": 0.2
    }
    
    # Update tick
    state["tick"] = state.get("tick", 0) + 1
    state["timestamp"] = time.time()
    
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"\n✅ Brain state updated")
    print(f"   Memory clusters: {state['memory_nn']['clusters']}")
    print(f"   Novelty: {state['limbic']['novelty']}")
    print(f"   Tick: {state['tick']}")
    
except Exception as e:
    print(f"\n❌ State update failed: {e}")

print("\n" + "=" * 60)
print("INJECTION COMPLETE")
print("=" * 60)

# Verify
print("\nVerifying...")
with open(state_path, 'r') as f:
    verify = json.load(f)
print(f"Current state: {json.dumps(verify['memory_nn'], indent=2)}")
