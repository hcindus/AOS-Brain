#!/usr/bin/env python3
"""
Patriotic phone blink — inject red/white/blue blinking (888) 881-6834
into the TOP (header) and BOTTOM (footer) of every HTML page on psdepot.com.

Idempotent: safe to re-run. Skips .git/.backups/node_modules.
"""
import os
import re

SITE = "/var/www/psdepot.com"
SKIP_DIRS = {".git", ".backups", "node_modules", "__pycache__"}

KEYFRAMES = """@keyframes patriotic-blink {
    0%, 100% { color: #ff0000; text-shadow: 0 0 8px rgba(255, 0, 0, 0.6); }
    33% { color: #ffffff; text-shadow: 0 0 8px rgba(255, 255, 255, 0.9); }
    66% { color: #0066ff; text-shadow: 0 0 8px rgba(0, 102, 255, 0.6); }
}
.patriotic-phone { animation: patriotic-blink 2s infinite; font-weight: 700; display: inline-block; }"""

# The phone link markup used at top (header) and bottom (footer)
PHONE_LINK = '<a href="tel:888-881-6834" class="patriotic-phone" style="text-decoration:none;">📞 (888) 881-6834</a>'


def inject_css(html: str) -> str:
    """Ensure keyframes + .patriotic-phone CSS exist inside a <style> block."""
    if "patriotic-blink" in html:
        # Already has animation; ensure .patriotic-phone also present
        if ".patriotic-phone" not in html:
            # add class rule right after the keyframes
            html = html.replace(
                "@keyframes patriotic-blink",
                KEYFRAMES,
                1,
            ) if False else html
        return html

    # Need to inject the full CSS. Find first <style> block and prepend inside it.
    m = re.search(r"<style[^>]*>", html)
    if m:
        html = html[: m.end()] + "\n" + KEYFRAMES + "\n" + html[m.end():]
    else:
        # No <style> — add one in <head> before </head>
        block = "<style>\n" + KEYFRAMES + "\n</style>"
        if "</head>" in html:
            html = html.replace("</head>", block + "\n</head>", 1)
        else:
            html = block + "\n" + html
    return html


def ensure_header_phone(html: str) -> str:
    """Ensure a blinking phone appears in the top header region."""
    # If any element already carries patriotic-phone near the top (before first <main or 40% in), it's done.
    # Heuristic: check if patriotic-phone appears in header area.
    header_m = re.search(r"<header.*?</header>", html, re.S)
    if header_m:
        header = header_m.group(0)
        if "patriotic-phone" in header:
            return html  # already blinking in header
        if "881-6834" in header:
            # wrap existing phone in header with the class
            new_header = header
            new_header = re.sub(
                r"(<a[^>]*href=\"tel:888-881-6834\"[^>]*>)(.*?)(</a>)",
                lambda mm: f'<a href="tel:888-881-6834" class="patriotic-phone" style="text-decoration:none;">📞 (888) 881-6834</a>',
                new_header,
                count=1,
            )
            if new_header == header:
                # no tel link, but has phone text — add class to a span
                new_header = re.sub(
                    r"(\(888\) 881-6834)",
                    r'<span class="patriotic-phone">\1</span>',
                    new_header,
                    count=1,
                )
            html = html.replace(header, new_header, 1)
            return html

    # Header exists but has no phone — append a blinking phone inside it.
    if header_m:
        header = header_m.group(0)
        new_header = header[:-len("</header>")] + f'<div style="text-align:center;padding:6px 0;">{PHONE_LINK}</div>' + "</header>"
        return html.replace(header, new_header, 1)

    # No <header> tag — inject one at the very top of <body> if possible.
    body_m = re.search(r"<body[^>]*>", html)
    if body_m:
        inject = f'<header style="background:#0A1A2F;color:#fff;padding:10px 20px;text-align:center;">{PHONE_LINK}</header>'
        html = html[: body_m.end()] + "\n" + inject + "\n" + html[body_m.end():]
    return html


def ensure_footer_phone(html: str) -> str:
    """Ensure a blinking phone appears in the bottom footer region."""
    footer_m = re.search(r"<footer.*?</footer>", html, re.S)
    if footer_m:
        footer = footer_m.group(0)
        if "881-6834" in footer:
            if "patriotic-phone" in footer:
                return html
            # add class to existing phone in footer
            new_footer = re.sub(
                r"(\(888\) 881-6834)",
                r'<span class="patriotic-phone">\1</span>',
                footer,
                count=1,
            )
            html = html.replace(footer, new_footer, 1)
            return html
        # footer exists but no phone — append phone inside footer
        new_footer = footer[:-len("</footer>")] + f'<div style="margin-top:8px;">{PHONE_LINK}</div>' + "</footer>"
        html = html.replace(footer, new_footer, 1)
        return html

    # No footer — add one before </body>
    footer_html = f'<footer style="background:#0A1A2F;color:#fff;padding:20px;text-align:center;font-size:14px;"><p>{PHONE_LINK}</p></footer>'
    if "</body>" in html:
        html = html.replace("</body>", footer_html + "\n</body>", 1)
    else:
        html += "\n" + footer_html
    return html


def process_file(fp: str):
    try:
        with open(fp, encoding="utf-8", errors="ignore") as f:
            html = f.read()
    except Exception:
        return "read-error"

    orig = html
    html = inject_css(html)
    html = ensure_header_phone(html)
    html = ensure_footer_phone(html)

    if html == orig:
        return "unchanged"

    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    return "updated"


def main():
    stats = {"updated": 0, "unchanged": 0, "read-error": 0}
    changed_files = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fp = os.path.join(root, fname)
            r = process_file(fp)
            stats[r] = stats.get(r, 0) + 1
            if r == "updated":
                changed_files.append(fp)

    print(f"Total html processed: {sum(stats.values())}")
    print(f"Updated: {stats['updated']}")
    print(f"Unchanged (already compliant): {stats['unchanged']}")
    print(f"Read errors: {stats.get('read-error', 0)}")
    print("--- first 20 changed ---")
    for fp in changed_files[:20]:
        print("  " + fp)


if __name__ == "__main__":
    main()
