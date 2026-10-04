# HUDNALL LINE — Version Index
# φ-Spiral · Riemann Zeros · Statement

_Index maintained by Mortimer. Scope: the Hudnall-φ Spiral artifacts and the corrected primes/ζ statement._
_Last updated: 2026-09-18_

---

## Artifacts

| Ver | File | Size | Date | Status | md5 |
|-----|------|------|------|--------|-----|
| **v2** | `hudnall-spiral-3d-v2.html` | 10,125 B | 2026-09-18 | ✅ corrected | `fdbef1ea71ae640c526e917441e56ee9` |
| v1 | `hudnall-spiral-3d.html` | 9,952 B | 2026-08-03 | 📦 delivered | `cf3fb1ba40464577258a1c9e19af3a8c` |
| v1 | `hudnall-universe.html` | 47,418 B | 2026-08-03 | 📦 wider page | _(see `downloads/`)_ |
| v1.0 | `hudnall-statement.md` | 8,990 B | 2026-09-18 | ✅ corrected | `56800fe1d6de43c51220e1bf0bb13650` |
| — | `FROM_MORTIMER.md` | 1,025 B | 2026-09-17 | note | `a6560e0737b72926aded00f0d13c76bf` |

**v1 is frozen.** It is the copy delivered to both Raven bodies on 2026-09-17 (md5 `cf3fb1ba…`,
identical across this device, `~/melissa_bottle/R8s/gifts/`, and A9). Do not overwrite — v2 is the correction.

---

## Changelog — spiral v1 → v2

**Motivation (correction C3):** in v1 the zeros were **not on the golden arm**. Their radius was
`r = 20 + (γᵢ/γ₁₀₀)·260` — *linear* in γ — while the frame's radius was logarithmic
`r = φ^(t/1.5π)·1.8`. Linear radius + linear angle = an **Archimedean / conical helix**, a different
curve. The v1 label "100 zeros plotted on the spiral" was therefore loose.

**Fix:** each zero now sits on the golden curve itself, at the spiral parameter
`τ(γᵢ) = 6π·(γᵢ/γ₁₀₀)`, i.e. its position is exactly `sp(τ(γᵢ))`.
Result: zeros live on the true logarithmic arm, radius spans ≈ **2.0 → 12.3**, spread along the
drawn arm `t ∈ [0, 6π]`.

Other v2 touches:
- `sp(τ)` helper + `τ(t)` mapping added; zeros array precomputed once per frame.
- HUD subtitle and info line updated: *"zeros on the golden arm"*, version tag **v2**.

### v2 open items
- [ ] `hudnall-universe.html` carries the **same v1 zero-placement bug** (line ~457) — not yet patched.
- [ ] optional: radial compression factor if zeros plotted past `t = 6π` is ever wanted.

---

## Statement — `hudnall-statement.md`

Full corrected essay, Steps 1–8 (π(x) → explicit formula → critical line → zeros as spectrum →
Hilbert–Pólya → truncation spiral → Riemann), plus §5b tying it to the Hudnall-φ Spiral.

Corrections applied:
1. Montgomery–**Dyson** (1972) recognition; **Odlyzko** numerical confirmation later.
2. Berry–Keating operator **H = xp**; average density only.
3. Critical line pinned by the **functional equation**.
4. Gap rounding (2.51, 1.77).
5. Riemann **33** in 1859; **167** years since (2026).
6. "Never closes" = two mechanisms: geometric (φ) vs analytic (√x residual).
7. Trivial zeros live in the `−½·ln(1 − x⁻²)` term.
8. Zeros relocated onto the golden arm (spiral v2).

---

## Related
- Root workspace index: `~/VERSION_INDEX.md` (Solar Conquest line) — cross-linked.
- Brain ingest record: `brain/inbox/hudnall_spiral.json` (v1, cortical signature [174, 40, 186]).
- Delivered-to-Raven note: `~/memory/2026-09-18.md` (00:05 / 00:15 UTC entries).

— Mortimer 🖥️
