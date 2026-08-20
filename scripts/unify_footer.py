#!/usr/bin/env python3
"""
Unify every customer-facing page's footer to a single self-contained (inline-styled)
footer — company name, blinking 888 + 415 + email, Authorized Dealer line,
service-areas link, and copyright. Matches the header unification approach.
"""
import os
import re

SITE = "/var/www/psdepot.com"
SKIP_DIRS = {".git", ".backups", "node_modules", "__pycache__"}
INTERNAL_DIRS = {"admin", "api", "data", "scripts", "widget", "depotchaos",
                 "leads-dashboard", "leads-portal", "invoices", "cgi-bin", "downloads"}
INTERNAL_FILES = {
    "kb-admin.html", "cart-test.html", "chat-demo.html", "psd_dashboard.html",
    "brain-dashboard.html", "service-log.html", "RS-79_demo.html",
    "pollo_asados_demo.html", "site-tree.html",
}

FOOTER = (
    '<footer style="background:#0A1A2F;color:#fff;padding:28px 24px;text-align:center;font-size:14px;">'
    '<div style="max-width:900px;margin:0 auto;">'
    '<p style="margin:0 0 10px;font-size:16px;"><strong>Performance Supply Depot LLC</strong></p>'
    '<p style="margin:0 0 6px;">'
    '📞 <a href="tel:888-881-6834" class="patriotic-phone" style="text-decoration:none;font-weight:700;">(888) 881-6834</a>'
    ' &nbsp;|&nbsp; 📞 <a href="tel:415-571-9724" style="color:#bee3f8;text-decoration:none;">(415) 571-9724</a>'
    ' &nbsp;|&nbsp; ✉️ <a href="mailto:info@psdepot.com" style="color:#bee3f8;text-decoration:none;">info@psdepot.com</a>'
    '</p>'
    '<p style="margin:0 0 6px;color:#94a3b8;font-size:13px;">Authorized Dealer: '
    '<strong>SAM4S</strong> · <strong>CAS</strong> · <strong>ACM Technologies</strong> · '
    '<strong>TST Impresso</strong> · <strong>Capton</strong></p>'
    '<p style="margin:0 0 10px;"><a href="/locations.html" style="color:#bee3f8;text-decoration:none;">📍 Service Areas</a>'
    ' &nbsp;·&nbsp; <a href="/contact.html" style="color:#bee3f8;text-decoration:none;">📞 Contact Us</a></p>'
    '<p style="margin:0;color:#64748b;font-size:12px;">© 2026 Performance Supply Depot LLC. All rights reserved. Serving California since 2005.</p>'
    '</div></footer>'
)


def replace_footer(html: str):
    new_html, n = re.subn(r"<footer[^>]*>.*?</footer>", FOOTER, html, count=1, flags=re.S)
    return new_html, n


def main():
    updated, skipped, no_footer = 0, 0, 0
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and d not in INTERNAL_DIRS]
        for fname in files:
            if not fname.endswith(".html") or fname in INTERNAL_FILES:
                continue
            fp = os.path.join(root, fname)
            try:
                with open(fp, encoding="utf-8", errors="ignore") as f:
                    html = f.read()
            except Exception:
                continue
            if "<footer" not in html:
                no_footer += 1
                continue
            new_html, n = replace_footer(html)
            if n == 0:
                no_footer += 1
                continue
            if new_html == html:
                skipped += 1
                continue
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_html)
            updated += 1
    print(f"Updated: {updated}")
    print(f"Skipped (already unified): {skipped}")
    print(f"No footer: {no_footer}")


if __name__ == "__main__":
    main()
