#!/usr/bin/env python3
import csv
from collections import defaultdict
from datetime import datetime

CSV = "/root/.openclaw/media/inbound/invoices-export-20261109T2047---7b180822-577c-4389-b64d-066d6b2b95a0.csv"
TODAY = datetime(2026, 11, 9)

rows = []
with open(CSV, newline="", encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        amt = float((r.get("Requested Amount") or "0").strip().replace("$", "").replace(",", "") or 0)
        paid = float((r.get("Amount Paid") or "0").strip().replace("$", "").replace(",", "") or 0)
        due_s = (r.get("Due Date") or "").strip()
        try:
            due = datetime.strptime(due_s, "%Y-%m-%d")
        except Exception:
            due = None
        rows.append({
            "name": (r.get("Customer Name") or "").strip(),
            "email": (r.get("Customer Email") or "").strip().lower(),
            "phone": (r.get("Customer Phone") or "").strip(),
            "inv": (r.get("Invoice ID") or "").strip(),
            "status": (r.get("Status") or "").strip(),
            "amount": amt,
            "paid": paid,
            "due": due,
        })

total = sum(r["amount"] for r in rows)
print(f"TOTAL_INVOICES={len(rows)}")
print(f"TOTAL_OUTSTANDING=${total:,.2f}")

# status breakdown
by_status = defaultdict(lambda: [0, 0.0])
for r in rows:
    by_status[r["status"]][0] += 1
    by_status[r["status"]][1] += r["amount"]
print("\n=== BY STATUS ===")
for s, (n, a) in sorted(by_status.items(), key=lambda x: -x[1][1]):
    print(f"  {s:12} {n:>3} inv  ${a:,.2f}")

# aging (overdue buckets) — only for Overdue
def aging(due):
    if not due:
        return "n/a"
    d = (TODAY - due).days
    if d <= 0:
        return "not-yet-due"
    if d <= 30:
        return "1-30d"
    if d <= 60:
        return "31-60d"
    if d <= 90:
        return "61-90d"
    return "90+d"

aging_buckets = defaultdict(lambda: [0, 0.0])
for r in rows:
    if r["status"] == "Overdue":
        b = aging(r["due"])
        aging_buckets[b][0] += 1
        aging_buckets[b][1] += r["amount"]
print("\n=== OVERDUE AGING ===")
order = ["1-30d", "31-60d", "61-90d", "90+d", "n/a"]
for b in order:
    if b in aging_buckets:
        n, a = aging_buckets[b]
        print(f"  {b:10} {n:>3} inv  ${a:,.2f}")

# top debtors (by customer, summed outstanding)
cust = defaultdict(lambda: [0.0, 0, ""])
for r in rows:
    key = r["email"] or r["name"]
    cust[key][0] += r["amount"]
    cust[key][1] += 1
    cust[key][2] = r["name"]

print("\n=== TOP DEBTORS ===")
for key, (a, n, name) in sorted(cust.items(), key=lambda x: -x[1][0])[:25]:
    print(f"  {name[:30]:30} {n:>2} inv  ${a:>10,.2f}   [{key[:35]}]")
