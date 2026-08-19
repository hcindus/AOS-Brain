---
name: jarvis-audit
description: Run a security, health, and data-integrity audit on the JARVIS tool. Use to verify the JARVIS service is hardened (token auth, PIN gate, rate limiting) and that the leads store is consistent. Returns a structured findings report (critical/high/medium/low/info) with an overall PASS/WARN/FAIL status.
---

# JARVIS Audit

Audits the JARVIS AI assistant (Performance Supply Depot) for security,
health, and data integrity.

## Checks

- **Security** — PIN gate configured (and strength), rate limiting active, token auth enforced.
- **Data integrity** — leads table accessible, no empty names, no negative values.
- **Health** — leads store reachable.

## Usage

### Standalone
```bash
cd /root/.openclaw/workspace
python3 skills/jarvis-audit/audit.py
```

### As a library
```python
from skills.jarvis_audit.audit import run_audit
from jarvis_core import LeadsStore, PinGate
report = run_audit(LeadsStore(), PinGate())
```

### Via the API
`GET /api/audit` on the running JARVIS service.

## Output
```json
{
  "status": "PASS|WARN|FAIL",
  "summary": {"total": N, "critical": N, "high": N, "medium": N, "low": N},
  "findings": [{"level": "critical|high|medium|low|info", "check": "...", "detail": "..."}]
}
```
