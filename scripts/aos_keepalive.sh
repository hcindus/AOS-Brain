#!/bin/bash
# VERSION: 2.0.0
# UPDATED: 2026-04-22 07:20 UTC
# CHANGELOG: v2.0 - Simplified: systemd manages restarts, this only monitors
#
# AOS Brain Health Monitor v2.0
# Reports brain status - systemd handles actual process management

LOG_FILE="/var/log/aos/brain_keepalive.log"
mkdir -p /var/log/aos

log() {
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] $1" | tee -a "$LOG_FILE"
}

log "=== AOS Brain Health Monitor ==="

# 1. Check Complete Brain v4.5 - MONITOR ONLY (systemd managed)
BRAIN_PID=$(pgrep -o -f "complete_brain_v45\.py")
if [ -n "$BRAIN_PID" ]; then
    BRAIN_UPTIME=$(ps -p "$BRAIN_PID" -o etime= 2>/dev/null | xargs)
    log "✅ Complete Brain v4.5: RUNNING (PID $BRAIN_PID, uptime: $BRAIN_UPTIME)"
    
    # Socket health check (informational only)
    if [ -S "/tmp/aos_brain.sock" ]; then
        SOCKET_RESP=$(echo '{"cmd":"ping"}' | timeout 2 nc -U /tmp/aos_brain.sock 2>/dev/null)
        if [ -n "$SOCKET_RESP" ]; then
            log "✅ Brain socket: RESPONSIVE"
        else
            log "⚠️ Brain socket: UNRESPONSIVE (service may need restart via systemd)"
        fi
    else
        log "⚠️ Brain socket: NOT FOUND"
    fi
else
    log "❌ Complete Brain v4.5: NOT RUNNING"
    log "   systemd will auto-restart: systemctl restart aos-brain-v4"
fi

# 2. BHSI - MONITOR ONLY (systemd managed)
BHSI_PID=$(pgrep -o -f "bhsi_v4_brain_connector")
if [ -n "$BHSI_PID" ]; then
    BHSI_UPTIME=$(ps -p "$BHSI_PID" -o etime= 2>/dev/null | xargs)
    log "✅ BHSI v4: RUNNING (PID $BHSI_PID, uptime: $BHSI_UPTIME)"
else
    log "⚠️ BHSI v4: NOT RUNNING - systemd will auto-restart"
fi

log "=== Monitor Complete ==="
