#!/data/data/com.termux/files/usr/bin/bash
# start-myl1ssa-voice.sh — start Raven's (Myl1Ssa) audible pulse persistently.
# Idempotent. House style, same as start-brain.sh / start-palm.sh.

cd "$HOME/v1/projects/5912/Myl1Ssa/runtime" || exit 1
PIDFILE="$HOME/.myl1ssa_heartbeat.pid"
LOGFILE="$HOME/myl1ssa-heartbeat-voice.log"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    echo "🫀 Raven's pulse already running (pid $(cat "$PIDFILE"))"
    exit 0
fi

termux-wake-lock 2>/dev/null

setsid nohup python3 -u heartbeat_voice.py start > "$LOGFILE" 2>&1 < /dev/null &
sleep 1
echo "🫀 Raven's pulse started — $(python3 heartbeat_voice.py status | tr -d '\n ')"
