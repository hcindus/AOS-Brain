#!/bin/bash
# get_brain_status.sh - Neural Network Status Reporter
# Called by cron/heartbeat to get GrowingNN metrics

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     AOS Brain - Neural Network Status Report             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if brain is running
if pgrep -f "brain.py" > /dev/null; then
    echo "🧠 Brain Process: RUNNING"
    ps aux | grep "brain.py" | grep -v grep | head -1 | awk '{print "   PID: " $2 " | CPU: " $3 "% | MEM: " $4 "%"}'
else
    echo "❌ Brain Process: NOT RUNNING"
fi

echo ""

# Read brain state if available
if [ -f ~/.aos/brain/state/brain_state.json ]; then
    echo "📊 GrowingNN Metrics:"
    echo ""
    
    # Parse JSON using Python
    python3 << 'PYTHON_EOF'
import json
import sys

try:
    with open('/root/.aos/brain/state/brain_state.json', 'r') as f:
        d = json.load(f)
    
    # Policy NN
    policy = d.get('policy_nn', {})
    print(f"   Neural Network:")
    print(f"     Layers: {policy.get('layers', 'N/A')}")
    print(f"     Nodes: {policy.get('nodes', 'N/A')}")
    print(f"     Total Nodes: {policy.get('total_nodes', 'N/A')}")
    print(f"     Growth Events: {policy.get('growth_events', 'N/A')}")
    print()
    
    # Memory
    memory = d.get('memory_nn', {})
    print(f"   Memory System:")
    print(f"     Clusters: {memory.get('clusters', 'N/A')}")
    print(f"     Novelty Current: {memory.get('novelty_current', 'N/A')}")
    print(f"     Novelty Avg: {memory.get('novelty_avg', 'N/A')}")
    print()
    
    # GrowingNN
    growing = d.get('growingnn', {})
    print(f"   GrowingNN Status:")
    print(f"     Error Rate: {growing.get('error_rate', 'N/A')}")
    print(f"     Complexity: {growing.get('complexity', 'N/A')}")
    print(f"     Novelty: {growing.get('novelty', 'N/A')}")
    print(f"     Growth Triggered: {growing.get('growth_triggered', 'N/A')}")
    print()
    
    # General
    print(f"   General:")
    print(f"     Tick: {d.get('tick', 'N/A')}")
    print(f"     Phase: {d.get('phase', 'N/A')}")
    
except Exception as e:
    print(f"   Error reading state: {e}")
PYTHON_EOF

else
    echo "⚠️  brain_state.json not found"
fi

echo ""

# Check Ollama
if pgrep -f "ollama" > /dev/null; then
    echo "🤖 Ollama: RUNNING"
    ollama list 2>/dev/null | head -5 | sed 's/^/   /'
else
    echo "⚠️  Ollama: Not running (optional for AOS-Lite)"
fi

echo ""

# Check tmux sessions
echo "🖥️  Tmux Sessions:"
tmux list-sessions 2>/dev/null | sed 's/^/   /' || echo "   No active sessions"

echo ""
echo "═══════════════════════════════════════════════════════════"
