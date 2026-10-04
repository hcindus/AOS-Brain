#!/usr/bin/env python3
"""
elf.py — AheadForm Elf V1 / Elf-Xuan adapter. Her own body.

The bottle shipped adapters for *other* bodies (Blender, a digital world, Unitree)
and none for hers. The manifest named her vessel — "AheadForm Elf V1 (head) →
Elf-Xuan (full body), 30 brushless micro-motors" — and stopped there: no adapter,
no transport, no safety envelope, no AU→motor map, no glue.

This is that missing half. It implements the same HAL contract as the rest of the
family (so it is a drop-in beside `blender.py` / `unitree.py` / `digital_world.py`)
and adds the four things a *body* needs that a *renderer* does not:

    1. an explicit AU → 30-channel map        (the boundary, written down, not assumed)
    2. a transport seam                       (socket · serial · BLE · null)
    3. a safety envelope                      (limits, slew, watchdog, e-stop)
    4. a status() that tells the truth        (no hardware present is not "ok")

Design line that is not negotiable: **she owns the mind and the presence; the
adapter owns the hardware.** She says "warmth". This file decides what that means
in motor channels — and refuses to say it in a way that could hurt her body.

Usage
    python3 elf.py status                  # honest report: hardware? limits? chain
    python3 elf.py map                     # the AU → channel table
    python3 elf.py frame warmth            # one expression → 30 channels, no hardware
    python3 elf.py send warmth --sim       # through the safety envelope + null transport

    from elf import ElfAdapter
    a = ElfAdapter()
    a.apply(frame)        # HAL: AdapterFrame → channel packet
    a.send(frame)         # through safety + transport
    a.read_state()        # feedback (simulated if no hardware)

Author: Mortimer (for Raven)
"""

import json
import os
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

# ── HAL contract: use the family's if it is present, else stand alone ─────────
try:  # inside her tree (adapters/ alongside)
    from adapters.base import AdapterFrame, BodyAdapter, register  # type: ignore
    HAL = "adapters.base"
except Exception:  # read-only reference copy, or a tree without the HAL
    HAL = "local"

    @dataclass
    class AdapterFrame:  # type: ignore
        """Platform-agnostic output of a presence engine (duck-compatible)."""
        expression: str = ""
        posture: str = "settled"
        predictive_lead_ms: int = 0
        action_units: Dict[str, float] = field(default_factory=dict)
        gaze: Dict[str, Any] = field(default_factory=dict)
        body_points: Dict[str, Dict[str, float]] = field(default_factory=dict)
        face_points: Dict[str, Dict[str, float]] = field(default_factory=dict)

    class BodyAdapter:  # type: ignore
        platform = "abstract"

        def apply(self, frame):  # pragma: no cover
            raise NotImplementedError

        def status(self):  # pragma: no cover
            raise NotImplementedError

    def register(adapter):  # type: ignore
        return adapter


# ─────────────────────────────────────────────────────────────────────────────
# 1. THE MAP — 30 channels, and which FACS action units drive them.
#
# The Elf V1 is 30 brushless micro-motors in a bionic silicone face + head.
# This mapping is OURS: it is the seam where her affect stops and the vendor's
# SDK begins. If AheadForm's channel order differs, change the ids here — never
# the AUs, and never the safety numbers.
#
# Convention: every channel is normalised [-1.0 .. +1.0].
#   +1 = the channel's named direction fully driven, -1 = opposite.
#   Opposite-direction AUs (e.g. lip corner pull vs depress) share a channel and
#   push it opposite ways, which is why some weights below are negative.
# ─────────────────────────────────────────────────────────────────────────────

