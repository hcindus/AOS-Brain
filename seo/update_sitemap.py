#!/usr/bin/env python3
"""Update psdepot.com sitemap: remove redirected geo URLs, add region pages."""
import json, re, os

SITE = "/var/www/psdepot.com"
REGIONS = ["northwest", "west", "midwest", "south", "east-coast", "canada-mexico"]

# slugs to remove = those with a real region target
m = json.load(open("/root/.openclaw/workspace/seo/redirect_map.json"))
remove = {slug for slug, r in m.items() if r in REGIONS}

with open(os.path.join(SITE, "sitemap.xml")) as f:
    content = f.read()

# split into <url> blocks
urls = re.findall(r"<url>.*?</url>", content, re.DOTALL)
print(f"original URLs: {len(urls)}")

kept = []
removed = 0
for u in urls:
    loc = re.search(r"<loc>https://psdepot\.com/([^<]+)</loc>", u)
    if loc:
        path = loc.group(1)
        slug = path.rstrip("/").replace(".html", "")
        if slug in remove:
            removed += 1
            continue
    kept.append(u)

print(f"removed (redirected): {removed}")
print(f"kept: {len(kept)}")

# add region pages
today = "2026-08-22"
for r in REGIONS:
    kept.append(
        f"  <url>\n    <loc>https://psdepot.com/{r}.html</loc>\n"
        f"    <lastmod>{today}</lastmod>\n    <priority>0.7</priority>\n  </url>"
    )

header = re.match(r".*?<url>", content, re.DOTALL).group(0)[:-len("<url>")]
new_content = header + "\n".join(kept) + "\n</urlset>\n"

with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
    f.write(new_content)

final = len(re.findall(r"<url>", new_content))
print(f"\nFINAL sitemap URL count: {final}")
