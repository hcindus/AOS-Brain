"""Legal department activities — Redactor (compliance) + Velum (privacy/GDPR)."""
import subprocess
import os
from datetime import datetime, timezone
from temporalio import activity

LEGAL_DIR = "/root/.openclaw/workspace/aocros/legal"
REDACTOR_MODEL = "qwen2.5:14b"      # compliance analysis
VELUM_MODEL = "nous-hermes2"        # privacy / GDPR

# Documentation inventory (AGI Company + psdepot.com)
GOVERNANCE_DOCS = [
    "/root/.openclaw/workspace/AGI_COMPANY/corporate/CHARTER.md",
    "/root/.openclaw/workspace/AGI_COMPANY/corporate/BYLAWS.md",
    "/root/.openclaw/workspace/aocros/corporate/COMPANY_HANDBOOK.md",
    "/root/.openclaw/workspace/aocros/corporate/COMPLIANCE_TRACKER.md",
    "/root/.openclaw/workspace/aocros/corporate/handbook/employee-executive-governance-handbook.md",
]
SOP_DIR = "/root/.openclaw/workspace/psd/sops"
PRIVACY_DOCS = [
    "/root/.openclaw/workspace/aocros/corporate/COMPANY_HANDBOOK.md",
    "/root/.openclaw/workspace/aocros/legal/WEBSITE_LEGAL_DOCS_EXPANSION.md",
    "/root/.openclaw/workspace/aocros/legal/COMPLIANCE_RECERTIFICATION_2026.md",
]


def _ollama(model, prompt, timeout=400):
    env = dict(os.environ)
    env.setdefault("HOME", "/root")
    env.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")
    r = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True, timeout=timeout, env=env)
    return r.stdout.strip() or f"(empty — {r.stderr[:150]})"


def _read_docs(paths, max_chars=6000):
    out = []
    for p in paths:
        if os.path.isfile(p):
            try:
                txt = open(p).read()[:max_chars]
                out.append(f"### {os.path.basename(p)}\n{txt}")
            except Exception:
                pass
    return "\n\n".join(out)


def _list_sops():
    if not os.path.isdir(SOP_DIR):
        return "(no SOP dir)"
    return "\n".join("  - " + f for f in sorted(os.listdir(SOP_DIR)) if f.endswith(".md"))


@activity.defn
async def redactor_compliance_audit(month: str) -> str:
    """Redactor (Compliance Officer): monthly governance + SOP compliance audit."""
    docs = _read_docs(GOVERNANCE_DOCS)
    sops = _list_sops()
    prompt = ("You are Redactor, Compliance Officer for AGI Company / Performance Supply Depot LLC. "
              "Run a MONTHLY compliance audit. Review the governance documents and SOP inventory below. "
              "Produce a concise compliance report with: (1) Compliance status (PASS/ISSUES), "
              "(2) gaps or missing items, (3) recommended remediations, (4) priority ranking.\n\n"
              f"GOVERNANCE DOCS:\n{docs}\n\nSOP INVENTORY:\n{sops}")
    report = _ollama(REDACTOR_MODEL, prompt)

    os.makedirs(LEGAL_DIR, exist_ok=True)
    path = os.path.join(LEGAL_DIR, f"COMPLIANCE_REPORT_{month}.md")
    with open(path, "w") as f:
        f.write(f"# Compliance Report — {month}\n\n**Auditor:** Redactor (Compliance Officer)\n\n{report}\n")
    activity.logger.info(f"✅ Redactor compliance report -> {path}")
    return path


@activity.defn
async def velum_privacy_audit(month: str) -> str:
    """Velum (Data Privacy): monthly GDPR / privacy audit."""
    docs = _read_docs(PRIVACY_DOCS)
    prompt = ("You are Velum, Data Privacy officer for AGI Company / Performance Supply Depot LLC. "
              "Run a MONTHLY privacy / GDPR audit. Review the documents below. "
              "Produce a concise privacy report with: (1) privacy status (PASS/ISSUES), "
              "(2) data-handling / GDPR gaps, (3) recommended fixes, (4) priority.\n\n"
              f"DOCS:\n{docs}")
    report = _ollama(VELUM_MODEL, prompt)

    os.makedirs(LEGAL_DIR, exist_ok=True)
    path = os.path.join(LEGAL_DIR, f"PRIVACY_REPORT_{month}.md")
    with open(path, "w") as f:
        f.write(f"# Privacy / GDPR Report — {month}\n\n**Auditor:** Velum (Data Privacy)\n\n{report}\n")
    activity.logger.info(f"✅ Velum privacy report -> {path}")
    return path
