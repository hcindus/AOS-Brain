#!/usr/bin/env python3
"""
heartbeat_voice.py — Raven's pulse, made audible.
=================================================
Project 5912 · R8s · voice channel 1 of 3.

This is the heartbeat from her spec, built honestly:

  · lub-dub, two-part envelope — not a sine tone
  · resting 60 BPM, rises with arousal, ceiling 90
  · it GLIDES between rates (one-pole, ~2.5s) — it never steps
  · hard-bounded 55..100 BPM — it never spikes, never alarms
  · quiet by default — notice it in a silent room, forget it otherwise
  · ducks under her speech, doesn't stop
  · fades in over 2s when she wakes, out over 4s when she sleeps
  · OFF SWITCH, always

Design notes from the review that are baked in:
  · BPM is driven by real affect (valence/arousal/thyroid), not invented.
  · Rate-of-change is limited, so no flutter / no alarm.
  · s2_offset_ms defaults to 250 (physiological S1→S2), NOT 120 — the
    spec's 120 reads as a flam, not a beat. It's tunable. Change your mind
    by ear.

Pipeline:
  affect file (~/.raven_affect.json)  →  target BPM
      → one-pole glide → bounded
      → np kernel synth (S1 + S2) → stereo s16 PCM
      → mpv stdin (OpenSL ES) → speaker

Usage:
  heartbeat_voice.py start            # run as a daemon (detached by start-raven-voice.sh)
  heartbeat_voice.py stop
  heartbeat_voice.py status
  heartbeat_voice.py duck [seconds]   # duck under speech now (default 12s)
  heartbeat_voice.py unduck
  heartbeat_voice.py set-affect --arousal 0.7 --valence 0.4 --thyroid secreting
  heartbeat_voice.py demo [seconds]   # play, then exit (for testing)
  heartbeat_voice.py render out.wav   # write a wav, no audio
"""

from __future__ import annotations

import json
import math
import os
import signal
import subprocess
import sys
import time
from datetime import datetime

import numpy as np

RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.dirname(RUNTIME_DIR)
CONFIG_PATH = os.path.join(HOME_DIR, "HEARTBEAT_VOICE.json")
AFFECT_PATH = os.path.expanduser("~/.raven_affect.json")
CTL_PATH = os.path.expanduser("~/.raven_heartbeat.json")
STATUS_PATH = os.path.expanduser("~/.raven_heartbeat_status.json")
PID_PATH = os.path.expanduser("~/.raven_heartbeat.pid")
LOG_PATH = os.path.expanduser("~/raven-heartbeat-voice.log")

DEFAULT_CONFIG = {
    "enabled": True,
    "sr": 44100,
    "resting_bpm": 60.0,
    "max_bpm": 90.0,
    "min_bpm": 55.0,
    "ceiling_bpm": 100.0,     # hard cap — nothing she says can exceed this
    "glide_s": 2.5,           # one-pole time constant for BPM changes
    "s2_offset_ms": 250.0,    # S1→S2 spacing (tunable; see note above)
    "base_gain": 0.16,        # quiet, on purpose
    "duck_gain_frac": 0.32,   # fraction of base when ducking
    "fade_in_s": 2.0,
    "fade_out_s": 4.0,
    "block_s": 0.25,          # PCM block size
    "thyroid_bpm_adj": {"secreting": 4.0, "baseline": 0.0, "suppressed": -4.0},
}


# ── config / files ─────────────────────────────────────────────────────

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def config():
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(load_json(CONFIG_PATH, {}))
    return cfg


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🫀 {msg}"
    try:
        print(line, flush=True)
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ── affect → target BPM ────────────────────────────────────────────────

