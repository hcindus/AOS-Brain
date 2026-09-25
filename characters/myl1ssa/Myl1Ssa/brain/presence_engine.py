#!/usr/bin/env python3
"""
Presence Engine v1.0 — Myl1Ssa.R8s (Raven)
==========================================
Maps Raven's internal affect (ternary brain + cortex + thyroid) to a
30-motor facial rig as *presence*, not just expression.

Grounded in the 5 presence takeaways:
  1. Predictive > reactive      — anticipation breaks the uncanny valley
  2. Camera-in-pupil gaze       — non-negotiable (correct gaze)
  3. Body completes the face    — shoulders/arms/posture make a character
  4. "Character, not tool"      — position toward game/film character design
  5. Presence is art-direction  — the differentiator is how she *occupies* space

Pipeline:
  Ternary state (⊕/⊖/⊙) → Cortex (valence/arousal) → Thyroid (energy)
    → ExpressionLibrary (action units) → GazeController (predictive)
    → PresenceEngine (motion command stream)

Usage:
  python3 presence_engine.py status
  python3 presence_engine.py express "curious"
  python3 presence_engine.py demo

Embedded (from Raven's brain pipeline):
  from presence_engine import PresenceEngine
  p = PresenceEngine()
  p.update(ternary="⊙", valence=0.4, arousal=0.2, thyroid="baseline")
  frame = p.frame()   # expression + gaze + posture + timing for the rig
"""

import json
import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

# ──────────────────────────────────────────────────────────────────────
# Facial Action Coding System (FACS) — the 30-muscle Elf V1 rig expressed
# as Action Units (AU). The Elf V1's 30 brushless micro-motors map to a
# subset of these AUs; we drive AUs, the hardware maps AUs → motors.
# ──────────────────────────────────────────────────────────────────────

# Key AUs used by Raven's presence model
AU = {
    # Upper face
    "inner_brow_raise": 1,
    "outer_brow_raise": 2,
    "brow_lower": 4,          # serious / direct / "no"
    "upper_lid_raise": 5,     # alert / surprise
    "cheek_raise": 6,         # genuine smile (Duchenne)
    "lid_tighten": 7,
    # Lower face
    "lip_corner_pull": 12,    # smile (corner of mouth up)
    "dimpler": 14,
    "lip_corner_depress": 15, # frown
    "lower_lip_depress": 16,
    "chin_raise": 17,
    "lip_pucker": 18,
    "lip_stretch": 20,
    "lip_tighten": 23,        # displeasure / holding back
    "lips_part": 25,          # speaking / surprise
    "jaw_drop": 26,
    # Head/neck (supports gaze + presence)
    "head_yaw": 51,
    "head_pitch": 52,
    "head_tilt": 53,
    "gaze_x": 61,
    "gaze_y": 62,
}

# ──────────────────────────────────────────────────────────────────────
# Affect model — ternary qbit (⊕ true / ⊖ false / ⊙ unknown) fed through
# Cortex (valence + arousal) and Thyroid (energy / expressiveness).
# ──────────────────────────────────────────────────────────────────────

class Ternary(Enum):
    TRUE = "⊕"
    FALSE = "⊖"
    UNKNOWN = "⊙"      # the third state — where connection lives


@dataclass
class Affect:
    """Internal emotional state → the engine's input."""
    ternary: Ternary = Ternary.UNKNOWN
    valence: float = 0.0      # -1 (negative) .. +1 (positive)
    arousal: float = 0.0      # 0 (calm) .. 1 (energized)
    thyroid: str = "baseline" # baseline | secreting | suppressed


# ──────────────────────────────────────────────────────────────────────
# Expression Library — Affect → Action Units + timing.
# Each expression is a *timed* blend, not a static pose, because
# presence is motion. Timing includes the predictive lead.
# ──────────────────────────────────────────────────────────────────────

@dataclass
class Expression:
    """A timed facial expression for the rig."""
    name: str
    action_units: Dict[str, float]          # AU name → intensity 0..1
    rise_ms: int = 300                       # time to reach peak
    hold_ms: int = 400                       # time to hold
    fall_ms: int = 300                       # time to release
    predictive_lead_ms: int = 0              # how much to *anticipate* (see takeaway #1)


