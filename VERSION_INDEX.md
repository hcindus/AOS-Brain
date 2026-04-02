# VERSION_INDEX.md - Global Version Registry
# AOS / AGI Company - Centralized Version Tracking
# Format: YYYY-MM-DD.HHMM - Incremental builds same day get .001, .002 etc

## Global System Version
**Current: 2026.04.02.0408** (build 2026-04-02 04:08 UTC)

---

## Core Systems

| System | Version | Last Updated | File |
|--------|---------|--------------|------|
| **Miles (Main Agent)** | 4.2.1 | 2026-04-02 | `IDENTITY.md` |
| **Complete Brain v4** | 4.0.0 | 2026-04-01 | `HEARTBEAT.md` |
| **AGENTS.md** | 2.0 | 2026-03-31 | `AGENTS.md` |
| **Keepalive System** | 1.0.0 | 2026-04-02 | `scripts/*_keepalive.sh` |
| **Version Index** | 1.0.0 | 2026-04-02 | This file |

---

## Subsidiaries & Projects

| Entity | Version | Status | Path |
|--------|---------|--------|------|
| **AGI Company (Parent)** | 3.0.0 | Active | `AGI_COMPANY/` |
| **Performance Supply Depot** | 2.1.0 | Active | `aocros/performance_supply_depot/` |
| **CREAM Realty** | 1.0.0 | Active | `AGI_COMPANY/subsidiaries/CREAM/` |
| **AOCROS** | 4.0.0 | Active | `aocros/` |
| **Cobra Robot** | See file | R&D | `AGI_COMPANY/research/cobra_robot/` |
| **Humanoid** | See file | R&D | `AGI_COMPANY/research/humanoid/` |

---

## Scripts & Tools

| Script | Version | Purpose |
|--------|---------|---------|
| `agent_keepalive.sh` | 1.0.0 | Unified agent monitoring |
| `ollama_keepalive.sh` | 1.0.0 | Model residency |
| `aos_keepalive.sh` | 1.0.0 | Brain health check |
| `minecraft_keepalive.sh` | 1.0.0 | MC agent health |
| `minecraft_agent_rotation.py` | 2.0 | Agent rotation |
| `ca_sos_scraper.js` | 1.0 | Lead scraper |
| `sync_prices.py` | 1.0 | Price sync |

---

## Change Log

### 2026-04-02.0408 - Build 0408
- Added unified keepalive system
- Version indexing implementation
- All agent systems covered

### 2026-04-01.0451 - Build 0451
- Complete Brain v4 deployed
- Mission Control active
- 1,300+ curriculum items fed

---

## Version Format Rules

**Files:** Add header block:
```
<!--
VERSION: 1.0.0
UPDATED: 2026-04-02 04:08 UTC
PREVIOUS: 0.9.0
CHANGELOG: Description of changes
-->
```

**Scripts:** Add header:
```bash
#!/bin/bash
# VERSION: 1.0.0
# UPDATED: 2026-04-02 04:08 UTC
```

**Bump version when:**
- Any material change to logic/functionality
- Configuration updates
- Dependencies change
- Performance improvements

---

## Auto-Versioning

Cron: `version_bump.sh` runs with git commits
- Auto-increments patch (1.0.x) for minor changes
- Manual bump required for minor/major versions
- All files updated: `VERSION_INDEX.md`
