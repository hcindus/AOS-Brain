# AOS AGENT SDK v1.0

## Quick Start

```python
from agent_sdk import AOSBrainClient

# Connect to running brain
client = AOSBrainClient(agent_id="my_agent")

# Register with cortex
client.register()

# Write a thought to cortex
client.write_thought("Processing visual input", priority=0.8)

# Read current state
snapshot = client.read_cortex()
print(f"Coherence: {snapshot.coherence}, Hotspots: {len(snapshot.hotspots)}")

# Check brain status
status = client.get_brain_status()
print(f"Brain tick: {status.tick}, Phase: {status.phase}")
```

## Socket Commands (for any language)

```bash
# Register agent
echo '{"cmd":"cortex_register","params":{"agent_id":"my_agent"}}' | nc -U /tmp/aos_brain.sock

# Write activations
echo '{"cmd":"cortex_write","params":{"agent_id":"my_agent","regions":[0,1],"activations":[[5,5,5,1],[6,6,6,-1]]}}' | nc -U /tmp/aos_brain.sock

# Read state
echo '{"cmd":"cortex_read","params":{"agent_id":"my_agent","regions":[0,1,2,3]}}' | nc -U /tmp/aos_brain.sock

# Get stats
echo '{"cmd":"cortex_stats"}' | nc -U /tmp/aos_brain.sock

# Trigger tick
echo '{"cmd":"cortex_tick"}' | nc -U /tmp/aos_brain.sock
```

## Multi-Agent Coordination

```python
from agent_sdk import MultiAgentCoordinator

coord = MultiAgentCoordinator()

# Create multiple agents
explorer = coord.create_agent("explorer_1")
analyzer = coord.create_agent("analyzer_1")
decider = coord.create_agent("decider_1")

# Agents share brain state
# Each can read/write cortex independently
# Check collective state
collective = coord.get_collective_state()
```

## Persistent Agents

```python
from agent_sdk import AOSBrainClient

agent = AOSBrainClient(agent_id="persistent_agent_1")
agent.register()

# On restart, read previous state
snapshot = agent.read_cortex()
if snapshot.tick > 0:
    print(f"Resuming from tick {snapshot.tick}")
    # Continue previous work
```

## Key Features

| Feature | Description |
|---------|-------------|
| `write_thought()` | Convert text to cortical activations |
| `write_cortex()` | Direct hotspot specification |
| `read_cortex()` | Get sparse snapshot of current state |
| `tick()` | Manually trigger propagation |
| `on_tick()` | Register callback for tick events |
| `ingest()` | Feed content to stomach |
| `perceive()` | Add observation to consciousness |

## Files

- `agent_sdk.py` - Full SDK
- `cortex_v25_optimized.py` - Optimized cortex with agent API
- `production_infra.py` - Vector DB, GPU, distributed consensus

## Production Status

| Component | Status |
|-----------|--------|
| Agent SDK | ✅ Ready |
| Cortex v2.5 | ✅ Integrated |
| Persistence | ✅ Fixed |
| Vector DB | 📝 Ready to use |
| GPU Offload | 📝 Structure ready |
| Distributed | 📝 Raft structure ready |

## Performance

- Python v2.5: ~0.8-1.0ms/tick
- 8 parallel regions
- Sparse ternary storage (8KB vs 32KB)
- Agent read/write: <0.1ms
