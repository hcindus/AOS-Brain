#!/bin/bash
# AOS Brain Health Monitor
# Run this via cron every 5 minutes to ensure brain stays running

BRAIN_DIR="/root/.openclaw/workspace/AOS/brain"
TMUX_SESSION="aos-brain"
RESTART_SCRIPT="/root/.openclaw/workspace/AOS/scripts/aos-brain-restart.sh"

# Check if brain process exists
if ! pgrep -f "python3 brain.py" > /dev/null; then
    echo "[$(date)] Brain process not found, restarting..."
    bash "$RESTART_SCRIPT"
    exit $?
fi

# Check if tmux session exists
if ! tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "[$(date)] Tmux session missing, restarting..."
    bash "$RESTART_SCRIPT"
    exit $?
fi

# Check Ollama connectivity
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "[$(date)] Warning: Ollama not responding"
    # Don't restart brain for Ollama issues, just log
fi

echo "[$(date)] Brain health check: OK"
exit 0
