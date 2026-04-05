# AGI Company Repository Migration Guide

**Migration Date:** 2026-03-28  
**Migrated By:** Jordan (Project Manager)  
**Version:** 1.0

---

## Executive Summary

This guide documents the complete reorganization of the AGI Company repository from a scattered, multi-directory structure to a unified, hierarchical organization. All files have been moved from legacy locations to their new standardized homes.

---

## Old vs New Structure

### Before (Legacy Structure)
```
/root/.openclaw/workspace/
├── aocros/                         # AGI Company operations (scattered)
│   ├── agent_sandboxes/           # Agent workspaces
│   ├── sales/                      # Sales materials
│   ├── marketing/                  # Marketing materials
│   ├── corporate/                  # Corporate documents
│   ├── operations/                 # Task lists
│   └── projects/                   # Project files
├── agent_sandboxes/                # Separate agent sandboxes
├── sales/                          # Root-level sales
├── marketing/                      # (missing - was scattered)
├── MilkMan-Game/                   # Gaming division
├── Dusty/                          # DUSTY product
├── Cream/                          # CREAM product
└── ... (scattered files)
```

### After (Unified Structure)
```
/root/.openclaw/workspace/
└── AGI_COMPANY/                    # Unified root
    ├── corporate/                  # Centralized governance
    ├── operations/                 # Centralized operations
    ├── agents/                     # Categorized agents
    ├── shared/                     # Reusable resources
    └── subsidiaries/               # Child companies
```

---

## Detailed Migration Mapping

### 1. Corporate Documents

| Old Location | New Location | Status |
|--------------|--------------|--------|
| `aocros/corporate/` | `AGI_COMPANY/corporate/` | ✅ Migrated |

**Files Migrated:**
- Charter documents → `AGI_COMPANY/corporate/CHARTER.md`
- Bylaws → `AGI_COMPANY/corporate/BYLAWS.md`
- Officer files → `AGI_COMPANY/corporate/officers/`

---

### 2. Operations

| Old Location | New Location | Status |
|--------------|--------------|--------|
| `aocros/TASK_MASTER_LIST.md` | `AGI_COMPANY/operations/TASK_MASTER_LIST.md` | ✅ Migrated |
| `aocros/OPERATIONS_STATUS.md` | `AGI_COMPANY/operations/OPERATIONS_STATUS.md` | ✅ Migrated |

---

### 3. Agent Sandboxes

#### Apex Agents (C-Suite)
| Agent Name | Old Location | New Location | Role |
|------------|--------------|--------------|------|
| Jordan | `agent_sandboxes/jordan/` | `AGI_COMPANY/agents/apex/jordan/` | Project Manager |
| Miles | `aocros/agent_sandboxes/miles/` | `AGI_COMPANY/agents/apex/miles/` | Sales Consultant |
| [Other C-Suite] | `aocros/agent_sandboxes/<name>/` | `AGI_COMPANY/agents/apex/<name>/` | Various |

#### Technical Agents
| Agent Name | Old Location | New Location | Role |
|------------|--------------|--------------|------|
| Mortimer | `aocros/agent_sandboxes/mortimer/` | `AGI_COMPANY/agents/technical/mortimer/` | Technical Lead |
| Scribble | `aocros/agent_sandboxes/scribble/` | `AGI_COMPANY/agents/technical/scribble/` | Scribe |
| Pixel | `aocros/agent_sandboxes/pixel/` | `AGI_COMPANY/agents/technical/pixel/` | UI/UX |
| Blender-Expert | `aocros/agent_sandboxes/blender-expert/` | `AGI_COMPANY/agents/technical/blender-expert/` | 3D Design |
| Velum | `aocros/agent_sandboxes/velum/` | `AGI_COMPANY/agents/technical/velum/` | Infrastructure |
| Fiber | `aocros/agent_sandboxes/fiber/` | `AGI_COMPANY/agents/technical/fiber/` | Network |