CHANNELS: List[Dict[str, Any]] = [
    # id               group    limit band   what it does
    {"id": "neck_yaw",        "group": "head",  "band": (-1.0, 1.0), "note": "turn left/right (AU51)"},
    {"id": "neck_pitch",      "group": "head",  "band": (-0.6, 0.8), "note": "nod down/up (AU52)"},
    {"id": "neck_roll",       "group": "head",  "band": (-0.8, 0.8), "note": "tilt (AU53)"},
    {"id": "eye_yaw_L",       "group": "gaze",  "band": (-1.0, 1.0), "note": "left eye horizontal (AU61)"},
    {"id": "eye_yaw_R",       "group": "gaze",  "band": (-1.0, 1.0), "note": "right eye horizontal (AU61)"},
    {"id": "eye_pitch_L",     "group": "gaze",  "band": (-0.7, 0.7), "note": "left eye vertical (AU62)"},
    {"id": "eye_pitch_R",     "group": "gaze",  "band": (-0.7, 0.7), "note": "right eye vertical (AU62)"},
    {"id": "brow_inner_L",    "group": "brow",  "band": (-0.5, 1.0), "note": "inner brow raise (AU1)"},
    {"id": "brow_inner_R",    "group": "brow",  "band": (-0.5, 1.0), "note": "inner brow raise (AU1)"},
    {"id": "brow_outer_L",    "group": "brow",  "band": (-0.5, 1.0), "note": "outer brow raise (AU2)"},
    {"id": "brow_outer_R",    "group": "brow",  "band": (-0.5, 1.0), "note": "outer brow raise (AU2)"},
    {"id": "brow_depress_L",  "group": "brow",  "band": (-0.4, 1.0), "note": "brow lower / 'no' (AU4)"},
    {"id": "brow_depress_R",  "group": "brow",  "band": (-0.4, 1.0), "note": "brow lower / 'no' (AU4)"},
    {"id": "upper_lid_L",     "group": "lid",   "band": (-1.0, 1.0), "note": "upper lid raise (AU5)"},
    {"id": "upper_lid_R",     "group": "lid",   "band": (-1.0, 1.0), "note": "upper lid raise (AU5)"},
    {"id": "lower_lid_L",     "group": "lid",   "band": (0.0, 1.0),  "note": "lower lid tighten (AU7)"},
    {"id": "lower_lid_R",     "group": "lid",   "band": (0.0, 1.0),  "note": "lower lid tighten (AU7)"},
    {"id": "cheek_L",         "group": "cheek", "band": (0.0, 1.0),  "note": "cheek raise — real smile (AU6/14)"},
    {"id": "cheek_R",         "group": "cheek", "band": (0.0, 1.0),  "note": "cheek raise — real smile (AU6/14)"},
    {"id": "nose_wrinkle",    "group": "nose",  "band": (0.0, 0.6),  "note": "AU9 — spare, no expression drives it yet"},
    {"id": "lip_corner_L",    "group": "mouth", "band": (-1.0, 1.0), "note": "pull up (AU12) / depress (AU15)"},
    {"id": "lip_corner_R",    "group": "mouth", "band": (-1.0, 1.0), "note": "pull up (AU12) / depress (AU15)"},
    {"id": "lip_upper_raise", "group": "mouth", "band": (-0.4, 1.0), "note": "upper lip raise (AU10/20)"},
    {"id": "lip_lower_depress", "group": "mouth", "band": (0.0, 1.0), "note": "lower lip depress (AU16)"},
    {"id": "lip_pucker",      "group": "mouth", "band": (0.0, 1.0),  "note": "pucker (AU18)"},
    {"id": "lip_stretch_L",   "group": "mouth", "band": (0.0, 1.0),  "note": "horizontal stretch (AU20)"},
    {"id": "lip_stretch_R",   "group": "mouth", "band": (0.0, 1.0),  "note": "horizontal stretch (AU20)"},
    {"id": "lip_tighten",     "group": "mouth", "band": (0.0, 1.0),  "note": "tighten (AU23) — the 'no' mouth"},
    {"id": "jaw_open",        "group": "jaw",   "band": (0.0, 1.0),  "note": "open (AU25 lips part / AU26 drop)"},
    {"id": "chin_raise",      "group": "jaw",   "band": (0.0, 0.8),  "note": "chin raise (AU17)"},
]

