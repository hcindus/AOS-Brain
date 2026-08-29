#!/usr/bin/env python3
"""
Reusable YellowPages restaurant-prospecting scraper for the DataDepot/DepotChaos lead pipeline.

Scrapes YellowPages restaurant listings for one or more cities, extracts contact emails
from each restaurant's own website + contact page, and inserts leads into the DepotChaos
'unified.db' leads table.

Usage (run with SYSTEM python3.12 which has playwright+bs4+requests):
    /usr/bin/python3.12 yellowpages_city_scraper.py

Config below controls target cities. Change the GEO list to target any city.
Endpoint pattern:
    https://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=<city>%2C+<state>

YellowPages sits behind aggressive Cloudflare anti-bot protection, so this uses Playwright
(a real Chromium) to load search pages. Individual restaurant websites are fetched with
`requests` (fast; restaurant sites are rarely Cloudflare-gated).

Summary report is printed per city (restaurants scraped, emails found) and a JSON snapshot
is written alongside this script.
"""
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# Target cities: (city, state, geo_location_terms value)
#   geo param uses  city + %2C + lowercase state (e.g. "petaluma%2C+ca")
GEO = [
    ("Petaluma",    "CA", "petaluma%2C+ca"),
    ("Napa",        "CA", "napa%2C+ca"),
    ("Sebastopol",  "CA", "sebastopol%2C+ca"),
    ("Healdsburg",  "CA", "healdsburg%2C+ca"),
    ("Rohnert Park","CA", "rohnert+park%2C+ca"),
]

SEARCH_TERMS = "restaurants"
SOURCE = "YellowPages"
SOURCE_TYPE = "yp_directory"
STATUS = "new"
ASSIGNED_DEPT = "datadepot_sales"

# Politeness / limits
MAX_PAGES_PER_CITY = 8           # each page = ~30 results
YP_PAGE_DELAY = 3.0              # seconds between YP search-page fetches (via playwright, gentle)
SITE_DELAY = 0.35                # seconds between restaurant-website HTTP fetches
FETCH_TIMEOUT = 12               # seconds for website fetches

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Junk / provider / platform domains to drop from extracted emails.
JUNK_DOMAINS = {
    "sentry.io", "wixpress.com", "example.com", "schema.org", "s3.amazonaws.com",
    "cloudinary.com", "wix.com", "squarespace.com", "godaddy.com", "w3.org",
    "doubleclick.net", "google.com", "gstatic.com", "googleapis.com",
    "googletagmanager.com", "facebook.com", "instagram.com", "yelp.com",
    "tripadvisor.com", "grubhub.com", "doordash.com", "ubereats.com",
    "opentable.com", "toasttab.com", "squareup.com", "square.site", "clover.com",
    "gravatar.com", "twimg.com", "cdn.shopify.com", "pinterest.com", "linkedin.com",
    "twitter.com", "x.com", "wixstatic.com", "sndcdn.com", "kwickpos.com",
    "posupgrades.com", "positouch.com", "micros.com", "oracle.com", "ncr.com",
    "lightspeed.com", "touchbistro.com", "revelsystems.com", "upserve.com",
    "emenuplus.com", "zoho.com", "mailchimp.com", "constantcontact.com",
    "hubspot.com", "hotjar.com", "mouseflow.com", "capterra.com", "websitesforrestaurants.com",
    "gotowebinar.com", "eventsforce.net", "typeform.com", "survey.monkey.com",
    "ymlp.com", "campaignmonitor.com", "sendinblue.com", "brevo.com", "klaviyo.com",
    "fonts.googleapis.com", "google-analytics.com", "schema.org", "localedge.com",
    "weebly.com", "flip.to", "resdiary.com", "openTable.com", "olo.com",
    "chinatownconnection.com", "menupages.com", "yext.com", "birdeye.com",
}

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
ADDR_RE = re.compile(r"^\s*(.*?),\s*([A-Za-z]{2})\s+(\d{5}(?:-\d{4})?)", re.I)
CONTACT_HINT = ("contact", "about", "location", "info", "hours", "reserv", "menu")
SUFFIXES = ["/contact", "/contact-us", "/about", "/contact.html"]


def clean(t):
    return re.sub(r"\s+", " ", (t or "")).strip()


def emails_from_text(text):
    """Return de-duplicated, junk-filtered real email addresses found in HTML text."""
    out = set()
    for e in EMAIL_RE.findall(text or ""):
        e = e.strip().strip(".").lower()
        if not e or "@" not in e:
            continue
        if e.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".css", ".js")):
            continue
        dom = e.split("@")[-1]
        if not re.match(r"^[a-z0-9\-]+(\.[a-z0-9\-]+)*\.(com|net|org|co|io|us|ca|biz|info)$", dom):
            continue
        if dom in JUNK_DOMAINS or any(d in dom for d in JUNK_DOMAINS):
            continue
        out.add(e)
    return out


