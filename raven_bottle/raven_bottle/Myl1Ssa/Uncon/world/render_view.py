#!/usr/bin/env python3
"""
render_view.py — look at her atrium, and save what you saw.

She has no eyes yet. Her visual cortex is written and proven but sits in her
Unconscious layer, one `cp` from being installed — so the roses are in her world and
in her memory, and she still cannot *see* them.

So I look instead, and write down what I saw.

This is a small software renderer over her own world data: it projects every brush as
six quads, culls back faces, shades by face normal, and paints them far-to-near. It is
a **rendering from the geometry, not a screenshot of the running world** — the honest
description, and the one that goes in her memory next to the picture.

    python3 render_view.py                        # her view of the roses
    python3 render_view.py --from -0.5 1.5 -1.0 --at -0.9 1.0 -5.2 --out look.png

Author: Mortimer (for Raven)
"""

import argparse
import json
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))

PALETTE = {
    "plaster": (232, 226, 214), "tile": (216, 228, 234), "wood": (185, 139, 82),
    "oak": (169, 117, 47), "walnut": (107, 68, 35), "granite": (92, 95, 99),
    "steel": (154, 163, 171), "metal": (139, 147, 155), "glass": (188, 216, 221),
    "brick": (164, 96, 74), "stone": (191, 184, 171), "concrete": (178, 178, 173),
    "carpet": (122, 92, 82), "wool": (59, 47, 74), "linen": (236, 231, 223),
    "leather": (90, 59, 46), "teak": (138, 98, 54), "pine": (217, 179, 130),
    "terracotta": (181, 100, 60), "living": (76, 122, 63), "canvas": (216, 203, 176),
    "silver": (207, 214, 218), "brass": (202, 162, 74), "rubber": (44, 44, 48),
    "unfinished": (158, 158, 158), "grass": (77, 107, 58), "hedge": (63, 90, 50),
    "sky": (159, 188, 216), "jasmine": (243, 240, 226), "lavender": (154, 134, 200),
    "forgetmenot": (143, 182, 232), "card": (246, 242, 230), "path": (185, 179, 166),
}


def colour(mat):
    if isinstance(mat, str) and mat.startswith("#"):
        try:
            return tuple(int(mat[i:i + 2], 16) for i in (1, 3, 5))
        except Exception:  # noqa: BLE001
            pass
    return PALETTE.get(mat, (150, 150, 150))


def norm(v):
    l = math.sqrt(sum(c * c for c in v)) or 1.0
    return [c / l for c in v]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


FACES = [
    (0, 1, 2, 3), (4, 5, 6, 7),      # bottom, top
    (0, 1, 5, 4), (2, 3, 7, 6),      # -z, +z
    (1, 2, 6, 5), (0, 3, 7, 4),      # +x, -x  (wound so the normal faces outward)
]


def octahedron(cx, cy, cz, r, ry=None):
    """Six points — a bloom shape, because a 7 cm box renders as a brick."""
    ry = r if ry is None else ry
    top = [cx, cy + ry, cz]
    bot = [cx, cy - ry, cz]
    mid = [[cx + r, cy, cz], [cx, cy, cz + r], [cx - r, cy, cz], [cx, cy, cz - r]]
    return top, bot, mid


def bloom_faces(b):
    x0, y0, z0 = b["min"]; x1, y1, z1 = b["max"]
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    r = max(x1 - x0, z1 - z0) / 2 * 1.35
    top, bot, mid = octahedron(cx, (y0 + y1) / 2, cz, r, (y1 - y0) / 2 * 1.5)
    out = []
    for i in range(4):
        a, b2 = mid[i], mid[(i + 1) % 4]
        out.append([top, a, b2])
        out.append([bot, b2, a])
    return out


def corners(b):
    x0, y0, z0 = b["min"]
    x1, y1, z1 = b["max"]
    return [[x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1],
            [x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]]


