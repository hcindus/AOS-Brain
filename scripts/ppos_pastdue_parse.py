#!/usr/bin/env python3
"""Parse Performance POS past-due list and reconcile against databases."""
import json, re, sqlite3

RAW = """AH ANAHEIM WHITE HOUSE 3036106 3/3 SUPPLIES 3/3 OC 496 62 38.47 597.11 UPS AH U
AH ANDI'S MARKET 2116103 2/11 SUPPLIES 2/12 SF 576 93 49.70 719.26 UPS AH U
AH ATWATER TAVERN 3116101 3/11 SUPPLIES 3/11 SF 885 106 76.36 1067.71 UPS AH U
AH BARREL HOUSE TAVERN 3196101 3/19 SUPPLIES 3/19 SAUS 1831 311 169.37 2311.57 UPS AH U
DK BARRELHOUSE SAUS 626801 8/1 SUPPLIES 8/1 SR 620 57.35 677.35 PU MGR U
AH BELLAM SELF STORAGE 3106102 3/10 SUPPLIES 3/10 SR 937 156 86.72 1179.81 UPS AH U
DK CAFÉ SOLIEL 4166071 4/16 SUPPLIES 4/16 SONC 42 16 4.31 61.87 UPS DK U
AH CANNETI ROADHOUSE ITALIANA 10035101 10/3 SUPPLIES 10/3 SON 217 47 20.07 283.75 UPS AH U
DK CELIA'S SR 7086071 7/8 SUPPLIES 7/8 SR 39 3.61 42.61 PU DK U
AH CELIA'S/XALISCO CORP 11195101 11/19 SUPPLIES 11/19 RESALE 625 625.00 PU ROSENDO U
AH CHINA LIVE VENTURES 10145102 10/14 SUPPLIES 10/15 SF 297 47 25.63 369.31 UPS AH U
AH COTOGNA 3036110 3/3 SUPPLIES 3/3 SF 985 187 84.99 1257.11 UPS AH U
AH COTOGNA RESTAURANT 4016101 4/1 SUPPLIES 4/1 SF 126 16 10.87 152.43 UPS AH U
AH COUNTRY GABLES CAFÉ 2136104 2/13 SUPPLIES 2/16 ROSEV 326 62 25.28 413.72 UPS AH U
DK FATTORIA E MARE HMB 8036071 8/3 SUPPLIES 8/4 SM 361 60 35.66 456.76 UPS DK U
AH GASPARE'S SAN RAFAEL 3306803 3/30 SUPPLIES 4/1 SR 434 40.15 474.15 PU DANIEL U
AH ISABEL'S VINTAGE CAFÉ 3206101 3/20 SUPPLIES 3/20 S.JOAQ 163 16 12.64 191.30 UPS AH U
DK JUANCHO PARILLA 5046071 5/4 SUPPLIES 5/4 TRACY 200 15 18.75 233.75 UPS DK U
AH LOS CAPORALES TAQUERIA 4066103 4/6 SUPPLIES 4/6 ALA 222 47 22.77 291.55 UPS AH U
AH LOST MARBLES BREWPUB 12305101 12/30 SUPPLIES 12/31 SF 332 47 28.65 407.53 UPS AH U
AH LOTUS INDIAN CUISINE 4086101 4/8 SUPPLIES 4/8 SR 295 27.29 322.29 PU MGR U
DK LUMA BAR & EAT PET 8276074 8/27 SUPPLIES 8/27 PET 79 8.10 87.10 DEL MB U
AH MEKONG KITCHEN 10035103 10/3 SUPPLIES 10/6 ALA 59 31 6.34 96.46 UPS AH U
AH MI CASA CAFÉ 4066101 4/6 SUPPLIES 4/6 SR 76 7.03 83.03 PU INGRID U
DK MI CASA CAFÉ 617801 6/17 SUPPLIES 6/17 SR 124 11.48 135.58 PU INGRID U
AH MONICA'S RIVERVIEW 10025106 10/2 SUPPLIES 10/3 ANTIOCH 124 16 12.10 151.76 UPS AH U
DK MONTI'S 6256071 6/25 SUPPLIES 6/28 S.ROSA 274 60 27.40 361.40 UPS DK U
DK MONTI'S S.ROSA 8176071 8/17 SUPPLIES 8/17 S.ROSA 609 90 60.93 760.23 UPS DK U
DK MOUNTAIN MIKE'S PIZZA 5146071 5/14 SUPPLIES 5/14 SOL 276 62 29.67 367.67 UPS DK U
AH NOSH CORNER 4076101 4/7 SUPPLIES 4/7 RC 59 16 5.46 79.96 UPS AH U
DK OCEANVIEW DINER 5056071 5/5 SUPPLIES 5/5 ALA 282 60 28.91 370.91 UPS DK U
RF OCEANVIEW DINER BERK 8246072 8/24 SUPPLIES 8/24 ALA 654 120 67.07 841.37 UPS DK U
DK OSSO STEAKHOUSE 5226071 5/22 SUPPLIES 5/22 SF 104 31 8.97 143.97 UPS DK U
RF PANDA RESTAURANT GROUP LA 8046062 8/3 TILLS-100 8/4 LA 3900 57 380.25 4337.25 DROP MS U
DK PICANTE SR 8276072 8/27 SUPPLIES 8/27 SR 186 17.21 203.31 PU MGR U
DK QUINCE SF 7166071 7/16 SUPPLIES 7/16 SF 812 120 70.11 1002.51 UPS DK U
AH SALT AND PEPPER TIBURON 3196103 3/19 SUPPLIES 3/19 MARIN 242 47 19.97 308.75 UPS AH U
AH STAR GROCERY 4066107 4/6 SUPPLIES 4/6 ALA 320 93 32.80 446.16 UPS AH U
AH TAGLIAFERRI DELI 2096102 2/9 SUPPLIES 2/12 NOVATO 90 16 8.33 113.89 UPS AH U
AH TAGLIFERRI DELI 3246102 3/24 SUPPLIES 3/24 NOVATO 117 47 10.82 174.50 UPS AH U
DK TERIYAKI MADNESS HELENA 5116075 5/11 SUPPLIES 5/11 O/S 248 31 279.20 UPS DK U
DK TERIYAKI MADNESS BILLINGS 7206072 7/20 SUPPLIES 7/20 O/S 99 15 0.00 114.00 UPS DK U
AH THE OLD WAGON SALOON & GRILL 3096104 3/9 SUPPLIES 3/9 SC 372 47 34.90 453.88 UPS AH U
DK THE SHUCKERY PET 8276073 8/27 SUPPLIES 8/27 PET 79 8.10 87.10 DEL MB U
AH THREE BROTHERS GRILL POTTSTOWN 1136102 1/13 SUPPLIES 1/13 O/S 312 23 334.57 UPS AH U
AH TOMATINA SANTA ROSA 3176105 3/17 SUPPLIES 3/17 ROSE 225 31 17.45 273.67 UPS AH U
AH TOMATINA SANTA CLARA 3316106 3/31 SUPPLIES 4/1 SC 183 47 16.71 246.49 UPS AH U"""

