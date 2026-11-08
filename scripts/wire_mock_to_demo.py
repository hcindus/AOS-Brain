#!/usr/bin/env python3
"""
Wire the mock CA_SOS scraper's synthetic output into the DEMO table.

The mock scraper (`scripts/ca_sos_scraper.js`) fabricates fake CA businesses and
dumps them to `data/PENDING_TASKS.json`. Per Captain's directive: synthetic data
feeds the DEMO table (`datadepot_intelligence_demo`), real data feeds the LIVE
table (`datadepot_intelligence` via sync_depotchaos_live.py). This script funnels
the mock's JSON into the DEMO table only — it NEVER touches the LIVE table.

Idempotent: uses entity_number + source as a dedupe key.
"""
import json
import os
import sqlite3
from datetime import datetime, timezone

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
QUEUE_FILE = "/root/.openclaw/workspace/data/PENDING_TASKS.json"
DEMO_TABLE = "datadepot_intelligence_demo"
SOURCE_TAG = "CA_SOS_MOCK"  # clearly synthetic, never confused with real CA_ABC


def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    try:
        with open(QUEUE_FILE) as f:
            data = json.load(f)
        return data.get("tasks", [])
    except (json.JSONDecodeError, AttributeError):
        return []


def main():
    tasks = load_queue()
    if not tasks:
        print("No tasks in PENDING_TASKS.json — nothing to sync.")
        return

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    inserted = 0
    skipped = 0
    for t in tasks:
        bname = t.get("company_name", "")
        ent = t.get("entity_number", "") or t.get("id", "")
        if not bname:
            skipped += 1
            continue

        # dedupe on entity_number + source
        c.execute(
            f"SELECT 1 FROM {DEMO_TABLE} WHERE license_number=? AND source=?",
            (ent, SOURCE_TAG),
        )
        if c.fetchone():
            skipped += 1
            continue

        data = json.dumps({
            "business_type": t.get("business_type", ""),
            "registration_date": t.get("registration_date", ""),
            "priority": t.get("priority", ""),
            "entity_number": ent,
            "mock": True,
        })
        c.execute(
            f"""INSERT INTO {DEMO_TABLE}
                (business_name, license_number, source, data, created_at, city,
                 state, license_status, issue_date)
                VALUES (?,?,?,?,?,?,?,?,?)""",
            (bname, ent, SOURCE_TAG, data, now, t.get("city", ""),
             t.get("state", "CA"), t.get("status", "Active"),
             t.get("registration_date", "")),
        )
        inserted += 1

    conn.commit()
    demo_count = c.execute(f"SELECT COUNT(*) FROM {DEMO_TABLE}").fetchone()[0]
    live_count = c.execute("SELECT COUNT(*) FROM datadepot_intelligence").fetchone()[0]
    conn.close()

    print(f"Inserted {inserted} synthetic rows → {DEMO_TABLE} (now {demo_count:,})")
    print(f"Skipped {skipped} (dupes / missing name)")
    print(f"LIVE table untouched: {live_count:,} rows")


if __name__ == "__main__":
    main()
