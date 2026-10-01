# Monthly Audit Report - 2026-10-01

## GitHub Audit — hcindus (33 repositories)

Scope: uncommitted changes, large files (gitignore candidates), stale branches, dependency vulnerabilities, README coverage.

---

### 1. Uncommitted Changes

Remote-only audit; local workspace (`hcindus/AOS-Brain`, branch `main`):

```
 ? aocros            (submodule — dirty/untracked)
```

⚠️ `aocros` remains wired as a git submodule but reports as dirty/untracked. Confirm the submodule pointer is committed, or migrate to a vendored copy to avoid drift. (Unchanged from Sept.)

Remote uncommitted changes cannot be detected via API — requires a local clone per repo. Recommend `git status --porcelain` against each active clone.

Open PRs (potential unmerged work):
- **AOS-Brain #1** — "DAILY STATUS REPORT - 2026-04-13" (stale, ~6 mo old, unmerged). Close or merge.

---

### 2. Large Files / Gitignore Candidates

| Repo | Path | Size | Issue |
|------|------|------|-------|
| AOS-Brain | `.venv/**/*.so` (multiple), `numpy/_core/_multiarray_umath...so`, `cryptography/_rust.abi3.so`, `temporal_sdk_bridge.abi3.so` | MBs | Committed virtualenvs / compiled binaries |
| AOS-Brain | `backups/databases/*.db.gz`, `data/depot_chaos/*.db`, `datadepot/backups/*.db`, `DepotChaos/depot_chaos.db` | MBs | Committed database backups |
| AOS-Brain | `datadepot/data/*.csv`, `AGI_COMPANY/data/leads_generated/*.csv` | MBs | Committed data exports |
| AOS-Brain | `mortimer-build/prism-llama/models/*.gguf` | MBs | Model weights in repo |
| AOS-Brain | `reggiestarr-rs80/app/build/**` (`.apk`, `.dex`), `rs79-clone/.next/**` | MBs | Build artifacts |
| AOS-Brain | `*.stl` (milkman_hero, osy7_v2..v5), `*.wav` | MBs | Binary assets |
| AGI-Company | `.venv`, `node_modules/typescript`, `*.stl`, compiled binaries, CSV | MBs | Same pattern as AOS-Brain |
| tappylewis.cloud | `music/tracks/*.mp3`, `velvet-cabaret/sets/**/*.mp3` | 5–8 MB each | Audio committed to git |
| aocros | `skills/evm-wallet/banner*.png` | 5–7 MB | Large image |
| aios-sync | `.pi/agent/skills/evm-wallet*/banner*.png` | 5–7 MB | Duplicated across two folders |
| skills | `agi-company/aos-brain-interface/node_modules/typescript/*.js` | 6–9 MB | `node_modules` committed |

**Top offenders:** `AOS-Brain` and `AGI-Company` remain bloated by committed `.venv`, `node_modules`, database backups, and build artifacts. `tappylewis.cloud` now carries several MB of MP3 audio in git.

**Recommendation:** Add/expand `.gitignore` (`.venv/`, `node_modules/`, `*.db*`, `*.csv`, `*.stl`, `*.wav`, `*.gguf`, `build/`, `.next/`, `*.apk`, `*.mp3`, large `banner*.png`). Consider Git LFS for intentional binary assets, or move audio/backups to object storage.

---

### 3. Stale Branches

| Repo | Branch | Last Commit | Age |
|------|--------|-------------|-----|
| aocros | AOS | 2026-03-15 | ~6.5 mo |
| aocros | pocket-v1.1 | 2026-03-05 | ~7 mo |
| aocros | pocket-v1.1-clean | 2026-03-02 | ~7 mo |
| aocros | archive_20260309 | 2026-03-09 | ~7 mo |
| aocros | fresh-start | 2026-02-26 | ~7 mo |
| aocros | communication-update | 2026-02-21 | ~7 mo |
| aocros | chipp-pages | 2026-08-10 | ~2 mo |
| performance-supply-depot | main-clean | 2026-02-22 | ~7 mo |
| performance-supply-depot | clean-push | 2026-02-21 | ~7 mo |
| performance-supply-depot | communication-update | 2026-02-21 | ~7 mo |
| tappylewis.cloud | master | 2026-03-07 | ~7 mo |
| milkman-game | master | 2026-03-30 | ~6 mo |
| AOS-Brain | backup-push-20260628-0004 | 2026-06-28 | ~3 mo |
| AOS-Brain | master | 2026-09-21 | main/master split |

**Note:** `AOS-Brain`, `tappylewis.cloud`, and `milkman-game` each have a `main`/`master` split. Confirm which is canonical and delete the other.

**Recommendation:** Delete merged/stale branches after confirming they are merged. Consolidate `main`/`master`.

---

### 4. Security / Dependency Vulnerabilities

⚠️ **Dependabot alerts are DISABLED for all 33 repositories.** No automated dependency vulnerability scanning is active. Enable Dependabot alerts (and ideally security updates) at org/repo level.

Critical findings:
- **aocros** — `secrets/private_key.pem` committed to the repo. Rotate the key immediately and remove from git history (use `git filter-repo` / BFG). Do NOT treat as safe merely because the repo is private.
- **aocros** — `agent_sandboxes/the-great-cryptonio/run_with_credentials.sh` committed; audit for embedded credentials.

No active `npm audit` / `pip-audit` CVE list was produced this cycle (remote-only). Recommend running `npm audit` / `pip-audit` in local clones of active repos (`AGI-Company`, `aocros`, `skills`, `cream-mobile`).

---

### 5. README Updates Needed

Missing README (14 repos — **unchanged from Sept**):

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

Also empty/legacy repos that may need content or archival: depotcrm, new-scraper, AOCROS-, myl0n.r1s, Myl0n.R0s, Warzone-2100-Maps.

**Recommendation:** Add a minimal README (description, run instructions, license) to the public repos at minimum.

---

### Action Items (priority order)

1. 🔴 Rotate & purge `aocros/secrets/private_key.pem`.
2. 🔴 Enable Dependabot alerts across all repos.
3. 🟠 Add `.gitignore` to AOS-Brain / AGI-Company / tappylewis.cloud and prune committed binaries, DBs, and audio.
4. 🟠 Resolve `aocros` submodule dirty state.
5. 🟡 Delete stale branches / consolidate `main`+`master`.
6. 🟡 Add READMEs to 14 repos.
7. ⚪ Close/merge stale PR AOS-Brain #1.