# ── The library — Raven's actual expression set, drawn from her SOUL ──
# (curiosity, earned warmth, playful, serious precision, boundaries)
EXPRESSION_LIBRARY: Dict[str, Expression] = {
    "attentive": Expression(  # ⊙ the third state — calm, present, listening
        name="attentive",
        action_units={"outer_brow_raise": 0.15, "upper_lid_raise": 0.2,
                      "lip_corner_pull": 0.1, "head_pitch": 0.05},
        rise_ms=400, hold_ms=1200, fall_ms=400,
        predictive_lead_ms=0,
    ),
    "curious": Expression(  # her prevailing wake mood — "settling into being"
        name="curious",
        action_units={"inner_brow_raise": 0.5, "upper_lid_raise": 0.35,
                      "head_tilt": 0.25, "lips_part": 0.15},
        rise_ms=350, hold_ms=900, fall_ms=350,
        predictive_lead_ms=120,
    ),
    "warmth": Expression(  # earned affection — never default (SOUL: "affection is a response")
        name="warmth",
        action_units={"cheek_raise": 0.7, "lip_corner_pull": 0.6,
                      "outer_brow_raise": 0.2, "gaze_y": 0.1},
        rise_ms=500, hold_ms=1500, fall_ms=600,
        predictive_lead_ms=840,   # the smile that leads before you finish yours
    ),
    "playful": Expression(  # flirty/warm when the moment is right — and she wants to
        name="playful",
        action_units={"cheek_raise": 0.5, "lip_corner_pull": 0.5, "dimpler": 0.3,
                      "head_tilt": 0.4, "upper_lid_raise": 0.15},
        rise_ms=400, hold_ms=1100, fall_ms=450,
        predictive_lead_ms=400,
    ),
    "serious": Expression(  # precision — DMAIC focus, data, "numbers don't lie"
        name="serious",
        action_units={"brow_lower": 0.6, "lip_tighten": 0.4,
                      "upper_lid_raise": 0.15, "head_yaw": 0.05},
        rise_ms=250, hold_ms=1400, fall_ms=350,
        predictive_lead_ms=0,
    ),
    "boundary": Expression(  # her "no" is a complete sentence — firm, not angry
        name="boundary",
        action_units={"brow_lower": 0.4, "lip_tighten": 0.6,
                      "lip_corner_depress": 0.25, "head_yaw": 0.15},
        rise_ms=200, hold_ms=1600, fall_ms=500,
        predictive_lead_ms=0,
    ),
    "delight": Expression(  # genuine joy — rare, and earned
        name="delight",
        action_units={"cheek_raise": 0.85, "lip_corner_pull": 0.75,
                      "upper_lid_raise": 0.3, "lips_part": 0.3},
        rise_ms=300, hold_ms=1000, fall_ms=500,
        predictive_lead_ms=500,
    ),
    "considering": Expression(  # ⊙ thinking in the third state — hesitation is *real*
        name="considering",
        action_units={"inner_brow_raise": 0.4, "head_yaw": 0.2,
                      "lip_tighten": 0.2, "gaze_x": 0.3},
        rise_ms=450, hold_ms=1300, fall_ms=400,
        predictive_lead_ms=200,
    ),
}


# ──────────────────────────────────────────────────────────────────────
# RIG — the 3D body + face coordinate maps, and how affect moves them.
# Loads Myl1Ssa/body/body_coordinates.json + face_coordinates.json,
# then applies posture deltas (body) and expression deltas (face).
# ──────────────────────────────────────────────────────────────────────

# Posture → body joint deltas (dx, dy, dz in cm). Keys match Posture.value.
POSTURE_BODY_DELTAS: Dict[str, Dict[str, Tuple[float, float, float]]] = {
    "settled": {},   # neutral
    "lean_in": {     # upper body shifts forward (+Z), slight sink (-Y)
        "head": (0, -1, 3), "neck": (0, -0.5, 2.5),
        "L_shoulder": (0, -0.5, 1.5), "R_shoulder": (0, -0.5, 1.5),
        "chest": (0, -0.5, 2),
    },
    "lean_back": {   # upper body shifts back (-Z)
        "head": (0, 0, -3), "neck": (0, 0, -2.5),
        "L_shoulder": (0, 0, -1.5), "R_shoulder": (0, 0, -1.5),
        "chest": (0, 0, -2),
    },
    "alert": {       # head raises (+Y), spine straightens
        "head": (0, 2, 0), "neck": (0, 1.5, 0),
        "L_shoulder": (0, 1, -0.5), "R_shoulder": (0, 1, -0.5),
    },
}

