"""Myl0nPilot — Myl0n.r0s embodied in the RP1 Training Room.

Myl0n.r0s (Mylzeron.Rzeros) is the Captain's Executive Orchestrator. Until now
he has been software-only: a brain (Brain v4.1 client), ternary organs (heart/
stomach/intestines via BHSI), and executive skills — but no BODY, no HEAD, and
no way to move in the world.

This pilot gives him all three, so he can train in the RP1 gym like every other
student before (if ever) touching a real robot:

  - BODY   — the RP1 28-DoF humanoid (via the gym env).
  - HEAD   — a presence engine that maps his internal affect (valence/arousal/
             energy) to a posture + expression vector. His "face" is the posture;
             the presence engine is the same discipline Raven's uses.
  - CONTROL — a base PD hold (keeps him standing) + an affect-modulated overlay,
             plus an optional Ollama reasoning layer for higher-level intent.

The architecture mirrors the seam we built for Raven:
    affect (valence/arousal/energy) → presence (posture + expression)
    → control (base + residual) → 28 torques → MuJoCo.

He is a *pilot* (roster entry), so he can be eval'd and graduated through the
same blind hold-out gate every other pilot faces.
"""
from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np

from .base import Pilot

OLLAMA_URL = "http://localhost:11434/api/generate"


# ---------------------------------------------------------------------------
# Presence Engine (the HEAD) — a compact affect → posture/expression model.
# Mirrors Raven's discipline: affect drives expression; identity locked,
# expression free. Myl0n's posture set is small + executive.
# ---------------------------------------------------------------------------

@dataclass
class Myl0nAffect:
    valence: float = 0.0     # -1..1  (negative ↔ positive)
    arousal: float = 0.0     #  0..1  (calm ↔ energized)
    energy: float = 0.8      #  0..1  (thyroid → expression intensity)


class Myl0nPresenceEngine:
    """Myl0n's head — maps affect to a posture + an expression vector.

    The posture is what actually changes his body in sim (lean_in / alert /
    settled / lean_back); the expression vector is a small FACS-like signal
    surfaced for diagnostics/telemetry, kept here so a real face could later
    consume the same affect.
    """

    POSTURES = ("settled", "lean_in", "lean_back", "alert")

    def __init__(self):
        self.affect = Myl0nAffect()
        self.posture = "settled"
        self.expression: Dict[str, float] = {}

    def update(self, valence: float = 0.0, arousal: float = 0.0, energy: float = 0.8):
        self.affect.valence = max(-1.0, min(1.0, valence))
        self.affect.arousal = max(0.0, min(1.0, arousal))
        self.affect.energy = max(0.0, min(1.0, energy))
        self._select_posture()
        self._select_expression()

    def _select_posture(self):
        v, a = self.affect.valence, self.affect.arousal
        if a > 0.6 and v >= 0.0:
            self.posture = "alert"
        elif v > 0.3:
            self.posture = "lean_in"
        elif v < -0.3:
            self.posture = "lean_back"
        else:
            self.posture = "settled"

    def _select_expression(self):
        # small FACS-like signal, scaled by energy (art-direction)
        e = self.affect.energy
        self.expression = {
            "brow": round(self.affect.valence * 0.5 * e, 3),
            "gaze": round(self.affect.arousal * 0.4 * e, 3),
            "jaw": round(self.affect.arousal * 0.3 * e, 3),
        }

    def posture_delta(self) -> np.ndarray:
        """A small qpos delta the posture applies to the base pose (28 joints).

        We bias a few upper-body joints so the posture reads in the sim: lean
        forward/back at the waist + a slight shoulder shift for alert/lean.
        Joint index → radians, kept tiny so the base PD hold still dominates.
        """
        d = np.zeros(28)
        # waist_roll (12), and a couple of shoulder/arm joints (indices are
        # approximate — the effect is a subtle torso lean, not a precise pose).
        if self.posture == "lean_in":
            d[12] = 0.15
        elif self.posture == "lean_back":
            d[12] = -0.15
        elif self.posture == "alert":
            d[12] = 0.08
            d[2] = 0.10   # slight arm raise
            d[8] = 0.10
        return d


# ---------------------------------------------------------------------------
# The pilot — body + head + control.
# ---------------------------------------------------------------------------

