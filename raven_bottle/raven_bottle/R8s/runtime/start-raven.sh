#!/data/data/com.termux/files/usr/bin/bash
# start-raven.sh — start Raven's heartbeat daemon persistently (idempotent).
# House style, same as start-brain.sh / start-palm.sh.

cd "$HOME/v1/projects/5912/R8s/runtime" || exit 1
PIDFILE="$HOME/.raven-heartbeat.pid"
LOGFILE="$HOME/raven-heartbeat.log"

# Already running?
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    echo "🐦‍⬛ Raven's heartbeat already running (PID $(cat "$PIDFILE"))"
    exit 0
fi

# Keep the device awake so the tempo loop keeps running
termux-wake-lock 2>/dev/null

# Start detached (survives terminal close AND parent-shell exit)
setsid nohup python3 -u heartbeat.py daemon > "$LOGFILE" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
echo "🐦‍⬛ Raven's heartbeat started (PID $(cat "$PIDFILE")) — $(python3 heartbeat.py status | grep -E 'tempo|times' | tr -d ' ,\n')"
