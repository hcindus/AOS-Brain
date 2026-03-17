# VPS Cleanup Inventory
**Date:** 2026-03-16  
**Agent:** Jordan (Subagent)  
**Status:** INVENTORY COMPLETE — AWAITING REVIEW

---

## Python Cache Files

### System-Wide Count
- **__pycache__ directories:** 1,231
- **.pyc files:** 11,415+
- **.pyo files:** 0 (none found)

### Workspace-Specific Count
- **__pycache__ directories:** 16
- **.pyc/.pyo files:** 56

### Key Locations in Workspace
```
/root/.openclaw/workspace/test-bench/environments/aos-brain-test/brain/agents/__pycache__
/root/.openclaw/workspace/aocros/projects/netprobe/decryptor/__pycache__
/root/.openclaw/workspace/aocros/projects/netprobe/analysis/__pycache__
/root/.openclaw/workspace/aocros/projects/teleport/phase2/__pycache__
/root/.openclaw/workspace/aocros/projects/teleport/__pycache__
/root/.openclaw/workspace/aocros/projects/ReggieStarr/__pycache__
/root/.openclaw/workspace/aocros/projects/censys/__pycache__
/root/.openclaw/workspace/aocros/projects/voice-system/__pycache__
/root/.openclaw/workspace/aocros/projects/socket-arsenal/core/__pycache__
/root/.openclaw/workspace/aocros/projects/socket-arsenal/probes/__pycache__
/root/.openclaw/workspace/aocros/projects/socket-arsenal/drill/__pycache__
/root/.openclaw/workspace/aocros/projects/portal/__pycache__
/root/.openclaw/workspace/aocros/agent_sandboxes/r2-d2/__pycache__
/root/.openclaw/workspace/aocros/test-bench/environments/aos-brain-test/brain/agents/__pycache__
/root/.openclaw/workspace/AOS/brain/__pycache__
/root/.openclaw/workspace/AOS/brain/agents/__pycache__
```

### What It Is
Compiled Python bytecode cache files generated automatically when Python scripts run.

### Why It Exists
Python compiles `.py` source files to bytecode (`.pyc`) for faster subsequent execution. `__pycache__` directories store these compiled files organized by Python version.

### Safe to Delete?
**YES** — These are regenerated automatically when Python code runs.

### Recommendation: **REMOVE**
- Safe to delete all `__pycache__` directories
- Safe to delete all `.pyc` and `.pyo` files
- Will regenerate on next Python execution
- Consider adding to `.gitignore` if not already present

---

## Backup Files

### Critical Backup Files (REVIEW CAREFULLY)

| File Path | Purpose | KEEP/REMOVE |
|-----------|---------|-------------|
| `/root/.openclaw/workspace/aocros/secrets/CRITICAL_KEYS_BACKUP.md` | Crypto wallet, API keys, credentials backup | **KEEP** — Critical operational data |
| `/root/.openclaw/workspace/aocros/KEY_BACKUP_STATUS.md` | Key inventory and backup status tracking | **KEEP** — Documentation |
| `/root/.openclaw/workspace/aocros/tappy-lewis-reconstituted/communications/BACKUP_PROTOCOLS.md` | Communication protocols for Tappy Lewis | **KEEP** — Operational protocol |

### Code Backup Files (LIKELY SAFE TO REMOVE)

| File Path | Purpose | KEEP/REMOVE |
|-----------|---------|-------------|
| `/root/.openclaw/workspace/AOS/brain/agents/hippocampus_agent_FIXED.py` | Fixed version of hippocampus agent | **REVIEW** — Compare with current version |
| `/root/.openclaw/workspace/AOS/brain/agents/hippocampus_agent_backup.py` | Backup of hippocampus agent (8,070 bytes) | **REVIEW** — May be outdated |
| `/root/.openclaw/workspace/AOS/brain/agents/thalamus_agent_backup.py` | Backup of thalamus agent (201 bytes) | **REVIEW** — Likely safe to remove |
| `/root/.openclaw/workspace/test-bench/environments/aos-brain-test/brain/agents/hippocampus_agent_FIXED.py` | Duplicate of above | **REVIEW** — Same file, different location |
| `/root/.openclaw/workspace/test-bench/environments/aos-brain-test/brain/agents/hippocampus_agent_backup.py` | Duplicate backup | **REVIEW** — Same file, different location |
| `/root/.openclaw/workspace/test-bench/environments/aos-brain-test/brain/agents/thalamus_agent_backup.py` | Duplicate backup | **REVIEW** — Same file, different location |
| `/root/.openclaw/workspace/aocros/test-bench/environments/aos-brain-test/brain/agents/hippocampus_agent_FIXED.py` | Third copy | **REVIEW** — Same file, different location |
| `/root/.openclaw/workspace/aocros/test-bench/environments/aos-brain-test/brain/agents/hippocampus_agent_backup.py` | Third copy | **REVIEW** — Same file, different location |
| `/root/.openclaw/workspace/aocros/test-bench/environments/aos-brain-test/brain/agents/thalamus_agent_backup.py` | Third copy | **REVIEW** — Same file, different location |

