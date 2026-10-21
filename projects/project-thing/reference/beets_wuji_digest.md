# Project Thing — Wuji Hardware Reference Digest

**Compiled by:** Beets
**Date:** 2026-10-21
**Sources:** `reference/wuji_raw_dump.md` (raw capture by Miles, 2026-10-21), `DESIGN.md` (DRAFT v0.2, 2026-10-20)
**Upstream docs:** docs.wuji.tech (wuji-hand, wuji-glove, release-notes), wuji.tech

---

## 0. One-Page Summary

Project Thing is a DexHand that learns to crawl — modeled on "Thing" from The Addams Family. The cheap path is the open-source DexHand (~$300, RP2040 brain). The **premium graduation target** is the **Wuji Hand 2.2 Beta**, which is the exact hand ETH Zurich's Soft Robotics Lab used to build a fingertip-walking robot. Wuji's design already contains two of our signature ideas as product features: a **user-removable skin layer** (our leather glove) and a **breathing RGB status light** (our "alive" heartbeat). The Wuji Hand is tethered (Ethernet + 200 W), so walking still requires the 80 g backpack ETH built — our Phase 3 problem either way.

---

## 1. Wuji Hand 2.2 — Specs

**Model:** Wuji Hand 2, version **2.2 Beta**, **non-tactile** prototype.

### Mechanical

| Spec | Value |
|---|---|
| Active DoF | **20** (4 per finger) |
| Articulation | Full thumb opposition + lateral abduction |
| Joint type | Back-drivable direct-drive rotary joints |
| Min grasp diameter | **0 mm** |
| Finger lengths | Index/middle/ring ~**137 mm**, little ~**134 mm**, thumb ~**140 mm** |
| Dimensions | **180 × 80 × 40 mm** |
| Weight | **800 g** curb — **650 g** bare hand + **70 g** base (separate) |
| Durability | **300 K** cycle lifespan, **80 cm** drop test, impact-resistant (twist-lock + slot locking) |

### Control & Electronics

| Spec | Value |
|---|---|
| Motor control | **FOC** vector control, all brushless |
| Control paradigm | **MIT force-position hybrid**, user-tunable parameters |
| Control rate | **1000 Hz × 20 axes** |
| Communication | **RJ45 Ethernet, 100BASE-TX** |
| Power | **11–13 V DC** (12 V nominal); **12 V 20 A** adapter (≥200 W); XT30 + RJ45 |

**Implication:** the hand is **tethered** — wall power, wired Ethernet. There is no on-board battery. Any untethered locomotion requires an added power/compute pack (see §5, ETH Zurich).

### Three-Layer Construction

1. **Skeleton** — load-bearing structure.
2. **Soft pad** — compliance layer at contact points.
3. **Skin** — protection only, **no sensing**.

> ⚠️ **The skin is user-removable and replaceable — and the hand must NEVER be run without the skin fitted.**

This is the single most important line in the document for Project Thing: **the skin is the manufacturer-intended customization point.** Our leather-glove concept is not a mod; it is the designed affordance.

### Status Light (back of hand)

RGB indicator with distinct alive/idle semantics:

| State | Meaning |
|---|---|
| White, **breathing** | Ready (idle) |
| Blue | Powering up |
| White, solid | Running |
| Yellow / red | Warning / fault |

The breathing idle state is exactly the "heartbeat" tell we wanted for creature legibility.

### Software & Tooling

- **SDK:** Python + C, **joint-level** API — device discovery, state read, command output.
- **Sim models:** URDF, MJCF, USD — supports **MuJoCo** and **Isaac Sim**, including a **fingertip soft-pad model**. Enables gait development with **no hardware**.
- **Teleop:** Wuji Glove–based teleoperation demo included (cross-product).

### Beta Caveats

- Fingertip **soft-pad hardness still being tuned**.
- **Skin design not finalized** at 2.2 Beta.
- **Non-tactile** — no contact sensing in this revision.
- **Price not published** (contact `sales@wuji.tech`). Realistically thousands: 20 brushless DOFs, 1000 Hz control, Ethernet, 200 W.

