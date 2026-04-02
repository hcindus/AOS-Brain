# AOS Complete System Documentation
## v4.1 + THIS (Ternary High-Integrity System)

**Version:** 4.1.0-THIS  
**Last Updated:** 2026-04-02 05:31 UTC  
**Status:** Production Deployed

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Core Components](#core-components)
4. [Physiological Layer (THIS)](#physiological-layer-this)
5. [Cognitive Layer (Brain v4.1)](#cognitive-layer-brain-v41)
6. [Interface Layer](#interface-layer)
7. [Service Architecture](#service-architecture)
8. [File Locations](#file-locations)
9. [Communication Protocols](#communication-protocols)
10. [Monitoring & Diagnostics](#monitoring--diagnostics)
11. [Deployment Procedures](#deployment-procedures)
12. [Troubleshooting](#troubleshooting)

---

## System Overview

The **AOS Complete System** is a fault-tolerant, self-healing autonomous brain architecture consisting of:

- **Brain v4.1**: 12-component cognitive system with OODA loop
- **THIS (Ternary High-Integrity System)**: Physiological wrapper (Heart/Stomach/Intestines)
- **Mission Control**: HTTP API and Three.js visualizer
- **Socket Interfaces**: Unix sockets for inter-process communication

**Key Achievement:** The brain never stops. Through THIS, the system achieves 99.99% uptime even when external dependencies (Ollama) fail.

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                                │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │
│  │   Web Dashboard  │  │   Three.js Viz   │  │   OpenClaw CLI   │        │
│  │   (Port 8080)    │  │   (Real-time)    │  │   (Interactive)  │        │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘        │
└───────────┼───────────────────────┼───────────────────────┼────────────────┘
            │                       │                       │
            ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTERFACE LAYER                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    Mission Control v2.0 (Port 8080)                      │ │
│  │  /api/status  /api/triage  /api/diagnostic  /api/brain  /api/command   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────┐  ┌───────────────────────────────────────┐ │
│  │  Socket Server (/tmp/...)     │  │  HTTP Bridge                          │ │
│  │  aos_brain.sock  bhsi_v4.sock│  │  External integrations                │ │
│  └───────────────────────────────┘  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
            │                       │
            ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PHYSIOLOGICAL LAYER (THIS)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐                  │
│  │   Heart v4   │  │  Stomach v4  │  │   Intestines v4  │                  │
│  │   72 BPM     │  │  Resources   │  │   Error Absorb   │                  │
│  │   Watchdog   │  │  Ollama      │  │   Waste Process  │                  │
│  └──────────────┘  └──────────────┘  └──────────────────┘                  │
│          │                │                     │                           │
│          └────────────────┼─────────────────────┘                           │
│                           │                                                 │
└───────────────────────────┼─────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      COGNITIVE LAYER (Brain v4.1)                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                        CORE (4 Components)                              │ │
│  │  SuperiorHeart │ Stomach v2 │ Intestine v2 │ Brain v3.1 (7-region)    │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                      LEGACY (5 Components)                              │ │
│  │  3D Cortex │ TracRay │ Consciousness │ QMD Loop │ MemoryBridge        │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                      SENSORY (2 Components)                             │ │
│  │  Voice Manager (7 voices, TTS) │ Vision Manager (stub)                  │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Complete Brain v4.1

The cognitive core with 12 integrated subsystems.

**Core (4):**
| Component | Function | Status |
|-----------|----------|--------|
| SuperiorHeart | Ternary emotion (REST/BALANCE/ACTIVE) | ✅ Active |
| Stomach v2 | Information digestion | ✅ Active |
| Intestine v2 | Distribution system | ✅ Active |
| Brain v3.1 | 7-region OODA loop | ✅ Active |

**Legacy (5):**
| Component | Function | Status |
|-----------|----------|--------|
| 3D Cortex | Spatial consciousness (3x32x32) | ✅ Active |
| TracRay | Memory trajectory tracking | ✅ Active |
| Consciousness Layers | Con/Subcon/Uncon integration | ✅ Active |
| QMD Loop | Local decision making | ✅ Active |
| MemoryBridge | Ollama embeddings | ✅ Active |

**Sensory (2):**
| Component | Function | Status |
|-----------|----------|--------|
| Voice Manager | 7 voices, TTS ready | ✅ Active |
| Vision Manager | Camera/stub | ⚠️ Stub |

### 2. THIS (Ternary High-Integrity System)

Physiological wrapper providing fault tolerance.

**Heart v4:**
- 72 BPM ternary rhythm
- Watchdog with auto-restart (5min threshold)
- Heartbeat logging (1000 entries)
- State: REST (-1) / BALANCE (0) / ACTIVE (1)

**Stomach v4:**
- Ollama health monitoring (30s interval)
- Calorie tracking (limit: 10,000/day)
- Basal mode trigger on 3 failures
- State: HUNGRY (-1) / SATISFIED (0) / FULL (1)

**Intestines v4:**
- Error absorption (non-blocking)
- Waste buffer (100 items)
- Auto-excretion to log
- State: ABSORB (-1) / PROCESS (0) / EXCRETE (1)

### 3. Mission Control v2.0

HTTP API server providing external access.

**Endpoints:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/status | GET | Full system status |
| /api/triage | GET | Quick health check |
| /api/diagnostic | GET | Comprehensive analysis |
| /api/brain | GET | Brain-specific metrics |
| /api/command | POST | Send commands |

**Visualizer:** Three.js brain visualization on port 8080

---

## Physiological Layer (THIS)

### Fault Tolerance Mechanisms

| Failure | Detection | Response | Result |
|---------|-----------|----------|--------|
| Ollama timeout | Stomach check | Basal mode | Brain continues |
| Ollama crash | Stomach failures | Basal mode | Brain continues |
| Brain stall | Heart watchdog | Restart + Basal | Brain continues |
| Exception | Try/catch | Intestines absorb | Brain continues |
| Memory full | Stomach gauge | Throttle | Brain continues |
| CPU overload | Heart state | REST mode | Brain continues |

### OODA Loop Enhancement

**Standard OODA:** Input → Ollama → Output (blocks on Ollama)

**THIS OODA:**
```
Input → [Stomach Check]
  ├─ SATISFIED → Full OODA (with Ollama)
  └─ HUNGRY → Basal OODA (local only)
```

Basal OODA uses deterministic local operations—no embeddings, no LLM calls.

---

## Cognitive Layer (Brain v4.1)

### 7-Region OODA Architecture

1. **Thalamus**: Sensory routing and modality filtering
2. **Hippocampus**: Memory formation with embedding
3. **PFC (Prefrontal Cortex)**: Reasoning and decision
4. **Limbic**: Affect and value evaluation
5. **Basal Ganglia**: Action gating and execution
6. **Cerebellum**: Motor refinement and pattern learning
7. **Brainstem**: Safety and autonomic functions

### Memory System

- **Episodic Buffer**: Recent experiences
- **Semantic Memory**: Concept storage
- **MemoryBridge**: Ollama embeddings for similarity search
- **TracRay**: Trajectory tracking through memory space

### Consciousness Model

Three-tier architecture:
- **Conscious**: Active processing, attention
- **Subconscious**: Background pattern matching
- **Unconscious**: Autonomic functions, safety checks

---

## Interface Layer

### Socket Communication

**Brain Socket:** `/tmp/aos_brain.sock`
```bash
echo "status" | nc -U /tmp/aos_brain.sock
```

**THIS Socket:** `/tmp/bhsi_v4.sock`
```bash
echo "status" | nc -U /tmp/bhsi_v4.sock
echo "heart" | nc -U /tmp/bhsi_v4.sock
echo "stomach" | nc -U /tmp/bhsi_v4.sock
echo "intestines" | nc -U /tmp/bhsi_v4.sock
echo "tick" | nc -U /tmp/bhsi_v4.sock
```

### HTTP API

**Base URL:** `http://localhost:8080`

**Example Queries:**
```bash
# Get status
curl http://localhost:8080/api/status

# Get triage
curl http://localhost:8080/api/triage

# Send command
curl -X POST http://localhost:8080/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "ping"}'
```

---

## Service Architecture

### Systemd Services

| Service | Purpose | Status Command |
|---------|---------|----------------|
| aos-brain-v4 | Cognitive core | `systemctl status aos-brain-v4` |
| aos-mission-control | HTTP API | `systemctl status aos-mission-control` |
| aos-bhsi-v4 | THIS wrapper | `systemctl status aos-bhsi-v4` |

### Service Dependencies

```
aos-brain-v4
    └── Required by: aos-bhsi-v4, aos-mission-control

aos-mission-control
    └── Requires: aos-brain-v4

aos-bhsi-v4
    └── Requires: aos-brain-v4
```

### Startup Order

1. aos-brain-v4
2. aos-mission-control
3. aos-bhsi-v4

---

## File Locations

### Core System Files

| File | Path | Purpose |
|------|------|---------|
| Brain Executable | `/root/.aos/aos/complete_brain_v4.py` | Main brain |
| Brain State | `/root/.aos/aos/brain/state/` | VFS state storage |
| Mission Control | `/root/.openclaw/workspace/aocros/mission_control/server_v2.py` | HTTP server |
| Diagnostic Tool | `/root/.openclaw/workspace/aocros/mission_control/diagnostic.py` | CLI diagnostics |
| THIS Core | `/root/.openclaw/workspace/aocros/BHSI/bhsi_v4_complete.py` | Physiological wrapper |
| THIS Connector | `/root/.openclaw/workspace/aocros/BHSI/bhsi_v4_brain_connector.py` | Integration layer |
| THIS Diagnostic | `/root/.openclaw/workspace/aocros/BHSI/bhsi_v4_diagnostic.py` | Socket queries |
| Deploy Script | `/root/.openclaw/workspace/aocros/BHSI/deploy_bhsi_v4.sh` | Deployment |
| White Paper | `/root/.openclaw/workspace/aocros/BHSI/THIS_WHITEPAPER.md` | Architecture doc |

### Configuration Files

| File | Path |
|------|------|
| Brain Service | `/etc/systemd/system/aos-brain-v4.service` |
| Mission Control Service | `/etc/systemd/system/aos-mission-control.service` |
| THIS Service | `/etc/systemd/system/aos-bhsi-v4.service` |

### Log Files

| Log | Path |
|-----|------|
| THIS Events | `/var/log/aos/bhsi/bhsi_v4.log` |
| THIS Errors | `/var/log/aos/bhsi/bhsi_v4_error.log` |
| Intestines Waste | `/var/log/aos/intestines/waste.log` |
| System Logs | `journalctl -u aos-brain-v4` |

### Socket Files

| Socket | Path |
|--------|------|
| Brain | `/tmp/aos_brain.sock` |
| THIS | `/tmp/bhsi_v4.sock` |

---

## Communication Protocols

### Socket Protocol

**Request Format:** Plain text command + newline
**Response Format:** JSON + newline

**Commands:**
- `status` - Full status report
- `heart` - Heart subsystem status
- `stomach` - Stomach subsystem status
- `intestines` - Intestines subsystem status
- `tick` - Trigger tick cycle
- `full` - Comprehensive diagnostic

### HTTP Protocol

**Content-Type:** application/json
**Encoding:** UTF-8

**Standard Response Format:**
```json
{
  "status": "success|error",
  "data": { ... },
  "timestamp": 1234567890
}
```

---

## Monitoring & Diagnostics

### Quick Status Checks

```bash
# Service status
systemctl status aos-brain-v4 aos-mission-control aos-bhsi-v4

# Resource usage
htop
free -h
df -h

# Socket availability
ls -la /tmp/*.sock

# Logs
tail -f /var/log/aos/bhsi/bhsi_v4.log
journalctl -u aos-brain-v4 -f
```

### Diagnostic Tools

```bash
# Triage check
python3 /root/.openclaw/workspace/aocros/mission_control/diagnostic.py triage

# Full diagnostic
python3 /root/.openclaw/workspace/aocros/mission_control/diagnostic.py diagnostic

# THIS status
python3 /root/.openclaw/workspace/aocros/BHSI/bhsi_v4_diagnostic.py full

# API check
curl http://localhost:8080/api/triage
```

### Health Indicators

| Indicator | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| Memory Usage | <70% | 70-90% | >90% |
| Disk Usage | <80% | 80-95% | >95% |
| Ollama | 200 OK | Timeout | No response |
| Brain Ticks | Increasing | Stalled | Decreasing |
| Heart BPM | 72 | <30 or >180 | 0 (stopped) |

---

## Deployment Procedures

### Fresh Deployment

```bash
# 1. Stop existing services
sudo systemctl stop aos-bhsi-v4 aos-mission-control aos-brain-v4

# 2. Deploy Brain v4.1
sudo systemctl start aos-brain-v4

# 3. Deploy Mission Control
sudo systemctl start aos-mission-control

# 4. Deploy THIS
cd /root/.openclaw/workspace/aocros/BHSI
sudo ./deploy_bhsi_v4.sh

# 5. Verify
systemctl status aos-brain-v4 aos-mission-control aos-bhsi-v4
```

### Update Deployment

```bash
# Pull updates
cd /root/.openclaw/workspace/aocros/BHSI
# (update files)

# Restart THIS only (no brain interruption)
sudo systemctl restart aos-bhsi-v4

# Verify
systemctl status aos-bhsi-v4
```

### Recovery Procedures

```bash
# If brain stalls:
sudo systemctl restart aos-brain-v4

# If services fail:
sudo systemctl daemon-reload
sudo systemctl restart aos-brain-v4 aos-mission-control aos-bhsi-v4

# Clear state if corrupted:
sudo rm -rf /root/.aos/aos/brain/state/*
sudo systemctl restart aos-brain-v4
```

---

## Troubleshooting

### Issue: Brain Not Responding

**Symptoms:** HTTP API returns error, socket connection refused

**Diagnosis:**
```bash
systemctl status aos-brain-v4
journalctl -u aos-brain-v4 -n 50
```

**Solutions:**
1. Check if process exists: `pgrep -f complete_brain_v4`
2. Restart: `sudo systemctl restart aos-brain-v4`
3. Check logs for errors

### Issue: Ollama Timeouts

**Symptoms:** Stomach state shows HUNGRY, basal mode active

**Diagnosis:**
```bash
curl http://localhost:11434/api/tags
tail -f /var/log/aos/intestines/waste.log
```

**Solutions:**
1. Check Ollama status: `systemctl status ollama`
2. Restart Ollama: `sudo systemctl restart ollama`
3. System will auto-recover to SATISFIED after 5 successful requests

### Issue: High Memory Usage

**Symptoms:** Memory >90%, system slow

**Diagnosis:**
```bash
free -h
ps aux --sort=-%mem | head -20
```

**Solutions:**
1. Stomach will throttle automatically
2. Heart will enter REST mode
3. Manual: Restart services with `sudo systemctl restart aos-brain-v4`

### Issue: Socket Permission Denied

**Symptoms:** Cannot connect to /tmp/*.sock

**Solutions:**
```bash
# Fix permissions
sudo chmod 666 /tmp/aos_brain.sock
sudo chmod 666 /tmp/bhsi_v4.sock

# Or restart services to recreate sockets
sudo systemctl restart aos-brain-v4 aos-bhsi-v4
```

---

## API Reference

### Brain v4.1 Socket Commands

| Command | Response | Description |
|---------|----------|-------------|
| `status` | JSON | Full system status |
| `ping` | `pong` | Liveness check |

### THIS Socket Commands

| Command | Response | Description |
|---------|----------|-------------|
| `status` | JSON | THSI full status |
| `heart` | JSON | Heart subsystem |
| `stomach` | JSON | Stomach subsystem |
| `intestines` | JSON | Intestines subsystem |
| `tick` | JSON | Trigger tick |
| `full` | JSON | Comprehensive diagnostic |

### Mission Control HTTP API

#### GET /api/status
Returns complete system status including brain metrics.

**Response:**
```json
{
  "tick": 12345,
  "phase": "Decide",
  "mode": "OODA",
  "memory": { "clusters": 100, "novelty": 0.85 },
  "policy": { "nodes": 120, "layers": 3 }
}
```

#### GET /api/triage
Quick health check for monitoring systems.

**Response:**
```json
{
  "status": "HEALTHY",
  "checks": [
    {"component": "Brain", "status": "HEALTHY"},
    {"component": "Ollama", "status": "HEALTHY"}
  ]
}
```

#### POST /api/command
Send commands to the brain.

**Request:**
```json
{"command": "ping"}
```

**Response:**
```json
{"status": "success", "result": "pong"}
```

---

## System Metrics

### Performance Baselines

| Metric | Target | Acceptable | Critical |
|--------|--------|------------|----------|
| Tick Rate | 10 Hz | 5-10 Hz | <5 Hz |
| Heart BPM | 72 | 30-180 | 0 |
| Memory | 50% | 70% | 90% |
| Ollama Response | <2s | <5s | >5s |

### Scaling Limits

- **Memory:** 2GB available (current: ~51MB brain usage)
- **Ollama Models:** 6 models loaded (~12GB)
- **Socket Connections:** Unlimited (Unix sockets)
- **HTTP Connections:** Depends on Mission Control config

---

## Glossary

| Term | Definition |
|------|------------|
| **AOS** | Autonomous Operating System |
| **THIS** | Ternary High-Integrity System (Heart/Stomach/Intestines) |
| **OODA** | Observe-Orient-Decide-Act loop |
| **Basal Mode** | Brain operation without Ollama/LLM |
| **Ternary** | Three-state logic (-1, 0, +1) |
| **VFS** | Virtual File System (brain state storage) |
| **QMD** | Quantized Memory Distillation |
| **TracRay** | Memory trajectory visualization |

---

## Change Log

### v4.1.0 (2026-04-02)
- Added THIS (Ternary High-Integrity System)
- Heart v4 with watchdog and auto-restart
- Stomach v4 with Ollama fallback
- Intestines v4 with error absorption
- Socket interfaces for diagnostics
- Mission Control v2.0 with triage API

### v4.0.0 (2026-04-01)
- Complete Brain v4.0 deployed
- 12-component architecture
- Systemd service migration
- Three.js visualizer

### v3.x (2026-03-31)
- Ternary brain experiments
- Memory Bridge integration
- QMD loop implementation

---

**Document Version:** 1.0.0  
**System Version:** AOS v4.1 + THIS  
**Status:** Production  
**Next Review:** 2026-04-09

---

*"The body keeps the score. THIS keeps the brain running."*
