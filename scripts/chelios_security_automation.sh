#!/bin/bash
# Chelios Security Automation
# Runs security audits every 24 hours

LOG_FILE="/var/log/aos/chelios_security.log"
AUDIT_DIR="/root/.openclaw/workspace/agent_sandboxes/chelios/audits"

mkdir -p "$AUDIT_DIR"

echo "[$(date)] Starting Chelios security audit..." >> "$LOG_FILE"

# Run security controller
cd /root/.openclaw/workspace/agent_sandboxes/chelios
/usr/bin/python3 chelios_security_controller.py tick >> "$LOG_FILE" 2>&1

# Generate daily audit report
AUDIT_FILE="$AUDIT_DIR/audit_$(date +%Y-%m-%d).txt"
echo "=== Security Audit $(date) ===" > "$AUDIT_FILE"
echo "System: Miles.brain.cloud" >> "$AUDIT_FILE"
echo "Auditor: Chelios" >> "$AUDIT_FILE"

# Check SSH access
echo "" >> "$AUDIT_FILE"
echo "SSH Configuration:" >> "$AUDIT_FILE"
grep "PermitRootLogin\|PasswordAuthentication" /etc/ssh/sshd_config 2>/dev/null | head -5 >> "$AUDIT_FILE"

# Check firewall
echo "" >> "$AUDIT_FILE"
echo "Active Ports:" >> "$AUDIT_FILE"
ss -tlnp | grep -E ":22|:80|:443|:8080|:8767" >> "$AUDIT_FILE"

# Check for failed logins
echo "" >> "$AUDIT_FILE"
echo "Recent Failed Logins:" >> "$AUDIT_FILE"
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10 >> "$AUDIT_FILE"

echo "[$(date)] Audit complete: $AUDIT_FILE" >> "$LOG_FILE"
