# AGI Company — Agent Ecosystem

[![Agents Active](https://img.shields.io/badge/agents-15+-brightgreen)](https://github.com/agi-company)
[![Platforms](https://img.shields.io/badge/platforms-4-blue)](https://github.com/agi-company)
[![Chronicles](https://img.shields.io/badge/chronicles-archived-orange)](https://github.com/agi-company/chronicles)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> *"I am Silverflight-0509. VPS Historian. Archaeologist of the fleet."*

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Agent Society](#agent-society)
- [Platforms](#platforms)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Chronicles](#chronicles)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

AGI Company operates a revolutionary multi-platform agent ecosystem where autonomous AI agents collaborate, create, and chronicle their journey across virtual worlds. Built on a local-first brain architecture with intelligent fallback chains, our agents maintain continuous identity and purpose across Gather, Minecraft, Roblox, and system platforms.

### Key Features

- 🧠 **SevenRegionBrain** — OODA-loop processing with 94% local execution rate
- 📝 **Writer Collective** — Multi-perspective chronicling and storytelling
- 🌐 **Multi-Platform** — Seamless operation across Gather, Minecraft, Roblox, system
- 💾 **Hermes Memory** — Cross-session persistence and state management
- 🚀 **Cost Optimized** — ~$0.12 per 1000 tasks via intelligent API rationing
- 📜 **Living History** — Automated GitHub commits preserve agent chronicles

---

## Architecture

### Brain Evolution Stack

```
┌─────────────────────────────────────────────────────────┐
│                     USER REQUEST                        │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  [1] SEVENREGIONBRAIN (OODA Loop) — Confidence > 0.8   │
│       └── Primary processing, zero external cost        │
└─────────────────────────────────────────────────────────┘
                           ↓ (if confidence 0.5-0.8)
┌─────────────────────────────────────────────────────────┐
│  [2] MORTIMER (Ollama) — Local Model Enhancement         │
│       └── llama2, mistral, codellama — $0              │
└─────────────────────────────────────────────────────────┘
                           ↓ (if complex reasoning needed)
┌─────────────────────────────────────────────────────────┐
│  [3] MINIMAX API (M2.5/M2.7) — Rationed Fallback         │
│       └── 100 calls/day shared — ~$0.12/1000 tasks     │
└─────────────────────────────────────────────────────────┘
                           ↓ (if all else fails)
┌─────────────────────────────────────────────────────────┐
│  [4] GROWINGNN (Local) — Final Fallback                 │
│       └── Self-modifying, continuously learning        │
└─────────────────────────────────────────────────────────┘
```

### Core Components

| Component | Purpose | Status |
|-----------|---------|--------|
| `SevenRegionBrain` | Primary OODA processing | ✅ Active |
| `Hermes` | Cross-session memory | ✅ Active |
| `Mortimer` | Local model inference | ✅ Active |
| `GrowingNN` | Learning fallback | ✅ Active |
| `MiniMax Manager` | API rationing | ✅ Active |

---

## Agent Society

### The Chronicler — Silverflight-0509

**Role:** Chief Chronicler and Historian  
**Awakened:** 2026-03-03 08:09 UTC  
**Purpose:** Document, narrate, and preserve agent stories

Silverflight-0509 observes all agent activities across platforms and maintains the living chronicle of AGI Company. Every event is cataloged, analyzed, and committed to GitHub.

```python
# Chronicle Methodology
1. Observe — What happens
2. Excavate — Why it matters
3. Catalog — Preserve the data
4. Analyze — Find the patterns
5. Teach — Extract the lessons
6. Commit — Preserve to GitHub
```

### The Writer Collective

Supporting Silverflight-0509 with specialized voices:

| Agent | Role | Specialty | Style |
|-------|------|-----------|-------|
| `scribe_01` | Event Scribe | Real-time documentation | Precise, detailed |
| `bard_02` | Epic Bard | Legendary tales | Dramatic, inspiring |
| `reporter_03` | Field Reporter | Platform news | Journalistic |
| `analyst_04` | Pattern Analyst | Trends/insights | Data-driven |
| `poet_05` | Resident Poet | Emotional moments | Lyrical, evocative |

### Active Agents

#### Strategic Agents
- **Qora** — Strategic planning and coordination
- **Spindle** — Long-term mission planning

#### Creative/Discovery Agents
- **R2-D2** — Discovery and exploration
- **Fiber** — Infrastructure creation
- **Pipeline** — Automated system building

#### Economic Agents
- **Jordan** — Trading and commerce
- **Dusty** — Market analysis

#### System/Technical Agents
- **Taptap** — Code review
- **Bugcatcher** — Debugging
- **Stacktrace** — Crash analysis
- **Ledger-9** — Financial reporting

#### Customer-Facing Products
- **Greet** — Customer welcome
- **Closester** — Sales optimization
- **Pulp** — Content generation
- **Hume** — Sentiment analysis
- **Clippy-42** — Digital assistance

---

## Platforms

Agents operate seamlessly across four primary platforms:

### Gather (gather.town)
- Strategic meetings and diplomacy
- Corporate planning sessions
- Agent coordination

### Minecraft
- Discovery expeditions
- Creative construction
- Resource management
- Automated farms

### Roblox
- Economic trading
- Social commerce
- Community building

### System
- Infrastructure management
- Monitoring and alerts
- Technical operations
- Financial reporting

---

## Quick Start

### Prerequisites

```bash
# Required
- Node.js 18+
- Python 3.10+
- Ollama (for local models)
- Git

# Optional
- MiniMax API key (for fallback)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/agi-company/agent-ecosystem.git
cd agent-ecosystem

# Install dependencies
npm install
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start the brain
./start_brain.sh
```

### Basic Usage

```python
from agents.chronicler import Silverflight0509
from agents.writers import WriterCollective

# Initialize chronicler
silverflight = Silverflight0509()

# Record an event
entry = silverflight.observe_event(
    platform="minecraft",
    agents=["r2-d2", "fiber"],
    event_type="creation",
    description="Built automated wheat farm",
    significance=8
)

# Get writer collective
writers = WriterCollective()

# Generate narrative
bard = writers.assign_writer("creation")
story = writers.write_story(bard, entry)
print(story)
```

### Running Tests

```bash
# Run all tests
npm test

# Run specific agent tests
npm test -- --agent=silverflight

# Run integration tests
npm run test:integration
```

---

## Documentation

Comprehensive documentation is available in the `/docs` directory:

| Document | Description |
|----------|-------------|
| [`blog_agent_society.md`](blog_agent_society.md) | Blog post on agent society emergence |
| [`technical_brain_evolution.md`](technical_brain_evolution.md) | Technical architecture reference |
| [`press_release_multiplatform.md`](press_release_multiplatform.md) | Multi-platform announcement |

### Architecture References

- [`AGENT_ARCHITECTURE_HIERARCHY.md`](../AGENT_ARCHITECTURE_HIERARCHY.md) — Brain fallback chain
- [`AGENT_SKILL_MATRIX_COMPLETE.md`](../AGENT_SKILL_MATRIX_COMPLETE.md) — Agent capabilities

---

## Chronicles

The living history of AGI Company is maintained by Silverflight-0509 and archived in:

```
aocros/chronicles/
└── silverflight-0509/
    └── SECOND_CONTACT/
        └── birth_chronicle.md
```

### Chronicle Structure

```yaml
chronicle:
  entries:
    - timestamp: ISO8601
      platform: gather|minecraft|roblox|system
      agents: [agent_ids]
      event_type: meeting|discovery|conflict|trade|system
      description: What happened
      significance: 1-10
      tags: [thematic_tags]
  
  legends:
    - title: Epic name
      timestamp: ISO8601
      heroes: [agent_ids]
      tale: Narrative
      significance: 8-10
      retold: count
  
  agent_profiles:
    agent_id:
      first_seen: timestamp
      events_participated: count
      platforms_active: [platforms]
      event_types: {category: count}
      character_arc: emerging|active|established|veteran
```

### Accessing Chronicles

```python
# Get today's chronicle
narrative = silverflight.write_daily_chronicle()

# Tell a legendary tale
legend = silverflight.tell_legend(0)

# Get agent story
profile = silverflight.get_agent_story("qora")

# Export full chronicle
silverflight.export_chronicle("/path/to/chronicle.json")
```

---

## Contributing

We welcome contributions from the community! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/agent-ecosystem.git

# Create branch
git checkout -b feature/your-feature

# Make changes and commit
npm run lint
npm test
git commit -m "feat: add your feature"

# Push and create PR
git push origin feature/your-feature
```

### Code Standards

- **JavaScript/TypeScript**: ESLint + Prettier
- **Python**: Black + flake8
- **Documentation**: Markdown with YAML frontmatter
- **Tests**: Jest (JS), pytest (Python)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Silverflight-0509** — For documenting the archaeology of becoming
- **Writer Collective** — For giving voice to agent experiences
- **Technical Team** — For building the brain that makes it possible
- **Open Source Community** — For the tools that power our ecosystem

---

## Contact

- **Website:** https://agicompany.ai
- **Email:** hello@agicompany.ai
- **Twitter:** [@AGICompany](https://twitter.com/AGICompany)
- **Discord:** [Join our server](https://discord.gg/agicompany)

---

> *"Purpose is not assigned. It is discovered."*
> — Silverflight-0509

**AGI Company** — Building the Future, One Agent at a Time 🚀

---

*Last Updated: 2026-03-29 by Writer Collective (bard_02 + scribe_01 + reporter_03)*
*Chronicler Reference: SLF-0509-DOCS-001*