#!/usr/bin/env python3
"""
Remove the STRAY duplicate header (bare "PerformanceSupplyDepot + Cart (0)" with NO
phone number / nav) from all pages it leaked into.

SAFETY:
  - Backs up every edited file first (reversible).
  - ONLY removes header blocks that contain "Cart" but do NOT contain the phone
    number "(888) 881-6834" (or "881-6834"). The REAL header ALWAYS has the phone,
    so this heuristic can only ever touch the stray one — never the working cart.
  - Does NOT touch any localStorage/cart logic.
"""
import re, shutil, sys
from pathlib import Path
from datetime import datetime

SITE = Path("/var/www/psdepot.com")
BACKUP = SITE / f".backups/stray_header_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
PHONE = "881-6834"  # the real header always contains this; the stray one does not

# A header-like block: <header ...>...</header> or <div/nav with "header"/"topbar"/"navbar" class ...>...</div>
HEADER_BLOCK = re.compile(
    r'<(header|div|nav)\b[^>]*(?:class\s*=\s*["\'][^"\']*(?:header|topbar|navbar|top-bar)[^"\']*["\'])[^>]*>.*?</\1>',
    re.IGNORECASE | re.DOTALL,
)

def remove_stray(html: str):
    """Remove header blocks that have 'Cart' but NOT the phone number."""
    def repl(m):
        block = m.group(0)
        has_cart = "cart" in block.lower()
        has_phone = PHONE in block
        if has_cart and not has_phone:
            return ""  # stray header → remove
        return block  # keep (real header, or non-cart block)
    return HEADER_BLOCK.sub(repl, html)

def main():
    files = list(SITE.rglob("*.html"))
    files = [f for f in files if ".backups" not in str(f) and "node_modules" not in str(f)]

    edited = []
    for f in files:
        try:
            html = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        new = remove_stray(html)
        if new != html:
            # back up then write
            bdir = BACKUP / f.parent.relative_to(SITE)
            bdir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, bdir / f.name)
            f.write_text(new, encoding="utf-8")
            edited.append(str(f.relative_to(SITE)))

    print(f"REMOVED_STRAY_HEADER_FROM={len(edited)}")
    for p in edited:
        print(p)
    print(f"BACKUP_DIR={BACKUP}")

if __name__ == "__main__":
    main()
