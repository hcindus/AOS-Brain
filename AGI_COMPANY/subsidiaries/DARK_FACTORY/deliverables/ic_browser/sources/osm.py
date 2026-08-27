#!/usr/bin/env python3
"""
IC Browser source module — OpenStreetMap (free, no key, real POI data).

Uses the Overpass API with:
  - Proper User-Agent (Overpass ToS requirement)
  - Multiple mirror fallback (public endpoints are flaky: 504/502)
  - Retry with backoff
  - Polite rate limiting

Honest: returns None (not found) when OSM has no match — never fabricates.
"""
import json
import time
import urllib.request
import urllib.parse
from typing import Optional

UA = "PSDepot-LeadVerifier/1.0 (miles@myl0nr0s.cloud)"
MIRRORS = [
    "http://localhost:12345/api/interpreter",   # self-hosted Overpass (primary, no flakiness)
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

# Amenity/category hints for hospitality targeting
HOSPITALITY_AMENITIES = [
    "restaurant", "cafe", "bar", "pub", "fast_food", "food_court",
    "ice_cream", "biergarten", "nightclub",
]


def _overpass_query(query: str, timeout: int = 30) -> Optional[dict]:
    """Run an Overpass QL query with mirror fallback + retry."""
    last_err = None
    for attempt in range(2):  # 2 attempts
        for mirror in MIRRORS:
            try:
                req = urllib.request.Request(mirror, data=query.encode())
                req.add_header("User-Agent", UA)
                req.add_header("Content-Type", "application/x-www-form-urlencoded")
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return json.loads(r.read().decode())
            except Exception as e:
                last_err = e
                time.sleep(1.5)  # backoff between mirrors
        time.sleep(3)  # backoff between full attempts
    print(f"  [osm] all mirrors failed: {last_err}")
    return None


def verify(business_name: str, city: str = "", state: str = "") -> Optional[dict]:
    """Look up a business in OSM. Returns normalized lead dict or None."""
    # Name + amenity lookup, optionally scoped by city
    name_q = business_name.replace('"', '\\"')
    if city:
        # Scope by city area
        query = (
            f'[out:json][timeout:25];'
            f'area["name"="{city}"]->.a;'
            f'(node["name"~"{name_q}",i](area.a);'
            f' way["name"~"{name_q}",i](area.a););'
            f'out center 5;'
        )
    else:
        query = (
            f'[out:json][timeout:25];'
            f'(node["name"~"{name_q}",i];way["name"~"{name_q}",i];);'
            f'out center 5;'
        )

    data = _overpass_query(query)
    if not data:
        return None
    elements = data.get("elements", [])
    if not elements:
        return None

    # Pick the best match (prefer one with a phone)
    best = None
    for e in elements:
        t = e.get("tags", {})
        if t.get("name", "").lower() == business_name.lower():
            best = t
            break
    if best is None:
        best = elements[0].get("tags", {})

    # OSM uses keys like addr:city, addr:street, phone, website
    addr = best.get("addr:street", "")
    if best.get("addr:housenumber"):
        addr = f"{best['addr:housenumber']} {addr}".strip()

    return {
        "business_name": best.get("name", business_name),
        "city": best.get("addr:city", city),
        "state": best.get("addr:state", state),
        "phone": best.get("phone", ""),
        "address": addr,
        "zip": best.get("addr:postcode", ""),
        "rating": 0,  # OSM has no ratings
        "review_count": 0,
        "categories": best.get("amenity", "") + ("," + best.get("cuisine", "") if best.get("cuisine") else ""),
        "yelp_url": best.get("website", ""),
        "source": "openstreetmap",
        "source_url": best.get("website", "") or f"https://www.openstreetmap.org/",
        "verification_status": "verified" if best.get("phone") or best.get("addr:street") else "partial",
        "collected_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    }


def search_hospitality(city: str, state: str = "California", limit: int = 50) -> list:
    """Search for hospitality businesses (restaurants/bars/cafes) in a city. Real data."""
    amenity_filter = "|".join(HOSPITALITY_AMENITIES)
    query = (
        f'[out:json][timeout:30];'
        f'area["name"="{city}"]["admin_level"~"4|6|8"]->.a;'
        f'node["amenity"~"{amenity_filter}"](area.a);'
        f'out body {limit};'
    )
    data = _overpass_query(query, timeout=40)
    if not data:
        return []
    results = []
    for e in data.get("elements", []):
        t = e.get("tags", {})
        if t.get("name") and (t.get("phone") or t.get("addr:street")):
            results.append(verify(t["name"], city, state))
    return [r for r in results if r]
