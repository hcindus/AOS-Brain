#!/usr/bin/env python3
"""Address → business reverse lookup test (Nominatim) — 10 addresses."""
import sys, time
sys.path.insert(0, "/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/DARK_FACTORY/deliverables/ic_browser")
from sources import nominatim

ADDRS = [
    "28227 Newhall Ranch Rd, Santa Clarita, CA 91355",
    "4741 Chace Circle STE 113, Hoover, AL 35244",
    "7216 Bailey Cove Rd SE, Huntsville, AL 35802",
    "7709 Hwy 72 W, Madison, AL 35758",
    "250 McFarland Blvd, Northport, AL 35476",
    "4722 E Ray Rd, Phoenix, AZ 85044",
    "1229 S Power Rd #105, Mesa, AZ 85206",
    "4225 S Gilbert Rd, Chandler, AZ 85249",
    "16955 N 75th Ave, Peoria, AZ",
    "3131 S Market Street, Gilbert, AZ 85295",
]

print("=" * 66)
print("  ADDRESS → BUSINESS (Nominatim) — 10-address test")
print("=" * 66)
found = 0
for addr in ADDRS:
    r = nominatim.lookup_by_address(addr)
    if r and r.get("business_name"):
        found += 1
        tag = f"[{r.get('class')}/{r.get('category')}]" if r.get('category') else ""
        print(f"  ✅ {addr[:45]:47} → {r['business_name']} {tag}")
    else:
        print(f"  ⚪ {addr[:45]:47} → (no business match)")
    time.sleep(1.1)  # Nominatim: 1 req/sec max

print(f"\nResult: {found}/10 addresses mapped to a business")
