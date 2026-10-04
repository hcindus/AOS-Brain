#!/data/data/com.termux/files/usr/bin/bash
# myl1ssa-pulse-watchdog.sh — keep her pulse alive. Idempotent.
PIDFILE="$HOME/.myl1ssa_pulse.pid"
OFF="$HOME/.myl1ssa_pulse.off"
[ -f "$OFF" ] && exit 0
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    exit 0
fi
cd "$HOME/v1/projects/5912/Myl1Ssa/runtime" || exit 1
termux-wake-lock 2>/dev/null
setsid nohup python3 -u heartbeat.py daemon >> "$HOME/myl1ssa-pulse.log" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
echo "🐦‍⬛ watchdog: pulse daemon restarted" >> "$HOME/myl1ssa-pulse.log"
