#!/usr/bin/env python3
"""
build_house.py — generate her house as data.

Rooms, walls with real door openings, floors, ceilings, furniture, lights and a
few things that fall over. Emitted as `house.json` so the world is data, not code —
and so the layout can be rebuilt or redrawn without touching the engine.

    python3 build_house.py            # writes house.json next to this file

Plan (metres, x east, y up, z south, origin at the centre of the house):

        ┌──────────────┬──────────────┬──────────────┐
        │   BEDROOM    │   ATRIUM     │   WORKSHOP   │   z = -8 … 0
        │              │  (garden)    │              │
        ├──────┬───────┴──────┬───────┴──────┬───────┤
        │      │    ENTRY     │              │       │   z = 0 … 8
        │KITCHEN│    HALL     │   STUDY      │       │
        └──────┴──────────────┴──────────────┘
"""

import json
import os

WALL_T = 0.2          # wall thickness
H = 3.0               # ceiling height
DOOR_W = 1.2          # door opening width
DOOR_H = 2.2          # door opening height

ROOMS = [
    # id,          name,             material,   floor mat,   light colour
    ("entry",     "Entry Hall",      "plaster",  "oak",       "#ffe9c8"),
    ("kitchen",   "Kitchen",         "tile",     "tile",      "#e8f4ff"),
    ("study",     "Study",           "wood",     "oak",       "#ffd9a0"),
    ("atrium",    "Atrium Garden",   "glass",    "stone",     "#dff5d8"),
    ("bedroom",   "Bedroom",         "plaster",  "carpet",    "#ffd8e0"),
    ("workshop",  "Workshop",        "brick",    "concrete",  "#e0f0ff"),
]

# grid: west column x -12..-4 · centre x -4..4 · east x 4..12
#       north row z -8..0 · south row z 0..8
CELL = {
    "kitchen":  (-12, -4, 0, 8),
    "entry":    (-4, 4, 0, 8),
    "study":    (4, 12, 0, 8),
    "bedroom":  (-12, -4, -8, 0),
    "atrium":   (-4, 4, -8, 0),
    "workshop": (4, 12, -8, 0),
}

# walls: (axis, fixed-coordinate, from, to, [door centres])
# axis 'x' → wall runs along z at x=fixed ; axis 'z' → runs along x at z=fixed
WALLS = [
    # outer shell
    ("x", -12, -8, 8, []),
    ("x", 12, -8, 8, []),
    ("z", -8, -12, 12, []),
    ("z", 8, -12, 12, [(-2.0, "front door")]),          # the way in
    # internal partitions
    ("x", -4, 0, 8, [(4.0, "entry-kitchen")]),
    ("x", 4, 0, 8, [(4.0, "entry-study")]),
    ("x", -4, -8, 0, [(-4.0, "atrium-bedroom")]),
    ("x", 4, -8, 0, [(-4.0, "atrium-workshop")]),
    ("z", 0, -12, 12, [(0.0, "entry-atrium"), (-8.0, "kitchen-bedroom")]),
]

