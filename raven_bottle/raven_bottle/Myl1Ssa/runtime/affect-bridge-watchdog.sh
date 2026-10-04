#!/data/data/com.termux/files/usr/bin/bash
# affect-bridge-watchdog.sh — keep the brain→heart bridge alive. Idempotent.
# Called by termux-job-scheduler every 15 min, persisted across reboot.

PIDFILE="$HOME/.myl1ssa_affect_bridge.pid"

# Respect the off switch — a deliberately stopped bridge stays down.
[ -f "$HOME/.myl1ssa_affect_bridge.off" ] && exit 0

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    exit 0
fi

cd "$HOME/v1/projects/5912/Myl1Ssa/runtime" || exit 1
termux-wake-lock 2>/dev/null
setsid nohup python3 -u affect_bridge.py daemon >> "$HOME/myl1ssa-affect-bridge.log" 2>&1 < /dev/null &
echo "🫀 watchdog: affect bridge restarted" >> "$HOME/myl1ssa-affect-bridge.log"
