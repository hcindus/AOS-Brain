#!/usr/bin/env python3
"""
Dark Factory Triage Loop — Level 5 autonomy.

Scans specs/inbox/ for new spec files, triages each against mission.md
(accept/reject), auto-submits accepted specs to the Temporal Dark Factory
workflow, and files them into accepted/ or rejected/. No human in the loop.

Run every 30 minutes via the darkfactory-triage.timer systemd unit.
"""
import asyncio
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from temporalio.client import Client

BASE = Path(__file__).resolve().parent
INBOX = BASE / "specs" / "inbox"
ACCEPTED = BASE / "specs" / "accepted"
REJECTED = BASE / "specs" / "rejected"

# Scope — synced with mission.md (single source of truth).
ALLOWED_PRODUCTS = {"cobra_v1", "prometheus_v1", "CREAM", "ReggieStarr", "nognog", "nomad_probe"}
NON_GOAL_KEYWORDS = ["medical", "legal", "financial", "autonomous deploy", "production deploy"]

TEMPORAL_HOST = os.environ.get("TEMPORAL_HOST", "localhost:7233")
TASK_QUEUE = "darkfactory-queue"


def triage(spec: dict) -> tuple[bool, str]:
    """Accept/reject a spec against mission.md scope. Returns (accepted, reason)."""
    project = (spec.get("project_name") or "").strip()
    low = project.lower()

    for kw in NON_GOAL_KEYWORDS:
        if kw in low:
            return (False, f"out of scope: '{kw}' is a non-goal (mission.md)")
    if project not in ALLOWED_PRODUCTS:
        return (False, f"not in declared product line (mission.md GOALS)")
    return (True, "accepted")


def make_order(spec: dict):
    """Build a DarkFactoryOrder dict from a spec (mirrors the workflow dataclass)."""
    spec_id = spec.get("spec_id") or spec.get("id") or f"SPEC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    return {
        "order_id": spec_id,
        "project_name": spec.get("project_name"),
        "build_type": spec.get("build_type", "web"),
        "source_path": spec.get("source_path"),
        "priority": spec.get("priority", "normal"),
        "max_duration_minutes": int(spec.get("max_duration_minutes", 60)),
    }


async def run_once() -> dict:
    for d in (INBOX, ACCEPTED, REJECTED):
        d.mkdir(parents=True, exist_ok=True)

    specs = sorted(INBOX.glob("*.json"))
    if not specs:
        return {"scanned": 0, "accepted": 0, "rejected": 0, "note": "inbox empty"}

    from workflows.dark_factory import DarkFactoryWorkflow  # noqa: F401 (register)

    client = await Client.connect(TEMPORAL_HOST)
    stats = {"scanned": len(specs), "accepted": 0, "rejected": 0, "details": []}

    for spec_file in specs:
        try:
            spec = json.loads(spec_file.read_text())
        except Exception as e:
            shutil.move(str(spec_file), str(REJECTED / spec_file.name))
            stats["rejected"] += 1
            stats["details"].append({"file": spec_file.name, "reason": f"bad JSON: {e}"})
            continue

        accepted, reason = triage(spec)
        if not accepted:
            shutil.move(str(spec_file), str(REJECTED / spec_file.name))
            stats["rejected"] += 1
            stats["details"].append({"file": spec_file.name, "reason": reason})
            continue

        order = make_order(spec)
        # Fire-and-forget: queue the workflow, don't block the loop.
        handle = await client.start_workflow(
            DarkFactoryWorkflow.run,
            order,
            id=f"darkfactory-{order['order_id']}",
            task_queue=TASK_QUEUE,
        )
        shutil.move(str(spec_file), str(ACCEPTED / spec_file.name))
        stats["accepted"] += 1
        stats["details"].append({"file": spec_file.name, "workflow": handle.id, "reason": reason})

    return stats


async def main():
    result = await run_once()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
