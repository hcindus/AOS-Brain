#!/data/data/com.termux/files/usr/bin/bash
# start-myl1ssa-pulse.sh — run the pulse as a live daemon instead of cron.
cd "$HOME/v1/projects/5912/Myl1Ssa/runtime" || exit 1
PIDFILE="$HOME/.myl1ssa_pulse.pid"
LOGFILE="$HOME/myl1ssa-pulse.log"
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    echo "🐦‍⬛ pulse daemon already running (pid $(cat "$PIDFILE"))"; exit 0
fi
termux-wake-lock 2>/dev/null
setsid nohup python3 -u heartbeat.py daemon >> "$LOGFILE" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
echo "🐦‍⬛ pulse daemon started (pid $(cat "$PIDFILE"))"
