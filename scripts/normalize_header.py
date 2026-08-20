#!/usr/bin/env python3
"""
Normalize the header of 4 core pages to match index.html's reference header:
logo + contact-info (888 blinking + 415 + email + cart), wrapped in .container.

For each page: replace <header>...</header> with the standard block, and
inject any missing CSS (.contact-info, .cart-icon, .header-content, .logo, header bg).
"""
import os
import re

SITE = "/var/www/psdepot.com"
FILES = ["blog/index.html", "about.html", "locations.html", "contact.html"]

STANDARD_HEADER = """    <header>
        <div class="container">
            <div class="header-content">
                <a href="/" class="logo">Performance<span>Supply</span>Depot</a>
                <div class="contact-info">
                    <a href="tel:888-881-6834" class="patriotic-phone" style="text-decoration: none;">📞 (888) 881-6834</a>
                    <a href="tel:415-571-9724" style="text-decoration: none;">📞 (415) 571-9724</a>
                    <a href="mailto:info@psdepot.com" style="text-decoration: none;">✉️ info@psdepot.com</a>
                    <a href="/checkout.html" class="cart-icon">
                        🛒 Cart (<span id="cart-count">0</span>)
                    </a>
                </div>
            </div>
        </div>
    </header>"""

# CSS rules to ensure exist (each checked individually)
CSS_BLOCKS = {
    "header_bg": "header { background: var(--primary); color: white; padding: 16px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }",
    "header_content": ".header-content { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }",
    "logo": ".logo { font-size: 24px; font-weight: 800; color: white; text-decoration: none; }",
    "logo_span": ".logo span { color: #63b3ed; }",
    "contact_info": ".contact-info { display: flex; gap: 24px; flex-wrap: wrap; font-size: 14px; }",
    "contact_info_a": ".contact-info a { color: #bee3f8; text-decoration: none; font-weight: 500; }",
    "contact_info_hover": ".contact-info a:hover { color: white; text-decoration: underline; }",
    "cart_icon": ".cart-icon { background: var(--accent, #FF7A00); color: white !important; padding: 8px 16px; border-radius: 20px; font-weight: 600; }",
}


def ensure_css(html: str) -> str:
    """Inject any missing CSS rules into the first <style> block."""
    # determine which selectors are present
    def has(selector):
        return selector in html

    missing = []
    if not has(".contact-info"):
        missing.append(CSS_BLOCKS["contact_info"])
        missing.append(CSS_BLOCKS["contact_info_a"])
        missing.append(CSS_BLOCKS["contact_info_hover"])
    if not has(".cart-icon"):
        missing.append(CSS_BLOCKS["cart_icon"])
    # header-content / logo / header bg — only add if page lacks them
    if not has(".header-content"):
        missing.append(CSS_BLOCKS["header_content"])
    if not has(".logo"):
        missing.append(CSS_BLOCKS["logo"])
        missing.append(CSS_BLOCKS["logo_span"])

    if not missing:
        return html

    block = "\n        /* Standard header (normalized) */\n        " + "\n        ".join(missing) + "\n"
    m = re.search(r"<style[^>]*>", html)
    if m:
        html = html[: m.end()] + "\n" + block + html[m.end():]
    return html


def main():
    for rel in FILES:
        fp = os.path.join(SITE, rel)
        if not os.path.exists(fp):
            print(f"! missing {rel}")
            continue
        html = open(fp, encoding="utf-8", errors="ignore").read()

        # Replace the header block (non-greedy from <header to </header>)
        new_html, n = re.subn(r"<header.*?</header>", STANDARD_HEADER, html, count=1, flags=re.S)
        if n == 0:
            print(f"! no <header> found in {rel}")
            continue

        # Ensure CSS present
        new_html = ensure_css(new_html)

        open(fp, "w", encoding="utf-8").write(new_html)
        print(f"+ normalized {rel}")
    print("done")


if __name__ == "__main__":
    main()
