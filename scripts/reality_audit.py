#!/usr/bin/env python3
"""
DepotChaos Reality Audit — separate REAL businesses from DEMO (synthetic) data.

Signals used (multi-factor, not just phone):
  1. Source (primary) — real import sources vs scraper generators
  2. Name pattern — synthetic templates ("XXX Corp", "OldXXX", "Bottle Shop", etc.)
  3. Area code validity — real NANP (201–989) vs fake (592, 999, etc.)
  4. Email — example.com / fake domains vs real

Output: adds `data_class` column ('real' | 'demo' | 'unknown') to vendors + leads.
Non-destructive — nothing deleted, both piles coexist.
"""
import sqlite3, re, sys

VENDORS_DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
UNIFIED_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# ---- Real sources (actual business data) ----
REAL_SOURCES = {
    "Teriyaki Madness Official", "Teriyaki Madness Franchise", "teriyaki_madness",
    "Mountain Mikes Franchise", "CREAM_RealEstate_Daily",
    "yp_directory", "yelp_directory", "LL_Hawaiian_Research",
    "msg657_Pendo", "Pendo", "client_list", "yelp_USA",
}

# ---- Demo/synthetic sources (scraper generators) ----
DEMO_SOURCES = {
    "CA_SOS_Scraper_V3", "CA_SOS_Scraper", "CA_SOS", "CA_ABC_Raw", "CA_ABC",
    "ABC License Data", "CA_ABC_Scraper", "web_scrape",
    "daily_scraper", "alaska_priority_scrape", "multi_state_scraper",
    "AGI_County_Leads_TX", "AGI_County_Leads_CA", "AGI_County_Leads",
    "CA_ALL_COUNTIES", "CA_northern_ca_restaurants",
}

# ---- Synthetic name patterns (scraper templates) ----
SYNTHETIC_NAME = [
    r"\bCorp$", r"\bCo \d+$", r"^Old", r"Management \d+$",
    r"Convenience Store Co \d+$", r"\bBottle Shop$", r"\bTavern Corp$",
    r"\bSaloon Corp$", r"\bLounge Co$", r"\bBar & Grill .* Co",
    r"TheClub .* Valley \d+$", r"^Place Group \d+", r"^House Group",
    r"^NewPlace \d+", r"^Grill San Diego", r"^Spot San Diego",
    r"^Grill$", r"^LOCATION$", r"^WORLDPAY",
    # multi_state_scraper: "<CityName> Restaurant" / "The <CityName> Bar & Grill"
    r"^(?:[A-Z][a-z]+ )?Restaurant$", r"^The [A-Z][a-z]+ Bar & Grill$",
]

# Valid NANP area codes: 200–989, excluding 9xx (9xx is reserved)
def valid_area_code(phone):
    if not phone:
        return False
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 10:
        return False
    # handle +1 prefix
    if digits.startswith("1") and len(digits) == 11:
        digits = digits[1:]
    ac = digits[:3]
    try:
        n = int(ac)
    except ValueError:
        return False
    # Valid: 200-989, but 9xx is reserved/unassigned; 0xx/1xx invalid
    return 200 <= n <= 898  # 899 is last "real" reserved-ish; keep 200-898 conservative


def is_fake_email(email):
    if not email:
        return False
    e = email.lower()
    return ("example" in e or "fake" in e or "test" in e or "noemail" in e or
            ".con" in e.split("@")[-1] or "abc@abc" in e)


def classify(name, source, phone, email):
    """Return 'real', 'demo', or 'unknown'."""
    name = (name or "").strip()
    source = (source or "").strip()
    phone = (phone or "").strip()
    email = (email or "").strip()

    # 1. Source is the strongest signal (prefix/substring match — sources carry date suffixes)
    if any(source.startswith(r) or r in source for r in REAL_SOURCES):
        return "real"
    if any(source.startswith(d) or d in source for d in DEMO_SOURCES):
        return "demo"

    # 2. Synthetic name pattern
    for pat in SYNTHETIC_NAME:
        if re.search(pat, name, re.IGNORECASE):
            return "demo"

    # 3. Fake area code or fake email = demo
    if phone and not valid_area_code(phone):
        return "demo"
    if email and is_fake_email(email):
        return "demo"

    # 4. Real-ish signals
    if source and ("franchise" in source.lower() or "directory" in source.lower()
                   or "official" in source.lower()):
        return "real"

    return "unknown"


def add_column_and_classify(db, table, name_col, source_col, phone_col, email_col):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # Add data_class column if not present
    cols = [r[1] for r in c.execute(f"PRAGMA table_info({table})").fetchall()]
    if "data_class" not in cols:
        c.execute(f"ALTER TABLE {table} ADD COLUMN data_class TEXT DEFAULT 'unknown'")
        print(f"  added data_class column to {table}")

    # Fetch all rows to classify
    c.execute(f"SELECT rowid, {name_col}, {source_col}, {phone_col}, {email_col} FROM {table}")
    rows = c.fetchall()

    stats = {"real": 0, "demo": 0, "unknown": 0}
    updates = []
    for rowid, name, source, phone, email in rows:
        cls = classify(name, source, phone, email)
        stats[cls] += 1
        updates.append((cls, rowid))

    # Batch update
    c.executemany(f"UPDATE {table} SET data_class=? WHERE rowid=?", updates)
    conn.commit()
    conn.close()
    return stats


if __name__ == "__main__":
    print("=" * 60)
    print("  DepotChaos Reality Audit — REAL vs DEMO separation")
    print("=" * 60)

    # vendors table
    print("\n[1/2] vendors table (depot_chaos.db)")
    vs = add_column_and_classify(VENDORS_DB, "vendors", "name", "source_file", "phone", "email")
    print(f"  real: {vs['real']:,} | demo: {vs['demo']:,} | unknown: {vs['unknown']:,}")

    # leads table
    print("\n[2/2] leads table (unified.db)")
    ls = add_column_and_classify(UNIFIED_DB, "leads", "business_name", "source_type", "phone", "email")
    print(f"  real: {ls['real']:,} | demo: {ls['demo']:,} | unknown: {ls['unknown']:,}")

    total_real = vs["real"] + ls["real"]
    total_demo = vs["demo"] + ls["demo"]
    print("\n" + "=" * 60)
    print(f"  TOTAL REAL businesses: {total_real:,}")
    print(f"  TOTAL DEMO (synthetic): {total_demo:,}")
    print("=" * 60)
