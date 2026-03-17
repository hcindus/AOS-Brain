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
- Brain: 🔴 **DOWN/STALLED** (Tick 462, no change since 17:44 UTC - 2.5+ hours ago)
- Tmux Session: NOT FOUND
- Memory Bridge: ACTIVE (8 chunks indexed, semantic retrieval working)
- Models: qwen2.5:3b, phi3:3.8b, phi3:latest, nomic-embed-text, Mortimer:latest
- Cost: $0/month
- Last Updated: 2026-03-16 20:16 UTC

## ⚠️ CRITICAL ALERT
Brain process stalled at 17:44 UTC. Tick count frozen at 462. Tmux session 'aos-brain' not found. OODA loop not cycling. **RESTART REQUIRED** to restore brain function.