---

## 2. Wuji Glove — Specs

**Type:** Intelligent data glove for robotic teleoperation and human-computer interaction.

| Spec | Value |
|---|---|
| Touch points | **526** |
| Capture rate | **120 FPS** real-time, tactile + pose |
| Sensing | Tactile array + **IMU** hand tracking |
| Recording | **MCAP** format |
| Offline pipeline | Recompute hand products + IMU fusion |
| Calibration | Hand-model calibration + tactile contact calibration |
| SDK | Data subscription, merge, rate-limit; **Python + C** |
| Firmware | **v0.12.0** (teleop glove) |

**Relevance to Thing:** the Glove is a teleoperation and **data-collection** instrument. Two uses:
1. **Bootstrap training data** — teleoperate the Wuji Hand to record demonstrations before RL takes over.
2. **Reference target for our own skin** — 526 points at 120 FPS is the benchmark for what "sensing skin" means if we ever want the leather glove to *feel* rather than merely protect.

Note the discrepancy worth tracking: the raw dump lists Glove firmware **v0.12.0**, while the release notes cite Glove firmware **v1.0.3**. Likely different channels (teleop glove build vs. released firmware). Verify before relying on either.

---

## 3. Release Notes — Key Facts (Oct 2026)

| Date / Item | Fact |
|---|---|
| 2026-10-12 | **Wuji Description** packages released for **Hand 2.1 + 2.2** ROS 2: `wuji_hand2_1_description`, `wuji_hand2_2_description` |
| Platform support | SDK/CLI on **Ubuntu 20.04+**, **x86_64 + arm64**, **Python 3.8+** |
| Firmware | Hand 2: **v2.12.0** · Glove: **v1.0.3** |
| SDK | **v2026.10.12** — `pip install wuji-sdk` |
| **Port change** | Default SDK port **50001** (was 7447) since **firmware v2.7.0 / Sept 2026** |
| **Feed-forward compensation** | **Enabled by default** on units shipped **Oct 2026+** (firmware **v2.10.0**) |
| MIT impedance defaults | **kp = 5.0**, **kd = 0.1** |

**Practical notes:**
- Old tutorials and code samples referencing port **7447** are stale. Use **50001**.
- The ROS 2 description packages mean URDF-driven visualization (RVIZ2) is available off the shelf — this directly serves our "first gait simulation, no hardware" open question.
- kp/kd defaults are a *starting* point, not a tuning. MIT impedance gains are per-application; crawling will need its own values.
- Feed-forward compensation default-on is a behavior change: older firmware units will feel different from Oct 2026+ units for the same command stream.

---

## 4. Mapping Wuji Hardware → Project Thing Phases

Project Thing's five phases (from DESIGN.md §5) are: **P1 Assemble · P2 The Eye · P3 Walk · P4 Soul · P5 Voice**. The design doc's metamorphosis sequence is: **bare hand → leather glove (skin) → armor plates**, adding **camera eye**, **hearing**, and the **SI soul**.

### 4.1 Phase → Hardware Map

