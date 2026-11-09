#!/usr/bin/env python3
"""
cheap_enrich.py — FREE-tier vendor email/phone enrichment for DepotChaos.

Tools: duckduckgo-search (DDGS), requests, BeautifulSoup, regex. No paid APIs.

Rules (Captain's orders):
  - NEVER guess-pattern emails (no firstname@domain construction).
  - Only store an email regex-extracted from a page on the vendor's OWN site
    (same registrable domain as the site we found via search).
  - Only store a phone if it appears on that same site.
  - High confidence only.

Usage:
  ./cheap_enrich.py --limit 60 [--state CA] [--dry-run] [--delay 1.5]
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "depot_chaos.db")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?1[\s.\-]?)?\(?([2-9]\d{2})\)?[\s.\-]?(\d{3})[\s.\-]?(\d{4})\b")

# emails we never want
BAD_EMAIL_PAT = re.compile(
    r"(sentry|wixpress|@example\.|@domain\.|@email\.com|@sentry|wix|godaddy|"
    r"\.png$|\.jpg$|\.gif$|\.webp$|@2x|squarespace|@site\.|your@|name@|"
    r"info@company|test@|user@|admin@example)", re.I)

CONTACT_HINTS = ("contact", "about", "connect", "location", "hours", "visit",
                 "reach", "info", "menu") 
SKIP_DOMAINS = (
    "facebook.com", "instagram.com", "twitter.com", "x.com", "yelp.com",
    "tripadvisor.com", "doordash.com", "ubereats.com", "grubhub.com",
    "opentable.com", "mapquest.com", "yellowpages.com", "manta.com",
    "bbb.org", "linkedin.com", "youtube.com", "pinterest.com", "tiktok.com",
    "google.com", "bing.com", "duckduckgo.com", "foursquare.com", "zomato.com",
    "allmenus.com", "menupix.com", "restaurantji.com", "sirved.com",
    "yellowpage", "chamberofcommerce.com", "bizapedia.com", "zoominfo.com",
    "wikipedia.org", "amazon.com", "doordash", "seamless.com", "postmates",
    "trip.com", "expedia.com", "hotels.com", "yellowpages", "superpages.com",
    "citysearch.com", "nicelocal.com", "yellow.place", "cylex", "hotfrog",
    "brownbook", "ehealth", "healthgrades", "mapquest", "ezlocal", "merchantcircle",
)


def log(msg):
    print(msg, flush=True)


def registrable(host):
    """Cheap eTLD+1: last two labels (good enough for .com/.net/.org)."""
    host = host.lower().strip(".")
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) >= 3 and parts[-2] in ("co", "com", "net", "org", "gov", "edu") and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def site_url(raw):
    if not raw:
        return None
    try:
        p = urlparse(raw if "://" in raw else "http://" + raw)
        if not p.netloc:
            return None
        return f"{p.scheme}://{p.netloc}"
    except Exception:
        return None


def clean_phone(m):
    d = re.sub(r"\D", "", m)
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    if len(d) != 10:
        return None
    if d[0] in "01" or d[3] in "01":   # invalid NANP
        return None
    if d == d[0] * 10 or d in ("1234567890", "5555555555"):
        return None
    return f"+1{d}"


class Fetcher:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

    def get(self, url, timeout=12):
        try:
            r = self.s.get(url, timeout=timeout, allow_redirects=True)
            ct = r.headers.get("content-type", "")
            if r.status_code >= 400 or "html" not in ct.lower():
                return None, None
            if len(r.content) > 3_000_000:
                return None, None
            return r.text, r.url
        except Exception:
            return None, None

    def find_site(self, name, address):
        """DDGS search -> best official site URL."""
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            from ddgs import DDGS
        queries = [f'"{name}" {address}', f'"{name}" {address} contact']
        seen = []
        try:
            with DDGS() as ddgs:
                for q in queries:
                    for res in ddgs.text(q, max_results=8):
                        href = res.get("href") or res.get("url") or ""
                        host = urlparse(href).netloc.lower()
                        if not host:
                            continue
                        if any(b in host for b in SKIP_DOMAINS):
                            continue
                        u = site_url(href)
                        if u and u not in seen:
                            seen.append(u)
                    if seen:
                        break
        except Exception as e:
            log(f"    [ddg error] {e}")
            return None
        return seen[0] if seen else None


def harvest(html, page_url, want_domain):
    """Extract (emails, phone) that belong to want_domain."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # mailto: links are strongest signal
    emails, phones = [], []
    for a in soup.find_all("a", href=True):
        h = a["href"].strip()
        if h.lower().startswith("mailto:"):
            e = h[7:].split("?")[0].strip().strip("'\"")
            if EMAIL_RE.fullmatch(e or ""):
                emails.append(e)
        if h.lower().startswith("tel:"):
            p = clean_phone(h[4:])
            if p:
                phones.append(p)

    for e in EMAIL_RE.findall(text):
        emails.append(e.strip(".,;:()<>"))

    # order-preserving dedupe, filtered by domain + junk patterns
    good_e, seen = [], set()
    for e in emails:
        e = e.lower()
        if e in seen or BAD_EMAIL_PAT.search(e):
            continue
        # reject image/cdn hashes and long random locals
        local, _, dom = e.partition("@")
        if len(local) > 30 or re.fullmatch(r"[0-9a-f]{16,}", local):
            continue
        if not dom.endswith(want_domain) and dom != want_domain:
            # allow subdomain of the site or site of subdomain
            if not (dom.endswith("." + want_domain) or want_domain.endswith("." + dom)):
                continue
        seen.add(e)
        good_e.append(e)

    if not phones:
        for m in PHONE_RE.finditer(text):
            p = clean_phone("".join(m.groups()))
            if p:
                phones.append(p)
    return good_e, (phones[0] if phones else None)


