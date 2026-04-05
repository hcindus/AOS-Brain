# VPS Security Probe Installation Summary
**Installed By:** Dusty  
**Date:** 2026-04-05 01:39:57 UTC  
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

