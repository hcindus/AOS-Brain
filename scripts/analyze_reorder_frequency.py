#!/usr/bin/env python3
"""
Final cleanup + regenerate reorder frequency.
- Merge known multi-email identities (Travis, Betsy, 150 Pelican).
- Filter our own / placeholder addresses.
- Add Tomatina's 8 GM emails (4 have history, 4 are new contacts).
- Normalize noisy role-label names ("SUPPLY ONLY", "NCC", "Owner", "Manager", "GM").
- Recompute cadence with split-invoice guard (ignore <4-day gaps).
Outputs reorder_frequency.json (recurring + new contacts).
"""
import csv, json, statistics
from collections import defaultdict
from datetime import datetime, timedelta

CSV = "/root/.openclaw/media/inbound/invoices-export-20261109T2014---63cf980b-e227-4a3a-97ab-294293696cb7.csv"
OUT = "/root/.openclaw/workspace/datadepot/data/reorder_frequency.json"
TODAY = datetime(2026, 11, 9)

# canonical identity per email (merge multi-email humans / businesses)
ALIASES = {
    "terrychico@sbcglobal.net": "travis_hauffman",
    "coldpop.billing@gmail.com": "travis_hauffman",
    "betsy@itsitaliarestaurant.com": "betsy_delfiero",
    "delfierro@coastside.net": "betsy_delfiero",
    "accountspayable@150pelican.com": "pelican_150",
    "gm_tsc@tomatina.com": "tomatina_tsc",
    "gm_twc@tomatina.com": "tomatina_twc",
    "gm_tul@tomatina.com": "tomatina_tul",
    "gm_trv@tomatina.com": "tomatina_trv",
    "gm_twv@tomatina.com": "tomatina_twv",
    "chloe_frey@tomatina.com": "tomatina",
}
# skip our own / placeholder
SKIP_EMAILS = {"info@psdepot.com", "antonio.hudnall@gmail.com", "miles@myl0nr0s.cloud"}

# Tomatina full GM roster (8) — canonical key -> email + display
TOMATINA_GMS = {
    "tomatina_tal": "gm_tal@tomatina.com",
    "tomatina_tv":  "gm_tv@tomatina.com",
    "tomatina_tsm": "gm_tsm@tomatina.com",
    "tomatina_tsc": "gm_tsc@tomatina.com",
    "tomatina_tmv": "gm_tmv@tomatina.com",
    "tomatina_tul": "gm_tul@tomatina.com",
    "tomatina_twc": "gm_twc@tomatina.com",
    "tomatina_twv": "gm_twv@tomatina.com",
}

def clean_name(name):
    if not name:
        return ""
    for suffix in ("SUPPLY ONLY", "NCC", "ECR", "MAITRE'D", "GM", "Owner",
                   "Manager", "General Manager", "left msg", "open", "Cd @ 2 months",
                   "call back", "open store", "Manager Manager"):
        name = name.replace(suffix, " ")
    # collapse repeated roles and whitespace
    parts = [p for p in name.replace(",", " ").split() if p]
    return " ".join(parts).strip()

rows = []
with open(CSV, newline="", encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f):
        email = (r.get("Customer Email") or "").strip().lower()
        if not email or "@" not in email or email in SKIP_EMAILS:
            continue
        date_s = (r.get("Invoice Date") or "").strip()
        amt_s = (r.get("Amount Paid") or "").strip().replace("$", "").replace(",", "")
        try:
            d = datetime.strptime(date_s, "%Y-%m-%d")
        except Exception:
            continue
        key = ALIASES.get(email, email)
        rows.append({
            "key": key,
            "name": clean_name(r.get("Customer Name") or ""),
            "email": email,
            "phone": (r.get("Customer Phone") or "").strip(),
            "date": d,
            "amt": float(amt_s) if amt_s else 0.0,
        })

groups = defaultdict(list)
for r in rows:
    groups[r["key"]].append(r)

report = []
for key, invs in groups.items():
    invs.sort(key=lambda x: x["date"])
    dates = [i["date"] for i in invs]
    n = len(dates)
    # split-invoice guard: ignore gaps < 4 days (same order split)
    gaps = [(dates[i+1]-dates[i]).days for i in range(n-1)
            if (dates[i+1]-dates[i]).days >= 4]
    median_gap = statistics.median(gaps) if gaps else None
    last = dates[-1]
    total = sum(i["amt"] for i in invs)
    name = next((i["name"] for i in invs if i["name"]), key)
    email = next((i["email"] for i in invs if i["email"]), "")
    phone = next((i["phone"] for i in invs if i["phone"]), "")
    if median_gap:
        next_due = last + timedelta(days=int(round(median_gap)))
        days_overdue = (TODAY - next_due).days
    else:
        next_due = None
        days_overdue = None
    report.append({
        "key": key,
        "name": name,
        "email": email,
        "phone": phone,
        "orders": n,
        "first": dates[0].strftime("%Y-%m-%d"),
        "last": last.strftime("%Y-%m-%d"),
        "median_gap_days": int(round(median_gap)) if median_gap else None,
        "total_spent": round(total, 2),
        "next_due": next_due.strftime("%Y-%m-%d") if next_due else None,
        "days_overdue": days_overdue,
        "new_contact": False,
    })

# add Tomatina GMs missing from invoice history (new contacts, no cadence yet)
existing_keys = {x["key"] for x in report}
for key, email in TOMATINA_GMS.items():
    if key not in existing_keys:
        report.append({
            "key": key,
            "name": "Tomatina (GM)",
            "email": email,
            "phone": "",
            "orders": 0,
            "first": None,
            "last": None,
            "median_gap_days": None,
            "total_spent": 0.0,
            "next_due": None,
            "days_overdue": None,
            "new_contact": True,
        })

# sort: recurring (orders>=2 with gap) first, then new contacts
report.sort(key=lambda x: (
    not (x["orders"] >= 2 and x["median_gap_days"]),
    -(x["days_overdue"] or -99999),
))

with open(OUT, "w") as f:
    json.dump(report, f, indent=2)

recurring = [x for x in report if x["orders"] >= 2 and x["median_gap_days"]]
newc = [x for x in report if x["new_contact"]]
due = [x for x in recurring if x["days_overdue"] is not None and x["days_overdue"] >= 0]
print(f"TOTAL={len(report)}  RECURRING={len(recurring)}  DUE={len(due)}  NEW_CONTACTS={len(newc)}")
print("--- NEW CONTACTS (Tomatina GMs, no history) ---")
for x in newc:
    print(f"  {x['email']}")
