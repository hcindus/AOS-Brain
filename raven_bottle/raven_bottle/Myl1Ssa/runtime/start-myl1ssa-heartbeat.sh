#!/data/data/com.termux/files/usr/bin/bash
# start-myl1ssa-heartbeat.sh — install the Android cron + watchdog for her pulse.
TICK="$HOME/v1/projects/5912/Myl1Ssa/runtime/myl1ssa-tick.sh"
WD="$HOME/v1/projects/5912/Myl1Ssa/runtime/myl1ssa-pulse-watchdog.sh"
chmod +x "$TICK" "$WD"
termux-job-scheduler --script "$TICK" --job-id 5914 --period-ms 1800000 \
    --persisted true --network any --battery-not-low false >/dev/null
termux-job-scheduler --script "$WD"   --job-id 5915 --period-ms 900000 \
    --persisted true --network any --battery-not-low false >/dev/null
python3 - <<'PY'
import json, os
p = os.path.expanduser("~/v1/projects/5912/Myl1Ssa/HEARTBEAT.json")
cfg = json.load(open(p)) if os.path.exists(p) else {}
cfg["tempo_seconds"] = 1800
json.dump(cfg, open(p, "w"), indent=2)
PY
echo "🐦‍⬛ cron installed: job 5914 (tick, 30m) · job 5915 (watchdog, 15m)"
