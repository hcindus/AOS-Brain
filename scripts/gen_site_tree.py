#!/usr/bin/env python3
"""Generate psdepot.com site tree page (site-tree.html) from live filesystem."""
import os, html, datetime

ROOT = "/var/www/psdepot.com"
OUT = os.path.join(ROOT, "site-tree.html")

# Ordered sections
DIRS = [
    ("Products", "products"),
    ("Industries", "industries"),
    ("Guides", "guides"),
    ("Resources", "resources"),
    ("Blog", "blog"),
    ("Categories", "categories"),
    ("Services", "services"),
    ("POS Systems", "pos"),
    ("ReggieStarr", "reggiestarr"),
    ("Capton", "capton"),
    ("Landing", "landing"),
    ("Security", "sentinel-shield"),
    ("CREAM", "cream"),
    ("Collections", "collections"),
    ("ReggieStarr POS", "reggiestarr-pos"),
    ("RS-80", "rs-80"),
    ("Locations", "locations"),
    ("Sales", "sales"),
    ("E-Commerce", "ecom"),
    ("Events", "events"),
    ("Appointments", "appointments"),
]

def slug_label(fname):
    # humanize filename -> label
    s = fname.replace(".html", "").replace("-", " ").replace("_", " ")
    return s.title()

def link_for(relpath):
    return "/" + relpath.replace("\\", "/")

sections = []
for label, d in DIRS:
    dp = os.path.join(ROOT, d)
    if not os.path.isdir(dp):
        continue
    files = sorted(f for f in os.listdir(dp) if f.endswith(".html"))
    if not files:
        continue
    items = []
    for f in files:
        if f == "_template.html":
            continue  # skip template from public tree
        rel = f"{d}/{f}"
        disp = "index.html" if f == "index.html" else f
        items.append((link_for(rel), slug_label(f), disp))
    sections.append((label, items))

# Root-level pages (exclude the new site-tree itself and known-internal)
internal_skip = {"site-tree.html", "kb-admin.html", "cart-test.html", "chat-demo.html",
                 "psd_customer.html", "psd_dashboard.html", "psd_performance.html",
                 "brain-dashboard.html", "service-log.html", "4th-of-july.html",
                 "pollo_asados_demo.html", "RS-79_demo.html", "business-cards.html",
                 "thank-you-payment.html"}
root_files = sorted(f for f in os.listdir(ROOT)
                    if f.endswith(".html") and f not in internal_skip)
root_items = [(link_for(f), slug_label(f), f) for f in root_files]

today = datetime.date.today().isoformat()
total = len(root_items) + sum(len(items) for _, items in sections)

def esc(s):
    return html.escape(s, quote=True)

# Build HTML
links_html = []
links_html.append(f'<div class="wrap">')
links_html.append(f'<h1>Site Tree</h1>')
links_html.append(f'<p class="sub">Complete index of {total} public pages on Performance Supply Depot — generated {today}.</p>')

for label, items in sections:
    links_html.append(f'<h2>{esc(label)}</h2><div class="grid">')
    for href, disp, fname in items:
        links_html.append(f'<a href="{esc(href)}">{esc(disp)}</a>')
    links_html.append('</div>')

links_html.append('<h2>Site Pages</h2><div class="grid">')
for href, disp, fname in root_items:
    links_html.append(f'<a href="{esc(href)}">{esc(disp)}</a>')
links_html.append('</div>')
links_html.append('</div>')

body_inner = "\n".join(links_html)

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Site Tree | Performance Supply Depot</title>
<meta name="description" content="Complete site index of Performance Supply Depot — POS supplies, industries served, guides, resources, and more. Find every page in one place.">
<meta name="robots" content="noindex,follow">
<style>
body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#F8F9FA;color:#111;margin:0;padding:2rem;line-height:1.6}}
h1{{color:#0A1A2F}}
h2{{color:#0A1A2F;border-bottom:2px solid #FF7A00;padding-bottom:.25rem;margin-top:2rem}}
p.sub{{color:#555}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.3rem 1.5rem}}
a{{color:#0A1A2F;text-decoration:none}}
a:hover{{color:#FF7A00;text-decoration:underline}}
.wrap{{max-width:1100px;margin:0 auto}}
.main-nav{{background:#12283f;border-bottom:3px solid #c53030}}
.main-nav .container{{display:flex;gap:4px;flex-wrap:wrap}}
.main-nav a{{display:inline-block;color:#bee3f8;text-decoration:none;font-weight:600;font-size:15px;padding:12px 18px;border-bottom:2px solid transparent}}
.main-nav a:hover,.main-nav a:focus{{color:#fff;background:rgba(255,255,255,0.08);border-bottom-color:#c53030}}
</style>
</head>
<body>
<nav class="main-nav" aria-label="Primary">
    <div class="container">
        <a href="/">Home</a>
        <a href="/products/index.html">Products</a>
        <a href="/blog/index.html">Blog</a>
        <a href="/services.html">Services</a>
        <a href="/about.html">About</a>
        <a href="/testimonials.html">Testimonials</a>
        <a href="/resources/faq.html">FAQ</a>
        <a href="/contact.html">Contact</a>
        <a href="/locations.html">Service Areas</a>
    </div>
</nav>
{body_inner}
</body>
</html>
"""

with open(OUT, "w") as f:
    f.write(html_doc)

print(f"Wrote {OUT}")
print(f"Total public pages indexed: {total}")
print(f"Sections: {len(sections)}")
print(f"Root pages: {len(root_items)}")
