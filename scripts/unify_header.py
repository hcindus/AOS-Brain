#!/usr/bin/env python3
"""
Unify every page's header to a single self-contained (inline-styled) header
so it renders identically site-wide — no text jumping, no CSS-context drift.

The header is fully inline-styled (does not depend on each page's --primary/
--accent/--logo CSS), so it looks the same everywhere. It includes:
  logo "PerformanceSupplyDepot", blinking 888 number, 415, email, cart.

Replaces <header>...</header> on every .html page. The blinking 888 relies on
the @keyframes patriotic-blink + .patriotic-phone CSS already injected site-wide.
"""
import os
import re

SITE = "/var/www/psdepot.com"
SKIP_DIRS = {".git", ".backups", "node_modules", "__pycache__"}

# Internal / backend / utility dirs — NOT customer-facing, skip.
INTERNAL_DIRS = {"admin", "api", "data", "scripts", "widget", "depotchaos",
                 "leads-dashboard", "leads-portal", "invoices", "cgi-bin", "downloads"}

# Internal / diagnostic / demo pages — have page-specific header content, skip.
INTERNAL_FILES = {
    "kb-admin.html", "cart-test.html", "chat-demo.html", "psd_dashboard.html",
    "brain-dashboard.html", "service-log.html", "RS-79_demo.html",
    "pollo_asados_demo.html", "site-tree.html",
}

# Self-contained header — inline styles only, matching index.html look.
HEADER = (
    '<header style="background:#0A1A2F;color:#fff;padding:14px 0;box-shadow:0 2px 4px rgba(0,0,0,0.12);">'
    '<div style="max-width:1200px;margin:0 auto;padding:0 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">'
    '<a href="/" style="font-size:23px;font-weight:800;color:#fff;text-decoration:none;line-height:1.2;">'
    'Performance<span style="color:#63b3ed;">Supply</span>Depot</a>'
    '<div style="display:flex;gap:20px;flex-wrap:wrap;align-items:center;font-size:14px;">'
    '<a href="tel:888-881-6834" class="patriotic-phone" style="text-decoration:none;font-weight:700;">📞 (888) 881-6834</a>'
    '<a href="tel:415-571-9724" style="color:#bee3f8;text-decoration:none;font-weight:500;">📞 (415) 571-9724</a>'
    '<a href="mailto:info@psdepot.com" style="color:#bee3f8;text-decoration:none;font-weight:500;">✉️ info@psdepot.com</a>'
    '<a href="/checkout.html" style="background:#c53030;color:#fff;padding:8px 16px;border-radius:20px;font-weight:600;text-decoration:none;line-height:1;">'
    '🛒 Cart (<span id="cart-count">0</span>)</a>'
    '</div></div></header>'
)


def replace_header(html: str):
    """Replace the first <header>...</header> with the unified header."""
    new_html, n = re.subn(r"<header[^>]*>.*?</header>", HEADER, html, count=1, flags=re.S)
    return new_html, n


def main():
    updated, skipped = 0, 0
    missing = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and d not in INTERNAL_DIRS]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            if fname in INTERNAL_FILES:
                continue
            fp = os.path.join(root, fname)
            try:
                with open(fp, encoding="utf-8", errors="ignore") as f:
                    html = f.read()
            except Exception:
                continue
            if "<header" not in html:
                missing.append(fp)
                continue
            new_html, n = replace_header(html)
            if n == 0:
                missing.append(fp)
                continue
            if new_html == html:
                skipped += 1
                continue
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_html)
            updated += 1

    print(f"Updated: {updated}")
    print(f"Skipped (already unified): {skipped}")
    print(f"Missing/no header: {len(missing)}")
    for m in missing[:20]:
        print("  ! " + m)


if __name__ == "__main__":
    main()
