#!/bin/bash
# VERSION: 1.1.0
# UPDATED: 2026-04-22 06:31 UTC
# CHANGELOG: Fixed duplicate process detection, added BHSI checking
#
# AOS Brain Keepalive Script
# Checks Complete Brain v4 + BHSI health, handles duplicates, restarts if needed

LOG_FILE="/var/log/aos/brain_keepalive.log"
mkdir -p /var/log/aos

log() {
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] $1" | tee -a "$LOG_FILE"
}

log "=== AOS Brain Keepalive Check ==="

# 1. Check Complete Brain v4.5 - count processes, kill duplicates
BRAIN_PIDS=$(pgrep -f "complete_brain_v45\.py")
BRAIN_COUNT=$(echo "$BRAIN_PIDS" | grep -c '^' 2>/dev/null || echo "0")

if [ "$BRAIN_COUNT" -eq 0 ]; then
    log "❌ Complete Brain v4.5: NOT RUNNING"
    log "🔄 Attempting restart via systemd..."
    systemctl restart aos-brain-v4 2>/dev/null || log "Failed to restart brain"
elif [ "$BRAIN_COUNT" -eq 1 ]; then
    BRAIN_UPTIME=$(ps -p "$BRAIN_PIDS" -o etime= 2>/dev/null | xargs)
    log "✅ Complete Brain v4.5: RUNNING (PID $BRAIN_PIDS, uptime: $BRAIN_UPTIME)"
else
    log "⚠️ Complete Brain v4.5: $BRAIN_COUNT PROCESSES DETECTED (duplicates!)"
    # Kill all but the oldest (lowest PID)
    OLDEST_PID=$(echo "$BRAIN_PIDS" | sort -n | head -1)
    log "🔄 Keeping PID $OLDEST_PID, killing duplicates..."
    for pid in $BRAIN_PIDS; do
        if [ "$pid" != "$OLDEST_PID" ]; then
            kill "$pid" 2>/dev/null && log "   Killed duplicate PID $pid" || log "   Failed to kill PID $pid"
        fi
    done
    BRAIN_UPTIME=$(ps -p "$OLDEST_PID" -o etime= 2>/dev/null | xargs)
    log "✅ Complete Brain v4.5: CLEANED (PID $OLDEST_PID, uptime: $BRAIN_UPTIME)"
fi

# 2. Check BHSI (Stomach + Intestines) - often dies silently
BHSI_PIDS=$(pgrep -f "bhsi_v4_brain_connector")
BHSI_COUNT=$(echo "$BHSI_PIDS" | grep -c '^' 2>/dev/null || echo "0")

if [ "$BHSI_COUNT" -eq 0 ]; then
    log "❌ BHSI v4 (Stomach/Intestines): NOT RUNNING"
    log "🔄 Attempting restart via systemd..."
    systemctl restart aos-bhsi-v4 2>/dev/null || log "Failed to restart BHSI"
elif [ "$BHSI_COUNT" -eq 1 ]; then
    BHSI_UPTIME=$(ps -p "$BHSI_PIDS" -o etime= 2>/dev/null | xargs)
    log "✅ BHSI v4: RUNNING (PID $BHSI_PIDS, uptime: $BHSI_UPTIME)"
else
    log "⚠️ BHSI v4: $BHSI_COUNT PROCESSES DETECTED"
    OLDEST_BHSI=$(echo "$BHSI_PIDS" | sort -n | head -1)
    for pid in $BHSI_PIDS; do
        [ "$pid" != "$OLDEST_BHSI" ] && kill "$pid" 2>/dev/null
    done
    BHSI_UPTIME=$(ps -p "$OLDEST_BHSI" -o etime= 2>/dev/null | xargs)
    log "✅ BHSI v4: CLEANED (PID $OLDEST_BHSI, uptime: $BHSI_UPTIME)"
fi

# 3. Verify socket responsiveness (optional health check)
if [ -S "/tmp/aos_brain.sock" ]; then
    SOCKET_RESP=$(echo '{"cmd":"ping"}' | timeout 2 nc -U /tmp/aos_brain.sock 2>/dev/null)
    if [ -n "$SOCKET_RESP" ]; then
        log "✅ Brain socket: RESPONSIVE"
    else
        log "⚠️ Brain socket: NO RESPONSE (process may be stuck)"
    fi
else
    log "⚠️ Brain socket: NOT FOUND"
fi

log "=== Keepalive Check Complete ==="