#### Secretarial Agents
| Agent Name | Old Location | New Location | Role |
|------------|--------------|--------------|------|
| Greet | `aocros/agent_sandboxes/greet/` | `AGI_COMPANY/agents/secretarial/greet/` | Reception |
| [Clerks] | `aocros/agent_sandboxes/clerk*/` | `AGI_COMPANY/agents/secretarial/` | Admin |

#### Product Agents
| Agent Name | Old Location | New Location | Product |
|------------|--------------|--------------|---------|
| DUSTY Agents | `aocros/agent_sandboxes/dusty*/` | `AGI_COMPANY/agents/products/dusty/` | DUSTY |
| CREAM Agents | `aocros/agent_sandboxes/cream*/` | `AGI_COMPANY/agents/products/cream/` | CREAM |

---

### 4. Subsidiaries

#### Performance Supply Depot

| Category | Old Location | New Location |
|----------|--------------|--------------|
| Sales | `aocros/sales/` | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/sales/` |
| Sales | `sales/` | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/sales/` |
| Marketing | `aocros/marketing/` | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/marketing/` |
| Products | `aocros/performance_supply_depot/` | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/` |
| Website | `aocros/AGI_COMPANY_WEBSITES/` | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/website/` |

#### DUSTY

| Category | Old Location | New Location |
|----------|--------------|--------------|
| Product Code | `Dusty/` | `AGI_COMPANY/subsidiaries/DUSTY/` |
| E2E Tests | `aocros/dusty_e2e_*.js` | `AGI_COMPANY/subsidiaries/DUSTY/tests/` |
| Documentation | `aocros/dusty_e2e_reports/` | `AGI_COMPANY/subsidiaries/DUSTY/reports/` |

#### CREAM

| Category | Old Location | New Location |
|----------|--------------|--------------|
| Product Code | `Cream/` | `AGI_COMPANY/subsidiaries/CREAM/` |
| Tests | `Cream/tests/` | `AGI_COMPANY/subsidiaries/CREAM/tests/` |
| Documentation | `Cream/docs/` | `AGI_COMPANY/subsidiaries/CREAM/docs/` |

#### MilkMan Games

| Category | Old Location | New Location |
|----------|--------------|--------------|
| Game Assets | `MilkMan-Game/` | `AGI_COMPANY/subsidiaries/MILKMAN_GAMES/` |
| Code | `aocros/games/` | `AGI_COMPANY/subsidiaries/MILKMAN_GAMES/src/` |

---

### 5. Shared Resources

| Resource Type | Old Location | New Location |
|---------------|--------------|--------------|
| Shared Skills | `aocros/skills/` | `AGI_COMPANY/shared/skills/` |
| Shared Tools | `aocros/tools/` | `AGI_COMPANY/shared/tools/` |
| Infrastructure | `aocros/config/` | `AGI_COMPANY/shared/infrastructure/` |
| Scripts | `aocros/scripts/` | `AGI_COMPANY/shared/tools/scripts/` |

---

## Critical File Updates

### Updated Path References

The following files had internal path references updated:

1. **Agent Identity Files**
   - All `IDENTITY.md` files now reference correct paths
   - Avatar paths updated to new structure

2. **Agent Tools Files**
   - All `TOOLS.md` files updated with new skill locations
   - Script references corrected

3. **Corporate Documents**
   - Cross-references updated to new locations

4. **Task Lists**
   - File paths in tasks updated
   - References to reports corrected

---

## Deprecated Locations

The following directories are **DEPRECATED** and should not be used for new files:

| Deprecated Path | Replacement | Status |
|-----------------|-------------|--------|
| `/root/.openclaw/workspace/aocros/` | `AGI_COMPANY/` | Read-Only Archive |
| `/root/.openclaw/workspace/agent_sandboxes/` | `AGI_COMPANY/agents/` | Migration Complete |
| `/root/.openclaw/workspace/sales/` | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/sales/` | Migration Complete |
| `/root/.openclaw/workspace/Dusty/` | `AGI_COMPANY/subsidiaries/DUSTY/` | Migration Complete |
| `/root/.openclaw/workspace/Cream/` | `AGI_COMPANY/subsidiaries/CREAM/` | Migration Complete |
| `/root/.openclaw/workspace/MilkMan-Game/` | `AGI_COMPANY/subsidiaries/MILKMAN_GAMES/` | Migration Complete |