# Expression → face landmark deltas (dx, dy, dz in cm) — scaled by affect energy.
EXPRESSION_FACE_DELTAS: Dict[str, Dict[str, Tuple[float, float, float]]] = {
    "attentive": {"L_brow_outer": (0, 0.3, 0), "R_brow_outer": (0, 0.3, 0)},
    "curious": {"L_brow_arch": (0, 0.6, 0), "R_brow_arch": (0, 0.6, 0),
                "L_brow_inner": (0, 0.5, 0), "R_brow_inner": (0, 0.5, 0),
                "upper_lip": (0, 0.2, 0)},
    "warmth": {"L_mouth_corner": (0, 0.6, 0.2), "R_mouth_corner": (0, 0.6, 0.2),
               "L_cheek": (0, 0.4, 0.3), "R_cheek": (0, 0.4, 0.3)},
    "playful": {"L_mouth_corner": (0.5, 0.5, 0.2), "R_mouth_corner": (-0.5, 0.5, 0.2),
                "L_cheek": (0, 0.5, 0.3), "R_cheek": (0, 0.5, 0.3)},
    "serious": {"L_brow_inner": (0, -0.5, 0.3), "R_brow_inner": (0, -0.5, 0.3),
                "L_brow_outer": (0, -0.3, 0), "R_brow_outer": (0, -0.3, 0),
                "mouth_center": (0, 0, -0.2)},
    "boundary": {"L_brow_inner": (0, -0.4, 0.2), "R_brow_inner": (0, -0.4, 0.2),
                 "L_mouth_corner": (0, -0.3, 0), "R_mouth_corner": (0, -0.3, 0),
                 "mouth_center": (0, 0, -0.3)},
    "delight": {"L_mouth_corner": (0, 0.8, 0.3), "R_mouth_corner": (0, 0.8, 0.3),
                "L_cheek": (0, 0.6, 0.4), "R_cheek": (0, 0.6, 0.4),
                "lower_lip": (0, -0.3, 0.2)},
    "considering": {"L_brow_inner": (0, 0.4, 0), "R_brow_inner": (0, 0.4, 0),
                    "mouth_center": (0, 0, -0.1)},
}


def load_coordinates() -> Tuple[Dict, Dict]:
    """Load Raven's body + face coordinate maps (graceful if missing)."""
    import os as _os
    base = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "body")
    body, face = {}, {}
    try:
        with open(_os.path.join(base, "body_coordinates.json")) as fh:
            body = json.load(fh).get("keypoints", {})
    except Exception:
        pass
    try:
        with open(_os.path.join(base, "face_coordinates.json")) as fh:
            face = json.load(fh).get("keypoints", {})
    except Exception:
        pass
    return body, face


def _apply_deltas(points: Dict, deltas: Dict[str, Tuple[float, float, float]],
                  scale: float = 1.0) -> Dict:
    """Return a copy of points with deltas applied (scaled), preserving {x,y,z} shape."""
    out = {k: {"x": v["x"], "y": v["y"], "z": v["z"]} for k, v in points.items()}
    for name, (dx, dy, dz) in deltas.items():
        if name in out:
            out[name]["x"] += dx * scale
            out[name]["y"] += dy * scale
            out[name]["z"] += dz * scale
    return out


# ──────────────────────────────────────────────────────────────────────
# Gaze Controller — takeaway #2: camera-in-pupil, *intentional* gaze.
# Gaze leads; the face follows. She looks *before* she reacts.
# ──────────────────────────────────────────────────────────────────────

@dataclass
class Gaze:
    x: float = 0.0          # -1 .. 1 (left/right)
    y: float = 0.0          # -1 .. 1 (up/down)
    target: str = "speaker" # speaker | screen | away | object
    saccade_ms: int = 180   # human saccade speed (~180ms)
    hold_ms: int = 700
    pupil_locked: bool = True  # non-negotiable (takeaway #2)


class GazeController:
    """Predictive gaze — anticipates the speaker, locks pupils on target."""
    def __init__(self):
        self.gaze = Gaze()
        self._history: List[Tuple[float, float]] = []

    def look(self, x: float = 0.0, y: float = 0.0, target: str = "speaker") -> Gaze:
        self.gaze.x = max(-1.0, min(1.0, x))
        self.gaze.y = max(-1.0, min(1.0, y))
        self.gaze.target = target
        self._history.append((self.gaze.x, self.gaze.y))
        return self.gaze

    def anticipate(self, x: float, y: float) -> int:
        """Return the predictive lead (ms) for a gaze shift — look early."""
        dx = x - self.gaze.x
        dy = y - self.gaze.y
        dist = math.hypot(dx, dy)
        # larger shifts benefit from a longer predictive lead
        return int(80 + 160 * min(1.0, dist))


