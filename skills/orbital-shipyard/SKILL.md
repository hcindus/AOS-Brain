---
name: orbital-shipyard
description: Locked visual + architectural setting for orbital shipyards / in-space construction scaffolds — the shared industrial backdrop for Kael Voss and any orbital-yard scenes. Includes the master setting anchor, zoned layout, design drivers, and ready-to-paste Grok image prompts. Use whenever generating, describing, or referencing orbital shipyard environments.
---

# Orbital Shipyard — Setting Regeneration

**Setting archetype:** An expandable, robotically-serviced industrial scaffold optimized for the physics of space — open where possible, modular and shielded where necessary, designed from the start for growth. Less "building" in the terrestrial sense, more a machine that grows itself.

Paste the **Master Setting Anchor** into every environment prompt and swap only the zone/camera tail. Never describe the yard from scratch — always point back here.

---

## Master Setting Anchor

Paste this block into every orbital-yard environment prompt:

> Photorealistic industrial orbital shipyard in space. Open truss spines and long central keels with attached robotic arms, docking ports, and solar arrays. Exposed gantries, cable runs, large empty assembly volumes, and empty corridors. Cool industrial tones — greys, blues, faded metallics. Muted overcast lighting from Earth albedo and reflected light, hard edges softened by grime. Lightweight composite panels (CFRP honeycomb), aluminum and titanium alloys, layered Whipple shielding. Keep the truss spine, robotic arms, docking ports, and cool grey-blue industrial palette exactly consistent across every image.

---

## Core Design Drivers (do not violate)

| Driver | Locked Detail |
|--------|---------------|
| Microgravity/vacuum | Open frameworks, very long keels, no self-weight support; fluids/tools/debris managed; EVA minimized → robotics + telepresence |
| Launch constraints | Everything arrives in fairing-sized (or Starship-class) pieces; robotic docking, berthing, welding, expansion |
| Environment | Radiation, thermal cycling, micrometeoroids/debris → Whipple multi-layer, composites, thicker walls; power = large solar arrays; heat rejection = radiators |
| Operations | Zero-g construction volumes separated from any artificial-gravity crew areas; automation + Earth teleoperation preferred (lower life-support cost) |

---

## Structural Hierarchy (render this, in order of prominence)

1. **Primary structure** — long truss spines, central beams, or open cylindrical barrels = the backbone (ISS Integrated Truss Structure scaled up). Linear central beams with attached functional units (STARFAB-style).
2. **Assembly volumes / "drydocks"** — open frameworks or large cylindrical voids (100–200 m diameter open barrels) for free assembly of long spacecraft. Enclosed options: rigid modules, welded plate structures (hexagonal / soccer-ball panels welded on-orbit), or thin-walled inflatable/partial-pressure membranes.
3. **Support modules** — habitats, storage, power systems, material processing (hoppers, printers, forges), logistics depots, control centers — attach modularly via standardized interfaces.
4. **Robotic infrastructure** — large external arms, internal manipulators, rail-based shuttles, free-flying drones (material movement, welding, inspection).
5. **Artificial gravity (when present)** — rotation: annular decks or stacked rings around a zero-g central void, counter-rotating elements for stability, or cylindrical/toroidal habitats. Construction zones stay non-rotating. Spin targets fractional-g to 1g at the rim.

---

## Zoned Layout (canonical)

| Zone | Location | Function |
|------|----------|----------|
| Zero-g forge / assembly | Central or underside | Keels + large structures |
| Industrial processing levels | Surrounding / stacked annular | Processing, robotics |
| Habitat / control | Separate (possibly spun) | Crew + ops |
| Power + thermal | Outer | Solar arrays, radiators |

---

## Visual Character (locked)

- **Lighting:** muted / overcast — Earth albedo, reflected light, or artificial sources; cool industrial tones (greys, blues, faded metallics); hard edges softened by grime.
- **Materials:** lightweight composites (CFRP honeycomb), aluminum/titanium alloys, advanced shielding layers.
- **Key enablers:** orbital 3D printing (additive manufacturing), in-space welding — growth beyond launched modules.
- **Overall mood:** industrial utility — exposed trusses, gantries, docking ports, cable runs, large empty volumes or corridors.

---

## Representative Concept Types (pick one per scene)

- **LEO high-tech yard** — automation, telepresence, protected assembly volumes near Earth (real-time control + logistics).
- **Welded large-volume platform** — launch plates, robotically assemble + weld into large pressurized/protected volumes that scale significantly (ThinkOrbital / NIAC "Construction Assembly Destination").
- **Cylindrical / ring hybrid** — open central barrel for ship assembly, rotating outer sections or stacked rings for gravity + support, processing bays and material hoppers.
- **Asteroid / free-flying rugged yard** — lower-cost, open or cave-based, minimal enclosure.
- **O'Neill / Stanford torus / Bernal sphere** — adapted for industrial (not pure habitat) use; modern modular station concepts.

---

## Ready-to-Paste Grok Prompts (self-contained)

- **The forge spine (hero wide)** — `Photorealistic wide shot of an open orbital shipyard assembly volume in space, a long truss spine and central keel with robotic arms and docking ports, exposed gantries and cable runs, a large empty cylindrical assembly void, cool grey-blue industrial tones, muted overcast light from Earth albedo, faded metallics, grime on hard edges.`
- **Empty corridor (Kael's walkway)** — `Photorealistic shot of a long empty corridor inside an orbital shipyard, exposed trusses and cable runs along the walls, thin composite paneling, cool grey industrial light, hard edges softened by grime, a single figure's perspective walking away.`
- **Welded plate volume** — `Photorealistic shot of a welded plate assembly volume in space, hexagonal and soccer-ball style panels joined with visible weld seams, robotic arms positioning a panel, cold industrial blue-grey lighting, faded metallic surfaces.`
- **Annular habitat ring** — `Photorealistic shot of a rotating annular habitat ring around a central zero-g void in an orbital shipyard, stacked industrial levels, exposed gantries, counter-rotating elements, cool muted light, grey and faded-blue palette.`
- **Material processing bay** — `Photorealistic shot of an orbital material processing bay, hoppers and orbital 3D printers and forges, robotic manipulators moving stock, exposed framework and cable runs, muted overcast industrial light, faded metallics.`
- **Solar array + radiator field** — `Photorealistic shot of large solar arrays and radiators on the outer surface of an orbital shipyard, truss structure, cool grey-blue industrial tones, muted reflected light from Earth albedo, hard edges.`

---

## Consistency Workflow

1. Generate the **forge spine (hero wide)** first — this becomes the master environment.
2. Feed that image back to Grok as a reference ("match this exact truss style, palette, and lighting") before other zones.
3. Do corridors, bays, and ring views from that locked environment.
4. Add the character (e.g. Kael Voss) last, referencing both the environment master and the character master face.

**Rule:** If a render drifts, fix the prompt against this sheet — never change the sheet to match a drifted render.
