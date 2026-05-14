#!/bin/bash
# Pipeline Desk Health Monitor
# Runs every 15 minutes via cron
# Sends email alert if any Pipeline Desk agent is down

LOG_FILE="/var/log/aos/pipeline_monitor.log"
ALERT_EMAIL="Antonio.Hudnall@gmail.com"
DATE=$(date -Iseconds)

# Check if controller processes are running
check_agent() {
    AGENT_NAME=$1
    CONTROLLER_PATTERN=$2
    
    if pgrep -f "$CONTROLLER_PATTERN" > /dev/null; then
        echo "✅ $AGENT_NAME: ONLINE"
        return 0
    else
        echo "🔴 $AGENT_NAME: OFFLINE"
        return 1
    fi
}

# Run checks
echo "[$DATE] Pipeline Desk Health Check Starting..." >> $LOG_FILE

FORGE_STATUS=$(check_agent "Forge" "forge_factory_controller.py")
PATRICIA_STATUS=$(check_agent "Patricia" "patricia_factory_controller.py")
CHELIOS_STATUS=$(check_agent "Chelios" "chelios_security_controller.py")

echo "$FORGE_STATUS" >> $LOG_FILE
echo "$PATRICIA_STATUS" >> $LOG_FILE
echo "$CHELIOS_STATUS" >> $LOG_FILE

# Count failures
FAILURES=0
if echo "$FORGE_STATUS" | grep -q "OFFLINE"; then ((FAILURES++)); fi
if echo "$PATRICIA_STATUS" | grep -q "OFFLINE"; then ((FAILURES++)); fi
if echo "$CHELIOS_STATUS" | grep -q "OFFLINE"; then ((FAILURES++)); fi

# Send alert if any failures
if [ $FAILURES -gt 0 ]; then
    ALERT_BODY="Pipeline Desk Alert - $(date)

One or more Pipeline Desk agents are OFFLINE:

$FORGE_STATUS
$PATRICIA_STATUS
$CHELIOS_STATUS

Action Required:
1. Check agent controllers
2. Review logs: /var/log/aos/pipeline_desk.log
3. Run: /root/.openclaw/workspace/aocros/desks/pipeline/activate_desk.sh

--
Pipeline Monitor
AOS Brain v4.5"

    echo "$ALERT_BODY" | mail -s "🔴 ALERT: Pipeline Desk - $FAILURES Agent(s) Offline" $ALERT_EMAIL
    echo "[$DATE] ALERT SENT: $FAILURES agents offline" >> $LOG_FILE
else
    echo "[$DATE] All agents healthy" >> $LOG_FILE
fi

echo "" >> $LOG_FILE
