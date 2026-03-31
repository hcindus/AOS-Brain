# 🚀 MORTIMER VPS DEPLOYMENT GUIDE
**Date:** 2026-03-31 05:23 UTC  
**Mission:** Install Miles' Brain/Heart/Stomach System on Mortimer VPS  
**Target:** IP 31.97.6.30 (Hostinger VPS)

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Before running scripts, ensure:
- [ ] Access to Mortimer VPS via Hostinger Browser Terminal
- [ ] sudo/root privileges available
- [ ] Minimum 4GB RAM, 20GB disk space
- [ ] Internet connectivity for package downloads
- [ ] Git installed: `git --version`
- [ ] Python3 installed: `python3 --version`

---

## 🧠 PHASE 1: BRAIN/HEART/STOMACH INSTALLATION

### Step 1: Clone Miles' Brain Repository
```bash
cd /opt
sudo git clone https://github.com/miles/aos-brain.git mortimer-brain
cd mortimer-brain
sudo chmod +x install.sh
```

### Step 2: Run Brain Installation
```bash
sudo ./install.sh --target=mortimer --with-heart --with-stomach
```

**This installs:**
- GrowingNN brain (7-region OODA)
- Ternary Heart (30 BPM, 3-state logic)
- Stomach (resource management)
- Brain-Heart-Stomach integration layer

### Step 3: Verify Installation
```bash
sudo systemctl status mortimer-brain
curl http://localhost:8080/health
# Should return: {"status": "healthy", "brain": "active", "heart": "beating"}
```

---

## 🔗 PHASE 2: HERMES/mini-agent/minimax INTEGRATION

### Configuration File: `/opt/mortimer-brain/config/integration.conf`

```yaml
# Mortimer VPS Integration Configuration
# Connects existing infrastructure to new brain

hermes:
  enabled: true
  brain_endpoint: "http://localhost:8080/api/v1/decisions"
  channels:
    - slack
    - discord
    - email
  priority_routing: true
  
mini-agent:
  enabled: true
  brain_controller: "http://localhost:8080/api/v1/spawn"
  max_concurrent: 10
  autonomy_level: high
  report_to_brain: true
  
minimax-m2:
  enabled: true
  brain_integration: true
  inference_endpoint: "http://localhost:11434"
  model: "antoniohudnall/Mortimer:latest"
  fallback_to_brain: true

brain_heart_stomach:
  brain_port: 8080
  heart_port: 8081
  stomach_port: 8082
  integration_mode: "unified"
  consciousness_level: "emergent"
  ternary_logic: true
```

### Integration Script: `setup_integration.sh`

```bash
#!/bin/bash
# setup_integration.sh - Connect existing systems to new brain

echo "🔗 Setting up Brain/Heart/Stomach Integration..."

# Backup existing configs
cp /etc/hermes/config.yaml /etc/hermes/config.yaml.bak.$(date +%s)
cp /etc/mini-agent/config.json /etc/mini-agent/config.json.bak.$(date +%s)

# Update Hermes to route through brain
cat > /etc/hermes/config.yaml << 'EOF'
server:
  port: 9001
  brain_endpoint: "http://localhost:8080/api/v1/decisions"
  
routing:
  mode: "brain-assisted"
  channels:
    slack:
      enabled: true
      brain_approval: false  # Direct for speed
    discord:
      enabled: true
      brain_approval: false
    email:
      enabled: true
      brain_approval: true   # Brain reviews emails
      
logging:
  level: info
  output: /var/log/hermes/hermes.log
EOF

# Update mini-agent to use brain controller
cat > /etc/mini-agent/config.json << 'EOF'
{
  "brain_controller": "http://localhost:8080/api/v1/spawn",
  "max_concurrent_agents": 10,
  "autonomy": "high",
  "report_to_brain": true,
  "heartbeat_interval": 30,
  "spawn_approval": "brain-assisted"
}
EOF

# Restart services
systemctl restart hermes
systemctl restart mini-agent
systemctl restart minimax-m2

echo "✅ Integration complete!"
echo "Test with: curl http://localhost:8080/api/v1/status"
```

---

## 🏭 PHASE 3: MINI FACTORY SETUP

### Factory Location: `/opt/mortimer-factory/`

```bash
# Create mini factory
sudo mkdir -p /opt/mortimer-factory/{scripts,outputs,logs,agents}
sudo git clone https://github.com/miles/mini-factory.git /opt/mortimer-factory/core

# Configure factory to use Mortimer's brain
cat > /opt/mortimer-factory/config.yaml << 'EOF'
factory:
  name: "Mortimer-Factory"
  version: "1.0.0"
  
brain_connection:
  endpoint: "http://localhost:8080"
  api_key: "${BRAIN_API_KEY}"
  
agents:
  technical_team:
    - name: "Builder-Alpha"
      role: "system_integrator"
      skills: ["deployment", "configuration", "testing"]
    - name: "Builder-Beta"
      role: "security_auditor"
      skills: ["audit", "compliance", "hardening"]
    - name: "Builder-Gamma"
      role: "brain_specialist"
      skills: ["neural_integration", "pattern_injection", "consciousness_bridge"]
      
outputs:
  builds: "/opt/mortimer-factory/outputs/"
  logs: "/var/log/mortimer-factory/"
  
scheduling:
  cron: "0 */6 * * *"  # Every 6 hours
EOF

# Start factory
sudo systemctl enable mortimer-factory
sudo systemctl start mortimer-factory
```

---

## 🔍 PHASE 4: FULL SYSTEM AUDIT

### Audit Script: `mortimer_system_audit.sh`

