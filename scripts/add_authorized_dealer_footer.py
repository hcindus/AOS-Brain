#!/usr/bin/env python3
"""Add an 'Authorized Dealer' trust line to footers of key psdepot.com pages."""
import re

FILES = [
    "index.html", "about.html", "contact.html", "services.html",
    "security.html", "testimonials.html", "independent-grocer.html",
    "electronic-shelf-labels.html", "self-checkout.html", "sam4pos.html",
    "pos-software.html", "blog/index.html", "products/index.html",
    "industries/grocery-stores.html",
]

TRUST_LINE = (
    '<p style="margin-top: 12px; font-size: 13px; color: inherit; opacity: 0.85;">'
    'Authorized Dealer: <strong>SAM4S</strong> &middot; <strong>CAS</strong> &middot; '
    '<strong>ACM Technologies</strong> &middot; <strong>TST Impresso</strong> &middot; '
    '<strong>Capton</strong></p>'
)

import os
SITE = "/var/www/psdepot.com"
updated, skipped, missing = [], [], []

for rel in FILES:
    fp = os.path.join(SITE, rel)
    if not os.path.exists(fp):
        missing.append(rel)
        continue
    html = open(fp, encoding="utf-8", errors="ignore").read()
    if "Authorized Dealer:" in html:
        skipped.append(rel)
        continue

    # Find the footer block
    fm = re.search(r"<footer.*?</footer>", html, re.S)
    if not fm:
        missing.append(rel + " (no footer)")
        continue

    footer = fm.group(0)
    # Insert trust line before </footer>
    new_footer = footer[:-len("</footer>")] + "\n" + TRUST_LINE + "\n" + "</footer>"
    html = html.replace(footer, new_footer, 1)
    open(fp, "w", encoding="utf-8").write(html)
    updated.append(rel)

print(f"Updated: {len(updated)}")
for u in updated: print("  + " + u)
print(f"Skipped (already has): {len(skipped)}")
for s in skipped: print("  = " + s)
print(f"Missing/no-footer: {len(missing)}")
for m in missing: print("  ! " + m)
