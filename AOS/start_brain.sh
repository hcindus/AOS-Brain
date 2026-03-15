#!/usr/bin/env bash

echo "Starting AOS Brain in continuous background mode..."

# Ensure logs directory exists
mkdir -p ~/.aos/logs

# 1. Start Ollama backend if not already running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama server in tmux session 'ollama'..."
    tmux new-session -d -s ollama 'ollama serve'
    sleep 5
else
    echo "Ollama is already running."
fi

# 2. Start the AOS Brain OODA Loop
if tmux has-session -t aos-brain 2>/dev/null; then
    echo "AOS Brain is already running in tmux session 'aos-brain'. Restarting it..."
    tmux kill-session -t aos-brain
fi

echo "Activating all brain regions and initiating OODA loop..."
tmux new-session -d -s aos-brain 'python3 /root/.openclaw/workspace/AOS/brain/brain.py 2>&1 | tee ~/.aos/logs/brain.log'

# 3. Start the Visualizer (Optional, outputs to a separate log if running headless)
if tmux has-session -t aos-visualizer 2>/dev/null; then
    tmux kill-session -t aos-visualizer
fi
tmux new-session -d -s aos-visualizer 'python3 /root/.openclaw/workspace/AOS/visualizer/brain_visualizer.py 2>&1 | tee ~/.aos/logs/visualizer.log'

echo "===================================================="
echo "🧠 AOS Brain is now LIVE and running continuously!"
echo "💰 Cost: $0/month (100% Local Inference)"
echo "===================================================="
echo "To view the live brain logs, run: tail -f ~/.aos/logs/brain.log"
echo "To attach to the brain session, run: tmux attach -t aos-brain"
echo "To detach from tmux, press: Ctrl+B, then D"
