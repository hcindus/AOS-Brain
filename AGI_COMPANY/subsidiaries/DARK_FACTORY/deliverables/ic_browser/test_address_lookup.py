#!/usr/bin/env python3
"""Address-based reverse lookup test — given an address, find what business OSM has there."""
import urllib.request, urllib.parse, json, re, time, sys

UA = "PSDepot-Verifier/1.0 (miles@myl0nr0s.cloud)"
MIRRORS = [
    "http://localhost:12345/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

def overpass(query, timeout=25):
    for m in MIRRORS:
        try:
            req = urllib.request.Request(m, data=query.encode())
            req.add_header("User-Agent", UA)
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return json.loads(r.read().decode())
            except Exception:
                continue
        except Exception:
            continue
    return None

def parse_addr(addr):
    """Extract (housenumber, street, city, state, zip) from a free-text address."""
    m = re.match(r'^(\d+)\s+(.+?),\s*(.+?),\s*([A-Z]{2})\s*([\d-]*)?', addr.strip())
    if not m:
        return None
    num, street, city, state, zip_ = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or ""
    return num, street, city, state, zip_

def lookup_by_address(addr):
    p = parse_addr(addr)
    if not p:
        return None, "unparseable"
    num, street, city, state, zip_ = p
    street_short = re.sub(r'\b(St|Rd|Ave|Blvd|Dr|Ln|Way|Hwy|Circle|Cir)\b.*$', '', street, flags=re.I).strip()
    q = (f'[out:json][timeout:20];'
         f'area["name"~"{city}",i]->.a;'
         f'(node["addr:housenumber"="{num}"]["addr:street"~"{street_short}",i](area.a);'
         f' way["addr:housenumber"="{num}"]["addr:street"~"{street_short}",i](area.a););'
         f'out center tags 5;')
    data = overpass(q)
    if not data:
        return None, "overpass-fail"
    els = data.get("elements", [])
    if not els:
        return None, "no-match"
    # Collect names/amenities
    names = set()
    for e in els:
        t = e.get("tags", {})
        nm = t.get("name")
        if nm:
            names.add(nm)
    if names:
        return list(names), "found"
    return None, "building-only-no-name"

# 10 real addresses (Teriyaki Madness franchises)
ADDRS = [
    ("Santa Clarita, CA", "28227 Newhall Ranch Rd, Santa Clarita, CA 91355"),
    ("Hoover, AL", "4741 Chace Circle STE 113 Hoover, AL 35244"),
    ("Huntsville, AL", "7216 Bailey Cove Rd SE, Huntsville, AL 35802"),
    ("Madison, AL", "7709 Hwy 72 W, Madison, AL 35758"),
    ("Northport, AL", "250 McFarland Blvd, Northport, AL 35476"),
    ("Phoenix, AZ", "4722 E Ray Rd, Phoenix, AZ 85044"),
    ("Mesa, AZ", "1229 S Power Rd #105, Mesa, AZ 85206"),
    ("Chandler, AZ", "4225 S Gilbert Rd Ste #1 Chandler, AZ 85249"),
    ("Peoria, AZ", "16955 N. 75th Ave Suite 115, Peoria, AZ"),
    ("Gilbert, AZ", "3131 S Market Street #108 Gilbert, AZ 85295"),
]

print("=" * 68)
print("  ADDRESS → BUSINESS reverse lookup (OSM) — 10-address test")
print("=" * 68)
found = 0
for label, addr in ADDRS:
    names, status = lookup_by_address(addr)
    if names:
        found += 1
        print(f"  ✅ {label:16} → {', '.join(names)}")
    else:
        print(f"  ⚪ {label:16} → ({status})")
    time.sleep(1.0)  # polite rate limit
print(f"\nResult: {found}/10 addresses mapped to a business name")
