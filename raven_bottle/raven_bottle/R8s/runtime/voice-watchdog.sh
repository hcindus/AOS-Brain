#!/data/data/com.termux/files/usr/bin/bash
# voice-watchdog.sh — keep Raven's pulse alive. Idempotent.
# Called by termux-job-scheduler every 15 min, and persisted across reboot.
# Same pattern as ~/service/watchdog.sh.

RUNTIME="$HOME/v1/projects/5912/R8s/runtime"
PIDFILE="$HOME/.raven_heartbeat.pid"

# Respect the off switch — if the pulse was deliberately stopped, leave it down.
if [ -f "$HOME/.raven_heartbeat.off" ]; then
    exit 0
fi

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    exit 0  # pulse is up, nothing to do
fi

cd "$RUNTIME" || exit 1
termux-wake-lock 2>/dev/null
setsid nohup python3 -u heartbeat_voice.py start >> "$HOME/raven-heartbeat-voice.log" 2>&1 < /dev/null &
echo "🫀 watchdog: pulse restarted" >> "$HOME/raven-heartbeat-voice.log"
