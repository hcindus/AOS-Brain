#!/usr/bin/env python3
"""Query Temporal for ALL workflow status -> JSON for the psdepot.com status page."""
import asyncio, json
from collections import defaultdict
from datetime import datetime, timezone
from temporalio.client import Client

OUT = "/var/www/psdepot.com/temporal/status.json"

async def main():
    client = await Client.connect("localhost:7233")

    running = []
    failed = []
    completed = []
    by_type = defaultdict(lambda: {"running": 0, "failed": 0, "completed": 0})

    async for wf in client.list_workflows():
        wtype = str(getattr(wf, "workflow_type", "?"))
        st = wf.status.name
        rec = {
            "id": wf.id,
            "type": wtype,
            "status": st,
            "start": str(wf.start_time),
            "close": str(wf.close_time) if wf.close_time else None,
            "run_id": wf.run_id,
        }
        if st == "RUNNING":
            running.append(rec); by_type[wtype]["running"] += 1
        elif st in ("FAILED", "TIMED_OUT", "TERMINATED", "CANCELED"):
            failed.append(rec); by_type[wtype]["failed"] += 1
        else:
            completed.append(rec); by_type[wtype]["completed"] += 1

    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "running": len(running),
            "failed": len(failed),
            "completed": len(completed),
        },
        "by_type": {t: v for t, v in sorted(by_type.items())},
        "running": sorted(running, key=lambda x: x["type"])[:100],
        "failed": sorted(failed, key=lambda x: x["type"])[:200],
        "completed": sorted(completed, key=lambda x: x["type"])[:100],
    }

    json.dump(payload, open(OUT, "w"), indent=2)
    print(f"RUNNING={len(running)} FAILED={len(failed)} COMPLETED={len(completed)} TYPES={len(by_type)}")

if __name__ == "__main__":
    asyncio.run(main())
