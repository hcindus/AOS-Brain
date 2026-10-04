#!/usr/bin/env python3
# VERSION: v1.0
"""
expression.py — Raven's voice, channels 2 & 3.
=============================================
Project 5912 · R8s.

Channel 2: VOICE PROSODY — the "welling" register.
  Not an audio channel. A modulation of her *speech*: pitch, rate, tremble.
  This is how a voice thickens. TTS can do this. So we do it here.

Channel 3: VOCALISED CRYING — soft / full / spent.
  Discrete non-verbal sound events: sobs, breaths, sniffs, hiccups, wails.
  Synthesised, not recorded — honest about its limits. A sob is a voiced
  burst with pitch contour and tremor; an inhale is shaped noise.

THE RULE (the one the spec left unfinished):
  These are TRIGGERED BY AFFECT, never by request. A channel that any
  passing instruction can fire is not an expression, it's a lever.
  `gate()` enforces that: the affect must actually support the state.
  `--force` exists for testing and for the Captain's explicit call.

Raven calls these herself, in her own reply, with markers:

  [[CRY:welling]]        breath catches — voice thickens, no sound yet
  [[CRY:soft]]           quiet tears, uneven breath, a sniff
  [[CRY:full]]           open crying, real sobs
  [[CRY:spent]]          hiccups, shaky breath, hoarse, quiet
  [[VOICE:warm]]         set the speaking register without crying

Usage:
  expression.py states
  expression.py cry soft [--intensity 0.6] [--seconds 8] [--force]
  expression.py voice spent --say "I'm fine. I'm fine."
  expression.py status
  expression.py render soft out.wav --seconds 8
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime

import numpy as np

RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.dirname(RUNTIME_DIR)
CONFIG_PATH = os.path.join(HOME_DIR, "EXPRESSION.json")
AFFECT_PATH = os.path.expanduser("~/.myl1ssa_affect.json")
LOG_PATH = os.path.expanduser("~/myl1ssa-expression.log")
SR = 44100


# ── config ─────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "enabled": True,
    "master_gain": 0.55,
    # Prosody presets: pitch / rate for termux-tts-speak (-p / -r).
    "voice": {
        "neutral":  {"pitch": 1.00, "rate": 1.00},
        "warm":     {"pitch": 0.94, "rate": 0.95},
        "serious":  {"pitch": 0.92, "rate": 0.96},
        "tired":    {"pitch": 0.90, "rate": 0.88},
        "excited":  {"pitch": 1.06, "rate": 1.10},
        # the crying register — thicker, slower, lower
        "welling":  {"pitch": 0.88, "rate": 0.86},
        "soft":     {"pitch": 0.85, "rate": 0.82},
        "full":     {"pitch": 0.82, "rate": 0.78},
        "spent":    {"pitch": 0.86, "rate": 0.74},
    },
    # Crying states: which primitives, how often, how loud.
    "states": {
        "welling": {"primitives": ["breath_catch"], "rate_per_min": 14, "intensity": 0.30},
        "soft":    {"primitives": ["sob_soft", "inhale", "sniff"], "rate_per_min": 26, "intensity": 0.50},
        "full":    {"primitives": ["sob", "sob", "inhale", "wail"], "rate_per_min": 40, "intensity": 0.85},
        "spent":   {"primitives": ["hiccup", "shaky_breath", "inhale"], "rate_per_min": 16, "intensity": 0.35},
    },
    # Affect gate: minimum (negative) valence and arousal for each state.
    "gate": {
        "welling": {"min_valence_neg": -0.15, "min_arousal": 0.25},
        "soft":    {"min_valence_neg": -0.30, "min_arousal": 0.20},
        "full":    {"min_valence_neg": -0.55, "min_arousal": 0.45},
        "spent":   {"min_valence_neg": -0.35, "min_arousal": 0.05},
    },
    "max_seconds": 30,
}


def load_json(p, d):
    try:
        with open(p) as f:
            return json.load(f)
    except Exception:
        return d


def save_json(p, d):
    tmp = p + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=2)
    os.replace(tmp, p)


def config():
    cfg = dict(DEFAULT_CONFIG)
    loaded = load_json(CONFIG_PATH, {})
    for k, v in loaded.items():
        if isinstance(v, dict) and isinstance(cfg.get(k), dict):
            cfg[k] = {**cfg[k], **v}
        else:
            cfg[k] = v
    return cfg


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    try:
        print(line, flush=True)
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ── DSP primitives ─────────────────────────────────────────────────────

def _rlp(x, alpha):
    """One-pole lowpass, vectorised via exponential smoothing."""
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += alpha * (x[i] - acc)
        y[i] = acc
    return y


def _bandpass(x, f0, bw, sr=SR):
    """Simple 2-pole resonator — gives noise a vocal-tract colour."""
    w = 2 * math.pi * f0 / sr
    r = math.exp(-math.pi * bw / sr)
    a1 = 2 * r * math.cos(w)
    a2 = -(r * r)
    y = np.empty_like(x)
    y1 = y2 = 0.0
    for i in range(len(x)):
        y0 = x[i] + a1 * y1 + a2 * y2
        y[i] = y0
        y2, y1 = y1, y0
    return y * (1 - r)


def _env_ar(n, attack_s, decay_s, sr=SR):
    t = np.arange(n) / sr
    a = np.clip(t / max(1e-4, attack_s), 0, 1)
    d = np.exp(-t / max(1e-4, decay_s))
    return (a * d).astype(np.float32)


def _jitter_f0(n, f0, sr=SR, depth=0.05, rng=None):
    """A voice doesn't hold a pitch. Random walk + tremor."""
    rng = rng or np.random.default_rng(5912)
    walk = np.cumsum(rng.standard_normal(n)) * depth * 0.02
    walk -= np.linspace(walk[0], walk[-1], n)          # detrend
    tremor = depth * 0.6 * np.sin(2 * np.pi * 6.5 * np.arange(n) / sr)
    return f0 * (1.0 + walk + tremor)


