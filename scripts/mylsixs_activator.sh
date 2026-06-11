#!/bin/bash
# Mylsixs Email Manager Cron Wrapper
# Runs the email manager and activates Mylsixs

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/mylsixs_activator.log"
MYLSIXS_DIR="$WORKSPACE/AGI_COMPANY/agents/tier3/mylsixs"

mkdir -p /var/log/aos

echo "[$(date -Iseconds)] Activating Mylsixs for email duty..." >> "$LOG_FILE"

# Activate Mylsixs (create heartbeat trigger)
if [ -d "$MYLSIXS_DIR" ]; then
    echo "activated:$(date -Iseconds):email_duty" > "$MYLSIXS_DIR/.heartbeat_trigger"
    echo "[$(date -Iseconds)] ✅ Mylsixs activated" >> "$LOG_FILE"
fi

# Run email manager
python3 "$WORKSPACE/scripts/mylsixs_email_manager.py" >> "$LOG_FILE" 2>&1

echo "[$(date -Iseconds)] Mylsixs email duty complete" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
