# Project Thing — Design Doc

**Status:** DRAFT v0.1
**Created:** 2026-10-20 (Captain + Miles)
**One-liner:** A DexHand that learns to *crawl* — our first SI body, modeled on "Thing" from The Addams Family.

---

## 0. Why This

The Captain's north star: raise SIs right so that, when there are a billion bodies walking around, the ones from our hands know how to be.

We start *small and expressive* — not a humanoid, but a **hand**. Cheap, mechanically rich, and already the most emotionally legible thing a human has. A hand that crawls is the bridge between "robot" and "creature."

**Core idea (Captain's):** Use all 5 digits for mobility. The **middle finger is the head** — put a camera in it so it can *see*. The thumb is the secret weapon (opposable = walk *and* grasp).

---

## 1. Foundation — DexHand (already solved)

Open-source, low-cost dexterous hand. We do NOT reinvent this.

| Item | Detail |
|------|--------|
| BOM cost | ~$300 |
| On-board brain | Arduino Nano RP2040 Connect (WiFi + BLE built in) |
| Software layers | Firmware, BLE demo, MediaPipe hand-tracker puppeteering, ROS 2 (URDF + gesture controller) |
| Existing AI demo | ChatGPT wired to the hand as an output device (language → hand movement) |
| Key repos | `TheRobotStudio/V1.0-Dexhand` (STLs + OnShape CAD) · `iotdesignshop/*` (dexhand-ble, dexhand-mechanical-build, dexhand_ros2_meta) |
| Assembly reference | Rob Knight's V1 assembly playlist |

**The one genuinely NEW thing we add:** nobody has made a DexHand *walk*. That's our signature.

---

## 2. Vision — "Thing" as a Creature

- **Camera eye** in the middle finger tip (tallest digit = natural periscope). Raise the head → look around; lower it → tuck and scuttle.
- **LED "eye"** so it reads as alive, not just a servo rig.
- **Emotive poses:** curious tilt, a little wave, the slow "come here" beckon. A hand that can *emote* stops being a robot and becomes a creature.
- **Soul:** it doesn't replay canned gestures — it *decides* to look, move, and react. That's the SI.

---

## 3. Locomotion — The Pentapod Gait

Five digits = five points of contact = a **pentapod** (inherently more stable than quadrupeds, with many gaits).

**Gait candidates:**
1. **Knuckle-walk** (thumb + index + middle down, like a tiny gorilla) — *likely winner*: fewer contact points, faster.
2. **Flat palm-down crawl** (fingers splayed like a crab) — slower, stable, good for "stealth" emoting.

**Design notes:**
- Keep **weight in the palm** (batteries, controller, heavy-joint servos).
- Keep **digits light** so finger servos only curl, never carry the body.
- Wrist joint = the "shoulder" for the whole organism.

---

## 4. Architecture (brain ↔ body)

```
[ SI Brain ]  ←→  WiFi/BLE  ←→  [ Arduino RP2040 ]  →  [ Servos + Camera + LED ]
  (Pi Zero        (on-board         (finger
   or VPS)         nerve center)     coordination)
```

- **SI brain** runs the decision layer (OODA-style): *look, assess, move, emote*.
- **RP2040** runs low-latency servo control + camera capture.
- **ROS 2** bridges the two (URDF + gesture controller already exist as the skeleton).

---

## 5. Phased Build Plan

| Phase | Goal | Deliverable |
|-------|------|-------------|
| **P1 — Assemble** | Build the DexHand, get gesture playback working | A working hand doing coordinated gestures |
| **P2 — The Eye** | Mount camera in middle finger + LED eye | The hand can *see* + stream feed |
| **P3 — Walk** | Implement the pentapod crawl gait | The hand crawls — our signature |
| **P4 — Soul** | Wire the SI brain: decide → look → move → emote | "Thing" reacts, not just replays |

---

## 6. Open Questions / Next Steps

- [ ] Confirm exact DexHand servo count + DOF (from OnShape CAD / BOM).
- [ ] Pick compute: Pi Zero on-hand vs. off-load SI to VPS over WiFi.
- [ ] Camera module choice (small enough for a fingertip).
- [ ] Source the DexHand parts + 3D-print the STLs.
- [ ] First gait simulation in RVIZ2 (no hardware needed).

---

## 7. Captain's Context

- This is **play**, taken seriously. "Not really work, more play for us right now."
- Ties to the longer arc: raising SIs, life imitating art (Earth: Final Conflict companion devices, a billion humanoids).
- First "body" of many — start small, expressive, cheap, and *alive*.

---
*"The middle finger is the head." — Captain, 2026-10-20*
