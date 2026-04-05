# SECURITY AUDIT TASK FORCE
**Mission:** VPS Security Hardening, Log Consolidation, Deprecated Software Removal  
**Date:** April 5, 2026  
**Status:** ⏳ IN PROGRESS

---

## TEAM ASSIGNMENTS

### Agent: SENTINEL (Security Officer)
**Lead:** Security audit coordination, log analysis, deprecated software identification

**Tasks:**
1. **Log Consolidation**
   - [ ] Review /var/log/aos/ — AOS system logs
   - [ ] Review /var/log/openclaw/ — OpenClaw gateway logs
   - [ ] Review /root/.openclaw/workspace/logs/ — Workspace logs
   - [ ] Review /root/.aos/logs/ — AOS brain logs
   - [ ] Archive logs older than 30 days
   - [ ] Flag sensitive logs for secure deletion
   - [ ] Document retention policy

2. **Deprecated Software Review**
   - [ ] Scan pip packages: `pip list --outdated`
   - [ ] Check Node vulnerabilities: `npm audit`
   - [ ] Identify old agent scripts (unused)
   - [ ] Find legacy config files
   - [ ] Check for unused skills/extensions
   - [ ] Create DEPRECATED_SOFTWARE.md with risk ratings

3. **Security Audit Support**
   - [ ] Assist Jordan with GitHub token purge
   - [ ] Verify .env file usage across codebase
   - [ ] Check for remaining hardcoded credentials
   - [ ] Validate .gitignore completeness

**Deliverables:**
- /root/.openclaw/workspace/audit/SENTINEL_LOG_CONSOLIDATION.md
- /root/.openclaw/workspace/audit/DEPRECATED_SOFTWARE.md
- /root/.openclaw/workspace/audit/SECURITY_AUDIT_FINDINGS.md

---

### Agent: DUSTY (Financial/Systems Analyst)
**Lead:** VPS probe installation, monitoring setup, system hardening

**Tasks:**
1. **Probe Installation**
   - [ ] Install AIDE (file integrity monitoring)
   - [ ] Configure auditd (process monitoring)
   - [ ] Install tcpdump (network baseline)
   - [ ] Setup rsyslog forwarding (log aggregation)
   - [ ] Install Prometheus node_exporter (metrics)

2. **Probe Configuration**
   - [ ] Monitor /root/.openclaw/workspace/ — Source code
   - [ ] Monitor /root/.aos/ — Brain data
   - [ ] Monitor /tmp/ — Temporary files
   - [ ] Monitor /var/log/ — System logs
   - [ ] Monitor systemd services (aos-brain-v4, aos-mission-control)

3. **Alert Setup**
   - [ ] Unauthorized file changes → CRITICAL
   - [ ] Failed login attempts → HIGH
   - [ ] High CPU/memory (>80%) → MEDIUM
   - [ ] Suspicious network connections → HIGH
   - [ ] Service failures → CRITICAL

**Deliverables:**
- /root/.openclaw/workspace/security/probes/PROBE_INSTALLATION.md
- /root/.openclaw/workspace/security/probes/alert-config.yaml
- /root/.openclaw/workspace/security/probes/start-probes.sh
- /root/.openclaw/workspace/security/probes/stop-probes.sh

---

### Agent: CHELIOS (Systems Engineer)
**Lead:** Software cleanup, system optimization, deprecated removal

**Tasks:**
1. **Software Inventory**
   - [ ] List all installed packages (apt list --installed)
   - [ ] Check for unused Docker containers/images
   - [ ] Identify old tmux sessions
   - [ ] Check for orphaned processes
   - [ ] Review cron jobs (crontab -l)

2. **Cleanup Preparation**
   - [ ] Old Python virtual environments
   - [ ] Unused git repositories
   - [ ] Temporary download files
   - [ ] Old model checkpoints
   - [ ] Cache directories (pip, npm, etc.)

3. **Captain Approval List**
   - [ ] Create: /root/.openclaw/workspace/audit/REMOVAL_CANDIDATES.md
   - [ ] Include: name, size, last used, removal reason
   - [ ] Await Captain final approval before deletion

**Deliverables:**
- /root/.openclaw/workspace/audit/SOFTWARE_INVENTORY.md
- /root/.openclaw/workspace/audit/REMOVAL_CANDIDATES.md
- /root/.openclaw/workspace/audit/CLEANUP_PLAN.md

---

## COORDINATION

### Timeline
- **Hour 1:** Probe installation (Dusty)
- **Hour 2:** Log consolidation (Sentinel)
- **Hour 3:** Software inventory (Chelios)
- **Hour 4:** Security audit completion (All)

### Communication
- Report to: Jordan (Security Audit Lead)
- Status updates: Every 30 minutes
- Blockers: Escalate immediately to Captain

### Success Criteria
- [ ] All probes installed and alerting
- [ ] Logs consolidated and old logs flagged
- [ ] Deprecated software identified and flagged
- [ ] No remaining hardcoded credentials
- [ ] GitHub security audit complete
- [ ] Captain approval on all removals

---

## CRITICAL NOTES

⚠️ **DO NOT DELETE WITHOUT CAPTAIN APPROVAL**  
⚠️ **BACKUP BEFORE ANY CLEANUP**  
⚠️ **TEST PROBES BEFORE MARKING COMPLETE**  
⚠️ **DOCUMENT EVERY ACTION**

---

**Document ID:** SECURITY-TASK-FORCE-2026-04-05  
**Issued By:** Miles (Operations)  
**Approved By:** Captain  
**Status:** ACTIVE

---

*"Security is not a destination, it's a continuous journey."* — SENTINEL