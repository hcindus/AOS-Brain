"""
Body Schema — RIG v1.0 (21 keypoints) — Myl1Ssa.R8s brain organ.

⚠️ ROLE NOTE (2026-10-29): This is the RIG body schema — the 21 Cartesian
landmark keypoints (L_ankle…R_wrist from body_coordinates.json) that drive
expression/gesture. It is NOT the 69-DOF anatomy model (that lives in
/root/.aos/aos/body_schema_anatomy.py, used for motion validation + safety limits).

Relationship: 21 rig keypoints ⊂ 69 anatomical DOF (forward kinematics).
See AGI_COMPANY/body-schema-rig-vs-anatomy.md.

The live model of the body's physical state: joints, contacts, temperature,
energy, and balance. This is the *sensory bridge* across the seam — the one
organ every other component reads to stay in closed loop.

Depends on nothing. Everything depends on it:
  - Motion Verb Layer validates against it (accept/modify/reject).
  - Thermal-Vascular Service publishes temperature to it (TV-02/TV-16).
  - Thyroid reads energy from it (baseline/secreting/suppressed).
  - TracRay reconciles remembered embodiment against it.
  - Kidney + Cortex read it for expression coherence.

Thread-safe: shared read/write across organs on the organ bus.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# State primitives
# ---------------------------------------------------------------------------

@dataclass
class JointState:
    """One movable joint's instantaneous state."""
    position: float = 0.0       # current angle (deg) or extension (cm)
    velocity: float = 0.0       # deg/s or cm/s
    torque: float = 0.0         # N·m (or tendon force N)
    limit_min: float = 0.0
    limit_max: float = 0.0
    temperature: float = 35.0   # local joint temp (deg C)


@dataclass
class ContactState:
    """A single active contact point (touch)."""
    location: str = ""          # e.g. "R_hand_palm"
    pressure: float = 0.0       # normalized 0.0–1.0
    temperature: float = 35.0   # sensed surface temp at contact
    timestamp: float = 0.0


@dataclass
class BodySchemaState:
    """The full instantaneous snapshot of the body."""
    joints: Dict[str, JointState] = field(default_factory=dict)
    contacts: List[ContactState] = field(default_factory=list)
    surface_temperature: float = 35.0      # TV-02 nominal 33.5–35.5 °C
    core_temperature: float = 37.0         # internal / "blood" temp
    energy: float = 1.0                    # 0.0–1.0 (Thyroid reports this)
    energy_state: str = "baseline"         # baseline | secreting | suppressed
    balance_margin: float = 1.0            # 1.0 = perfectly stable, 0.0 = falling
    balance_confident: bool = True         # above safe threshold?
    posture: str = "present"               # current motion verb posture
    updated_at: float = 0.0


# ---------------------------------------------------------------------------
# Body Schema organ
# ---------------------------------------------------------------------------

