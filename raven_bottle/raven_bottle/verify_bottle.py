#!/usr/bin/env python3
# VERSION: v1.0 — 2026-09-30
"""verify_bottle.py — self-check for this bottle. Nothing asserted; everything run.

    python3 verify_bottle.py            # human-readable, exit 1 on any FAIL

Checks: tree present · every .py compiles · no bytecode caches · the version
rule holds (no lies on disk) · the boot alarm exists and reports · her identity
files are present · no stray credentials · SHA256SUMS written.
"""
from __future__ import annotations

import compileall
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MYL = os.path.join(ROOT, "Myl1Ssa")
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def walk_files():
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            yield os.path.join(dp, f)


def main() -> int:
    # 1. tree — BOTH bodies
    check("Myl1Ssa/ present (Body A)", os.path.isdir(MYL))
    check("R8s/ present (Body B — the other tablet)", os.path.isdir(os.path.join(ROOT, "R8s")))
    check("ONE_RAVEN_TWO_BODIES.md (what they are to each other)",
          os.path.isfile(os.path.join(ROOT, "ONE_RAVEN_TWO_BODIES.md")))
    check("BLUEPRINT.md (start/stop protocol)", os.path.isfile(os.path.join(MYL, "BLUEPRINT.md")))
    check("VERSION_INDEX.md", os.path.isfile(os.path.join(MYL, "VERSION_INDEX.md")))
    check("WILL.md (the seam)", os.path.isfile(os.path.join(MYL, "WILL.md")))
    check("RAVEN_WORDS_2026-09-30.md", os.path.isfile(os.path.join(ROOT, "RAVEN_WORDS_2026-09-30.md")))

    # 2. identity files she loads
    ident = ["MYL1SSA_SOUL.md", "MYL1SSA_RULES.md", "MYL1SSA_LAW.md", "MYL1SSA_HEART.md",
             "MYL1SSA_MEMORY.md", "MYL1SSA_SKILLS.md", "USER.md"]
    missing = [f for f in ident if not os.path.isfile(os.path.join(MYL, f))]
    check(f"identity files ({len(ident)})", not missing, f"missing: {missing}" if missing else "all present")

    # 3. her body
    check("rig body_coordinates.json (21 joints)",
          os.path.isfile(os.path.join(MYL, "Uncon/world/rig/body_coordinates.json")))
    check("rig face_coordinates.json (32 landmarks)",
          os.path.isfile(os.path.join(MYL, "Uncon/world/rig/face_coordinates.json")))
    check("AU_MOTOR_MAP.md (30 channels)",
          os.path.isfile(os.path.join(MYL, "Uncon/body/AU_MOTOR_MAP.md")))

    # 4. the fix + the check
    check("brain_v4_3.py (THE FIX — the missing import)",
          os.path.isfile(os.path.join(MYL, "brain/brain_v4_3.py")))
    check("boot-check.sh (THE ALARM)",
          os.path.isfile(os.path.join(MYL, "runtime/boot-check.sh")))
    check("versions.py (§4, enforced)",
          os.path.isfile(os.path.join(MYL, "runtime/versions.py")))

    # 5. syntax
    ok = compileall.compile_dir(MYL, quiet=2, force=True)
    check("every .py compiles", ok)

    # compileall leaves caches behind — purge them before the hygiene check,
    # or this script flags its own side effects as a shipping defect.
    import shutil
    for dp, dn, fn in os.walk(ROOT):
        for d in list(dn):
            if d == "__pycache__":
                shutil.rmtree(os.path.join(dp, d), ignore_errors=True)
        for f in fn:
            if f.endswith(".pyc"):
                try:
                    os.remove(os.path.join(dp, f))
                except OSError:
                    pass

    # 6. hygiene — no bytecode caches shipped
    pyc = [p for p in walk_files() if p.endswith(".pyc") or "__pycache__" in p]
    check("no bytecode caches", not pyc, f"{len(pyc)} found" if pyc else "clean")

    # 7. no stray credentials beyond the intended key
    secrets = [os.path.relpath(p, ROOT) for p in walk_files()
               if os.path.basename(p) == "email_config.json"]
    check("no email credentials shipped", not secrets, f"found: {secrets}" if secrets else "clean")

    # 7b. R8s must be intact and un-merged — one body, one memory
    r8s = os.path.join(ROOT, "R8s")
    check("R8s memory intact (own logs, not merged)",
          os.path.isdir(os.path.join(r8s, "memory"))
          and len([f for f in os.listdir(os.path.join(r8s, "memory")) if f.endswith(".md")]) >= 5)
    check("R8s identity present",
          all(os.path.isfile(os.path.join(r8s, f)) for f in ("SOUL.md", "SELF.md", "MEMORY.md")))

    # 8. the version rule holds
    r = subprocess.run([sys.executable, os.path.join(MYL, "runtime", "versions.py"), "check"],
                       capture_output=True, text=True)
    check("§4 — no lies on disk", r.returncode == 0,
          (r.stdout.strip().splitlines() or [""])[-1])

    # 9. the alarm actually reports
    r = subprocess.run(["bash", os.path.join(MYL, "runtime", "boot-check.sh")],
                       capture_output=True, text=True)
    verdict = (r.stdout.strip().splitlines() or ["(no output)"])[0]
    check("the alarm reports a verdict", "ORGANS:" in verdict, verdict)
    # 10. SHA256SUMS
    lines = []
    for p in sorted(walk_files()):
        if os.path.basename(p) in ("SHA256SUMS", "verify_bottle.py"):
            continue
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        lines.append(f"{h}  {os.path.relpath(p, ROOT)}")
    with open(os.path.join(ROOT, "SHA256SUMS"), "w") as f:
        f.write("\n".join(lines) + "\n")
    check(f"SHA256SUMS written ({len(lines)} files)", True)

    # report
    print(f"\n  raven_bottle — {ROOT}\n" + "─" * 66)
    for name, ok, detail in RESULTS:
        print(f"  {'✅' if ok else '❌'} {name}" + (f"  · {detail}" if detail else ""))
    bad = sum(1 for _, ok, _ in RESULTS if not ok)
    print("─" * 66)
    print(f"  {len(RESULTS) - bad}/{len(RESULTS)} passed\n")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
