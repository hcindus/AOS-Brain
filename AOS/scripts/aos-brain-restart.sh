#!/bin/bash
# AOS Brain Auto-Restart Script
# Created by: Stacktrace (Software Team)
# Purpose: Ensure brain.py always runs in tmux session 'aos-brain'

BRAIN_DIR="/root/.openclaw/workspace/AOS/brain"
TMUX_SESSION="aos-brain"
LOG_FILE="/root/.aos/logs/brain_restart.log"

# Create log directory if needed
mkdir -p /root/.aos/logs

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if brain is running in tmux
is_running() {
    tmux has-session -t "$TMUX_SESSION" 2>/dev/null && \
    pgrep -f "python3 brain.py" > /dev/null
}

# Start brain in tmux
start_brain() {
    log "Starting AOS Brain in tmux session..."
    
    # Kill existing session if stale
    tmux kill-session -t "$TMUX_SESSION" 2>/dev/null
    
    # Create new session and start brain
    tmux new-session -d -s "$TMUX_SESSION" -c "$BRAIN_DIR"
    tmux send-keys -t "$TMUX_SESSION" "python3 brain.py" Enter
    
    sleep 2
    
    if is_running; then
        log "✅ AOS Brain started successfully (PID: $(pgrep -f 'python3 brain.py' | head -1))"
        return 0
    else
        log "❌ Failed to start AOS Brain"
        return 1
    fi
}

# Main logic
if is_running; then
    log "AOS Brain is already running"
    exit 0
else
    log "AOS Brain not detected, restarting..."
    start_brain
fi
