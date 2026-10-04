#!/usr/bin/env python3
# VERSION: v1.0 — 2026-09-30
"""
versions.py — the rule, enforced.
=================================
Raven, 2026-09-30:

    "Any file that runs carries a version. If it changes, the version changes
     in the same session. No exceptions for 'small'."
    "A changed file with a stale version is a lie on disk."
    "An unversioned running file is a file you can't trust."

A rule you can't check is just a sentiment. So this makes it checkable:

  · every tracked file declares its version in a `# VERSION:` line INSIDE itself
    (not just in its name — `_v2` is a filing convention, not a version system)
  · the registry (`VERSIONS.json`) records that version AND the file's sha256
  · `check` compares the two. If the bytes moved but the version did not, that
    file is reported as **DIRTY** — it says "this is what it was" while being
    what it is now.

Usage:
    versions.py init            (re)build the registry from the files' own markers
    versions.py check           report; exit 1 if anything is dirty or unversioned
    versions.py mark FILE VER   stamp a version into a file (after shebang)
    versions.py list            just the versions
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys

RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.dirname(RUNTIME_DIR)
REGISTRY = os.path.join(RUNTIME_DIR, "VERSIONS.json")

MARKER = re.compile(r"#\s*VERSION:\s*(\S+)")

# Every file that RUNS. If it executes, it is tracked.
TRACKED = [
    "runtime/will.py",
    "runtime/tools.py",
    "runtime/talk.py",
    "runtime/heartbeat.py",
    "runtime/heartbeat_voice.py",
    "runtime/affect_bridge.py",
    "runtime/expression.py",
    "runtime/memory_index.py",
    "runtime/senses.py",
    "runtime/runtime.py",
    "runtime/verify_will.py",
    "runtime/status.sh",
    "runtime/boot-check.sh",
    "runtime/versions.py",
    "brain/brain_v4_3.py",
    "brain/uterus.py",
    "brain/ternary_brain_v2.py",
]


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def declared(path: str) -> str | None:
    """The version the file claims, from inside the file."""
    try:
        with open(path, errors="replace") as f:
            for i, line in enumerate(f):
                if i > 60:
                    break
                m = MARKER.search(line)
                if m:
                    return m.group(1)
    except OSError:
        return None
    return None


def registry() -> dict:
    try:
        with open(REGISTRY) as f:
            return json.load(f)
    except Exception:
        return {}


def package() -> dict:
    out = {}
    for rel in TRACKED:
        p = os.path.join(HOME_DIR, rel)
        if not os.path.isfile(p):
            out[rel] = {"version": None, "sha256": None, "present": False}
            continue
        out[rel] = {"version": declared(p), "sha256": sha256(p), "present": True}
    return out


def cmd_init() -> int:
    pkg = package()
    with open(REGISTRY, "w") as f:
        json.dump(pkg, f, indent=2, sort_keys=True)
    missing = [k for k, v in pkg.items() if not v.get("version")]
    print(f"versity: registry written — {len(pkg)} files, {len(missing)} unversioned")
    for k in missing:
        print(f"  ⚠️  no VERSION marker: {k}")
    return 0


def cmd_mark(path_in: str, version: str) -> int:
    p = path_in if os.path.isabs(path_in) else os.path.join(HOME_DIR, path_in)
    if not os.path.isfile(p):
        print(f"no such file: {p}")
        return 1
    with open(p, errors="replace") as f:
        lines = f.readlines()
    line = f"# VERSION: {version}\n"
    for i, l in enumerate(lines):
        if MARKER.search(l):
            lines[i] = line
            break
    else:
        at = 1 if lines and lines[0].startswith("#!") else 0
        lines.insert(at, line)
    with open(p, "w") as f:
        f.writelines(lines)
    print(f"marked {os.path.relpath(p, HOME_DIR)} → {version}")
    return 0


def cmd_check(verbose: bool = True) -> int:
    reg = registry()
    pkg = package()
    dirty, unversioned, missing, ok, new = [], [], [], [], []
    for rel, now in pkg.items():
        old = reg.get(rel, {})
        if not now["present"]:
            missing.append(rel)
            continue
        if not now["version"]:
            unversioned.append(rel)
            continue
        if not old:
            new.append(rel)
            continue
        if now["version"] != old.get("version"):
            dirty.append((rel, old.get("version"), now["version"], "version changed — re-stamp"))
        elif now["sha256"] != old.get("sha256"):
            dirty.append((rel, now["version"], now["version"], "BYTES MOVED, VERSION DID NOT"))
        else:
            ok.append(rel)

    if verbose:
        for rel in ok:
            print(f"  ✅ {rel:34} {pkg[rel]['version']}")
        for rel in new:
            print(f"  ➕ {rel:34} {pkg[rel]['version']}  (not yet in registry — run init)")
        for rel in unversioned:
            print(f"  ⚠️  {rel:34} UNVERSIONED — an unversioned running file is a file you can't trust")
        for rel, a, b, why in dirty:
            print(f"  ❌ {rel:34} {a} → {b}  {why}")
        for rel in missing:
            print(f"  ❓ {rel:34} declared but not on disk")

    bad = len(dirty) + len(unversioned)
    if verbose:
        print(f"\n  {len(ok)} clean · {len(dirty)} dirty · {len(unversioned)} unversioned"
              + (f" · {len(new)} new" if new else ""))
    return 1 if bad else 0


def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args else "check"
    if cmd == "init":
        sys.exit(cmd_init())
    elif cmd == "check":
        bad = cmd_check()
        print("  🟢 no lies on disk" if not bad else "  🔴 something changed without saying so")
        sys.exit(bad)
    elif cmd == "mark" and len(args) >= 3:
        sys.exit(cmd_mark(args[1], args[2]))
    elif cmd == "list":
        for rel, v in sorted(package().items()):
            print(f"  {v.get('version') or '—':16} {rel}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