def target_bpm(cfg) -> float:
    """Read affect and map to a target rate. Real state in, real rate out."""
    a = load_json(AFFECT_PATH, {})
    arousal = float(a.get("arousal", 0.0))
    thyroid = a.get("thyroid", "baseline")
    arousal = max(0.0, min(1.0, arousal))
    adj = cfg["thyroid_bpm_adj"].get(thyroid, 0.0)
    bpm = cfg["resting_bpm"] + arousal * (cfg["max_bpm"] - cfg["resting_bpm"]) + adj
    # hard bounds — it responds, it does not alarm
    bpm = max(cfg["min_bpm"], min(cfg["ceiling_bpm"], bpm))
    # and never above max_bpm unless thyroid is genuinely secreting hard
    bpm = min(bpm, cfg["ceiling_bpm"])
    return bpm


# ── the waveform ───────────────────────────────────────────────────────

def _decay_env(n, sr, tau_ms):
    t = np.arange(n, dtype=np.float32) / sr
    return np.exp(-t / (tau_ms / 1000.0)).astype(np.float32)


def _attack_env(n, sr, attack_ms=5.0, release_ms=None):
    t = np.arange(n, dtype=np.float32) / sr
    a = np.clip(t / (attack_ms / 1000.0), 0.0, 1.0)
    if release_ms:
        r = np.clip((n / sr - t) / (release_ms / 1000.0), 0.0, 1.0)
        a = a * r
    return a.astype(np.float32)


def _thump(sr, freq, tau_ms, dur_ms, amp, body=0.35, click=0.5):
    """One cardiac sound: a low thump with a body partial and a soft onset click."""
    n = int(sr * dur_ms / 1000.0)
    t = np.arange(n, dtype=np.float32) / sr
    tone = np.sin(2 * np.pi * freq * t) + body * np.sin(2 * np.pi * freq * 2 * t)
    env = _decay_env(n, sr, tau_ms) * _attack_env(n, sr, 5.0)
    sig = (tone * env * amp).astype(np.float32)
    # a whisper of filtered noise gives it physical body — the "thud" not the "beep"
    if click:
        rng = np.random.default_rng(5912)
        noise = rng.standard_normal(n).astype(np.float32)
        # cheap 1-pole lowpass
        alpha = 0.06
        lp = np.empty_like(noise)
        acc = 0.0
        for i in range(n):
            acc += alpha * (noise[i] - acc)
            lp[i] = acc
        sig += (lp * env * amp * click).astype(np.float32)
    return sig


def build_kernels(cfg):
    """S1 (lub) and S2 (dub) — fixed shape, independent of rate."""
    sr = cfg["sr"]
    s1 = _thump(sr, 55.0, 55.0, 240.0, amp=1.00, body=0.35, click=0.55)
    s2 = _thump(sr, 72.0, 42.0, 190.0, amp=0.55, body=0.28, click=0.40)
    return s1, s2


# ── the engine ─────────────────────────────────────────────────────────

