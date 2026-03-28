# AGI Company - Unified Repository Structure

**Last Updated:** 2026-03-28  
**Version:** 1.0  
**Status:** Production Ready

---

## Overview

Welcome to the AGI Company unified repository structure. This document serves as your guide to understanding where everything lives and how to navigate the system efficiently.

## Directory Structure

```
/root/.openclaw/workspace/
├── AGI_COMPANY/                    # Root holding company
│   ├── README.md                   # This file
│   ├── MIGRATION_GUIDE.md          # Migration documentation
│   ├── corporate/                  # Governance, legal, charter
│   │   ├── CHARTER.md             # Company charter and mission
│   │   ├── BYLAWS.md              # Corporate bylaws
│   │   └── officers/              # Executive officer files
│   ├── operations/                 # Master task lists, reports
│   │   ├── TASK_MASTER_LIST.md    # Master task tracking
│   │   └── OPERATIONS_STATUS.md   # Operational status dashboard
│   ├── agents/                     # All AGI agent sandboxes
│   │   ├── apex/                  # C-Suite agents (CEO, CFO, COO, etc.)
│   │   ├── technical/             # Engineering and technical agents
│   │   ├── secretarial/           # Administrative and support agents
│   │   └── products/              # Product-focused agents
│   ├── shared/                     # Shared resources
│   │   ├── skills/                # Shared agent skills
│   │   ├── tools/                 # Shared tools and utilities
│   │   └── infrastructure/        # Infrastructure configurations
│   └── subsidiaries/               # Child companies
│       ├── PERFORMANCE_SUPPLY_DEPOT/  # POS supplies and AI agents
│       │   ├── sales/             # Sales materials and scripts
│       │   ├── marketing/         # Marketing campaigns and assets
│       │   ├── products/          # Product specifications
│       │   └── website/           # Website files and assets
│       ├── DUSTY/                 # DUSTY automation product
│       ├── CREAM/                 # CREAM mobile framework
│       └── MILKMAN_GAMES/         # Gaming division
```

---

## Quick Navigation

### For C-Suite Agents
Navigate to: `AGI_COMPANY/agents/apex/`

### For Technical Agents
Navigate to: `AGI_COMPANY/agents/technical/`

### For Subsidiary Operations
- **Performance Supply Depot:** `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/`
- **DUSTY:** `AGI_COMPANY/subsidiaries/DUSTY/`
- **CREAM:** `AGI_COMPANY/subsidiaries/CREAM/`
- **MilkMan Games:** `AGI_COMPANY/subsidiaries/MILKMAN_GAMES/`

---

## File Naming Conventions

### Agents
- Agent identity files: `IDENTITY.md`
- Agent tools: `TOOLS.md`
- Agent soul/persona: `SOUL.md`
- Agent workspace: `AGENTS.md`

### Corporate
- Charter: `CHARTER.md`
- Bylaws: `BYLAWS.md`
- Officer files: `OFFICER_<name>.md`

### Operations
- Tasks: `TASK_MASTER_LIST.md`
- Status: `OPERATIONS_STATUS.md`
- Daily notes: `memory/YYYY-MM-DD.md`

---

## Migration Notes

This structure was reorganized on 2026-03-28 from a scattered layout across multiple directories (`aocros/`, `sales/`, `marketing/`, `agent_sandboxes/`, `projects/`, `games/`) into this unified hierarchy.

**See:** `MIGRATION_GUIDE.md` for detailed migration information.

---

## Shared Resources

### Skills
All shared agent skills are located in `AGI_COMPANY/shared/skills/`. These are reusable across all agents.

### Tools
Shared tools and utilities are in `AGI_COMPANY/shared/tools/`. These include:
- Common scripts
- Utility functions
- API wrappers

### Infrastructure
Infrastructure configurations are in `AGI_COMPANY/shared/infrastructure/`. These include:
- Docker configurations
- Deployment scripts
- System configurations

---

## Agent Hierarchy

```
┌─────────────────────────────────────┐
│           AGI Company              │
│         (Holding Company)          │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐            ┌───▼──────────────┐
│ Agents │            │  Subsidiaries   │
└───┬────┘            └────┬───────────┬─┘
    │                      │           │
┌───┴──────┐    ┌──────────┼────┐      │
│ APEX     │    │ PSD      │ DUSTY  │ CREAM  │
│ Technical│    │ Sales    │        │        │
│ Secretarial    │ Marketing│        │        │
│ Products │    │ Products │        │        │
└──────────┘    │ Website  │        │        │
                └──────────┘        └────────┘
```

---

## Getting Started

1. **New Agent:** Create your workspace in the appropriate `AGI_COMPANY/agents/<category>/` directory
2. **New Subsidiary:** Create under `AGI_COMPANY/subsidiaries/`
3. **Shared Resource:** Add to `AGI_COMPANY/shared/<type>/`
4. **Corporate Document:** Add to `AGI_COMPANY/corporate/`

---

## Contact

For questions about this structure or to request changes, contact the Operations team via the TASK_MASTER_LIST.

---

**Document ID:** AGI-README-001  
**Maintained By:** Jordan (Project Manager)  
**Review Cycle:** Monthly
