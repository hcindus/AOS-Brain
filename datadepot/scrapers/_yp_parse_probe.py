import re

with open("/root/.openclaw/workspace/datadepot/scrapers/_yp_playwright.html") as f:
    html = f.read()

# Find a result block. YellowPages uses div.N-... classes but commonly has:
# <a class="business-name" ...><span>Name</span></a>
# Let's find business-name occurrences
for m in re.finditer(r'class="business-name"[^>]*>', html):
    s = m.start()
    # print surrounding
    print("==== business-name block ====")
    print(html[s-100:s+2000].replace("\n"," "))
    break
