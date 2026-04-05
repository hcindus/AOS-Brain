#!/bin/bash
# Custom security probe - runs every 5 minutes via cron

LOG_FILE="/var/log/security-probes/custom-probe.log"
ALERT_FILE="/root/.openclaw/workspace/security/alerts.json"
mkdir -p /root/.openclaw/workspace/security

# Check for high CPU usage (>80%)
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "{\"timestamp\":\"$(date -u -Iseconds)\",\"alert\":\"HIGH_CPU\",\"value\":$CPU_USAGE}" >> "$ALERT_FILE"
fi

# Check for high memory usage (>80%)
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 80 ]; then
    echo "{\"timestamp\":\"$(date -u -Iseconds)\",\"alert\":\"HIGH_MEMORY\",\"value\":$MEM_USAGE}" >> "$ALERT_FILE"
fi

# Check for failed login attempts
FAILED_LOGINS=$(grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l)
if [ "$FAILED_LOGINS" -gt 10 ]; then
    echo "{\"timestamp\":\"$(date -u -Iseconds)\",\"alert\":\"FAILED_LOGINS\",\"count\":$FAILED_LOGINS}" >> "$ALERT_FILE"
fi

# Log probe run
echo "$(date -u -Iseconds) - Probe check complete" >> "$LOG_FILE"
