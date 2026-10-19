#!/usr/bin/env python3
"""
Runtime-emitted heartbeat monitor — writes fresh heartbeats for agents whose
controllers are actually running (honest reflection of liveness).

Runs every 5 min via cron. For each agent, checks for a live process and
writes/updates .heartbeat_trigger ONLY if the controller is running.
Agents with no process (event-driven / on-demand) correctly show no fresh
heartbeat — they're not "down", they're just not continuously ticking.
"""
import os
import subprocess
from datetime import datetime

SANDBOXES = "/root/.openclaw/workspace/agent_sandboxes"

# agent → process-match substring (from the controller's while-loop command)
AGENT_PROCESS = {
    "patricia": "patricia_factory_controller",
    "forge": "forge_factory_controller",
    "jordan": "jordan_office_controller",
    "chelios": "chelios_security_controller",
    "aurora": "aurora.log",  # aurora's bash loop writes to aurora.log
}


def is_running(substring: str) -> bool:
    try:
        r = subprocess.run(["pgrep", "-f", substring], capture_output=True, text=True)
        return bool(r.stdout.strip())
    except Exception:
        return False


def write_heartbeat(agent: str):
    path = os.path.join(SANDBOXES, agent, ".heartbeat_trigger")
    with open(path, "w") as f:
        f.write(f"activated:{datetime.now().isoformat()}\n")
        f.write(f"{agent}:runtime-emitted:active\n")


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for agent, pattern in AGENT_PROCESS.items():
        if is_running(pattern):
            write_heartbeat(agent)
            print(f"[{now}] {agent}: running → heartbeat updated")
        else:
            print(f"[{now}] {agent}: NOT running (no heartbeat written)")


if __name__ == "__main__":
    main()
