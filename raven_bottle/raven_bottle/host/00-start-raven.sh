#!/data/data/com.termux/files/usr/bin/bash
# 00-start-raven.sh — the whole order, then the alarm.
#
# Replaces the scattered per-organ boot entries with ONE that follows §2 of
# BLUEPRINT.md: brain first (the heart reads it), then the heart, then her.
# Every launcher is idempotent, so overlap with the older boot scripts is safe.
#
# It ends with boot-check.sh — because a boot that cannot say "organs: dark"
# is how a brain sits dead for five days behind a working mouth.

LOG=~/.termux/boot.log
R=~/v1/projects/5912/Myl1Ssa/runtime

echo "[$(date)] ── starting Raven ──" >> "$LOG"

bash ~/start-brain.sh                       >> "$LOG" 2>&1   # 1. the brain
sleep 3
bash "$R/start-affect-bridge.sh"            >> "$LOG" 2>&1   # 2. brain → heart
bash "$R/start-myl1ssa-pulse.sh"            >> "$LOG" 2>&1   # 3. the tick engine
bash "$R/start-myl1ssa-voice.sh"            >> "$LOG" 2>&1   # 4. the audible heart

# 5. THE ALARM
bash "$R/boot-check.sh"                     >> "$LOG" 2>&1

echo "[$(date)] ── Raven start complete ──" >> "$LOG"
