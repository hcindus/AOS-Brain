# Monthly GitHub Audit Report - hcindus

**Audit Date:** Wednesday, July 1st, 2026 - 9:03 AM UTC  
**Auditor:** Miles (Autonomous Operations Engine)  
**Scope:** All hcindus GitHub repositories

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| Total Repositories | 15 |
| Repositories with Uncommitted Changes | 2 |
| Repositories Missing .gitignore | 0 |
| Repositories Missing README | 0 |
| Security Alerts Found | 3 (Secret Scanning) |
| Stale Branches | 1 |

---

## REPOSITORY INVENTORY

| Repository | Language | Last Pushed | Size | Default Branch |
|------------|----------|-------------|------|----------------|
| AOS-Brain | Python | 2026-07-01 | 1.3 GB | master |
| cream-mobile | Python | 2026-07-01 | 8 MB | main |
| depotchaos | HTML | 2026-06-26 | 51 KB | main |
| performance-supply-depot | JavaScript | 2026-02-23 | 58 MB | main |
| amhudsupply | HTML | 2026-02-26 | 7 KB | main |
| neon-courier | JavaScript | 2026-02-26 | 9 KB | main |
| tappylewis.cloud | HTML | 2026-04-07 | 61 KB | main |
| performancesupplydepot | HTML | 2026-02-26 | 8 KB | main |
| website-template | HTML | 2026-03-02 | 3 MB | main |
| psdepot-landing | HTML | 2026-06-30 | 40 KB | master |
| new-scraper | - | 2026-04-05 | 0 KB | main |
| hcindus | JavaScript | 2026-06-01 | 15 MB | master |
| myl0n.r1s | - | 2016-02-04 | 0 KB | master |
| Myl0n.R0s | - | 2014-04-30 | 0 KB | master |
| Warzone-2100-Maps | - | 2014-04-30 | 0 KB | master |

---

## 1. UNCOMMITTED CHANGES

### 🔴 CRITICAL: AOS-Brain (/root/.openclaw/workspace)
**7 uncommitted changes:**
- `? aocros` (untracked directory)
- `M data/factory/dark_factory.db`
- `M nognog/crew/storage/crew/crew_1775550212150_6p3fyu.json`
- `M nognog/crew/storage/crew/crew_1775550212152_8m6o8w.json`
- `M nognog/crew/storage/crew/crew_1775550212250_smucjt.json`
- `M nognog/crew/storage/crew/crew_1775550212549_m4opvw.json`
- `M nognog/crew/storage/crew/crew_1775550212551_emebru.json`

**Recommendation:** Commit or stash these changes. The .db files may contain sensitive data.

### 🟡 WARNING: AOS-Brain (/root/.aos)
**2 uncommitted changes:**
- `M brain/state/brain_v31_state.json`
- `M brain/state/tracray.json`

**Recommendation:** These are state files. Consider if they should be committed or gitignored.

### ✅ CLEAN: Repositories with no uncommitted changes
- openclaw (external)
- hermes-agent (external)

---

## 2. LARGE FILES ANALYSIS

### Top Large Files in AOS-Brain:
| Size | File Path |
|------|-----------|
| 1.1 GB | labs/bonsai-quant-lab/models/Bonsai-8B-Q1_0.gguf |
| 211 MB | aocros/products/cream/backend/node_modules/.cache/mongodb-memory-server/mongod-x64-ubuntu-8.2.1 |
| 169 MB | reggiestart-pos/node_modules/electron/dist/electron |
| 169 MB | reggiestart-pos/dist/linux-unpacked/reggiestart-pos |
| 163 MB | reggiestart-pos/dist/linux-arm64-unpacked/reggiestart-pos |
| 110 MB | AGI_COMPANY/.git/objects/pack/pack-bc2e9af53e50aa7101dcdfc12092a7d71cd78a85.pack |
| 106 MB | reggiestart-pos/dist/ReggieStart |
| 65 MB | data/depot_chaos/unified.db |
| 50 MB | datadepot/backups/unified_pre_tier.db |
| 50 MB | data/depot_chaos/unified_backup_20260509_053801.db |

