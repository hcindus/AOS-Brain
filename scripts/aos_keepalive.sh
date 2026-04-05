#!/bin/bash
# AOS Brain Keepalive Script
# Checks Complete Brain v4 health and restarts if needed

LOG_FILE="/var/log/aos/brain_keepalive.log"
mkdir -p /var/log/aos

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] === AOS Brain Keepalive Check ===" | tee -a "$LOG_FILE"

# Check if brain process is running
BRAIN_PID=$(pgrep -f "complete_brain_v4" | head -1)
if [ -n "$BRAIN_PID" ]; then
    BRAIN_UPTIME=$(ps -p $BRAIN_PID -o etime= 2>/dev/null | xargs)
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ✅ Complete Brain v4: RUNNING (PID $BRAIN_PID, uptime: $BRAIN_UPTIME)" | tee -a "$LOG_FILE"
else
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ❌ Complete Brain v4: NOT RUNNING" | tee -a "$LOG_FILE"
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] 🔄 Attempting restart via systemd..." | tee -a "$LOG_FILE"
    systemctl restart aos-brain-v4 2>/dev/null || echo "Failed to restart" | tee -a "$LOG_FILE"
fi

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] === Keepalive Check Complete ===" | tee -a "$LOG_FILE"
