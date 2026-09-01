# Monthly Audit Report - 2026-09-01

## GitHub Audit — hcindus (33 repositories)

Scope: uncommitted changes, large files (gitignore candidates), stale branches, dependency vulnerabilities, README coverage.

---

### 1. Uncommitted Changes

Remote-only audit; local workspace (`hcindus/AOS-Brain`, branch `main`):

```
 ? aocros            (submodule — untracked/pointing elsewhere)
```

⚠️ `aocros` is still wired as a git submodule but reports as dirty/untracked. Confirm the submodule pointer is committed, or migrate to a vendored copy to avoid drift.

Remote uncommitted changes cannot be detected via API — requires a local clone per repo. Recommend running `git status --porcelain` against each clone in the next audit cycle.

---

### 2. Large Files That Should Be Gitignored

| Repo | Path | Size | Issue |
|------|------|------|-------|
| AOS-Brain | `backups/databases/unified_*.db.gz` (multiple) | ~11.5 MB ea. | DB backups committed to git |
| AGI-Company | `data/leads_generated/CA_ABC_CONSOLIDATED_2026-05-07.csv` | 12.6 MB | Generated data dump |
| AGI-Company | `operations/collections/temporal-workflow/collections-worker` | 29.4 MB | Compiled binary |
| AGI-Company | `shared/skills/*/node_modules/typescript/lib/typescript.js` | 9.1 MB | `node_modules` committed |
| AGI-Company | `subsidiaries/MILKMAN_GAMES/hardware/milkman_hero.stl` | 6.4 MB | Binary asset |
| skills | `agi-company/aos-brain-interface/node_modules/...` | 9.1 MB | `node_modules` committed |
| hcindus | `myl2n.r3s.apk`, `abn.apk` | 6.6 / 5.2 MB | Built APKs in repo |
| (6 repos) | `*/evm-wallet/banner4.png` | 6.9 MB | Large image duplicated across repos |

**Top offenders:** `AOS-Brain` (1.6 GB total repo size) and `AGI-Company` (184 MB) are bloated by committed database backups, `node_modules`, compiled binaries, and build artifacts.

**Recommendation:** Add `.gitignore` rules for `backups/`, `node_modules/`, `*.apk`, `*.db.gz`, `*.csv` (in data dirs), and large banner assets (or move to LFS / CDN). Consider `git filter-repo` to strip history for the biggest repos.

---

### 3. Stale Branches (unmerged, >90 days)

| Repo | Branch | Last commit | Age |
|------|--------|-------------|-----|
| aocros | AOS | 2026-03-15 | ~5.5 mo |
| aocros | pocket-v1.1 | 2026-03-05 | ~6 mo |
| aocros | pocket-v1.1-clean | 2026-03-02 | ~6 mo |
| aocros | archive_20260309 | 2026-03-09 | ~6 mo |
| aocros | fresh-start | 2026-02-26 | ~6 mo |
| aocros | communication-update | 2026-02-21 | ~6 mo |
| performance-supply-depot | main-clean | 2026-02-22 | ~6 mo |
| performance-supply-depot | clean-push | 2026-02-21 | ~6 mo |
| performance-supply-depot | communication-update | 2026-02-21 | ~6 mo |
| tappylewis.cloud | master | 2026-03-07 | ~6 mo |
| milkman-game | master | 2026-03-30 | ~5 mo |
| AOS-Brain | backup-push-20260628-0004 | 2026-06-28 | ~2 mo |

**Note:** `AOS-Brain` has a `main`/`master` split (main active since 2026-09-01; master last touched 2026-08-31). Confirm which is canonical and delete the other to avoid confusion.

**Recommendation:** Delete merged/stale branches after confirming nothing unmerged. `performance-supply-depot` itself appears abandoned (last push 2026-02-23) — consider archiving.

---

### 4. Security Vulnerabilities in Dependencies

❌ **Dependabot vulnerability alerts are DISABLED on all repositories.** The vulnerability-alerts endpoint returned `404 — Vulnerability alerts are disabled` for every repo.

**Recommendation:**
- Enable Dependabot alerts + security updates org-wide (Settings → Code security & analysis).
- Remove committed `node_modules/` (supply-chain risk; dependency drift).
- Run `npm audit` / `pip-audit` in a local clone of active repos (`AGI-Company`, `aocros`, `skills`, `cream-mobile`) to get an actual CVE list.

---

### 5. README Updates Needed

Missing README (14 repos):

- depotchaos
- psdepot
- psdepot-landing
- antoniohudnall-e-ivory-auto
- ivory-auto
- milkman-game
- depotcrm
- website-template
- performance-supply-depot
- Ronstrapp
- Memory
- ReggeStar
- AOCROS-
- Myl0n.R0s

Also empty repos (`size_kb=0`) that may need either content or archival: depotcrm, new-scraper, AOCROS-, myl0n.r1s, Myl0n.R0s, Warzone-2100-Maps.

**Recommendation:** Add a minimal README (description, run instructions, license) to the public repos at minimum (`depotchaos`, `psdepot`, `psdepot-landing`, `website-template`, `new-scraper`).

---

## Summary of Priorities

1. **Enable Dependabot** org-wide (no cost, immediate security visibility).
2. **Strip large binaries/backups/node_modules** from `AOS-Brain` and `AGI-Company` + add `.gitignore`.
3. **Prune stale branches** across `aocros`, `performance-supply-depot`, and resolve the `AOS-Brain` main/master split.
4. **Add READMEs** to public repos lacking them.
5. **Resolve `aocros` submodule drift** in the workspace.

---

*Audit completed at 2026-09-01T09:03:00+00:00*
