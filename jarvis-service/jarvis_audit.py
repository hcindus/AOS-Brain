#!/usr/bin/env python3
"""
JARVIS Audit — run a security + health + data-integrity audit on the JARVIS tool.

Produces a structured report of findings (severity: critical/high/medium/low/info)
and an overall status (PASS / WARN / FAIL). Used both as a standalone skill and
exposed via the JARVIS API at GET /api/audit.
"""
from datetime import datetime
from typing import Any


def audit_leads(store) -> list[dict]:
    """Data-integrity checks on the leads table."""
    findings = []
    try:
        leads = store.all()
    except Exception as e:
        return [{"level": "critical", "check": "leads-accessible",
                 "detail": f"Leads store unreachable: {e}"}]

    findings.append({"level": "info", "check": "lead-count",
                     "detail": f"{len(leads)} lead(s) on file"})

    for lead in leads:
        if not lead.get("name"):
            findings.append({"level": "medium", "check": "lead-integrity",
                             "detail": f"Lead #{lead.get('id')} has an empty name"})
        if lead.get("value") is not None and lead["value"] < 0:
            findings.append({"level": "medium", "check": "lead-integrity",
                             "detail": f"Lead #{lead.get('id')} has a negative value"})
    return findings


def audit_security(pin_gate) -> list[dict]:
    """Security-configuration checks."""
    findings = []
    pins = pin_gate.pins
    if not pins:
        findings.append({"level": "critical", "check": "pin-configured",
                         "detail": "No PIN configured — auth is effectively disabled"})
    else:
        weak = [p for p in pins if len(p) < 4]
        if weak:
            findings.append({"level": "high", "check": "pin-strength",
                             "detail": f"Short PIN(s): {', '.join(weak)}"})
        findings.append({"level": "info", "check": "pin-configured",
                         "detail": f"{len(pins)} PIN(s) configured"})

    if getattr(pin_gate, "rate_limit", 0) <= 0:
        findings.append({"level": "high", "check": "rate-limiting",
                         "detail": "Rate limiting disabled"})
    else:
        findings.append({"level": "info", "check": "rate-limiting",
                         "detail": f"Rate limit {pin_gate.rate_limit} attempts / {pin_gate.rate_window}s"})
    return findings


def run_audit(store, pin_gate) -> dict[str, Any]:
    findings = audit_security(pin_gate) + audit_leads(store)

    levels = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
    worst = max((levels.get(f["level"], 0) for f in findings), default=0)

    status = "PASS" if worst <= 1 else "WARN" if worst <= 3 else "FAIL"

    return {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": len(findings),
            "critical": sum(1 for f in findings if f["level"] == "critical"),
            "high": sum(1 for f in findings if f["level"] == "high"),
            "medium": sum(1 for f in findings if f["level"] == "medium"),
            "low": sum(1 for f in findings if f["level"] == "low"),
        },
        "findings": findings,
    }


if __name__ == "__main__":
    import json
    from jarvis_core import LeadsStore, PinGate
    result = run_audit(LeadsStore(), PinGate())
    print(json.dumps(result, indent=2))
