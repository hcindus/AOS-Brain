---
name: blender-spaceship-alpha-maps
description: Build a huge-looking sci-fi spaceship in Blender using only primitive shapes + alpha maps (no hard-surface modeling). Use when asked to model a detailed spaceship/space scene fast, or to follow the Stefeliga Flavius "alpha maps" workflow.
---

# Blender Spaceship (Alpha-Map Technique)

**KPI:** A convincing, "huge" spaceship from primitives + textures — no hard-surface boolean/edge-loop modeling. (Inspired by Stefeliga Flavius / Paul Chadeisson.)

## Core Idea
The ship looks massively detailed, but it's all **primitive cylinders + image textures (alpha maps)**, not hard-surface modeling. Detail comes from stacking cylinders and letting alpha-cut panels cast shadows on each other. **Weakness:** looks bad close-up — this is a mid/far-distance + particle-fleet technique.

## Prerequisites / Textures
- **Panel detail textures:** generate with **JSplacement** (windmillart.net) — free hard-surface generator.
- **Spaceship base models:** TechLevel free pack (cgtrader) or `ship.shapewright.com` generator — for the low-poly fleet.
- **Project files:** stefeligaflavius.gumroad.com

## Process

### 1. Scene setup
1. Rename default cube + mesh (clean names for export to Unity etc.).
2. World: color → pitch black, **no HDRI**.
3. Add **Sun** lamp, rotate to fit scene, **Emission = 3000**.
4. Save.

### 2. Base cylinder (the hull)
1. Edit mode → delete cube, add **cylinder with 64 faces** (not 32).
2. Delete top + bottom faces.
3. Rotate 90° on X, scale **1.5 on Y**, smooth + enable **Auto Smooth**.
4. Duplicate the cylinder in edit mode, extrude the front edge outward (lock axis for even radius) to fake "thickness."
5. Connect extruded edge back to cylinder with **Bridge Edge Loops**.
6. Clean UV: add seams (edge select → mark seam), select faces (Alt+click), **Unwrap**. In UV editor, align first rectangle of each island to X/Y, then **Face Select → L (hover island) → Right-click → Follow Active Quads**. Repeat per island so texture doesn't curve/stretch.

### 3. Base material
1. One **Image Texture** → plug into **Color, Metallic, Roughness** (leave color space sRGB, or set Non-Color for metal/rough — experiment).
2. Add **Color Ramp** on grayscale for more control.
3. Select image node → **Ctrl+T** (Node Wrangler) for Mapping + Texture Coordinate. Adjust **Scale X/Y** to shrink detail.

### 4. Bump / normal
1. Add normal map → same Mapping values.
2. Add **Bump node** (normal → bump → normal input). Play with displacement value to kill flat/straight shadows.

### 5. Camera
- Add camera, position it, **Focal length = 150mm** (long-lens compression makes it feel huge).

### 6. Inner detail cylinders (the "ring" structure)
Repeat this pattern for each detail layer:
1. Add cylinder (**fewer faces** this time, e.g. 28 or 32), rotate 90° X, scale 1.5 Y, delete caps.
2. Scale Z/X slightly so it sits inside the hull.
3. **Ctrl+R** to add ~5 loop cuts, select all faces, **bevel** small amount → delete the (still-highlighted) beveled faces to get a lattice of rectangles.
4. Offset rectangles on Y for depth.
5. New material per mesh (name shaders after the mesh name).
6. Duplicate faces, scale Z/X, position Y → **add an alpha map** to these faces. Offset size/position so alpha panels **cast shadows** on faces below → fake intricacy.

### 7. Light/emissive cylinder (interior glow)
1. Add 32-face cylinder (same 90°X / 1.5Y / delete-caps recipe), fit between inner rectangles.
2. Texture = **light map with tiny square dots** → serve for both **Emission + Alpha** (looks like lit rooms/corridors).
3. Scale image to size dots; **crank Emission strength high**.
4. Duplicate it, scale inward, new material, assign — texture Color/Metal/Rough/Alpha/Bump, tune Mapping.

### 8. Exterior edges + details
1. Select hull outer edges (face select → Alt+click), assign a simple edge material.
2. Detail pass: duplicate inner circle (Shift+D), **Shift+H** to isolate, subdivide once, Alt+click edge → dissolve, bevel (Ctrl+B), **Ctrl+I invert** → delete → new material (easy re-select later).
3. **Alt+E → Extrude Faces Along Normals** to make protruding details; cull extras that look too busy.
4. Duplicate circle inward + assign another alpha texture.

### 9. Exterior hull shell
1. 64-face cylinder, 90°X, 1.5Y, delete caps, scale to encase everything.
2. Texture → **Color + Alpha only**; Ctrl+T mapping, increase texture size.
3. In UV editor rotate island **90°** to catch more detail.
4. Duplicate + scale to fully encase; add "panel above lines" texture for variety.

### 10. Antennas / poles (entrance)
1. Cylinder (same recipe), but **loop cut in half, delete one half**.
2. Place in front of ship, custom alpha material, rotate UV 90° for clean projection.
3. Repeat for a second rescaled cylinder.

### 11. Side details
1. Add a cube, reshape in edit mode, add more planes, assign existing hull materials.
2. Scale/position/rotate to taste — **unwrap everything** for clean projection.

### 12. Finishing pass
- Loop back over every mesh + material, tweak color/roughness/reflection/texture values until cohesive.

### 13. Fleet + particles (tiny ships)
1. Make/download low-poly spaceships (`ship.shapewright.com` or TechLevel cgtrader pack) → put into a **collection**.
2. Add **two planes facing each other** — one inside the ship, one outside.
3. Add a **particle system** to a plane, **Gravity = 0**, set the spaceship collection as the render object, tune size/number.

## Rules
- **Alpha maps do the detail, not geometry.** Never model panels by hand — texture + alpha-cut shadows.
- **Name every mesh and every shader**, and keep them matched (mesh "Hull" ↔ material "Hull") so edits stay sane.
- **Long lens (150mm) + pitch-black + strong sun** sells the scale.
- **This breaks close-up** — use for hero mid-shots + particle fleets, not macro detail shots.
- **Node Wrangler** required for Ctrl+T mapping; enable if not already.
- **UV discipline:** Follow Active Quads on every island, or textures curve/stretch.