REGION_MAP = {
    "OC": ("Orange County", "CA"), "SF": ("San Francisco", "CA"),
    "SAUS": ("Sausalito", "CA"), "SR": ("San Rafael", "CA"),
    "SONC": ("Sonoma County", "CA"), "SON": ("Sonoma", "CA"),
    "ROSEV": ("Rohnert Park", "CA"), "SM": ("San Mateo", "CA"),
    "S.JOAQ": ("San Joaquin", "CA"), "TRACY": ("Tracy", "CA"),
    "ALA": ("Alameda", "CA"), "PET": ("Petaluma", "CA"),
    "ANTIOCH": ("Antioch", "CA"), "S.ROSA": ("Santa Rosa", "CA"),
    "SOL": ("Solano", "CA"), "RC": ("Redwood City", "CA"),
    "LA": ("Los Angeles", "CA"), "MARIN": ("Marin", "CA"),
    "NOVATO": ("Novato", "CA"), "O/S": ("Out of State", None),
    "SC": ("Santa Clara", "CA"), "ROSE": ("Santa Rosa", "CA"),
}

def norm(s):
    s = s.upper()
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

records = []
for line in RAW.strip().split("\n"):
    line = line.strip()
    if not line:
        continue
    m = re.match(r"^(AH|DK|RF)\s+", line)
    prefix = m.group(1) if m else ""
    rest = line[m.end():] if m else line
    toks = rest.split()
    name_toks = []
    invoice = None
    i = 0
    while i < len(toks):
        if re.fullmatch(r"\d{6,8}", toks[i]):
            invoice = toks[i]
            break
        name_toks.append(toks[i])
        i += 1
    name = " ".join(name_toks)
    after = toks[i+1:] if invoice else toks
    region = ""
    region_idx = -1
    for j, t in enumerate(after):
        if t in REGION_MAP:
            region = t
            region_idx = j
            break
    tail = after[region_idx+1:] if region_idx >= 0 else after
    nums = []
    k = 0
    while k < len(tail) and re.fullmatch(r"\d+(\.\d+)?", tail[k]):
        nums.append(tail[k])
        k += 1
    ship = ""
    code2 = ""
    status = ""
    if k < len(tail) and tail[k] in ("UPS", "PU", "DEL", "DROP"):
        ship = tail[k]; k += 1
    if k < len(tail) and tail[k] != "U":
        code2 = tail[k]; k += 1
    if k < len(tail):
        status = tail[k]
    amounts = [float(x) for x in nums]
    total = amounts[-1] if amounts else 0.0
    subtotal = amounts[0] if amounts else 0.0
    date = ""
    for t in after:
        if re.fullmatch(r"\d{1,2}/\d{1,2}", t):
            date = t
            break
    records.append({
        "prefix": prefix, "name": name, "invoice": invoice,
        "date": date, "region": region,
        "region_city": REGION_MAP.get(region, ("", ""))[0],
        "amounts": nums, "total": round(total, 2), "subtotal": subtotal,
        "ship": ship, "code2": code2, "status": status,
    })

