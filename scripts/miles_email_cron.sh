#!/bin/bash
# Miles Email Responder Cron Wrapper
# Runs the email responder every 5 minutes

WORKSPACE="/root/.openclaw/workspace"
LOG_FILE="/var/log/aos/miles_email_responder.log"

mkdir -p /var/log/aos

echo "[$(date -Iseconds)] Miles activating for email duty..." >> "$LOG_FILE"

# Run email responder
python3 "$WORKSPACE/scripts/miles_email_responder.py" >> "$LOG_FILE" 2>&1

echo "[$(date -Iseconds)] Miles email duty complete" >> "$LOG_FILE"