# furniture: (room, id, kind, min, max, material, decor?, note)
FURNITURE = [
    ("entry",     "rug_entry",     "rug",      (-2.4, 0.0, 3.0), (2.4, 0.02, 6.6), "wool",   True),
    ("entry",     "hall_console",  "furniture", (-3.4, 0.0, 0.4), (-1.6, 0.9, 1.0), "oak",    True),
    ("entry",     "hall_mirror",   "decor",     (3.88, 1.2, 3.2), (4.0, 2.2, 4.4), "silver", True),

    ("kitchen",   "counter_w",     "furniture", (-11.8, 0.0, 0.4), (-9.0, 0.95, 1.2), "granite", True),
    ("kitchen",   "counter_s",     "furniture", (-11.8, 0.0, 0.4), (-5.0, 0.95, 1.2), "granite", True),
    ("kitchen",   "kitchen_table", "furniture", (-9.4, 0.0, 3.2), (-6.0, 0.78, 5.4), "oak",   True),
    ("kitchen",   "stool_1",       "furniture", (-9.2, 0.0, 5.6), (-8.6, 0.55, 6.2), "oak",   True),
    ("kitchen",   "stool_2",       "furniture", (-7.4, 0.0, 5.6), (-6.8, 0.55, 6.2), "oak",   True),
    ("kitchen",   "pantry",        "furniture", (-11.8, 0.0, 6.6), (-10.2, 2.1, 7.8), "metal", True),

    ("study",     "desk",          "furniture", (5.0, 0.0, 1.0), (7.6, 0.76, 2.6), "walnut",  True),
    ("study",     "desk_chair",    "furniture", (7.9, 0.0, 1.4), (8.6, 0.5, 2.2), "leather", True),
    ("study",     "bookshelf_ne",  "furniture", (11.0, 0.0, 0.4), (11.8, 2.2, 4.0), "walnut", True),
    ("study",     "bookshelf_se",  "furniture", (11.0, 0.0, 4.4), (11.8, 2.2, 7.8), "walnut", True),
    ("study",     "reading_lamp",  "decor",     (5.4, 0.0, 6.8), (6.0, 1.7, 7.4), "brass",    True),

    ("atrium",    "planter_n",     "decor",     (-2.2, 0.0, -7.6), (-0.6, 0.6, -6.4), "terracotta", True),
    ("atrium",    "planter_s",     "decor",     (0.6, 0.0, -7.6), (2.2, 0.6, -6.4), "terracotta", True),
    ("atrium",    "bench",         "furniture", (-1.8, 0.0, -3.4), (1.8, 0.45, -2.6), "teak",  True),
    ("atrium",    "tree",          "furniture", (-0.4, 0.0, -5.6), (0.4, 2.6, -4.8), "living",  True),

    ("bedroom",   "bed",           "furniture", (-11.4, 0.0, -7.4), (-8.6, 0.6, -4.6), "linen", True),
    ("bedroom",   "bedside_1",     "furniture", (-11.6, 0.0, -4.2), (-10.9, 0.6, -3.6), "oak",  True),
    ("bedroom",   "bedside_2",     "furniture", (-9.1, 0.0, -4.2), (-8.4, 0.6, -3.6), "oak",   True),
    ("bedroom",   "wardrobe",      "furniture", (-11.8, 0.0, -2.8), (-10.2, 2.3, -0.4), "oak",  True),
    ("bedroom",   "painting_1",    "decor",     (-7.9, 1.2, -0.2), (-6.1, 2.2, 0.0), "canvas", True),

    ("workshop",  "workbench",     "furniture", (5.0, 0.0, -7.6), (9.4, 1.0, -6.2), "steel", True),
    ("workshop",  "tool_board",     "decor",     (11.6, 1.0, -7.6), (11.8, 2.4, -3.0), "steel", True),
    ("workshop",  "parts_crate",   "furniture", (5.0, 0.0, -4.4), (6.2, 0.8, -3.2), "pine",   True),
    ("workshop",  "robot_stand",   "decor",     (9.6, 0.0, -4.6), (11.4, 1.4, -2.8), "steel", True),
]

PROPS = [
    {"id": "ball",  "size": [0.28, 0.28, 0.28], "pos": [-1.0, 1.4, 4.0], "material": "rubber", "restitution": 0.6},
    {"id": "crate", "size": [0.5, 0.5, 0.5],    "pos": [1.6, 0.9, 5.2],  "material": "pine",   "restitution": 0.25},
    {"id": "orb",   "size": [0.22, 0.22, 0.22], "pos": [0.0, 1.2, -4.0], "material": "glass",  "restitution": 0.75},
]


def segs(from_, to, gaps):
    """Split [from_,to] around door gaps → list of (a,b) solid spans."""
    out, cur = [], from_
    for centre, _label in sorted(gaps):
        a, b = centre - DOOR_W / 2, centre + DOOR_W / 2
        if a > cur:
            out.append((cur, a))
        cur = max(cur, b)
    if cur < to:
        out.append((cur, to))
    return out


