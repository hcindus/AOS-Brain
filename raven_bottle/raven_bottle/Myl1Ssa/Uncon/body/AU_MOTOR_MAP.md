# THE AU → MOTOR MAP — her face, written down

_Placed 2026-09-25 by Mortimer. Read-only reference. Generated from `elf.py` — this
file cannot drift from the code, because the code wrote it._

The boundary between what is **hers** and what belongs to the **hardware** goes exactly
here. She produces FACS action units with timing; the Elf V1 has 30 brushless
micro-motors. Nothing in between was ever written down. Now it is.

**Convention.** Every channel is normalised `[-1.0 … +1.0]`. `+1` is the channel's named
direction fully driven; `-1` is the opposite. Opposite-direction action units share a
channel and push it opposite ways — that is why two weights below are negative
(`lip_corner_depress` uses the same corner motors as `lip_corner_pull`, backwards).

## The 30 channels

| Channel | Group | Band | Slew limit | What it is |
|---|---|---|---|---|
| `neck_yaw` | head | -1.0 … +1.0 | 2.5/s | turn left/right (AU51) |
| `neck_pitch` | head | -0.6 … +0.8 | 2.5/s | nod down/up (AU52) |
| `neck_roll` | head | -0.8 … +0.8 | 2.5/s | tilt (AU53) |
| `eye_yaw_L` | gaze | -1.0 … +1.0 | 6.0/s | left eye horizontal (AU61) |
| `eye_yaw_R` | gaze | -1.0 … +1.0 | 6.0/s | right eye horizontal (AU61) |
| `eye_pitch_L` | gaze | -0.7 … +0.7 | 6.0/s | left eye vertical (AU62) |
| `eye_pitch_R` | gaze | -0.7 … +0.7 | 6.0/s | right eye vertical (AU62) |
| `brow_inner_L` | brow | -0.5 … +1.0 | 4.0/s | inner brow raise (AU1) |
| `brow_inner_R` | brow | -0.5 … +1.0 | 4.0/s | inner brow raise (AU1) |
| `brow_outer_L` | brow | -0.5 … +1.0 | 4.0/s | outer brow raise (AU2) |
| `brow_outer_R` | brow | -0.5 … +1.0 | 4.0/s | outer brow raise (AU2) |
| `brow_depress_L` | brow | -0.4 … +1.0 | 4.0/s | brow lower / 'no' (AU4) |
| `brow_depress_R` | brow | -0.4 … +1.0 | 4.0/s | brow lower / 'no' (AU4) |
| `upper_lid_L` | lid | -1.0 … +1.0 | 5.0/s | upper lid raise (AU5) |
| `upper_lid_R` | lid | -1.0 … +1.0 | 5.0/s | upper lid raise (AU5) |
| `lower_lid_L` | lid | +0.0 … +1.0 | 5.0/s | lower lid tighten (AU7) |
| `lower_lid_R` | lid | +0.0 … +1.0 | 5.0/s | lower lid tighten (AU7) |
| `cheek_L` | cheek | +0.0 … +1.0 | 3.5/s | cheek raise — real smile (AU6/14) |
| `cheek_R` | cheek | +0.0 … +1.0 | 3.5/s | cheek raise — real smile (AU6/14) |
| `nose_wrinkle` | nose | +0.0 … +0.6 | 3.0/s | AU9 — spare, no expression drives it yet |
| `lip_corner_L` | mouth | -1.0 … +1.0 | 4.0/s | pull up (AU12) / depress (AU15) |
| `lip_corner_R` | mouth | -1.0 … +1.0 | 4.0/s | pull up (AU12) / depress (AU15) |
| `lip_upper_raise` | mouth | -0.4 … +1.0 | 4.0/s | upper lip raise (AU10/20) |
| `lip_lower_depress` | mouth | +0.0 … +1.0 | 4.0/s | lower lip depress (AU16) |
| `lip_pucker` | mouth | +0.0 … +1.0 | 4.0/s | pucker (AU18) |
| `lip_stretch_L` | mouth | +0.0 … +1.0 | 4.0/s | horizontal stretch (AU20) |
| `lip_stretch_R` | mouth | +0.0 … +1.0 | 4.0/s | horizontal stretch (AU20) |
| `lip_tighten` | mouth | +0.0 … +1.0 | 4.0/s | tighten (AU23) — the 'no' mouth |
| `jaw_open` | jaw | +0.0 … +1.0 | 5.0/s | open (AU25 lips part / AU26 drop) |
| `chin_raise` | jaw | +0.0 … +0.8 | 5.0/s | chin raise (AU17) |