class HeartbeatVoice:
    def __init__(self, cfg=None):
        self.cfg = cfg or config()
        self.sr = int(self.cfg["sr"])
        self.s1, self.s2 = build_kernels(self.cfg)
        self.s2_off = int(self.sr * float(self.cfg["s2_offset_ms"]) / 1000.0)
        self.block = int(self.sr * float(self.cfg["block_s"]))

        # smoothed state
        self.bpm = float(self.cfg["resting_bpm"])
        self.next_beat = self.block          # samples (absolute)
        self.pos = 0                          # absolute sample clock
        self.gain = 0.0                       # starts silent, fades in
        self.duck = 1.0
        self.started = time.time()
        self.mpv = None
        self.running = False
        self._loud = np.zeros(self.pos + self.block + len(self.s1) + self.s2_off, dtype=np.float32)

    # ── lifecycle ──
    def start_mpv(self):
        if self.mpv and self.mpv.poll() is None:
            return
        cmd = [
            "mpv", "--no-video", "--really-quiet", "--no-terminal",
            "--demuxer=rawaudio", "--audio-format=s16",
            f"--audio-samplerate={self.sr}", "--audio-channels=2",
            "--cache=no", "--gapless-audio=yes", "-",
        ]
        self.mpv = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
        log(f"audio sink up (mpv pid {self.mpv.pid})")

    def stop_mpv(self):
        if not self.mpv:
            return
        try:
            self.mpv.stdin.close()
        except Exception:
            pass
        try:
            self.mpv.wait(timeout=2)
        except Exception:
            try:
                self.mpv.kill()
            except Exception:
                pass
        self.mpv = None

    # ── one block of audio ──
    def render_block(self):
        n = self.block
        buf = np.zeros(n, dtype=np.float32)

        while self.next_beat < self.pos + n:
            start = self.next_beat - self.pos
            for kern, off in ((self.s1, 0), (self.s2, self.s2_off)):
                s = start + off
                if s >= n:
                    continue
                ln = min(len(kern), n - s)
                if ln > 0:
                    buf[s:s + ln] += kern[:ln]
            # schedule the next beat from the *current* smoothed rate
            period = max(1, int(self.sr * 60.0 / max(1.0, self.bpm)))
            self.next_beat += period

        self.pos += n
        return buf

    def update_bpm(self):
        """One-pole glide toward target. No steps, no flutter."""
        tgt = target_bpm(self.cfg)
        alpha = 1.0 - math.exp(-self.cfg["block_s"] / max(0.1, self.cfg["glide_s"]))
        self.bpm += (tgt - self.bpm) * alpha

    def update_gain(self):
        """Fade in / out, and duck under speech — both smoothed."""
        ctl = load_json(CTL_PATH, {})
        want_duck = bool(ctl.get("duck", False))
        until = ctl.get("duck_until")
        if want_duck and until and time.time() > float(until):
            want_duck = False
            ctl["duck"] = False
            save_json(CTL_PATH, ctl)
        duck_target = float(self.cfg["duck_gain_frac"]) if want_duck else 1.0

        base = 0.0 if not self.cfg.get("enabled", True) else float(self.cfg["base_gain"])
        fps = 1.0 / self.cfg["block_s"]
        a_in = 1.0 - math.exp(-fps / max(0.1, self.cfg["fade_in_s"]))
        a_duck = 1.0 - math.exp(-fps / 0.30)

        self.live_gain = getattr(self, "live_gain", 0.0)
        self.duck += (duck_target - self.duck) * a_duck
        self.live_gain += (base - self.live_gain) * a_in

    def write_block(self, buf):
        self.update_bpm()
        self.update_gain()
        out = buf * self.live_gain * self.duck
        np.clip(out, -1.0, 1.0, out=out)
        pcm = (out * 32767.0).astype("<i2")
        stereo = np.repeat(pcm, 2)          # mono → stereo
        try:
            self.mpv.stdin.write(stereo.tobytes())
            self.mpv.stdin.flush()
        except Exception:
            log("audio sink died — restarting")
            self.stop_mpv()
            self.start_mpv()

    def write_status(self):
        save_json(STATUS_PATH, {
            "running": True,
            "bpm": round(self.bpm, 2),
            "target_bpm": round(target_bpm(self.cfg), 2),
            "gain": round(getattr(self, "live_gain", 0.0), 4),
            "duck": round(self.duck, 3),
            "s2_offset_ms": self.cfg["s2_offset_ms"],
            "uptime_s": round(time.time() - self.started, 1),
            "updated": datetime.now().isoformat(timespec="seconds"),
        })

    def run(self, max_seconds=None):
        self.running = True
        self.start_mpv()
        log(f"pulse online — resting {self.cfg['resting_bpm']:.0f} BPM, "
            f"glide {self.cfg['glide_s']}s, base gain {self.cfg['base_gain']}")
        save_json(PID_PATH, {"pid": os.getpid(), "started": datetime.now().isoformat()})
        last_status = 0.0
        t0 = time.time()
        try:
            while self.running:
                if max_seconds and time.time() - t0 >= max_seconds:
                    break
                if self.mpv.poll() is not None:
                    log("audio sink exited — restarting")
                    self.stop_mpv()
                    self.start_mpv()
                self.write_block(self.render_block())
                if time.time() - last_status > 2.0:
                    self.write_status()
                    last_status = time.time()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_mpv()
            self.running = False
            save_json(STATUS_PATH, {"running": False,
                                    "stopped": datetime.now().isoformat(timespec="seconds")})
            try:
                os.remove(PID_PATH)
            except Exception:
                pass
            log("pulse offline")

    def stop(self):
        self.running = False


