# Space Game Asset Library — MANIFEST

**Created:** 2026-10-31 (Captain, Hcindus)
**Source:** Hi3D renders dropped via Telegram (2026-10-30 batch)
**Purpose:** Next-generation game assets for the space game (spacebattle / orbital-shipyard universe). These replace the earlier geometric-placeholder ships with detailed fighters, mechs, alien enemies, vehicles, and pods.

**Design language:** cohesive "gloss-black / silver / white-armor" — premium, quiet, expensive sci-fi. Range from pure machine (walkers, pods, hover vehicles) → bio-mechanical (biped).

---

## Asset Inventory (16 renders)

### Mechs (2)
| File | Description |
|------|-------------|
| `mechs/white-armored-humanoid.jpg` | Sleek white armored humanoid robot, clean studio backdrop |
| `mechs/six-legged-walker.jpg` | White/grey robotic walker on six jointed mechanical legs |

### Alien Enemies (1)
| File | Description |
|------|-------------|
| `alien-enemies/bio-mech-biped.jpg` | Bipedal robot blending organic + mechanical features (white/gray) |

### Fighters (4)
| File | Description |
|------|-------------|
| `fighters/silver-jet-flying-car.jpg` | Silver jet-powered flying car (collage) |
| `fighters/black-spacecraft-mountains.jpg` | Glossy black spacecraft hovering over mountainous landscape |
| `fighters/flying-pod-gray.jpg` | Sleek flying pod, glossy black, neutral gray bg |
| `fighters/black-flying-vehicle.jpg` | Black flying vehicle hovering over minimalist gray floor |

### Vehicles (4)
| File | Description |
|------|-------------|
| `vehicles/black-futuristic-vehicle-4views.jpg` | Black futuristic vehicle, 4 views |
| `vehicles/wheel-less-hover-vehicle.jpg` | Wheel-less hover vehicle, white bg |
| `vehicles/dark-backdrop-concept-vehicle.jpg` | Aerodynamic concept vehicle, dark minimalist backdrop |
| `vehicles/pod-city-plaza-4seats.jpg` | Pod hovering over misty sci-fi city plaza; glass canopy, 4 luxury bucket seats, LED strips |

### Pods (4)
| File | Description |
|------|-------------|
| `pods/black-gloss-transport-pod.jpg` | High-gloss black transport pod, multi-angle |
| `pods/black-pod-front-side.jpg` | Black pod, front + side profiles |
| `pods/pod-glass-viewport.jpg` | Glossy black pod w/ silver accents, large glass viewport |
| `pods/teardrop-pod.jpg` | Aerodynamic teardrop-shaped pod |

### Machinery (1)
| File | Description |
|------|-------------|
| `machinery/black-silver-machinery-sheet.jpg` | Black + silver machinery concept sheet, multiple profiles |

---

## Status
- [ ] Preserved (this library) ✅
- [ ] Next: generate 3D GLBs from these via Hi3D REST API (`hi3d_client.py`, image→3D)
- [ ] Next: optimize + build viewer pages (like existing `mech.html`, `cyborg.html`, fleet pages)
- [ ] Next: wire into spacebattle game as actual in-game models

**Note:** original Hi3D source files remain in `/root/.openclaw/media/inbound/` (UUID-named). This library is the canonical, human-readable copy.
