#!/usr/bin/env python3
"""Add missing og:image, canonical, and meta description to MARKETING pages.

Derives canonical from the file's relative path and og:image from the fixed
brand asset. Adds a template meta description only when the page has a <title>
we can reference. Skips app/tool pages (ecom, appointments, admin, dashboards,
capton, cream, ivoire/ivory, depotchaos, partner portals, thank-you, demo pages,
booking, business-cards, brain-dashboard, psd_*, etc.).
"""
import os
import re

VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]

OG_IMAGE = "https://psdepot.com/assets/images/og-image.png"

# Directories that are apps/tools — do NOT touch.
SKIP_DIRS = {
    "ecom", "ivory-auto", "ivoire-auto", "depotchaos", "appointments", "sales",
    "reggiestarr", "pages", "events", "orders", "invoices", "admin", "partners",
    "net30", "newsletter", "landing", "credit-card", "collections", "capton",
    "cream", "pos", "rs-80", "sentinel-shield", "leads-portal", "leads-dashboard",
}

# Root-level tool/demo/utility pages to skip.
SKIP_FILES = {
    "404.html", "RS-79_demo.html", "RS-80.html", "4th-of-july.html",
    "pollo_asados_demo.html", "brain-dashboard.html", "psd_customer.html",
    "psd_dashboard.html", "psd_performance.html", "service-log.html",
    "booking.html", "chat-demo.html", "kb-admin.html", "checkout.html",
    "cart-test.html", "clear-cart.html", "site-tree.html", "business-cards.html",
    "cream.html", "cream2.html", "cream3.html", "reggiestarr.html",
    "thank-you-payment.html", "thank-you-payment-chinese.html",
    "thank-you-payment-hindi.html", "thank-you-payment-russian.html",
    "thank-you-payment-spanish.html", "thank-you-payment-tagalog.html",
    "thank-you-payment-urdu.html", "thank-you-payment-vietnamese.html",
}


def should_skip(relpath: str) -> bool:
    parts = relpath.split(os.sep)
    for p in parts[:-1]:
        if p in SKIP_DIRS:
            return True
    if parts[-1] in SKIP_FILES:
        return True
    return False


def fix_file(path: str, ver: str) -> tuple[int, str]:
    """Returns (changes_made, note)."""
    rel = os.path.relpath(path, ver)
    with open(path) as f:
        content = f.read()

    # Skip non-HTML-head pages (must have a <title>)
    m = re.search(r"<title>(.*?)</title>", content, re.S)
    title = m.group(1).strip() if m else ""
    if not title:
        return 0, "no-title"

    url = "https://psdepot.com/" + rel.lstrip("./")
    changed = 0

    # 1. canonical
    if "rel=\"canonical\"" not in content and "rel='canonical'" not in content:
        # insert after </title> (first occurrence)
        content = re.sub(
            r"(</title>)",
            r'\1\n<link rel="canonical" href="' + url + r'">',
            content, count=1,
        )
        changed += 1

    # 2. og:image block (image + width + height)
    if "og:image" not in content:
        og_block = (
            f'<meta property="og:image" content="{OG_IMAGE}">\n'
            f'<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">'
        )
        # insert after canonical if present, else after </title>
        if "rel=\"canonical\"" in content:
            content = re.sub(
                r'(rel="canonical" href="[^"]+">)',
                r'\1\n' + og_block,
                content, count=1,
            )
        else:
            content = re.sub(r"(</title>)", r'\1\n' + og_block, content, count=1)
        changed += 1

    # 3. meta description (only if missing AND we have a title to base it on)
    if 'name="description"' not in content and 'name=\'description\'' not in content:
        # Derive a safe description from the title
        desc = f"Performance Supply Depot — {title}. Thermal paper, receipt paper, printer ribbons, and POS supplies. Call (888) 881-6834."
        content = re.sub(
            r"(</title>)",
            r'\1\n<meta name="description" content="' + re.escape(desc) + r'">',
            content, count=1,
        )
        changed += 1

    if changed:
        with open(path, "w") as f:
            f.write(content)
    return changed, ""


def main():
    total = 0
    for ver in VERSIONS:
        count = 0
        skipped = 0
        for dirpath, dirnames, filenames in os.walk(ver):
            dirnames[:] = [d for d in dirnames if d not in (".backups", "ivory-auto-backup", "node_modules")]
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                full = os.path.join(dirpath, fn)
                if should_skip(os.path.relpath(full, ver)):
                    skipped += 1
                    continue
                n, _ = fix_file(full, ver)
                if n:
                    count += 1
        print(f"{ver}: fixed {count} pages (skipped {skipped} app/tool pages)")
        total += count
    print(f"\nTOTAL: {total}")


if __name__ == "__main__":
    main()