def enrich_one(f, name, address):
    site = f.find_site(name, address)
    if not site:
        return None, None, None, "no_site"
    dom = registrable(urlparse(site).netloc)
    html, final = f.get(site)
    if not html:
        return None, None, site, "fetch_fail"

    pages = [(html, final)]
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        t = (a.get_text() or "").strip().lower()
        h = a["href"]
        if any(k in t for k in CONTACT_HINTS) or any(k in h.lower() for k in CONTACT_HINTS):
            u = h if h.startswith("http") else site.rstrip("/") + "/" + h.lstrip("/")
            if registrable(urlparse(u).netloc) == dom and u not in links:
                links.append(u)
    for u in links[:2]:
        h2, f2 = f.get(u)
        if h2:
            pages.append((h2, f2))

    all_e, phone = [], None
    for h, u in pages:
        e, p = harvest(h, u, dom)
        all_e.extend(e)
        phone = phone or p
    # dedupe keeping preference: info@/contact@ first
    all_e = list(dict.fromkeys(all_e))
    all_e.sort(key=lambda x: (0 if x.split("@")[0] in
                              ("info", "contact", "hello", "orders", "sales") else 1, x))
    email = all_e[0] if all_e else None
    return email, phone, site, "ok" if (email or phone) else "nothing"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--state", default="CA")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--delay", type=float, default=1.2)
    args = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""
        SELECT MIN(id) AS id, name, address, city, state, phone, email
        FROM vendors
        WHERE data_class='real' AND (email IS NULL OR email='') AND state=?
        GROUP BY name, address
        ORDER BY city ASC, name ASC
    """, (args.state,)).fetchall()
    log(f"Queue: {len(rows)} distinct {args.state} no-email leads")

    f = Fetcher()
    stats = {"processed": 0, "email": 0, "phone": 0, "both": 0,
             "no_site": 0, "fetch_fail": 0, "nothing": 0}
    results = []

    for r in rows[: args.limit]:
        stats["processed"] += 1
        log(f"[{stats['processed']}/{min(args.limit,len(rows))}] {r['city']} — {r['name']}")
        try:
            email, phone, site, status = enrich_one(f, r["name"], r["address"] or r["city"])
        except Exception as e:
            log(f"    [error] {e}")
            email, phone, site, status = None, None, None, "error"
        stats[status if status in stats else "nothing"] = stats.get(status if status in stats else "nothing", 0) + 1
        if email:
            stats["email"] += 1
        if phone:
            stats["phone"] += 1
        if email and phone:
            stats["both"] += 1
        log(f"    {status:10s} site={site} email={email} phone={phone}")
        results.append({"id": r["id"], "name": r["name"], "city": r["city"],
                        "email": email, "phone": phone, "site": site, "status": status})

        if (email or phone) and not args.dry_run:
            sets, vals = [], []
            if email:
                sets.append("email=?")
                vals.append(email)
            if phone and not r["phone"]:
                sets.append("phone=?")
                vals.append(phone)
            if sets:
                vals.append(r["id"])
                # update all duplicate rows sharing name+address
                con.execute(
                    f"UPDATE vendors SET {', '.join(sets)} "
                    "WHERE data_class='real' AND name=? AND address IS ?",
                    vals[:-1] + [r["name"], r["address"]])
                con.commit()
        time.sleep(args.delay)

    with open("enrich_last_run.json", "w") as fh:
        json.dump({"stats": stats, "results": results}, fh, indent=2)

    p = stats["processed"] or 1
    log("\n=== SUMMARY ===")
    log(f"processed : {stats['processed']}")
    log(f"email     : {stats['email']}  ({100*stats['email']/p:.1f}%)")
    log(f"phone     : {stats['phone']}  ({100*stats['phone']/p:.1f}%)")
    log(f"both      : {stats['both']}")
    log(f"no site   : {stats['no_site']}")
    log(f"nothing   : {stats['nothing']}")
    log(f"yield     : {100*(stats['email'])/p:.1f}% email rate")
    return stats


if __name__ == "__main__":
    main()
