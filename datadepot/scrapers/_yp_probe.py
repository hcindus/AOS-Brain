#!/usr/bin/env python3
"""Probe YellowPages search page structure to understand the HTML layout."""
import requests, re, json

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

url = "https://www.yellowpages.com/search?search_terms=restaurants&geo_location_terms=petaluma%2C+ca"
r = S.get(url, timeout=20, allow_redirects=True)
print("status:", r.status_code)
print("final url:", r.url)
print("len:", len(r.text))

# Save the raw HTML for inspection
with open("/root/.openclaw/workspace/datadepot/scrapers/_yp_probe_petaluma.html", "w") as f:
    f.write(r.text)

# Look for the listing containers
text = r.text
# Find elements with class 'result' or similar
for pat in ["info", "business-name", "phones", "street-address", "adr", "tracked-business", "result"]:
    count = len(re.findall(r'class=["\'][^"\']*' + pat, text))
    print(f"class patterns matching '{pat}': {count}")

# Print a sample of listing structure around 'business-name'
idx = text.find("business-name")
print("\n--- sample around first business-name ---")
print(text[idx-200:idx+1500].replace("\n", " "))