### Other Backup Files

| File Path | Purpose | KEEP/REMOVE |
|-----------|---------|-------------|
| `/root/.openclaw/workspace/aocros/archives/dusty_e2e_reports/dusty_e2e_test_fixed.js` | Fixed E2E test | **REVIEW** — Check if current |
| `/root/.openclaw/workspace/aocros/dusty_mvp_sandbox/bridge_guardian_fixed.sh` | Fixed bridge guardian script | **REVIEW** — Check if current |
| `/root/.openclaw/workspace/aocros/dusty_mvp_sandbox/bridge_mock_v1_backup.js` | Backup of bridge mock | **REVIEW** — Likely outdated |

### System Backup Files (KEEP — Not User Data)
- `/usr/libexec/dpkg/dpkg-db-backup` — System package manager backup
- `/usr/share/man/man8/cryptsetup-luksHeaderBackup.8.gz` — System documentation
- `/usr/share/man/man8/vgcfgbackup.8.gz` — System documentation
- `/usr/share/perl5/Debconf/DbDriver/Backup.pm` — System Perl module
- `/etc/console-setup/Uni2-Fixed16.psf.gz` — System console font
- `/usr/share/consolefonts/*-Fixed*.psf.gz` — System console fonts (47 files)

---

## Temporary Files

### /tmp Directory Contents

#### Large Archive (REVIEW)
| File | Size | Age | Recommendation |
|------|------|-----|----------------|
| `/tmp/blender-4.2.0-linux-x64.tar.xz` | **336 MB** | Jul 16 2024 (8+ months old) | **REMOVE** — Old installer archive |

#### Log Files (REVIEW)
| File | Size | Status | Recommendation |
|------|------|--------|----------------|
| `/tmp/brain.log` | 0 bytes | Empty | **REMOVE** — Empty log |
| `/tmp/brain_new.log` | 0 bytes | Empty | **REMOVE** — Empty log |
| `/tmp/m2_bridge.log` | 0 bytes | Empty | **REMOVE** — Empty log |
| `/tmp/miles_webhook.log` | 873 bytes | Has content | **REVIEW** — Check if needed |

#### Script Files (REVIEW)
| File | Size | Recommendation |
|------|------|----------------|
| `/tmp/generate_signal_report.py` | 2,155 bytes | **REVIEW** — May be temporary script |
| `/tmp/periodic_table.txt` | 3,082 bytes | **REVIEW** — May be temporary data |

#### System Temp Files (KEEP — System Managed)
- `/tmp/.ICE-unix/` — X11 session sockets
- `/tmp/.X11-unix/` — X11 display sockets
- `/tmp/.XIM-unix/` — X input method sockets
- `/tmp/.font-unix/` — Font server sockets
- `/tmp/jiti/` — JIT compilation cache
- `/tmp/node-compile-cache/` — Node.js compilation cache
- `/tmp/systemd-private-*` — Systemd service private directories
- `/tmp/tmux-0/` — Tmux session directory
- `/tmp/tsx-0/` — TypeScript execution cache
- `/tmp/openclaw/` — OpenClaw temp directory
- `/tmp/openclaw-0/` — OpenClaw temp directory

#### Ollama Backup Files (REVIEW)
Location: `/tmp/ollama-backups/`
- `config.json.1773562670` (51 bytes)
- `config.json.1773562704` (78 bytes)
- `config.json.1773562712` (83 bytes)
- `config.json.1773562922` (154 bytes)
- `config.json.1773563230` (179 bytes)
- `openclaw.json.1773562712` (2,084 bytes)
- `openclaw.json.1773563230` (2,655 bytes)

**Recommendation:** These appear to be rotated config backups. **REVIEW** — May be safe to remove older ones.

#### Other Temp Files (REVIEW)
- `/tmp/aos-lite.pid` — Process ID file (7 bytes) — **KEEP** if service running
- `/tmp/tmp.*` files — Various temporary files created by processes

---

## Duplicate Files

### Python Files with Same Name (Multiple Locations)

