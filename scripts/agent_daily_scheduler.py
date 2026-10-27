#!/usr/bin/env python3
"""
Agent Daily Scheduler — puts agents on a daily task cycle so nothing goes stale.

Runs every day (cron 6:00 AM). For each active agent:
  1. Refreshes its PENDING_TASKS.md with today's date + status (no more months-stale files)
  2. Flags tasks approaching staleness (3-day early warning, not 7-day)
  3. Writes a "today's focus" so the agent knows what to address

Complements heartbeat_monitor.py (liveness) with a *task* cycle (work).
"""
import os
import json
from datetime import datetime, timezone
from pathlib import Path

SANDBOXES = "/root/.openclaw/workspace/agent_sandboxes"
LOG = "/var/log/aos/agent_daily_scheduler.log"

# Agents that are actually active (have a running controller → heartbeat fresh)
# We derive active agents by checking heartbeat freshness, not hardcoding.

def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    Path(LOG).parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")


def get_active_agents():
    """Agents whose heartbeat is fresh (< 1 day old) = actually running."""
    active = []
    for d in sorted(Path(SANDBOXES).iterdir()):
        if not d.is_dir():
            continue
        hb = d / ".heartbeat_trigger"
        if hb.exists():
            age_h = (datetime.now().timestamp() - hb.stat().st_mtime) / 3600
            if age_h < 24:
                active.append(d.name)
    return active


def refresh_pending_tasks(agent):
    """Rewrite the agent's PENDING_TASKS.md with a fresh timestamp + today's focus."""
    agent_dir = Path(SANDBOXES) / agent
    tasks_dir = agent_dir / "tasks"
    pt_file = agent_dir / "PENDING_TASKS.md"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Count pending tasks (md files in tasks/, excluding the scheduler itself)
    task_count = 0
    task_names = []
    if tasks_dir.exists():
        for tf in sorted(tasks_dir.glob("*.md")):
            age_days = (datetime.now().timestamp() - tf.stat().st_mtime) / 86400
            task_count += 1
            task_names.append((tf.stem, age_days))

    lines = [
        f"# PENDING_TASKS — {agent}",
        f"**Updated:** {today} (auto-refreshed by agent_daily_scheduler)",
        f"**Pending tasks:** {task_count}",
        "",
        "## Today's focus",
    ]
    if task_names:
        # Sort by age descending (oldest first = highest priority)
        task_names.sort(key=lambda x: -x[1])
        for name, age in task_names[:5]:
            flag = "🔴 STALE" if age > 7 else ("🟡 approaching" if age > 3 else "🟢 fresh")
            lines.append(f"- [ ] {name} ({age:.0f}d — {flag})")
    else:
        lines.append("- No pending tasks.")
    lines += [
        "",
        "## Schedule",
        "- Daily: this file auto-refreshes + tasks flagged before they go stale.",
        "- Heartbeat: runtime-emitted every 5 min (heartbeat_monitor.py).",
        "",
        "**Rule:** address any 🔴/🟡 task before it becomes a blocker.",
    ]

    pt_file.write_text("\n".join(lines) + "\n")
    return task_count


def main():
    log("=" * 50)
    log("Agent Daily Scheduler — running")
    active = get_active_agents()
    log(f"Active agents (fresh heartbeat): {active}")

    if not active:
        log("No active agents found — nothing to schedule")
        return

    for agent in active:
        n = refresh_pending_tasks(agent)
        log(f"  {agent}: PENDING_TASKS refreshed ({n} tasks)")

    log("Scheduler complete")


if __name__ == "__main__":
    main()
