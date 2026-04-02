#!/bin/bash
# VERSION: 1.0.0
# UPDATED: 2026-04-02 04:08 UTC
# CHANGELOG: Initial brain health monitor
#
# AOS Brain Keepalive
# Monitors and maintains Complete Brain v4 service

BRAIN_PID=$(pgrep -f "complete_brain_v4.py")
LOG_FILE="/root/.openclaw/workspace/logs/aos_keepalive.log"

mkdir -p /root/.openclaw/workspace/logs

if [ -z "$BRAIN_PID" ]; then
    echo "[$(date)] Brain not running - checking for lock file..." >> "$LOG_FILE"
    
    if [ -f /tmp/aos_brain.lock ]; then
        echo "[$(date)] Removing stale lock file" >> "$LOG_FILE"
        rm -f /tmp/aos_brain.lock
    fi
    
    # Restart brain
    echo "[$(date)] Restarting Complete Brain v4..." >> "$LOG_FILE"
    /usr/bin/python3 /root/.aos/aos/complete_brain_v4.py >> "$LOG_FILE" 2>&1 &
else
    # Check if actually responsive (not hung)
    UPTIME_SEC=$(ps -o etimes= -p $BRAIN_PID 2>/dev/null || echo "0")
    
    # Log minimal status every hour only
    if [ $(($(date +%M) % 60)) -eq 0 ]; then
        echo "[$(date)] Brain OK - PID $BRAIN_PID, uptime ${UPTIME_SEC}s" >> "$LOG_FILE"
    fi
fi
