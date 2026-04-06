#!/bin/bash
# Spawn individual MYL agent with retry logic
AGENT=$1
AGENT_SCRIPT="/root/.openclaw/workspace/AGI_COMPANY/shared/brain/minecraft_bridge/mineflayer_agent.js"
LOG_DIR="/root/.openclaw/workspace/logs/myl_agents"
mkdir -p "$LOG_DIR"

if [ -z "$AGENT" ]; then
    echo "Usage: $0 <agent_name>"
    exit 1
fi

# Check if already running
if pgrep -f "mineflayer_agent.*$AGENT" > /dev/null; then
    echo "🟢 $AGENT already running"
    exit 0
fi

echo "🚀 Spawning $AGENT..."
nohup node "$AGENT_SCRIPT" "$AGENT" "localhost" "25565" "ws://localhost:8767" > "$LOG_DIR/${AGENT}.log" 2>&1 &
sleep 4

# Check if successful
if pgrep -f "mineflayer_agent.*$AGENT" > /dev/null; then
    echo "✅ $AGENT spawned successfully"
else
    echo "❌ $AGENT failed to spawn"
    tail -5 "$LOG_DIR/${AGENT}.log"
fi
