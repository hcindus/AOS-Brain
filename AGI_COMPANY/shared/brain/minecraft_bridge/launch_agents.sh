#!/bin/bash
#
# Launch Mineflayer Agent System
# Usage: ./launch_agents.sh [number_of_agents]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENT_COUNT=${1:-7}

echo "=========================================="
echo "  MINEFLAYER AGENT SYSTEM LAUNCHER"
echo "=========================================="
echo ""
echo "Spawning $AGENT_COUNT autonomous agents"
echo "with Brain OODA integration"
echo ""

# Check dependencies
echo "[1/4] Checking dependencies..."

if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found"
    echo "Install with: apt install nodejs npm"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found"
    exit 1
fi

if [ ! -d "$SCRIPT_DIR/node_modules/mineflayer" ]; then
    echo "Installing Mineflayer..."
    cd "$SCRIPT_DIR"
    npm install mineflayer mineflayer-pathfinder mineflayer-collectblock ws vec3
fi

echo "✓ Dependencies OK"
echo ""

# Check Minecraft server
echo "[2/4] Checking Minecraft server..."

if ! nc -z localhost 25566 2>/dev/null; then
    echo "WARNING: Minecraft server not detected on port 25566"
    echo "Agents may fail to connect until server is ready"
else
    echo "✓ Minecraft server detected"
fi
echo ""

# Start Brain WebSocket server
echo "[3/4] Starting Brain WebSocket server..."

cd "$SCRIPT_DIR"
python3 brain_websocket_server.py --port 8767 &
WS_PID=$!
echo $WS_PID > /tmp/brain_ws.pid

echo "✓ Brain WebSocket server started (PID $WS_PID)"
echo "  Agent endpoint: ws://localhost:8767"
echo "  Observer endpoint: ws://localhost:8768"
echo ""

# Wait for server to be ready
sleep 2

# Start agent supervisor
echo "[4/4] Starting agent supervisor..."
echo ""

python3 supervisor.py --count $AGENT_COUNT

# Cleanup on exit
echo ""
echo "Shutting down Brain WebSocket server..."
if [ -f /tmp/brain_ws.pid ]; then
    kill $(cat /tmp/brain_ws.pid) 2>/dev/null || true
    rm /tmp/brain_ws.pid
fi

echo "=========================================="
echo "  AGENT SYSTEM STOPPED"
echo "=========================================="