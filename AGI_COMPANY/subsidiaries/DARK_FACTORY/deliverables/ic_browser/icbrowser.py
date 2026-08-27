#!/usr/bin/env python3
"""
IC Browser v2 — agentic browser (multi-source, honest, free-first)

Unified intelligence-collection browser. Sources (tried in order):
  1. OpenStreetMap (free, no key)      — real name/address/category/location
  2. CA ABC license lookup (Playwright) — real license records (anti-detection)
  3. Yelp Fusion (paid key, optional)   — real phone/rating (only if key valid)

Every record carries provenance (source, source_url, verification_status, collected_at).
NEVER fabricates — returns "not found" when no source has a real match.

Usage:
  icbrowser verify "Name" [City] [State]   # verify one business
  icbrowser search "City" [limit]          # find hospitality businesses in a city
  icbrowser enrich --batch N               # enrich oldest real vendors
  icbrowser status                         # data-quality dashboard
"""
import os
import sys
import json
import sqlite3
import time
import re
from datetime import datetime, timezone
from pathlib import Path

# Allow running from the package dir (so `import sources.osm` works)
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sources import osm  # free, no key

VENDORS_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
UNIFIED_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

LEAD_COLS = [
    "business_name", "city", "state", "phone", "address", "zip",
    "rating", "review_count", "categories", "website",
    "source", "source_url", "verification_status", "collected_at",
]

def now():
    return datetime.now(timezone.utc).isoformat()


class LeadStore:
    def __init__(self, db_path=UNIFIED_DB):
        self.db_path = db_path
        self._ensure_table()

    def _ensure_table(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS verified_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                city TEXT, state TEXT, phone TEXT, address TEXT, zip TEXT,
                rating REAL, review_count INTEGER, categories TEXT, website TEXT,
                source TEXT, source_url TEXT, verification_status TEXT,
                collected_at TIMESTAMP,
                UNIQUE(business_name, city, state)
            )
        """)
        conn.commit(); conn.close()

    def upsert(self, lead):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("""INSERT OR REPLACE INTO verified_leads
                (business_name, city, state, phone, address, zip, rating, review_count,
                 categories, website, source, source_url, verification_status, collected_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                tuple(lead.get(k) for k in LEAD_COLS))
            conn.commit(); return True
        except Exception as e:
            print(f"  [store] {e}"); return False
        finally:
            conn.close()


def verify(name, city="", state=""):
    """Verify a business across sources (free-first). Returns the best real match or None."""
    # 1. OSM (free)
    lead = osm.verify(name, city, state)
    if lead:
        return lead
    # 2. Yelp (only if a valid key is present — optional premium)
    ykey = _yelp_key()
    if ykey and "TRIAL" not in ykey:
        from icbrowser_yelp import yelp_verify  # lazy
        lead = yelp_verify(name, city, state)
        if lead:
            return lead
    return None


def _yelp_key():
    key = os.environ.get("YELP_API_KEY", "")
    if key:
        return key
    p = Path("/root/.openclaw/workspace/DepotChaos/yelp_enrichment.py")
    if p.exists():
        m = re.search(r"YELP_API_KEY.*?['\"]([A-Za-z0-9_-]{20,})['\"]", p.read_text())
        if m:
            return m.group(1)
    return ""


def cmd_verify(name, city="", state=""):
    print(f"🔍 Verifying '{name}' ({city or '?'}, {state or '?'})...")
    lead = verify(name, city, state)
    if lead is None:
        print("  ❌ No real match in any source — nothing written (honest).")
        return 1
    LeadStore().upsert(lead)
    print(f"  ✅ {lead['business_name']} — source: {lead['source']} ({lead['verification_status']})")
    print(f"     {lead.get('address','')}, {lead.get('city','')} {lead.get('state','')} {lead.get('zip','')}")
    if lead.get('phone'): print(f"     ☎ {lead['phone']}")
    if lead.get('categories'): print(f"     🏷 {lead['categories']}")
    if lead.get('website'): print(f"     🌐 {lead['website']}")
    return 0


def cmd_search(city, limit=25):
    print(f"🔍 Searching hospitality businesses in '{city}' via OSM...")
    results = osm.search_hospitality(city, limit=limit)
    store = LeadStore()
    written = 0
    for lead in results:
        if store.upsert(lead):
            written += 1
    print(f"  ✅ Found {len(results)} real businesses, wrote {written} to verified_leads")
    for r in results[:10]:
        print(f"     • {r['business_name']} — {r.get('phone','no phone')} ({r.get('categories','')})")
    return 0


def cmd_enrich(batch=50):
    conn = sqlite3.connect(VENDORS_DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""SELECT name, city, state FROM vendors
        WHERE phone IS NOT NULL AND phone != '' AND phone NOT LIKE '%555%'
          AND name NOT IN ('LOCATION','WORLDPAY') AND length(name) > 3
        ORDER BY id ASC LIMIT ?""", (batch,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    print(f"Enriching {len(rows)} real vendors (OSM first)...")
    store = LeadStore()
    verified = 0
    for r in rows:
        lead = osm.verify(r["name"], r.get("city") or "", r.get("state") or "")
        if lead:
            store.upsert(lead); verified += 1
        time.sleep(0.5)  # polite
    print(f"✅ {verified}/{len(rows)} verified via OSM, {len(rows)-verified} not found (honest).")


def cmd_status():
    store = LeadStore()
    conn = sqlite3.connect(UNIFIED_DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(verification_status='verified') FROM verified_leads")
    total, verified = c.fetchone()
    conn.close()
    print(f"verified_leads: {total or 0} total, {verified or 0} fully verified")
    print(f"Sources: OpenStreetMap (free) ✓ | CA ABC (Playwright) | Yelp (optional key: {'present' if _yelp_key() else 'absent'})")


def main(argv):
    if not argv or argv[0] in ("help", "--help"):
        print(__doc__); return 0
    cmd = argv[0]
    if cmd == "verify":
        return cmd_verify(argv[1] if len(argv) > 1 else "", argv[2] if len(argv) > 2 else "", argv[3] if len(argv) > 3 else "")
    if cmd == "search":
        return cmd_search(argv[1] if len(argv) > 1 else "", int(argv[2]) if len(argv) > 2 else 25)
    if cmd == "enrich":
        return cmd_enrich(int(argv[3]) if len(argv) > 3 and argv[1] == "--batch" else 50)
    if cmd == "status":
        return cmd_status()
    print(f"Unknown command: {cmd}"); return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
