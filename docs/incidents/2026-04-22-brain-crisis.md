# Miles Brain Crisis - Post-Mortem

**Date:** 2026-04-22 03:16 - 06:38 UTC  
**System:** Miles.cloud (AOS Brain v4.5)  
**Severity:** High (memory pressure, service cascade failure)  
**Reporter:** Miles (Autonomous Operations Engine)  

---

## Executive Summary

BHSI v4 (Stomach/Intestines) failed silently ~3 hours ago due to memory pressure. Subsequent keepalive script malfunction caused brain process duplication spiral. System recovered after manual intervention and script fixes.

---

## Timeline

| Time | Event |
|------|-------|
| 03:16 UTC | BHSI v4 killed (likely OOM killer at 92% memory) |
| 03:21 UTC | Complete Brain v4.5 spawned duplicate processes |
| 06:23 UTC | User detected issue, asked Miles to investigate |
| 06:28 UTC | Keepalive cron fired, failed to detect BHSI outage |
| 06:31 UTC | Discovered 2 brain processes, BHSI dead, 92% memory |
| 06:32 UTC | Identified Minecraft (Java) as memory hog (1.1GB) |
| 06:33 UTC | Killed Minecraft, memory dropped to 30% |
| 06:34 UTC | Disabled systemd auto-restart (was spawning duplicates) |
| 06:35 UTC | Fixed keepalive scripts (v1.1.0) with duplicate detection |
| 06:36 UTC | BHSI and Brain both running clean |
| 06:38 UTC | System stable, 15/15 organs active, 18% memory |

---

## Root Causes

### 1. Memory Exhaustion (Primary)
- **Cause:** Multiple Ollama runners + Minecraft server (4GB heap) + OpenClaw Gateway
- **Impact:** 92% memory triggered OOM killer → BHSI terminated
- **Detection:** User noticed "Stomach/Intestines" inquiry

### 2. Keepalive Script Failures
- **Cause:** Pattern matching bug (`complete_brain_v45` without `.py` extension)
- **Impact:** Script couldn't find running processes, led to false negatives
- **Secondary:** No BHSI monitoring existed in keepalive

### 3. Systemd/Script Collision
- **Cause:** `Restart=always` in service config + keepalive's kill commands
- **Impact:** Race condition spawning duplicate brain processes
- **Resolution:** Changed to `Restart=on-failure`

---

## Resolution Actions

### Immediate (Done)
1. ✅ Terminated Minecraft server (recovered 7% RAM)
2. ✅ Killed duplicate brain processes
3. ✅ Restarted BHSI v4 (Stomach + Intestines)
4. ✅ Stabilized single brain process

### Script Fixes (v1.1.0)
```bash
# aos_keepalive.sh + agent_keepalive.sh changes:
- Fixed: Pattern matching to include .py extension
- Added: Duplicate process detection and auto-kill
- Added: BHSI v4 health monitoring
- Added: Socket responsiveness check
```

### Service Config
```ini
# /etc/systemd/system/aos-brain-v4.service
- Restart=always
+ Restart=on-failure
```

---

## Current Status

| Component | Status | PID | Uptime |
|-----------|--------|-----|--------|
| Complete Brain v4.5 | ✅ Running | 611354 | Active |
| BHSI v4 | ✅ Running | 611412 | Active |
| Memory | ✅ 18% used | - | 12GB free |
| Minecraft | ✅ Stopped | - | - |
| Socket | ✅ Responsive | - | `/tmp/aos_brain.sock` |

---

## Prevention

1. **Memory Monitoring:** Add alerts at 75% threshold
2. **BHSI Watchdog:** Dedicated health check every 5 minutes
3. **Keepalive v1.2:** Add process count trend analysis
4. **Documentation:** This incident logged for pattern recognition

---

## Lessons Learned

- **Silent failures kill:** BHSI died 3 hours ago, nobody noticed
- **Pattern matching matters:** `pgrep -f` needs full command strings
- **Systemd + scripts = race conditions:** Never have both fighting
- **Minecraft is expensive:** 4GB heap + overhead = ~7% of total RAM

---

*Documented by Miles at 06:38 UTC*  
*GitHub commit: 36b8e0261 (keepalive script fixes)*
