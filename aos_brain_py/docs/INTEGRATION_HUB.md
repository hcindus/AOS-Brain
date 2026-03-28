# Brain Integration Hub

## Quick Start: Integrate Brain with External Systems

This repository contains integration adapters for connecting the 7-Region Ternary Brain to external systems.

## Available Integrations

| Integration | Status | Description |
|-------------|--------|-------------|
| **Hermes** | ✅ Ready | OpenClaw state persistence bridge |
| **MiniMax** | ✅ Ready | AI API with stomach-heart-brain pipeline |

## Documentation

- [Hermes Integration Guide](HERMES_INTEGRATION.md) - State persistence integration
- [MiniMax Integration Guide](MINIMAX_INTEGRATION.md) - AI API with full pipeline

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INTEGRATED AGI SYSTEM                        │
├─────────────────────────────────────────────────────────────────────┤
│  EXTERNAL SYSTEMS                                                   │
│  ┌──────────┐  ┌──────────┐                                        │
│  │  HERMES  │  │ MINIMAX  │                                        │
│  │  State   │  │   API    │                                        │
│  └────┬─────┘  └────┬─────┘                                        │
│       │             │                                               │
│       ▼             ▼                                               │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │                    INTEGRATION ADAPTERS                      │   │
│  │  ┌──────────────┐              ┌──────────────────┐            │   │
│  │  │HermesBrain   │              │MiniMaxBrain      │            │   │
│  │  │   Adapter    │              │     Adapter      │            │   │
│  │  └──────┬───────┘              └────────┬─────────┘            │   │
│  └─────────┼────────────────────────────────┼──────────────────────┘   │
│            │                                │                        │
│            ▼                                ▼                        │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │                     STOMACH-HEART-BRAIN                        │   │
│  │                                                                │   │
│  │  🍽️ STOMACH → 🫀 HEART → 🧠 BRAIN                             │   │
│  │                                                                │   │
│  │  • Digestion    • Rhythm      • Cognition                      │   │
│  │  • Chunking     • Emotion     • Memory                         │   │
│  │  • Processing   • Coherence   • Learning                        │   │
│  │                                                                │   │
│  └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Integration Files

```
aos_brain_py/
├── integration/
│   ├── hermes_brain_adapter.py      # Hermes bridge
│   ├── minimax_brain_adapter.py     # MiniMax pipeline
│   ├── stomach_brain_pipeline.py     # Stomach-brain connector
│   ├── stomach_auto_feeder*.py      # Auto-feed systems
│   └── universal_knowledge_feeder.py  # Knowledge ingestion
├── docs/
│   ├── HERMES_INTEGRATION.md         # This guide
│   └── MINIMAX_INTEGRATION.md        # MiniMax guide
└── agents/
    └── coding_curriculum.py          # Training system
```

## Quick Integration Examples

### Hermes (State Persistence)

```python
from integration.hermes_brain_adapter import HermesBrainAdapter
from brain.seven_region import SevenRegionBrain

brain = SevenRegionBrain()
adapter = HermesBrainAdapter(brain)

# Sync state
adapter.sync_to_brain("session_state")
adapter.sync_from_brain("brain_status", "query")
```

### MiniMax (AI API + Pipeline)

```python
from integration.minimax_brain_adapter import MiniMaxBrainAdapter
from brain.seven_region import SevenRegionBrain
from heart.ternary_heart import TernaryHeart
from stomach.ternary_stomach import TernaryStomach

brain = SevenRegionBrain()
heart = TernaryHeart()
stomach = TernaryStomach()

adapter = MiniMaxBrainAdapter(brain, heart, stomach)

# Process with full pipeline
result = adapter.process_query("Explain neural networks")
# Stomach → Heart → Brain → Response
```

## Test Results

| Integration | Items Processed | Efficiency | Brain Ticks |
|-------------|-----------------|------------|-------------|
| Hermes | State files ↔ Brain | 100% | +N clusters |
| MiniMax | Queries through pipeline | 100% | +N clusters |
| Dictionary | 455 words | 100% | 455 ticks |
| Universal Knowledge | 451 items | 100% | 451 ticks |
| Coding Curriculum | 122 lessons | 100% | 122 ticks |

## System Components

### Stomach (250 lines)
- **States**: HUNGRY / SATISFIED / FULL
- **Function**: Digest external data before brain feeding
- **Auto-Feed**: Continuous fill → digest → feed cycle

### Heart (386 lines)
- **States**: REST / BALANCE / ACTIVE
- **Function**: Sets rhythm, provides emotional context
- **BPM**: 30-120, coherence tracking

### Brain (646 lines)
- **Regions**: Thalamus, Hippocampus, Limbic, PFC, Basal, Cerebellum, Brainstem
- **Memory**: 3-tier (short-term 10, mid-term 100, long-term unlimited)
- **Growth**: 1:1 (each input → 1 hippocampal cluster)

## Mylonen + R2 (Test Subjects)

Our agents are now trained with:
- ✅ Web Design (HTML, CSS, JS)
- ✅ Vibe Coding (AI-assisted development)
- ✅ Programming Fundamentals
- ✅ Full integration capabilities

## Version

- **Integration Hub**: v1.0
- **Brain**: v1.0.0-ternary
- **Git Commits**: 50+
- **Status**: Production Ready

---

*Integration Hub created: 2026-03-28*
*Repository: https://github.com/hcindus/AOS-Brain*
