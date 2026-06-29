#!/bin/bash
# PENDING_TASKS Freshness Checker
# Runs daily to alert on stale tasks

CHECK_DATE=$(date +%s)
ALERT_DAYS=7
CRITICAL_DAYS=30
LOG_FILE="/var/log/aos/pending_tasks_freshness.log"

# Function to check file age
check_freshness() {
    local file=$1
    local name=$2
    
    if [ -f "$file" ]; then
        FILE_AGE=$(( (CHECK_DATE - $(stat -c %Y "$file")) / 86400 ))
        
        if [ $FILE_AGE -gt $CRITICAL_DAYS ]; then
            echo "[CRITICAL] $name: ${FILE_AGE} days stale"
            return 2
        elif [ $FILE_AGE -gt $ALERT_DAYS ]; then
            echo "[WARNING] $name: ${FILE_AGE} days stale"
            return 1
        fi
    fi
    return 0
}

# Check all agent PENDING_TASKS
echo "=== PENDING_TASKS Freshness Check $(date) ===" >> "$LOG_FILE"

for agent_dir in /root/.openclaw/workspace/agent_sandboxes/*/; do
    if [ -d "$agent_dir/tasks" ]; then
        for task_file in "$agent_dir/tasks/"*.md; do
            if [ -f "$task_file" ]; then
                AGENT_NAME=$(basename "$agent_dir")
                TASK_NAME=$(basename "$task_file" .md)
                check_freshness "$task_file" "$AGENT_NAME/$TASK_NAME" >> "$LOG_FILE"
            fi
        done
    fi
done

# Send alert if critical items found
if grep -q "\[CRITICAL\]" "$LOG_FILE"; then
    echo "CRITICAL: Stale PENDING_TASKS detected. Review required." | \
    mail -s "CRITICAL: PENDING_TASKS Stale Alert" miles@myl0nr0s.cloud 2>/dev/null || true
fi

echo "Check complete. See $LOG_FILE for details."
