#!/usr/bin/env python3
"""
IC Browser source module — Nominatim (free, no key) address → business lookup.

Forward-geocodes an address and returns the business/POI at that location.
This is the correct tool for "search by address, see what business appears"
(OSM's data model separates address from business; Nominatim joins them).

Honest: returns None when no match — never fabricates.
"""
import json
import time
import urllib.request
import urllib.parse
from typing import Optional

UA = "PSDepot-Verifier/1.0 (miles@myl0nr0s.cloud)"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Nominatim usage policy: max 1 req/sec. Track last request time.
_last_req = 0.0

def _rate_limit():
    global _last_req
    elapsed = time.time() - _last_req
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)
    _last_req = time.time()


def lookup_by_address(address: str) -> Optional[dict]:
    """Forward geocode an address → the business/POI there. Returns a dict or None."""
    if not address or not address.strip():
        return None
    _rate_limit()
    params = {"q": address.strip(), "format": "json", "addressdetails": "1", "limit": "1"}
    url = NOMINATIM_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
    except Exception as e:
        print(f"  [nominatim] {e}")
        return None
    if not data:
        return None
    x = data[0]
    ad = x.get("address", {})
    return {
        "business_name": ad.get("shop") or ad.get("amenity") or ad.get("name") or x.get("display_name", "").split(",")[0],
        "category": x.get("type", ""),          # e.g. dry_cleaning, restaurant, fast_food
        "class": x.get("class", ""),            # shop, amenity, building
        "city": ad.get("city") or ad.get("town") or ad.get("village", ""),
        "state": ad.get("state", ""),
        "zip": ad.get("postcode", ""),
        "address": f"{ad.get('house_number','')} {ad.get('road','')}".strip(),
        "lat": x.get("lat", ""),
        "lon": x.get("lon", ""),
        "source": "nominatim",
        "source_url": f"https://nominatim.openstreetmap.org/ui/search.html?q={urllib.parse.quote(address)}",
        "verification_status": "verified" if (ad.get("shop") or ad.get("amenity") or ad.get("name")) else "geocoded",
        "collected_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    }


def reverse(lat: str, lon: str) -> Optional[dict]:
    """Reverse geocode coordinates → nearest address/business."""
    _rate_limit()
    url = ("https://nominatim.openstreetmap.org/reverse?"
           + urllib.parse.urlencode({"lat": lat, "lon": lon, "format": "json", "addressdetails": "1", "zoom": "18"}))
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            x = json.loads(r.read().decode())
    except Exception as e:
        print(f"  [nominatim] reverse {e}")
        return None
    ad = x.get("address", {})
    return {
        "business_name": ad.get("shop") or ad.get("amenity") or ad.get("name") or "",
        "category": x.get("type", ""),
        "class": x.get("class", ""),
        "city": ad.get("city") or ad.get("town") or "",
        "state": ad.get("state", ""),
        "zip": ad.get("postcode", ""),
        "address": f"{ad.get('house_number','')} {ad.get('road','')}".strip(),
        "lat": x.get("lat", ""),
        "lon": x.get("lon", ""),
        "source": "nominatim",
        "source_url": f"https://nominatim.openstreetmap.org/ui/reverse.html?lat={lat}&lon={lon}",
        "verification_status": "verified" if (ad.get("shop") or ad.get("amenity") or ad.get("name")) else "geocoded",
        "collected_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    }
