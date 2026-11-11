#!/usr/bin/env python3
"""
Work the Mortimer Hwy4/680 phone leads.

Usage:
  python3 work_mortimer_leads.py next 10            # show next 10 to call
  python3 work_mortimer_leads.py called "Mai Thai"  # mark a lead as contacted
  python3 work_mortimer_leads.py note "Mai Thai" "left voicemail, will follow up Tue"
"""
import sqlite3, sys
from datetime import datetime, timezone

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
SOURCE = "mortimer-hwy4-680"


def con():
    return sqlite3.connect(DB)


def next_leads(n=10):
    c = con()
    cur = c.cursor()
    cur.execute("""SELECT id, name, phone, city, status FROM vendors
                   WHERE source_file=? AND status='new' AND (phone IS NOT NULL AND phone != '')
                   ORDER BY city, name LIMIT ?""", (SOURCE, n))
    rows = cur.fetchall()
    c.close()
    return rows


def mark_called(name, note=""):
    c = con()
    cur = c.cursor()
    cur.execute("SELECT id FROM vendors WHERE source_file=? AND name=? LIMIT 1", (SOURCE, name))
    r = cur.fetchone()
    if not r:
        # fuzzy match
        cur.execute("SELECT id, name FROM vendors WHERE source_file=? AND name LIKE ? LIMIT 5",
                    (SOURCE, f"%{name}%"))
        matches = cur.fetchall()
        if not matches:
            print(f"NO LEAD FOUND for '{name}'")
            c.close()
            return
        if len(matches) > 1:
            print("Multiple matches:")
            for mid, mname in matches:
                print(f"  {mid}: {mname}")
            c.close()
            return
        r = matches[0]
    vid = r[0]
    now = datetime.now(timezone.utc).isoformat()
    cur.execute("UPDATE vendors SET status='contacted', last_contact_at=? WHERE id=?", (now, vid))
    if note:
        cur.execute("UPDATE vendors SET notes = notes || '; contact: ' || ? WHERE id=?", (note, vid))
    c.commit()
    print(f"MARKED '{name}' (id {vid}) as contacted")
    c.close()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "next":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        for vid, name, phone, city, status in next_leads(n):
            print(f"{vid:6d}  {name[:32]:32s} {city[:12]:12s} {phone or '(no phone)'}")
    elif cmd == "called":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        note = sys.argv[3] if len(sys.argv) > 3 else ""
        mark_called(name, note)
    elif cmd == "note":
        name = sys.argv[2]
        note = " ".join(sys.argv[3:])
        c = con()
        cur = c.cursor()
        cur.execute("UPDATE vendors SET notes = notes || '; note: ' || ? WHERE source_file=? AND name=?",
                    (note, SOURCE, name))
        c.commit()
        print(f"NOTED '{name}'")
        c.close()


if __name__ == "__main__":
    main()
