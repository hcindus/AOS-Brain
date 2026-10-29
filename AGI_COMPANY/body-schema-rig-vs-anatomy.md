# Body Schema — Rig (21) vs Anatomy (69) — the relationship

*Reconciled by Miles 2026-10-29, following Captain's steer that the two "Body Schema" files are the same body at two resolutions, not two rival truth sources.*

---

## The one-liner

**The 21-joint rig and the 69-DOF anatomy are the same body — Myl1Ssa.R8s (Raven), 169 cm / hourglass 37-27-39 — seen at two different granularities, with a clean forward-kinematics relationship between them.**

| | 21-joint RIG | 69-DOF ANATOMY |
|---|---|---|
| What it is | Cartesian **landmark positions** | **Joint angles** (range-of-motion) |
| Question it answers | "Where are her movable points?" | "What are her joint limits?" |
| Units | cm (x/y/z) | degrees |
| Source | `body_coordinates.json` (v1.0.0) | `myl2ssa-spec.md` ROMs → `body_schema_v1.py` |
| Consumer | Presence Engine (expression/gesture) | Motion Verb Layer + Body Schema (validation) |
| Granularity | 21 keypoints | 69 individual DOF in 23 groups |

---

## The mapping (rig keypoint → driving anatomical DOF)

Each rig landmark is *moved by* a subset of the anatomical DOF. Forward kinematics: joint angles (69) → landmark positions (21).

| Rig keypoint | Driven by (anatomical DOF group) |
|---|---|
| `head` | neck_rotation, neck_tilt, neck_nod |
| `L_ear` / `R_ear` | neck_rotation, neck_tilt (rigid with head) |
| `neck` | neck_rotation, neck_tilt, neck_nod |
| `L_shoulder` / `R_shoulder` | shoulder_abduction, shoulder_flexion, shoulder_extension, shoulder_rotation |
| `L_elbow` / `R_elbow` | elbow_flexion |
| `L_wrist` / `R_wrist` | wrist_flexion, wrist_rotation |
| `chest` | torso_rotation (rigid, follows ribcage) |
| `L_bust` / `R_bust` | torso_rotation (rigid with chest) |
| `waist` | torso_rotation, lumbar_flexion, lumbar_extension, lumbar_lateral |
| `pelvis` | hip_flexion, hip_extension, hip_abduction, hip_rotation (bilateral) |
| `L_hip` / `R_hip` | hip_flexion, hip_extension, hip_abduction, hip_rotation |
| `L_knee` / `R_knee` | knee_flexion |
| `L_ankle` / `R_ankle` | ankle_dorsiflexion, ankle_inversion |

**Note:** the 69-DOF inventory also includes DOF the 21-point rig does NOT expose (fingers ×20, toes ×14) — those are *end-effector* DOF with no dedicated rig landmark. So 21 rig points **⊂** 69 anatomy, but the anatomy is strictly richer.

---

## Why two files is *correct*, not a bug

- **Rig (21)** = the *expression* model. Presence Engine moves these points to render posture/gesture against facial expression. It wants few, meaningful, visually-salient landmarks.
- **Anatomy (69)** = the *safety/kinematics* model. The Motion Verb Layer validates joint targets against real ROM limits before accepting motion.

Merging them would produce one object bad at both jobs (an animation skeleton that also tries to be a joint-limit table). The correct design is **two artifacts + a documented FK mapping** between them.

---

## The adapter is already 69-DOF-capable

`AdapterFrame.body_points: Dict[str, Dict[str, float]]` is a generic point map — it carries 21 points today, 69 tomorrow, with zero contract change. The adapter (base.py `BodyAdapter.apply()`) is hardware-agnostic by design ("the agent owns presence, the adapter owns hardware").

**The one real gap:** the Presence Engine (`presence_engine.py`) only *emits* the 21 rig points; it does not yet expose the 69-DOF anatomy. To "map to both," the presence engine needs an `anatomy_frame()` (or the adapter needs to read anatomy from the Body Schema organ) so a single affect state drives **expression (21) + validated motion (69)** through one pipeline.

---

## Resolution (what to build)

1. **Keep two artifacts**, clearly named:
   - `body_schema_rig.py` → 21 landmarks (Presence Engine's expression domain)
   - `body_schema_anatomy.py` → 69 DOF (Motion Verb Layer's validation domain)
2. **A documented FK mapping** (this file) so the relationship is a fact, not an accident.
3. **The bridge** — one of two options (decide with Captain):
   - (a) Presence Engine gains an `anatomy_frame()` that maps its 21-point gesture into 69-DOF joint targets via FK, OR
   - (b) the adapter reads anatomy directly from the Body Schema organ, keeping the Presence Engine pure-expression.

Both kill the "two files claiming to be the Body Schema" ambiguity; (a) centralizes in the presence engine, (b) keeps the adapter as the single hardware truth.
