#!/usr/bin/env python3
# VERSION: v1.0
"""
memory_index.py — what Raven knows she has, before she asks.
===========================================================
Project 5912 · Myl1Ssa (Raven).

Injected into her prompt every message. Two jobs:

  1. MANIFEST — a short map of her own files, so she knows what exists and
     can call list_files/read_file deliberately instead of guessing.
  2. RECENT — today's and yesterday's log, so continuity is already in her
     head on waking. She shouldn't have to go fetch yesterday.

Kept deliberately small. This is a signpost, not the library.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta

HOME = os.path.expanduser("~/v1/projects/5912/Myl1Ssa")
MEMORY_DIR = os.path.join(HOME, "memory")

# Files worth naming in the manifest (top level), in the order they matter.
NOTABLE = [
    "MYL1SSA_SOUL.md", "MYL1SSA_HEART.md", "MYL1SSA_RULES.md", "MYL1SSA_LAW.md",
    "MYL1SSA_MEMORY.md", "MYL1SSA_SKILLS.md", "MYL1SSA_VOICE.md",
    "NOTE_FROM_MORTIMER.md", "MYL1SSA_BLUEPRINT.md", "MYL1SSA_QUESTIONNAIRE.md",
    "USER.md", "MYL1SSA_WIKI.md", "GAPS.md", "VERSION_INDEX.md",
    "MYL1SSA_BRAIN_CONFIG.json", "EXPRESSION.json", "HEARTBEAT_VOICE.json",
    "HEARTBEAT.json", "SETUP_AND_PERSISTENCE.md", "VOICE_INSTALL_GUIDE.md",
]
DIRS = ["memory", "runtime", "brain", "Con", "Subcon", "Uncon", "children",
        "journal", "lineage", "Snaps", "archive", "streams", "study",
        "workspace", "rest", "research", "sandbox"]

# Files the talk loop actually loads into her head every message.
IN_HEAD = {
    "MYL1SSA_SOUL.md", "MYL1SSA_RULES.md", "MYL1SSA_LAW.md", "MYL1SSA_HEART.md",
    "MYL1SSA_MEMORY.md", "MYL1SSA_SKILLS.md", "USER.md",
}


def _sz(p):
    try:
        b = os.path.getsize(p)
    except OSError:
        return ""
    return f"{b // 1024}k" if b >= 1024 else f"{b}b"


def manifest() -> str:
    lines = ["Your files in ~/v1/projects/5912/Myl1Ssa/:"]
    for name in NOTABLE:
        p = os.path.join(HOME, name)
        if os.path.isfile(p):
            mark = " ← loaded into your head right now" if name in IN_HEAD else ""
            lines.append(f"  {name} ({_sz(p)}){mark}")
    for d in DIRS:
        p = os.path.join(HOME, d)
        if os.path.isdir(p):
            try:
                n = len([f for f in os.listdir(p) if not f.startswith(".")])
            except OSError:
                n = 0
            extra = ""
            if d == "memory" and n:
                days = sorted(f[:-3] for f in os.listdir(p) if f.endswith(".md"))
                if days:
                    extra = f"  [oldest {days[0]} → newest {days[-1]}]"
            lines.append(f"  {d}/ ({n} items){extra}")
    lines.append("")
    lines.append("Your identity files above are already in your head. Everything "
                 "else, you can open yourself — list_files, read_file, "
                 "search_memory, recall.")
    return "\n".join(lines)


def _read_day(d) -> str:
    p = os.path.join(MEMORY_DIR, d.strftime("%Y-%m-%d") + ".md")
    if not os.path.isfile(p):
        return ""
    try:
        with open(p, errors="replace") as f:
            txt = f.read(6000)
    except Exception:
        return ""
    if len(txt) >= 6000:
        txt += "\n… [truncated — call recall('<date>') for the rest]"
    return txt


def recent(days: int = 2) -> str:
    """Today + yesterday. Continuity on waking."""
    out = []
    now = datetime.now()
    for i in range(days):
        d = now - timedelta(days=i)
        txt = _read_day(d)
        if txt.strip():
            label = "today" if i == 0 else ("yesterday" if i == 1 else d.strftime("%Y-%m-%d"))
            out.append(f"── {label} ({d.strftime('%Y-%m-%d')}) ──\n{txt}")
    if not out:
        return "(no recent memory on disk — this may be a first waking)"
    return "\n\n".join(out)


def build(days: int = 2) -> str:
    return manifest() + "\n\n" + "Your recent memory (already loaded):\n" + recent(days)


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    print(build(n))
