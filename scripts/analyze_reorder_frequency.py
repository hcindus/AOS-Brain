#!/usr/bin/env python3
"""
Paid-customer ORDER FREQUENCY analysis.
Groups every invoice by customer, computes reorder cadence (median days between
orders), predicts next reorder date, and flags who's "due" (past their cadence).
Outputs a report + a JSON for the reorder-reminder scheduler.
"""
import csv, json, statistics
from collections import defaultdict
from datetime import datetime, timedelta

CSV = "/root/.openclaw/media/inbound/invoices-export-20261109T2014---63cf980b-e227-4a3a-97ab-294293696cb7.csv"
OUT_JSON = "/root/.openclaw/workspace/datadepot/data/reorder_frequency.json"
OUT_CSV = "/root/.openclaw/workspace/datadepot/data/reorder_frequency.csv"
TODAY = datetime(2026, 11, 9)  # current date per session

# merge multiple emails into one canonical identity (same human/business)
EMAIL_ALIASES = {
    "terrychico@sbcglobal.net": "Travis Hauffman",
    "coldpop.billing@gmail.com": "Travis Hauffman",
    "betsy@itsitaliarestaurant.com": "Betsy Delfiero",
    "delfierro@coastside.net": "Betsy Delfiero",
    "saggu.am@gmail.com": "Sam Owner",
}

rows = []
with open(CSV, newline="", encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        email = (r.get("Customer Email") or "").strip().lower()
        name = (r.get("Customer Name") or "").strip()
        phone = (r.get("Customer Phone") or "").strip()
        date_s = (r.get("Invoice Date") or "").strip()
        amt_s = (r.get("Amount Paid") or "").strip().replace("$", "").replace(",", "")
        try:
            d = datetime.strptime(date_s, "%Y-%m-%d")
        except Exception:
            continue
        if not email or "@" not in email:
            # phone-only: key by phone
            key = f"PHONE:{phone}" if phone else f"NAME:{name}"
        else:
            key = EMAIL_ALIASES.get(email, email)
        rows.append({
            "key": key,
            "name": name,
            "email": email,
            "phone": phone,
            "date": d,
            "amt": float(amt_s) if amt_s else 0.0,
        })

# group by canonical key
groups = defaultdict(list)
for r in rows:
    groups[r["key"]].append(r)

report = []
for key, invs in groups.items():
    invs.sort(key=lambda x: x["date"])
    dates = [i["date"] for i in invs]
    n = len(dates)
    first = dates[0]
    last = dates[-1]
    gaps = [(dates[i+1] - dates[i]).days for i in range(n-1) if (dates[i+1]-dates[i]).days > 0]
    if gaps:
        median_gap = statistics.median(gaps)
    else:
        median_gap = None  # single order
    total = sum(i["amt"] for i in invs)
    # representative identity (prefer a non-empty name, first non-empty email)
    name = next((i["name"] for i in invs if i["name"]), key)
    email = next((i["email"] for i in invs if i["email"]), "")
    phone = next((i["phone"] for i in invs if i["phone"]), "")
    # predicted next reorder
    if median_gap:
        next_due = last + timedelta(days=int(round(median_gap)))
        days_overdue = (TODAY - next_due).days
    else:
        next_due = None
        days_overdue = None
    report.append({
        "name": name,
        "email": email,
        "phone": phone,
        "orders": n,
        "first": first.strftime("%Y-%m-%d"),
        "last": last.strftime("%Y-%m-%d"),
        "median_gap_days": int(round(median_gap)) if median_gap else None,
        "total_spent": round(total, 2),
        "next_due": next_due.strftime("%Y-%m-%d") if next_due else None,
        "days_overdue": days_overdue,
    })

# sort: recurring customers (2+ orders) first, then by days_overdue (most overdue first)
report.sort(key=lambda x: (x["orders"] < 2, -(x["days_overdue"] or -99999)))

# write JSON + CSV
with open(OUT_JSON, "w") as f:
    json.dump(report, f, indent=2)
with open(OUT_CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(report[0].keys()) if report else [])
    w.writeheader()
    w.writerows(report)

# print summary
recurring = [x for x in report if x["orders"] >= 2 and x["median_gap_days"]]
due = [x for x in recurring if x["days_overdue"] is not None and x["days_overdue"] >= 0]
print(f"TOTAL_IDENTITIES={len(report)}")
print(f"RECURRING={len(recurring)}")
print(f"DUE_FOR_REORDER={len(due)}")
print("\n=== TOP 30 RECURRING CUSTOMERS BY CADENCE ===")
print(f"{'Customer':28} {'Ord':>3} {'Gap(d)':>6} {'Last':>10} {'NextDue':>10} {'Overdue':>7} {'Total$':>9}")
for x in recurring[:30]:
    print(f"{x['name'][:28]:28} {x['orders']:>3} {x['median_gap_days']:>6} {x['last']:>10} {x['next_due']:>10} {str(x['days_overdue']):>7} {x['total_spent']:>9.0f}")
