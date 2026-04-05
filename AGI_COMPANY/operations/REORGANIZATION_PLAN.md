# AGI Company Repository Reorganization Plan

**Project Owner:** Jordan (Project Manager AGI Agent)  
**Date:** 2026-03-28  
**Status:** IN PROGRESS

---

## Executive Summary

This plan outlines the consolidation of scattered files and directories across the repository into a unified AGI_COMPANY/ structure. The goal is to create a clean, organized hierarchy where files are logically grouped by company/subsidiary and purpose.

---

## Current State Analysis

### Source Directories (to be consolidated)

1. **aocros/agent_sandboxes/** - 58 agent directories containing agent configurations, sandboxes, and workspaces
2. **aocros/games/** - Game assets, blueprints, scripts, and game-related files
3. **aocros/sales/** - Sales materials, CRM data, cadence, scripts, and templates
4. **aocros/marketing/** - Marketing campaigns and templates
5. **aocros/AGI_COMPANY_WEBSITES/** - Website files for multiple subsidiaries
6. **Dusty/sales/** - DUSTY subsidiary sales materials
7. **Cream/sales/** - CREAM subsidiary sales materials
8. **agent_sandboxes/** (root) - Jordan's sandbox

### Target Structure

```
AGI_COMPANY/
├── agents/                    # Agent sandboxes organized by tier
│   ├── tier1/
│   ├── tier2/
│   ├── tier3/
│   └── technical/
├── subsidiaries/
│   ├── MILKMAN_GAMES/        # Game development subsidiary
│   │   ├── assets/
│   │   ├── src/
│   │   └── hardware/
│   ├── PERFORMANCE_SUPPLY_DEPOT/  # Sales & marketing subsidiary
│   │   ├── sales/
│   │   ├── marketing/
│   │   └── website/
│   ├── DUSTY/                # QA/testing subsidiary
│   │   └── sales/
│   └── CREAM/                # Desktop software subsidiary
│       └── sales/
└── ... (existing structure preserved)
```

---

## Consolidation Tasks

### Phase 1: Agent Sandboxes → AGI_COMPANY/agents/

**Source:** `aocros/agent_sandboxes/` (58 directories)  
**Target:** `AGI_COMPANY/agents/`

Agent organization by tier:
- **Tier 1 (Core Sales/Marketing):** miles, jordan, jane, dusty, executive, greet, judy
- **Tier 2 (Support/Technical):** bugcatcher, cryptonio, qora, sentinel, pipeline, taptap, stacktrace
- **Tier 3 (Specialized):** harper, fiber, clerk, velvet, ledger, r2-d2, mylfours, mylsixes, mylonen, etc.
- **Technical/Development:** blender-expert, unity-expert, unreal-expert
- **Personal:** personal
- **Legacy:** mortimer, mylzeon, mylzeron, etc.

**Action:** Move all agent sandboxes to AGI_COMPANY/agents/, preserving directory structure.

### Phase 2: Games → MILKMAN_GAMES

**Source:** `aocros/games/`  
**Target:** `AGI_COMPANY/subsidiaries/MILKMAN_GAMES/`

Contents:
- ChronospaceExplorer/
- SGVD/
- assets/
- blueprints/
- daverse/
- scripts/

**Action:** Merge with existing MILKMAN_GAMES structure. Review for duplicates.

### Phase 3: Sales Materials → PERFORMANCE_SUPPLY_DEPOT/sales/

**Source:** `aocros/sales/`  
**Target:** `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/sales/`

Contents:
- cadence/
- crm/
- guides/
- office-manager/
- playbook/
- products/
- psdepot/
- scripts/
- templates/

**Action:** Merge with existing sales structure. Review and deduplicate.

### Phase 4: Marketing → PERFORMANCE_SUPPLY_DEPOT/marketing/

**Source:** `aocros/marketing/`  
**Target:** `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/marketing/`

Contents:
- campaigns/
- templates/

**Action:** Merge with existing marketing structure.

### Phase 5: Websites → PERFORMANCE_SUPPLY_DEPOT/website/

**Source:** `aocros/AGI_COMPANY_WEBSITES/`  
**Target:** `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/website/`

Contents:
- am-hud-supply/
- deploy_packages/
- myl0nr0s/
- performance-supply-depot/
- portal/

**Action:** Merge with existing website structure. Review for conflicts.

### Phase 6: Subsidiary Sales Directories

**Source:** `Dusty/sales/` → `AGI_COMPANY/subsidiaries/DUSTY/sales/`  
**Source:** `Cream/sales/` → `AGI_COMPANY/subsidiaries/CREAM/sales/`  
**Source:** `agent_sandboxes/jordan/` → `AGI_COMPANY/agents/jordan/`

**Action:** Move contents to target locations.

---

## Execution Rules

1. **Preserve all important data** - Never delete without review
2. **Delete only obvious temp/backup files** - *.tmp, *.bak, *.log (if stale)
3. **Update file paths in scripts** - Search for hardcoded paths in moved files
4. **Maintain git history** - Use git mv where possible for tracking
5. **Commit incrementally** - One phase per commit for clarity
6. **Document conflicts** - Note any files that can't be auto-merged

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Broken references in scripts | High | Medium | Search/replace paths after move |
| Duplicate files | Medium | Low | Compare before overwriting |
| Missing files | Low | High | Verify with find + md5sum |
| Git tracking issues | Medium | Low | Use git mv, verify with git status |

---

## Progress Tracker

- [x] Phase 1: Agent Sandboxes - COMPLETED
- [x] Phase 2: Games - COMPLETED
- [x] Phase 3: Sales Materials - COMPLETED
- [x] Phase 4: Marketing - COMPLETED
- [x] Phase 5: Websites - COMPLETED
- [x] Phase 6: Subsidiary Sales - COMPLETED (verified empty)
- [x] Clean up temp files - COMPLETED (no temp files found)
- [x] Final verification - COMPLETED
- [x] Complete documentation - COMPLETED

---

## Post-Migration Tasks

1. Update AGENTS.md with new paths
2. Update any README files referencing old locations
3. Create migration summary report
4. Archive old directories (after verification)
