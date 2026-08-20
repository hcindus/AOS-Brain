#!/usr/bin/env python3
"""
Ensure every page header shows the full contact block:
logo + blinking 888 + 415 + email.
Adds the missing 415 number and email anchors right after the 888 anchor
inside each <header>. Idempotent.
"""
import os
import re

SITE = "/var/www/psdepot.com"
SKIP_DIRS = {".git", ".backups", "node_modules", "__pycache__"}

ANCHOR_888 = '<a href="tel:888-881-6834" class="patriotic-phone" style="text-decoration:none;">📞 (888) 881-6834</a>'
ANCHOR_415 = '<a href="tel:415-571-9724" style="text-decoration:none;">📞 (415) 571-9724</a>'
ANCHOR_EMAIL = '<a href="mailto:info@psdepot.com" style="text-decoration:none;">✉️ info@psdepot.com</a>'

# The full trio to place (888 blinking + 415 + email)
TRIO = ANCHOR_888 + ' ' + ANCHOR_415 + ' ' + ANCHOR_EMAIL


def fix_header(html: str) -> (str, bool):
    """Ensure the <header> contains 888 + 415 + email. Returns (html, changed)."""
    hm = re.search(r"<header.*?</header>", html, re.S)
    if not hm:
        return html, False
    header = hm.group(0)
    changed = False

    # Case 1: header already has all three → done
    has_888 = "881-6834" in header
    has_415 = "415-571-9724" in header or "571-9724" in header
    has_email = "info@psdepot.com" in header
    if has_888 and has_415 and has_email:
        return html, False

    # Case 2: has 888 but missing 415 and/or email → insert after the 888 anchor
    if has_888:
        m888 = re.search(r'<a[^>]*href="tel:888-881-6834"[^>]*>.*?</a>', header, re.S)
        if m888:
            anchor = m888.group(0)
            additions = ""
            if not has_415:
                additions += " " + ANCHOR_415
            if not has_email:
                additions += " " + ANCHOR_415 if False else (" " + ANCHOR_EMAIL if not has_415 else " " + ANCHOR_EMAIL)
            # Build cleanly
            to_add = []
            if not has_415:
                to_add.append(ANCHOR_415)
            if not has_email:
                to_add.append(ANCHOR_EMAIL)
            insert = anchor + (" " + " ".join(to_add) if to_add else "")
            new_header = header.replace(anchor, insert, 1)
            html = html.replace(header, new_header, 1)
            return html, True

    # Case 3: no 888 at all (shouldn't happen post-injection) → inject full trio
    # Append trio right before </header>
    new_header = header[:-len("</header>")] + '<div style="text-align:center;padding:6px 0;">' + TRIO + '</div>' + "</header>"
    html = html.replace(header, new_header, 1)
    return html, True


def main():
    updated = 0
    unchanged = 0
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fp = os.path.join(root, fname)
            try:
                with open(fp, encoding="utf-8", errors="ignore") as f:
                    html = f.read()
            except Exception:
                continue
            html2, changed = fix_header(html)
            if changed:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(html2)
                updated += 1
            else:
                unchanged += 1
    print(f"Updated: {updated}")
    print(f"Unchanged (already full): {unchanged}")


if __name__ == "__main__":
    main()
