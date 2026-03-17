# HEARTBEAT.md

# AOS Brain Health Monitoring

## Active Cron Jobs

### 1. Lead Piping Scraper
- **Schedule:** Every 24 hours (86400000ms)
- **Purpose:** Execute ca_sos_scraper.js to pull new leads from CA Secretary of State
- **Output:** Formats leads into PENDING_TASKS queue for Miles

### 2. AOS Brain Health Monitor (NEW)
- **Schedule:** Every 30 minutes (1800000ms)
- **Purpose:** Verify brain is running, check Ollama connectivity, review brain_state.json
- **Action:** Reports system health status

## Manual Checks
If you need to verify brain status manually:
```bash
tmux list-sessions
tail -f ~/.aos/logs/brain.log
cat ~/.aos/brain/state/brain_state.json
```

## Current Status
- Brain: 🔴 **DOWN** (Tick 998 frozen, no tmux sessions)
- Ollama: 🟢 **STABLE** (6 consecutive keepalives succeeded since 07:34 UTC)
- Tmux Session: NOT FOUND
- Memory Bridge: ACTIVE (8 chunks indexed, semantic retrieval working)
- Models: Loaded but inference broken
- Cost: $0/month
- Last Updated: 2026-03-17 06:19 UTC

## ⚠️ CRITICAL ALERT
**OLLAMA SERVICE RECOVERED**: /api/generate endpoint responding at 06:59 UTC after multiple failures. AOS brain restart is now possible. Brain has been down since tick 998 (~13+ hours ago).
