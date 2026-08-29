#!/usr/bin/env python3
"""
Driver: run the reusable YellowPages scraper across ALL 50 site-map US cities
automatically (no per-city manual approval).

Reads the authoritative city list from site_map_cities.json and builds the
geo_location_terms string for each as '<city>%2C+<st>' (lowercase, spaces -> +).
Reuses the proven functions/constants from yellowpages_city_scraper.py to avoid
duplicating parsing, email-extraction, or DB-insent logic.

Run with SYSTEM python3.12 (has playwright + bs4 + requests + lxml):
    /usr/bin/python3.12 yp_all50.py

Writes per-city summary to yp_all50_summary.json
"""
import json
import os
import sys
import time
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import yellowpages_city_scraper as yp  # noqa: E402

CITIES_JSON = os.path.join(HERE, "site_map_cities.json")
SUMMARY_PATH = os.path.join(HERE, "yp_all50_summary.json")
PROGRESS_PATH = os.path.join(HERE, "yp_all50_progress.txt")


def build_geo(city, state):
    """'Los Angeles' + 'CA' -> 'los+angeles%2C+ca' (lowercase, spaces -> +)."""
    c = city.strip().lower().replace(" ", "+")
    s = state.strip().lower()
    return f"{c}%2C+{s}"


def load_cities():
    with open(CITIES_JSON) as f:
        data = json.load(f)
    return [(c["name"], c["state"]) for c in data["cities"]]


def log_progress(msg):
    with open(PROGRESS_PATH, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} {msg}\n")


def run_all():
    cities = load_cities()
    print(f"Loaded {len(cities)} cities from {CITIES_JSON}")
    log_progress(f"START: {len(cities)} cities")

    results = {}
    total_new = 0
    total_emails = 0
    city_index = 0

    with yp.sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
        )
        ctx = browser.new_context(
            user_agent=yp.UA, locale="en-US",
            viewport={"width": 1366, "height": 768},
        )
        ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
        """)
        page = ctx.new_page()

        for city, state in cities:
            city_index += 1
            city_display = f"{city}, {state}"
            geo = build_geo(city, state)
            print(f"\n[{city_index}/{len(cities)}] --- {city_display} ---")
            log_progress(f"CITY_START {city_display} geo={geo}")

            url = yp.build_search_url(geo)
            all_listings = []
            seen_names = set()
            page_stop = "ok"
            try:
                for pg in range(1, yp.MAX_PAGES_PER_CITY + 1):
                    html = yp.yp_fetch_search(page, url, pg, city_display)
                    if not html:
                        page_stop = "fetch_failed"
                        break
                    listings = yp.parse_search_html(html, city, state)
                    new = [L for L in listings if L["name"] not in seen_names]
                    if not new:
                        if all_listings and pg > 1:
                            page_stop = "no_new"
                            break
                        if not all_listings and pg == 1:
                            page_stop = "empty_page1"
                            break
                        break
                    for L in new:
                        seen_names.add(L["name"])
                    all_listings.extend(new)
                    print(f"    page {pg}: +{len(new)} new (cum {len(all_listings)})")
                    if len(listings) < 5:
                        page_stop = "short_page"
                        break
            except Exception as e:
                print(f"    [ERR] browse {city_display}: {e}")
                page_stop = f"error:{e}"

            uniq = {}
            for L in all_listings:
                uniq.setdefault((L["name"], L["city"], L["state"]), L)
            all_listings = list(uniq.values())
            print(f"  {city_display}: {len(all_listings)} organic scraped (stop={page_stop})")
            log_progress(f"CITY_PARSED {city_display} n={len(all_listings)} stop={page_stop}")

            # email extraction
            email_count = 0
            for L in all_listings:
                if not L.get("website"):
                    continue
                try:
                    em = yp.extract_site_emails(L["website"])
                except Exception as e:
                    print(f"    [ERR] emails {L['name']}: {e}")
                    em = []
                if em:
                    L["email"] = em[0]
                    email_count += 1
            print(f"  {city_display}: {email_count}/{len(all_listings)} with emails")
            log_progress(f"CITY_EMAILS {city_display} emails={email_count}")

            # insert
            try:
                ins, skp = yp.insert_leads(all_listings)
            except Exception as e:
                print(f"    [ERR] insert {city_display}: {e}")
                ins, skp = 0, 0
            total_new += ins
            total_emails += email_count

            results[city_display] = {
                "scraped": len(all_listings),
                "emails": email_count,
                "inserted": ins,
                "skipped_dup_in_db": skp,
            }
            print(f"  {city_display}: inserted {ins}, dup-in-db {skp}")
            log_progress(f"CITY_DONE {city_display} ins={ins} skp={skp}")

        browser.close()

    # ----- write final summary -----
    summary = {
        "generated_at": datetime.utcnow().isoformat(),
        "cities_count": len(results),
        "totals": {
            "restaurants_scraped": sum(r["scraped"] for r in results.values()),
            "emails_found": total_emails,
            "leads_inserted": total_new,
            "dups_in_db": sum(r["skipped_dup_in_db"] for r in results.values()),
        },
        "per_city": results,
    }
    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    # ----- stdout summary -----
    print("\n" + "=" * 62)
    print("FINAL SUMMARY (all 50 cities)")
    print("=" * 62)
    for c, r in results.items():
        print(f"  {c}: {r['scraped']} scraped | {r['emails']} emails | "
              f"{r['inserted']} inserted | {r['skipped_dup_in_db']} dup")
    print("-" * 62)
    print(f"  TOTAL cities processed: {len(results)}")
    print(f"  TOTAL restaurants scraped: {summary['totals']['restaurants_scraped']}")
    print(f"  TOTAL emails found: {summary['totals']['emails_found']}")
    print(f"  TOTAL leads inserted: {summary['totals']['leads_inserted']}")
    print(f"  TOTAL dups-in-db: {summary['totals']['dups_in_db']}")
    print(f"  Summary JSON: {SUMMARY_PATH}")
    log_progress(f"DONE total_scraped={summary['totals']['restaurants_scraped']} "
                 f"total_emails={summary['totals']['emails_found']} "
                 f"total_inserted={summary['totals']['leads_inserted']}")
    return summary


if __name__ == "__main__":
    run_all()
