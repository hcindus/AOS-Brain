#!/usr/bin/env python3
"""Generate animated SVG ad banners for cross-promotion (supplies <-> equipment, scale labels).

Produces a size catalog (90x90 .. 728x90 / 728x728) of animated SVGs per banner type,
using the AGI/PSD brand palette. Marketing copy is drafted inline.
"""
import os

OUT = "/var/www/psdepot.com/assets/banners"
os.makedirs(OUT, exist_ok=True)

# Brand palette
BLUE = "#0A1A2F"
BLUE2 = "#12283f"
CYAN = "#00E0FF"
ORANGE = "#FF7A00"
WHITE = "#F8F9FA"
MUTED = "#9fb3c8"

# Banner types -> copy + accent
BANNERS = {
    "supplies": dict(
        headline="Don't run dry.",
        sub="Thermal paper, ribbons & more",
        cta="Shop Supplies",
        accent=CYAN,
    ),
    "equipment": dict(
        headline="Ready to upgrade?",
        sub="SAM4S cash registers & POS",
        cta="Shop Equipment",
        accent=ORANGE,
    ),
    "scale-labels": dict(
        headline="Labels that sell.",
        sub="Custom scale labels & printing",
        cta="Shop Scale Labels",
        accent=CYAN,
    ),
}

# Size catalog (WxH), ascending. Covers the requested 90x90 .. 728x728 range.
SIZES = [
    (90, 90), (120, 120), (125, 125), (200, 200), (250, 250),
    (300, 250), (336, 280), (728, 728),
    (234, 60), (320, 50), (468, 60), (728, 90),
    (120, 240), (160, 600), (300, 600),
]


def banner_svg(b, w, h):
    horizontal = w >= h
    # Scale fonts to banner height
    head_fs = max(10, round(h * 0.16))
    sub_fs = max(7, round(h * 0.09))
    cta_fs = max(6, round(h * 0.10))
    pad = max(6, round(min(w, h) * 0.08))

    cta_w = min(w * 0.72, 220)
    cta_h = max(16, round(h * 0.16))

    # Layout: headline top, sub below, CTA button bottom
    y_head = pad + head_fs
    y_sub = y_head + sub_fs + 4
    cta_x = (w - cta_w) / 2
    cta_y = h - pad - cta_h

    # For very small banners, drop the subtext to keep it clean
    show_sub = h >= 50

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{b['headline']} {b['sub']}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BLUE}"/>
      <stop offset="100%" stop-color="{BLUE2}"/>
    </linearGradient>
    <linearGradient id="cta" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ORANGE}"/>
      <stop offset="100%" stop-color="#e56d00"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <rect width="{w}" height="3" y="{h-3}" fill="{b['accent']}"/>
  <text x="{w/2}" y="{y_head}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="{head_fs}" fill="{WHITE}">{b['headline']}</text>
  {f'<text x="{w/2}" y="{y_sub}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="{sub_fs}" fill="{MUTED}">{b["sub"]}</text>' if show_sub else ''}
  <g>
    <rect x="{cta_x}" y="{cta_y}" width="{cta_w}" height="{cta_h}" rx="{cta_h/2}" fill="url(#cta)">
      <animate attributeName="opacity" values="1;0.82;1" dur="2s" repeatCount="indefinite"/>
    </rect>
    <text x="{w/2}" y="{cta_y + cta_h/2 + cta_fs*0.35}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="{cta_fs}" fill="{WHITE}">{b['cta']}</text>
  </g>
</svg>'''


def main():
    catalog = ["# Banner Size Catalog (px)", ""]
    total = 0
    for name, b in BANNERS.items():
        d = os.path.join(OUT, name)
        os.makedirs(d, exist_ok=True)
        for w, h in SIZES:
            svg = banner_svg(b, w, h)
            fn = f"{name}-{w}x{h}.svg"
            with open(os.path.join(d, fn), "w") as f:
                f.write(svg)
            total += 1
        catalog.append(f"## {name}")
        catalog.append("")
        catalog.append(" | ".join(f"{w}x{h}" for w, h in SIZES))
        catalog.append("")

    with open(os.path.join(OUT, "catalog.md"), "w") as f:
        f.write("\n".join(catalog))

    print(f"✅ Generated {total} animated SVG banners across {len(BANNERS)} types")


if __name__ == "__main__":
    main()