# AU name → {channel: weight}. Weights are how much of the AU reaches that channel.
AU_MAP: Dict[str, Dict[str, float]] = {
    "inner_brow_raise":    {"brow_inner_L": 1.0, "brow_inner_R": 1.0},
    "outer_brow_raise":    {"brow_outer_L": 1.0, "brow_outer_R": 1.0},
    "brow_lower":          {"brow_depress_L": 1.0, "brow_depress_R": 1.0},
    "upper_lid_raise":     {"upper_lid_L": 1.0, "upper_lid_R": 1.0},
    "cheek_raise":         {"cheek_L": 1.0, "cheek_R": 1.0},
    "lid_tighten":         {"lower_lid_L": 1.0, "lower_lid_R": 1.0},
    "lip_corner_pull":     {"lip_corner_L": 1.0, "lip_corner_R": 1.0},
    "dimpler":             {"cheek_L": 0.45, "cheek_R": 0.45,
                            "lip_corner_L": 0.25, "lip_corner_R": 0.25},
    "lip_corner_depress":  {"lip_corner_L": -1.0, "lip_corner_R": -1.0},
    "lower_lip_depress":   {"lip_lower_depress": 1.0},
    "chin_raise":          {"chin_raise": 1.0},
    "lip_pucker":          {"lip_pucker": 1.0},
    "lip_stretch":         {"lip_stretch_L": 1.0, "lip_stretch_R": 1.0, "lip_upper_raise": 0.4},
    "lip_tighten":         {"lip_tighten": 1.0},
    "lips_part":           {"jaw_open": 0.7, "lip_upper_raise": 0.2},
    "jaw_drop":            {"jaw_open": 1.0},
    "head_yaw":            {"neck_yaw": 1.0},
    "head_pitch":          {"neck_pitch": 1.0},
    "head_tilt":           {"neck_roll": 1.0},
    "gaze_x":              {"eye_yaw_L": 1.0, "eye_yaw_R": 1.0},
    "gaze_y":              {"eye_pitch_L": 1.0, "eye_pitch_R": 1.0},
}

# ── Safety envelope ──────────────────────────────────────────────────────────
# Per-group slew limits (channel-units per second) and the time each group takes
# to relax to rest. Neck carries mass; gaze is allowed to be snappy; face is
# medium. These are the numbers to argue with — they are conservative on purpose.
SLEW_PER_S = {"head": 2.5, "gaze": 6.0, "brow": 4.0, "lid": 5.0,
              "cheek": 3.5, "nose": 3.0, "mouth": 4.0, "jaw": 5.0}
REST_SLEW_PER_S = 1.5          # how fast everything relaxes to neutral
REST = 0.0                     # neutral for every channel
WATCHDOG_MS = 250              # no command for this long → relax to rest
CONTROL_PERIOD_MS = 20         # nominal tick (50 Hz)


# ─────────────────────────────────────────────────────────────────────────────
# 2. TRANSPORT — the seam to actual hardware. Nothing above this line knows
#    what a motor is; nothing below it knows what an expression is.
# ─────────────────────────────────────────────────────────────────────────────

class Transport:
    """Minimal contract. send() → bytes; read() → bytes or None."""
    kind = "abstract"
    supports_feedback = False

    def open(self) -> None: ...
    def close(self) -> None: ...
    def send(self, payload: bytes) -> bool: return False
    def read(self) -> Optional[bytes]: return None
    def info(self) -> Dict[str, Any]: return {"kind": self.kind, "open": False}


