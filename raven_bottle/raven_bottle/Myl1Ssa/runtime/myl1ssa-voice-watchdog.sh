#!/data/data/com.termux/files/usr/bin/bash
# myl1ssa-voice-watchdog.sh — keep Raven's (Myl1Ssa) AUDIBLE pulse alive.
# Idempotent. Called by termux-job-scheduler every 15 min, persisted across reboot.
#
# Distinction that caused the 2026-09-30 silence:
#   heartbeat.py daemon       = tick/logic engine   (watchdog: 5915)
#   heartbeat_voice.py start  = audible lub-dub     (watchdog: THIS, job 5916)
# The pulse daemon came back after reboot; the audio never did. This closes that gap.
# Same pattern as R8s/runtime/voice-watchdog.sh and ~/service/watchdog.sh.

RUNTIME="$HOME/v1/projects/5912/Myl1Ssa/runtime"
PIDFILE="$HOME/.myl1ssa_heartbeat.pid"

# Respect the off switch — if the pulse was deliberately stopped, leave it down.
if [ -f "$HOME/.myl1ssa_heartbeat.off" ]; then
    exit 0
fi

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
    exit 0  # pulse is up, nothing to do
fi

cd "$RUNTIME" || exit 1
termux-wake-lock 2>/dev/null
setsid nohup python3 -u heartbeat_voice.py start >> "$HOME/myl1ssa-heartbeat-voice.log" 2>&1 < /dev/null &
echo "🫀 watchdog: pulse restarted" >> "$HOME/myl1ssa-heartbeat-voice.log"
