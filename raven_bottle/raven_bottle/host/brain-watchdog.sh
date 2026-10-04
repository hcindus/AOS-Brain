#!/data/data/com.termux/files/usr/bin/bash
# brain-watchdog.sh — keep the Mortimer Brain Runtime (:8765) alive.
# Idempotent. Called by termux-job-scheduler every 15 min, persisted.
#
# This exists because the brain DIED on 2026-09-25 at 19:34 and stayed dead for
# five days. It had a boot script but no watchdog, so a crash meant permanent
# silence until the next device reboot. A boot entry is not persistence.

LOG="$HOME/brain.log"
PIDFILE="$HOME/.brain_runtime.pid"

# Is it actually answering, not just "a pid exists"?
if curl -s -m 3 -o /dev/null "http://127.0.0.1:8765/health" 2>/dev/null; then
    exit 0
fi

# Dead or wedged — clear the stale pid and bring it back.
if [ -f "$PIDFILE" ] && ! kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    :
fi
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🧠 watchdog: brain not answering — restarting" >> "$LOG"
bash "$HOME/start-brain.sh" >> "$LOG" 2>&1