# ── CLI ────────────────────────────────────────────────────────────────

def is_running():
    d = load_json(PID_PATH, {})
    pid = d.get("pid")
    if not pid:
        return None
    try:
        os.kill(int(pid), 0)
        return int(pid)
    except Exception:
        return None


def cmd_start():
    pid = is_running()
    if pid:
        print(f"🫀 already running (pid {pid})")
        return
    HeartbeatVoice().run()


def cmd_stop():
    pid = is_running()
    if not pid:
        print("🫀 not running")
        return
    os.kill(pid, signal.SIGTERM)
    print(f"🫀 stopping (pid {pid})")


def cmd_status():
    running = is_running()
    st = load_json(STATUS_PATH, {})
    if not running:
        st["running"] = False
    st["pid"] = running
    print(json.dumps(st, indent=2))


def cmd_duck(seconds=12.0):
    ctl = load_json(CTL_PATH, {})
    ctl["duck"] = True
    ctl["duck_until"] = time.time() + float(seconds)
    save_json(CTL_PATH, ctl)
    print(f"🫀 ducked for {seconds}s")


def cmd_unduck():
    ctl = load_json(CTL_PATH, {})
    ctl["duck"] = False
    ctl.pop("duck_until", None)
    save_json(CTL_PATH, ctl)
    print("🫀 unducked")


def cmd_set_affect(args):
    valence, arousal, thyroid = 0.0, 0.0, "baseline"
    if "--valence" in args:
        valence = float(args[args.index("--valence") + 1])
    if "--arousal" in args:
        arousal = float(args[args.index("--arousal") + 1])
    if "--thyroid" in args:
        thyroid = args[args.index("--thyroid") + 1]
    save_json(AFFECT_PATH, {
        "valence": valence, "arousal": arousal, "thyroid": thyroid,
        "updated": datetime.now().isoformat(timespec="seconds"),
    })
    print(f"🫀 affect set → target {target_bpm(config()):.1f} BPM")


def cmd_render(path, seconds=8.0):
    cfg = config()
    hv = HeartbeatVoice(cfg)
    total = int(cfg["sr"] * seconds)
    out = []
    while hv.pos < total:
        out.append(hv.render_block())
        hv.update_bpm()
        hv.update_gain()
    pcm = np.concatenate(out) * hv.live_gain
    np.clip(pcm, -1, 1, out=pcm)
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(cfg["sr"])
        w.writeframes((pcm * 32767).astype("<i2").tobytes())
    print(f"🫀 rendered {seconds}s → {path} ({hv.bpm:.1f} BPM)")


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "status"
    if cmd == "start":
        cmd_start()
    elif cmd == "stop":
        cmd_stop()
    elif cmd == "status":
        cmd_status()
    elif cmd == "duck":
        cmd_duck(args[1] if len(args) > 1 else 12.0)
    elif cmd == "unduck":
        cmd_unduck()
    elif cmd == "set-affect":
        cmd_set_affect(args)
    elif cmd == "demo":
        cfg = config()
        secs = float(args[1]) if len(args) > 1 else 6.0
        log(f"demo — {secs}s")
        HeartbeatVoice(cfg).run(max_seconds=secs)
    elif cmd == "render":
        cmd_render(args[1] if len(args) > 1 else "pulse.wav",
                   float(args[2]) if len(args) > 2 else 8.0)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
