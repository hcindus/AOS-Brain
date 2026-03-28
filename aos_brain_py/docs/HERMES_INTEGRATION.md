# Hermes Integration Guide

## Overview

Integrate OpenClaw's Hermes state system (`~/.local/state/hermes/`) with the 7-Region Ternary Brain.

## What is Hermes?

Hermes is OpenClaw's state persistence system. It stores:
- Gateway state files
- Session persistence
- Agent coordination data
- Lock files for distributed operations

## Integration Architecture

```
Hermes State Files (JSON) ←→ HermesBrainAdapter ←→ 7-Region Brain
     ~/.local/state/hermes/      (Bridge Layer)      Hippocampal Memory
```

## Installation

1. Ensure brain components are available:
```python
from integration.hermes_brain_adapter import HermesBrainAdapter
from brain.seven_region import SevenRegionBrain
```

2. Create the adapter:
```python
brain = SevenRegionBrain()
adapter = HermesBrainAdapter(brain)
```

## Usage

### Sync Hermes to Brain

```python
# Read state from Hermes and feed to brain
adapter.sync_to_brain("session_state")
adapter.sync_to_brain("gateway_state")
adapter.sync_to_brain("agent_state")
```

### Sync Brain to Hermes

```python
# Write brain state back to Hermes
adapter.sync_from_brain("brain_status", "current_query")
```

### Bidirectional Sync

```python
# Run full bidirectional synchronization
adapter.bidirectional_sync()
```

## How It Works

1. **Read Phase**: Adapter reads JSON state files from `~/.local/state/hermes/`
2. **Digest Phase**: State content is formatted and fed to brain via stomach pipeline
3. **Learn Phase**: Brain creates hippocampal clusters for each state entry
4. **Write Phase**: Brain status (ticks, clusters, queries) saved back to Hermes

## API Reference

### HermesBrainAdapter Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `read_hermes_state(key)` | Read state file | `key`: filename without .json |
| `write_hermes_state(key, data)` | Write state file | `key`: filename, `data`: dict |
| `sync_to_brain(key)` | Sync Hermes → Brain | `key`: state file to sync |
| `sync_from_brain(key, query)` | Sync Brain → Hermes | `key`: output file, `query`: context |
| `bidirectional_sync()` | Full sync | None |
| `test_integration()` | Test the integration | None |

## Example

```python
from integration.hermes_brain_adapter import HermesBrainAdapter
from brain.seven_region import SevenRegionBrain

# Initialize
brain = SevenRegionBrain()
adapter = HermesBrainAdapter(brain)

# Sync session state to brain
adapter.sync_to_brain("session_state")

# Brain now has session data in memory
print(f"Brain ticks: {brain.tick_count}")
print(f"Clusters: {brain.regions['hippocampus'].get_cluster_count()}")

# Sync brain status back
adapter.sync_from_brain("brain_mirror", "session_sync")
```

## File Locations

- **Hermes Path**: `~/.local/state/hermes/`
- **State Files**: `{key}.json`
- **Adapter**: `aos_brain_py/integration/hermes_brain_adapter.py`

## State Persistence

Brain state persists across restarts via:
1. Hermes JSON files (structured data)
2. Brain hippocampal clusters (learned patterns)
3. Bidirectional sync keeps both in sync

## Troubleshooting

**Issue**: State not appearing in brain
- Check: `adapter.hermes_path.exists()`
- Ensure state files are valid JSON

**Issue**: Sync slow
- Normal: Each sync triggers brain tick cycle
- Optimization: Batch multiple states before sync

## Version

- **Adapter Version**: 1.0
- **Brain Compatibility**: 7-Region Ternary Brain v1.0+
- **Hermes Version**: OpenClaw standard

---

*Integration created: 2026-03-28*
*Git Commit: 44 (bab2926)*