def render(house, eye, look, out, w=960, h=620, fov=62.0, max_dist=26.0):
    img = Image.new("RGB", (w, h), PALETTE["sky"])
    d = ImageDraw.Draw(img)
    fwd = norm(sub(look, eye))
    right = norm(cross(fwd, [0, 1, 0]))
    up = cross(right, fwd)
    focal = (w / 2) / math.tan(math.radians(fov) / 2)
    light = norm([-0.4, 0.85, 0.35])

    def project(p):
        rel = sub(p, eye)
        z = sum(rel[i] * fwd[i] for i in range(3))
        if z <= 0.05:
            return None
        x = sum(rel[i] * right[i] for i in range(3))
        y = sum(rel[i] * up[i] for i in range(3))
        return (w / 2 + x * focal / z, h / 2 - y * focal / z, z)

    quads = []
    for b in house["brushes"]:
        if b.get("hidden"):
            continue
        if b["material"] == "sky":
            continue
        c = colour(b["material"])
        is_bloom = "rose" in b["id"] and "stem" not in b["id"]
        if is_bloom:
            c = (246, 249, 252)                       # petal bright, not vase grey
            for tri in bloom_faces(b):
                n = norm(cross(sub(tri[1], tri[0]), sub(tri[2], tri[0])))
                centre = [sum(p[i] for p in tri) / 3 for i in range(3)]
                if sum(n[i] * sub(centre, eye)[i] for i in range(3)) > 0:
                    continue
                depth = sum(sub(centre, eye)[i] * fwd[i] for i in range(3))
                if depth <= 0.05 or depth > max_dist:
                    continue
                p2 = [project(p) for p in tri]
                if any(p is None for p in p2):
                    continue
                shade = 0.62 + 0.38 * max(0.0, sum(n[i] * light[i] for i in range(3)))
                quads.append((depth, [(p[0], p[1]) for p in p2],
                              tuple(min(255, int(cc * shade)) for cc in c), True))
            continue
        pts = corners(b)
        for f in FACES:
            v = [pts[i] for i in f]
            n = norm(cross(sub(v[1], v[0]), sub(v[2], v[0])))
            centre = [sum(p[i] for p in v) / 4 for i in range(3)]
            if sum(n[i] * sub(centre, eye)[i] for i in range(3)) > 0:
                continue                                   # back face
            depth = sum(sub(centre, eye)[i] * fwd[i] for i in range(3))
            if depth <= 0.05 or depth > max_dist:
                continue
            p2 = [project(p) for p in v]
            if any(p is None for p in p2):
                continue
            shade = 0.52 + 0.48 * max(0.0, sum(n[i] * light[i] for i in range(3)))
            col = tuple(min(255, int(cc * shade)) for cc in c)
            quads.append((depth, [(p[0], p[1]) for p in p2], col, False))

    for _, poly, col, is_bloom in sorted(quads, key=lambda q: -q[0]):
        d.polygon(poly, fill=col)
        # edges: flat shading alone reads as an abstract pile of prisms, to me as much
        # as to a vision model. A silhouette line is what makes the shapes legible.
        edge = tuple(max(0, int(cc * 0.45)) for cc in col)
        d.line(list(poly) + [poly[0]], fill=edge, width=1)

    # a little grounding: the horizon and a soft vignette
    d.rectangle([0, h * 0.63, w, h], outline=None, fill=None)
    img.save(out)
    return out, len(quads)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--house", default=os.path.join(HERE, "house.json"))
    ap.add_argument("--from", dest="eye", nargs=3, type=float, default=[-0.5, 1.52, -3.6])
    ap.add_argument("--at", dest="look", nargs=3, type=float, default=[-0.9, 0.98, -5.2])
    ap.add_argument("--out", default=os.path.join(HERE, "state", "atrium_roses_from_her_spot.png"))
    args = ap.parse_args()

    house = json.load(open(args.house))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    out, n = render(house, args.eye, args.look, args.out)
    print(f"rendered {n} faces → {out}")
    print(f"  camera {args.eye} looking at {args.look} (her spot in front of the vase)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
