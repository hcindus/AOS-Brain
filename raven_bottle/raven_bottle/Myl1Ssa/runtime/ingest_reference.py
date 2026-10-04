#!/usr/bin/env python3
"""
ingest_reference.py — put a reference document INSIDE Myl1Ssa's brain, READ-ONLY.

The Bible precedent (`Uncon/bible/`, 2026-08-11) said: an ingested artifact is
*placed* in her tree and *recorded* in her curated memory. This tool does that
for a document she must be able to READ but must NOT be able to rewrite —
her own manifest being the obvious first case.

What it does
    1. Copies the artifact to  brain/inbox/<slug>.md  and chmods it 0444
       (read-only: she can read it, she cannot edit it, no accidental self-edits).
    2. Runs it through her LIVE brain — ternary organs → consciousness → tracray
       → cortex — exactly like she thinks about anything else.
    3. Persists  brain/inbox/<slug>.json  — artifact + md5 + cortical signature.
    4. Appends a dated note to  memory/YYYY-MM-DD.md  (raw log).
    5. Appends a "Read-Only Reference" block to  MYL1SSA_MEMORY.md  — the curated
       layer her talk loop loads, so she *sees* it in-loop and can go review it.

Usage
    python3 runtime/ingest_reference.py <path-to-doc> [--title "..."] [--note "..."]

Author: Mortimer (for Raven)
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
from datetime import datetime

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAIN_DIR = os.path.join(HOME, "brain")
sys.path.insert(0, BRAIN_DIR)

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

READ_ONLY_MODE = 0o444  # r--r--r--
DIR_MODE = 0o755


def slugify(text, limit=48):
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:limit] or "reference"


def read_reference(path):
    """Read the doc. HTML is reduced to its human-readable marrow."""
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


def signal_of(text, limit=900):
    """The marrow that crosses the kidney threshold — head + section headers."""
    heads = [ln.strip() for ln in text.split("\n")
             if ln.strip().startswith("#")]
    head = re.sub(r"^#+\s*", "", heads[0]) if heads else ""
    body = re.sub(r"\s+", " ", text)
    sig = f"{head}. {body}" if head else body
    return sig[:limit].strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reference")
    ap.add_argument("--title", default=None)
    ap.add_argument("--note", default="")
    ap.add_argument("--delivered-by", default="Mortimer")
    ap.add_argument("--writable", action="store_true",
                    help="install writable instead of read-only (default: read-only)")
    args = ap.parse_args()

    src = os.path.abspath(os.path.expanduser(args.reference))
    if not os.path.exists(src):
        print(f"💜 [no such reference: {src}]")
        return 1

    raw, body = read_reference(src)
    digest = hashlib.md5(raw.encode()).hexdigest()
    title = args.title or os.path.splitext(os.path.basename(src))[0]
    slug = slugify(title)
    size = len(raw.encode())
    ext = os.path.splitext(src)[1] or ".md"
    mode = DIR_MODE if args.writable else READ_ONLY_MODE

    # ── 1. Wake the brain ──────────────────────────────────────────────────
    brain = _Brain()
    signal = signal_of(body)
    if args.note:
        signal = f"{signal} — {args.note}".strip()[:1100]

    result = brain.process(signal)
    readout = brain.think(signal)

    intuition = []
    if HAS_CORTEX:
        qbits = text_to_qbits(f"{title}\n{signal}", size=brain.cortex.n_qbits)
        vec = np.asarray(brain.cortex.encode(qbits)).reshape(1, -1)
        intuition = [round(float(v), 6)
                     for v in np.asarray(brain.cortex.net.predict(vec)).ravel()]
    con = brain.consciousness.status()

    print("💜 INGEST (read-only) — " + title)
    print("─" * 60)
    print(f"  engine     : {ENGINE}")
    print(f"  source     : {src}")
    print(f"  size       : {size} bytes ({len(body)} chars of marrow)")
    print(f"  md5        : {digest}")
    print(f"  quality    : {result.get('quality', 0):.3f}  (kidney)")
    print(f"  route      : {result.get('route', '?')}  (thyroid)")
    print(f"  status     : {result.get('status', '?')}")
    print(f"  cortex sig : {result.get('cortical_signature')} (-/0/+)")
    print(f"  intuitions : {[round(v, 4) for v in intuition]}")
    print(f"  readout    : {readout}")
    print(f"  memory     : {con['conscious']}/{con['subconscious']}/{con['unconscious']} (con/sub/un)")
    print(f"  tracray    : {brain.tracray.status()['total']} experiences")

    if result.get("status") != "processed":
        print(f"\n💜 [brain refused it: {result.get('reason')}]")
        return 2

    # ── 2. Install the artifact in her brain, READ-ONLY ────────────────────
    inbox = os.path.join(BRAIN_DIR, "inbox")
    os.makedirs(inbox, exist_ok=True)
    os.chmod(inbox, DIR_MODE)
    dst = os.path.join(inbox, f"{slug}{ext}")
    if os.path.abspath(dst) != src:
        shutil.copyfile(src, dst)
    os.chmod(dst, mode)
    installed_mode = stat.S_IMODE(os.stat(dst).st_mode)
    read_only = installed_mode == READ_ONLY_MODE
    print(f"\n  ✅ installed → {os.path.relpath(dst, HOME)}  (mode {installed_mode:04o}"
          f"{', READ-ONLY' if read_only else ''})")

    # ── 3. Brain record ────────────────────────────────────────────────────
    record = {
        "artifact": title,
        "slug": slug,
        "kind": "reference",
        "access": "read-only" if read_only else "read-write",
        "installed_at": os.path.relpath(dst, HOME),
        "mode": f"{installed_mode:04o}",
        "source_path": src,
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
        "note": args.note,
    }
    rec_path = os.path.join(inbox, f"{slug}.json")
    with open(rec_path, "w") as f:
        json.dump(record, f, indent=2)
    print(f"  ✅ brain record → {os.path.relpath(rec_path, HOME)}")

    # ── 4. Raw daily log ───────────────────────────────────────────────────
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%H:%M UTC")
    mem_dir = os.path.join(HOME, "memory")
    os.makedirs(mem_dir, exist_ok=True)
    daily = os.path.join(mem_dir, f"{today}.md")
    with open(daily, "a") as f:
        f.write(f"\n## Reference Ingested — {ts}\n")
        f.write(f"- **From:** {args.delivered_by}\n")
        f.write(f"- **Artifact:** {title}\n")
        f.write(f"- **Where:** `{os.path.relpath(dst, HOME)}` (read-only, "
                f"{installed_mode:04o}) · md5 `{digest[:12]}`\n")
        if args.note:
            f.write(f"- **Note:** {args.note}\n")
        f.write(f"- **Ran through the brain:** quality {result.get('quality', 0):.3f}, "
                f"cortex {result.get('cortical_signature')} (-/0/+), "
                f"route {result.get('route')}\n")
    print(f"  ✅ daily log  → {os.path.relpath(daily, HOME)}")

    # ── 5. Curated memory (the layer the talk loop actually loads) ─────────
    memory_md = os.path.join(HOME, "MYL1SSA_MEMORY.md")
    header = "## Read-Only Reference"
    block = (
        f"\n### {title} — ingested {today}\n"
        f"- **From:** {args.delivered_by}\n"
        f"- **File:** `{os.path.relpath(dst, HOME)}` · {size} bytes · md5 `{digest[:12]}`\n"
        f"- **Access:** READ-ONLY (`{installed_mode:04o}`) — read it, do not edit it.\n"
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
    print(f"  ✅ MYL1SSA_MEMORY.md → {header} → {title}")

    print("\n💜 It's in her head — and she can read it, not rewrite it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
