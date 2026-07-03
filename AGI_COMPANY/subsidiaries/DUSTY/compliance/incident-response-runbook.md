# Incident Response Runbook

**Version:** 1.0  
**Last Updated:** 2026-07-03  
**Status:** Phase 1 Ready

---

## 1. Incident Classification

| Severity | Definition | Examples | Response Time |
|----------|------------|----------|---------------|
| **Critical** | System down, funds at risk | Exchange API breach, wallet compromise, data breach | 15 minutes |
| **High** | Service degraded, potential loss | API rate limiting, connection failures, suspicious activity | 1 hour |
| **Medium** | Non-critical issues | Performance degradation, minor errors | 4 hours |
| **Low** | Documentation, questions | User inquiries, feature requests | 24 hours |

---

## 2. Response Team

| Role | Responsibility | Contact |
|------|----------------|---------|
| Incident Commander | Overall coordination, decision making | Captain |
| Technical Lead | System assessment, containment | Mortimer |
| Compliance Officer | Regulatory notifications | Patricia2 |
| Communications | User notifications, status updates | Miles |

---

## 3. Response Procedures

### Phase 1: Detection & Assessment (0-15 min)

1. **Alert received** (monitoring, user report, automated)
2. **Verify incident** - Check if legitimate, assess scope
3. **Classify severity** - Use table above
4. **Notify team** - Page incident commander
5. **Open incident channel** - Dedicated communication line

### Phase 2: Containment (15-60 min)

1. **Isolate affected systems**
   - Disable compromised API keys
   - Block suspicious IPs
   - Freeze affected wallets (if applicable)
2. **Preserve evidence**
   - Save logs, screenshots
   - Document timeline
3. **Assess impact**
   - Affected users
   - Financial exposure
   - Data exposure

### Phase 3: Eradication & Recovery (1-4 hours)

1. **Remove threat**
   - Patch vulnerabilities
   - Rotate credentials
   - Update firewall rules
2. **Restore service**
   - Bring systems online in order of priority
   - Verify functionality
3. **Monitor for recurrence**

### Phase 4: Post-Incident (24-72 hours)

1. **Post-mortem meeting**
   - What happened?
   - Why did it happen?
   - How did we respond?
   - What could be better?
2. **Documentation**
   - Incident report
   - Lessons learned
   - Action items
3. **Communication**
   - User notifications (if required)
   - Regulatory notifications (if required)
   - Internal debrief

---

## 4. Communication Templates

### User Notification (Data Breach)

```
Subject: Important Security Notice

We are writing to inform you of a security incident that may have affected your account...
[Details]
Steps we are taking...
Steps you should take...
```

### Regulatory Notification

- **FinCEN:** Within 30 days of discovery (if MSB)
- **State regulators:** Per state requirements
- **Law enforcement:** If criminal activity suspected

---

## 5. Escalation Matrix

| Time | Action |
|------|--------|
| 15 min | If critical, page all team members |
| 1 hour | If unresolved, engage external support |
| 4 hours | If unresolved, consider full system halt |
| 24 hours | Executive briefing required |

---

## 6. Testing Schedule

- **Tabletop exercise:** Monthly
- **Live drill:** Quarterly
- **Full simulation:** Annually

---

## 7. Contact Information

**Emergency:** support@psdepot.com  
**Legal:** legal@psdepot.com  
**Compliance:** compliance@psdepot.com

---

*Document Owner: Mortimer*  
*Review Date: Quarterly*
