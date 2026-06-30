#!/bin/bash
# Auto-Escalation System for Stale Tasks
# Runs hourly to escalate tasks >30 days

ESCALATION_DIR="/root/.openclaw/workspace/aocros/escalations"
LOG_FILE="/var/log/aos/auto_escalation.log"
ESCALATION_DAYS=30

mkdir -p "$ESCALATION_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting auto-escalation check..."

# Find tasks older than ESCALATION_DAYS
find /root/.openclaw/workspace/agent_sandboxes -name "*.md" -path "*/tasks/*" -mtime +$ESCALATION_DAYS 2>/dev/null | while read task; do
    agent=$(echo "$task" | cut -d'/' -f7)
    task_name=$(basename "$task" .md)
    age=$(stat -c %Y "$task" 2>/dev/null | xargs -I {} echo "($(date +%s) - {}) / 86400" | bc)
    
    log "ESCALATING: $agent/$task_name (${age} days old)"
    
    # Create escalation notice
    cat > "$ESCALATION_DIR/${task_name}_${agent}_$(date +%Y%m%d).txt" << EOC
ESCALATION NOTICE
=================
Task: $task_name
Agent: $agent
Age: ${age} days
File: $task

This task has exceeded the ${ESCALATION_DAYS}-day threshold and requires
CAPTAIN intervention.

Patricia has attempted resolution but this item needs
your direct attention.

EOC
done

log "Auto-escalation complete."
