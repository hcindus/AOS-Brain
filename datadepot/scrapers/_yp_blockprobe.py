#!/usr/bin/env python3
"""Probe what YellowPages returns when Playwright fetches a search page after a fresh browser."""
import sys, time
sys.path.insert(0, '/root/.openclaw/workspace/datadepot/scrapers')
import yellowpages_city_scraper as yp

geo = 'chicago%2C+il'
url = yp.build_search_url(geo)
print("URL:", url)
with yp.sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
    ctx = b.new_context(user_agent=yp.UA, locale='en-US', viewport={'width':1366,'height':768})
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page = ctx.new_page()
    page.goto(url, timeout=45000, wait_until='domcontentloaded')
    time.sleep(5)
    title = page.title() or ''
    html = page.content()
    print("TITLE:", repr(title))
    print("HTML len:", len(html))
    low = html.lower()
    for marker in ['cloudflare','attention required','cf-chl','challenge','verify','captcha','robot','access denied','just a moment','error code 1020','<form id="challenge-form"']:
        if marker in low:
            print("  MARKER:", marker)
    # count v-card
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.select('div.v-card')
    print("v-card count:", len(cards))
    # dump a snippet around where a block indicator would be
    for kw in ['blocked','sorry','javascript','enable cookies','prove you','we have detected']:
        idx = low.find(kw)
        if idx > 0:
            print(f"  [snippet '{kw}']:", html[max(0,idx-80):idx+120].replace('\n',' '))
    b.close()