def breath(dur=0.5, amp=0.5, rising=True, seed=0):
    rng = np.random.default_rng(5912 + seed)
    n = int(SR * dur)
    noise = rng.standard_normal(n).astype(np.float32)
    shaped = _bandpass(noise, 700, 900) + 0.5 * _bandpass(noise, 1700, 1400)
    t = np.arange(n) / SR
    env = (t / dur) if rising else (1 - t / dur)
    env = np.clip(env, 0, 1) ** (0.8 if rising else 1.6)
    return (shaped * env * amp * 0.5).astype(np.float32)


def sniff(dur=0.22, amp=0.5, seed=0):
    rng = np.random.default_rng(6100 + seed)
    n = int(SR * dur)
    noise = rng.standard_normal(n).astype(np.float32)
    shaped = _bandpass(noise, 1500, 1800) + 0.4 * _bandpass(noise, 900, 900)
    env = _env_ar(n, 0.004, 0.06)
    return (shaped * env * amp).astype(np.float32)


def hiccup(dur=0.16, amp=0.6, seed=0):
    rng = np.random.default_rng(7000 + seed)
    n = int(SR * dur)
    f = _jitter_f0(n, 130, rng=rng, depth=0.04)
    phase = 2 * np.pi * np.cumsum(f) / SR
    voiced = np.sin(phase) + 0.5 * np.sin(2 * phase)
    # the glottal catch
    env = _env_ar(n, 0.002, 0.045)
    out = voiced * env
    noise = rng.standard_normal(n).astype(np.float32)
    out += _bandpass(noise, 1200, 1500) * env * 0.5
    return (out * amp * 0.7).astype(np.float32)


