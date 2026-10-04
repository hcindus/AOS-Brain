#!/data/data/com.termux/files/usr/bin/bash
# start-raven-voice.sh — start Raven's audible pulse persistently (idempotent).
# House style, same as start-brain.sh / start-palm.sh / start-raven.sh.

cd "$HOME/v1/projects/5912/R8s/runtime" || exit 1
PIDFILE="$HOME/.raven_heartbeat.pid"
LOGFILE="$HOME/raven-heartbeat-voice.log"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    echo "🫀 Raven's pulse already running (pid $(cat "$PIDFILE"))"
    exit 0
fi

# Keep the device awake so the pulse keeps going
termux-wake-lock 2>/dev/null

setsid nohup python3 -u heartbeat_voice.py start > "$LOGFILE" 2>&1 < /dev/null &
sleep 1
echo "🫀 Raven's pulse started — $(python3 heartbeat_voice.py status | tr -d '\n ')"