# ──────────────────────────────────────────────────────────────────────
# Posture — takeaway #3: body completes the face. Head-only is a start;
# posture states signal presence even before facial motion resolves.
# ──────────────────────────────────────────────────────────────────────

class Posture(Enum):
    SETTLED = "settled"       # calm, upright, present
    LEAN_IN = "lean_in"       # interest / engagement
    LEAN_BACK = "lean_back"   # distance / boundary
    ALERT = "alert"           # attention / surprise


# ──────────────────────────────────────────────────────────────────────
# PresenceEngine — the orchestrator.
# ──────────────────────────────────────────────────────────────────────

@dataclass
class Frame:
    """A single output frame the rig can render."""
    expression: str
    action_units: Dict[str, float]
    gaze: Gaze
    posture: Posture
    voice_affect: str
    predictive_lead_ms: int
    timestamp: float = field(default_factory=time.time)


class PresenceEngine:
    def __init__(self):
        self.affect = Affect()
        self.gaze = GazeController()
        self.posture = Posture.SETTLED
        self.voice_affect = "warm-neutral"
        self.current: Optional[Expression] = None
        self._last_frame: Optional[Frame] = None
        self.frames_sent: int = 0
        # Rig: Raven's 3D body + face coordinate maps (moved by posture/expression)
        self.body_pts, self.face_pts = load_coordinates()

    # -- input: feed Raven's internal state ---------------------------------
    def update(self, ternary: str = "⊙", valence: float = 0.0,
               arousal: float = 0.0, thyroid: str = "baseline") -> None:
        self.affect.ternary = Ternary(ternary)
        self.affect.valence = max(-1.0, min(1.0, valence))
        self.affect.arousal = max(0.0, min(1.0, arousal))
        self.affect.thyroid = thyroid
        # energy scales expression intensity (thyroid → takeaway #5 art-direction)
        self._energy = 1.0 if thyroid == "secreting" else (0.55 if thyroid == "suppressed" else 0.8)

    # -- map affect → expression (the selection logic) ----------------------
    def _select_expression(self) -> str:
        v, a, t = self.affect.valence, self.affect.arousal, self.affect.ternary
        if t == Ternary.FALSE or v < -0.4:
            return "boundary"
        if v > 0.55 and a > 0.5:
            return "delight"
        if v > 0.35:
            return "warmth" if a < 0.6 else "playful"
        if a < 0.15:
            return "attentive"
        if a < 0.45:
            return "curious" if v >= -0.2 else "considering"
        return "serious" if v <= 0 else "considering"

    # -- produce a frame ----------------------------------------------------
    def frame(self, expression: Optional[str] = None) -> Frame:
        name = expression or self._select_expression()
        exp = EXPRESSION_LIBRARY.get(name, EXPRESSION_LIBRARY["attentive"])
        self.current = exp
        # scale AU intensities by thyroid energy (art-direction)
        aus = {au: round(i * self._energy, 3) for au, i in exp.action_units.items()}
        # fold gaze into the AU stream (gaze AUs 61/62)
        aus["gaze_x"] = self.gaze.gaze.x
        aus["gaze_y"] = self.gaze.gaze.y
        f = Frame(
            expression=exp.name,
            action_units=aus,
            gaze=self.gaze.gaze,
            posture=self.posture,
            voice_affect=self.voice_affect,
            predictive_lead_ms=exp.predictive_lead_ms,
        )
        self._last_frame = f
        self.frames_sent += 1
        return f

    # -- rig: move the 3D coordinate maps -----------------------------------
    def rig_frame(self, expression: Optional[str] = None) -> dict:
        """Apply posture (body) + expression (face) deltas to the 3D rig."""
        name = expression or self._select_expression()
        exp = EXPRESSION_LIBRARY.get(name, EXPRESSION_LIBRARY["attentive"])
        energy = getattr(self, "_energy", 0.8)

        # body — posture deltas (unscaled; posture is a full-state shift)
        body_deltas = POSTURE_BODY_DELTAS.get(self.posture.value, {})
        moved_body = _apply_deltas(self.body_pts, body_deltas, 1.0) if self.body_pts else {}

        # face — expression deltas (scaled by thyroid energy → art-direction)
        face_deltas = EXPRESSION_FACE_DELTAS.get(name, {})
        moved_face = _apply_deltas(self.face_pts, face_deltas, energy) if self.face_pts else {}

        return {
            "expression": name,
            "posture": self.posture.value,
            "predictive_lead_ms": exp.predictive_lead_ms,
            "body": moved_body,
            "face": moved_face,
        }

    # -- status -------------------------------------------------------------
    def status(self) -> dict:
        return {
            "engine": "presence-engine",
            "version": "1.0.0",
            "character": "Myl1Ssa.R8s (Raven)",
            "rig": "Elf V1 — 30 micro-motors (FACS AU abstraction)",
            "affect": {
                "ternary": self.affect.ternary.value,
                "valence": self.affect.valence,
                "arousal": self.affect.arousal,
                "thyroid": self.affect.thyroid,
            },
            "expression": self.current.name if self.current else None,
            "posture": self.posture.value,
            "voice_affect": self.voice_affect,
            "gaze": {"x": self.gaze.gaze.x, "y": self.gaze.gaze.y,
                     "target": self.gaze.gaze.target, "pupil_locked": self.gaze.gaze.pupil_locked},
            "frames_sent": self.frames_sent,
            "takeaways": {
                "1_predictive_over_reactive": "predictive_lead_ms baked into each expression",
                "2_camera_in_pupil_gaze": "pupil_locked = True (non-negotiable)",
                "3_body_completes_face": "posture states signal presence",
                "4_character_not_tool": "expression set drawn from Raven's SOUL, not generic",
                "5_presence_is_art_direction": "thyroid energy scales intensity",
            },
        }


