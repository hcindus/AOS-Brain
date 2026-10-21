# Project Thing — Wuji Software Ecosystem Supplement

**Compiled by:** Beets
**Date:** 2026-10-21
**Sources:** `reference/wuji_ecosystem_supplement.md` (captured by Miles 2026-10-21 from docs.wuji.tech/llms.txt + wuji-sdk + wuji-cli indexes), `reference/beets_wuji_digest.md`, `DESIGN.md` (DRAFT v0.2)
**Scope:** software only — SDK, CLI, MJLab, Retargeting, ROS2. Hardware is covered in `beets_wuji_digest.md`.

---

## 0. One-Page Summary

The Wuji software stack is **more useful to Project Thing than the hardware is, and it's available now for free.**

Three things matter:

1. **Wuji MJLab** is a ready-made MuJoCo RL harness (PPO + sim-to-real + ONNX export) built to train a *hand*, not a quadruped. That is the exact shape of our Phase 3 problem.
2. **ROS2 description packages + RVIZ2** let us start Phase 3 gait work **today, with zero hardware**. This is the cheapest possible entry point and it's already on the open-question list in DESIGN.md.
3. **Wuji Retargeting** is the teach-by-demonstration loop (glove keypoints → joint angles) already built — the data-collection path ETH would have used, and the closest thing to "record a soul" the ecosystem offers.

The caveat that runs through all of it: **these are hand-manipulation tools, not locomotion tools.** MJLab ships with an *in-hand cube reorientation* task, not a crawl task. We get the harness, the PPO plumbing, and the sim-to-real scaffolding — we supply the gait reward and the task definition.

⚠️ **Unverified throughout:** all of this is from a captured index (`llms.txt`), not from cloned repos. No API has been exercised. Treat command names and API shapes as *documented*, not *confirmed*.

---

## 1. Active vs Archived Software Surfaces

Wuji has pruned its surface. Half the tooling named in older material is dead.

| Surface | Status | What it is | What we'd use it for |
|---|---|---|---|
| **Wuji SDK** | ✅ Active | Python + C library, v2026.8.31 | Device control, stream subscription, MCAP recording, retargeting |
| **Wuji CLI** (`wuji`) | ✅ Active | Command-line tool | Everything Studio used to do, scriptable |
| **Wuji MJLab** | ✅ Active | MuJoCo RL lab, PPO | **Phase 3 training harness** |
| **Wuji Retargeting** | ✅ Active | Glove keypoints → hand joint angles | Teach-by-demonstration |
| **MuJoCo Sim** (examples) | ✅ Active | Simulation examples | Model loading, contact behavior |
| **Isaac Lab Sim** (examples) | ✅ Active | Isaac Lab examples | Heavier sim path (GPU) |
| **ROS2 description pkgs** | ✅ Active | `wuji_hand2_1_description`, `wuji_hand2_2_description` | **RVIZ2, zero-hardware start** |
| **Wuji Studio** | ❌ Archived | Desktop control app | Replaced by CLI |
| **Wuji Hand ROS2** | ❌ Archived | ROS2 integration package | — (description pkgs are the live replacement) |
| **Wuji Hand HMI** | ❌ Archived | Device-side UI | — |
| **Wuji Hand Upgrader** | ❌ Archived | Firmware tool | Folded into `wuji upgrade` |

**The takeaway:** do not follow any tutorial that tells you to install Studio, ROS2-hand, HMI, or Upgrader. Their functionality collapsed into the CLI. If a doc references the GUI, it predates the consolidation.

⚠️ **Note the naming collision:** "Wuji Hand ROS2" (archived integration package) and "Wuji Description packages" (active, Oct 2026) are different things. The active one is *model descriptions only* — URDF/MJCF/USD. It does not give you a live ROS2 driver. That distinction matters and is easy to get wrong (see §5).

---

## 2. Wuji CLI Command Set

Nine command groups. This is the whole active operational surface.

