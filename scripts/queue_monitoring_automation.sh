#!/bin/bash
# Queue monitoring automation
# Alert on bottlenecks, generate daily reports

LOG_FILE="/var/log/aos/queue_monitor.log"
ALERT_THRESHOLD=1000
DAILY_REPORT="/root/.openclaw/workspace/aocros/reports/daily_queue_report.md"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Count tasks across all agents
TOTAL_TASKS=0
for agent_dir in /root/.openclaw/workspace/agent_sandboxes/*/; do
    if [ -d "$agent_dir/tasks" ]; then
        agent_name=$(basename "$agent_dir")
        task_count=$(ls "$agent_dir/tasks/"*.md 2>/dev/null | wc -l)
        TOTAL_TASKS=$((TOTAL_TASKS + task_count))
        log "$agent_name: $task_count tasks"
    fi
done

log "Total queue size: $TOTAL_TASKS"

# Alert if over threshold
if [ "$TOTAL_TASKS" -gt "$ALERT_THRESHOLD" ]; then
    log "ALERT: Queue size $TOTAL_TASKS exceeds threshold $ALERT_THRESHOLD"
    echo "Queue Alert: $TOTAL_TASKS tasks pending" | mail -s "Queue Alert" miles@myl0nr0s.cloud 2>/dev/null || true
fi

# Generate daily report
cat > "$DAILY_REPORT" << EOT
# Daily Queue Report
**Date:** $(date +%Y-%m-%d)
**Total Tasks:** $TOTAL_TASKS
**Threshold:** $ALERT_THRESHOLD

## Queue Status
$(for agent_dir in /root/.openclaw/workspace/agent_sandboxes/*/; do
    if [ -d "$agent_dir/tasks" ]; then
        agent_name=$(basename "$agent_dir")
        task_count=$(ls "$agent_dir/tasks/"*.md 2>/dev/null | wc -l)
        echo "- $agent_name: $task_count tasks"
    fi
done)

## Alerts
$(if [ "$TOTAL_TASKS" -gt "$ALERT_THRESHOLD" ]; then
    echo "🔴 Queue exceeds threshold - redistribute workload"
else
    echo "✅ Queue within normal limits"
fi)

EOT

log "Daily report generated: $DAILY_REPORT"
