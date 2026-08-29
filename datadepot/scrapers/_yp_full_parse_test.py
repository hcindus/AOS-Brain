#!/usr/bin/env python3
"""Full extraction test on saved Petaluma HTML."""
from bs4 import BeautifulSoup
import re

with open("/root/.openclaw/workspace/datadepot/scrapers/_yp_playwright.html") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")
cards = soup.select("div.v-card")

def clean(t):
    return re.sub(r'\s+', ' ', t).strip()

ADDR_RE = re.compile(r'^\s*(.*?),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)', re.I)

def parse_card(card):
    name_a = card.select_one("a.business-name")
    name = clean(name_a.get_text()) if name_a else None
    cats = [clean(a.get_text()) for a in card.select("div.categories a")]
    site = None
    for a in card.select("div.links a"):
        if "website" in a.get_text().strip().lower():
            site = a.get("href"); break
    # phone
    phone = None
    pe = card.select_one("div.phones.phone.primary") or card.select_one("div.phone")
    if pe: phone = clean(pe.get_text())
    # address
    street = None; city=None; state=None; zipc=None
    adr = card.select_one("div.adr")
    if adr:
        se = adr.select_one("div.street-address")
        if se: street = clean(se.get_text())
        le = adr.select_one("div.locality")
        if le:
            m = ADDR_RE.match(clean(le.get_text()))
            if m:
                city, state, zipc = m.group(1), m.group(2), m.group(3)
    is_ad = bool(card.select_one("span.ad-pill"))
    return {"name":name,"cats":cats,"site":site,"phone":phone,
            "street":street,"city":city,"state":state,"zip":zipc,"ad":is_ad}

for card in cards:
    r = parse_card(card)
    if r["name"]:
        print(f"{r['name']} | {r['phone']} | {r['street']} | {r['city']},{r['state']} {r['zip']} | {r['site']} | AD={r['ad']}")
