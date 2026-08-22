#!/usr/bin/env python3
"""Regenerate psdepot.com sitemap.xml from all live HTML files."""
import os, datetime

SITE = "/var/www/psdepot.com"
TODAY = datetime.date.today().isoformat()
BASE = "https://psdepot.com"

EXCLUDE_DIRS = {"_archive", "_archive_thin", "admin", "cgi-bin", "staging", "node_modules", ".git", ".backups", "BACKUPS"}
EXCLUDE_FILES = {"404.html", "cart-test.html", "_template.html"}

def priority_for(path):
    if path == "index.html":
        return "1.0"
    if path.startswith("products/"):
        return "0.7"
    if path.startswith("blog/"):
        return "0.5"
    if path in ("privacy.html", "terms.html", "return-policy.html", "shipping-policy.html"):
        return "0.3"
    return "0.5"

urls = []
for root, dirs, files in os.walk(SITE):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fn in files:
        if not fn.endswith(".html") or fn in EXCLUDE_FILES:
            continue
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, SITE)
        urls.append(rel)

urls = sorted(set(urls))

xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    xml.append("  <url>")
    xml.append(f"    <loc>{BASE}/{u}</loc>")
    xml.append(f"    <lastmod>{TODAY}</lastmod>")
    xml.append(f"    <priority>{priority_for(u)}</priority>")
    xml.append("  </url>")
xml.append("</urlset>")

open(os.path.join(SITE, "sitemap.xml"), "w").write("\n".join(xml) + "\n")
print(f"✅ sitemap.xml regenerated: {len(urls)} URLs")
