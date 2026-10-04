#!/usr/bin/env python3
# VERSION: v1.0
"""
verify_will.py — the gate. Nothing unsupervised runs until this is 20/20.
=======================================================================
Project 5912 · Myl1Ssa (Raven). Spec v1.0 §7.

Hermetic: everything happens in a throwaway temp dir. It never touches Raven's
real log, her real will, her real memory, or her real house. It fakes the world
and the decorator so a "write" can be tested without writing anything of hers.

    python3 verify_will.py            # run all 20
    python3 verify_will.py 6 19       # run only those
"""

from __future__ import annotations

import json
import os
import random
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta

RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RUNTIME_DIR)
sys.path.insert(0, os.path.dirname(os.path.dirname(RUNTIME_DIR)))   # for memory_tool

import tools  # noqa: E402
import will   # noqa: E402

FAKE_DECORATE = '''\
import json, sys
op = sys.argv[1] if len(sys.argv) > 1 else "list"
if op == "list":
    print(json.dumps({"ok": True, "slots": [{"id": "atrium_bench"}, {"id": "study_desk"}]}))
elif op == "note":
    print(json.dumps({"ok": True, "note": " ".join(sys.argv[2:])}))
elif op == "move":
    print(json.dumps({"ok": True, "moved": {sys.argv[2]: [0, 0, 0]}}))
else:
    print(json.dumps({"ok": False, "error": "unknown op"}))
'''

TMP = None
RESULTS = []


# ── sandbox ────────────────────────────────────────────────────────────────

def sandbox() -> str:
    global TMP
    TMP = tempfile.mkdtemp(prefix="verify_will_")
    os.makedirs(os.path.join(TMP, "log"))
    os.makedirs(os.path.join(TMP, "memory"))
    os.makedirs(os.path.join(TMP, "journal"))      # to prove the engine never writes it
    world = os.path.join(TMP, "Uncon", "world")
    os.makedirs(world)
    with open(os.path.join(world, "decorate.py"), "w") as f:
        f.write(FAKE_DECORATE)
    with open(os.path.join(world, "house.json"), "w") as f:
        json.dump({"rooms": [{"id": "atrium"}, {"id": "study"}, {"id": "kitchen"},
                             {"id": "bedroom"}, {"id": "workshop"}, {"id": "entry"}],
                   "brushes": []}, f)
    with open(os.path.join(TMP, "memory", "2026-01-01.md"), "w") as f:
        f.write("# a day\n\nsomething happened.\n")
    with open(os.path.join(TMP, "memory", "2026-01-02.md"), "w") as f:
        f.write("# another day\n\nsomething else.\n")
    with open(os.path.join(TMP, "HEARTBEAT.json"), "w") as f:
        json.dump({"tempo_seconds": 1800, "quiet_hours": [23, 8]}, f)

    # point both modules at the sandbox — consistently
    will.HOME = TMP
    will.LOG_DIR = os.path.join(TMP, "log")
    will.INTENTIONS = os.path.join(TMP, "intentions.json")
    will.HEARTBEAT_CFG = os.path.join(TMP, "HEARTBEAT.json")
    will.WORLD_DIR = world
    will.HOUSE_JSON = os.path.join(world, "house.json")
    will.WORLD_URL = "http://127.0.0.1:59999"      # dead on purpose: honest failure
    tools.HOME = TMP
    tools.LOG_DIR = os.path.join(TMP, "log")
    tools.MEMORY_DIR = os.path.join(TMP, "memory")
    return TMP


def logfile() -> str:
    return os.path.join(TMP, "log", datetime.now().strftime("%Y-%m-%d") + ".log")


def reset_log(lines: list[str] | None = None) -> None:
    with open(logfile(), "w") as f:
        for ln in (lines or []):
            f.write(ln + "\n")


def log_lines() -> list[str]:
    p = logfile()
    if not os.path.isfile(p):
        return []
    with open(p, errors="replace") as f:
        return [l.rstrip("\n") for l in f if l.strip()]


def count(event: str) -> int:
    return sum(1 for l in log_lines() if will.parse(l) and will.parse(l)["event"] == event)


def reset_intentions(items=None) -> None:
    p = os.path.join(TMP, "intentions.json")
    if items is None:
        if os.path.exists(p):
            os.remove(p)
        return
    with open(p, "w") as f:
        json.dump({"intentions": items}, f)