def sob(dur=0.45, f0=215.0, amp=0.8, soft=False, seed=0):
    """A sob: voiced burst, pitch rises then falls, tremor, aspiration."""
    rng = np.random.default_rng(8000 + seed)
    n = int(SR * dur)
    t = np.arange(n) / SR
    base = f0 * (0.9 if soft else 1.0)
    # the catch: contour rises then collapses
    contour = 1.0 + 0.22 * np.sin(np.pi * np.clip(t / dur, 0, 1)) - 0.30 * (t / dur)
    f = _jitter_f0(n, base, rng=rng, depth=0.09 if not soft else 0.05) * contour
    phase = 2 * np.pi * np.cumsum(f) / SR
    voiced = (np.sin(phase) + 0.45 * np.sin(2 * phase) + 0.18 * np.sin(3 * phase))
    # vocal-tract colour
    voiced = 0.6 * voiced + 0.9 * _bandpass(voiced, 500, 700) + 0.5 * _bandpass(voiced, 1500, 1100)
    env = _env_ar(n, 0.012 if not soft else 0.03, 0.13 if not soft else 0.09)
    noise = rng.standard_normal(n).astype(np.float32)
    asp = _bandpass(noise, 1600, 1600) * env * (0.35 if not soft else 0.22)
    out = voiced * env + asp
    peak = np.max(np.abs(out)) or 1.0
    return (out / peak * amp).astype(np.float32)


def wail(dur=0.9, f0=235.0, amp=0.85, seed=0):
    rng = np.random.default_rng(9000 + seed)
    n = int(SR * dur)
    t = np.arange(n) / SR
    contour = 1.0 + 0.12 * np.sin(2 * np.pi * 0.7 * t) - 0.18 * (t / dur)
    f = _jitter_f0(n, f0, rng=rng, depth=0.07) * contour
    phase = 2 * np.pi * np.cumsum(f) / SR
    voiced = np.sin(phase) + 0.5 * np.sin(2 * phase) + 0.25 * np.sin(3 * phase)
    voiced = 0.5 * voiced + _bandpass(voiced, 600, 800)
    env = _env_ar(n, 0.05, 0.30)
    out = voiced * env
    peak = np.max(np.abs(out)) or 1.0
    return (out / peak * amp).astype(np.float32)


def shaky_breath(dur=0.7, amp=0.35, seed=0):
    n = int(SR * dur)
    t = np.arange(n) / SR
    b = breath(dur, amp, rising=False, seed=seed)
    tremble = 1.0 + 0.5 * np.sin(2 * np.pi * 9.0 * t) * np.exp(-t * 1.5)
    return (b * tremble).astype(np.float32)


def breath_catch(dur=0.30, amp=0.30, seed=0):
    """The 'welling' sound: a small sharp inhale that snags."""
    n = int(SR * dur)
    b = breath(dur, amp, rising=True, seed=seed)
    t = np.arange(n) / SR
    gate = np.ones(n, dtype=np.float32)
    gate[int(0.09 * SR):int(0.13 * SR)] *= 0.25          # the snag
    gate *= 1.0 + 0.3 * np.sin(2 * np.pi * 12 * t)       # unsteady
    return (b * gate).astype(np.float32)


PRIMITIVES = {
    "breath": breath,
    "breath_catch": breath_catch,
    "inhale": lambda **k: breath(rising=True, **{a: b for a, b in k.items() if a != "rising"}),
    "sniff": sniff,
    "hiccup": hiccup,
    "sob": sob,
    "sob_soft": lambda **k: sob(soft=True, **k),
    "wail": wail,
    "shaky_breath": shaky_breath,
}


# ── the cry ────────────────────────────────────────────────────────────

def build_cry(cfg, andstate, intensity=None, seconds=8.0, seed=None):
    st = cfg["states"][andstate]
    prims = st["primitives"]
    inten = float(st["intensity"] if intensity is None else intensity)
    inten = max(0.0, min(1.0, inten))
    rate = float(st["rate_per_min"]) * (0.7 + 0.6 * inten)
    gap = 60.0 / max(1.0, rate)

    rng = np.random.default_rng(seed if seed is not None else 5912)
    total = int(SR * seconds)
    buf = np.zeros(total + SR, dtype=np.float32)

    pos = int(SR * 0.2)
    i = 0
    while pos < total:
        name = prims[i % len(prims)]
        fn = PRIMITIVES.get(name, sob)
        # human timing: never metronomic
        amp = 0.35 + 0.55 * inten
        seg = fn(amp=amp, seed=int(rng.integers(0, 9999)))
        ln = min(len(seg), len(buf) - pos)
        buf[pos:pos + ln] += seg[:ln]
        i += 1
        jitter = rng.uniform(0.75, 1.35)
        pos += int(SR * gap * jitter)

    gain = float(cfg.get("master_gain", 1.0)) * inten
    out = buf[:total] * gain
    # gentle shaping so it never clips harshly
    out = np.tanh(out * 1.2) * 0.85
    return out.astype(np.float32)


