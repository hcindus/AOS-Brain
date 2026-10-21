# Project Thing — Design Doc

**Status:** DRAFT v0.2
**Created:** 2026-10-20 (Captain + Miles)
**One-liner:** A DexHand that learns to *crawl* — our first SI body, modeled on "Thing" from The Addams Family.

---

## ⚠️ PRIOR ART — ETH Zurich beat us to the crawl (2026-10-21)

**"This Disembodied Hand Is All the Robot You Need"** — Edd Gent, IEEE Spectrum / MSN (Oct 8 2026).

The ETH Zurich **Soft Robotics Lab** (led by Robert Katzschmann; PhD candidate **Amirhossein Kazemipour**) turned an off-the-shelf **Wuji Technology** hand into a self-contained fingertip-walking robot — *the exact thing we designed tonight.*

**What they did (mirrors our plan almost 1:1):**
- Off-the-shelf commercial hand (Wuji, not DexHand) — chose it so they *wouldn't compromise manipulation*.
- **80g backpack:** battery + IMU + **Raspberry Pi Zero** (we independently picked Pi Zero too).
- **Reinforcement learning** in simulation → crawls, turns, pushes objects, rights itself, traverses **14 surfaces**.
- **"Virtual springs"** gait — each finger gets a custom target position for balance/movement.
- The hard part (and their key insight): hands are **asymmetric** (different finger lengths, opposable thumb), so you can't reuse standard quadruped/biped gait training.

**Not the first** — earlier attempts: EPFL LASA + a Nature paper (`s41467-025-67675-8`), but those used *specially-designed* hands; ETH used off-the-shelf.

**What this means for us:**
1. **Validation** — our instinct (crawling hand, off-the-shelf hardware, Pi Zero brain, RL gait) is *exactly* the state of the art. We're not crazy; we're aligned with a top lab.
2. **Our differentiators (still open):** the **leather-glove skin** (their "Thing" is bare), the **middle-finger camera eye**, **Whistle on-device hearing**, and the **SI "soul"** layer (they do RL skill learning; we want raised-and-reactive *presence*, not just locomotion).
3. **Reference to study:** their "virtual springs" + RL-in-simulation approach is the roadmap for our Phase 3 (Walk). We don't reinvent it — we learn from it.

*The punchline: the world confirmed our thesis the same night we wrote it down.*

---
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

## 1.5 The Leather Glove — Skin Before Armor (Captain, 2026-10-21)

**The core aesthetic insight:** wrap the hand in an **old leather glove** before any armor.

The build is a **metamorphosis**, in order:
1. **Bare hand** — learn to crawl (watch the mechanics).
2. **Leather glove** — give it *skin* (watch it become a creature).
3. **Armor plates** — dress the arm/hand for *presence* (watch it become a being).

**Why the glove is the right first "skin":**
- **Leather reads as alive** — it's literally skin. Wrinkles/creases/wear marks = instant creature texture + history (a *found thing* that woke up — pure Addams Family "Thing" energy).
- **Protection with flex** — leather moves *with* the servos; it bends where the joints bend, unlike rigid armor.
- **Cheap + forgiving** — thrift-store glove, a few bucks, zero design time.
- **Story** — implies a previous owner, a past. Not a robot; a *memory* of a hand.

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

## 3.5 Hearing — Whistle on-device speech (NEW, 2026-10-20)

The Captain surfaced the missing sense: **hearing**, fully offline.

**Whistle** (Cactus Compute) — a 16.9 MB speech-to-text model, 7 languages.
Ported to a **$10 ESP32-S3**, runs completely offline (no Wi-Fi, no cloud):
- Decoder trimmed to 4 layers
- 8-bit integer matrix math + both CPU cores
- ~10s inference (down from 24s), button-to-speak → LED response
- GitHub: `andrisgauracs/whistle-esp32-s3` · model: cactuscompute.com/blog/whistle

