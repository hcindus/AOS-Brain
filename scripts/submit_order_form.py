#!/usr/bin/env python3
"""
CLOSETER Google Form auto-submit (Option A — no Google Cloud creds).
Loads the 5-page order form in a headless browser, fills all fields, and submits.
Fallback: raw HTTP POST to /formResponse if Playwright isn't available.
"""
import sys, re, urllib.request, urllib.parse

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf_MpGmbwkrZm2nVsL-RYiVHCsEqEMpjZ6eHKTQ8rr1KUx2Cw/viewform"
POST_URL = FORM_URL.replace("/viewform", "/formResponse")

# Field IDs extracted from the form's data-params (page 1)
FIELDS = {
    "manager_name": "entry.137364416",
    "business_name": "entry.1156315973",
    "address": "entry.1843265236",
    "city": "entry.1720911976",
    "state": "entry.1420432229",
    "zip": "entry.1670994120",
    "date": "entry.1851360912",
}

def submit_via_playwright(order: dict) -> str:
    """Use Playwright to fill + submit the multi-page form (most reliable)."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(FORM_URL)
        # TODO: fill each page's fields by label/ID, click Next, then Submit.
        # For now, report that the browser loaded (structure confirmed).
        title = page.title()
        browser.close()
        return f"BROWSER_LOADED (title={title})"

def submit_via_post(order: dict) -> str:
    """Raw HTTP POST to /formResponse (simpler, but multi-page forms may reject)."""
    data = {}
    if order.get("manager_name"): data[FIELDS["manager_name"]] = order["manager_name"]
    if order.get("business_name"): data[FIELDS["business_name"]] = order["business_name"]
    if order.get("address"): data[FIELDS["address"]] = order["address"]
    if order.get("city"): data[FIELDS["city"]] = order["city"]
    if order.get("state"): data[FIELDS["state"]] = order["state"]
    if order.get("zip"): data[FIELDS["zip"]] = order["zip"]
    if order.get("date"): data[FIELDS["date"]] = order["date"]
    # partialResponse + pageHistory needed for multi-page forms
    data["partialResponse"] = "[]"
    data["pageHistory"] = "0,1,2,3,4"
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(POST_URL, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return f"POST_OK status={r.status}"
    except Exception as e:
        return f"POST_FAIL {e}"

if __name__ == "__main__":
    # Test order
    order = {
        "manager_name": "Test Manager",
        "business_name": "Test Cafe",
        "address": "123 Main St",
        "city": "Testville",
        "state": "CA",
        "zip": "99999",
        "date": "2026-11-10",
    }
    # try Playwright first (multi-page form needs a real browser)
    try:
        result = submit_via_playwright(order)
    except Exception as e:
        result = f"PLAYWRIGHT_UNAVAILABLE ({e})"
    print(result)
    # fallback POST
    print(submit_via_post(order))
