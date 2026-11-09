#!/usr/bin/env python3
"""
Submit 5 enriched food-service leads/day as LeadOutreachWorkflow to Temporal
(replaces the direct SMTP send — now durable/resumable).
"""
import asyncio, sqlite3, json
from temporalio.client import Client
from temporalio.workflow import WorkflowHandle

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
SUBMITTED = "/root/.openclaw/workspace/datadepot/data/submitted_leads.json"
TASK_QUEUE = "outreach-queue"

FOOD_TYPES = ("restaurant", "cafe", "bar", "seafood", "brewery", "pub", "coffee shop", "bakery", "taqueria")
SKIP = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud",
        "terrychico@sbcglobal.net", "coldpop.billing@gmail.com"}

PER_DAY = 5

def load(p, d):
    try: return json.load(open(p))
    except Exception: return d

def save(p, o):
    json.dump(o, open(p, "w"), indent=2)

async def main():
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    c = conn.cursor()
    q = ("SELECT id, name, email, phone, city, state, vendor_type FROM vendors "
         "WHERE data_class='real' AND email IS NOT NULL AND email != '' "
         "AND phone IS NOT NULL AND phone != '' "
         "AND (vendor_type IN (%s) OR lower(name) LIKE '%%cafe%%' OR lower(name) LIKE '%%coffee%%' "
         "OR lower(name) LIKE '%%taquer%%' OR lower(name) LIKE '%%baker%%') "
         "AND lower(email) NOT LIKE '%%example.com%%' "
         "ORDER BY state='CA' DESC, state, city" % ",".join("?"*len(FOOD_TYPES)))
    rows = c.execute(q, FOOD_TYPES).fetchall()
    conn.close()

    submitted = load(SUBMITTED, {})
    picks = []
    for r in rows:
        email = r["email"].strip().lower()
        if not email or "@" not in email or email in SKIP or submitted.get(email):
            continue
        picks.append(dict(r))
        if len(picks) >= PER_DAY:
            break

    if not picks:
        print("NO_NEW_LEADS")
        return

    client = await Client.connect("localhost:7233")
    n = 0
    for lead in picks:
        email = lead["email"].strip().lower()
        wf_id = f"outreach-{email}"
        await client.start_workflow(
            "LeadOutreachWorkflow",
            lead,
            id=wf_id,
            task_queue=TASK_QUEUE,
        )
        submitted[email] = True
        n += 1
        print(f"SUBMITTED {lead['name'][:30]} | {email}")

    save(SUBMITTED, submitted)
    print(f"SUBMITTED_TODAY={n}")

if __name__ == "__main__":
    asyncio.run(main())