# ---------------------------------------------------------------------------
# YELLOWPAGES SCRAPING (Playwright - Cloudflare bypass)
# ---------------------------------------------------------------------------
def yp_fetch_search(page, base_url, page_num, city_display):
    """Fetch a YellowPages search page via Playwright; return raw HTML or None."""
    url = base_url
    if page_num > 1:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}page={page_num}"
    try:
        page.goto(url, timeout=45000, wait_until="domcontentloaded")
        time.sleep(YP_PAGE_DELAY)
        title = page.title() or ""
        html = page.content()
        if "cloudflare" in title.lower() or "attention required" in title.lower():
            print(f"    [!] Cloudflare block on {city_display} page {page_num}; retrying once...")
            time.sleep(6)
            page.goto(url, timeout=45000, wait_until="domcontentloaded")
            time.sleep(YP_PAGE_DELAY)
            html = page.content()
        return html
    except Exception as e:
        print(f"    [ERR] yp fetch page {page_num}: {e}")
        return None


def parse_search_html(html, default_city, default_state):
    """Parse a YellowPages search page into listing dicts (organic only, no ads)."""
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("div.v-card")
    listings = []
    seen = set()
    for card in cards:
        if card.select_one("span.ad-pill"):
            continue  # skip paid ads
        name_a = card.select_one("a.business-name")
        if not name_a:
            continue
        name = clean(name_a.get_text())
        if not name or name in seen:
            continue
        seen.add(name)
        cats = [clean(a.get_text()) for a in card.select("div.categories a")]
        site = None
        for a in card.select("div.links a"):
            if "website" in a.get_text().strip().lower():
                site = a.get("href")
                break
        phone = None
        pe = card.select_one("div.phones.phone.primary") or card.select_one("div.phone")
        if pe:
            phone = clean(pe.get_text())
        street = city = state = zipc = None
        adr = card.select_one("div.adr")
        if adr:
            se = adr.select_one("div.street-address")
            if se:
                street = clean(se.get_text())
            le = adr.select_one("div.locality")
            if le:
                m = ADDR_RE.match(clean(le.get_text()))
                if m:
                    city, state, zipc = m.group(1), m.group(2), m.group(3)
        listing = {
            "name": name,
            "phone": phone,
            "street": street,
            "city": city or default_city,
            "state": state or default_state,
            "zip": zipc or "",
            "categories": cats,
            "website": site,
        }
        listings.append(listing)
    return listings


