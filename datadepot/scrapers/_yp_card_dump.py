import re
with open("/root/.openclaw/workspace/datadepot/scrapers/_yp_playwright.html") as f:
    html = f.read()
# find a non-ad card and dump full html
idx = html.find("Cucina Paradiso")
print(html[idx-3000:idx+200].replace("\n"," "))