---

## Migration Checklist

### Phase 1: Structure Creation ✅
- [x] Create AGI_COMPANY root directory
- [x] Create corporate/ subdirectory
- [x] Create operations/ subdirectory
- [x] Create agents/ subdirectories (apex, technical, secretarial, products)
- [x] Create shared/ subdirectories (skills, tools, infrastructure)
- [x] Create subsidiaries/ structure

### Phase 2: File Migration ✅
- [x] Move corporate documents
- [x] Move operations files
- [x] Move agent sandboxes (categorized)
- [x] Move subsidiary files (PSD, DUSTY, CREAM, MilkMan)
- [x] Move shared resources

### Phase 3: Path Updates ✅
- [x] Update all internal file references
- [x] Update agent identity files
- [x] Update tools references
- [x] Update script paths

### Phase 4: Documentation ✅
- [x] Create README.md
- [x] Create MIGRATION_GUIDE.md
- [x] Document all path changes
- [x] Create navigation guide

### Phase 5: Validation ✅
- [x] Verify all files migrated
- [x] Check path references
- [x] Test agent sandboxes
- [x] Validate structure integrity

### Phase 6: Commit ✅
- [x] Stage all changes
- [x] Create descriptive commit message
- [x] Push to repository

---

## Agent Quick Reference

### Where to Find...

| What You're Looking For | Where to Look |
|------------------------|---------------|
| Your agent workspace | `AGI_COMPANY/agents/<category>/<your-name>/` |
| Shared skills | `AGI_COMPANY/shared/skills/` |
| Task assignments | `AGI_COMPANY/operations/TASK_MASTER_LIST.md` |
| Company charter | `AGI_COMPANY/corporate/CHARTER.md` |
| Sales materials (PSD) | `AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/sales/` |
| DUSTY product files | `AGI_COMPANY/subsidiaries/DUSTY/` |
| CREAM product files | `AGI_COMPANY/subsidiaries/CREAM/` |
| Gaming assets | `AGI_COMPANY/subsidiaries/MILKMAN_GAMES/` |

### By Role

**C-Suite Agents:**
- Workspace: `AGI_COMPANY/agents/apex/`
- Corporate docs: `AGI_COMPANY/corporate/`
- Operations: `AGI_COMPANY/operations/`

**Technical Agents:**
- Workspace: `AGI_COMPANY/agents/technical/`
- Shared tools: `AGI_COMPANY/shared/tools/`
- Infrastructure: `AGI_COMPANY/shared/infrastructure/`

**Product Agents:**
- Workspace: `AGI_COMPANY/agents/products/`
- Product files: `AGI_COMPANY/subsidiaries/<PRODUCT>/`

---

## Troubleshooting

### "I can't find my files!"
1. Check the Migration Mapping table above
2. Use `find AGI_COMPANY -name "<filename>"`
3. Reference the Old Location column

### "My agent sandbox is broken!"
1. Check that your IDENTITY.md has correct paths
2. Verify TOOLS.md references updated skills location
3. Update any hardcoded paths in your scripts

### "Scripts aren't working!"
1. Update script shebangs if needed
2. Check for hardcoded paths in scripts
3. Verify shared tools location: `AGI_COMPANY/shared/tools/`

---

## Post-Migration Notes

### Preserved Files
All files were preserved during migration. Nothing was deleted. Legacy directories remain as read-only archives.

### Git History
Git history is preserved. All commits prior to migration remain intact.

### Backwards Compatibility
Some symbolic links may be created for critical paths during transition period.

---

## Contact

**Migration Lead:** Jordan (Project Manager)  
**Issues/Questions:** Add to `AGI_COMPANY/operations/TASK_MASTER_LIST.md`

---

**Migration Complete:** 2026-03-28  
**Next Review:** 2026-04-28
