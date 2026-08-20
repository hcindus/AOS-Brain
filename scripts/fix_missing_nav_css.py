#!/usr/bin/env python3
"""Inject .main-nav CSS into pages that have nav markup but no .main-nav CSS.

Root cause: add_nav_public_pages.py injected the nav <nav> markup correctly, but
its CSS injection used replace('    </style>', ...) which FAILED on pages with a
minified single-line <style> block (no 4-space-indented </style>). Result: nav
markup exists but has zero styling -> left-justified unstyled links.

This script finds pages with nav markup but missing .main-nav CSS, and inserts
the full .main-nav CSS rule set immediately before the closing </style> tag,
regardless of indentation.
"""
import os
import re

VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]

NAV_CSS = """.main-nav {
            background: #12283f;
            border-bottom: 3px solid var(--accent);
        }
        .main-nav .container {
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
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


def fix_file(path: str) -> bool:
    with open(path) as f:
        content = f.read()

    # Must have nav markup but no .main-nav CSS
    if 'nav class="main-nav"' not in content:
        return False
    if ".main-nav" in content:
        return False
    if "</style>" not in content:
        return False

    # Insert CSS before the closing </style> tag
    content = content.replace("</style>", NAV_CSS + "</style>", 1)
    with open(path, "w") as f:
        f.write(content)
    return True


def main():
    total = 0
    for ver in VERSIONS:
        count = 0
        for dirpath, dirnames, filenames in os.walk(ver):
            dirnames[:] = [d for d in dirnames if d not in (".backups", "ivory-auto-backup", "node_modules")]
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                if fix_file(os.path.join(dirpath, fn)):
                    count += 1
        print(f"{ver}: fixed {count} pages")
        total += count
    print(f"\nTOTAL: {total}")


if __name__ == "__main__":
    main()
