#!/usr/bin/env python3
"""Remove ALL breadcrumb blocks (div + nav variants) from psdepot.com pages.

Handles:
  <div class="breadcrumb"> ... </div>
  <nav class="breadcrumb"> ... </nav>

Both are multi-line and redundant with the main nav. Removes the whole block
including the leading/trailing blank lines. Leaves the CSS rules (harmless).
"""
import os
import re

VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]
ROOT = None  # set per version

# Match a breadcrumb block: opening tag ... closing tag, across lines, non-greedy.
BLOCK_RE = re.compile(
    r'\n?\s*<(div|nav) class="breadcrumb">.*?</\1>\s*\n',
    re.S,
)


def strip_breadcrumbs(path: str) -> bool:
    with open(path) as f:
        content = f.read()
    new, n = BLOCK_RE.subn("", content)
    if n == 0:
        return False
    with open(path, "w") as f:
        f.write(new)
    return True


def main():
    total = 0
    for ver in VERSIONS:
        root = ver
        count = 0
        for dirpath, dirnames, filenames in os.walk(root):
            # skip backups
            dirnames[:] = [d for d in dirnames if d not in (".backups", "ivory-auto-backup")]
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                path = os.path.join(dirpath, fn)
                if strip_breadcrumbs(path):
                    count += 1
        print(f"{ver}: removed breadcrumb from {count} pages")
        total += count
    print(f"\nTOTAL pages cleaned: {total}")


if __name__ == "__main__":
    main()