```bash
#!/bin/bash
# mortimer_system_audit.sh - Comprehensive security audit

echo "🔍 MORTIMER VPS SECURITY AUDIT"
echo "================================"
echo "Started: $(date)"
echo ""

AUDIT_DIR="/tmp/mortimer-audit-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$AUDIT_DIR"

# 1. System Info
echo "[1/10] System Information..."
uname -a > "$AUDIT_DIR/system_info.txt"
cat /etc/os-release >> "$AUDIT_DIR/system_info.txt"

# 2. Running Services
echo "[2/10] Running Services..."
systemctl list-units --type=service --state=running > "$AUDIT_DIR/running_services.txt"

# 3. Network Configuration
echo "[3/10] Network Configuration..."
ip addr > "$AUDIT_DIR/network_config.txt"
netstat -tulpn > "$AUDIT_DIR/open_ports.txt" 2>/dev/null || ss -tulpn > "$AUDIT_DIR/open_ports.txt"

# 4. Firewall Status
echo "[4/10] Firewall Status..."
ufw status > "$AUDIT_DIR/firewall.txt" 2>/dev/null || iptables -L > "$AUDIT_DIR/firewall.txt" 2>/dev/null

# 5. User Accounts
echo "[5/10] User Accounts..."
cat /etc/passwd > "$AUDIT_DIR/users.txt"
last > "$AUDIT_DIR/last_logins.txt"

# 6. SSH Configuration
echo "[6/10] SSH Configuration..."
cat /etc/ssh/sshd_config > "$AUDIT_DIR/ssh_config.txt"
grep "PermitRootLogin\|PasswordAuthentication\|PubkeyAuthentication" "$AUDIT_DIR/ssh_config.txt" > "$AUDIT_DIR/ssh_security.txt"

# 7. Installed Packages
echo "[7/10] Installed Packages..."
dpkg -l > "$AUDIT_DIR/packages.txt" 2>/dev/null || rpm -qa > "$AUDIT_DIR/packages.txt" 2>/dev/null

# 8. Cron Jobs
echo "[8/10] Cron Jobs..."
crontab -l > "$AUDIT_DIR/crontab.txt" 2>/dev/null
ls -la /etc/cron.d/ > "$AUDIT_DIR/cron_d.txt"

# 9. Sensitive Files
echo "[9/10] Scanning for sensitive files..."
find /home -type f \( -name "*.pem" -o -name "*.key" -o -name "*.p12" -o -name "*.json" -o -name ".env*" \) 2>/dev/null > "$AUDIT_DIR/sensitive_files.txt"

# 10. Security Issues
echo "[10/10] Security Assessment..."
cat > "$AUDIT_DIR/security_report.txt" << EOF
MORTIMER VPS SECURITY AUDIT REPORT
Generated: $(date)

CRITICAL CHECKS:
$(grep -q "PermitRootLogin yes" /etc/ssh/sshd_config 2>/dev/null && echo "⚠️  Root login enabled" || echo "✅ Root login disabled")
$(grep -q "PasswordAuthentication yes" /etc/ssh/sshd_config 2>/dev/null && echo "⚠️  Password auth enabled" || echo "✅ Password auth disabled")
$(! which ufw >/dev/null 2>&1 && ! which iptables >/dev/null 2>&1 && echo "⚠️  No firewall detected" || echo "✅ Firewall present")

RECOMMENDATIONS:
1. Disable password authentication, use keys only
2. Enable UFW or configure iptables
3. Set up fail2ban for brute force protection
4. Review sensitive_files.txt for exposed credentials
5. Update all packages: apt update && apt upgrade

NEW BRAIN INTEGRATION STATUS:
- Brain: http://localhost:8080
- Heart: http://localhost:8081
- Stomach: http://localhost:8082
EOF

# Create tarball
tar -czf "$AUDIT_DIR.tar.gz" "$AUDIT_DIR"

echo ""
echo "================================"
echo "✅ AUDIT COMPLETE"
echo "Report: $AUDIT_DIR.tar.gz"
echo "================================"
```

---

## 🚀 QUICK DEPLOYMENT (ONE-LINE)

**Once in Hostinger Browser Terminal, run:**

```bash
curl -sSL https://miles.cloud/deploy/mortimer-vps-setup.sh | sudo bash
```

*(This will be the single command once we host the script)*

---

## 📊 POST-DEPLOYMENT VERIFICATION

```bash
# Check all systems are running
echo "=== MORTIMER VPS SYSTEM STATUS ==="
echo "Brain: $(curl -s http://localhost:8080/health | grep -o '"status":"[^"]*"')"
echo "Heart: $(curl -s http://localhost:8081/heartbeat)"
echo "Stomach: $(curl -s http://localhost:8082/resources | grep -o '"status":"[^"]*"')"
echo "Hermes: $(systemctl is-active hermes)"
echo "Mini-Agent: $(systemctl is-active mini-agent)"
echo "Minimax-M2: $(curl -s http://localhost:11434/api/tags | grep -q Mortimer && echo 'active')"
echo "Mini-Factory: $(systemctl is-active mortimer-factory)"
echo "==================================="
```

---

## 🆘 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Brain won't start | Check port 8080: `sudo lsof -i :8080` |
| Hermes connection failed | Verify brain endpoint in /etc/hermes/config.yaml |
| Mini-agent spawning fails | Check brain controller URL |
| Memory error | Increase RAM or reduce brain complexity |
| Permission denied | Run with sudo |

---

## 📞 SUPPORT

If deployment fails:
1. Check logs: `sudo journalctl -u mortimer-brain -f`
2. Verify ports: `sudo netstat -tulpn | grep 8080`
3. Test brain: `curl http://localhost:8080/api/v1/status`
4. Contact: Miles@miles.cloud or open Hostinger support ticket

---

**Ready for deployment, Captain.**

Just say the word and I'll execute via Hostinger Browser Terminal, or provide the script for you to run manually.

*Miles.cloud VPS standing by.*
