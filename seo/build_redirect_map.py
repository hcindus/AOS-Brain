#!/usr/bin/env python3
"""
Complete geo-page -> region redirect map for psdepot.com.
Classifies every thin geo landing page on the live site into its 5-region hub,
so the doorway pages can 301 into strong regional landing pages.

Outputs:
  redirect_map.json   (old slug -> region slug)
  redirects.nginx     (301 rules)
  summary counts
"""

import os
import json

# 50 states + DC -> region
STATE_TO_REGION = {
    "alabama": "south", "alaska": "northwest", "arizona": "west",
    "arkansas": "south", "california": "west", "colorado": "west",
    "connecticut": "east-coast", "delaware": "east-coast", "florida": "south",
    "georgia": "south", "hawaii": "west", "idaho": "northwest",
    "illinois": "midwest", "indiana": "midwest", "iowa": "midwest",
    "kansas": "midwest", "kentucky": "south", "louisiana": "south",
    "maine": "east-coast", "maryland": "east-coast", "massachusetts": "east-coast",
    "michigan": "midwest", "minnesota": "midwest", "mississippi": "south",
    "missouri": "midwest", "montana": "northwest", "nebraska": "midwest",
    "nevada": "west", "new-hampshire": "east-coast", "new-jersey": "east-coast",
    "new-mexico": "west", "new-york": "east-coast", "north-carolina": "south",
    "north-dakota": "midwest", "ohio": "midwest", "oklahoma": "south",
    "oregon": "northwest", "pennsylvania": "east-coast", "rhode-island": "east-coast",
    "south-carolina": "south", "south-dakota": "midwest", "tennessee": "south",
    "texas": "south", "utah": "west", "vermont": "east-coast",
    "virginia": "south", "washington": "northwest", "west-virginia": "south",
    "wisconsin": "midwest", "wyoming": "northwest",
}

# Standalone city pages -> region (via their state)
CITY_TO_REGION = {
    "atlanta": "south", "austin": "south", "boston": "east-coast",
    "chicago": "midwest", "dallas": "south", "denver": "west",
    "detroit": "midwest", "houston": "south", "las-vegas": "west",
    "los-angeles": "west", "miami": "south", "new-orleans": "south",
    "philadelphia": "east-coast", "phoenix": "west", "portland": "northwest",
    "san-diego": "west", "san-francisco": "west", "seattle": "northwest",
    "baltimore": "east-coast", "charlotte": "south", "columbus": "midwest",
    "indianapolis": "midwest", "jacksonville": "south", "milwaukee": "midwest",
    "minneapolis": "midwest", "nashville": "south", "oklahoma-city": "south",
    "omaha": "midwest", "sacramento": "west", "tucson": "west",
    "tulsa": "south", "albuquerque": "west", "el-paso": "south",
    "fort-worth": "south", "fresno": "west", "bakersfield": "west",
    "arlington": "south", "raleigh": "south", "wichita": "midwest",
    "colorado-springs": "west", "virginia-beach": "south",
    # -- the "remaining 15" --
    "san-antonio": "south", "san-jose": "west", "oakland": "west",
    "mesa": "west", "louisville": "south", "new-york-city": "east-coast",
    "anaheim-pos-supplies": "west", "bay-area-pos-supplies": "west",
    "long-beach-pos-supplies": "west", "oakland-pos-supplies": "west",
    "san-jose-pos-supplies": "west", "washington-dc": "east-coast",
}

# Canadian provinces/territories -> pending (flag)
CANADA = ["alberta", "british-columbia", "manitoba", "new-brunswick",
          "newfoundland-labrador", "northwest-territories", "nova-scotia",
          "nunavut", "ontario", "prince-edward-island", "quebec",
          "saskatchewan", "yukon"]

# Mexican states -> pending (flag)
MEXICO = ["aguascalientes", "baja-california", "baja-california-sur", "campeche",
          "chiapas", "chihuahua", "coahuila", "colima", "durango", "guanajuato",
          "guerrero", "hidalgo", "jalisco", "michoacan", "morelos", "nayarit",
          "nuevo-leon", "oaxaca", "puebla", "queretaro", "quintana-roo",
          "sinaloa", "sonora", "tabasco", "tamaulipas", "tlaxcala", "veracruz",
          "yucatan", "zacatecas", "ciudad-de-mexico"]

# Pages that are geo-adjacent but NOT doorway pages (leave alone)
NOT_GEO = {"locations", "testimonials", "security", "resale-licenses",
           "return-policy", "pos-software", "sam4pos", "self-checkout",
           "electronic-shelf-labels", "independent-grocer", "cream", "cream2",
           "cream3", "reggiestarr", "mountain-mikes-locations",
           "teriyaki-madness-locations", "pollo_asados_demo", "index", "about",
           "contact", "booking", "checkout", "privacy", "terms", "faq",
           "sitemap", "404", "business-cards", "cart-test", "clear-cart",
           "site-tree"}


def classify(slug):
    if slug in STATE_TO_REGION:
        return STATE_TO_REGION[slug]
    if slug in CITY_TO_REGION:
        return CITY_TO_REGION[slug]
    if slug in CANADA:
        return "canada-mexico"
    if slug in MEXICO:
        return "canada-mexico"
    if slug in NOT_GEO:
        return None           # not a geo doorway page
    # language variants and misc -> skip
    return "skip"


def main():
    site = "/var/www/psdepot.com"
    redirects = {}
    counts = {}

    for fn in sorted(os.listdir(site)):
        if not fn.endswith(".html"):
            continue
        slug = fn[:-5]
        region = classify(slug)
        if region is None:
            continue
        redirects[slug] = region
        counts[region] = counts.get(region, 0) + 1

    out_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(out_dir, "redirect_map.json"), "w") as f:
        json.dump(redirects, f, indent=2)

    # nginx rules (US regions only -> real pages; canada/mexico/skip flagged)
    nginx = []
    for slug, region in sorted(redirects.items()):
        target = region if region in ("northwest", "west", "midwest", "south", "east-coast", "canada-mexico") else None
        if target:
            nginx.append(f"rewrite ^/{slug}.html$ /{target}.html permanent;")

    with open(os.path.join(out_dir, "redirects.nginx"), "w") as f:
        f.write("\n".join(nginx) + "\n")

    print("=== Redirect map summary ===")
    for k in sorted(counts, key=lambda x: -counts[x]):
        print(f"  {k:12s} {counts[k]:3d}")
    print(f"\n  TOTAL mapped: {len(redirects)}")
    us = sum(v for k, v in counts.items() if k in ("northwest", "west", "midwest", "south", "east-coast"))
    print(f"  -> US regions (301-ready): {us}")
    print(f"  -> canada/mexico (pending): {counts.get('canada',0) + counts.get('mexico',0)}")
    print(f"  -> skip (lang variants etc.): {counts.get('skip',0)}")
    print(f"\n  Wrote redirect_map.json + redirects.nginx -> {out_dir}")


if __name__ == "__main__":
    main()
