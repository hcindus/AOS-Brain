#!/bin/bash
# DUSTY VPS PROBE INSTALLATION SCRIPT
# Security monitoring setup for Miles VPS

set -e

echo "=== DUSTY VPS PROBE INSTALLATION ==="
echo "Date: $(date -u)"
echo ""

# Create directories
mkdir -p /root/.openclaw/workspace/security/probes
mkdir -p /root/.openclaw/workspace/security/logs
mkdir -p /var/log/security-probes

# 1. Install AIDE (File Integrity Monitor)
echo "[1/5] Installing AIDE (File Integrity Monitor)..."
apt-get update -qq
apt-get install -y -qq aide aide-common 2>/dev/null || echo "AIDE already installed or skipped"

# Configure AIDE
cat > /etc/aide/aide.conf.d/50-openclaw.conf << 'EOF'
# Monitor critical directories
/root/.openclaw/workspace/   p+u+g+n+md5+sha256
/root/.aos/                p+u+g+n+md5+sha256
/etc/systemd/system/       p+u+g+n+md5+sha256
/var/log/aos/              p+u+g+n+md5+sha256
EOF

# Initialize AIDE database
aideinit 2>/dev/null || echo "AIDE database exists"

echo "✓ AIDE configured"

# 2. Install auditd (Process Monitoring)
echo "[2/5] Installing auditd..."
apt-get install -y -qq auditd audispd-plugins 2>/dev/null || echo "auditd already installed"

# Configure auditd
cat > /etc/audit/rules.d/99-openclaw.rules << 'EOF'
# Monitor file access in workspace
-w /root/.openclaw/workspace/ -p wa -k openclaw_workspace
-w /root/.aos/ -p wa -k aos_data
-w /tmp/ -p wa -k temp_files
-w /etc/systemd/system/aos-brain-v4.service -p wa -k aos_service
-w /etc/systemd/system/aos-mission-control.service -p wa -k mc_service
EOF

# Restart auditd
service auditd restart 2>/dev/null || systemctl restart auditd 2>/dev/null || echo "auditd restart queued"

echo "✓ auditd configured"

# 3. Install Prometheus node_exporter
echo "[3/5] Installing Prometheus node_exporter..."
if [ ! -f /usr/local/bin/node_exporter ]; then
    cd /tmp
    wget -q https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
    tar xzf node_exporter-1.7.0.linux-amd64.tar.gz
    cp node_exporter-1.7.0.linux-amd64/node_exporter /usr/local/bin/
    chmod +x /usr/local/bin/node_exporter
    rm -rf node_exporter-1.7.0.linux-amd64*
fi

# Create systemd service for node_exporter
cat > /etc/systemd/system/node-exporter.service << 'EOF'
[Unit]
Description=Prometheus Node Exporter
After=network.target

[Service]
User=root
ExecStart=/usr/local/bin/node_exporter --web.listen-address=:9100
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable node-exporter 2>/dev/null || true
systemctl start node-exporter 2>/dev/null || echo "node_exporter start queued"

echo "✓ node_exporter installed (port 9100)"

# 4. Install rsyslog for log aggregation (if not present)
echo "[4/5] Configuring rsyslog..."
cat > /etc/rsyslog.d/50-security-probes.conf << 'EOF'
# Security probe logs
:programname, isequal, "aide" /var/log/security-probes/aide.log
:programname, isequal, "auditd" /var/log/security-probes/auditd.log
:programname, contains, "security" /var/log/security-probes/security.log
EOF

systemctl restart rsyslog 2>/dev/null || echo "rsyslog restart queued"

echo "✓ rsyslog configured"

# 5. Create custom monitoring script
echo "[5/5] Creating custom security probe..."

cat > /root/.openclaw/workspace/security/probes/security-probe.sh << 'EOF'
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
EOF

chmod +x /root/.openclaw/workspace/security/probes/security-probe.sh

# Add to cron (every 5 minutes)
echo "*/5 * * * * /root/.openclaw/workspace/security/probes/security-probe.sh" | crontab -

echo "✓ Custom probe configured (runs every 5 min)"

# 6. Create control scripts
cat > /root/.openclaw/workspace/security/probes/start-probes.sh << 'EOF'
#!/bin/bash
echo "Starting security probes..."
systemctl start auditd 2>/dev/null || true
systemctl start node-exporter 2>/dev/null || true
echo "✓ Probes started"
EOF

