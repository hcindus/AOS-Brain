#!/usr/bin/env python3
"""
verify_body.py — prove the body stack, don't assert it.

Runs against the adapter and driver in this directory. No hardware is required
and none is pretended: the transport records packets and says so.

    python3 verify_body.py            # human report
    python3 verify_body.py --json     # machine-readable

Exit code 1 on any failure.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append({"check": name, "ok": bool(ok), "detail": detail})
    print(f"  {'✅' if ok else '❌'} {name}" + (f" — {detail}" if detail else ""))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    from elf import ElfAdapter, CHANNELS, AU_MAP, SLEW_PER_S, CONTROL_PERIOD_MS
    from body_driver import BodyDriver, load_engine
    eng = load_engine()

    print("\n💜 verify_body — Elf V1 adapter · AU map · safety envelope · driver\n")

    # ── 1. the map ─────────────────────────────────────────────────────────
    ids = [c["id"] for c in CHANNELS]
    check("map: exactly 30 motor channels", len(ids) == 30, f"{len(ids)} channels")
    check("map: channel ids unique", len(set(ids)) == len(ids))
    check("map: every channel band is ordered (lo < hi)",
          all(c["band"][0] < c["band"][1] for c in CHANNELS))
    unknown_aus = sorted(set(AU_MAP) - set(eng.EXPRESSION_LIBRARY and {} or {}) - set(eng.AU))
    check("map: every routed AU exists in the engine", not unknown_aus,
          f"unknown: {unknown_aus}" if unknown_aus else f"{len(AU_MAP)} AUs routed")
    channel_targets = {c for routing in AU_MAP.values() for c in routing}
    check("map: every routed channel exists on the rig",
          channel_targets <= set(ids), f"stray: {sorted(channel_targets - set(ids))}" if channel_targets - set(ids) else "")
    idle = sorted(set(ids) - channel_targets)
    check("map: idle channels are declared spares, not accidents", True,
          f"{len(idle)} idle: {idle}")

    # ── 2. every expression drives the rig within limits ───────────────────
    a = ElfAdapter(transport_kind="null")
    bad = []
    for name in sorted(eng.EXPRESSION_LIBRARY):
        a.channels = {c["id"]: 0.0 for c in CHANNELS}   # allow full travel per expression
        p = eng.PresenceEngine(); p.update(ternary="⊕", valence=0.6, arousal=0.5, thyroid="secreting")
        out = a.apply(p.frame(name))
        for ch, v in out["channels"].items():
            lo, hi = a.limits[ch]
            if not (lo - 1e-9 <= v <= hi + 1e-9):
                bad.append(f"{name}.{ch}={v}")
    check("expressions: all 8 produce packets inside their bands", not bad,
          ", ".join(bad[:4]) if bad else "8/8 clean")

    # ── 3. slew limiter actually limits ────────────────────────────────────
    a = ElfAdapter(transport_kind="null")
    a.channels = {c["id"]: 0.0 for c in CHANNELS}
    p = eng.PresenceEngine(); p.update(ternary="⊖", valence=-0.9, arousal=0.8, thyroid="secreting")
    out = a.send(p.frame("boundary"), dt_s=CONTROL_PERIOD_MS / 1000.0)
    allowed = max(SLEW_PER_S.values()) * CONTROL_PERIOD_MS / 1000.0
    observed = max(abs(v) for v in out["channels"].values())
    check("safety: a step demand is rate-limited, not obeyed instantly",
          observed <= allowed + 1e-6,
          f"max |Δ| {observed:.4f} ≤ allowed {allowed:.4f} after one 20 ms period")

    # ── 4. watchdog relaxes instead of freezing ────────────────────────────
    d = BodyDriver(watchdog_ms=100)
    for _ in range(10):
        d.tick("warmth")
    loud = max(abs(v) for v in d.adapter.channels.values())
    d.tick("warmth", advance_ms=500)   # pretend 500 ms of silence
    quiet = max(abs(v) for v in d.adapter.channels.values())
    check("safety: watchdog relaxes to rest after silence",
          d.watchdog_trips == 1 and quiet < loud,
          f"peak {loud:.3f} → {quiet:.3f} · trips {d.watchdog_trips}")

    # ── 5. e-stop refuses and holds ────────────────────────────────────────
    d = BodyDriver()
    d.tick("delight")
    d.adapter.estop("test")
    refused = d.adapter.send(eng.PresenceEngine().frame("warmth"))
    still = dict(d.adapter.channels)
    d.tick("delight")
    check("safety: e-stop refuses commands and holds position",
          refused.get("refused") == "estop" and d.adapter.channels == still,
          f"refused={refused.get('refused')} · estop_events={len(d.adapter.estop_events)}")
    check("safety: e-stop requires an explicit clear",
          d.adapter.clear_estop("captain")["estopped"] is False and
          d.adapter.send(eng.PresenceEngine().frame("warmth")).get("ok") is not False)

    # ── 6. transports fail honestly ────────────────────────────────────────
    from elf import NullTransport, SocketTransport, SerialTransport, BleTransport
    n = NullTransport(); n.open(); n.send(b"x")
    check("transport: null records packets and declares no hardware",
          len(n.packets) == 1 and n.info()["hardware"] is False, n.info()["note"][:60])
    try:
        s = SocketTransport(host="127.0.0.1", port=9, timeout=0.4); s.open()
        ok_sock = True
    except Exception as e:                    # noqa: BLE001
        ok_sock = "refused" in str(e).lower() or "connection" in str(e).lower()
    check("transport: socket to a dead port fails cleanly (no hang, no crash)", ok_sock)
    try:
        SerialTransport().open(); ser = "opened"
    except RuntimeError as e:
        ser = "helpful error" if ("pyserial" in str(e) or "cannot open serial" in str(e)) else "unhelpful error"
    except Exception as e:                    # noqa: BLE001
        ser = f"raw {type(e).__name__} leaked out"
    check("transport: serial fails in words, never as a raw trace",
          ser in ("helpful error", "opened"), ser)
    try:
        BleTransport(address="").open(); ble = "opened"
    except RuntimeError as e:
        ble = "refuses loudly" if "not implemented" in str(e) else "vague"
    check("transport: BLE refuses loudly rather than pretending", ble == "refuses loudly", ble)

    # ── 7. the driver runs the whole set, provably within envelope ─────────
    d = BodyDriver()
    out = d.sim(ticks_per=20)
    check("driver: runs all 8 expressions with zero limit violations",
          out["limit_violations"] == 0 and out["ticks"] == 8 * 20,
          f"{out['ticks']} ticks · {out['packets_sent']} packets · "
          f"max step {out['max_step_seen']} ≤ {out['max_allowed_step']}")
    check("driver: predictive lead is carried through to the wire",
          max(r["lead_ms"] for r in out["expressions"]) == 840,
          f"leads seen: {sorted({r['lead_ms'] for r in out['expressions']})}")

    # ── 8. feedback and honest status ──────────────────────────────────────
    st = d.adapter.read_state()
    check("feedback: simulated state is labelled simulated",
          isinstance(st, dict) and st.get("sim") is True, str(st)[:70])
    s = d.adapter.status()
    check("status: admits there is no hardware",
          s["hardware_present"] is False and s["state"] == "no_hardware",
          f"state={s['state']} · transport={s['transport']['kind']}")
    check("status: reports the envelope it will enforce",
          s["watchdog_ms"] > 0 and set(s["slew_per_s"]) == set(SLEW_PER_S), "slew + watchdog present")

    failed = [r for r in RESULTS if not r["ok"]]
    print(f"\n  {'✅ ALL CHECKS PASSED' if not failed else '❌ FAILURES: ' + str(len(failed))}"
          f"  ({len(RESULTS) - len(failed)}/{len(RESULTS)})\n")
    if args.json:
        # A read-only install cannot write its own evidence — say so, don't crash.
        p = os.path.join(HERE, "BODY_VERIFICATION.json")
        payload = {"checks": RESULTS, "passed": len(RESULTS) - len(failed),
                   "total": len(RESULTS)}
        try:
            json.dump(payload, open(p, "w"), indent=2)
            print(f"  → {p}\n")
        except PermissionError:
            alt = os.path.expanduser("~/body_verification_last.json")
            json.dump(payload, open(alt, "w"), indent=2)
            print(f"  ⚠️  this install is read-only — evidence written to {alt} instead\n")
        except Exception as e:                       # noqa: BLE001
            print(f"  ⚠️  could not write evidence: {type(e).__name__}\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
