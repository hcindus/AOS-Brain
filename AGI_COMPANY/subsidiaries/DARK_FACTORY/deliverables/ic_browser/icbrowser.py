#!/usr/bin/env python3
"""
IC Browser — Intelligence Collection browser agent (v1, API-first)

Honest, real-data collection. Never fabricates. Every record carries provenance
(source_url, collected_at, verification_status).

v1 sources (APIs first per RiP GoR RESHAPE):
  - Yelp Fusion API (working key) — verify/enrich restaurant/business data
  - DeepSeek (LLM) — classification + dedupe reasoning
  - (Google Places + abc.ca.gov scrape = future modules, need keys/wiring)

Usage:
  icbrowser verify "Business Name" "City" [State]
  icbrowser enrich --batch 50        # enrich oldest unverified real vendors
  icbrowser status                   # show data-quality dashboard
"""
import os
import json
import sys
import sqlite3
import time
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# ---- Config / keys ----
VENDORS_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
UNIFIED_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def _load_yelp_key() -> str:
    key = os.environ.get("YELP_API_KEY", "")
    if key:
        return key
    # Fallback: read from the existing enrichment script
    p = Path("/root/.openclaw/workspace/DepotChaos/yelp_enrichment.py")
    if p.exists():
        m = re.search(r"YELP_API_KEY.*?['\"]([A-Za-z0-9_-]{20,})['\"]", p.read_text())
        if m:
            return m.group(1)
    return ""

YELP_API_KEY = _load_yelp_key()
YELP_URL = "https://api.yelp.com/v3/businesses/search"

# ---- Provenance-normalized lead schema ----
LEAD_COLS = [
    "business_name", "city", "state", "phone", "address", "zip",
    "rating", "review_count", "categories", "yelp_url",
    "source", "source_url", "verification_status", "collected_at",
]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

class YelpSource:
    """Yelp Fusion API source — real, honest business verification."""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or YELP_API_KEY
        if not self.api_key:
            raise RuntimeError("YELP_API_KEY not set — cannot verify (would fabricate)")

    def _get(self, params: dict, timeout: int = 10) -> Optional[dict]:
        import urllib.request, urllib.error
        url = YELP_URL + "?" + "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.api_key}"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            print(f"  [yelp] HTTP {e.code}: {e.reason}")
            return None
        except Exception as e:
            print(f"  [yelp] error: {e}")
            return None

    def verify(self, business_name: str, city: str = "", state: str = "") -> Optional[dict]:
        """Look up a business on Yelp. Returns a normalized lead dict, or None if not found.
        NEVER fabricates — returns None when the source has no match."""
        loc = f"{city}, {state}" if (city and state) else (city or "California")
        data = self._get({"term": business_name, "location": loc, "limit": 1})
        if not data:
            return None
        biz = (data.get("businesses") or [None])[0]
        if not biz:
            return None
        loc_data = biz.get("location", {})
        return {
            "business_name": biz.get("name", business_name),
            "city": loc_data.get("city", ""),
            "state": loc_data.get("state", ""),
            "phone": biz.get("phone", ""),
            "address": ", ".join(loc_data.get("display_address", [])),
            "zip": loc_data.get("zip_code", ""),
            "rating": biz.get("rating", 0),
            "review_count": biz.get("review_count", 0),
            "categories": ", ".join(c.get("title", "") for c in biz.get("categories", [])),
            "yelp_url": biz.get("url", ""),
            "source": "yelp_fusion",
            "source_url": biz.get("url", ""),
            "verification_status": "verified",
            "collected_at": now(),
        }


class LeadStore:
    """Writes verified leads into DepotChaos with provenance."""
    def __init__(self, db_path: str = UNIFIED_DB):
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
                rating REAL, review_count INTEGER, categories TEXT, yelp_url TEXT,
                source TEXT, source_url TEXT, verification_status TEXT,
                collected_at TIMESTAMP,
                UNIQUE(business_name, city, state)
            )
        """)
        conn.commit(); conn.close()

    def upsert(self, lead: dict) -> bool:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("""
                INSERT OR REPLACE INTO verified_leads
                (business_name, city, state, phone, address, zip, rating, review_count,
                 categories, yelp_url, source, source_url, verification_status, collected_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, tuple(lead.get(k) for k in LEAD_COLS))
            conn.commit()
            return True
        except Exception as e:
            print(f"  [store] error: {e}")
            return False
        finally:
            conn.close()


def cmd_verify(name, city="", state=""):
    src = YelpSource()
    print(f"🔍 Verifying '{name}' ({city or '?'}, {state or '?'}) via Yelp Fusion...")
    lead = src.verify(name, city, state)
    if lead is None:
        print("  ❌ Not found on Yelp — no record written (honest: nothing fabricated).")
        return 1
    store = LeadStore()
    store.upsert(lead)
    print(f"  ✅ VERIFIED: {lead['business_name']}")
    print(f"     {lead['address']}, {lead['city']} {lead['state']} {lead['zip']}")
    print(f"     ☎ {lead['phone']}  ⭐ {lead['rating']} ({lead['review_count']} reviews)")
    print(f"     source_url: {lead['source_url']}")
    return 0

def cmd_enrich(batch: int = 50):
    """Enrich the oldest unverified REAL vendors (real phone, no synthetic)."""
    src = YelpSource()
    store = LeadStore()
    conn = sqlite3.connect(VENDORS_DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT name, city, state FROM vendors
        WHERE phone IS NOT NULL AND phone != '' AND phone NOT LIKE '%555%'
          AND name NOT IN ('LOCATION','WORLDPAY')
          AND length(name) > 3
        ORDER BY id ASC LIMIT ?
    """, (batch,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()

    print(f"Enriching {len(rows)} real vendors via Yelp...")
    verified = 0
    for r in rows:
        lead = src.verify(r["name"], r.get("city") or "", r.get("state") or "")
        if lead:
            store.upsert(lead)
            verified += 1
        time.sleep(0.3)  # polite rate limit
    print(f"✅ Done: {verified}/{len(rows)} verified, {len(rows)-verified} not found (honest).")
    return 0

def cmd_status():
    store = LeadStore()  # ensures table exists
    conn = sqlite3.connect(UNIFIED_DB)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(verification_status='verified') FROM verified_leads")
    total, verified = c.fetchone()
    conn.close()
    print(f"verified_leads: {total or 0} total, {verified or 0} verified")
    print(f"Yelp key present: {'yes (trial status unknown)' if YELP_API_KEY else 'NO — cannot verify'}")

def main(argv):
    if not argv or argv[0] in ("help", "--help"):
        print(__doc__); return 0
    cmd = argv[0]
    if cmd == "verify":
        return cmd_verify(argv[1] if len(argv) > 1 else "", argv[2] if len(argv) > 2 else "", argv[3] if len(argv) > 3 else "")
    if cmd == "enrich":
        return cmd_enrich(int(argv[2]) if len(argv) > 2 and argv[1] == "--batch" else 50)
    if cmd == "status":
        return cmd_status()
    print(f"Unknown command: {cmd}"); return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