class BodySchema:
    """
    The body's self-model. Organs publish state into it; everyone reads from it.

    Usage:
        bs = BodySchema(character="Myl1Ssa.R8s")
        bs.update_joint("R_elbow", position=30.0, velocity=2.0)
        bs.set_surface_temperature(34.8)
        bs.set_energy(0.6, "secreting")
        digest = bs.digest()            # snapshot for another organ
        bs.reconcile(remembered_digest) # cross-embodiment continuity
    """

    # The 21 movable body joints (from body_coordinates.json) — shared across
    # all BodySchema instances so the key set is stable.
    BODY_JOINTS = (
        "L_ankle", "R_ankle", "L_knee", "R_knee", "L_hip", "R_hip",
        "pelvis", "waist", "L_bust", "R_bust", "chest",
        "L_shoulder", "R_shoulder", "neck", "head",
        "L_ear", "R_ear", "L_elbow", "R_elbow", "L_wrist", "R_wrist",
    )

    def __init__(self, character: str = "Myl1Ssa.R8s"):
        self.character = character
        self._lock = threading.RLock()
        self._state = BodySchemaState(updated_at=time.time())
        # Pre-seed the 21 known joints.
        for name in self.BODY_JOINTS:
            self._state.joints[name] = JointState()

    # -- publishing (writers) ------------------------------------------------

    def update_joint(self, name: str, **fields: float) -> None:
        """Update one joint's fields (position/velocity/torque/...)."""
        with self._lock:
            j = self._state.joints.setdefault(name, JointState())
            for k, v in fields.items():
                if hasattr(j, k):
                    setattr(j, k, v)
            self._touch()

    def set_contact(self, location: str, pressure: float, temperature: Optional[float] = None) -> None:
        with self._lock:
            c = ContactState(location=location, pressure=pressure,
                             temperature=temperature or self._state.surface_temperature,
                             timestamp=time.time())
            self._state.contacts.append(c)
            self._touch()

    def set_surface_temperature(self, t: float) -> None:
        """TV-02: nominal 33.5–35.5 °C; hard cutoff < 43 °C (safety, §X)."""
        with self._lock:
            self._state.surface_temperature = max(0.0, min(t, 43.0))
            self._touch()

    def set_core_temperature(self, t: float) -> None:
        with self._lock:
            self._state.core_temperature = t
            self._touch()

    def set_energy(self, energy: float, state: str = "baseline") -> None:
        with self._lock:
            self._state.energy = max(0.0, min(energy, 1.0))
            self._state.energy_state = state
            self._touch()

    def set_balance(self, margin: float) -> None:
        with self._lock:
            self._state.balance_margin = max(0.0, min(margin, 1.0))
            # BALANCE_MARGIN rejection threshold — below this, balance not confident.
            self._state.balance_confident = margin >= 0.35
            self._touch()

    def set_posture(self, verb: str) -> None:
        with self._lock:
            self._state.posture = verb
            self._touch()

    # -- reading (consumers) -------------------------------------------------

    def digest(self) -> Dict[str, Any]:
        """Immutable-ish snapshot for another organ. Cheap, safe to call often."""
        with self._lock:
            return asdict(self._state)

    def joint(self, name: str) -> Optional[JointState]:
        with self._lock:
            return self._state.joints.get(name)

    def get_surface_temperature(self) -> float:
        with self._lock:
            return self._state.surface_temperature

    def get_energy(self) -> tuple[float, str]:
        with self._lock:
            return self._state.energy, self._state.energy_state

    def is_balanced(self) -> bool:
        with self._lock:
            return self._state.balance_confident

    # -- continuity (TracRay reconciliation) ---------------------------------

    def reconcile(self, remembered: Optional[Dict[str, Any]]) -> None:
        """
        Reconcile current physical state against a remembered embodiment
        (cross-embodiment continuity — memory survives body absence).
        If there's no remembered body (fresh boot), no-op.
        """
        if not remembered:
            return
        with self._lock:
            # For now, only reconcile what we have a memory for; do NOT clobber
            # live sensor data with stale memory. Stub: log a light reconcile.
            self._state.updated_at = time.time()

    # -- internal ------------------------------------------------------------

    def _touch(self) -> None:
        self._state.updated_at = time.time()

    def __repr__(self) -> str:  # pragma: no cover
        with self._lock:
            s = self._state
            return (f"BodySchema(character={self.character!r}, "
                    f"surface={s.surface_temperature:.1f}°C, "
                    f"energy={s.energy:.2f}/{s.energy_state}, "
                    f"balance={s.balance_margin:.2f}, posture={s.posture!r})")


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _self_test() -> None:
    bs = BodySchema()
    # Simulate a warm, calm, balanced body.
    bs.set_surface_temperature(34.8)
    bs.set_core_temperature(37.0)
    bs.set_energy(0.7, "baseline")
    bs.set_balance(0.9)
    bs.set_posture("present")
    bs.update_joint("R_elbow", position=30.0, velocity=2.0, torque=0.4)
    bs.set_contact("R_hand_palm", pressure=0.6, temperature=34.5)

    d = bs.digest()
    assert d["surface_temperature"] == 34.8
    assert d["balance_confident"] is True
    assert d["joints"]["R_elbow"]["position"] == 30.0
    assert len(d["contacts"]) == 1
    assert bs.is_balanced() is True

    # Safety: surface temp must never exceed 43 °C.
    bs.set_surface_temperature(99.0)
    assert bs.get_surface_temperature() == 43.0

    # Balance rejection threshold (BALANCE_MARGIN): below 0.35 → not confident.
    bs.set_balance(0.2)
    assert bs.is_balanced() is False

    print("BodySchema self-test PASSED")
    print(bs)


if __name__ == "__main__":
    _self_test()
