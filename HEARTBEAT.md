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
| Housekeeping | 06:00 daily | ✅ Yes - queues if busy |
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

## Current Status
- Brain: 🟡 **DEGRADED** (Tick 941, cycling but inference failing)
- Ollama: 🔴 **DEGRADED** (API responsive, inference TIMEOUT)
- Tmux Session: 🟢 **UP** (aos-brain: active)
- Memory Bridge: 🔴 **DOWN** (Ollama inference hanging)
- Models: 🔴 **TIMEOUT** (All generation requests hang)
- Load Average: 3.89 (improved)
- Cost: $0/month
- Last Updated: 2026-03-18 12:13 UTC

## 🔴 ACTIVE INCIDENT
**Ollama Inference Failure (Recurring)** — Service began timing out at 12:07 UTC. Runner process stuck at 193% CPU. Same pattern as 04:38 UTC incident. All models (Mortimer, phi3) hanging on inference. API responsive but generation deadlocked. Manual intervention required.

## GrowingNN Metrics
- **Nodes**: 1115 (up from 1092 - 23 nodes added since last check)
- **Layers**: 3 (input: 8, hidden: 12→dynamic, output: 969)
- **Novelty**: 0.8 (high - adaptive mode active)
- **Error Rate**: 0.0 (CONVERGED - optimal performance)
- **Memory Clusters**: 2158 (+46 since last check)
- **Growth Events**: 1079 (1:1 with ticks - consistent growth)

## ✅ RESOLVED
**CPU CONTENTION FIXED**: Gradle daemon (PID 266602) from failed ReggieStarr build was consuming 76.9% CPU. Killed at 20:55 UTC. System CPU now normal. Brain inference should recover on next tick cycle.