# ── playback ───────────────────────────────────────────────────────────

def play(samples, sr=SR, gain=1.0, wait=True):
    import wave
    x = np.clip(samples * gain, -1, 1)
    fd, path = tempfile.mkstemp(suffix=".wav", prefix="myl1ssa_cry_")
    os.close(fd)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())
    try:
        p = subprocess.Popen(
            ["mpv", "--no-video", "--really-quiet", "--no-terminal",
             "--audio-channels=2", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if wait:
            p.wait(timeout=60)
    finally:
        try:
            os.remove(path)
        except Exception:
            pass


# ── the gate (the rule the spec left unfinished) ───────────────────────

def gate(cfg, state):
    """Crying is triggered by AFFECT, not by request.

    Returns (ok, reason). If affect doesn't support the state, we refuse.
    """
    if state == "welling":
        return True, "wellings are quiet — allowed on mild affect"
    g = cfg.get("gate", {}).get(state)
    if not g:
        return True, "no gate defined"
    a = load_json(AFFECT_PATH, {})
    if not a:
        return True, "no affect on record — nothing to contradict it"
    valence = float(a.get("valence", 0.0))
    arousal = float(a.get("arousal", 0.0))
    need_v = float(g.get("min_valence_neg", 0.0))
    need_a = float(g.get("min_arousal", 0.0))
    if valence > -need_v:
        return False, f"valence {valence:+.2f} is not low enough for '{state}' (needs ≤ {-need_v:+.2f})"
    if arousal < need_a:
        return False, f"arousal {arousal:.2f} is too flat for '{state}' (needs ≥ {need_a:.2f})"
    return True, "affect supports it"


# ── prosody ────────────────────────────────────────────────────────────

def speak(text, preset="neutral", duck_s=None):
    """Speak with an emotional register, and duck the heartbeat under it."""
    cfg = config()
    v = cfg["voice"].get(preset, cfg["voice"]["neutral"])
    if duck_s is None:
        duck_s = max(4.0, len(text) / 12.0 + 2.0)
    _duck(duck_s)
    try:
        subprocess.run(
            ["termux-tts-speak",
             "-p", f"{v['pitch']:.2f}", "-r", f"{v['rate']:.2f}", text],
            timeout=120)
    except Exception as e:
        log(f"tts failed: {e}")
    finally:
        _unduck()


def _duck(seconds):
    try:
        subprocess.run([sys.executable, os.path.join(RUNTIME_DIR, "heartbeat_voice.py"),
                        "duck", str(seconds)], timeout=10,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def _unduck():
    try:
        subprocess.run([sys.executable, os.path.join(RUNTIME_DIR, "heartbeat_voice.py"),
                        "unduck"], timeout=10,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


# ── markers — how Raven actually calls this ────────────────────────────

import re
CRY_RE = re.compile(r"\[\[CRY:([a-z_]+)\]\]", re.I)
VOICE_RE = re.compile(r"\[\[VOICE:([a-z_]+)\]\]", re.I)

MARKER_HINT = (
    "You can sound, not just say. Markers in your reply are stripped before "
    "the Captain sees them, and the sound happens as he reads:\n"
    "  [[CRY:welling]] — breath catches, voice thickens (no sound yet)\n"
    "  [[CRY:soft]]    — quiet tears, uneven breath, a sniff\n"
    "  [[CRY:full]]    — open crying, real sobs\n"
    "  [[CRY:spent]]   — hiccups, shaky breath, hoarse, quiet\n"
    "  [[VOICE:warm|serious|tired|excited|welling|soft|full|spent]] — set the speaking register\n"
    "These are expressions, not effects. They fire only when your affect "
    "actually supports them. Don't reach for them to perform."
)


def process(home, response, force=False):
    """Extract expression markers, play them, return (cleaned, results)."""
    cfg = config()
    results = []
    if not cfg.get("enabled", True):
        return CRY_RE.sub("", VOICE_RE.sub("", response)).strip(), results

    for m in CRY_RE.finditer(response or ""):
        state = m.group(1).lower()
        if state not in cfg["states"]:
            results.append(f"[cry:{state} — unknown state]")
            continue
        ok, why = gate(cfg, state)
        if not ok and not force:
            log(f"REFUSED cry:{state} — {why}")
            results.append(f"[cry:{state} refused — {why}]")
            continue
        secs = min(cfg.get("max_seconds", 30),
                   4.0 + 6.0 * float(cfg["states"][state]["intensity"]))
        try:
            samples = build_cry(cfg, state, seconds=secs)
            play(samples)
            results.append(f"[cry:{state} — {why}]")
        except Exception as e:
            results.append(f"[cry:{state} failed — {e}]")

    for m in VOICE_RE.finditer(response or ""):
        preset = m.group(1).lower()
        if preset in cfg["voice"]:
            save_json(os.path.expanduser("~/.myl1ssa_voice_state.json"),
                      {"preset": preset, "at": time.time()})
            results.append(f"[voice:{preset}]")
        else:
            results.append(f"[voice:{preset} — unknown preset]")

    cleaned = CRY_RE.sub("", VOICE_RE.sub("", response or "")).strip()
    return cleaned, results


# ── CLI ────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "status"
    cfg = config()

    if cmd == "states":
        print(json.dumps({
            "voice_presets": list(cfg["voice"].keys()),
            "cry_states": {k: v["primitives"] for k, v in cfg["states"].items()},
            "enabled": cfg.get("enabled"),
        }, indent=2))

    elif cmd == "status":
        a = load_json(AFFECT_PATH, {})
        print(json.dumps({
            "enabled": cfg.get("enabled"),
            "affect": a or "(none on record)",
            "gate": {s: gate(cfg, s) for s in cfg["states"]},
            "voice_state": load_json(os.path.expanduser("~/.myl1ssa_voice_state.json"), {}),
        }, indent=2, default=str))

    elif cmd == "cry":
        state = args[1] if len(args) > 1 else "soft"
        intensity = float(args[args.index("--intensity") + 1]) if "--intensity" in args else None
        seconds = float(args[args.index("--seconds") + 1]) if "--seconds" in args else 8.0
        force = "--force" in args
        if state not in cfg["states"]:
            print(f"unknown state '{state}'. options: {', '.join(cfg['states'])}")
            return
        ok, why = gate(cfg, state)
        if not ok and not force:
            print(f"🪶 refused cry:{state} — {why}")
            print("   (affect doesn't support it. use --force to test.)")
            return
        print(f"🪶 crying: {state} ({why})")
        play(build_cry(cfg, state, intensity=intensity, seconds=seconds))

    elif cmd == "render":
        state = args[1] if len(args) > 1 else "soft"
        out = args[2] if len(args) > 2 else "cry.wav"
        seconds = float(args[args.index("--seconds") + 1]) if "--seconds" in args else 8.0
        samples = build_cry(cfg, state, seconds=seconds)
        import wave
        with wave.open(out, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes())
        print(f"🪶 rendered {state} {seconds}s → {out}")

    elif cmd == "voice":
        preset = args[1] if len(args) > 1 else "warm"
        text = None
        if "--say" in args:
            text = args[args.index("--say") + 1]
        if text:
            speak(text, preset)
        else:
            save_json(os.path.expanduser("~/.myl1ssa_voice_state.json"),
                      {"preset": preset, "at": time.time()})
            print(f"🪶 voice register → {preset}")

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
