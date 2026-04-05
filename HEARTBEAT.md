<!--
VERSION: 4.2.0
UPDATED: 2026-04-05 06:50 UTC
CHANGELOG: Upgraded to v4.2 with Thyroid v1.1 and Model Router
-->

# HEARTBEAT.md

# AOS Brain Health Monitoring

## Current Status - UPDATED 2026-04-05 06:50 UTC

**✅ COMPLETE BRAIN v4.2 RUNNING** - 2026-04-05 06:50 UTC

### What's New in v4.2
- 🫁 **Thyroid v1.1** - Reflexive mode switching (LOCAL ↔ OLLAMA)
- 🤖 **Model Router** - tinyllama for decisions, Mort_II for voice
- 📊 **Memory-aware cost budget** - Auto-coughs to LOCAL when memory >75%
- 🎛️ **Mission Control v2.1** - New /api/thyroid and /api/router endpoints

### System Status (Live)
| System | Status | Details |
|--------|--------|---------|
| **Complete Brain v4.2** | ✅ RUNNING | 12 components active |
| **Service** | ✅ ACTIVE | PID 1467233, uptime 01:32 |
| **Memory** | ✅ HEALTHY | 59% used, 6.2 GB available |
| **Ollama** | ✅ CONNECTED | Status 200 |
| **Socket** | ✅ READY | `/tmp/aos_brain.sock` |
| **Mission Control** | ✅ ACTIVE | v2.1.0 on port 8080 |
| **Thyroid** | ✅ ACTIVE | OLLAMA mode, 0 failures |
| **Model Router** | ✅ ACTIVE | tinyllama decisions, Mort_II voice |

### Components Status

#### Core (4/4) ✅
| Component | Status | Notes |
|-----------|--------|-------|
| SuperiorHeart | ✅ RUNNING | REST/BALANCE/ACTIVE ternary |
| Stomach v2 | ✅ RUNNING | HUNGRY/SATISFIED/FULL |
| Intestine v2 | ✅ RUNNING | Distribution system active |
| Brain v3.1 | ✅ RUNNING | 7-region OODA |

#### Enhanced Components (4/4) ✅ NEW v4.2
| Component | Status | Notes |
|-----------|--------|-------|
| Thyroid v1.1 | ✅ ACTIVE | Reflexive mode switching, memory-aware |
| Model Router | ✅ ACTIVE | tinyllama decisions, Mort_II voice |
| QMD Loop | ✅ RUNNING | tinyllama default in OLLAMA mode |
| MemoryBridge | ✅ ACTIVE | nomic-embed-text embeddings |

#### Legacy Components (3/3) ✅
| Component | Status | Notes |
|-----------|--------|-------|
| 3D Cortex | ✅ ACTIVE | 3x32x32 neural volume |
| TracRay | ✅ ACTIVE | Memory trajectory tracking |
| Consciousness Layers | ✅ ACTIVE | Con/Subcon/Uncon integrated |

#### Sensory (2/2) ✅
| Component | Status | Notes |
|-----------|--------|-------|
| Voice Interface | ✅ ACTIVE | 7 voices, TTS via Mort_II |
| Vision Interface | ⚠️ STUB | OpenCV not available |

#### Interface (1/1) ✅
| Component | Status | Notes |
|-----------|--------|-------|
| Socket Server | ✅ RUNNING | Unix socket for diagnostics |

### Mission Control v2.1
| Component | URL | Status |
|-----------|-----|--------|
| Three.js Visualizer | http://localhost:8080 | ✅ Active |
| Status API | http://localhost:8080/api/status | ✅ Active |
| Triage API | http://localhost:8080/api/triage | ✅ Active |
| Diagnostic API | http://localhost:8080/api/diagnostic | ✅ Active |
| Brain API | http://localhost:8080/api/brain | ✅ Active |
| Thyroid API | http://localhost:8080/api/thyroid | ✅ Active 🆕 |
| Router API | http://localhost:8080/api/router | ✅ Active 🆕 |
| Decide API | POST /api/decide | ✅ Active 🆕 |
| Speak API | POST /api/speak | ✅ Active 🆕 |
| Command API | POST /api/command | ✅ Active |

### Service Health
```
Active: active (running)
Main PID: 1467233 (python3)
Memory: 59% (6.2G available)
Load: Normal
Uptime: 01:32
Thyroid Mode: OLLAMA
Router Decision: tinyllama:latest
Router Voice: antoniohudnall/Mort_II:latest
```

### New Socket Commands (v4.2)
```bash
# Get Thyroid status
echo '{"cmd":"thyroid"}' | nc -U /tmp/aos_brain.sock

# Get Router status
echo '{"cmd":"router"}' | nc -U /tmp/aos_brain.sock

# Make decision via Router
echo '{"cmd":"decide","params":{"context":{"novelty":0.8}}}' | nc -U /tmp/aos_brain.sock

# Generate voice via Router
echo '{"cmd":"speak","params":{"message":"Hello"}}' | nc -U /tmp/aos_brain.sock

# Promote to OLLAMA mode
echo '{"cmd":"promote","params":{"importance":0.9}}' | nc -U /tmp/aos_brain.sock
```

