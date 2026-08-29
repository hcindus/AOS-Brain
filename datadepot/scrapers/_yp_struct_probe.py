import re, json

with open("/root/.openclaw/workspace/datadepot/scrapers/_yp_playwright.html") as f:
    html = f.read()

# count business-name anchors
names = re.findall(r'<a class="business-name"[^>]*>(.*?)</a>', html, re.S)
print("business-name anchors:", len(names))
print("sample:", names[:5])

# Count result divs - look for the search-result parent structure
for pat in ["search-result", "result organic", 'class="result"', "v-card", "organic", "ad-pill"]:
    print(f"'{pat}':", html.count(pat))

# phone count
phones = re.findall(r'<div class="phone">(.*?)</div>', html)
print("phone blocks:", len(phones), phones[:5])

# adr count
adrs = re.findall(r'<p class="adr">(.*?)</p>', html)
print("adr blocks:", len(adrs), adrs[:5])

# website links
sites = re.findall(r'<div class="links">(.*?)</div>', html, re.S)
print("links blocks:", len(sites))
for s in sites[:3]:
    m = re.findall(r'href="(http[^"]+)"[^>]*>(?:Website)', s)
    print("  site:", m)

# Check pagination
pages = re.findall(r'href="([^"]*page=2[^"]*)"', html)
print("page2 links:", pages[:3])

# Check if there's a 'narrow' classification; look for count of total
tot = re.findall(r'(\d+)\s*Restaurants', html)
print("total count text:", tot[:3])
