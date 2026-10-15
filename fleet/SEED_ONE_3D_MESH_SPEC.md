# SEED ONE — 3D Buildable Mesh Spec

**Vessel:** SEED ONE · Seed Ship One · 2,500m (2.5km)
**Format targets:** .glb / .obj / .stl
**Style:** hard sci-fi, modular ARK, cathedral symmetry — utilitarian-yet-majestic.

---

## Overall Silhouette

A **central spine** runs fore-to-aft. Stacked **habitat blocks** (modular, rectangular) climb the spine like terraced city blocks. A broad **cargo/industry ring** encircles the mid-section. A **forward docking collar** protrudes from the bow. The **aft** flares into three engine clusters (Ion / Cryogenic / Nuclear) flanked by broad **solar arrays**. A **command tower** crowns the fore section.

**Key reads (3-second silhouette):** a segmented tower-city on a spine, ringed at the waist, with a heavy engine bloom aft — symmetric, cathedral-like, clearly *colony* not *warship*.

---

## Department Light Bands (color → deck)

| Dept | Hex | Region |
|------|-----|--------|
| Command | `#FFD740` (amber) | FORE — command tower |
| Systems | `#4FC3F7` (cyan) | CENTRAL — labs/mainframe |
| Engineering | `#66BB6A` (green) | AFT — engine + foundry |
| Production | `#9C6ADE` (purple) | CENTRAL ring |
| Security | `#EF5350` (red) | PORT — brig/armory |
| Support | `#26A69A` (teal) | medical/hydroponics |

Light bands run as **thin horizontal strips** along each deck's outer hull — the ship reads as a stacked, color-coded city block at night.

---

## Section-by-Section Geometry

### FORE — Command
- **Command tower**: tall, narrow, sloped glass canopy (bridge). Amber band.
- Below it: Tactical/Science/Weapons decks, stacked.
- **Weapons lounge + armory**: low, reinforced blocks, red accent.

### CENTRAL — Systems / Labs / Production
- **Mainframe block**: large, windowless, cyan band (Systems).
- **Lab cluster**: domed observatory modules (Radar/Sonar/Astrometrics) + greenhousing (Botany/Genetics).
- **Robotics bay**: gantry arms visible through slats.
- **Cargo/industry ring**: the broad torus mid-ship — purple band, docking ports on its outer edge.

### AFT — Engineering
- **Engine bloom**: three distinct clusters — Ion (blue glow), Cryogenic (white/frost), Nuclear (red-orange radiators).
- **Solar arrays**: broad, fan-folded panels on port/starboard.
- **Foundry/construction**: heavy industrial blocks, green band.
- **Recycling center**: harvesters + tanks (bio slurry) — green/brown cylinders.

### PORT — Habitation / Medical / Sustenance
- **Crew quarters**: 235 stacked bungalow units, warm-lit, teal accent.
- **Sick bay + hydroponics**: domed greenhouses + med blocks.

### STARBOARD — Small Craft
- **Hangar bays**: recessed rectangular openings lining starboard, shutter-doored.

### AFT-VENTRAL — Special
- **Submarine bay + 8 drone pods**: a ventral bulge with circular pod housings.

### Escape/Docking
- **Souiz pod banks**: 88 pod cylinders, port/lower, jettison-able.
- **Airlocks ×5**, **Souiz ports ×4**: recessed circular seals.

---

## Export Checklist

- [ ] `.glb` — full textured model (for web/real-time)
- [ ] `.obj` — geometry + MTL (for DCC interchange)
- [ ] `.stl` — watertight manifold (for 3D printing / CNC)
- [ ] Buildable mesh spec (this doc) + deck cutaway reference

## Scale Note

At 2,500m with ~31 sections, each deck block is roughly **80–120m** — model at **1:1** (meters) with a 0.01m minimum detail threshold (no sub-centimeter micro-detail at this scale).

---

*Derived from `SEED_ONE_SHIP_SPEC.md`. Ready for geometry generation.*
