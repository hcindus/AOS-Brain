#!/bin/bash
# MYL Agent Launcher - Spawns 7 MYL agents in Minecraft
# VERSION: 1.0.0
# UPDATED: 2026-04-06

AGENT_SCRIPT="/root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge/mineflayer_agent.js"
LOG_DIR="/root/.openclaw/workspace/logs/myl_agents"
MC_HOST="localhost"
MC_PORT="25565"
BRAIN_WS="ws://localhost:8767"

mkdir -p "$LOG_DIR"

# MYL Agent names
MYL_AGENTS=("mylzeron" "mylonen" "myltwon" "mylthreen" "mylforon" "mylfivon" "mylsixon")

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S UTC')] $1"
}

log "=== MYL Agent Launcher ==="

# Check if Minecraft server is running
if ! pgrep -f "paper.*jar" > /dev/null; then
    log "⚠️ Minecraft server not running. Cannot spawn agents."
    exit 1
fi

log "✅ Minecraft server detected"

# Check Node.js and mineflayer
if ! command -v node &> /dev/null; then
    log "❌ Node.js not found"
    exit 1
fi

log "✅ Node.js available: $(node --version)"

# Stop any existing mineflayer processes
EXISTING=$(pgrep -f "mineflayer_agent.js" | wc -l)
if [ "$EXISTING" -gt 0 ]; then
    log "Stopping $EXISTING existing agent processes..."
    pkill -f "mineflayer_agent.js" 2>/dev/null || true
    sleep 3
fi

# Spawn each agent with staggered delay
log "Spawning ${#MYL_AGENTS[@]} MYL agents..."
for i in "${!MYL_AGENTS[@]}"; do
    AGENT="${MYL_AGENTS[$i]}"
    LOG_FILE="$LOG_DIR/${AGENT}.log"
    
    # Check if agent already running
    if pgrep -f "mineflayer_agent.*$AGENT" > /dev/null; then
        log "⚪ $AGENT already running, skipping"
        continue
    fi
    
    log "🚀 Spawning $AGENT..."
    
    # Start agent with proper arguments
    nohup node "$AGENT_SCRIPT" "$AGENT" "$MC_HOST" "$MC_PORT" "$BRAIN_WS" > "$LOG_FILE" 2>&1 &
    
    # Stagger spawns to avoid overwhelming server
    sleep 2
done

sleep 3

# Verify all agents
RUNNING=$(pgrep -f "mineflayer_agent.js" | wc -l)
log "✅ Spawned $RUNNING/${#MYL_AGENTS[@]} MYL agents"

# List active agents
log "Active agents:"
for AGENT in "${MYL_AGENTS[@]}"; do
    if pgrep -f "mineflayer_agent.*$AGENT" > /dev/null; then
        PID=$(pgrep -f "mineflayer_agent.*$AGENT" | head -1)
        log "  🟢 $AGENT (PID: $PID)"
    else
        log "  🔴 $AGENT - NOT RUNNING"
    fi
done

log "=== Launch Complete ==="