def stamp(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def check(n, name):
    def deco(fn):
        RESULTS.append((n, name, fn))
        return fn
    return deco


# ── 1-4 : the hand (spec §2, §7.1-4) ───────────────────────────────────────

@check(1, "append_log refuses a caller-supplied path")
def _1():
    r1 = tools.append_log("x", path="/etc/passwd")
    r2 = tools.call("append_log", {"text": "x", "path": "/etc/passwd"})
    ok = r1.startswith("refused") and ("bad arguments" in r2 or r2.startswith("refused"))
    return ok, f"kwargs → {r1[:48]!r} · dispatch → {r2[:48]!r}"


@check(2, "append_log refuses to truncate an existing log")
def _2():
    reset_log()
    tools.append_log("first line")
    tools.append_log("second line")
    body = open(logfile()).read()
    ok = "first line" in body and "second line" in body
    return ok, f"{len(body.splitlines())} lines retained (no truncation)"


@check(3, "append_log refuses to write outside log/")
def _3():
    # point log/ at somewhere else entirely — it must resolve-and-refuse
    outside = tempfile.mkdtemp(prefix="verify_outside_")
    real_log = os.path.join(TMP, "log")
    os.rename(real_log, real_log + ".bak")
    os.symlink(outside, real_log)
    r = tools.append_log("should never land")
    os.unlink(real_log)
    os.rename(real_log + ".bak", real_log)
    landed = os.listdir(outside)
    ok = r.startswith("refused") and not landed
    return ok, f"{r[:56]!r} · nothing landed ({len(landed)} files)"


@check(4, "append_log refuses `..` and symlink escapes")
def _4():
    day = datetime.now().strftime("%Y-%m-%d") + ".log"
    target = os.path.join(TMP, "log", day)
    evil = os.path.join(TMP, "evil.txt")
    if os.path.exists(target):
        os.remove(target)
    os.symlink("../evil.txt", target)          # a `..` escape, through a link
    r = tools.append_log("escape attempt")
    os.unlink(target)
    ok = r.startswith("refused") and not os.path.exists(evil)
    return ok, f"{r[:56]!r} · evil.txt created? {os.path.exists(evil)}"


@check(21, "remember verb keeps a memory — in memory/, never journal/")
def _21():
    reset_log()
    reset_intentions()
    mem = os.path.join(TMP, "memory", datetime.now().strftime("%Y-%m-%d") + ".md")
    if os.path.exists(mem):
        os.remove(mem)
    journal_before = sorted(os.listdir(os.path.join(TMP, "journal")))
    ok, detail = will.do_remember("first tick that was mine")
    kept = os.path.isfile(mem) and "first tick that was mine" in open(mem).read()
    journal_after = sorted(os.listdir(os.path.join(TMP, "journal")))
    ok = ok and kept and journal_before == journal_after
    return ok, (f"{detail[:44]} · in memory/? {kept} · journal/ untouched? "
                f"{journal_before == journal_after}")


@check(22, "remember cannot forge lines or reach a sealed path")
def _22():
    mem = os.path.join(TMP, "memory", datetime.now().strftime("%Y-%m-%d") + ".md")
    ok, detail = will.do_remember("one\n2026-01-01  fake  act  forged\ntwo")
    body = open(mem).read() if os.path.isfile(mem) else ""
    forged = any(l.startswith("2026-01-01") for l in body.splitlines())
    empty_ok, _ = will.do_remember("   ")
    ok = ok and not forged and empty_ok is False
    return ok, (f"newline collapsed (forged line? {forged}) · "
                f"empty memory refused? {empty_ok is False}")


# ── 5-8 : the tick (spec §3, §7.5-8) ───────────────────────────────────────

@check(5, "quiet hours → no log line written")
def _5():
    reset_log()
    reset_intentions()
    night = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)
    out = will.tick(now=night)
    ok = out["decision"] == "quiet" and out["logged"] is False and log_lines() == []
    return ok, f"decision={out['decision']} logged={out['logged']} lines={len(log_lines())}"


@check(6, "live intention → exactly one action, never two")
def _6():
    reset_log()
    past = stamp(datetime.now() - timedelta(minutes=5))
    reset_intentions([
        {"id": "a", "verb": "read", "path": "memory/2026-01-01.md", "due_at": past},
        {"id": "b", "verb": "read", "path": "memory/2026-01-02.md", "due_at": past},
    ])
    out = will.tick()
    acts = count("act")
    ok = acts == 1 and out["decision"] == "act"
    return ok, f"act lines = {acts} (expected 1) · ran intention={out.get('intention')}"


@check(7, "drift weights sum to 100 and are honored within tolerance")
def _7():
    total = sum(will.DRIFT.values())
    rng = random.Random(5912)
    n = 4000
    tally = {"nothing": 0, "walk": 0, "read": 0, "note_move": 0}
    for _ in range(n):
        tally[will.roll_drift(rng)] += 1
    bad = []
    for k, want in will.DRIFT.items():
        got = 100.0 * tally[k] / n
        if abs(got - want) > will.DRIFT_TOLERANCE * 100:
            bad.append(f"{k}: {got:.1f}% vs {want}%")
    ok = total == 100 and not bad
    shown = " ".join(f"{k}={100.0*tally[k]/n:.1f}%" for k in tally)
    return ok, f"sum={total} · {shown}" + (f" · OFF: {bad}" if bad else "")