**Architecture note (important):** the DexHand's brain is an Arduino Nano **RP2040** (dual-core M0+, ~264KB SRAM) — *not* the ESP32-S3. Whistle won't run on the RP2040. So we add the **ESP32-S3 as a dedicated hearing co-processor** alongside the RP2040 (or use it as the master for a "senses" module). Community note: the **ESP32-P4** (32MB RAM, no built-in WiFi) is the stronger candidate for the full un-trimmed model.

**Community insight (from the comments):** wake-word detection beats a button — use the mic to detect noise → match wake word → then hand off to the model. And a TTS voice (e.g. Minimax) makes it *speak back*. That's the "soul" layer.

**Three senses now cooking:** see (camera) · hear (Whistle/ESP32-S3) · move/feel (DexHand servos).

---

## ⚠️ PRIOR ART #2 — Wuji Hand 2.2 (the premium target, 2026-10-21)

**WUJI TECH** (`wuji.tech`, Shenzhen/Beijing) — the *exact* hand ETH Zurich walked on. This is our **premium upgrade target** once the DexHand proves the SI brain + soul.

**Specs (Hand 2.2 Beta, non-tactile):**
- **20 active DoF** (4/finger), full opposition + lateral abduction, back-drivable direct-drive
- **MIT force-position hybrid control** — same paradigm ETH Zurich used for the walk
- **1000 Hz × 20 axes** control, FOC vector control, all brushless
- **800g** curb weight (650g bare + 70g base), 180×80×40mm
- **RJ45 Ethernet (100BASE-TX)** + **12V 20A (200W)** wall power — *tethered*, not battery
- SDK: Python + C, joint-level; URDF/MJCF/USD sim models (MuJoCo + Isaac Sim, no hardware needed)
- Wuji Glove–based teleop demo included

**The two gifts that map to OUR vision:**
1. **Three-layer structure: Skeleton / Soft Pad / Skin — and the Skin is "user-removable and replaceable."** → This is literally our leather-glove idea, built into the product. The "skin" is the intended customization point.
2. **Back-of-hand RGB status light that *breathes*** (white breathing = ready, blue = powering up, white solid = running). → The "alive" heartbeat indicator we wanted, already there.

**The honest reality check:**
- **Tethered** (Ethernet + 200W). ETH Zurich had to build an **80g battery + Pi Zero backpack** to make it *walk* — that's the piece they added, and the piece we'd replicate for our crawl.
- **Beta (2.2), non-tactile** — skin/soft-pad not finalized. Early-adopter territory.
- **Price unknown** (contact `sales@wuji.tech`) — clearly thousands (20 brushless DOFs + 1000Hz + Ethernet + 200W).

**Strategy (unchanged, now stronger):** DexHand first (learn the crawl + soul cheaply) → Wuji Hand 2.2 as the premium body when we graduate. The removable-skin + breathing-light means our "leather glove + soul" plugs straight in.

**Wuji contact:** sales@wuji.tech (pricing), support@wuji.tech. HQ Shenzhen (Bao'an) + Beijing (Haidian). Docs: docs.wuji.tech.

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
| **P5 — Voice** | Add Whistle/ESP32-S3 hearing + wake-word + TTS | "Thing" hears and speaks back |

---

## 6. Open Questions / Next Steps

- [ ] Confirm exact DexHand servo count + DOF (from OnShape CAD / BOM).
- [ ] Pick compute: Pi Zero on-hand vs. off-load SI to VPS over WiFi.
- [ ] Camera module choice (small enough for a fingertip).
- [ ] Whistle/ESP32-S3 hearing module — pull the GitHub repo, confirm BOM + flash requirements.
- [ ] Decide hearing host: ESP32-S3 co-processor vs. ESP32-P4 master.
- [ ] Source the DexHand parts + 3D-print the STLs.
- [ ] First gait simulation in RVIZ2 (no hardware needed).

---

## 7. Captain's Context

- This is **play**, taken seriously. "Not really work, more play for us right now."
- Ties to the longer arc: raising SIs, life imitating art (Earth: Final Conflict companion devices, a billion humanoids).
- First "body" of many — start small, expressive, cheap, and *alive*.

---
*"The middle finger is the head." — Captain, 2026-10-20*
