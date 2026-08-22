#!/usr/bin/env python3
"""Update sitemap.xml + products index to reflect the SAM4S/CAS catalog changes."""
import re, os, datetime

SITE = "/var/www/psdepot.com"
TODAY = datetime.date.today().isoformat()

# New pages added this session
NEW = [
    "products/cas-cl7200.html",
    "products/cas-cl3000.html",
    "products/cas-pd-2z.html",
    "products/cas-sw-rs.html",
    "products/cas-s2000-jr.html",
    "products/cas-tracker-r457.html",
    "products/mscashdrawer/sam4s-gcube-receipt-printer.html",
    "products/mscashdrawer/sam4s-ellix40ii-receipt-printer.html",
    "products/mscashdrawer/sam4s-giant-100-receipt-printer.html",
    "products/mscashdrawer/sam4s-hcube-receipt-printer.html",
    "products/mscashdrawer/sam4s-astra-android-kiosk.html",
    "products/mscashdrawer/sam4s-sapphire-android-pos-terminal.html",
]

# Archived (removed) 'cash register' pages
REMOVED = [
    "products/mscashdrawer/cas-se-c3500mc-split-keyboard-cash-register.html",
    "products/mscashdrawer/cas-sr-4000mc-raised-keyboarddual-station-printer.html",
    "products/mscashdrawer/cas-te-3000-ecr-stroke-keyboard-multi-line-lcd.html",
    "products/mscashdrawer/cas-te-4500fb-cb-with-mid-size-cash-drawer-dl-3616.html",
    "products/mscashdrawer/cas-tk-3200c-flat-keyboard-cash-register.html",
]

# --- Update sitemap.xml ---
sp = os.path.join(SITE, "sitemap.xml")
xml = open(sp).read()

for r in REMOVED:
    # remove the whole <url> block for the removed page
    xml = re.sub(rf'\s*<url>\s*<loc>https://psdepot\.com/{re.escape(r)}</loc>.*?</url>', '', xml, flags=re.S)

# add new URLs before </urlset>
new_blocks = ""
for n in NEW:
    new_blocks += f"  <url>\n    <loc>https://psdepot.com/{n}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>0.7</priority>\n  </url>\n"
xml = xml.replace("</urlset>", new_blocks + "</urlset>")
open(sp, "w").write(xml)
print(f"✅ sitemap.xml updated: +{len(NEW)} added, -{len(REMOVED)} removed")

# --- Update products/index.html (remove archived links) ---
idx = os.path.join(SITE, "products", "index.html")
html = open(idx).read()
for r in REMOVED:
    html = html.replace(f"mscashdrawer/{os.path.basename(r)}", "#removed")
open(idx, "w").write(html)
print("✅ products/index.html: removed archived cash-register links")
