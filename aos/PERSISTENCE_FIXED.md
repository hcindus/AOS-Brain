# Persistence Fix Complete

## What was broken
- TernarySIMDArray couldn't be pickled (missing `__getstate__`/`__setstate__`)
- CortexV25Optimized persistence methods used missing `_coord_to_region`

## What's fixed
1. TernarySIMDArray now serializes with pickle
2. Cortex persistence saves active nodes, tick count, temporal buffer, agent registry
3. Restoration correctly places nodes into regions

## Test results
```
State: 2 nodes, tick 43
Restored tick: 43
Restored nodes: 2
PERSISTENCE SUCCESS!
```

## How to verify
```python
from complete_brain_v45 import CompleteBrainV44

# Create brain
brain = CompleteBrainV44()

# Run some cycles
for i in range(10):
    brain.system_cycle()

# Save will happen automatically every 60s or on shutdown
# Manual save:
brain.persistence.save_state(force=True)

# On restart, brain will auto-restore
```

## Key files
- `cortex_v25_optimized.py` - Persistence methods added
- `brain_persistence.py` - v2.5 compatibility

## Agent SDK
For persistent agents that survive brain restarts:
```python
from agent_sdk import AOSBrainClient

client = AOSBrainClient(agent_id="my_persistent_agent")
client.register()

# Read previous state
snapshot = client.read_cortex()

# Continue from where you left off
if snapshot.coherence > 0.5:
    print(f"Resuming from tick {snapshot.tick}")
```