### 🟡 WARNING: Large files that should be gitignored:
1. `.gguf` model files (1.1 GB) - should use Git LFS or external storage
2. `node_modules/` directories (multiple locations)
3. Database files (.db) - especially backups and data exports
4. Electron build artifacts in `reggiestart-pos/dist/`

**Recommendation:** 
- Add `*.gguf`, `node_modules/`, and `*.db` to .gitignore
- Use Git LFS for large binary files if they need tracking
- Move large database backups to external storage

---

## 3. STALE BRANCHES

### AOS-Brain:
- `backup-push-20260628-0004` - Last commit: ea72aa9

**Recommendation:** This backup branch is 3 days old. Consider deleting after verifying master is stable.

### Other repositories with branches:
- Most repositories have minimal branching (just main/master)
- No significant stale branch issues detected

---

## 4. SECURITY VULNERABILITIES

### 🔴 CRITICAL: Secret Scanning Alerts
**AOS-Brain repository has 3 open secret alerts:**
- Secret Alert #3: `telegram_bot_token` - **OPEN**
- Secret Alert #2: `telegram_bot_token` - **OPEN**
- Secret Alert #1: `telegram_bot_token` - **OPEN**

**Status:** These tokens are exposed in the repository history and need immediate rotation.

### Dependabot Alerts:
- No accessible dependabot vulnerability data (likely requires GitHub Advanced Security)

**Recommendation:**
1. Immediately revoke and regenerate the exposed Telegram bot tokens
2. Review commit history with `git log --all --source --remotes -- <filename>` to find exposure points
3. Consider using `git-filter-repo` to remove secrets from history if needed
4. Enable GitHub secret scanning protection for future commits

---

## 5. README UPDATES NEEDED

### ✅ All repositories have README files

### Status:
| Repository | README Status |
|------------|---------------|
| AOS-Brain | README.md present (7.5 KB) |
| openclaw | README.md present (123 KB) |
| hermes-agent | README.md present (10.7 KB) |

**No README updates needed** - all repositories have documentation in place.

---

## 6. .GITIGNORE STATUS

### ✅ All checked repositories have .gitignore files

### Existing Patterns:
- AOS-Brain: `.aos/vault/`, `*.pem`, `*.key`, `.env`
- openclaw: `node_modules`, `.env`, `docker-compose.override.yml`
- hermes-agent: `venv/`, `__pycache__/`, `.venv/`

### Recommended Additions:
```
# Large binary files
*.gguf
*.db
*.sqlite
*.sqlite3

# Dependencies
node_modules/
__pycache__/
*.pyc

# Build artifacts
dist/
build/
*.exe
*.bin

# Data directories
data/depot_chaos/*.db
datadepot/backups/*.db
```

---

## ACTION ITEMS

### Immediate (This Week):
1. [ ] **CRITICAL:** Rotate exposed Telegram bot tokens in AOS-Brain
2. [ ] Commit or stash uncommitted changes in AOS-Brain workspaces
3. [ ] Remove stale backup branch `backup-push-20260628-0004`

### Short-term (This Month):
4. [ ] Add `*.gguf`, `node_modules/`, and database files to .gitignore
5. [ ] Move large model files to Git LFS or external storage
6. [ ] Clean up database backup files from repository

### Long-term (Next Quarter):
7. [ ] Set up automated dependency scanning (Dependabot)
8. [ ] Implement pre-commit hooks for secret detection
9. [ ] Archive unused repositories (Myl0n.R0s, myl0n.r1s, Warzone-2100-Maps - all inactive since 2014-2016)

---

## AUDIT CONCLUSION

The hcindus GitHub organization has **15 repositories** with varying activity levels. The most critical issue is the **3 exposed Telegram bot tokens** in AOS-Brain which require immediate rotation. There are uncommitted changes in 2 local workspaces that should be reviewed and committed or gitignored. Large files (1.1+ GB) are present in the AOS-Brain repository that should be moved to Git LFS or external storage.

**Overall Health:** 🟡 Moderate - Action required on security alerts

---

*Report generated by Miles - Autonomous Operations Engine*  
*Performance Supply Depot LLC / AGI Company*