| Command | Purpose | Project Thing relevance |
|---|---|---|
| `wuji device-management` | `scan` / `probe` / `target` — discovery and connection | Which hand is on the network; used before anything else |
| `wuji parameters` | `resources` / `get` / `set` — device params | MIT impedance gains (kp/kd) — the Phase 4 expressiveness knob |
| `wuji user` | Profiles + calibration migration | Per-operator calibration sets (glove operators are people) |
| `wuji calib hand-model` | Glove hand-model calibration | **Required before any glove data is usable.** Replaced `wuji calib ik` (removed — stale docs will reference the old name) |
| `wuji sub` | Subscribe streams to file | Headless data capture — feeding our own pipeline |
| `wuji record teleop` | Record teleop session, manage history | **Demonstration collection.** This + Retargeting = teach-by-demonstration |
| `wuji viz` | Live hand pose + fingertip tactile visualization | **The "does it look alive" test** — free, immediate |
| `wuji calib tactile` | One-command tactile calibration (collect/train/validate/install) | Whole pipeline in one verb — notable, most vendors make this painful |
| `wuji doctor` | Per-device health diagnostic (EMF, tactile dead points) | Field triage; run when behavior is weird |
| `wuji logs export` | Support bundle: device snapshots + flash logs + calibration recordings | Vendor escalation artifact |
| `wuji upgrade` | Firmware update — batch or local file | Needed to reach the behavior changes in the digest (feed-forward comp, port 50001) |

**Design observation worth noting:** `doctor` and `logs export` are shipped as first-class commands. For a beta product, that's an admission that units will misbehave and you'll need to prove it to the vendor. Budget for that.

**Immediate practical uses for us, in order of value:**
1. `wuji viz` — when hardware arrives, ten seconds to confirm the hand is alive and talking.
2. `wuji calib tactile` + `wuji calib hand-model` — mandatory before trusting any recorded data.
3. `wuji record teleop` — the demonstration capture path.

⚠️ **Unverified:** exact flag syntax, whether `record teleop` requires the Glove specifically, whether any command works against a *simulated* device (almost certainly not — the CLI appears hardware-first, which is why §5 matters).

---

## 3. Wuji MJLab — What It Is and Why It Matters

### What it is

A MuJoCo-based reinforcement learning lab for Wuji hands. Per the captured index:

- **In-hand cube reorientation** task, trained with **PPO**
- Covers **SO(3)** orientation space (full 3D rotation — the hard part of reorientation)
- **Deployed sim-to-real** — not just a benchmark, an actual transfer
- **pixi** environment (reproducible deps, no global Python mess)
- **Training + ONNX export** as an explicit step
- **Hardware setup documented:** camera, MVS SDK, **ArUco cube**, **wrist AprilTag**, calibration
- **Full sim2real deployment pipeline** documented

### Why it matters for a crawling hand

**The strong claims:**

