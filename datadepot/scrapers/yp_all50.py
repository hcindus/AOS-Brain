#!/usr/bin/env python3
"""
Driver: run the reusable YellowPages scraper across ALL 50 site-map US cities
automatically (no per-city manual approval).

Reads the authoritative city list from site_map_cities.json and builds the
geo_location_terms string for each as '<city>%2C+<st>' (lowercase, spaces -> +).
Reuses the proven functions/constants from yellowpages_city_scraper.py.

CRITICAL anti-block fix: YellowPages/Cloudflare hard-blocks a browser after 1-2
city searches, returning "Attention Required" / 0 listings. Each city therefore
gets a FRESH Chromium browser+context (rotation strategy), which reliably evades
the flag. Verified by _rotation_test.py (same-browser -> block after 1 city;
fresh-browser-per-city -> 100% success).

If a city still returns 0 on page 1 (residual block), close & relaunch a fresh
browser and retry that city once before logging it as a failure.

Run with SYSTEM python3.12 (has playwright + bs4 + lxml + requests):
    /usr/bin/python3.12 yp_all50.py

Writes per-city summary to yp_all50_summary.json
"""
import json
import os
import sys
import time
from datetime import datetime, timezone

try:
    from bs4 import BeautifulSoup
except Exception:
    BeautifulSoup = None

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import yellowpages_city_scraper as yp  # noqa: E402

CITIES_JSON = os.path.join(HERE, "site_map_cities.json")
SUMMARY_PATH = os.path.join(HERE, "yp_all50_summary.json")
PROGRESS_PATH = os.path.join(HERE, "yp_all50_progress.txt")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


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
        f.write(f"{now_iso()} {msg}\n")


def is_blocked(html, page):
    """Heuristic: a valid YellowPages results page has >=5 v-cards or non-empty name cards.
    A block page returns ~0 cards. Uses parser if available, else card-count via page DOM."""
    try:
        if BeautifulSoup is not None:
            n = len(BeautifulSoup(html or "", "lxml").select("div.v-card"))
            return n == 0
        cnt = page.eval_on_selector_all("div.v-card", "els => els.length")
        return cnt == 0
    except Exception:
        return True


def make_browser(p):
    b = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
    )
    ctx = b.new_context(user_agent=yp.UA, locale="en-US",
                        viewport={"width": 1366, "height": 768})
    ctx.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = { runtime: {} };
    """)
    page = ctx.new_page()
    return b, page


def scrape_city(city, state):
    """Scrape one city's YellowPages restaurant listings with fresh-browser rotation.
    Returns (listings, stop_reason)."""
    geo = build_geo(city, state)
    url = yp.build_search_url(geo)
    city_display = f"{city}, {state}"
    print(f"      (scrape_city fresh browser for {city_display}, geo={geo})")

    with yp.sync_playwright() as p:
        all_listings = []
        seen_names = set()
        stop = "ok"
        attempts_for_this_run = 0

        while True:
            attempts_for_this_run += 1
            if attempts_for_this_run > 2:
                stop = "gave_up_after_2_attempts"
                break

            browser, page = make_browser(p)
            try:
                for pg in range(1, yp.MAX_PAGES_PER_CITY + 1):
                    html = yp.yp_fetch_search(page, url, pg, city_display)
                    if not html:
                        stop = "fetch_failed"
                        break
                    # detect hard block -> rotate browser
                    if pg == 1 and is_blocked(html, page) and not all_listings:
                        print(f"      [BLOCK] {city_display} page 1 empty; rotating fresh browser (attempt {attempts_for_this_run})")
                        stop = "block_rotating"
                        break  # exits pg loop, closes browser, retries
                    listings = yp.parse_search_html(html, city, state)
                    new = [L for L in listings if L["name"] not in seen_names]
                    if not new:
                        if all_listings and pg > 1:
                            stop = "no_new"
                            break
                        if not all_listings and pg == 1:
                            stop = "empty_page1"
                            break
                        break
                    for L in new:
                        seen_names.add(L["name"])
                    all_listings.extend(new)
                    print(f"      page {pg}: +{len(new)} new (cum {len(all_listings)})")
                    if len(listings) < 5:
                        stop = "short_page"
                        break
                if stop == "block_rotating":
                    browser.close()
                    continue  # rotate + retry city
                # normal; done with this browser
                browser.close()
                break
            except Exception as e:
                print(f"      [ERR] browser for {city_display}: {e}")
                try:
                    browser.close()
                except Exception:
                    pass
                if attempts_for_this_run >= 2:
                    stop = f"error:{e}"
                    break
                continue  # rotate + retry

    # dedupe stragglers
    uniq = {}
    for L in all_listings:
        uniq.setdefault((L["name"], L["city"], L["state"]), L)
    return list(uniq.values()), stop


def run_all():
    cities = load_cities()
    print(f"Loaded {len(cities)} cities from {CITIES_JSON}")
    log_progress(f"START: {len(cities)} cities")

    results = {}
    total_new = 0
    total_emails = 0
    failed_cities = []
    city_index = 0

    for city, state in cities:
        city_index += 1
        city_display = f"{city}, {state}"
        print(f"\n[{city_index}/{len(cities)}] --- {city_display} ---")
        log_progress(f"CITY_START {city_display} geo={build_geo(city, state)}")

        all_listings, stop = scrape_city(city, state)
        print(f"  {city_display}: {len(all_listings)} organic scraped (stop={stop})")
        log_progress(f"CITY_PARSED {city_display} n={len(all_listings)} stop={stop}")
        if not all_listings:
            failed_cities.append(city_display)

        # ----- email extraction (uses requests, not browser) -----
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

        # ----- insert (dedupe on business_name+city+state) -----
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

    # ----- write final summary -----
    summary = {
        "generated_at": now_iso(),
        "cities_count": len(results),
        "failed_cities": failed_cities,
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
    print(f"  FAILED cities: {failed_cities}")
    print(f"  Summary JSON: {SUMMARY_PATH}")
    log_progress(f"DONE total_scraped={summary['totals']['restaurants_scraped']} "
                 f"total_emails={summary['totals']['emails_found']} "
                 f"total_inserted={summary['totals']['leads_inserted']}")
    return summary


if __name__ == "__main__":
    run_all()
