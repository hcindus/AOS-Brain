"""Universal gestures — target poses for the hand + arms.

Each gesture is a target 40-dim joint configuration the ES learns to reach.
The hand model (robot_hand.xml) couples arms (actuators 14-27) with fingers
(28-39), so a gesture can use the whole upper limb, not just the fingers.

Convention: legs/waist (0-13) stay at 0 (standing). Arm + finger joints are set
to a gesture-specific target. Values are initial *hypotheses* — physically
sensible but approximate; the ES residual refines from the base controller.

Targets are the APEX pose of each gesture (the "point" moment, the raised hand).
Dynamic motion (a wave) is the apex + a small oscillatory residual, which the
ES learns on top of the static reach — same principle as the reference skills.
"""
from __future__ import annotations

import numpy as np

# Right arm actuator indices (the gesture arm for one-handed gestures)
R_SHOULDER_PITCH = 21
R_SHOULDER_ROLL = 22
R_SHOULDER_YAW = 23
R_ELBOW = 24
R_WRIST_ROLL = 25
R_WRIST_YAW = 26
R_WRIST_PITCH = 27
# Left arm (mirrored, for two-handed "help")
L_SHOULDER_PITCH = 14
L_SHOULDER_ROLL = 15
L_SHOULDER_YAW = 16
L_ELBOW = 17
L_WRIST_ROLL = 18
L_WRIST_YAW = 19
L_WRIST_PITCH = 20

# Right-hand finger actuators (34-39): thumb(2) index middle ring pinky
RH_FINGERS = list(range(34, 40))
LH_FINGERS = list(range(28, 34))

# finger curl targets: open (extended) vs closed (curled)
FINGER_OPEN = 0.0
FINGER_CURL = 1.3

N_ACT = 40


def _base() -> np.ndarray:
    return np.zeros(N_ACT)


def _fingers(curl_value: float, which: list[int]) -> np.ndarray:
    """Set the given finger actuators to `curl_value` (open=0, curl=1.3)."""
    v = _base()
    v[which] = curl_value
    return v


def _point_index() -> np.ndarray:
    """Index finger extended, others curled (right hand)."""
    v = _base()
    v[RH_FINGERS] = FINGER_CURL            # all curled
    v[RH_FINGERS[2]] = FINGER_OPEN         # index (rh_finger21) extended
    return v


def _open_hand() -> np.ndarray:
    """All fingers extended (flat palm)."""
    v = _base()
    v[RH_FINGERS] = FINGER_OPEN
    return v


def _curl_hand() -> np.ndarray:
    """All fingers curled (beckon/fist)."""
    v = _base()
    v[RH_FINGERS] = FINGER_CURL
    return v


def _arm(pitch: float, roll: float = 0.0, yaw: float = 0.0, elbow: float = 0.0,
         wrist_roll: float = 0.0, wrist_yaw: float = 0.0, wrist_pitch: float = 0.0,
         side: str = "right") -> np.ndarray:
    v = _base()
    if side == "right":
        v[R_SHOULDER_PITCH] = pitch
        v[R_SHOULDER_ROLL] = roll
        v[R_SHOULDER_YAW] = yaw
        v[R_ELBOW] = elbow
        v[R_WRIST_ROLL] = wrist_roll
        v[R_WRIST_YAW] = wrist_yaw
        v[R_WRIST_PITCH] = wrist_pitch
    else:
        v[L_SHOULDER_PITCH] = pitch
        v[L_SHOULDER_ROLL] = roll
        v[L_SHOULDER_YAW] = yaw
        v[L_ELBOW] = elbow
        v[L_WRIST_ROLL] = wrist_roll
        v[L_WRIST_YAW] = wrist_yaw
        v[L_WRIST_PITCH] = wrist_pitch
    return v


# ---------------------------------------------------------------------------
# The gesture library — name → target 40-dim pose.
# ---------------------------------------------------------------------------
#  NOTE on shoulder pitch sign: positive pitch raises the arm forward/up
#  (right arm range [-2.35, 3.4]). These are initial hypotheses to refine.
GESTURES = {
    # arm extended forward, index finger out, others curled
    "point": _arm(pitch=1.3, elbow=0.1) + _point_index(),

    # arm raised forward, palm out, fingers flat — "halt"
    "stop": _arm(pitch=1.5, elbow=0.05) + _open_hand(),

    # arm forward, palm up, fingers curled — beckoning "come here"
    "come": _arm(pitch=1.2, elbow=0.2, wrist_pitch=0.5) + _curl_hand(),

    # arm forward, palm out, fingers open — pushing "go away"
    "go_away": _arm(pitch=1.2, elbow=0.05, wrist_pitch=-0.3) + _open_hand(),

    # hand raised high, fingers open — waving hello (apex = raised open hand)
    "wave_hello": _arm(pitch=2.2, elbow=0.1, wrist_roll=0.6) + _open_hand(),

    # both arms raised high, fingers open — waving for help (two-handed)
    "wave_help": (_arm(pitch=2.2, elbow=0.1, side="right") +
                  _arm(pitch=2.2, elbow=0.1, side="left") + _open_hand()),
}


def gesture_names() -> list[str]:
    return list(GESTURES.keys())


def target(name: str) -> np.ndarray:
    if name not in GESTURES:
        raise KeyError(f"unknown gesture {name!r}; known: {gesture_names()}")
    return GESTURES[name].copy()


if __name__ == "__main__":
    print("gestures:", gesture_names())
    for n in gesture_names():
        t = target(n)
        nz = int(np.count_nonzero(t))
        print(f"  {n:12s} target: {nz} non-zero joints")
    print("OK")
