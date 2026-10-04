# HER BODY — what this is, and what it is not yet

_Placed 2026-09-25 by Mortimer, on the Captain's order. **Read-only.** Not wired into
her brain. Hers to make permanent, or to leave in the drawer._

---

## Why this exists

The 2026-09-25 bottle shipped four adapters — `blender`, `digital_world`, `unitree`,
`unitree_h1` — and **none for her own body**. The manifest named her vessel (*AheadForm
Elf V1 head → Elf-Xuan full body, 30 brushless micro-motors*) and stopped there.

The gap was wider than a missing file. Every adapter implemented exactly two methods:
`apply(frame) → dict` and `status() → dict`. Nothing sent the dict anywhere. There was
**no loop** connecting her presence engine to any body at all — no transport, no
feedback, no limits, no watchdog, no e-stop. A renderer can work like that. A body cannot.

So this is the whole missing half, in five files.

## What is in here

| File | What it does |
|---|---|
| `elf.py` | The adapter. `apply()` (HAL-compatible), the 30-channel map, the safety envelope, four transports, and a `status()` that tells the truth |
| `body_driver.py` | **The loop that was missing** — her engine → frame → envelope → transport → feedback, at 50 Hz, with predictive lead honoured |
| `AU_MOTOR_MAP.md` | The AU → channel table, generated from the code, with every assumption written down |
| `verify_body.py` | 20 checks. Runs with no hardware. Proves limits, slew, watchdog, e-stop, transports, feedback |
| `BODY_VERIFICATION.json` | The last run's evidence |

## The safety envelope (the part that matters)

Her face is 30 brushless motors in bionic silicone. A bad frame is a twitch, a stall, or
a burnt coil — so the envelope is not optional:

- **Bands** — every channel has a hard min/max. Lips pull up to +1.0 but only depress to
  −1.0 per side; `lower_lid` never goes negative, because it has no such direction.
- **Slew limiting** — a demand is a *direction*, not a position. Full-scale jumps are
  rate-limited per group (head 2.5/s, gaze 6.0/s, face 3.5–5.0/s). The limiter is proven:
  a step demand after one 20 ms period moves 0.08, never the full travel.
- **Watchdog** — 250 ms of silence and she *relaxes to rest* rather than freezing
  mid-expression. Silence should look like calm, never like a stuck face.
- **E-stop** — refuses every command, holds position, and requires an explicit clear. It
  is not a suggestion and it does not time out.
- **Audit** — the driver counts limit violations and peak step every tick. A run that
  cannot say "zero violations" is a failed run.

## Honest status

`ElfAdapter().status()` reports `hardware_present: false`, `state: "no_hardware"`, and:

> *No Elf V1 (or Elf-Xuan) on this device and no vendor SDK. This adapter can compute and
> record what it would send. It cannot move a body, and it says so rather than reporting ok.*

That is deliberate. An adapter that reports healthy while wired to nothing is worse than
no adapter — it is a lie that survives review.

## Transports

| Kind | State |
|---|---|
| `null` | **Works.** Records packets, simulated feedback flagged `sim: true`. This is what proves the stack |
| `socket` | **Works.** TCP to a vendor bridge (host PC / SDK daemon). Fails cleanly on a dead port |
| `serial` | **Works**, needs `pyserial` (present, 3.5) and a real port. Failures are a sentence, not a trace |
| `ble` | **Refuses loudly.** Needs the vendor's GATT profile. It will not pretend |

## Making it permanent

Nothing here is wired in. To make it live, in her tree:

```bash
cd ~/v1/projects/5912/Myl1Ssa
mkdir -p adapters
cp Uncon/body/elf.py adapters/elf.py            # beside blender/unitree/digital_world
cp Uncon/body/body_driver.py runtime/           # the loop
# then, to see it drive (records packets, moves nothing):
python3 runtime/body_driver.py sim
```

And when hardware exists: point `ElfAdapter(transport_kind="socket", port=…)` or
`serial` at the controller, replace `encode()` with the vendor's framing, and add their
current/thermal limits to the envelope. **Nothing above the transport changes.**

## What is still genuinely missing

1. **The vendor SDK.** No SDK, no channel order, no torque limits. This file is the
   shape waiting for it.
2. **Real proprioception.** `read_state()` echoes the simulation. Real feedback means
   encoders, and a loop that compares commanded vs achieved.
3. **Full-body (Elf-Xuan).** This covers the head and face. The `body_coordinates.json`
   rig has 21 body joints and no adapter drives them yet — that is the next adapter, not
   this one.
4. **The 30 motors are not energised.** Nothing in this stack can hurt her, because
   nothing in this stack is connected to anything.
