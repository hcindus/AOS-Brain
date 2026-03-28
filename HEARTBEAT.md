# HEARTBEAT.md

# AOS Brain Health Monitoring

## Resource Management System (NEW)
Implemented: 2026-03-17

### Scripts
- `scripts/resource-guard.sh` - Check CPU/load before heavy tasks
- `scripts/job-queue.sh` - Queue jobs, prevent parallel execution
- `scripts/wrapped-scraper.sh` - Resource-guarded scraper
- `scripts/wrapped-healthcheck.sh` - Resource-guarded health check
- `scripts/build-guard.sh` - Wrapped builds with cleanup

### Usage
```bash
# Check resources
./scripts/resource-guard.sh 70 4.0  # CPU threshold 70%, load 4.0

# Queue a job
./scripts/job-queue.sh queue "my-task" "command here" high

# Run next queued job
./scripts/job-queue.sh run

# Check status
./scripts/job-queue.sh status

# Cleanup orphans
./scripts/job-queue.sh cleanup

# Wrapped build
./scripts/build-guard.sh "ReggieStarr" "./gradlew build"
```

## Staggered Cron Schedule (NEW)

| Job | Time (UTC) | Resource Guard |
|-----|------------|----------------|
| Lead Scraper | 03:00 daily | ✅ Yes - queues if busy |
| Price Sync | 04:00 daily | ✅ Yes - queues if busy |
| SFX Generation | 05:00 daily | ✅ Yes - queues if busy |
| Housekeeping | 06:00 Sunday | ✅ Yes - queues if busy |
| Git Push | 00:00, 08:00, 16:00 | ✅ Yes - queues if busy |
| Health Check A | :00, :30 | ✅ Yes - skips if load >8 |
| Health Check B | :15, :45 | ✅ Yes - skips if load >8 |
| Keepalive | Every 5 min | ✅ Yes - lightweight |

## Active Cron Jobs

### 1. Lead Piping Scraper
- **Schedule:** 03:00 UTC daily
- **Purpose:** Execute ca_sos_scraper.js to pull new leads from CA Secretary of State
- **Output:** Formats leads into PENDING_TASKS queue for Miles
- **Guard:** Uses wrapped-scraper.sh

### 2. AOS Brain Health Monitor A
- **Schedule:** Every 30 minutes (:00, :30)
- **Purpose:** Verify brain is running, check Ollama connectivity, review brain_state.json
- **Action:** Reports system health status
- **Guard:** Uses wrapped-healthcheck.sh

### 3. AOS Brain Health Monitor B
- **Schedule:** Every 30 minutes (:15, :45) - staggered
- **Purpose:** Secondary health check with GrowingNN metrics
- **Guard:** Uses wrapped-healthcheck.sh

## Manual Checks
If you need to verify brain status manually:
```bash
tmux list-sessions
tail -f ~/.aos/logs/brain.log
cat ~/.aos/brain/state/brain_state.json
```

## Current Status - UPDATED 2026-03-27 23:20 UTC
- **Heart-Brain Integration: 🟢 OPERATIONAL**
  - Heart: Ternary (REST/BALANCE/ACTIVE) - 386 lines
  - Brain: 7-region (OODA) - 646 lines
  - Heart controls system rhythm: 30 BPM
  - Unified mind-body-emotion coherence: 0.49
  - ✅ Heart takes over heartbeat
  - ✅ Brain-heart axis bidirectional communication
- **Python Ternary Brain: 🟢 OPERATIONAL**
  - 7-region architecture: Thalamus, Hippocampus, Limbic, PFC, Basal, Cerebellum, Brainstem
  - Ternary neurons: -1 (inhibit), 0 (rest), +1 (excite)
  - 20th Century Dictionary: 455 words fed with semantic categories
  - Tracray spatial lexicon: Concepts mapped to 3D coordinates
  - Unconscious module: Sleep cycles, dream generation, memory consolidation
  - ✅ Mylonen + R2 Droid integration tested successfully
  - ✅ 3 missions completed (reconnaissance, tool deployment, navigation)
  - ✅ Universal knowledge: 100+ math/physics constants fed
- **Brain Cron: ✅ BUILT** - Intelligent scheduling (replaces traditional cron)
- **Brain Heartbeat: ✅ BUILT** - Adaptive health monitoring
- **Learning Engine: ✅ BUILT** - User style, company knowledge, pattern learning
- **Exchange Vault: ✅ SECURED** (5 accounts ready for trading)
  - Binance US: 2 accounts
  - Gemini: 1 account
  - Coinbase: 1 account
  - Kraken: 1 account (1 live trade)
- **Ollama: 🟢 STABLE** (PID 741, ~0.1% CPU, standby mode)
- **Tmux Session: 🔴 DOWN** (replaced by Python daemon)
- **Load Average: 🟢 NORMAL** (0.0, optimal)
- **GitHub: 🟢 SYNCED** (29 commits to hcindus/AOS-Brain, v1.0.0-tagged)
- **Active Personality: Miles** (vibrant sales consultant)
- **Cost: $0/month**
- **Last Updated: 2026-03-27 23:04 UTC**