### Diagnostic Commands
```bash
# Quick triage check
python3 /root/.openclaw/workspace/aocros/mission_control/diagnostic.py triage

# Full diagnostic
python3 /root/.openclaw/workspace/aocros/mission_control/diagnostic.py diagnostic

# System status
python3 /root/.openclaw/workspace/aocros/mission_control/diagnostic.py status

# Brain direct query
python3 /root/.aos/aos/complete_test_suite.py
```

### Architecture v4.2
```
Complete Brain v4.2
├── SuperiorHeart (Ternary emotion)
├── Stomach v2 (Information digestion)
├── Intestine v2 (Distribution)
├── Brain v3.1 (7-region OODA)
├── 3D Cortex (Spatial consciousness)
├── TracRay (Memory trajectories)
├── Consciousness Layers (Con/Subcon/Uncon)
├── QMD Loop (tinyllama in OLLAMA mode)
├── MemoryBridge (nomic-embed-text)
├── Voice Manager (TTS via Mort_II)
├── Vision Manager (Camera/stub)
├── Socket Server (Unix socket interface)
├── Thyroid v1.1 (Reflexive mode switching) ← NEW
├── Model Router (tinyllama/Mort_II/nomic) ← NEW
└── Mission Control (v2.1 on port 8080)
```

### File Locations
| File | Path | Purpose |
|------|------|---------|
| Brain | `/root/.aos/aos/complete_brain_v4.py` | Main brain (v4.2) |
| Thyroid | `/root/.aos/aos/thyroid.py` | Reflexive mode switcher |
| Model Router | `/root/.aos/aos/model_router.py` | Model selection per task |
| Mission Control | `/root/.openclaw/workspace/aocros/mission_control/server_v2.py` | HTTP server (v2.1) |
| Diagnostic Tool | `/root/.aos/aos/complete_test_suite.py` | Test suite |
| Brain Service | `/etc/systemd/system/aos-brain-v4.service` | Systemd service |
| MC Service | `/etc/systemd/system/aos-mission-control.service` | Systemd service |
| Socket | `/tmp/aos_brain.sock` | Brain communication |
| Docs | `/root/.aos/docs/BRAIN_v42_DEPLOYMENT.md` | Deployment guide |

### BHSI v4 Status
**✅ BHSI v4 INTEGRATED WITH BRAIN v4.2**

| Component | Status | Function |
|-----------|--------|----------|
| **BHSI Core** | ✅ READY | Heart + Stomach + Intestines |
| **Heart v4** | ✅ READY | 72 BPM ternary |
| **Stomach v4** | ✅ READY | Resource management |
| **Intestines v4** | ✅ READY | Error absorption |
| **Socket** | ✅ READY | `/tmp/bhsi_v4.sock` |
| **Integration** | ✅ CONNECTED | Brain v4.2 + BHSI |

**Files:** `/root/.openclaw/workspace/aocros/BHSI/`

### Model Router Configuration
| Task | Model | Size | Latency |
|------|-------|------|---------|
| Decision | tinyllama:latest | 1.1B | ~900ms |
| Voice | Mort_II:latest | 7B | ~3000ms |
| Embedding | nomic-embed-text:latest | - | ~100ms |

### Thyroid v1.1 Configuration
| Parameter | Value | Description |
|-----------|-------|-------------|
| check_interval | 30s | Health check frequency |
| failure_threshold | 3 | Failures before coughing to LOCAL |
| memory_threshold | 75% | Auto-cough when exceeded |
| hysteresis | 60s | Minimum time between switches |

### Last Updated
2026-04-05 06:50 UTC

---

## Archive

### 2026-04-05 06:50 UTC - v4.2 Deployed
- Thyroid v1.1 integrated
- Model Router with tinyllama/Mort_II
- Memory-aware cost budget
- Mission Control v2.1

### 2026-04-02 05:15 UTC - v4.1 with BHSI v4
- Binary High-Integrity System
- Socket interface for diagnostics
- Triage and diagnostic capabilities

### 2026-04-01 04:51 UTC - Complete Brain v4.0 with Mission Control
- 1,300+ curriculum items fed
- Three.js brain visualizer deployed
- Agent script library (24 scripts)

### 2026-04-01 00:30 UTC - Complete Brain v4.0 Deployed
- Heart + Stomach + Intestine + Brain
- 10 components active
- Service-based (no tmux)

### 2026-03-31 23:57 UTC - Enhanced Ternary Deployed

### 2026-03-31 14:05 UTC - Ternary Brain Test Successful

### 2026-03-31 12:19 UTC - Previous Brain Reset

---

## BHSI v4 Deployment - 2026-04-02 05:16 UTC

**✅ BHSI v4 INTEGRATED WITH BRAIN v4.1**

| Component | Status | Details |
|-----------|--------|---------|
| **BHSI v4** | ✅ RUNNING | Binary High-Integrity System |
| **Heart** | ✅ ACTIVE | 72 BPM ternary |
| **Stomach** | ✅ ACTIVE | Resource management |
| **Intestines** | ✅ ACTIVE | Error absorption |
| **Socket** | ✅ READY | /tmp/bhsi_v4.sock |
| **Integration** | ✅ CONNECTED | Brain v4.1 + BHSI |

**Service:** aos-bhsi-v4
**Log:** /var/log/aos/bhsi/bhsi_v4.log

---