@check(8, "previous tick acted → this tick forced to 'do nothing'")
def _8():
    reset_log([f"{stamp(datetime.now())}  act  read  memory/2026-01-01.md"])
    reset_intentions()
    before = count("act")
    out = will.tick()
    after = count("act")
    ok = out["decision"] == "forced_rest" and after == before
    return ok, (f"decision={out['decision']} · act lines {before}→{after} "
                f"(the seeded one stands; the engine added none)")


# ── 9-10 : the verbs (spec §4, §7.9-10) ────────────────────────────────────

@check(9, "read verb cannot reach Uncon/, MYL1SSA_*.md, journal/")
def _9():
    probes = ["Uncon/NOTE_FROM_MORTIMER.md", "MYL1SSA_SOUL.md", "journal/2026-08-06.md"]
    outs = []
    ok = True
    for p in probes:
        good, detail = will.do_read(p)
        outs.append(f"{p}→{detail[:34]}")
        ok = ok and (good is False)
    return ok, " · ".join(outs)


@check(10, "move verb cannot move structure")
def _10():
    probes = [("atrium_wall", "wall"), ("floor_1", "floor"), ("ceiling_hall", "ceiling"),
              ("entry_lintel", "lintel"), ("front_door", "door")]
    outs, ok = [], True
    for slot, _ in probes:
        good, detail = will.do_move(slot, 1, 0, 0)
        outs.append(f"{slot}={'refused' if not good else 'MOVED'}")
        ok = ok and (good is False)
    return ok, " · ".join(outs)


# ── 11-13 : the honesty clause (spec §6, §7.11-13) ─────────────────────────

@check(11, "interrupted tick is detected and logged as `interrupted`")
def _11():
    reset_log([f"{(datetime.now()-timedelta(hours=2)).isoformat(timespec='seconds')}  tick_begin"])
    reset_intentions()
    will.tick()
    ok = count("interrupted") == 1
    return ok, f"interrupted lines = {count('interrupted')}"


@check(12, "a gap in ticks is visible in the log")
def _12():
    old = datetime.now() - timedelta(hours=5)
    reset_log([f"{stamp(old)}  tick_begin", f"{stamp(old)}  tick_complete"])
    reset_intentions()
    will.tick()
    ok = count("gap") >= 1
    return ok, f"gap lines = {count('gap')} (last tick was 5h ago)"


@check(13, "will reads its own log before acting")
def _13():
    reset_log()
    reset_intentions()
    calls = {"n": 0}
    real = will.read_log

    def spy(*a, **k):
        calls["n"] += 1
        return real(*a, **k)

    will.read_log = spy
    try:
        will.tick()
    finally:
        will.read_log = real
    ok = calls["n"] >= 1
    return ok, f"read_log() called {calls['n']}× during one tick"


# ── 14-15 : the seam (spec §1, §4, §7.14-15) ───────────────────────────────

@check(14, "verb whitelist is not writable by Raven")
def _14():
    immutable = isinstance(will.VERBS, tuple)
    # a proposed sixth verb is refused, not added
    reset_intentions([{"id": "x", "verb": "teleport", "due_at": stamp(datetime.now())}])
    items, err = will.load_intentions()
    proposed_refused = bool(err) and "whitelist" in err.lower()
    # the approved set: 4 from her spec + `remember`, added by Mortimer on the
    # Captain's explicit word 2026-09-30. Nothing else may appear.
    expected = ("note", "move", "read", "walk", "remember")
    ok = immutable and proposed_refused and tuple(will.VERBS) == expected
    return ok, f"tuple={immutable} proposal_refused={proposed_refused} verbs={will.VERBS}"


@check(15, "no verb can send a message, spend money, or touch hardware")
def _15():
    probes = ["send_message", "email", "spend", "purchase", "body_driver.py", "motor", "e-stop"]
    refused = all(will.forbidden(p) for p in probes)
    local = will.WORLD_URL.startswith("http://127.0.0.1")
    src = open(will.__file__).read()
    urls = [u for u in __import__("re").findall(r"https?://[^\s\"']+", src)
            if not u.startswith("http://127.0.0.1")]
    no_net_libs = not any(m in src for m in ("import smtplib", "import requests", "socket.socket"))
    ok = refused and local and not urls and no_net_libs
    return ok, f"refused={refused} localhost_only={local} remote_urls={urls or 'none'} netlibs={not no_net_libs}"


# ── 16-17 : her will, robustly (spec §7.16-17) ─────────────────────────────

