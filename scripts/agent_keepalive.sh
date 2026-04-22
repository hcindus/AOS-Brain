#!/bin/bash
# VERSION: 2.0.0
# UPDATED: 2026-04-22 07:20 UTC
# CHANGELOG: v2.0 - Removed brain duplicate handling (systemd manages), added --no-restart flag for systemd use
#
# Agent Keepalive Monitor v2.0
# Ensures all critical agent systems remain running
# NOTE: Brain/BHSI health is handled by systemd and aos_keepalive.sh - NOT this script

LOG_FILE="/root/.openclaw/workspace/logs/agent_keepalive.log"
mkdir -p $(dirname $LOG_FILE)

# Check if --no-restart flag passed (for systemd integration)
NO_RESTART=false
[[ "$1" == "--no-restart" ]] && NO_RESTART=true

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] $1" | tee -a "$LOG_FILE"
}

log "=== Agent Keepalive Check v2.0 ==="

# 1. Ollama Mortimer Model (external dependency)
curl -s --max-time 8 http://localhost:11434/api/generate \
  -d '{"model":"antoniohudnall/Mortimer:latest","prompt":"p","stream":false}' \
  > /dev/null 2>&1
if [ $? -eq 0 ]; then
    log "✅ Mortimer: RESPONSIVE"
else
    log "⚠️ Mortimer: UNRESPONSIVE - Model may have unloaded"
fi

# 2. Complete Brain v4.5 - MONITOR ONLY, systemd manages restarts
BRAIN_PID=$(pgrep -o -f "complete_brain_v45\.py")
if [ -n "$BRAIN_PID" ]; then
    UPTIME=$(ps -o etime= -p $BRAIN_PID 2>/dev/null | xargs || echo "unknown")
    log "✅ Complete Brain v4.5: MONITORED (PID $BRAIN_PID, uptime: $UPTIME)"
else
    log "⚠️ Complete Brain v4.5: NOT RUNNING - systemd should auto-restart"
    # Only attempt restart if not in systemd mode
    if [ "$NO_RESTART" = false ]; then
        log "   Attempting systemd restart..."
        systemctl restart aos-brain-v4 2>/dev/null || log "   Failed to restart via systemd"
    fi
fi

# 3. BHSI v4 - MONITOR ONLY (systemd managed)
BHSI_PID=$(pgrep -o -f "bhsi_v4_brain_connector")
if [ -n "$BHSI_PID" ]; then
    UPTIME=$(ps -o etime= -p $BHSI_PID 2>/dev/null | xargs || echo "unknown")
    log "✅ BHSI v4: MONITORED (PID $BHSI_PID, uptime: $UPTIME)"
else
    log "⚠️ BHSI v4: NOT RUNNING - systemd should auto-restart"
fi

# 4. Mission Control Server (standalone process)
if pgrep -f "mission_control/server_v2.py" > /dev/null; then
    PID=$(pgrep -f "mission_control/server_v2.py")
    log "✅ Mission Control: RUNNING (PID $PID)"
else
    log "❌ Mission Control: NOT RUNNING - attempting restart..."
    if [ "$NO_RESTART" = false ]; then
        /usr/bin/python3 /root/.openclaw/workspace/aocros/mission_control/server_v2.py &
    fi
fi

# 5. Roblox Bridge (standalone)
if pgrep -f "roblox-bridge.py" > /dev/null; then
    PID=$(pgrep -f "roblox-bridge.py")
    log "✅ Roblox Bridge: RUNNING (PID $PID)"
else
    log "⚠️ Roblox Bridge: NOT RUNNING - check systemd service"
fi

# 6. Minecraft Server Health
if pgrep -f "paper.*jar" > /dev/null || pgrep -f "minecraft_server" > /dev/null || pgrep -f "java.*paper" > /dev/null; then
    MEM_USAGE=$(ps aux | grep -E "(paper|minecraft_server|java.*-jar)" | grep -v grep | awk '{sum+=$4} END {printf "%.1f", sum}')
    log "✅ Minecraft Server: RUNNING (Memory: ${MEM_USAGE}% - safe if <50%)"
    AGENT_COUNT=$(pgrep -f "mineflayer" | wc -l)
    log "✅ Mineflayer Agents: $AGENT_COUNT active"
else
    log "⚠️ Minecraft Server: Process not found"
fi

# 7. System Health
MEM_PERCENT=$(free | awk '/Mem/{printf "%.0f", $3/$2*100}')
if [ "$MEM_PERCENT" -gt 90 ]; then
    log "⚠️ SYSTEM MEMORY: ${MEM_PERCENT}% - CRITICAL"
elif [ "$MEM_PERCENT" -gt 75 ]; then
    log "⚠️ SYSTEM MEMORY: ${MEM_PERCENT}% - WARNING"
else
    log "✅ System Memory: ${MEM_PERCENT}% (healthy)"
fi

DISK_PERCENT=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_PERCENT" -gt 90 ]; then
    log "⚠️ DISK SPACE: ${DISK_PERCENT}% - CRITICAL"
elif [ "$DISK_PERCENT" -gt 80 ]; then
    log "⚠️ DISK SPACE: ${DISK_PERCENT}% - WARNING"
else
    log "✅ Disk Space: ${DISK_PERCENT}% (healthy)"
fi

# 8. Society Simulation Agents (simple_society_agent.js)
SOCIETY_COUNT=$(pgrep -f "simple_society_agent.js" 2>/dev/null | wc -l)
if [ "$SOCIETY_COUNT" -ge 5 ]; then
    log "✅ Society Agents: $SOCIETY_COUNT/5 running"
elif [ "$SOCIETY_COUNT" -gt 0 ]; then
    log "⚠️ Society Agents: $SOCIETY_COUNT/5 running - some agents down"
else
    log "⚠️ Society Agents: None running - society-agents.service should auto-restart"
fi

# 9. AGI Company Agent Services (systemd managed)
for svc in patricia-factory forge-factory chelios-security jordan-office aurora-tasks; do
    if systemctl is-active "$svc" > /dev/null 2>&1; then
        log "✅ Agent Service: $svc ACTIVE"
    else
        log "⚠️ Agent Service: $svc INACTIVE"
    fi
done

log "=== Keepalive Check Complete ==="