| Filename | Locations | Notes |
|----------|-----------|-------|
| `__init__.py` | 6 locations | Standard Python package files — **KEEP** |
| `basal_agent.py` | 4 locations | AOS brain agent — **REVIEW** |
| `brain.py` | 4 locations | AOS brain core — **REVIEW** |
| `brain_alt_tui.py` | 4 locations | TUI variant — **REVIEW** |
| `brain_lite.py` | 2 locations | Lite version — **REVIEW** |
| `brain_tui.py` | 4 locations | TUI version — **REVIEW** |
| `brain_visualizer.py` | 2 locations | Visualizer — **REVIEW** |
| `brainstem_agent.py` | 4 locations | Brainstem agent — **REVIEW** |
| `cerebellum_agent.py` | 4 locations | Cerebellum agent — **REVIEW** |
| `conscious.py` | 4 locations | Consciousness module — **REVIEW** |
| `dashboard_server.py` | 2 locations | Cryptonio dashboard — **REVIEW** |
| `dusty_complete_e2e.py` | 2 locations | Dusty E2E test — **REVIEW** |
| `dusty_e2e_test.py` | 2 locations | Dusty E2E test — **REVIEW** |
| `dynamic_thresholds.py` | 2 locations | Threshold module — **REVIEW** |
| `error_prediction.py` | 2 locations | Error prediction — **REVIEW** |
| `feed_brain.py` | 2 locations | Brain feeder — **REVIEW** |
| `github_webhook_receiver.py` | 2 locations | Webhook receiver — **REVIEW** |
| `hippocampus_agent.py` | 4 locations | Hippocampus agent — **REVIEW** |
| `hippocampus_agent_FIXED.py` | 3 locations | Fixed version — **REVIEW** |
| `hippocampus_agent_backup.py` | 3 locations | Backup version — **REVIEW** |
| `thalamus_agent.py` | 4 locations | Thalamus agent — **REVIEW** |
| `thalamus_agent_backup.py` | 3 locations | Backup version — **REVIEW** |

**Note:** Many duplicates exist between `/AOS/`, `/aocros/AOS-Brain/`, `/test-bench/`, and `/aocros/test-bench/` directories. These may be intentional copies for different environments.

---

## Large Files (>10MB)

### System Files (KEEP — Required)
| File | Size | Purpose |
|------|------|---------|
| `/boot/vmlinuz-6.8.0-90-generic` | ~12 MB | Linux kernel — **KEEP** |
| `/boot/initrd.img-6.8.0-90-generic` | ~85 MB | Initial RAM disk — **KEEP** |
| `/usr/libexec/docker/cli-plugins/docker-buildx` | ~65 MB | Docker build plugin — **KEEP** |
| `/usr/libexec/docker/cli-plugins/docker-compose` | ~55 MB | Docker Compose — **KEEP** |
| `/usr/bin/docker` | ~50 MB | Docker binary — **KEEP** |
| `/usr/bin/dockerd` | ~45 MB | Docker daemon — **KEEP** |
| `/usr/bin/node` | ~45 MB | Node.js runtime — **KEEP** |
| `/usr/bin/containerd` | ~40 MB | Container runtime — **KEEP** |
| `/usr/bin/cmake` | ~35 MB | Build system — **KEEP** |
| `/usr/bin/monarx-agent` | ~35 MB | Security agent — **KEEP** |
| `/usr/lib/llvm-18/lib/libLLVM.so.1` | ~110 MB | LLVM library — **KEEP** |
| `/usr/lib/llvm-18/lib/libclang-cpp.so.18.1` | ~45 MB | Clang library — **KEEP** |
| `/usr/lib/python3.12/config-3.12-x86_64-linux-gnu/libpython3.12.a` | ~15 MB | Python static lib — **KEEP** |

### Ollama Model Files (REVIEW)
| File | Size | Purpose |
|------|------|---------|
| `/usr/share/ollama/.ollama/models/blobs/sha256-*` (6 files) | Various | AI model weights — **KEEP** (active models) |
| `/usr/local/lib/ollama/cuda_v12/libcublasLt.so.12.8.4.1` | ~300 MB | CUDA library — **KEEP** |
| `/usr/local/lib/ollama/cuda_v12/libcublas.so.12.8.4.1` | ~150 MB | CUDA library — **KEEP** |
| `/usr/local/lib/ollama/cuda_v12/libggml-cuda.so` | ~400 MB | GGML CUDA backend — **KEEP** |
| `/usr/local/lib/ollama/cuda_v13/libcublasLt.so.13.1.0.3` | ~300 MB | CUDA library — **KEEP** |
| `/usr/local/lib/ollama/cuda_v13/libcublas.so.13.1.0.3` | ~150 MB | CUDA library — **KEEP** |
| `/usr/local/lib/ollama/cuda_v13/libggml-cuda.so` | ~400 MB | GGML CUDA backend — **KEEP** |
| `/usr/local/lib/ollama/mlx_cuda_v13/libnccl.so.2.29.7` | ~150 MB | NCCL library — **KEEP** |
| `/usr/local/lib/ollama/mlx_cuda_v13/libmlx.so` | ~200 MB | MLX library — **KEEP** |
| `/usr/local/lib/ollama/vulkan/libggml-vulkan.so` | ~150 MB | Vulkan backend — **KEEP** |

