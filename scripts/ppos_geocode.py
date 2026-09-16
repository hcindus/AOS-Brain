#!/usr/bin/env python3
"""Geocode Performance POS past-due accounts via Geoapify."""
import json, re, time, urllib.parse, urllib.request

KEY = "800cfe1b1239457386c7d8c46c5170e0"
RECON = "/root/.openclaw/workspace/data/ppos_pastdue_reconciled.json"

# location suffix tokens embedded in names, to strip for a cleaner query
SUFFIX = re.compile(
    r"\b(SF|SR|LA|PET|SAUS|HMB|S\.?ROSA|SANTA ROSA|SANTA CLARA|HELENA|BILLINGS|"
    r"POTTSTOWN|BERK|TIBURON|O/S|OC|SC|SONC|SON|SM|ALA|NOVATO|MARIN|ANTIOCH|"
    r"TRACY|ROSEV|SOL|RC|S\.JOAQ)\b",
    re.IGNORECASE,
)

def geocode(text):
    url = "https://api.geoapify.com/v1/geocode/search?" + urllib.parse.urlencode({
        "text": text, "apiKey": KEY, "limit": 1,
    })
    with urllib.request.urlopen(url, timeout=20) as r:
        data = json.load(r)
    feats = data.get("features", [])
    if not feats:
        return None
    p = feats[0]["properties"]
    return {
        "name": p.get("name"),
        "formatted": p.get("formatted"),
        "street": p.get("street"),
        "housenumber": p.get("housenumber"),
        "city": p.get("city"),
        "state": p.get("state"),
        "postcode": p.get("postcode"),
        "lat": p.get("lat"),
        "lon": p.get("lon"),
        "confidence": (p.get("rank") or {}).get("confidence"),
        "match_type": (p.get("rank") or {}).get("match_type"),
        "result_type": p.get("result_type"),
        "category": p.get("category"),
    }

records = json.load(open(RECON))

# state defaults
def state_for(r):
    if r.get("region") == "O/S":
        return {"TERIYAKI MADNESS HELENA": "MT",
                "TERIYAKI MADNESS BILLINGS": "MT",
                "THREE BROTHERS GRILL POTTSTOWN": "PA"}.get(r["name"].upper(), "")
    return "CA"

out = []
for i, r in enumerate(records, 1):
    name = r["name"]
    clean = SUFFIX.sub(" ", name).strip()
    clean = re.sub(r"\s+", " ", clean).strip()
    city = r.get("region_city") or ""
    state = state_for(r)
    # avoid duplicate city if already in clean name
    query = f"{clean}, {city}, {state}"
    if city and city.lower() in clean.lower():
        query = f"{clean}, {state}"
    g = geocode(query)
    r["geocode_query"] = query
    r["geocode"] = g
    out.append(r)
    flag = ""
    if not g:
        flag = "NO RESULT"
    elif not g.get("confidence") or g["confidence"] < 0.8:
        flag = f"LOW CONF ({g.get('confidence')})"
    print(f"[{i:2}/{len(records)}] {name[:28]:28} -> {g['formatted'][:50] if g else 'NONE':50} {flag}")
    time.sleep(0.35)

json.dump(out, open("/root/.openclaw/workspace/data/ppos_pastdue_geocoded.json", "w"), indent=2, ensure_ascii=False)

ok = sum(1 for r in out if r.get("geocode") and (r["geocode"].get("confidence") or 0) >= 0.8)
print(f"\n=== DONE === {ok}/{len(out)} high-confidence, saved to data/ppos_pastdue_geocoded.json")