| Phase | Project Thing goal | DexHand path (cheap) | Wuji Hand 2.2 path (premium) |
|---|---|---|---|
| **P1 — Crawl / Assemble** | Working hand, coordinated gesture playback | Build DexHand (~$300), RP2040, BLE demo, ROS 2 gesture controller | Off-the-shelf; SDK joint-level control, `wuji_hand2_2_description` URDF in RVIZ2 |
| **P2 — Camera Eye** | Camera in middle fingertip + LED eye | Mount module in printed fingertip; LED in tip | **Conflict:** fingers are sealed/engineered assemblies — no fingertip cavity. Middle fingering is ~137 mm but the digit is a product, not a build. Camera likely becomes an *external* mount or a between-finger rig, not an implant. The **breathing status light partially satisfies the LED-eye intent** already. |
| **P3 — Walk** | Pentapod crawl gait | Custom gait on RP2040; must tune gains by hand | **URDF/MJCF/USD + MuJoCo/Isaac Sim**, soft-pad model, MIT impedance, 1000 Hz. RL-in-simulation is fully supported. **Blocker: tethered.** Needs an 80 g backpack (battery + IMU + Pi Zero) — exactly ETH's addition. |
| **P4 — Soul** | SI brain: decide → look → move → emote | Pi Zero / VPS over WiFi/BLE; ROS 2 bridge | Ethernet to a host or on-board SBC; same OODA decision layer, richer actuation vocabulary (20 DoF vs DexHand's fewer). Impedance control makes *emotive* motion (compliance, yield, yield-then-push) far more expressive. |
| **P5 — Hearing / Voice** | Whistle on ESP32-S3, wake-word, TTS reply | ESP32-S3 co-processor alongside RP2040 (RP2040 cannot run Whistle) | Same hearing module, but the hand's Ethernet link means the audio co-processor can sit on the network rather than on the hand. |
| **Skin / Glove** | Leather glove as first skin | Wrap the printed hand — total freedom | **Built-in:** user-removable, replaceable skin layer. Our leather glove becomes a *skin replacement*, not a wrap. Never run skinless. Glove (526 pts @ 120 FPS) is the sensing benchmark and the teleop data source. |

### 4.2 Where Wuji Strengthens the Plan

1. **Removable skin = designed affordance.** DESIGN.md §1.5's "skin before armor" metamorphosis maps onto a real, manufacturer-sanctioned part swap. Our aesthetic sequence (bare → leather → armor) becomes: bare skeleton → leather skin replacement → armored/external plates.
2. **Breathing status light = pre-existing heartbeat.** We wanted an "alive" tell; the product ships one. Our job is to *read* it, not invent it — the SI layer can treat the light as an output channel for internal state (and it's already semantically mapped: ready/running/warning/fault).
3. **Sim-first gait development.** URDF + MJCF + USD across MuJoCo and Isaac Sim means Phase 3 can be developed entirely without hardware, and the *same* models transfer to the DexHand phase if we build matching URDFs.
4. **MIT impedance is an expressiveness tool, not just a control mode.** kp = 5.0 / kd = 0.1 defaults give compliant, back-drivable motion — the physical basis for "yield," "recoil," "reach hesitantly." That is soul-adjacent behavior available at the actuator layer.

### 4.3 Where Wuji Fights the Plan

1. **Tethered by design.** RJ45 + 12 V 20 A wall power. No battery. Every Phase 3 decision is downstream of solving untethered power — the 80 g backpack (battery + IMU + Pi Zero) is the known-good answer, and it's ETH's contribution, not Wuji's.
2. **No fingertip cavity for the camera eye.** Our "middle finger is the head" idea assumes a hand we build. On a Wuji the digits are finished products. The camera eye survives on the DexHand; on the Wuji it must be externalized (or the LED-eye idea substitutes).
3. **Non-tactile 2.2 Beta.** No contact sensing. The Glove provides tactile data for *teleoperation*, but the hand itself cannot feel the ground during a crawl. For a crawling creature, ground contact feedback is arguably the most valuable sense — this is a real gap, and a reason the DexHand path (where we can add our own sensors) may be *better* for Phase 3 than the premium hand.
4. **Beta hardware.** Soft-pad hardness and skin design both unfinalized. Buying into 2.2 Beta means buying a moving target.
5. **Price unknown, likely thousands.** Reinforces DexHand-first sequencing.

### 4.4 Recommended Sequencing

**DexHand first — unchanged, and now better justified.**

- Every differentiator in DESIGN.md §"What this means for us" — **leather glove skin, middle-finger camera eye, Whistle hearing, SI soul** — is *easier* on a hand we build and *harder or impossible* on the Wuji 2.2 Beta.
- The Wuji's genuine gifts (removable skin, breathing light, MIT impedance, sim models) are all **Phase 3–4 concerns**, and all of them will still be there — likely in a finalized, tactile 2.3+ revision — when we graduate.
- The Wuji is the **premium body for the soul we proved cheaply**, not the platform for proving it.

**Graduation triggers** (when to move to Wuji):
- DexHand crawls reliably across surfaces (our Phase 3 proven).
- SI soul layer demonstrably drives decide→look→move→emote.
- Wuji ships a **finalized, ideally tactile** revision with published pricing.
- We have solved untethered power (backpack design validated on the DexHand).

---

## 5. Prior Art — ETH Zurich Walking Hand (Oct 2026)

Our closest reference, and it used the Wuji hand.

| Item | Detail |
|---|---|
| Lab | ETH Zurich **Soft Robotics Lab** |
| People | Prof. **Robert Katzschmann** (PI), PhD candidate **Amirhossein Kazemipour** |
| Hardware | **Off-the-shelf Wuji Technology hand** — chosen so manipulation capability wasn't compromised |
| Addition | **80 g backpack**: battery + **IMU** + **Raspberry Pi Zero** |
| Method | **Reinforcement learning in simulation** → transferred gait |
| Capabilities | Fingertip walking, turning, pushing objects, self-righting, **14 surfaces** |
| Gait | **"Virtual springs"** — each finger gets a custom target position for balance/movement |
| Key challenge | Hand **asymmetry** (unequal finger lengths, opposable thumb) — standard quadruped/biped gait training does not transfer |
| Coverage | Edd Gent, IEEE Spectrum / MSN, "This Disembodied Hand Is All the Robot You Need," **Oct 8 2026** |
| Earlier work | **EPFL LASA** + Nature paper `s41467-025-67675-8` — but those used specially-designed hands |

**What to steal:**
- **Virtual springs gait** — the concrete technique for turning an asymmetric five-digit hand into a stable locomotor. This is the Phase 3 roadmap; do not reinvent it.
- **RL in simulation → transfer** — pairs directly with Wuji's URDF/MJCF/USD models, and with whatever URDF we author for the DexHand.
- **80 g backpack architecture** — the known-good untethered solution (battery + IMU + Pi Zero).
- **Pi Zero as brain** — independently the same choice we made.

**What remains ours:**
- **Leather-glove skin** (their Thing is bare).
- **Middle-finger camera eye.**
- **Whistle on-device hearing.**
- **SI "soul" layer** — they did skill learning (locomotion); we want raised-and-reactive *presence*, not just movement.

---

## 6. Vendor & Contact

| Item | Detail |
|---|---|
| Pricing / purchase | **sales@wuji.tech** |
| Support | **support@wuji.tech** |
| HQ | Shenzhen — Bao'an, COFCO Chuangxin R&D Center |
| Second office | Beijing — Haidian, Tsinghua Tongfang |
| Docs | docs.wuji.tech |
| Product line | Wuji Hand, Hand 2, Glove |

---

## 7. Open Items Raised by This Digest

- [ ] Confirm Glove firmware: **v0.12.0** (raw dump) vs **v1.0.3** (release notes) — different channels?
- [ ] Ask `sales@wuji.tech` for **Hand 2.2 Beta pricing** and **roadmap to tactile / finalized skin**.
- [ ] Verify whether the Wuji digits can be opened at all — if not, the camera-eye concept is DexHand-only.
- [ ] Pull `wuji_hand2_2_description` and validate the URDF in RVIZ2 (no hardware needed) — cheapest possible Phase 3 start.
- [ ] Check whether the soft-pad model in MJCF/USD is usable for contact-rich crawl RL (this is the crux of sim-to-real for a hand that walks on its fingertips).
- [ ] Track the ETH paper/repo for the "virtual springs" implementation once published.
- [ ] SDK port is **50001**, not 7447 — fix any stale notes or scripts.

---

*Compiled 2026-10-21. Upstream facts are as captured in the raw dump; anything marked "verify" or listed in §7 was inconsistent or unconfirmed at capture time.*
