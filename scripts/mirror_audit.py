#!/usr/bin/env python3
"""
Mirror Audit — deterministic health check for the psdepot.com blue-green mirror.

Checks the symlink, both versions, nginx, and live HTTP endpoints, then emits a
structured PASS/WARN/FAIL report (same shape as JARVIS's audit.py). No AI in the
loop — this is a pure state check meant to be run by hand or via cron.

Structure under audit:
  /var/www/psdepot.com   -> symlink -> /var/www/psdepot-v0 | psdepot-v1
  /var/www/psdepot-v0/   live or standby
  /var/www/psdepot-v1/   live or standby
"""
import json
import os
import subprocess
from datetime import datetime

BASE = "/var/www"
LINK = f"{BASE}/psdepot.com"
VERSIONS = ["psdepot-v0", "psdepot-v1"]

# Key pages that must return 200 for the site to be considered "up".
CRITICAL_PATHS = [
    "/",
    "/locations.html",
    "/service-areas-map.html",
    "/products/72-100-cash-drawer.html",
]


def _http_code(url: str) -> int:
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", "10", url],
            capture_output=True, text=True, timeout=15,
        )
        return int(r.stdout.strip() or 0)
    except Exception:
        return 0


def _findings() -> list[dict]:
    findings = []

    # 1. Symlink exists and is a symlink
    if not os.path.islink(LINK):
        findings.append({"level": "critical", "check": "symlink",
                         "detail": f"{LINK} is not a symlink"})
        return findings  # can't meaningfully proceed

    target = os.readlink(LINK)
    findings.append({"level": "info", "check": "symlink",
                     "detail": f"{LINK} -> {target}"})

    # 2. Symlink target is a valid directory
    resolved = os.path.realpath(LINK)
    if not os.path.isdir(resolved):
        findings.append({"level": "critical", "check": "symlink-target",
                         "detail": f"symlink resolves to missing dir: {resolved}"})
        return findings
    findings.append({"level": "info", "check": "symlink-target",
                     "detail": f"live version is {os.path.basename(resolved)}"})

    # 3. Both versions exist
    for v in VERSIONS:
        p = f"{BASE}/{v}"
        if not os.path.isdir(p):
            findings.append({"level": "critical", "check": f"version-{v}",
                             "detail": f"{p} missing"})
        else:
            html = 0
            for root, _, files in os.walk(p):
                html += sum(1 for f in files if f.endswith(".html"))
            findings.append({"level": "info", "check": f"version-{v}",
                             "detail": f"{p} present ({html} html files)"})

    # 4. v0 and v1 have matching html counts (drift detection)
    counts = {}
    for v in VERSIONS:
        p = f"{BASE}/{v}"
        if os.path.isdir(p):
            counts[v] = sum(1 for root, _, files in os.walk(p)
                            for f in files if f.endswith(".html"))
    if len(counts) == 2 and counts["psdepot-v0"] != counts["psdepot-v1"]:
        findings.append({"level": "high", "check": "version-drift",
                         "detail": (f"v0={counts['psdepot-v0']} vs "
                                    f"v1={counts['psdepot-v1']} html files")})
    elif len(counts) == 2:
        findings.append({"level": "info", "check": "version-drift",
                         "detail": f"both versions have {counts['psdepot-v0']} html files"})

    # 5. nginx active
    try:
        active = subprocess.run(["systemctl", "is-active", "nginx"],
                                capture_output=True, text=True, timeout=10)
        if active.stdout.strip() == "active":
            findings.append({"level": "info", "check": "nginx",
                             "detail": "nginx is active"})
        else:
            findings.append({"level": "critical", "check": "nginx",
                             "detail": f"nginx is {active.stdout.strip()}"})
    except Exception as e:
        findings.append({"level": "critical", "check": "nginx",
                         "detail": f"could not check nginx: {e}"})

    # 6. Live HTTP endpoints
    for path in CRITICAL_PATHS:
        code = _http_code(f"https://psdepot.com{path}")
        if code == 200:
            findings.append({"level": "info", "check": f"http{path}",
                             "detail": "200 OK"})
        else:
            findings.append({"level": "critical", "check": f"http{path}",
                             "detail": f"returned {code}"})

    return findings


def run_audit() -> dict:
    findings = _findings()
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
    print(json.dumps(run_audit(), indent=2))