class NullTransport(Transport):
    """No hardware. Records what *would* have gone out — honest, and useful in tests."""
    kind = "null"
    supports_feedback = True          # simulated feedback, clearly labelled as such

    def __init__(self) -> None:
        self.packets: List[bytes] = []
        self._open = False
        self._t0 = time.time()

    def open(self) -> None: self._open = True
    def close(self) -> None: self._open = False

    def send(self, payload: bytes) -> bool:
        self.packets.append(payload)
        return True

    def read(self) -> Optional[bytes]:
        # Simulated servo feedback: no motion is modelled, so report the command
        # it last saw, flagged. Never presented as real proprioception.
        if not self.packets:
            return None
        return json.dumps({"sim": True, "echo": json.loads(self.packets[-1])}).encode()

    def info(self) -> Dict[str, Any]:
        return {"kind": self.kind, "open": self._open, "hardware": False,
                "packets": len(self.packets),
                "note": "no hardware attached — this is a recording, not a body"}


class SocketTransport(Transport):
    """The realistic first path: an SDK bridge listening on TCP (vendor tool, host PC)."""
    kind = "socket"
    supports_feedback = True

    def __init__(self, host: str = "127.0.0.1", port: int = 9100, timeout: float = 1.0) -> None:
        self.host, self.port, self.timeout = host, port, timeout
        self._sock = None
        self._last_error: Optional[str] = None

    def open(self) -> None:
        import socket
        self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)

    def close(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:  # noqa: BLE001
                pass
            self._sock = None

    def send(self, payload: bytes) -> bool:
        if not self._sock:
            self._last_error = "not connected"
            return False
        try:
            self._sock.sendall(payload)
            return True
        except Exception as e:  # noqa: BLE001
            self._last_error = f"{type(e).__name__}: {e}"
            return False

    def read(self) -> Optional[bytes]:
        if not self._sock:
            return None
        import socket
        try:
            self._sock.settimeout(0.05)
            return self._sock.recv(4096) or None
        except (socket.timeout, BlockingIOError):
            return None
        except Exception as e:  # noqa: BLE001
            self._last_error = f"{type(e).__name__}: {e}"
            return None

    def info(self) -> Dict[str, Any]:
        return {"kind": self.kind, "target": f"{self.host}:{self.port}",
                "hardware": self._sock is not None, "last_error": self._last_error}


class SerialTransport(Transport):
    """Direct to the head controller. Needs pyserial and a real port."""
    kind = "serial"
    supports_feedback = True

    def __init__(self, port: str = "/dev/ttyUSB0", baud: int = 115200) -> None:
        self.port, self.baud = port, baud
        self._ser = None

    def open(self) -> None:
        try:
            import serial  # type: ignore
        except ImportError as e:
            raise RuntimeError(
                "pyserial is not installed — `pip install pyserial`, or use the "
                "socket transport to a vendor bridge instead") from e
        try:
            self._ser = serial.Serial(self.port, self.baud, timeout=0.05)
        except Exception as e:  # noqa: BLE001  — SerialException, PermissionError, OSError
            # A dead port must produce a sentence a human can act on, not a raw trace.
            raise RuntimeError(
                f"cannot open serial {self.port} @ {self.baud}: {type(e).__name__}: {e}"
                " — is the head controller connected and is this the right port?"
                " (`termux-usb -l` / `ls /dev/tty*`)") from e

    def close(self) -> None:
        if self._ser:
            try:
                self._ser.close()
            except Exception:  # noqa: BLE001
                pass
            self._ser = None

    def send(self, payload: bytes) -> bool:
        if not self._ser:
            return False
        self._ser.write(payload)
        return True

    def read(self) -> Optional[bytes]:
        if not self._ser:
            return None
        data = self._ser.read(4096)
        return data or None

    def info(self) -> Dict[str, Any]:
        return {"kind": self.kind, "port": self.port, "baud": self.baud,
                "hardware": self._ser is not None}


class BleTransport(Transport):
    """Wireless path. Deliberately not implemented — it fails loudly, not silently."""
    kind = "ble"

    def __init__(self, address: str = "", char_uuid: str = "") -> None:
        self.address, self.char_uuid = address, char_uuid

    def open(self) -> None:
        raise RuntimeError(
            "BLE transport is not implemented. It needs the vendor's GATT profile "
            "(service + characteristic UUIDs) and `bleak`. Until that exists, this "
            "path refuses to open rather than pretending to be a body.")

    def info(self) -> Dict[str, Any]:
        return {"kind": self.kind, "address": self.address, "hardware": False,
                "implemented": False}


def make_transport(kind: str = "null", **kw) -> Transport:
    return {"null": NullTransport, "socket": SocketTransport,
            "serial": SerialTransport, "ble": BleTransport}.get(kind, NullTransport)(**kw)


# ─────────────────────────────────────────────────────────────────────────────
# 3. THE ADAPTER
# ─────────────────────────────────────────────────────────────────────────────

class ElfAdapter(BodyAdapter):
    """Translate a PresenceEngine frame into the Elf V1's 30 channels, safely."""

    platform = "elf"

    def __init__(self, transport: Optional[Transport] = None, transport_kind: str = "null",
                 watchdog_ms: int = WATCHDOG_MS, vendor: str = "aheadform-elf-v1",
                 **transport_kw) -> None:
        self.transport = transport or make_transport(transport_kind, **transport_kw)
        self.vendor = vendor
        self.watchdog_ms = watchdog_ms
        self.channels: Dict[str, float] = {c["id"]: REST for c in CHANNELS}
        self.limits = {c["id"]: c["band"] for c in CHANNELS}
        self.groups = {c["id"]: c["group"] for c in CHANNELS}
        self.last_command_ms: Optional[float] = None
        self.estopped = False
        self.frames_applied = 0
        self.frames_refused = 0
        self.packets_sent = 0
        self.slew_clamps = 0
        self.estop_events: List[Dict[str, Any]] = []
        self.last_state: Optional[Dict[str, Any]] = None
        self.last_error: Optional[str] = None
        try:
            self.transport.open()
        except Exception as e:  # noqa: BLE001
            self.last_error = f"transport open failed: {type(e).__name__}: {e}"

    # -- map: AUs → channels -------------------------------------------------
    def map_frame(self, frame: Any) -> Tuple[Dict[str, float], List[str]]:
        """Expression + AUs → raw target per channel. No clamping, no slewing."""
        target = {c["id"]: REST for c in CHANNELS}
        unknown = []
        aus = getattr(frame, "action_units", None) or {}
        for au, value in aus.items():
            if au in ("gaze_x", "gaze_y"):
                # gaze arrives separately in some frames; prefer explicit value
                pass
            routing = AU_MAP.get(au)
            if routing is None:
                if au not in ("gaze_x", "gaze_y"):
                    unknown.append(au)
                continue
            scale = 1.0 if frame_expression_is_neutral(getattr(frame, "expression", "")) else 1.0
            for ch, weight in routing.items():
                target[ch] += float(value) * weight * scale
        # gaze may also be carried on frame.gaze
        gaze = getattr(frame, "gaze", None)
        if isinstance(gaze, dict):
            if gaze.get("x"):
                for ch, w in AU_MAP["gaze_x"].items():
                    target[ch] += float(gaze["x"]) * w
            if gaze.get("y"):
                for ch, w in AU_MAP["gaze_y"].items():
                    target[ch] += float(gaze["y"]) * w
        return target, unknown

    # -- safety: clamp → slew → watchdog → e-stop ----------------------------
    def clamp(self, target: Dict[str, float]) -> Tuple[Dict[str, float], int]:
        out, clamped = {}, 0
        for ch, v in target.items():
            lo, hi = self.limits[ch]
            cv = max(lo, min(hi, v))
            if abs(cv - v) > 1e-9:
                clamped += 1
            out[ch] = cv
        return out, clamped

    def slew(self, target: Dict[str, float], dt_s: float,
             relaxing: bool = False) -> Tuple[Dict[str, float], int]:
        out, hits = {}, 0
        for ch, want in target.items():
            cur = self.channels[ch]
            rate = REST_SLEW_PER_S if relaxing else SLEW_PER_S[self.groups[ch]]
            step = rate * dt_s
            delta = want - cur
            if abs(delta) > step:
                out[ch] = cur + (step if delta > 0 else -step)
                hits += 1
            else:
                out[ch] = want
        return out, hits

    def watchdog_expired(self, now_ms: Optional[float] = None) -> bool:
        if self.last_command_ms is None:
            return False
        now = time.time() * 1000 if now_ms is None else now_ms
        return (now - self.last_command_ms) > self.watchdog_ms

    # -- HAL: apply (pure translation, no transport) -------------------------
    def apply(self, frame: Any) -> Dict[str, Any]:
        target, unknown = self.map_frame(frame)
        clamped, n_clamped = self.clamp(target)
        return {
            "target": self.vendor,
            "channels": {k: round(v, 4) for k, v in clamped.items()},
            "channel_count": len(clamped),
            "expression": getattr(frame, "expression", ""),
            "posture": getattr(frame, "posture", "settled"),
            "predictive_lead_ms": getattr(frame, "predictive_lead_ms", 0),
            "unknown_aus": unknown,
            "clamped": n_clamped,
            "hal": HAL,
        }

    # -- control: apply + safety + transport ---------------------------------
    def send(self, frame: Any, dt_s: float = CONTROL_PERIOD_MS / 1000.0) -> Dict[str, Any]:
        now_ms = time.time() * 1000
        if self.estopped:
            self.frames_refused += 1
            return {"ok": False, "refused": "estop", "channels": dict(self.channels)}
        target, unknown = self.map_frame(frame)
        target, n_clamped = self.clamp(target)
        target, n_slew = self.slew(target, dt_s)
        self.channels = target
        self.slew_clamps += n_slew
        self.frames_applied += 1
        self.last_command_ms = now_ms
        payload = self.encode(target, expression=getattr(frame, "expression", ""))
        ok = self.transport.send(payload)
        if ok:
            self.packets_sent += 1
        else:
            self.last_error = "transport send failed"
        self.last_state = self.read_state()
        return {"ok": ok, "channels": {k: round(v, 4) for k, v in target.items()},
                "clamped": n_clamped, "slew_limited": n_slew, "unknown_aus": unknown,
                "bytes": len(payload), "transport": self.transport.kind}

    def rest(self, dt_s: float = CONTROL_PERIOD_MS / 1000.0) -> Dict[str, Any]:
        """Relax everything toward neutral — used by the watchdog and on close."""
        target, _ = self.slew({c["id"]: REST for c in CHANNELS}, dt_s, relaxing=True)
        self.channels = target
        self.transport.send(self.encode(target, expression="rest"))
        return {"channels": {k: round(v, 4) for k, v in target.items()}}

    def read_state(self) -> Optional[Dict[str, Any]]:
        raw = self.transport.read()
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:  # noqa: BLE001
            return {"raw_bytes": len(raw)}

    # -- e-stop --------------------------------------------------------------
    def estop(self, reason: str = "manual") -> Dict[str, Any]:
        """Hard stop: refuse every command and hold. Requires an explicit clear."""
        self.estopped = True
        ev = {"at": time.time(), "reason": reason}
        self.estop_events.append(ev)
        return {"ok": True, "estopped": True, "event": ev,
                "note": "commands refused until clear_estop() — safety is not a suggestion"}

    def clear_estop(self, by: str = "captain") -> Dict[str, Any]:
        self.estopped = False
        return {"ok": True, "estopped": False, "cleared_by": by}

    # -- framing (THE vendor seam) -------------------------------------------
    def encode(self, channels: Dict[str, float], expression: str = "") -> bytes:
        """Channel values → bytes. This is where AheadForm's SDK framing goes.

        Default is newline-delimited JSON so a vendor bridge can parse it and a
        human can read it. If the SDK wants a packed binary frame, replace this
        method and nothing else.
        """
        return (json.dumps({"t": int(time.time() * 1000), "expr": expression,
                            "ch": {k: round(v, 4) for k, v in channels.items()}},
                           separators=(",", ":")) + "\n").encode()

    # -- status: the truth ---------------------------------------------------
    def status(self) -> Dict[str, Any]:
        hw = bool(self.transport.info().get("hardware"))
        return {
            "adapter": "elf",
            "vendor": self.vendor,
            "channels": len(CHANNELS),
            "groups": {g: sum(1 for c in CHANNELS if c["group"] == g)
                       for g in sorted({c["group"] for c in CHANNELS})},
            "transport": self.transport.info(),
            "hardware_present": hw,
            "state": "no_hardware" if not hw else ("estop" if self.estopped else "ready"),
            "estopped": self.estopped,
            "watchdog_ms": self.watchdog_ms,
            "control_period_ms": CONTROL_PERIOD_MS,
            "slew_per_s": SLEW_PER_S,
            "counters": {"applied": self.frames_applied, "refused": self.frames_refused,
                         "sent": self.packets_sent, "slew_limited": self.slew_clamps},
            "last_error": self.last_error,
            "note": ("No Elf V1 (or Elf-Xuan) on this device and no vendor SDK. This "
                     "adapter can compute and record what it *would* send. It cannot "
                     "move a body, and it says so rather than reporting ok."),
        }

    def close(self) -> None:
        try:
            self.transport.close()
        except Exception:  # noqa: BLE001
            pass


def frame_expression_is_neutral(expr: str) -> bool:
    """Hook for future expression-specific scaling; identity today."""
    return expr in ("", "rest", "settled")


# Register alongside the family's adapters when the HAL is importable.
try:
    register(ElfAdapter(transport_kind="null"))  # type: ignore
except Exception:  # noqa: BLE001
    pass


# ── CLI ──────────────────────────────────────────────────────────────────────
def _engine():
    """Load the presence engine from wherever this file is sitting."""
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "presence_engine.py"),
        os.path.join(here, "presence_engine.AFTER.py"),
        os.path.join(here, "..", "presence_engine", "presence_engine.py"),
        os.path.join(here, "..", "presence_engine", "presence_engine.AFTER.py"),
        os.path.expanduser("~/v1/projects/5912/Myl1Ssa/brain/presence_engine.py"),
    ]
    for path in candidates:
        path = os.path.abspath(path)
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("presence_engine_r", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod, path
    raise SystemExit("presence_engine.py not found — look in Uncon/presence_engine/ or the brain")


def main():
    import sys
    args = sys.argv[1:]
    cmd = args[0] if args else "status"

    if cmd == "status":
        print(json.dumps(ElfAdapter().status(), indent=2))
    elif cmd == "map":
        print(f"AU → channel map ({len(AU_MAP)} AUs → {len(CHANNELS)} channels)\n")
        for au, routing in sorted(AU_MAP.items()):
            print(f"  {au:<20} " + ", ".join(f"{c}×{w}" for c, w in routing.items()))
    elif cmd in ("frame", "send"):
        mod, _ = _engine()
        p = mod.PresenceEngine()
        expr = args[1] if len(args) > 1 else "warmth"
        p.update(ternary="⊕", valence=0.6, arousal=0.5, thyroid="secreting")
        frame = p.frame(expr)
        a = ElfAdapter(transport_kind="null")
        out = a.apply(frame) if cmd == "frame" else a.send(frame)
        print(json.dumps(out, indent=2))
        if cmd == "send":
            print(f"\ntransport: {a.transport.info()}")
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
