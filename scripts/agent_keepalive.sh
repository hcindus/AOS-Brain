#!/bin/bash
# VERSION: 1.0.0
# UPDATED: 2026-04-02 04:08 UTC
# CHANGELOG: Initial unified keepalive system
#
# Agent Keepalive Monitor
# Ensures all critical agent systems remain running

LOG_FILE="/root/.openclaw/workspace/logs/agent_keepalive.log"
mkdir -p $(dirname $LOG_FILE)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] $1" | tee -a "$LOG_FILE"
}

log "=== Agent Keepalive Check ==="

# 1. Ollama Mortimer Model
curl -s --max-time 8 http://localhost:11434/api/generate \
  -d '{"model":"antoniohudnall/Mortimer:latest","prompt":"p","stream":false}' \
  > /dev/null 2>&1
if [ $? -eq 0 ]; then
    log "✅ Mortimer: RESPONSIVE"
else
    log "⚠️ Mortimer: UNRESPONSIVE - Model may have unloaded"
fi

# 2. Complete Brain v4 (AOD daemon) - check for duplicates
BRAIN_PIDS=$(pgrep -f "complete_brain_v45\.py")
BRAIN_COUNT=$(echo "$BRAIN_PIDS" | grep -c '^' 2>/dev/null || echo "0")

if [ "$BRAIN_COUNT" -eq 0 ]; then
    log "❌ Complete Brain v4.5: NOT RUNNING - attempting restart..."
    systemctl restart aos-brain-v4 2>/dev/null || log "Failed to restart brain"
elif [ "$BRAIN_COUNT" -eq 1 ]; then
    PID=$(echo "$BRAIN_PIDS" | head -1)
    UPTIME=$(ps -o etime= -p $PID 2>/dev/null || echo "unknown")
    log "✅ Complete Brain v4.5: RUNNING (PID $PID, uptime: $UPTIME)"
else
    log "⚠️ Complete Brain v4.5: $BRAIN_COUNT DUPLICATES DETECTED"
    OLDEST=$(echo "$BRAIN_PIDS" | sort -n | head -1)
    for pid in $BRAIN_PIDS; do
        [ "$pid" != "$OLDEST" ] && kill "$pid" 2>/dev/null
    done
    UPTIME=$(ps -o etime= -p $OLDEST 2>/dev/null || echo "unknown")
    log "✅ Complete Brain v4.5: CLEANED (PID $OLDEST, uptime: $UPTIME)"
fi

# 2b. BHSI (Stomach + Intestines) - check health
if pgrep -f "bhsi_v4_brain_connector" > /dev/null; then
    BHSI_PID=$(pgrep -f "bhsi_v4_brain_connector" | head -1)
    log "✅ BHSI v4 (Stomach/Intestines): RUNNING (PID $BHSI_PID)"
else
    log "❌ BHSI v4: NOT RUNNING - attempting restart..."
    systemctl restart aos-bhsi-v4 2>/dev/null || log "Failed to restart BHSI"
fi

# 3. Mission Control Server
if pgrep -f "mission_control/server_v2.py" > /dev/null; then
    PID=$(pgrep -f "mission_control/server_v2.py")
    log "✅ Mission Control: RUNNING (PID $PID)"
else
    log "❌ Mission Control: NOT RUNNING - attempting restart..."
    /usr/bin/python3 /root/.openclaw/workspace/aocros/mission_control/server_v2.py &
fi

# 4. Roblox Bridge
if pgrep -f "roblox-bridge.py" > /dev/null; then
    PID=$(pgrep -f "roblox-bridge.py")
    log "✅ Roblox Bridge: RUNNING (PID $PID)"
else
    log "❌ Roblox Bridge: NOT RUNNING - check systemd service"
fi

# 5. Minecraft Server Health
check_minecraft_health() {
    # Check if Minecraft Java process is running (including paper jar)
    if pgrep -f "paper.*jar" > /dev/null || pgrep -f "minecraft_server" > /dev/null || pgrep -f "java.*-jar.*minecraft" > /dev/null || pgrep -f "java.*paper" > /dev/null; then
        MEM_USAGE=$(ps aux | grep -E "(paper.*jar|minecraft_server|java.*-jar)" | grep -v grep | awk '{sum+=$4} END {printf "%.1f", sum}')
        log "✅ Minecraft Server: RUNNING (Memory: ${MEM_USAGE}% - safe if <50%)"
        
        # Check Mineflayer agents
        AGENT_COUNT=$(pgrep -f "mineflayer" | wc -l)
        log "✅ Mineflayer Agents: $AGENT_COUNT active"
    else
        log "⚠️ Minecraft Server: Process not found"
    fi
}
check_minecraft_health

# 6. Memory Health
MEM_PERCENT=$(free | awk '/Mem/{printf "%.0f", $3/$2*100}')
if [ "$MEM_PERCENT" -gt 90 ]; then
    log "⚠️ SYSTEM MEMORY: ${MEM_PERCENT}% - CRITICAL"
elif [ "$MEM_PERCENT" -gt 75 ]; then
    log "⚠️ SYSTEM MEMORY: ${MEM_PERCENT}% - WARNING"
else
    log "✅ System Memory: ${MEM_PERCENT}% (healthy)"
fi

# 7. Disk Space
DISK_PERCENT=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_PERCENT" -gt 90 ]; then
    log "⚠️ DISK SPACE: ${DISK_PERCENT}% - CRITICAL"
elif [ "$DISK_PERCENT" -gt 80 ]; then
    log "⚠️ DISK SPACE: ${DISK_PERCENT}% - WARNING"
else
    log "✅ Disk Space: ${DISK_PERCENT}% (healthy)"
fi

# 8. Society Simulation Agents
if pgrep -f "society_agent.js" > /dev/null; then
    SOCIETY_COUNT=$(pgrep -f "society_agent.js" | wc -l)
    log "✅ Society Agents: $SOCIETY_COUNT/5 running (3 male, 2 female)"
    
    # Check society server
    if pgrep -f "society_server.py" > /dev/null; then
        log "✅ Society Server: RUNNING (port 8768)"
    else
        log "⚠️ Society Server: NOT RUNNING - attempting restart..."
        /usr/bin/python3 /root/.openclaw/workspace/scripts/minecraft_agents/society_server.py &
    fi
else
    log "⚠️ Society Agents: None running"
fi

log "=== Keepalive Check Complete ==="
