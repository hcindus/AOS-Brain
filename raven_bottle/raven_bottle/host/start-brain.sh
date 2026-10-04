#!/data/data/com.termux/files/usr/bin/bash
# start-brain.sh — start the Mortimer Brain Runtime persistently (idempotent).

cd "$HOME"
PIDFILE="$HOME/.brain_runtime.pid"
LOGFILE="$HOME/brain_runtime.log"

# Already running?
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "Already running (PID $(cat "$PIDFILE"))"
    exit 0
fi

# Keep the device awake so the tick loop keeps running
termux-wake-lock 2>/dev/null

# Start detached (survives terminal close AND parent-shell exit)
setsid nohup python3 brain_runtime.py > "$LOGFILE" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
echo "Brain Runtime started (PID $(cat "$PIDFILE")) — API on http://127.0.0.1:8765"
