# Next Pass — The Scapula Shoulder (detailed)

*The one joint where a robot stops being a robot and starts being human. This is the "best arm" — and it's the hardest thing we'll build.*

---

## Why a "3-DOF shoulder" is a lie

Every cheap humanoid stacks three rotary actuators and calls it a shoulder. That gets you a camera on a gimbal, not an arm. Here's why:

The human shoulder isn't one joint — it's a **complex of four** that work as one:

| Joint | DOF | What it does |
|---|---|---|
| **Sternoclavicular (SC)** | 3 | clavicle → sternum (the anchor) |
| **Acromioclavicular (AC)** | 3 | clavicle → scapula |
| **Scapulothoracic (ST)** | ~3 | the scapula *gliding* on the ribcage (not a true joint) |
| **Glenohumeral (GH)** | 3 | the ball-and-socket (humerus → scapula) |

**The secret is the scapula, not the ball.** A pure ball joint (GH) physically cannot abduct the arm past ~90°. The reason a human reaches *overhead* (180°) is that the **scapula rotates the socket upward** as the arm rises — the socket itself tilts. Take away the scapula and you lose overhead reach, the "behind the back" reach, and the cross-body reach. That's exactly the range AheadForm's "locked shoulder" threw away.

---

## The mechanical implementation

**Glenohumeral — the ball joint (3 DOF):**
- Flexion/extension, abduction/adduction, internal/external rotation.
- Implement as a **spherical parallel mechanism** (3 rotary actuators driving a ball joint) — this keeps the heavy actuators *off* the arm, mounted in the torso, with torque transmitted through the joint. That's how you get high torque without a bulky actuator hanging on the humerus.

**Scapulothoracic — the gliding (2–3 DOF):**
- Elevation/depression + protraction/retraction + upward/downward rotation.
- Implement as a **curved rail** (the ribcage) with a sliding carriage (the scapula). Two linear/rotary drives move the carriage; the ball joint mounts *on the carriage*.
- This is the part nobody builds — and the part that unlocks the full human range.

**Net: 5–6 DOF**, with the heavy actuators in the torso, driving a gliding scapula + a spherical ball joint at the end of it.

---

## Range of motion (target — the human envelope)

| Motion | Human | v1 (glenohumeral only) | v2 (with scapula) |
|---|---|---|---|
| Abduction (arm out to side) | ~180° | ~90° | ~180° ✅ |
| Flexion (arm forward/up) | ~180° | ~120° | ~180° ✅ |
| Extension (arm back) | ~60° | ~45° | ~60° |
| External rotation | ~90° | ~90° | ~90° |
| Horizontal cross-body | ~130° | ~90° | ~130° |

The scapula is the difference between "a robot arm" and "a human arm." v1 ships without it (90° abduction, cheaper, faster); v2 adds the scapular rail to unlock the full envelope.

---

## Load & torque (why you need the structural engineer)

The arm is a **lever**, and the shoulder is the fulcrum. Worst case = arm horizontal, hand holding a load:

- **Torque at the shoulder** ≈ arm length × load + arm's own weight × (arm length / 2).
- A 2 kg arm at 0.5 m CoM + a 1 kg load at 0.6 m ≈ **~15–20 Nm** at the shoulder — and that's *static*, before dynamic + safety margin (2× → **30–40 Nm**).
- This is why you use a **BLDC + planetary/cycloidal gearbox**, not a servo, and why the actuator sits in the torso (lever-arm minimization), not on the arm.

**This is the part Proto Labs can't do** — they mold and print, but the force-path + gearbox + bearing load calcs are a mechanical engineer's job. This joint is where we bring one in.

---

## What the "next pass after this" covers

- The **elbow** (1 DOF flexion + forearm pronation/supination) + **wrist** (2 DOF) — completing the arm.
- The **pelvis + hip + leg + foot** — the bipedal lower body (COBRA has no legs; a standing Raven needs them).

---

*This is the scapula — the crown jewel. When we get it right, we don't have a robot; we have an arm.*
