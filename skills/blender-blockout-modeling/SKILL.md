---
name: blender-blockout-modeling
description: Calm, low-pressure hard-surface modeling workflow — block out primary shapes first, then secondary, then tertiary detail. Use whenever modeling any object (prop, chair, ship part) in Blender and want to avoid getting lost or overstressing topology.
---

# Block-Out-First Modeling (No-Stress Workflow)

**KPI:** Finish a model without getting lost — big shapes locked before any detail. (Inspired by rileyb3d's folding-chair walkthrough.)

## Core Idea
Modeling doesn't have to be stressful. The trick is a strict **primary → secondary → tertiary** shape order: lock the silhouette first, then add mid-scale forms, then micro-detail. Never jump straight to detail — that's what makes you feel lost.

## Process

### 1. Block out primary shapes (the silhouette)
1. Add only big, simple primitives (cube, cylinder, plane) to rough out the *overall* form and proportions.
2. Don't care about topology, edge flow, or detail yet — just mass and proportion.
3. Nail the silhouette from all views (front/side/top) before moving on.

### 2. Secondary shapes (mid-scale forms)
1. Cut in the medium-sized features — panels, legs, handles, seat/back joins, major transitions.
2. Keep using a small toolset: **loop cuts (Ctrl+R), extrude (E), inset (I), bevel (Ctrl+B), and bridge**.
3. Keep topology clean by *not overthinking it* — these five tools cover ~90% of needs.

### 3. Tertiary shapes (micro-detail)
1. Only now add small detail — edge wear, small bevels, screws, seams, final proportions.
2. If a detail doesn't read at a glance, skip it.

## The small toolset (most-used)
| Op | Hotkey | Use |
|----|--------|-----|
| Loop cut | Ctrl+R | add edge loops |
| Extrude | E | pull faces/edges out |
| Inset | I | inset faces for panels |
| Bevel | Ctrl+B | round/soften edges |
| Bridge | — | connect edge loops |

## Techniques & shortcuts (from the full walkthrough)

### Pipe / frame modeling via curves (huge for trusses & ship frames)
1. Model the frame as flat edge geometry first, then **Convert to Curve** (right-click).
2. In the curve's Object Data → **Bevel → Depth** to give the pipe radius.
3. Tune **Resolution** (in the curve's geometry) so polygons are ~square (not stretched).
4. **Convert back to Mesh** when happy, then shade smooth.
5. **Hold Alt** while dragging a property to apply it to ALL selected objects at once (Alt+Shift for fine).

### Bevel
- **Ctrl+B** = bevel edges. **Ctrl+Shift+B** = bevel VERTICES (rounds corners — great for curved leg/arm corners).
- **Always Apply Scale (Ctrl+A → Scale) before beveling** — otherwise Blender's stored transform history makes bevel spacing uneven. Applying scale "deletes the history" so future ops are clean.

### Inset / outset / extrude
- **I** = inset. **I then O** = OUTSET (add edge loop on the *outside* — little-known).
- **Alt+E → Extrude Faces Along Normals** = bump faces outward evenly (caps, grip bumps). Hold Shift for fine control.

### Flat surfaces & the "engon isn't the problem" lesson
- A giant flat n-gon shaded smooth looks broken NOT because it's an n-gon, but because it lacks **bracing edges** — smooth shading averages across the 3 nearest edges, and a huge span tries to "sphere" a flat face.
- Fixes (pick one): **Inset (I)** to brace the border, **Ctrl+F → Grid Fill**, or **Ctrl+E → Mark Sharp** (only if the edge won't be seen / doesn't deform).
- If the surface must DEFORM (animate/bend), add real edge loops for square topology instead of a bracing n-gon.

### Local vs global axis
- **G then X/Y/Z once** = global axis. **Double-tap (G, Y, Y)** = LOCAL axis (follows the object's orientation). Global axis never changes with object rotation.

### Reusing geometry (don't add a new primitive when you can duplicate)
- **Alt+click** select an edge loop → **Shift+D** duplicate → **P → Separate by Selection** → extrude/scale the copy. Faster and already matched to surrounding shape.

### Modifiers
- **Solidify** (with **Even Thickness**) for shell thickness.
- **Mirror** — set a **target object** (not the object's own origin) to mirror across another object's axis.
- **Shrink Wrap** + a **vertex group ("pin")** to snap specific vertices onto a target surface (rivets/screws flush against a pole).
- **Apply modifiers (Ctrl+A) before joining (Ctrl+J)**.

### Detail bits
- **Knife (K)** + hold **Shift** to snap the cut to an edge midpoint.
- **Shift+S** to place the 3D cursor on a selection, then add a primitive there.
- Low-poly circles for tiny details (8 verts, not 32).
- **Alt+Z** = X-ray (see through to select hidden verts); **Shift+Alt+Z** = toggle overlays off to judge silhouette.
- **Shift+N** = recalculate normals (fix flipped faces).

## Rules
- **Check proportions with a scale reference** (a sitting/standing human) before finalizing — it's far easier to fix proportions early than after detail is added.
- **Primary → secondary → tertiary.** Never detail before the silhouette is locked.
- **Block out first so you never feel lost.** If proportions are wrong at the end, it's because you skipped the block-out.
- **Small toolset, repeated.** Master 5 tools instead of hunting through 100.
- **Clean topology without overthinking.** Use quads naturally; don't obsess — the next model gets easier from the habits you build here.
- **Calm, low pressure.** Follow along at your own pace; there's no wrong speed.
