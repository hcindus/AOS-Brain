#!/usr/bin/env python3
"""Upgrade the truncated 5-link nav to the full 9-link nav on psdepot.com pages.

The 5-link nav (Home, Products, About, Contact, Service Areas) is missing:
Blog, Services, Testimonials, FAQ. This inserts them in the correct order.
"""
import os

VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]

# Exact 5-link pattern (consistent across all affected pages)
OLD = """        <a href="/">Home</a>
        <a href="/products/index.html">Products</a>
        <a href="/about.html">About</a>
        <a href="/contact.html">Contact</a>
        <a href="/locations.html">Service Areas</a>"""

NEW = """        <a href="/">Home</a>
        <a href="/products/index.html">Products</a>
        <a href="/blog/index.html">Blog</a>
        <a href="/services.html">Services</a>
        <a href="/testimonials.html">Testimonials</a>
        <a href="/about.html">About</a>
        <a href="/resources/faq.html">FAQ</a>
        <a href="/contact.html">Contact</a>
        <a href="/locations.html">Service Areas</a>"""

# Pages confirmed to have the truncated 5-link nav
PAGES = [
    "RS-80.html",
    "business-cards.html",
    "cream.html",
    "cream2.html",
    "cream3.html",
    "products/13-305-epson-impact-paper.html",
    "products/15-741-credit-card-paper.html",
    "products/30-150-integrated-scale.html",
    "products/54-230-epson-thermal.html",
    "products/62245-erc-ribbons.html",
    "products/67240-star-ribbons.html",
    "products/72-100-cash-drawer.html",
    "products/CC-235-carbonless-paper.html",
    "products/capton-1.5oz-pourer.html",
    "products/capton-1oz-pourer.html",
    "products/capton-2oz-pourer.html",
    "products/capton-cleaning-kit.html",
    "products/capton-pouring-systems.html",
    "products/capton-pourlink-analytics.html",
    "products/capton-pourlink-receiver.html",
    "products/capton-variety-pack.html",
    "products/capton-wine-pourer.html",
    "products/cas-lp-1000n.html",
    "products/cas-pdn-series.html",
    "products/cash-drawers.html",
    "products/lucki-tile.html",
    "products/orionstar-lucki.html",
    "products/pf-230-phenol-free-thermal-paper.html",
    "products/printer-ribbons.html",
    "products/sam4s-er-260.html",
    "products/sam4s-er-265.html",
    "products/sam4s-er-940.html",
    "products/sam4s-sap-630.html",
    "products/thermal-paper.html",
]

count = 0
for ver in VERSIONS:
    for page in PAGES:
        path = os.path.join(ver, page)
        if not os.path.exists(path):
            print(f"SKIP (missing): {path}")
            continue
        with open(path) as f:
            content = f.read()
        if OLD in content:
            content = content.replace(OLD, NEW, 1)
            with open(path, "w") as f:
                f.write(content)
            count += 1
            print(f"UPDATED: {path}")
        else:
            print(f"NO-MATCH: {path}")

print(f"\nTotal pages upgraded: {count}")
