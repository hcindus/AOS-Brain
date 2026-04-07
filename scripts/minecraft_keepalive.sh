#!/bin/bash
# VERSION: 1.0.1
# UPDATED: 2026-04-07 04:13 UTC
# CHANGELOG: v1.0.1 - Version bump for indexing consistency
#            v1.0.0 - Initial MC agent health check
#
# Minecraft Agent Keepalive
# Ensures Mineflayer agents stay connected

AGENT_DIR="/root/.openclaw/workspace/scripts/minecraft_agents"
LOG_FILE="/root/.openclaw/workspace/logs/mc_agent_keepalive.log"

mkdir -p /root/.openclaw/workspace/logs

# Check if agents need restart (if count drops below expected)
AGENT_COUNT=$(pgrep -f "node.*mineflayer" 2>/dev/null | wc -l)
EXPECTED_AGENTS=7

if [ "$AGENT_COUNT" -lt "$EXPECTED_AGENTS" ]; then
    echo "[$(date)] Only $AGENT_COUNT agents running, expected $EXPECTED_AGENTS" >> "$LOG_FILE"
    
    # Re-run rotation to restore agents
    python3 /root/.openclaw/workspace/scripts/minecraft_agent_rotation.py >> "$LOG_FILE" 2>&1 &
else
    : # echo "[$(date)] Agent count OK: $AGENT_COUNT/$EXPECTED_AGENTS" >> "$LOG_FILE"
fi