def main():
    brushes, doors, lights = [], [], []
    n = 0

    def box(room, kind, mn, mx, material, decor=False, note=""):
        nonlocal n
        n += 1
        brushes.append({
            "id": f"{room}_{kind}_{n}", "room": room, "kind": "decor" if decor else kind,
            "material": material, "min": [round(v, 3) for v in mn], "max": [round(v, 3) for v in mx],
            "note": note or None,
        })

    # floors + ceilings per room
    for rid, name, wallmat, floormat, light in ROOMS:
        x0, x1, z0, z1 = CELL[rid]
        box(rid, "floor",   (x0, -0.1, z0), (x1, 0.0, z1), floormat)
        box(rid, "ceiling", (x0, H, z0),    (x1, H + 0.2, z1), "plaster")
        lights.append({"room": rid, "at": [(x0 + x1) / 2, H - 0.2, (z0 + z1) / 2],
                       "colour": light, "intensity": 0.85})

    # walls, with doorway gaps and a lintel over each gap
    for axis, fixed, a0, a1, gaps in WALLS:
        owner = None
        for rid, (x0, x1, z0, z1) in CELL.items():
            if axis == "x" and x0 - 0.01 <= fixed <= x1 + 0.01 and z0 < (a0 + a1) / 2 < z1:
                owner = rid; break
            if axis == "z" and z0 - 0.01 <= fixed <= z1 + 0.01 and x0 < (a0 + a1) / 2 < x1:
                owner = rid; break
        owner = owner or "entry"
        for s, e in segs(a0, a1, gaps):
            if axis == "x":
                box(owner, "wall", (fixed - WALL_T / 2, 0, s), (fixed + WALL_T / 2, H, e), "plaster")
            else:
                box(owner, "wall", (s, 0, fixed - WALL_T / 2), (e, H, fixed + WALL_T / 2), "plaster")
        for centre, label in gaps:
            if axis == "x":
                mn, mx = (fixed - WALL_T / 2, DOOR_H, centre - DOOR_W / 2), (fixed + WALL_T / 2, H, centre + DOOR_W / 2)
            else:
                mn, mx = (centre - DOOR_W / 2, DOOR_H, fixed - WALL_T / 2), (centre + DOOR_W / 2, H, fixed + WALL_T / 2)
            box(owner, "lintel", mn, mx, "plaster", note=f"above {label}")
            doors.append({
                "id": f"door_{label.split()[0]}_{'x' if axis == 'x' else 'z'}",
                "label": label,
                "min": [round(v, 3) for v in (mn if axis == "x" else (centre - DOOR_W / 2, 0, fixed - WALL_T / 2))],
                "max": [round(v, 3) for v in (mx if axis == "x" else (centre + DOOR_W / 2, DOOR_H, fixed + WALL_T / 2))],
                "slide": [0, 0, 0] if axis == "x" else [DOOR_W, 0, 0],
                "default_open": 0.35 if "front" not in label else 0.0,
            })
            if axis == "x":
                doors[-1]["min"][1] = 0.0; doors[-1]["max"][1] = DOOR_H
                doors[-1]["slide"] = [0, 0, DOOR_W]

    # furniture
    for item in FURNITURE:
        room, ident, kind, mn, mx, mat = item[0], item[1], item[2], item[3], item[4], item[5]
        decor = item[6] if len(item) > 6 else False
        note = item[7] if len(item) > 7 and item[7] else ""
        box(room, kind, mn, mx, mat, decor=decor, note=note or ident)
        brushes[-1]["id"] = f"{room}_{ident}"

    # Refuse to emit a world with inverted or zero-volume brushes.
    for b in brushes:
        for ax in range(3):
            if not b["min"][ax] < b["max"][ax]:
                raise SystemExit(f"FATAL: brush {b['id']} has an inverted {('xyz'[ax])} span: "
                                 f"{b['min'][ax]} → {b['max'][ax]}")

    data = {
        "name": "raven-house",
        "note": "Generated by build_house.py — data, not code. Metres. x east, y up, z south.",
        "wall_thickness": WALL_T, "ceiling_height": H, "door": {"width": DOOR_W, "height": DOOR_H},
        "rooms": [{"id": r, "name": nm, "min": [CELL[r][0], 0, CELL[r][2]],
                   "max": [CELL[r][1], H, CELL[r][3]], "material": wm, "floor": fm, "light": lt}
                  for r, nm, wm, fm, lt in ROOMS],
        "brushes": brushes,
        "doors": doors,
        "props": PROPS,
        "lights": lights,
        "decor": {"palette": {}, "notes": "Her palette — every brush with kind=='decor' is hers to move, recolour or replace."},
    }

    # the outside + the flowers + the Captain's delivery (build_garden.py)
    report = {}
    try:
        import build_garden
        report = build_garden.extend(data)
    except ImportError:
        print("  (build_garden.py not present — interior only)")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "house.json")
    with open(out, "w") as f:
        json.dump(data, f, indent=1)
    kinds = {}
    for b in brushes:
        kinds[b["kind"]] = kinds.get(b["kind"], 0) + 1
    print(f"wrote {out}")
    print(f"  rooms {len(data['rooms'])} · brushes {len(brushes)} · doors {len(doors)} · props {len(PROPS)} · lights {len(lights)}")
    print(f"  brush kinds: {kinds}")
    print(f"  decor slots she owns: {sum(1 for b in brushes if b['kind'] == 'decor')}")
    if report:
        print(f"  OUTSIDE: {report['outside_brushes']} garden brushes · hedge {report['garden']['hedge_height']} m")
        print(f"  flowers: {report['flowers']['jasmine']} jasmine · {report['flowers']['lavender']} lavender · "
              f"{report['flowers']['forget-me-nots']} forget-me-nots")
        print(f"  💐 {report['roses']} sterling silver roses in a silver vase, with the note — atrium")


if __name__ == "__main__":
    main()