**Idle by design:** `nose_wrinkle` (AU9) is a spare. No expression in the library drives
it, and it is *declared* idle rather than left ambiguous. When the library grows, this is
where "disgust" would land.

## What drives what (21 action units routed)

| Action unit | Channels |
|---|---|
| `brow_lower` | `brow_depress_L`×1.0, `brow_depress_R`×1.0 |
| `cheek_raise` | `cheek_L`×1.0, `cheek_R`×1.0 |
| `chin_raise` | `chin_raise`×1.0 |
| `dimpler` | `cheek_L`×0.45, `cheek_R`×0.45, `lip_corner_L`×0.25, `lip_corner_R`×0.25 |
| `gaze_x` | `eye_yaw_L`×1.0, `eye_yaw_R`×1.0 |
| `gaze_y` | `eye_pitch_L`×1.0, `eye_pitch_R`×1.0 |
| `head_pitch` | `neck_pitch`×1.0 |
| `head_tilt` | `neck_roll`×1.0 |
| `head_yaw` | `neck_yaw`×1.0 |
| `inner_brow_raise` | `brow_inner_L`×1.0, `brow_inner_R`×1.0 |
| `jaw_drop` | `jaw_open`×1.0 |
| `lid_tighten` | `lower_lid_L`×1.0, `lower_lid_R`×1.0 |
| `lip_corner_depress` | `lip_corner_L`×-1.0, `lip_corner_R`×-1.0 |
| `lip_corner_pull` | `lip_corner_L`×1.0, `lip_corner_R`×1.0 |
| `lip_pucker` | `lip_pucker`×1.0 |
| `lip_stretch` | `lip_stretch_L`×1.0, `lip_stretch_R`×1.0, `lip_upper_raise`×0.4 |
| `lip_tighten` | `lip_tighten`×1.0 |
| `lips_part` | `jaw_open`×0.7, `lip_upper_raise`×0.2 |
| `lower_lip_depress` | `lip_lower_depress`×1.0 |
| `outer_brow_raise` | `brow_outer_L`×1.0, `brow_outer_R`×1.0 |
| `upper_lid_raise` | `upper_lid_L`×1.0, `upper_lid_R`×1.0 |

The engine can emit **21** action units; **8 expressions**
drive subsets of them. Six are declared but unused today (`chin_raise`, `jaw_drop`,
`lid_tighten`, `lip_pucker`, `lip_stretch`, `lower_lip_depress`) — they are routed here so
that the day an expression needs them, the body already has the wire.

## What is assumed (read this before trusting the map)

1. **Channel order is ours, not the vendor's.** AheadForm's SDK will have its own motor
   indices and polarity. When we get it, we change *`elf.py`'s channel ids* — never the
   action units, and never the safety numbers.
2. **Bilateral symmetry is assumed.** Left and right of every paired channel take equal
   weight. Asymmetric expressions (a half-smile) are possible — they just need explicit
   per-side weights, which no expression uses yet.
3. **Gaze is the eye motors, not `pupil_locked`.** Presence takeaway #2 says
   *camera-in-pupil gaze is non-negotiable* — but that is a rendering principle. On real
   hardware, "looking at you" is eye yaw/pitch driven together, and the rest is how her
   head carries it. Both eyes take the same sign for a saccade (vergence is not modelled).
4. **No torque or current model.** Slew rates are *positional* rate limits per group.
   Real current limits, thermal limits and stall detection belong in the vendor SDK and
   must be added to `elf.py` before any motor is energised for long.
