#!/data/data/com.termux/files/usr/bin/bash
# raven-tick.sh — one heartbeat pulse.
# Target of termux-job-scheduler (Raven's cron). Safe to run by hand.

cd "$(dirname "$0")" || exit 1
exec python3 heartbeat.py tick >> "$HOME/raven-heartbeat.log" 2>&1
