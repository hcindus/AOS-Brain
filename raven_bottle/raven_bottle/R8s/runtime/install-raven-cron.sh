#!/data/data/com.termux/files/usr/bin/bash
# install-raven-cron.sh — register Raven's heartbeat with Android JobScheduler.
#
# This is the "cron" that survives Termux being closed, the screen being off,
# and the device rebooting. It fires raven-tick.sh on a period.
#
#   Usage:  install-raven-cron.sh [period-minutes]     (default 30, min 15)
#           install-raven-cron.sh --remove
#           install-raven-cron.sh --show

TICK="$HOME/v1/projects/5912/R8s/runtime/raven-tick.sh"
JOB_ID=5912

chmod +x "$TICK"

case "$1" in
  --remove)
    termux-job-scheduler --cancel --job-id "$JOB_ID"
    echo "🐦‍⬛ Raven's cron removed (job $JOB_ID)"
    exit 0
    ;;
  --show)
    termux-job-scheduler --pending
    exit 0
    ;;
esac

MIN="${1:-30}"
if [ "$MIN" -lt 15 ]; then
    echo "⚠️  Android's minimum period is 15 minutes — using 15."
    MIN=15
fi
PERIOD_MS=$(( MIN * 60 * 1000 ))

termux-job-scheduler \
  --script "$TICK" \
  --job-id "$JOB_ID" \
  --period-ms "$PERIOD_MS" \
  --persisted true \
  --network any \
  --battery-not-low false

# keep heartbeat.py's own notion of cadence in step with the cron period
python3 - <<PY
import json, os
p = os.path.expanduser("~/v1/projects/5912/R8s/HEARTBEAT.json")
cfg = json.load(open(p)) if os.path.exists(p) else {}
cfg["tempo_seconds"] = $PERIOD_MS // 1000
json.dump(cfg, open(p, "w"), indent=2)
print("🐦‍⬛ tempo synced to", cfg["tempo_seconds"], "s")
PY

echo "🐦‍⬛ Raven's cron installed — job $JOB_ID, every $MIN min, persists across reboot."
termux-job-scheduler --pending