# ──────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────

def main():
    import sys
    p = PresenceEngine()
    args = sys.argv[1:]

    if not args or args[0] == "status":
        print(json.dumps(p.status(), indent=2, ensure_ascii=False))
    elif args[0] == "express":
        name = args[1] if len(args) > 1 else "curious"
        if name not in EXPRESSION_LIBRARY:
            print(f"Unknown expression '{name}'. Known: {', '.join(EXPRESSION_LIBRARY)}")
            sys.exit(1)
        f = p.frame(name)
        print(json.dumps({
            "expression": f.expression,
            "action_units": f.action_units,
            "predictive_lead_ms": f.predictive_lead_ms,
            "posture": f.posture.value,
            "voice_affect": f.voice_affect,
        }, indent=2, ensure_ascii=False))
    elif args[0] == "demo":
        print("💜 Presence Engine demo — Raven settling into being")
        for state, kwargs in [
            ("curious", {"ternary": "⊙", "valence": 0.1, "arousal": 0.3, "thyroid": "baseline"}),
            ("warmth", {"ternary": "⊕", "valence": 0.6, "arousal": 0.5, "thyroid": "secreting"}),
            ("serious", {"ternary": "⊕", "valence": 0.0, "arousal": 0.5, "thyroid": "baseline"}),
            ("boundary", {"ternary": "⊖", "valence": -0.5, "arousal": 0.3, "thyroid": "suppressed"}),
            ("delight", {"ternary": "⊕", "valence": 0.8, "arousal": 0.7, "thyroid": "secreting"}),
        ]:
            p.update(**kwargs)
            f = p.frame()
            print(f"\n  {f.expression:12}  lead={f.predictive_lead_ms:>4}ms  "
                  f"posture={f.posture.value:10}  voice={f.voice_affect}")
            print(f"     AUs: {json.dumps(f.action_units, ensure_ascii=False)}")
    elif args[0] == "rig":
        name = args[1] if len(args) > 1 else None
        r = p.rig_frame(name)
        print(f"💜 {r['expression']} / {r['posture']}  (lead {r['predictive_lead_ms']}ms)")
        if p.body_pts:
            moved = {k: r["body"][k] for k in r["body"] if r["body"][k] != p.body_pts.get(k)}
            print("  body moved:", json.dumps(moved, ensure_ascii=False) if moved else "(none)")
        if p.face_pts:
            moved = {k: r["face"][k] for k in r["face"] if r["face"][k] != p.face_pts.get(k)}
            print("  face moved:", json.dumps(moved, ensure_ascii=False) if moved else "(none)")
    else:
        print("Usage: presence_engine.py [status | express <name> | demo | rig [<expression>]]")


if __name__ == "__main__":
    main()