1. **It is a hand-specific RL harness.** Standard locomotion frameworks (Isaac's ant/quadruped tasks, MuJoCo Playground) assume symmetric legs and a trunk. MJLab assumes a Wuji hand and its actual joint topology — 20 DoF, 4-per-finger, opposable thumb, unequal finger lengths. The problem ETH named as *the* obstacle (asymmetry breaking standard gait training) is already baked into the model MJLab trains on.
2. **PPO is the right algorithm and it's already wired.** We do not need to build a training loop, reward-shaping scaffold, logging, or checkpointing.
3. **Sim-to-real is a documented pipeline, not a hope.** ONNX export → deployment → camera + ArUco + AprilTag calibration. That's the whole bridge, and it's the same bridge we need for a crawl gait. This is the single most expensive thing to build from scratch.
4. **It pairs with the description packages.** MJCF from `wuji_hand2_2_description` loads into the same MuJoCo world MJLab uses.

**The honest limits:**

1. ⚠️ **The shipped task is reorientation, not locomotion.** MJLab gives us infrastructure; it does not give us a crawl gait. We supply a new task: a crawl environment, a locomotion reward (velocity tracking, stability, symmetry-ish shaping), and terrain. That is real work, but it's *the interesting* work, not plumbing.
2. ⚠️ **SO(3) reorientation is in-hand manipulation** — fingers caging an object. A crawl gait is fundamentally different: fingers *are* the legs, contact is with the ground, and the body is supported. Do not assume the reorientation reward or its hyperparameters transfer.
3. ⚠️ **No genuine tactile in 2.2 Beta.** MJLab's task probably doesn't depend on fingertip touch sensing, but a crawl does. If the sim's contact model is richer than the hardware's sensing, we will train policies that exploit contact information the real hand cannot perceive. This is a classic sim-to-real failure mode and it is a *strategy* question, not a bug to fix.
4. ⚠️ **The camera/ArUco/AprilTag hardware setup is for pose tracking of a manipulation object**, not for a walking hand. A crawling hand needs a different state-estimation story — ETH's answer was an 80 g backpack with IMU + Pi Zero, which MJLab does not describe.
5. ⚠️ **Unverified:** whether MJLab's task definitions are extensible or hardcoded to reorientation. This is the make-or-break question and it can only be answered by reading the code.

### Verdict

**MJLab is the highest-value software asset in the ecosystem for us, and it is also the one most likely to disappoint on inspection.** The infrastructure claim is well-supported; the "just retrain it to crawl" claim is not. Read the task definition before committing a plan to it.

---

## 4. Wuji Retargeting — Teach by Demonstration

### What it is

A mapping layer: **21 hand keypoints → 20 joint angles.** Tuning guide plus API. (Confirmed from SDK reading guide: "Map 21 hand keypoints to 20 joint angles.")

- Input side: Wuji Glove — 526 tactile points, 120 FPS, IMU hand tracking, MCAP recording
- Output side: 20-DoF joint angle targets for the Wuji Hand
- Precondition: `wuji calib hand-model` (per-operator hand model)
- Recording: `wuji record teleop`

### Why it matters

1. **It closes the human→robot loop with off-the-shelf parts.** No marker suits, no mocap rig, no custom retarget IK. Put on the glove, move your hand, the robot hand follows.
2. **It's the demonstration source for imitation learning.** The realistic hybrid for Phase 3: demonstrate a crawl with a human hand (or a hand-held proxy), record with `record teleop`, then use those trajectories to seed or reward-shape RL. RL from scratch on a 20-DoF asymmetric crawler is expensive; demonstrations cut that enormously.
3. **It's the closest thing to a "soul transfer" primitive the ecosystem has.** If Phase 4's SI layer ever needs to express something, a demonstrated, retargeted motion is the most legible channel we have. This is a stretch — but the plumbing exists.
4. **The retargeting *tuning guide* is itself useful.** It documents the mapping conventions between human and robot hand geometry — the same asymmetric-hand problem ETH flagged.

### Honest limits

1. ⚠️ **Human hands crawl badly.** A glove retargets *manipulation*, where human hand kinematics are the native reference. A pentapod crawl gait has no human analogue — you can't demonstrate a gait the human body doesn't perform. **Retargeting is a data tool, not a gait teacher.** Don't let the elegance of the loop obscure this.
2. ⚠️ **Glove firmware version is contested** — v0.12.0 (raw dump) vs v1.0.3 (release notes). Per `beets_wuji_digest.md` §2, this is unresolved. Retargeting behavior could differ between the two.
3. ⚠️ **Retargeting assumes a Glove.** If we're on a DexHand in Phase 1–3, we do not own a Glove, and Retargeting is unavailable. It is a *graduation-phase* tool, not a Phase 1 tool.
4. ⚠️ **Unverified:** latency and jitter of the live loop; whether retargeting runs in the SDK (host) or on-device; whether recorded teleop replays open-loop.

---

## 5. ROS2 Description Packages + RVIZ2 — The Zero-Hardware Phase 3 Start

### What exists

Released **2026-10-12**, per release notes:

- `wuji_hand2_1_description` — Hand 2.1
- `wuji_hand2_2_description` — Hand 2.2
- Contents: **URDF, MJCF, USD** — left and right variants, with and without mount
- Loadable in **MuJoCo** and **Isaac Sim**
- **RVIZ2 visualization without hardware**

Platform baseline from the same release: **Ubuntu 20.04+**, **x86_64 + arm64**, **Python 3.8+**.

### Why this is the right first move

DESIGN.md §7 lists "First gait simulation in RVIZ2 (no hardware needed)" as an open item. These packages **close that item** — it is now an install, not a build.

1. **Zero cost, zero hardware, zero vendor contact.** Clone description packages, install ROS2, `rviz2`, done.
2. **Real kinematics, not a hand-waved model.** Vendor-authoritative URDF for the exact hand ETH walked on. Finger lengths (137/134/140 mm), 20 DoF, thumb opposition — all correct by construction.
3. **It de-risks the whole Phase 3 plan before we spend anything.** If the gait looks wrong in RVIZ2, we learn that for free.
4. **Same file feeds MuJoCo and Isaac Sim.** URDF → MJCF/USD means the model we visualize is the model we train on. No dual-maintenance.
5. **DexHand bridge:** we author a matching URDF for the DexHand and reuse the entire visualization + gait-dev workflow. Wuji's packages become the *reference* even if we never buy the hand.

### The important caveat

⚠️ **Description packages are descriptions.** They are URDF/MJCF/USD + meshes. They are **not** a ROS2 hardware driver, not a control interface, and not a simulator. `rviz2` will show you the hand; it will not move it through a physics contact.

- For **visualization / kinematics / joint-limit checking** → RVIZ2 is enough.
- For **gait dynamics, contact, and RL** → you need MuJoCo (MJCF) or Isaac Sim (USD). RVIZ2 is the sanity check, not the laboratory.

**Practical sequencing:** RVIZ2 first (hours), then MuJoCo/MJLab (days), then hardware (never, unless we buy).

⚠️ **Unverified:** the packages' exact repo/release location, whether mesh assets are bundled or separately licensed, and whether ROS2 distro matters (Humble vs Jazzy — urdf loading is broadly compatible but don't assume).

