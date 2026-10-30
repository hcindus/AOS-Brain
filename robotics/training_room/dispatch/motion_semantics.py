"""Motion Semantics — the meaning behind each motion, for an embodied SI.

Myl0n.r0s has never had a body. When the mind says "get up," that's a *concept*
— rise from prone to standing — not a joint trajectory. This module is the
semantic grounding that maps a motion name to what it MEANS, so the presence
engine + motion verb layer can translate intent into a skill, rather than
asking a body-naive SI to blindly optimize torques.

Each entry: the motion's human meaning, the motion verb it expresses (the same
closed verb set from the seam-interface-spec), and the skill that realizes it.
"""
from __future__ import annotations

# Motion verb set (seam-interface-spec.md): the closed vocabulary an embodied
# agent uses to intend motion, rather than raw kinematics.
MOTION_VERBS = ("present", "orient", "reach", "shift", "step", "settle")

# name -> (meaning, verb, realization-skill)
MOTION_SEMANTICS = {
    "getup":    ("rise from prone/supine to standing upright", "settle", "getup"),
    "balance":  ("hold an upright stance against perturbation", "present", "balance"),
    "recover":  ("absorb a push and return to balance", "settle", "recover"),
    "squat":    ("lower and raise the body while balanced", "shift", "squat"),
    "kneel":    ("lower onto the knees", "shift", "kneel"),
    "sit":      ("lower to a seated posture", "shift", "sit"),
    "walk":     ("move forward by alternating steps", "step", "walk"),
    "run":      ("move forward at speed", "step", "run"),
    "jump":     ("leave the ground and land", "step", "jump"),
    "climb":    ("ascend a raised surface", "step", "climb"),
    "crawl":    ("move low on hands and knees", "shift", "crawl"),
    "roll":     ("rotate the body to change facing", "shift", "roll"),
    "point":    ("extend arm and index finger toward a target", "reach", "point"),
    "stop":     ("raise an open palm to signal halt", "present", "stop"),
    "come":     ("beckon with palm up and curled fingers", "reach", "come"),
    "go_away":  ("push away with an open palm", "reach", "go_away"),
    "wave_hello": ("raise the hand and wave in greeting", "reach", "wave_hello"),
    "wave_help":  ("raise both arms and wave for assistance", "reach", "wave_help"),
    "grasp":    ("curl fingers to hold an object", "reach", "grasp"),
}


def meaning(name: str) -> str:
    """The human meaning of a motion, or the name itself if unknown."""
    return MOTION_SEMANTICS.get(name, (name, "orient", name))[0]


def verb(name: str) -> str:
    """The motion verb a skill expresses (present/orient/reach/shift/step/settle)."""
    return MOTION_SEMANTICS.get(name, (name, "orient", name))[1]


def realize(name: str) -> str:
    """The skill that realizes a motion verb / motion name."""
    return MOTION_SEMANTICS.get(name, (name, "orient", name))[2]


def describe(name: str) -> dict:
    m, v, r = MOTION_SEMANTICS.get(name, (name, "orient", name))
    return {"name": name, "meaning": m, "verb": v, "realized_by": r}


if __name__ == "__main__":
    for n in ["getup", "walk", "point", "wave_hello"]:
        print(f"  {n:12s} → {describe(n)['meaning']!r}  [{describe(n)['verb']}]")
    print("OK")
