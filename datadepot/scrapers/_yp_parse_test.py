#!/usr/bin/env python3
"""Test parsing YellowPages HTML with BeautifulSoup using the saved probe file."""
from bs4 import BeautifulSoup
import re

with open("/root/.openclaw/workspace/datadepot/scrapers/_yp_playwright.html") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")
cards = soup.select("div.v-card")
print("v-cards:", len(cards))

def clean(t):
    return re.sub(r'\s+', ' ', t).strip()

for card in cards[:6]:
    name_a = card.select_one("a.business-name")
    name = clean(name_a.get_text()) if name_a else None
    href = name_a["href"] if name_a and name_a.has_attr("href") else None
    # categories
    cats = [clean(a.get_text()) for a in card.select("div.categories a")]
    # website
    site = None
    links = card.select("div.links a")
    for a in links:
        txt = a.get_text().strip().lower()
        if "website" in txt:
            site = a.get("href")
            break
    # phone
    phone_el = card.select_one("div.phone")
    phone = clean(phone_el.get_text()) if phone_el else None
    # address
    adr_el = card.select_one("p.adr")
    adr = clean(adr_el.get_text()) if adr_el else None
    # ad pill?
    is_ad = bool(card.select_one("span.ad-pill"))
    print("----")
    print("NAME:", name, "| AD:", is_ad)
    print("  href:", href)
    print("  cats:", cats)
    print("  site:", site)
    print("  phone:", phone)
    print("  adr:", adr)