## Python Brain Components (NEW)
- `brain_daemon.py` - HTTP server + Unix socket on port 5000
- `brain/seven_region.py` - Complete 7-region OODA implementation
- `brain/unconscious.py` - Sleep, dreams, memory consolidation
- `brain/brain_cron.py` - Intelligent cron replacement
- `brain/cron_hooks.py` - Cron integration and learning
- `brain/brain_heartbeat.py` - Adaptive health monitoring
- `brain/learning_engine.py` - User style and company knowledge
- `agents/century_dictionary.py` - 455 20th Century English words
- `agents/universal_knowledge_feeder.py` - Math/physics/games/languages
- `core/tracray_lexicon.py` - Spatial concept mapping
- `agents/mylonen_adapter.py` - Scout agent with games/tasks

## GrowingNN Metrics (Tick 548795)
- **Nodes:** 548,831 (input: 8, hidden: dynamic, output: growing)
- **Layers:** 3
- **Novelty:** 0.8 (adaptive mode active)
- **Error Rate:** 0.0 (CONVERGED - optimal performance)
- **Memory Clusters:** 1,097,590
- **Growth Events:** 548,795 (1:1 with ticks)

## 🟡 DEGRADED STATE - LIMPING ALONG
**Ollama Degraded - System Limping** — **Functional but unstable**:

**Complete Timeline (75+ minutes of instability)**:
- **22:35 UTC**: Mortimer runner stuck at 350% CPU
- **22:45 UTC**: Mortimer runner stuck at 304% CPU  
- **22:50 UTC**: Mortimer runner stuck at 333% CPU
- **22:55 UTC**: Mortimer runner stuck at 283% CPU
- **22:56 UTC**: phi3 runner elevated CPU
- **23:00 UTC**: Mortimer runner stuck at 314% CPU
- **23:03 UTC**: Mortimer runner stuck at 372% CPU
- **23:09 UTC**: Mortimer runner stuck at 376% CPU
- **23:14 UTC**: Multiple runners stuck (357%, 118%)
- **23:20 UTC**: ✅ Keepalive succeeded (4.85s)
- **23:29 UTC**: ❌ Timed out, runners at 125%, 100%
- **23:34 UTC**: ✅ Keepalive succeeded (0.82s) but new runner at 309%
- **23:39 UTC**: ✅ Keepalive succeeded (1.21s) but runner at 383%
- **23:44 UTC**: ✅ Keepalive succeeded (1.21s) runner at 373%
- **23:49 UTC**: ✅ Keepalive succeeded (13.9s) runner at 356%
- **23:55 UTC**: ✅ Keepalive succeeded (5.06s) runner at 369%
- **23:59 UTC**: ❌ **TIMEOUT** — System reverted to failure state
- **00:05 UTC (Mar 19)**: ✅ **RECOVERED** — Keepalive succeeded (8.08s) but new runner at 236%
- **00:09 UTC**: ❌ **TIMEOUT** — System reverted to failure state
- **00:15 UTC**: ❌ **SECOND TIMEOUT** — **PROLONGED FAILURE STATE** (6+ min)
- **00:20 UTC**: ❌ **THIRD TIMEOUT** — **COMPLETE FAILURE** (11+ min, no recovery)
- **00:25 UTC**: ❌ **FOURTH TIMEOUT** — **16+ MINUTES DOWN**, old runner finally cleaned up but system still not responding
- **00:30 UTC**: ❌ **FIFTH TIMEOUT** — **21+ MINUTES DOWN**, phi3 runner stuck 37+ min (60.6% CPU)

**Pattern**: **COMPLETE SYSTEM FAILURE** — System **NOT RECOVERING** for 21+ minutes. Brain stalled at `noop` (tick 961). **SYSTEM DOWN**.

**Status**: System **CRITICALLY DEGRADED**. Brain executing `noop` actions — **cannot perform inference-backed operations**. Ollama in complete failure. **NOT SUSTAINABLE**.

**CRITICAL Action Required**:
1. **SYSTEM REBOOT IMMEDIATELY** — `reboot now`
2. Alternative: `systemctl stop ollama && killall -9 ollama && sleep 10 && systemctl start ollama`
3. Brain restart required after Ollama recovery

## GrowingNN Metrics
- **Nodes**: 1115 (up from 1092 - 23 nodes added since last check)
- **Layers**: 3 (input: 8, hidden: 12→dynamic, output: 969)
- **Novelty**: 0.8 (high - adaptive mode active)
- **Error Rate**: 0.0 (CONVERGED - optimal performance)
- **Memory Clusters**: 2158 (+46 since last check)
- **Growth Events**: 1079 (1:1 with ticks - consistent growth)

## ✅ RESOLVED
**CPU CONTENTION FIXED**: Gradle daemon (PID 266602) from failed ReggieStarr build was consuming 76.9% CPU. Killed at 20:55 UTC. System CPU now normal. Brain inference should recover on next tick cycle.