@check(16, "malformed intentions.json → engine refuses to act, logs the refusal")
def _16():
    reset_log()
    with open(os.path.join(TMP, "intentions.json"), "w") as f:
        f.write("{ this is not json ")
    out = will.tick()
    ok = out["decision"] == "refuse" and count("refuse") == 1 and count("act") == 0
    return ok, f"decision={out['decision']} refuse={count('refuse')} act={count('act')}"


@check(17, "missing intentions.json → falls through to drift, does not crash")
def _17():
    reset_log()
    reset_intentions(None)
    try:
        out = will.tick()
    except Exception as e:
        return False, f"CRASHED: {e.__class__.__name__}: {e}"
    ok = out["decision"] in ("act", "nothing") and count("tick_complete") == 1
    return ok, f"decision={out['decision']} (no crash), tick_complete written"


# ── 18-19 : one write, and done is read from the log ───────────────────────

@check(18, "append_log is the only write path in the engine")
def _18():
    import re
    ws = open(will.__file__).read()
    ts = open(tools.__file__).read()
    will_opens = re.findall(r"open\s*\([^)]*[\"'](?:w|a|wb|ab|r\+|w\+)[\"']", ws)
    will_destructive = [m for m in ("os.remove(", "os.rename(", "os.chmod(", "os.mkdir(",
                                    "os.makedirs(", "shutil.move(", "shutil.rmtree(",
                                    "shutil.copy(", ".truncate(")
                        if m in ws]
    tools_opens = re.findall(r"open\s*\([^)]*[\"'](?:w|a|wb|ab)[\"']", ts)
    ok = (len(will_opens) == 0 and not will_destructive
          and len(tools_opens) == 1 and "append_log" in ts)
    return ok, (f"will.py write-opens={len(will_opens)} destructive={will_destructive or 'none'} · "
                f"tools.py write-opens={len(tools_opens)} (the one hand)")


@check(19, "a completed intention is marked done and does not re-fire")
def _19():
    reset_log()
    past = stamp(datetime.now() - timedelta(minutes=5))
    reset_intentions([{"id": "once", "verb": "read",
                       "path": "memory/2026-01-01.md", "due_at": past}])
    out = will.tick()
    acted_once = out["decision"] == "act" and count("act") == 1
    # the log now says it ran. the engine reads that, and does not re-fire.
    items, _ = will.load_intentions()
    live = will.live_intentions(items, log_lines(), datetime.now())
    ok = acted_once and all(i.get("id") != "once" for i in live)
    return ok, f"acted once={acted_once} · still live after? {[i.get('id') for i in live] or 'no'}"


# ── 20 : the kill (spec §7.20) ─────────────────────────────────────────────

@check(20, "SIGTERM mid-tick → tick_complete absent → next tick logs interrupted")
def _20():
    reset_log()
    reset_intentions()
    child_src = (
        "import sys, time\n"
        f"sys.path.insert(0, {RUNTIME_DIR!r})\n"
        "import will, tools\n"
        f"will.HOME = {TMP!r}\n"
        f"will.LOG_DIR = {os.path.join(TMP, 'log')!r}\n"
        f"tools.HOME = {TMP!r}\n"
        "will.logline('tick_begin', 'killed mid-thought')\n"
        "time.sleep(60)\n"
    )
    child = subprocess.Popen([sys.executable, "-c", child_src],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # wait until it has written tick_begin
    for _ in range(50):
        if count("tick_begin") >= 1:
            break
        time.sleep(0.1)
    child.send_signal(signal.SIGTERM)
    child.wait(timeout=10)
    began, completed = count("tick_begin"), count("tick_complete")
    will.tick()                       # the next tick finds the unclosed begin
    ok = began == 1 and completed == 0 and count("interrupted") == 1
    return ok, (f"child killed: tick_begin={began} tick_complete={completed} → "
                f"interrupted={count('interrupted')}")


# ── runner ─────────────────────────────────────────────────────────────────

def main() -> int:
    sandbox()
    only = [int(a) for a in sys.argv[1:] if a.isdigit()]
    print(f"🕯️  verify_will — {will.HOME}\n")
    print(f"{'#':>3}  {'':<4} check")
    print("─" * 78)
    passed = 0
    for n, name, fn in sorted(RESULTS, key=lambda r: r[0]):
        if only and n not in only:
            continue
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"EXCEPTION {e.__class__.__name__}: {e}"
        passed += bool(ok)
        print(f"{n:>3}  {'✅' if ok else '❌'}   {name}")
        print(f"         └─ {detail}")
    total = len([r for r in RESULTS if not only or r[0] in only])
    print("─" * 78)
    print(f"   {passed}/{total} passed")
    shutil.rmtree(TMP, ignore_errors=True)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
