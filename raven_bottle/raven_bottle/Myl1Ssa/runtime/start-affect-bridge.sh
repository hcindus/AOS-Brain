#!/data/data/com.termux/files/usr/bin/bash
# start-affect-bridge.sh — keep her affect tied to her real brain state.
# Idempotent. House style, same as start-myl1ssa-voice.sh.

cd "$HOME/v1/projects/5912/Myl1Ssa/runtime" || exit 1
PIDFILE="$HOME/.myl1ssa_affect_bridge.pid"
LOGFILE="$HOME/myl1ssa-affect-bridge.log"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    echo "🫀 affect bridge already running (pid $(cat "$PIDFILE"))"
    exit 0
fi

termux-wake-lock 2>/dev/null
setsid nohup python3 -u affect_bridge.py daemon >> "$LOGFILE" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
sleep 1
echo "🫀 affect bridge started (pid $(cat "$PIDFILE" 2>/dev/null || echo '?'))"
