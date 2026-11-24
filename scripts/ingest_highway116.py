#!/usr/bin/env python3
"""
Ingest Highway 116 restaurant directory into the phone_call_queue.json.

Parses highway116_restaurants.md (name/cuisine/address/phone/website tables +
bullet lists), extracts restaurants WITH a real 10-digit phone number, maps each
to its town, normalizes phone to digits, dedupes against the existing queue, and
appends new entries.

Run: python3 ingest_highway116.py [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

SRC = Path("/root/.openclaw/workspace/data/email_inbox/highway116_restaurants.md")
QUEUE = Path("/root/.openclaw/workspace/datadepot/data/phone_call_queue.json")

# town section headers "## N · TOWN ..." — map header slug -> city name
TOWN_ALIASES = {
    "jenner": "Jenner",
    "guerneville": "Guerneville",
    "forestville": "Forestville",
    "graton": "Graton",
    "sebastopol": "Sebastopol",
    "cotati": "Cotati",
    "rohnert": "Rohnert Park",
    "petaluma": "Petaluma",
}

PHONE_RE = re.compile(r"\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})")


def norm_phone(m):
    return "".join(m.groups())


def town_from_header(line):
    low = line.lower()
    for slug, city in TOWN_ALIASES.items():
        if slug in low:
            return city
    return None


def parse():
    lines = SRC.read_text().splitlines()
    city = None
    sub_city = None
    seen = {}  # name -> phone (dedupe)
    entries = []  # list of (name, phone, city)

    def add(name, phone):
        name = name.strip()
        if not name or len(name) < 2:
            return
        if name in seen:
            return
        seen[name] = phone
        c = sub_city or city
        entries.append({"name": name, "phone": phone, "city": c or ""})

    for raw in lines:
        line = raw.strip()

        # main town header
        if line.startswith("## ") and "·" in line:
            city = town_from_header(line)
            sub_city = None
            continue

        # sub-section header (e.g. "### Rohnert Park — restaurants & cafes")
        if line.startswith("### "):
            t = town_from_header(line)
            if t:
                sub_city = t
            else:
                sub_city = None
            continue

        # table rows
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not cells or cells[0] in ("Name", "---", ""):
                continue
            name = cells[0]
            # find phone in remaining cells
            for c in cells[1:]:
                m = PHONE_RE.search(c)
                if m and re.search(r"\d{3}", c):
                    add(name, norm_phone(m))
                    break
            continue

        # bullet lines: - **Name** — ... (phone) ... website
        if line.startswith("- "):
            mname = re.search(r"\*\*(.+?)\*\*", line)
            if not mname:
                continue
            name = mname.group(1).strip()
            # skip "chains" roll-up lines (no specific phone)
            mphone = PHONE_RE.search(line)
            if mphone:
                add(name, norm_phone(mphone))
            continue

    return entries


def main():
    dry = "--dry-run" in sys.argv
    entries = parse()
    # load existing queue
    try:
        queue = json.loads(QUEUE.read_text())
    except Exception:
        queue = []
    if not isinstance(queue, list):
        queue = []

    existing = {f"{q.get('name','').strip().lower()}|{q.get('phone','')}" for q in queue}
    existing_names = {q.get("name", "").strip().lower() for q in queue}

    added = 0
    for e in entries:
        key = f"{e['name'].lower()}|{e['phone']}"
        if key in existing:
            continue
        if e["name"].lower() in existing_names:
            continue  # same name already queued
        queue.append({"name": e["name"], "phone": e["phone"], "city": e["city"], "email": ""})
        added += 1

    print(f"parsed entries with phone: {len(entries)}")
    print(f"new to add: {added}")
    print(f"existing queue size: {len(queue) - added} -> new total: {len(queue)}")

    if not dry and added:
        QUEUE.write_text(json.dumps(queue, indent=2))
        print(f"WROTE {QUEUE}")

    # show city breakdown of additions
    from collections import Counter
    cnt = Counter(e["city"] for e in entries)
    print("city breakdown (with-phone):", dict(cnt))


if __name__ == "__main__":
    main()