### Workspace Large Files (REVIEW)
| File | Size | Purpose |
|------|------|---------|
| `/root/.openclaw/workspace/aocros/archive/backups/github/performance-supply-depot-mirror-20260222/objects/pack/pack-*.pack` | Large | Git pack file — **REVIEW** |
| `/root/.openclaw/workspace/aocros/archive/backups/github/aocros-mirror-20260222/objects/pack/pack-*.pack` | Large | Git pack file — **REVIEW** |
| `/root/.openclaw/workspace/aocros/.git/objects/pack/pack-*.pack` | Large | Git pack file — **KEEP** (active repo) |

### Temporary Large Files (REMOVE)
| File | Size | Purpose |
|------|------|---------|
| `/tmp/blender-4.2.0-linux-x64.tar.xz` | **336 MB** | Old Blender installer — **REMOVE** |

---

## Action Plan

### Safe to Remove Immediately
1. **All Python cache files:**
   - All `__pycache__` directories (1,231 system-wide, 16 in workspace)
   - All `.pyc` files (11,415+ system-wide, 56 in workspace)
   - All `.pyo` files

2. **Empty log files:**
   - `/tmp/brain.log` (0 bytes)
   - `/tmp/brain_new.log` (0 bytes)
   - `/tmp/m2_bridge.log` (0 bytes)

3. **Old installer archive:**
   - `/tmp/blender-4.2.0-linux-x64.tar.xz` (336 MB, 8+ months old)

### Review with Captain (Miles)
1. **Code backup files** — Determine if `_backup.py` and `_FIXED.py` files are still needed:
   - `hippocampus_agent_backup.py` (3 copies)
   - `hippocampus_agent_FIXED.py` (3 copies)
   - `thalamus_agent_backup.py` (3 copies)

2. **Duplicate Python files** — Determine if multiple AOS brain copies are intentional:
   - `/AOS/brain/` vs `/aocros/AOS-Brain/` vs `/test-bench/` vs `/aocros/test-bench/`

3. **Temporary scripts/data** — Determine if still needed:
   - `/tmp/generate_signal_report.py`
   - `/tmp/periodic_table.txt`
   - `/tmp/miles_webhook.log`

4. **Ollama config backups** — Determine retention policy:
   - `/tmp/ollama-backups/config.json.*`
   - `/tmp/ollama-backups/openclaw.json.*`

5. **Git pack files in archive** — Determine if mirror backups needed:
   - `/aocros/archive/backups/github/*-mirror-*/`

### Keep
1. **Critical backup documentation:**
   - `CRITICAL_KEYS_BACKUP.md`
   - `KEY_BACKUP_STATUS.md`
   - `BACKUP_PROTOCOLS.md`

2. **System files** — All system binaries, libraries, kernels

3. **Active Ollama models** — Required for AI operations

4. **Active Git repositories** — `/aocros/.git/`

5. **Process ID files** — If services are running (`/tmp/aos-lite.pid`)

---

## Summary Statistics

| Category | Count/Size | Action |
|----------|------------|--------|
| Python cache directories | 1,231 | REMOVE |
| Python .pyc files | 11,415+ | REMOVE |
| Empty log files | 3 | REMOVE |
| Old installer archives | 336 MB | REMOVE |
| Code backup files | 9 files | REVIEW |
| Duplicate Python files | 20+ files | REVIEW |
| Temporary scripts | 2 files | REVIEW |
| Ollama config backups | 7 files | REVIEW |
| Git archive backups | 2 repositories | REVIEW |

**Estimated Space Recovery (if all safe items removed):** ~400+ MB

---

## Next Steps

1. **Captain Review:** Review items marked "REVIEW with Captain"
2. **Approval:** Get approval for deletions
3. **Backup:** Create snapshot before any deletions
4. **Execute:** Remove approved items
5. **Verify:** Confirm system functionality after cleanup

---

*Document generated by Jordan subagent for Miles review.*
*Process: Build → Test → Document → Deploy → Document*
