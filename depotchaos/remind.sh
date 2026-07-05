#!/bin/bash
# DepotChaos MS-Connect Follow-up Reminder System
# Add to crontab: */15 * * * * /root/.openclaw/workspace/depotchaos/remind.sh

PYTHON_PATH="/usr/bin/python3"
WORKFLOW_PATH="/root/.openclaw/workspace/depotchaos/temporal_workflow.py"
LOG_FILE="/var/log/depotchaos/reminders.log"

# Ensure log directory exists
mkdir -p /var/log/depotchaos

# Run reminder check
$PYTHON_PATH $WORKFLOW_PATH --check-reminders >> $LOG_FILE 2>&1

# Check for overdue tasks daily at 8am
# 0 8 * * * /root/.openclaw/workspace/depotchaos/remind.sh --overdue
