import re
with open("/root/.openclaw/workspace/datadepot/scrapers/_yp_playwright.html") as f:
    html = f.read()
# Find Cucina Paradiso card and dump the info-secondary section
idx = html.find("Cucina Paradiso")
# find all "info-secondary" near it
i2 = html.find('info-secondary', idx)
print(html[i2-200:i2+2500].replace("\n"," "))
