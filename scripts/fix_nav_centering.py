#!/usr/bin/env python3
"""Center the main-nav on pages whose .main-nav .container lacks max-width.

These pages have:
    .main-nav .container { display: flex; gap: 4px; flex-wrap: wrap; }
but NO base `.container { max-width: 1200px; margin: 0 auto; ... }` rule, so the
nav stretches full-width and left-aligns instead of centering under the header.

Fix: add max-width + margin auto to the .main-nav .container rule.
"""
import os
import re

VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]

# The broken rule (no max-width / margin)
OLD_RULE = """        .main-nav .container {
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
        }"""

# The fixed rule (centered, matching the header's 1200px + 24px padding)
NEW_RULE = """        .main-nav .container {
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
        }"""


def fix_file(path: str) -> bool:
    with open(path) as f:
        content = f.read()
    if OLD_RULE not in content:
        return False
    content = content.replace(OLD_RULE, NEW_RULE, 1)
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
