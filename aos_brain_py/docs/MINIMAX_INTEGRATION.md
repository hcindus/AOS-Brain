# MiniMax Integration Guide

## Overview

Integrate MiniMax AI API (MiniMax-M2.5 model) with the 7-Region Ternary Brain + Heart + Stomach system.

## What is MiniMax?

MiniMax is a Chinese LLM provider offering:
- **MiniMax-M2.5**: State-of-the-art language model
- **API Base**: `https://api.minimax.io` (global) or `https://api.minimaxi.com` (China)
- **MCP Support**: Model Context Protocol for extended capabilities

## Integration Architecture

```
MiniMax API Query → Stomach → Heart → Brain → Response
     (Input)         (Digest)  (Rhythm) (Cognition)
```

## Full Pipeline Flow

```
┌──────────────┐    ┌──────────┐    ┌────────┐    ┌────────┐    ┌──────────┐
│  MiniMax     │───→│ Stomach  │───→│ Heart  │───→│ Brain  │───→│ Response │
│  API Query   │    │ (Digest) │    │(Rhythm)│    │(Cognition)│   │          │
└──────────────┘    └──────────┘    └────────┘    └────────┘    └──────────┘
```

## Installation

1. Ensure all components are available:
```python
from integration.minimax_brain_adapter import MiniMaxBrainAdapter
from brain.seven_region import SevenRegionBrain
from heart.ternary_heart import TernaryHeart
from stomach.ternary_stomach import TernaryStomach
```

2. Create the integrated system:
```python
brain = SevenRegionBrain()
heart = TernaryHeart()
stomach = TernaryStomach()
adapter = MiniMaxBrainAdapter(brain, heart, stomach)
```

## Configuration

MiniMax config is auto-loaded from `~/.mini-agent/config/config.yaml`:

```yaml
api_key: "YOUR_MINIMAX_API_KEY"
api_base: "https://api.minimax.io"
model: "MiniMax-M2.5"
provider: "anthropic"
```

## Usage

### Process Query Through Pipeline

```python
result = adapter.process_query(
    query="What is the meaning of consciousness?",
    context="philosophy"
)

print(f"Chunks processed: {result['chunks_processed']}")
print(f"Heart state: {result['heart_state']}")
print(f"Brain ticks: {result['brain_ticks']}")
print(f"Stomach status: {result['stomach_status']}")
```

### Simulate MiniMax Response

```python
response = adapter.simulate_minimax_response(
    prompt="Explain neural networks"
)
print(response)
```

### Test Full Integration

```python
adapter.test_integration()
```

## How It Works

1. **Stomach Phase**: Query is chunked and consumed by stomach
2. **Digestion Phase**: Stomach digests chunks (complexity reduction)
3. **Heart Phase**: Heart beats, provides rhythm and emotional context
4. **Brain Phase**: Each chunk fed to 7-region brain for cognition
5. **Response Phase**: Brain state influences response generation

## Stomach-Heart-Brain Coordination

### Stomach Role
- **Consumes**: MiniMax queries (chunked)
- **Digests**: Reduces complexity before brain feeding
- **State**: HUNGRY → SATISFIED → FULL
- **Output**: Digested chunks ready for brain

### Heart Role
- **Rhythm**: Sets processing pace (BPM)
- **Emotion**: Provides emotional tone/context
- **Coherence**: Tracks heart-brain coherence
- **State**: REST → BALANCE → ACTIVE

### Brain Role
- **Cognition**: 7-region OODA loop processing
- **Memory**: Hippocampal cluster formation
- **Learning**: Pattern recognition from queries
- **Response**: Context-aware output

## API Reference

### MiniMaxBrainAdapter Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `process_query(query, context)` | Full pipeline processing | Dict with full status |
| `simulate_minimax_response(prompt)` | Brain-influenced response | String |
| `test_integration()` | Run integration test | Dict |

### Response Structure

```python
{
    "query": "original query",
    "chunks_processed": 3,
    "heart_state": {
        "bpm": 72.0,
        "coherence": 0.49,
        "state": "BALANCE"
    },
    "brain_ticks": 42,
    "brain_clusters": 42,
    "stomach_status": "🍽️ Stomach: SATISFIED...",
    "responses": [...]
}
```

## Example

```python
from integration.minimax_brain_adapter import MiniMaxBrainAdapter
from brain.seven_region import SevenRegionBrain
from heart.ternary_heart import TernaryHeart
from stomach.ternary_stomach import TernaryStomach

# Initialize full system
brain = SevenRegionBrain()
heart = TernaryHeart()
stomach = TernaryStomach()
adapter = MiniMaxBrainAdapter(brain, heart, stomach)

# Process through complete pipeline
result = adapter.process_query(
    "Explain quantum computing",
    context="physics"
)

# Check system state
print(f"Heart BPM: {heart.get_state_summary()}")
print(f"Brain clusters: {brain.regions['hippocampus'].get_cluster_count()}")
print(f"Stomach energy: {stomach.energy_level}")

# Generate response
response = adapter.simulate_minimax_response("Explain quantum computing")
print(response)
```

## Benefits

1. **Emotional Context**: Heart adds emotional intelligence to responses
2. **Cognitive Depth**: Brain provides deeper understanding than raw API
3. **Learning**: System learns from every MiniMax interaction
4. **Rhythm**: Heart sets natural conversation pace
5. **Memory**: Previous queries inform future responses

## File Locations

- **Adapter**: `aos_brain_py/integration/minimax_brain_adapter.py`
- **Config**: `~/.mini-agent/config/config.yaml`
- **Brain**: `aos_brain_py/brain/seven_region.py`
- **Heart**: `aos_brain_py/heart/ternary_heart.py`
- **Stomach**: `aos_brain_py/stomach/ternary_stomach.py`

## MCP Integration

MiniMax can use MCP servers:

```json
{
    "mcpServers": {
        "minimax_search": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/MiniMax-AI/minimax_search", "minimax-search"]
        }
    }
}
```

Brain-stomach-heart pipeline processes MCP tool outputs same as queries.

## Production Deployment

1. **Setup MiniMax**: Configure API key in `~/.mini-agent/config/config.yaml`
2. **Initialize Pipeline**: Create adapter with brain-heart-stomach
3. **Route Queries**: Send all MiniMax queries through `process_query()`
4. **Monitor**: Track heart coherence, brain clusters, stomach energy
5. **Scale**: Pipeline handles concurrent queries via stomach queue

## Troubleshooting

**Issue**: Slow response times
- Normal: Pipeline adds overhead for digestion/cognition
- Heart BPM affects processing speed
- Stomach complexity affects digestion time

**Issue**: Heart state stuck
- Check: `heart.get_state_summary()`
- Heart auto-adjusts based on brain feedback
- Manual: `heart.beat()` to force cycle

**Issue**: Stomach not digesting
- Check queue: `len(stomach.stomach_queue)`
- Digest manually: `stomach.digest()`
- Reduce complexity: Lower complexity parameter

## Version

- **Adapter Version**: 1.0
- **Brain Compatibility**: 7-Region Ternary Brain v1.0+
- **Heart Compatibility**: Ternary Heart v1.0+
- **Stomach Compatibility**: Ternary Stomach v1.0+
- **MiniMax Model**: MiniMax-M2.5

---

*Integration created: 2026-03-28*
*Git Commit: 44 (bab2926)*
