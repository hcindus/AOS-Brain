# Ollama Upgrade — Prep Notes (NOT YET EXECUTED)

**Status:** PREP ONLY — Captain has NOT authorized execution.
**Date:** 2026-08-16 20:18 UTC
**Goal:** Upgrade Ollama v0.18.0 → latest, then pull `qwen3.8:latest`.

## Current State (snapshot)
- **Ollama version:** 0.18.0 (too old for qwen3.8)
- **Binary:** `/usr/local/bin/ollama` (manual install, NOT apt/snap)
- **OS:** Ubuntu 24.04.4 LTS
- **Service:** systemd unit `/etc/systemd/system/ollama.service`
  - Runs as `User=ollama`, `Group=ollama`
  - Override: `/etc/systemd/system/ollama.service.d/keepalive.conf`
    - `OLLAMA_KEEP_ALIVE=168h`
    - `OLLAMA_NUM_PARALLEL=4`
- **Disk:** 57G free on `/` (plenty for qwen3.8 pull)

## Installed Models (backup list)
| Model | Size |
|-------|------|
| qwen3:latest | 5.2 GB |
| qwen3.5:latest | 6.6 GB |
| qwen2.5:14b | 9.0 GB |
| deepseek-r1:7b | 4.7 GB |
| nous-hermes2:latest | 6.1 GB |
| gemma2:2b | 1.6 GB |
| antoniohudnall/Mort_II:latest | 2.0 GB |
| llama3.1:latest | 4.9 GB |
| mistral:latest | 4.4 GB |
| tinyllama:latest | 637 MB |
| nomic-embed-text:latest | 274 MB |

## Dependencies / Risk
- **AOS Brain** (`aos-brain-v4` service) — depends on Ollama (Mort_II, tinyllama, nomic-embed-text). ACTIVE.
- **Mission Control** (`aos-mission-control`) — ACTIVE.
- Upgrade will briefly restart the Ollama service → brain may need a tick to recover.

## Upgrade Procedure (when authorized)
1. Note current version + model list (done above).
2. Download latest Ollama binary:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
   (or manual: fetch latest release tarball → replace `/usr/local/bin/ollama`)
3. `systemctl restart ollama`
4. Verify: `ollama --version`
5. Pull qwen3.8: `ollama pull qwen3.8:latest`
6. Verify brain recovered: `echo '{"cmd":"status"}' | nc -U /tmp/aos_brain.sock`

## Rollback
- Current binary backed up before overwrite: `cp /usr/local/bin/ollama /usr/local/bin/ollama.0.18.0.bak`
- Models are unaffected by binary upgrade (stored under `/root/.ollama/models` or `~ollama`).

## Open Questions
- [ ] Confirm exact target Ollama version (just "latest" OK?)
- [ ] Confirm qwen3.8 size / whether disk 57G is sufficient (likely yes)