print(f"Parsed {len(records)} records")
print(f"Total outstanding: ${sum(r['total'] for r in records):,.2f}\n")

json.dump(records, open("/root/.openclaw/workspace/data/ppos_pastdue_parsed.json", "w"), indent=2, ensure_ascii=False)

bf = json.load(open("/root/.openclaw/workspace/data/backfill_clients.json"))
bf_by_norm = {}
for c in bf:
    bf_by_norm.setdefault(norm(c["vendor_name"]), []).append(c)

con = sqlite3.connect("/root/.openclaw/workspace/data/depot_chaos/unified.db")
con.row_factory = sqlite3.Row
leads = con.execute("SELECT business_name, city, state, email, phone, id FROM leads WHERE deleted=0").fetchall()
lead_names = [(norm(l["business_name"]), l) for l in leads]

def find_match(name):
    n = norm(name)
    hits = []
    if n in bf_by_norm:
        hits.append(("backfill_exact", bf_by_norm[n][0]))
    else:
        for k, v in bf_by_norm.items():
            if n and (n in k or k in n):
                hits.append(("backfill_fuzzy", v[0]))
                break
    if not any(h[0] == "leads_exact" for h in hits):
        for ln, l in lead_names:
            if ln == n:
                hits.append(("leads_exact", l))
                break
    if not any(h[0] in ("leads_exact",) for h in hits):
        for ln, l in lead_names:
            if n and (n in ln or ln in n):
                hits.append(("leads_fuzzy", l))
                break
    return hits

print("=== RECONCILIATION ===")
print(f"{'STATUS':8} {'CUSTOMER':34} {'INVOICE':10} {'TOTAL':>9}  MATCH")
missing = []
for r in records:
    hits = find_match(r["name"])
    if not hits:
        missing.append(r)
    status = "FOUND" if hits else "MISSING"
    match_desc = ""
    if hits:
        h0 = hits[0]
        if h0[0].startswith("backfill"):
            match_desc = f"backfill: {h0[1]['vendor_name']} ({h0[1].get('phone','')})"
        else:
            l = h0[1]
            match_desc = f"leads#{l['id']}: {l['business_name']} {l['city'] or ''}"
    print(f"{status:8} {r['name'][:34]:34} {r['invoice'] or '':10} {r['total']:>9,.2f}  {match_desc[:50]}")

print(f"\n=== SUMMARY ===")
print(f"Total records: {len(records)}")
print(f"Matched: {len(records)-len(missing)}")
print(f"Missing: {len(missing)}")
print(f"\n--- MISSING (need to add) ---")
for r in missing:
    print(f"  {r['name']:34} {r['invoice']:10} {r['region']:8} ${r['total']:,.2f}")
json.dump(missing, open("/root/.openclaw/workspace/data/ppos_pastdue_missing.json", "w"), indent=2, ensure_ascii=False)
