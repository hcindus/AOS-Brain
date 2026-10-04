#!/data/data/com.termux/files/usr/bin/bash
# myl1ssa-tick.sh — one heartbeat pulse. Target of termux-job-scheduler.
cd "$(dirname "$0")" || exit 1
exec python3 heartbeat.py tick >> "$HOME/myl1ssa-pulse.log" 2>&1
