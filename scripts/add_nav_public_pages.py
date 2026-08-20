#!/usr/bin/env python3
"""Add the full 9-link nav to PUBLIC MARKETING pages that are missing it.

Skips secondary apps/tools (appointments, ecom, admin, dashboards, capton,
depotchaos, cream, ivoire/ivory auto, partner portals, etc.) and utility/demo
pages. Adds nav to location/city/state pages, industries, guides, resources,
categories, blog articles, product detail pages, and robotics pages.
"""
import os

VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]

# Directories that are standalone apps/tools — do NOT touch.
EXCLUDE_DIRS = {
    "appointments", "ecom", "admin", "capton", "collections", "credit-card",
    "depotchaos", "invoices", "ivoire-auto", "ivory-auto", "ivory-auto-backup",
    "leads-portal", "leads-dashboard", "net30", "newsletter", "orders",
    "partners", "sales", "reggiestarr", "reggiestarr-pos", "pages", "events",
    "sentinel-shield", "cream", "pos", "rs-80", "landing",
}

# Root-level utility/demo pages to skip.
EXCLUDE_FILES = {
    "404.html", "RS-79_demo.html", "RS-80.html", "4th-of-july.html",
    "pollo_asados_demo.html", "brain-dashboard.html", "psd_customer.html",
    "psd_dashboard.html", "psd_performance.html", "service-log.html",
    "booking.html", "chat-demo.html", "kb-admin.html", "checkout.html",
    "cart-test.html", "clear-cart.html", "site-tree.html",
    "service-areas-map.html", "thank-you-payment.html",
    "thank-you-payment-chinese.html", "thank-you-payment-hindi.html",
    "thank-you-payment-russian.html", "thank-you-payment-spanish.html",
    "thank-you-payment-tagalog.html", "thank-you-payment-urdu.html",
    "thank-you-payment-vietnamese.html",
}

NAV_CSS = """        .main-nav {
            background: #12283f;
            border-bottom: 3px solid var(--accent);
        }
        .main-nav .container {
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
        }
        .main-nav a {
            display: inline-block;
            color: #bee3f8;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            padding: 12px 18px;
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
        }
        .main-nav a:hover,
        .main-nav a:focus {
            color: #ffffff;
            background: rgba(255,255,255,0.08);
            border-bottom-color: var(--accent);
        }
        .main-nav a[aria-current="page"] {
            color: #ffffff;
            border-bottom-color: var(--accent);
        }
"""

NAV_MARKUP = """    <nav class="main-nav" aria-label="Primary">
        <div class="container">
            <a href="/">Home</a>
            <a href="/products/index.html">Products</a>
            <a href="/blog/index.html">Blog</a>
            <a href="/services.html">Services</a>
            <a href="/testimonials.html">Testimonials</a>
            <a href="/about.html">About</a>
            <a href="/resources/faq.html">FAQ</a>
            <a href="/contact.html">Contact</a>
            <a href="/locations.html">Service Areas</a>
        </div>
    </nav>
"""


def should_skip(relpath: str) -> bool:
    parts = relpath.split(os.sep)
    # skip if any parent dir is excluded
    for p in parts[:-1]:
        if p in EXCLUDE_DIRS:
            return True
    if parts[-1] in EXCLUDE_FILES:
        return True
    return False


def add_nav(path: str) -> bool:
    with open(path) as f:
        content = f.read()

    # Must have the standard header, and not already have a nav
    if "Performance<span style=\"color:#63b3ed;\">Supply</span>Depot" not in content:
        return False
    if '<nav class="main-nav"' in content:
        return False

    changed = False
    if ".main-nav {" not in content:
        content = content.replace("    </style>", NAV_CSS + "    </style>", 1)
        changed = True

    if "<nav class=\"main-nav\"" not in content:
        if "</header><div" in content:
            content = content.replace("</header><div", "</header>\n" + NAV_MARKUP + "\n<div", 1)
        else:
            content = content.replace("</header>", "</header>\n\n" + NAV_MARKUP, 1)
        changed = True

    if changed:
        with open(path, "w") as f:
            f.write(content)
    return changed


def main(dry_run=False):
    total = 0
    touched = []
    for ver in VERSIONS:
        root = ver
        count = 0
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in (".backups", "ivory-auto-backup", "node_modules")]
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root)
                if should_skip(rel):
                    continue
                if add_nav(full):
                    count += 1
                    touched.append(os.path.join(ver, rel))
        print(f"{ver}: {'WOULD ADD' if dry_run else 'ADDED'} nav to {count} pages")
        total += count
    print(f"\nTOTAL: {total}")
    if dry_run:
        for t in touched[:200]:
            print("  ", t)


if __name__ == "__main__":
    import sys
    main(dry_run="--dry-run" in sys.argv)
