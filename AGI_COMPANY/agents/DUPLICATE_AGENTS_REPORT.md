# Duplicate Agents Report
**Date:** 2026-03-31 04:31 UTC  
**Scope:** AGI_COMPANY/agents/  
**Action Required:** Consolidation

---

## 🔍 DUPLICATES FOUND

### 1. Velum
**Locations:**
- `/AGI_COMPANY/agents/technical/velum/` (Active)
- `/AGI_COMPANY/agents/legacy/velum/` (Inactive)

**Recommendation:** Keep technical/, remove legacy/

### 2. Scribble
**Locations:**
- `/AGI_COMPANY/agents/technical/scribble/` (Active)
- `/AGI_COMPANY/agents/legacy/scribble/` (Inactive)

**Recommendation:** Keep technical/, remove legacy/

---

## ✅ UNIQUE AGENTS (No Duplicates)

- `fiber` - Technical (1 copy)
- `clippy-42` - Legacy (1 copy)
- `alpha-9` - Legacy (1 copy)
- `mill` - Legacy (1 copy)
- `boxtron` - Legacy (1 copy)
- `redactor` - Legacy (1 copy)

---

## 🛠️ PROPOSED ACTIONS

### Option A: Remove Legacy Duplicates (Recommended)
```bash
# Remove duplicate legacy agents
rm -rf /root/.openclaw/workspace/AGI_COMPANY/agents/legacy/velum
rm -rf /root/.openclaw/workspace/AGI_COMPANY/agents/legacy/scribble

# Update references in documentation
# Archive legacy manifests if needed
```

### Option B: Archive Instead of Delete
```bash
# Move to archive instead of deleting
mkdir -p /root/.openclaw/workspace/AGI_COMPANY/agents/archived
mv /root/.openclaw/workspace/AGI_COMPANY/agents/legacy/velum /root/.openclaw/workspace/AGI_COMPANY/agents/archived/
mv /root/.openclaw/workspace/AGI_COMPANY/agents/legacy/scribble /root/.openclaw/workspace/AGI_COMPANY/agents/archived/
```

### Option C: Merge Configurations
```bash
# Keep both but merge any unique configs
# Technical version becomes primary
# Legacy version's unique data preserved in backup
```

---

## 📊 AGENT INVENTORY AFTER CLEANUP

| Directory | Count | Status |
|-----------|-------|--------|
| technical/ | 3 (velum, scribble, fiber) | ✅ Active |
| legacy/ | 5 (clippy-42, alpha-9, mill, boxtron, redactor) | ⚠️ Review |
| archived/ | 2 (velum, scribble) | 🗂️ Archived |

**Total:** 10 unique agents

---

## 📝 PRE-CLEANUP BACKUP

**Before any deletions, commit to GitHub:**
```bash
git add -A
git commit -m "Pre-cleanup: Agent duplicate inventory"
git push origin master
```

**Then:**
```bash
# Archive or remove duplicates
# Update AGENTS.md inventory
# Commit again
```

---

**Recommendation:** Execute Option A (Remove Legacy Duplicates) with Git backup.

**Awaiting Captain approval.**
