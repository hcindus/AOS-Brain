#!/usr/bin/env python3
"""Final nav-centering pass: catch every remaining variant of the broken rule.

Variants found:
1. minified single-line `.main-nav .container { display: flex; gap: 4px; flex-wrap: wrap; }`
2. minified no-space `.main-nav .container{display:flex;gap:4px;flex-wrap:wrap}`
3. multi-line with padding but no max-width/margin (products/index, blog/index)
4. `.main-nav .nav-wrap` (services/installation) — already centered, skip

For any `.main-nav .container` (or `.nav-wrap`) rule lacking `max-width`, inject
`max-width: 1200px; margin: 0 auto;`.
"""
import os
import re

VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]


def fix_file(path: str) -> bool:
    with open(path) as f:
        content = f.read()

    # Only touch pages that have nav markup
    if 'nav class="main-nav"' not in content:
        return False

    changed = False

    # Match any .main-nav .container or .main-nav .nav-wrap rule block
    # (handles minified single-line and multi-line variants)
    pattern = re.compile(
        r'(\.main-nav \.(?:container|nav-wrap)\s*\{[^}]*?\})',
        re.S,
    )

    def repl(m):
        rule = m.group(1)
        if "max-width" in rule:
            return rule  # already centered
        # inject max-width + margin auto right after the opening brace
        return rule.replace("{", "{ max-width: 1200px; margin: 0 auto; ", 1)

    new_content = pattern.sub(repl, content)
    if new_content != content:
        content = new_content
        changed = True

    if changed:
        with open(path, "w") as f:
            f.write(content)
    return changed


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
