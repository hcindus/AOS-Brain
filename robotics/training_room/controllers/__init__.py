"""Locomotion controllers — the missing brain that turns intent into torques.

Unlike `Pilot` (which sees only a compact observation vector), a controller is
model-based: it reads full MuJoCo state (CoM, contacts, torso orientation) and
maps a high-level intent ("stand", "walk") to 28 joint torques. This is the
"motion verb" the HAL's AdapterFrame is missing.
"""
