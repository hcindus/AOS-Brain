# TCPA Muscle — Build Spec (the first muscle we make)

*Goal: prove artificial muscle works, in an afternoon, for ~$30. This teaches the principle every soft actuator is built on.*

---

## Parts list

| # | Part | Spec | Approx cost |
|---|---|---|---|
| 1 | **Silver-plated nylon thread** (conductive) | e.g. "conductive thread," 2-ply or 3-ply | ~$10 |
| 2 | **Nylon 6,6 fishing line** | 0.5 mm monofilament (for high-force version) | ~$5 |
| 3 | **Drill** (or a cheap DC motor) | to twist the fiber | (have) |
| 4 | **Bench power supply** | 0–30 V, 0–3 A, current-limited | ~$40 (or use a LiPo + resistor) |
| 5 | **Mandrel** | a 1–2 mm rod (steel/brass) to coil around | ~$2 |
| 6 | **Weight** | ~50–100 g to hold tension while twisting | (have) |
| 7 | **Oven or hot-water bath** | to anneal (heat-set) the coil | (have) |

*Cheapest path: skip the power supply and use a 18650 cell + a resistor for Joule heating. But a bench supply is worth it for repeatable tests.*

---

## Build procedure (the classic TCPA recipe)

1. **Cut** ~1 m of silver-plated nylon thread (or fishing line).
2. **Fix one end** to a fixed point; **attach the other to the drill** with the weight hanging to keep tension.
3. **Twist** with the drill until the fiber is heavily twisted — it will start to **snarl/coil on itself**. (Thousands of twists per meter. You'll see it begin to buckle into loops.)
4. **Coil** the twisted fiber around the **mandrel** (wrap tightly, like a spring), keeping tension.
5. **Anneal**: bake at ~180 °C for ~1 hour (oven) or boil in water, to **set the coil shape** permanently.
6. **Cool and remove** from the mandrel. What you have is a **TCPA muscle** — a spring that contracts when heated.
7. **Actuate**: pass current through it (Joule heating via the silver coating). Watch it **contract**. Cut current → it **relaxes**.

---

## What to measure (the numbers that matter)

| Metric | Target | How |
|---|---|---|
| **Strain** | 20–30% | (rest length − contracted length) / rest length |
| **Force** | 1–5 N (single fiber) | hang increasing weight until it can't lift |
| **Speed** | ~0.1–1 s contract | time to full contraction at a given current |
| **Current** | ~0.2–1.5 A | note the current that gives fastest full contraction without melting |

**Force scales with fiber thickness + count.** Bundle N fibers in parallel → N× force. That's the "distributed muscle" idea — a bicep is thousands of parallel fibers, not one thick string.

---

## What this teaches (the principle)

The muscle contracts because the twisted fiber, when heated, **unwinds slightly and the coil tightens**. Cool it and it relaxes back. That's the whole thing — a **twisted string that remembers heat**. Everything fancier (McKibben, EHD, the MIT fiber) is the same "heat/energy → contract → relax" loop with better plumbing.

---

## Next after TCPA works

1. **Antagonistic pair** — two TCPAs, one contracts while the other relaxes → a joint. (This is the scapula shoulder's future muscle.)
2. **McKibben** — for higher force (silicone tube + braid).
3. **Nitinol** — for silent micro-motion (hands/face).
4. **EHD pump** — the untethered v2 fiber (reverse-engineer once 1–3 are understood).

*Build one, watch it contract, and you'll have understood more about "muscle" than a thousand papers.*