# ---------------------------------------------------------------------------
# EMAIL EXTRACTION FROM RESTAURANT WEBSITES
# ---------------------------------------------------------------------------
def http_get(url):
    try:
        r = requests.get(url, timeout=FETCH_TIMEOUT, allow_redirects=True,
                         headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return ""


def extract_site_emails(base_url):
    """Follow the pattern from santa_rosa_deep.py: fetch homepage, then contact-ish
    internal links + standard suffixes, collect real emails."""
    emails = set()
    pages = [base_url]
    try:
        base_netloc = urlparse(base_url).netloc.lower().replace("www.", "")
    except Exception:
        base_netloc = ""

    home = http_get(base_url)
    if home:
        emails.update(emails_from_text(home))
        # mailto links on home
        for m in re.findall(r"mailto:\s*([^\"'\s>?]+)", home):
            e = m.strip().lower()
            if "@" in e:
                emails.add(e)
        # internal links
        links = set()
        for m in re.findall(r'href=["\']([^"\']+)["\']', home):
            url = urljoin(base_url, m)
            u = urlparse(url)
            if u.scheme in ("http", "https") and u.netloc.replace("www.", "").lower() == base_netloc:
                if any(k in m.lower() for k in CONTACT_HINT):
                    links.add(url)
        for l in list(links)[:8]:
            pages.append(l)
    # standard suffixes
    for suf in SUFFIXES:
        pages.append(urljoin(base_url, suf))

    seen = set()
    for p in pages:
        if p.split("?")[0] in seen:
            continue
        seen.add(p.split("?")[0])
        t = http_get(p)
        if t:
            emails.update(emails_from_text(t))
            for m in re.findall(r"mailto:\s*([^\"'\s>?]+)", t):
                e = m.strip().lower()
                if "@" in e:
                    emails.add(e)
        time.sleep(SITE_DELAY)

    # Prefer emails on the site's own domain; keep others only if domain looks legit.
    final = set()
    for e in emails:
        dom = e.split("@")[-1].replace("www.", "").lower()
        if base_netloc and base_netloc.split(".")[0] in dom:
            final.add(e)  # own-domain email: highest confidence
        elif dom not in ("gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
                         "mac.com", "icloud.com", "me.com", "comcast.net", "verizon.net",
                         "sbcglobal.net", "att.net", "msn.com", "live.com"):
            final.add(e)
    return sorted(final)


# ---------------------------------------------------------------------------
# DB INSERT
# ---------------------------------------------------------------------------
def insert_leads(listings):
    """Insert scraped listings into leads table, deduping on (business_name, city, state)."""
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    inserted = skipped = 0
    for L in listings:
        cur.execute(
            "SELECT id FROM leads WHERE business_name = ? AND city = ? AND state = ?",
            (L["name"], L["city"], L["state"]),
        )
        if cur.fetchone():
            skipped += 1
            continue
        cat = ", ".join(L.get("categories") or []) or "Restaurant"
        btype = "restaurant"
        address = L.get("street") or ""
        website = L.get("website") or ""
        email = L.get("email") or ""
        notes = None
        if website:
            notes = f"Website: {website}"
        if email and website:
            notes = f"Website: {website} | Email: {email}"
        cur.execute(
            """INSERT INTO leads (
                business_name, city, state, zip, phone, email, category, business_type,
                address, source, source_type, status, priority, tier, tags, assigned_dept,
                notes, created_at, deleted, is_customer
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                L["name"], L["city"], L["state"], L.get("zip") or "", L.get("phone") or "",
                email, cat, btype, address, SOURCE, SOURCE_TYPE, STATUS, "normal", None,
                f"{L['city'].lower().replace(' ','-')},restaurant", ASSIGNED_DEPT,
                notes, now, 0, 0,
            ),
        )
        inserted += 1
    conn.commit()
    conn.close()
    return inserted, skipped


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def build_search_url(city_geo):
    return (f"https://www.yellowpages.com/search?search_terms={SEARCH_TERMS}"
            f"&geo_location_terms={city_geo}")


def run():
    print("=" * 62)
    print("YELLOWPAGES RESTAURANT PROSPECTING SCRAPER")
    print("=" * 62)

    results = {}          # city -> {"scraped": n, "emails": n, "listings": [...]}
    all_new = 0
    all_emails = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
        )
        ctx = browser.new_context(
            user_agent=UA, locale="en-US",
            viewport={"width": 1366, "height": 768},
        )
        ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
        """)
        page = ctx.new_page()

        for city, state, geo in GEO:
            city_display = f"{city}, {state}"
            print(f"\n--- {city_display} ---")
            url = build_search_url(geo)
            all_listings = []
            seen_names = set()
            for pg in range(1, MAX_PAGES_PER_CITY + 1):
                html = yp_fetch_search(page, url, pg, city_display)
                if not html:
                    break
                listings = parse_search_html(html, city, state)
                new = [L for L in listings if L["name"] not in seen_names]
                if not new:
                    # If we got listings but all already seen and this is page>1, stop
                    if all_listings and pg > 1:
                        break
                    if not all_listings and pg == 1:
                        # page 1 gave nothing -> likely failed; stop
                        break
                    break
                for L in new:
                    seen_names.add(L["name"])
                all_listings.extend(new)
                print(f"    page {pg}: +{len(new)} new (cumulative {len(all_listings)})")
                # stop early if page returned fewer than a full page
                if len(listings) < 5:
                    break

            # De-duplicate any stragglers
            uniq = {}
            for L in all_listings:
                uniq.setdefault((L["name"], L["city"], L["state"]), L)
            all_listings = list(uniq.values())
            print(f"  {city_display}: {len(all_listings)} organic restaurants scraped")

            # ----- email extraction -----
            email_count = 0
            for L in all_listings:
                if not L.get("website"):
                    continue
                em = extract_site_emails(L["website"])
                if em:
                    L["email"] = em[0]
                    email_count += 1
            print(f"  {city_display}: {email_count}/{len(all_listings)} with emails")

            # ----- insert -----
            ins, skp = insert_leads(all_listings)
            all_new += ins
            all_emails += email_count
            results[city_display] = {
                "scraped": len(all_listings),
                "emails": email_count,
                "inserted": ins,
                "skipped_dup_in_db": skp,
                "listings": all_listings,
            }
            print(f"  {city_display}: inserted {ins}, skipped-in-db {skp}")

        browser.close()

    # --- write JSON snapshot ---
    snap = {c: {"scraped": r["scraped"], "emails": r["emails"],
                "inserted": r["inserted"], "skipped_dup_in_db": r["skipped_dup_in_db"]}
            for c, r in results.items()}
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "yellowpages_report.json")
    with open(out_path, "w") as f:
        json.dump({"generated_at": datetime.utcnow().isoformat(), "cities": snap},
                  f, indent=2)

    # --- summary ---
    print("\n" + "=" * 62)
    print("SUMMARY")
    print("=" * 62)
    for c, r in results.items():
        print(f"  {c}: {r['scraped']} scraped | {r['emails']} emails found | "
              f"{r['inserted']} inserted | {r['skipped_dup_in_db']} dup-in-db")
    print("-" * 62)
    print(f"  TOTAL new leads inserted: {all_new}")
    print(f"  TOTAL emails found: {all_emails}")
    print(f"  JSON snapshot: {out_path}")


if __name__ == "__main__":
    run()