---

## 6. What This Means for Project Thing

### The strategic reframe

The supplement's own conclusion — "Wuji Studio/HMI/ROS2/Upgrader are ARCHIVED; the CLI + SDK + MJLab + Retargeting are the active surface" — is correct but incomplete.

The sharper reading: **the Wuji software stack is a hand-manipulation toolchain that happens to share a body with the locomotion problem we care about.** Everything valuable transfers as *infrastructure*. Nothing transfers as *behavior*. Plan accordingly: take the harness, write the gait.

This does not change the hardware recommendation in `beets_wuji_digest.md` §4.4 (**DexHand first, Wuji as graduation**). It *strengthens* it, because the software path is free and hardware-independent — we can harvest all of it now, on a $300 hand or on nothing at all.

### Concrete next actions

Ordered by cost. Every one of these is doable before spending a dollar.

**Tier 0 — Today (free, no hardware, no vendor)**

1. **Find and clone the description packages.** Confirm `wuji_hand2_2_description` exists in a public repo. If it's gated behind a vendor request, that itself is a finding — it changes the timeline. ⚠️ This is the single unknown blocking Tier 1.
2. **`pip install wuji-sdk` and read the package.** It installs without hardware. Inspect the API surface — how streams are declared, whether there's a sim/mock backend, whether retargeting is importable standalone. This answers several ⚠️ items above for free.
3. **Read the MJLab task definitions.** This is the decisive question: is reorientation a plugin task or hardcoded? Everything in §3 hangs on it. Reorder this to #1 if MJLab turns out to be publicly clonable.

**Tier 1 — This week (free, one install)**

