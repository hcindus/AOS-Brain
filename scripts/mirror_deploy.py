#!/usr/bin/env python3
"""
Mirror Deploy — flip psdepot.com between the blue-green versions.

Deterministic, audited, reversible. No AI in the loop.

Usage:
  python3 mirror_deploy.py deploy  v1     # make v1 live
  python3 mirror_deploy.py deploy  v0     # make v0 live
  python3 mirror_deploy.py rollback       # flip back to the other version
  python3 mirror_deploy.py status         # show current state
  python3 mirror_deploy.py refresh v1     # rsync current live -> v1 (sync working copy)

Safety: refuses to deploy if the target version is missing, and refuses to
flip if the live site is currently down (so we never swap in a broken build).
"""
import os
import subprocess
import sys

BASE = "/var/www"
LINK = f"{BASE}/psdepot.com"
VERSIONS = ("psdepot-v0", "psdepot-v1")


def current_version() -> str | None:
    if not os.path.islink(LINK):
        return None
    return os.path.basename(os.path.realpath(LINK))


def other_version() -> str:
    cur = current_version()
    return "psdepot-v1" if cur == "psdepot-v0" else "psdepot-v0"


def site_up() -> bool:
    try:
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                            "--max-time", "10", "https://psdepot.com/"],
                           capture_output=True, text=True, timeout=15)
        return r.stdout.strip() == "200"
    except Exception:
        return False


def validate(target: str) -> str | None:
    if target not in VERSIONS:
        return f"unknown version '{target}' (choose psdepot-v0 or psdepot-v1)"
    if not os.path.isdir(f"{BASE}/{target}"):
        return f"{BASE}/{target} does not exist"
    return None


def flip(target: str) -> int:
    err = validate(target)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1

    cur = current_version()
    if cur == target:
        print(f"Already live on {target} — nothing to do.")
        return 0

    # Safety: never flip away from a working site onto an unverified build
    if not site_up():
        print("ERROR: current site is DOWN — refusing to flip. Fix live first.",
              file=sys.stderr)
        return 1

    os.symlink(f"{BASE}/{target}", f"{LINK}.new")
    os.replace(f"{LINK}.new", LINK)  # atomic swap

    # reload nginx so alias/cache paths re-resolve cleanly
    subprocess.run(["systemctl", "reload", "nginx"], check=False)

    if site_up():
        print(f"DEPLOYED: live is now {target} (was {cur}). Site 200 OK.")
        return 0
    else:
        print("WARNING: flip completed but site check failed. Run mirror_audit.py.")
        return 1


def rollback() -> int:
    return flip(other_version())


def refresh(target: str) -> int:
    """Sync the current live version into the target working copy (rsync)."""
    err = validate(target)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1
    cur = current_version()
    if cur == target:
        print(f"Refusing to refresh the LIVE version ({target}). Choose the standby.")
        return 1
    src = f"{BASE}/{cur}/"
    dst = f"{BASE}/{target}/"
    r = subprocess.run(["rsync", "-a", "--delete", "--exclude", ".backups",
                        src, dst], check=False)
    if r.returncode == 0:
        print(f"Refreshed {target} from {cur}.")
        return 0
    print("rsync failed.", file=sys.stderr)
    return 1


def status() -> int:
    cur = current_version()
    print(f"Symlink: {LINK} -> {os.readlink(LINK) if os.path.islink(LINK) else '(not a symlink)'}")
    print(f"Live:    {cur}")
    print(f"Standby: {other_version() if cur else 'unknown'}")
    print(f"Site:    {'UP (200)' if site_up() else 'DOWN'}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "deploy" and len(sys.argv) == 3:
        sys.exit(flip(sys.argv[2]))
    elif cmd == "rollback":
        sys.exit(rollback())
    elif cmd == "refresh" and len(sys.argv) == 3:
        sys.exit(refresh(sys.argv[2]))
    elif cmd == "status":
        sys.exit(status())
    else:
        print(__doc__)
        sys.exit(1)
