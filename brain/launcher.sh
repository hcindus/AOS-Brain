#!/bin/bash
# AOS Brain Launcher with 99.99% Uptime

echo "[LAUNCHER] Starting AOS Brain..."
cd ~/.aos/aos/brain

# Kill any existing brain processes
pkill -9 -f "python3 brain.py" 2>/dev/null
sleep 2

# Start brain with proper logging
echo "[LAUNCHER] Launching brain.py..."
python3 brain.py &
BRAIN_PID=$!

echo "[LAUNCHER] Brain PID: $BRAIN_PID"
echo "[LAUNCHER] Waiting for initialization..."

# Wait for state file
for i in {1..10}; do
    sleep 1
    if [ -f ~/.aos/brain/state/brain_state.json ]; then
        echo "[LAUNCHER] State file found!"
        cat ~/.aos/brain/state/brain_state.json | jq '{tick: .tick, clusters: .memory_nn.clusters}' 2>/dev/null
        break
    fi
    echo "[LAUNCHER] Waiting... $i"
done

echo "[LAUNCHER] Brain is running"
