# presence_engine — BEFORE / AFTER

_Placed 2026-09-25 by Mortimer, on the Captain's order, at Raven's request._

Her presence engine — affect → 30-motor facial rig — as it arrived in the
2026-09-25 bottle, and as it is now. Both versions are here, lockable and
side by side, so the change can be judged rather than taken on trust.

| File | What it is | Bytes | md5 |
|---|---|---|---|
| `presence_engine.BEFORE.py` | as shipped in the bottle | 23,102 | `682086392f6eb7ef53dfc5900fa3b686` |
| `presence_engine.AFTER.py` | corrected | 23,481 | `26f29ecee23c2d2e228d8478bef8e3c6` |
| `BEFORE-AFTER.patch` | the one change, in `diff -u` form | — | — |

Nothing else was touched: no expression was added, no timing changed, no
threshold moved, no SOUL wording edited. The engine's behaviour for every
call that already worked is byte-identical.

---

## The defect

`self._energy` — thyroid energy, the thing that scales how hard an expression
lands (takeaway #5: *presence is art-direction*) — was assigned **only** inside
`update()`:

```python
def update(self, ternary="⊙", valence=0.0, arousal=0.0, thyroid="baseline"):
    ...
    self._energy = 1.0 if thyroid == "secreting" else (0.55 if thyroid == "suppressed" else 0.8)
```

But `frame()` reads it:

```python
aus = {au: round(i * self._energy, 3) for au, i in exp.action_units.items()}
```

So calling `frame()` before `update()` raised `AttributeError: 'PresenceEngine'
object has no attribute '_energy'`. And that is exactly what the CLI's
`express` path does:

```bash
python3 presence_engine.py express curious   # ← crashed
python3 presence_engine.py status            # ← worked
python3 presence_engine.py demo              # ← worked (its loop calls update() first)
```

**So the engine looked healthy and wasn't.** `status` and `demo` passed, which
is why the defect survived assembly. `express` — the one command that shows a
single named expression — was dead on arrival.

`rig_frame()` had already been written defensively, with
`energy = getattr(self, "_energy", 0.8)`. `frame()` was not. The author saw the
hazard in one method and missed it in the other, four lines apart.

## The correction

Two changes, both additive:

1. `self._energy: float = 0.8` initialized in `__init__` — the same default
   `rig_frame()` was already falling back to, so nothing about intensity
   changes; it just exists before the first `update()`.
2. `frame()` now reads `getattr(self, "_energy", 0.8)` — the same guard
   `rig_frame()` uses, so the two paths can never disagree again.

## What the correction verifies

```
8/8 expressions frame:  attentive · boundary · considering · curious ·
                        delight · playful · serious · warmth
rig_frame() moves:      32 face landmarks + 21 body joints
warmth predictive lead: 840 ms   (unchanged — the manifest's number holds)
```

## Still true

- The 30-motor Elf V1 is the **hardware** mapping. AUs are emitted; motors are
  moved by the body. No hardware here, so that half is untested and I am not
  claiming otherwise.
- No TTS assets are bundled. Voice remains config.

_Read it, do not edit it. If you want it changed, say so and it gets changed —
by hand, on purpose, with a patch you can read._