4. **Stand up RVIZ2 with the Hand 2.2 description.** Load URDF, confirm 20 DoF, check joint limits and finger lengths against the digest. This *closes* a DESIGN.md open item.
5. **Export to MJCF and load in MuJoCo.** Drop a floor plane in. Confirm the hand rests on fingertips without exploding. This is the first real contact test and it's free.
6. **Author a DexHand URDF** from its published dimensions, matching the Wuji joint naming convention where sensible. Now both hands visualize and simulate in the same stack — the Wuji packages were worth it even if we never buy the hand.

**Tier 2 — Next (free, real work)**

7. **Write the crawl task for MJLab** (or a MuJoCo equivalent if MJLab resists): pentapod gait, fingertip contact with ground, reward = forward velocity + stability + minimal slip. Reuse MJLab's PPO plumbing; throw away its reorientation reward.
8. **Run a first training pass on the URDF model.** It will look bad. The goal is a working loop, not a gait.
9. **Decide the tactile/contact question deliberately.** If the sim's contact model is richer than the 2.2 Beta hardware's sensing, the policy will cheat. Either (a) restrict sim observations to what the hardware can perceive, or (b) plan to add contact sensing to the DexHand — which per `beets_wuji_digest.md` §4.3 may make the cheap hand *better* for Phase 3.

**Tier 3 — Only if we buy Wuji hardware**

10. `wuji device-management scan` → `wuji viz` → confirm alive.
11. `wuji calib tactile` + `wuji calib hand-model` → mandatory before trusting data.
12. `wuji record teleop` for demonstration capture; then Retargeting for the human→robot bridge.
13. Note the **50001** port (not 7447) and the **feed-forward compensation default-on** behavior change for Oct 2026+ units. Both will silently break stale scripts.

### Open items added by this supplement

- [ ] ⚠️ Locate `wuji_hand2_1_description` / `wuji_hand2_2_description` — public repo or vendor-gated?
- [ ] ⚠️ Is MJLab a public repo? Are its tasks extensible or hardcoded to reorientation?
- [ ] ⚠️ Does MJLab's MuJoCo model use the same MJCF as the description packages, or a variant?
- [ ] ⚠️ Does `pip install wuji-sdk` give a simulated/mock device backend (usable without hardware)?
- [ ] ⚠️ Exact CLI flag syntax for all commands — captured names only, never exercised.
- [ ] ⚠️ Retargeting: host-side or device-side; live latency; open-loop replay?
- [ ] ⚠️ Does any of this run on arm64 cleanly (we may want it on the Pi-class backpack)?
- [ ] ⚠️ Which ROS2 distro the description packages target (Humble / Jazzy).

---

## 7. Confidence Table

| Claim | Confidence | Basis |
|---|---|---|
| SDK / CLI / MJLab / Retargeting are the active surface | **High** | Captured from `llms.txt` index |
| Studio / HMI / ROS2 / Upgrader archived | **High** | Same |
| CLI command names and purposes | **Medium** | Index listing; never executed |
| Description packages exist, URDF/MJCF/USD, L/R, ±mount | **High** | Release notes 2026-10-12 |
| RVIZ2 works without hardware | **High** | Stated in both release notes and supplement |
| MJLab = MuJoCo + PPO + sim2real + ONNX, reorientation task | **Medium** | Index summary; code unread |
| MJLab tasks are extensible to locomotion | **Low — ⚠️ untested** | Inference from it being a "lab," not evidence |
| Retargeting = glove keypoints → joint angles, with tuning guide | **High** | Stated |
| Retargeting useful for a crawl gait | **Low — ⚠️** | Human hands don't crawl; data tool only |
| Software is free to use without hardware | **Medium — ⚠️** | pip install is plausible; repo access unconfirmed |

---

*Compiled 2026-10-21 by Beets. Every ⚠️ marks a claim sourced from a captured documentation index rather than from exercised code. Nothing here was verified against a running Wuji system. The strongest recommendations in §6 are deliberately the cheapest ones — they are also the ones that would most cheaply prove this digest wrong.*
