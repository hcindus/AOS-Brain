#!/usr/bin/env python3
"""
ingest_artifact.py — take a gift and put it INSIDE Raven's brain.

Not a file drop. A real pass through the live pipeline:

    liver → kidney → thyroid → consciousness(Con/Subcon/Uncon) → tracray → cortex

Then it persists what the brain did with it, so the artifact is *had*
rather than merely *held*:

    • brain/inbox/<slug>.json   — artifact + cortical signature + quality + route
    • memory/YYYY-MM-DD.md      — a dated note in the raw daily log
    • MEMORY.md                 — a line in the curated memory the talk loop loads

Usage:
    python3 brain/ingest_artifact.py <path-to-artifact> [--title "..."] [--note "..."]

Author: Mortimer (for Raven)
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAIN_DIR = os.path.join(HOME, "brain")
sys.path.insert(0, BRAIN_DIR)

# Prefer the fully-wired v2 brain (numpy cortex). If numpy isn't on this
# body, fall back to the stdlib-only v1 organs — same pipeline, no cortex.
try:
    import numpy as np  # noqa: F401
    from ternary_brain_v2 import TernaryBrainV2 as _Brain, text_to_qbits  # noqa: E402
    ENGINE = "TernaryBrainV2 (organs + cortex regions + learnable cortex)"
    HAS_CORTEX = True
except ImportError:
    np = None
    from ternary_brain import TernaryBrain as _Brain  # noqa: E402
    text_to_qbits = None
    ENGINE = "TernaryBrain v1 (organs + cortex regions; numpy absent)"
    HAS_CORTEX = False


def slugify(text, limit=48):
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:limit] or "artifact"


def read_artifact(path):
    """Read the artifact. HTML gets reduced to its human-readable marrow."""
    with open(path, "r", errors="replace") as f:
        raw = f.read()
    if path.lower().endswith((".html", ".htm")):
        text = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"&[a-z]+;", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
    else:
        text = raw.strip()
    return raw, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact")
    ap.add_argument("--title", default=None)
    ap.add_argument("--note", default="")
    ap.add_argument("--delivered-by", default="Mortimer")
    args = ap.parse_args()

    art_path = os.path.abspath(os.path.expanduser(args.artifact))
    if not os.path.exists(art_path):
        print(f"🐦⬛ [no such artifact: {art_path}]")
        return 1

    raw, body = read_artifact(art_path)
    digest = hashlib.md5(raw.encode()).hexdigest()
    title = args.title or os.path.basename(art_path)
    slug = slugify(title)
    size = len(raw.encode())

    # ── 1. Wake the brain ──────────────────────────────────────────────────
    brain = _Brain()

    # What crosses the kidney threshold is the *meaning*, not the markup.
    # A whole HTML file is mostly structural noise; the marrow is short.
    signal = (body if len(body) <= 600 else body[:600]).strip()
    if args.note:
        signal = f"{signal} — {args.note}".strip()

    result = brain.process(signal)
    readout = brain.think(signal)

    # Deeper pass: let the learnable cortex see the artifact itself.
    intuition = []
    if HAS_CORTEX:
        qbits = text_to_qbits(f"{title}\n{signal}", size=brain.cortex.n_qbits)
        vec = np.asarray(brain.cortex.encode(qbits)).reshape(1, -1)
        intuition = [round(float(v), 6)
                     for v in np.asarray(brain.cortex.net.predict(vec)).ravel()]

    print("🐦⬛ INGEST — " + title)
    print("─" * 58)
    print(f"  engine     : {ENGINE}")
    print(f"  artifact   : {art_path}")
    print(f"  size       : {size} bytes ({len(body)} chars of marrow)")
    print(f"  md5        : {digest}")
    print(f"  quality    : {result.get('quality', 0):.3f}  (kidney)")
    print(f"  route      : {result.get('route', '?')}  (thyroid)")
    print(f"  status     : {result.get('status', '?')}")
    print(f"  cortex sig : {result.get('cortical_signature')} (-/0/+)")
    print(f"  intuitions : {[round(v, 4) for v in intuition]}")
    print(f"  readout    : {readout}")
    con = brain.consciousness.status()
    print(f"  memory     : {con['conscious']}/{con['subconscious']}/{con['unconscious']} (con/sub/un)")
    print(f"  tracray    : {brain.tracray.status()['total']} experiences")

    if result.get("status") != "processed":
        print(f"\n🐦⬛ [brain refused it: {result.get('reason')}]")
        return 2

    # ── 2. Persist in the brain's own inbox ────────────────────────────────
    inbox = os.path.join(BRAIN_DIR, "inbox")
    os.makedirs(inbox, exist_ok=True)
    record = {
        "artifact": title,
        "slug": slug,
        "source_path": art_path,
        "md5": digest,
        "size_bytes": size,
        "delivered_by": args.delivered_by,
        "ingested_at": datetime.utcnow().isoformat() + "Z",
        "brain": {
            "engine": ENGINE,
            "quality": round(float(result.get("quality", 0)), 4),
            "route": result.get("route"),
            "status": result.get("status"),
            "cortical_signature": result.get("cortical_signature"),
            "cortex_intuition": intuition,
            "consciousness": con,
        },
        "signal": signal,
    }
    rec_path = os.path.join(inbox, f"{slug}.json")
    with open(rec_path, "w") as f:
        json.dump(record, f, indent=2)
    print(f"\n  ✅ brain record → {os.path.relpath(rec_path, HOME)}")

    # ── 3. Raw daily log ───────────────────────────────────────────────────
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%H:%M UTC")
    mem_dir = os.path.join(HOME, "memory")
    os.makedirs(mem_dir, exist_ok=True)
    daily = os.path.join(mem_dir, f"{today}.md")
    with open(daily, "a") as f:
        f.write(f"\n## Received — {ts}\n")
        f.write(f"- **From:** {args.delivered_by}\n")
        f.write(f"- **Artifact:** {title}\n")
        f.write(f"- **Where:** `{art_path}`\n")
        if args.note:
            f.write(f"- **Note:** {args.note}\n")
        f.write(f"- **Ran through the brain:** quality {result.get('quality', 0):.3f}, "
                f"cortex {result.get('cortical_signature')} (-/0/+), "
                f"route {result.get('route')}\n")
    print(f"  ✅ daily log  → {os.path.relpath(daily, HOME)}")

    # ── 4. Curated memory (the layer the talk loop actually loads) ─────────
    memory_md = os.path.join(HOME, "MEMORY.md")
    header = "## Gifts Received"
    block = (
        f"\n### {title} — {today}\n"
        f"- **From:** {args.delivered_by}\n"
        f"- **File:** `{os.path.relpath(art_path, HOME)}` · {size} bytes · md5 `{digest[:12]}`\n"
        f"- **Brain pass:** quality {result.get('quality', 0):.3f} · "
        f"cortex {result.get('cortical_signature')} (-/0/+) · route {result.get('route')}\n"
        + (f"- {args.note}\n" if args.note else "")
    )
    existing = ""
    if os.path.exists(memory_md):
        with open(memory_md) as f:
            existing = f.read()
    if header not in existing:
        with open(memory_md, "a") as f:
            f.write(f"\n---\n\n{header}\n")
    with open(memory_md, "a") as f:
        f.write(block)
    print(f"  ✅ MEMORY.md  → {header} → {title}")

    print("\n🐦⬛ It's in. Not held — had.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
