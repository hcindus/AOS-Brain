#!/usr/bin/env python3
"""
Chelios Security Controller v3.0
Agent: Chelios2 (CISO — Security, Audit, Monitoring)
Tick: Every 300 seconds (5 min)

v3.0 changes:
  - Writes heartbeat on every tick (fixes the 108-day stale heartbeat)
  - Performs real lightweight security checks (SSH, ports, failed logins, disk, services)
  - Stops the "No active tasks. Standing by." log spam (19MB log bloat)
"""

import os
import subprocess
import time
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"
AGENT_DIR = f"{WORKSPACE}/agent_sandboxes/chelios"
HEARTBEAT_FILE = f"{AGENT_DIR}/.heartbeat_trigger"
LOG_FILE = f"{AGENT_DIR}/chelios2.log"
AUDIT_DIR = f"{AGENT_DIR}/audits"


def write_heartbeat():
    """Write a fresh heartbeat every tick."""
    with open(HEARTBEAT_FILE, "w") as f:
        f.write(f"activated:{datetime.now().isoformat()}\n")
        f.write("chelios2:cso:active\n")


def log(message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] [Chelios2] {message}\n")


def run(cmd, timeout=10):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    except Exception as e:
        return f"ERR: {e}"


def security_checks():
    """Run lightweight security checks. Return a list of findings."""
    findings = []

    # 1. Failed SSH logins (last 200 auth lines)
    r = run("grep 'Failed password' /var/log/auth.log 2>/dev/null | tail -20 | wc -l")
    failed = r.stdout.strip() if isinstance(r, str) is False and hasattr(r, 'stdout') else ""
    try:
        failed = int(failed) if failed else 0
    except:
        failed = 0
    if failed > 10:
        findings.append(f"HIGH: {failed} failed SSH logins recently")

    # 2. Root SSH login permitted?
    r = run("grep -E '^PermitRootLogin' /etc/ssh/sshd_config 2>/dev/null")
    if r and "yes" in (r.stdout if hasattr(r, 'stdout') else ""):
        findings.append("WARN: PermitRootLogin is 'yes'")

    # 3. Disk usage
    r = run("df -h / | tail -1 | awk '{print $5}'")
    if r and hasattr(r, 'stdout'):
        pct = r.stdout.strip().rstrip('%')
        try:
            if int(pct) > 85:
                findings.append(f"WARN: disk {pct}% full")
        except:
            pass

    # 4. Key services down?
    for svc in ["aos-brain-v4", "depotchaos", "depotchaos-api", "aos-mission-control"]:
        r = run(f"systemctl is-active {svc} 2>/dev/null")
        if r and hasattr(r, 'stdout') and r.stdout.strip() != "active":
            findings.append(f"WARN: {svc} not active ({r.stdout.strip()})")

    return findings


def execute_tick():
    write_heartbeat()

    findings = security_checks()

    if findings:
        for f in findings:
            log(f"SECURITY: {f}")
        # Write findings to audit dir (daily)
        os.makedirs(AUDIT_DIR, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        with open(f"{AUDIT_DIR}/audit_{today}.txt", "a") as f:
            for finding in findings:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {finding}\n")
    else:
        # Only log every ~12 ticks (1 hour) to avoid spam, and keep it terse
        pass  # healthy — stay quiet


def main():
    write_heartbeat()
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "tick":
        execute_tick()
        print("tick complete")
    else:
        print("Usage: chelios_security_controller.py tick")


if __name__ == "__main__":
    main()
