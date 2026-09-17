#!/usr/bin/env python3
"""
DepotChaos Intake Processor — auto-sync customer/account updates into the CRM.

Watches an inbox folder for structured intake files (JSON or pipe-delimited
lines) and upserts them into DepotChaos (unified.db -> leads table), marked as
customers. Runs headless on a cron so the Captain can drop a record without a
Miles round-trip.

Intake formats (either):
  1. JSON (single object or array) — most reliable.
  2. Pipe-delimited line, one record per line (see TEMPLATE.txt).

Canonical fields (all optional except business_name):
  business_name, email, phone, phone_alt, contact_name, contact_title,
  website, address, city, state, zip, amount, invoice, status, callback_date,
  notes

Usage:
  python3 depotchaos_intake.py process          # scan inbox, process all, archive
  python3 depotchaos_intake.py process --dry-run # report without writing
"""
import json, re, sqlite3, sys, os, shutil, datetime, glob

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
INBOX = "/root/.openclaw/workspace/data/depotchaos_intake/inbox"
PROCESSED = "/root/.openclaw/workspace/data/depotchaos_intake/processed"
FAILED = "/root/.openclaw/workspace/data/depotchaos_intake/failed"
LOG = "/root/.openclaw/workspace/data/depotchaos_intake/intake.log"

FIELDS = ["business_name", "email", "phone", "phone_alt", "contact_name",
          "contact_title", "website", "address", "city", "state", "zip",
          "amount", "invoice", "status", "callback_date", "notes"]

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper())).strip()

def log(msg):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def upsert(rec, con):
    """Upsert one record into leads. Returns ('updated'|'inserted', business_name)."""
    name = (rec.get("business_name") or "").strip()
    if not name:
        return ("skipped_empty", "")
    n = norm(name)
    cur = con.cursor()

    # find existing by normalized name
    cur.execute("SELECT id, business_name FROM leads WHERE deleted=0 AND business_name IS NOT NULL AND TRIM(business_name)!=''")
    existing = None
    for lid, bn in cur.fetchall():
        if norm(bn) == n:
            existing = (lid, bn)
            break

    # build contact notes for amount/invoice
    amount = rec.get("amount")
    invoice = rec.get("invoice")
    note_parts = []
    if amount:
        try:
            note_parts.append(f"Past due ${float(amount):,.2f}")
        except (TypeError, ValueError):
            note_parts.append(f"Amount: {amount}")
    if invoice:
        note_parts.append(f"(inv {invoice})")
    auto_note = " ".join(note_parts)
    custom_notes = (rec.get("notes") or "").strip()
    final_notes = custom_notes if custom_notes else auto_note

    cols = {
        "email": rec.get("email", ""),
        "phone": rec.get("phone", ""),
        "contact_name": rec.get("contact_name", ""),
        "contact_title": rec.get("contact_title", ""),
        "address": rec.get("address", ""),
        "city": rec.get("city", ""),
        "state": rec.get("state", ""),
        "zip": rec.get("zip", ""),
        "status": rec.get("status", "new"),
        "callback_date": rec.get("callback_date", ""),
    }

    if existing:
        lid = existing[0]
        sets = []
        vals = []
        for k, v in cols.items():
            if v:  # only overwrite with non-empty values
                sets.append(f"{k}=?")
                vals.append(v)
        if final_notes:
            sets.append("notes=?")
            vals.append(final_notes)
        sets.append("is_customer=1")
        sets.append("data_class=COALESCE(data_class,'ppos_pastdue')")
        if rec.get("status") == "contacted":
            sets.append("last_contact=?")
            vals.append(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"))
        if rec.get("callback_date"):
            sets.append("next_contact=?")
            vals.append(rec["callback_date"])
        cur.execute(f"UPDATE leads SET {', '.join(sets)} WHERE id=?", (*vals, lid))
        con.commit()
        return ("updated", existing[1])
    else:
        # insert
        today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        try:
            cur.execute("""INSERT INTO leads
                (business_name, email, phone, contact_name, contact_title, address,
                 city, state, zip, status, callback_date, notes, is_customer,
                 source_type, data_class, assigned_agent, created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,1,'depotchaos_intake','ppos_pastdue','Miles',?)""",
                (name, cols["email"], cols["phone"], cols["contact_name"],
                 cols["contact_title"], cols["address"], cols["city"], cols["state"],
                 cols["zip"], cols["status"], cols["callback_date"], final_notes, today))
            con.commit()
            return ("inserted", name)
        except sqlite3.IntegrityError:
            con.rollback()
            # name+city+state unique collision -> update by name
            cur.execute("""UPDATE leads SET is_customer=1, data_class='ppos_pastdue',
                notes=COALESCE(?,notes) WHERE business_name=?""", (final_notes, name))
            con.commit()
            return ("updated", name)

def parse_line(line):
    """Parse a pipe-delimited line into a record dict."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = [p.strip() for p in line.split("|")]
    rec = {}
    for i, f in enumerate(FIELDS):
        if i < len(parts):
            rec[f] = parts[i]
    return rec if rec.get("business_name") else None

def parse_file(path):
    records = []
    if path.endswith(".json"):
        data = json.load(open(path))
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = [data]
    else:
        for line in open(path):
            r = parse_line(line)
            if r:
                records.append(r)
    return records

def process(dry_run=False):
    os.makedirs(INBOX, exist_ok=True)
    os.makedirs(PROCESSED, exist_ok=True)
    os.makedirs(FAILED, exist_ok=True)
    files = sorted(glob.glob(os.path.join(INBOX, "*")))
    if not files:
        log("No intake files.")
        return
    con = sqlite3.connect(DB)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    for fp in files:
        base = os.path.basename(fp)
        try:
            records = parse_file(fp)
            if not records:
                log(f"[{base}] no records parsed.")
                shutil.move(fp, os.path.join(FAILED, f"{base}.{ts}"))
                continue
            for rec in records:
                if dry_run:
                    log(f"[DRY] would upsert: {rec.get('business_name')}")
                    continue
                action, name = upsert(rec, con)
                log(f"[{base}] {action}: {name}")
            if not dry_run:
                shutil.move(fp, os.path.join(PROCESSED, f"{base}.{ts}"))
        except Exception as e:
            log(f"[{base}] ERROR: {e}")
            try:
                shutil.move(fp, os.path.join(FAILED, f"{base}.{ts}"))
            except Exception:
                pass
    con.close()

if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry-run" in args
    if "process" in args:
        process(dry_run=dry)
    else:
        print(__doc__)
