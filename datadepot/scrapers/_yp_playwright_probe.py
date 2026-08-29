#!/usr/bin/env python3
"""Probe YellowPages with Playwright chromium to see if Cloudflare can be bypassed."""
import sys, time
from playwright.sync_api import sync_playwright

URL = "https://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=petaluma%2C+ca"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ]
    )
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        locale="en-US",
        viewport={"width": 1366, "height": 768},
    )
    # Basic stealth
    ctx.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US','en']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
    """)
    page = ctx.new_page()
    page.goto(URL, timeout=60000, wait_until="domcontentloaded")
    # Wait a bit for any JS challenge to resolve
    time.sleep(8)
    title = page.title()
    print("TITLE:", title)
    url = page.url
    print("URL:", url)
    # Check content
    try:
        content = page.content()
        print("LEN:", len(content))
        if "business-name" in content or "result" in content:
            print("HAS_RESULTS: YES")
            with open("/root/.openclaw/workspace/datadepot/scrapers/_yp_playwright.html","w") as f:
                f.write(content)
        else:
            print("HAS_RESULTS: NO (probably still blocked)")
            print(content[:800])
    except Exception as e:
        print("ERR:", e)
    browser.close()