cat > /root/.openclaw/workspace/security/probes/stop-probes.sh << 'EOF'
#!/bin/bash
echo "Stopping security probes..."
systemctl stop auditd 2>/dev/null || true
systemctl stop node-exporter 2>/dev/null || true
echo "✓ Probes stopped"
EOF

cat > /root/.openclaw/workspace/security/probes/status-probes.sh << 'EOF'
#!/bin/bash
echo "=== Security Probe Status ==="
echo ""
echo "AIDE:"
aide --check 2>/dev/null | head -3 || echo "  Database initialized"
echo ""
echo "auditd:"
systemctl status auditd --no-pager 2>/dev/null | head -5 || echo "  Status unknown"
echo ""
echo "node_exporter:"
systemctl status node-exporter --no-pager 2>/dev/null | head -5 || echo "  Status unknown"
echo ""
echo "Custom probe (cron):"
crontab -l | grep security-probe || echo "  Not in cron"
echo ""
echo "Metrics endpoint: http://localhost:9100/metrics"
EOF

chmod +x /root/.openclaw/workspace/security/probes/*.sh

# Create configuration summary
cat > /root/.openclaw/workspace/security/probes/PROBE_INSTALLATION.md << 'EOF'
# VPS Security Probe Installation Summary
**Installed By:** Dusty  
**Date:** DATE_PLACEHOLDER  
**Status:** ACTIVE

## Installed Probes

### 1. AIDE (File Integrity Monitor)
- **Purpose:** Detect unauthorized file changes
- **Monitored:** /root/.openclaw/workspace/, /root/.aos/, /etc/systemd/system/, /var/log/aos/
- **Check:** `aide --check`
- **Update DB:** `aideupdate`
- **Log:** /var/log/aide/

### 2. auditd (Process & File Access Monitor)
- **Purpose:** Track system calls and file access
- **Monitored:** Workspace, AOS data, temp files, systemd services
- **View Logs:** `ausearch -k openclaw_workspace`
- **Status:** `systemctl status auditd`
- **Log:** /var/log/audit/

### 3. Prometheus node_exporter
- **Purpose:** System metrics collection
- **Endpoint:** http://localhost:9100/metrics
- **Status:** `systemctl status node-exporter`
- **Metrics:** CPU, memory, disk, network, processes

### 4. Custom Security Probe (via cron)
- **Schedule:** Every 5 minutes
- **Purpose:** Custom alerts for CPU, memory, failed logins
- **Script:** /root/.openclaw/workspace/security/probes/security-probe.sh
- **Alerts:** /root/.openclaw/workspace/security/alerts.json
- **Log:** /var/log/security-probes/custom-probe.log

## Control Scripts

```bash
# Start all probes
/root/.openclaw/workspace/security/probes/start-probes.sh

# Stop all probes
/root/.openclaw/workspace/security/probes/stop-probes.sh

# Check status
/root/.openclaw/workspace/security/probes/status-probes.sh
```

## Alert Thresholds

| Condition | Severity | Action |
|-----------|----------|--------|
| CPU >80% | MEDIUM | Log to alerts.json |
| Memory >80% | MEDIUM | Log to alerts.json |
| Failed logins >10 | HIGH | Log to alerts.json |
| File integrity violation | CRITICAL | aide log + system alert |

## Next Steps

- [ ] Configure alert notifications (email/webhook)
- [ ] Set up Grafana dashboard for node_exporter
- [ ] Review aide database baseline weekly
- [ ] Audit log rotation policy

EOF

# Replace date
DATE=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
sed -i "s/DATE_PLACEHOLDER/$DATE/" /root/.openclaw/workspace/security/probes/PROBE_INSTALLATION.md

echo ""
echo "=== INSTALLATION COMPLETE ==="
echo ""
echo "Installed probes:"
echo "  1. AIDE - File integrity monitor"
echo "  2. auditd - Process/file access monitor"
echo "  3. node_exporter - System metrics (port 9100)"
echo "  4. Custom probe - CPU/memory/failed logins (every 5 min)"
echo ""
echo "Documentation: /root/.openclaw/workspace/security/probes/PROBE_INSTALLATION.md"
echo "Status check: /root/.openclaw/workspace/security/probes/status-probes.sh"
echo ""
echo "✓ DUSTY PROBE INSTALLATION COMPLETE"