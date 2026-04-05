#!/bin/bash
# AOS Brain Watchdog - Auto-restart on crash

LOG_FILE="/root/.aos/logs/watchdog.log"
BRAIN_CHECK_INTERVAL=30

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
}

log "Watchdog started"

while true; do
    if ! pgrep -f "brain.py" > /dev/null; then
        log "⚠️ Brain not running! Restarting..."
        tmux new-session -d -s aos-brain "cd /root/.openclaw/workspace/AOS/brain && python3 brain.py 2>&1 | tee ~/.aos/logs/brain.log"
        sleep 5
        if pgrep -f "brain.py" > /dev/null; then
            log "✅ Brain restarted"
        else
            log "❌ Restart failed"
        fi
    fi
    sleep $BRAIN_CHECK_INTERVAL
done