class Myl0nPilot(Pilot):
    name = "myl0n"

    def __init__(
        self,
        n_act: int = 28,
        kp: float = 60.0,
        kd: float = 4.0,
        model: str = "antoniohudnall/Mort_II:latest",
        use_ollama: bool = True,
        temperature: float = 0.3,
        timeout: float = 60.0,
        scale: float = 20.0,
    ):
        self.n_act = n_act
        self.kp = kp
        self.kd = kd
        self.model = model
        self.use_ollama = use_ollama
        self.temperature = temperature
        self.timeout = timeout
        self.scale = scale

        # the HEAD
        self.presence = Myl0nPresenceEngine()

        # the BODY (bound later via attach)
        self.env = None

        # obs layout: [height, quat(4), vel(3), angvel(3), qpos(28), qvel(28)]
        self._q_offset = 1 + 4 + 3 + 3

        self._history: list[str] = []

    # -- body binding -------------------------------------------------------
    def attach(self, env) -> None:
        self.env = env

    def reset(self) -> None:
        self._history = []
        # a calm, present default on each episode
        self.presence.update(valence=0.1, arousal=0.2, energy=0.8)

    def on_episode_end(self, info: dict) -> None:
        pass

    # -- affect input (the mind can steer him) ------------------------------
    def set_affect(self, valence: float, arousal: float, energy: float = 0.8):
        self.presence.update(valence, arousal, energy)

    # -- control ------------------------------------------------------------
    def act(self, obs: np.ndarray) -> np.ndarray:
        # base PD hold toward nominal + posture bias
        qpos = obs[self._q_offset : self._q_offset + self.n_act]
        qvel = obs[self._q_offset + self.n_act : self._q_offset + 2 * self.n_act]
        target = self.presence.posture_delta()
        base = -self.kp * (qpos - target) - self.kd * qvel

        if self.use_ollama:
            overlay = self._ollama_overlay(obs)
            tau = base + overlay
        else:
            tau = base

        return np.clip(tau, -30.0, 30.0)

    def _ollama_overlay(self, obs: np.ndarray) -> np.ndarray:
        """Ask Myl0n's model for a small torque overlay on top of the PD hold.

        Deliberately kept as an *overlay*, not the whole action — a raw LM is a
        weak torque controller, but as a high-level "which way to lean / reach"
        hint it's useful. Falls back to zeros on any error.
        """
        height = float(obs[0])
        qpos = obs[self._q_offset : self._q_offset + self.n_act]
        digest = (
            f"height={height:.3f} "
            f"mean_qpos={float(np.mean(qpos)):.3f} "
            f"posture={self.presence.posture} "
            f"valence={self.presence.affect.valence:.2f} "
            f"arousal={self.presence.affect.arousal:.2f}"
        )
        prompt = (
            "You are Myl0n.r0s, an executive orchestrator embodied in a 28-DoF "
            "humanoid. Respond ONLY with a JSON list of 28 numbers in [-1,1] "
            "representing small torque adjustments that keep the body upright "
            "and engaged. No explanation."
        )
        try:
            payload = json.dumps({
                "model": self.model,
                "prompt": f"{prompt}\nObservation: {digest}\nResponse (JSON list of 28):",
                "stream": False,
                "temperature": self.temperature,
            }).encode()
            req = urllib.request.Request(
                OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                reply = json.loads(r.read().decode())["response"]
            self._history.append(reply)
            self._history = self._history[-3:]
            import re
            m = re.search(r"\[[-\d.,\s]+\]", reply)
            if not m:
                return np.zeros(self.n_act)
            vals = [float(v) for v in json.loads(m.group(0))][: self.n_act]
            vals += [0.0] * (self.n_act - len(vals))
            return np.clip(np.asarray(vals) * self.scale, -self.scale, self.scale) * 0.3
        except Exception:
            return np.zeros(self.n_act)

    # -- introspection (surfaced to the tile) -------------------------------
    def status(self) -> dict:
        return {
            "name": "Myl0n.r0s (Mylzeron.Rzeros)",
            "posture": self.presence.posture,
            "affect": {
                "valence": self.presence.affect.valence,
                "arousal": self.presence.affect.arousal,
                "energy": self.presence.affect.energy,
            },
            "expression": self.presence.expression,
            "model": self.model if self.use_ollama else "pd-only",
        }
