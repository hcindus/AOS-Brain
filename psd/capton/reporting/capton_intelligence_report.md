# Capton Target Intelligence Report
**Date:** 2026-08-03 | **By:** Miles | **Source:** DepotChaos unified.db

---

## Database Summary

| Source | Count | Quality |
|--------|------:|---------|
| CA ABC Licenses (Types 41, 47, 48) | **56,099** active | Phone only, no emails |
| CA ABC — Major Cities Only | **17,334** | Los Angeles, SF, SD, Sac, SJ, etc. |
| Enriched Leads (POS data, emails) | **919** | High quality, Midwest-heavy |
| Unified Leads (by cuisine) | **1,500+** | All types, mixed contact info |
| CA SOS V3 Leads | **12,941** | Business registrations |

---

## Tier 1: Enriched Leads — Ready to Contact

919 leads with emails, phone, POS system, replacement score, and revenue estimates.

### Top Targets by Replacement Score (85 = most likely to switch POS)

| Business | City | State | POS | Volume | Score |
|----------|------|-------|-----|--------|------:|
| Iowa City Pub House | Iowa City | IA | Square | $3M-5M | 85 |
| West Des Moines Cafe | Des Moines | IA | Square | $3M-5M | 85 |
| Classic Pub on Main | Davenport | IA | Square | $500K-1M | 85 |
| Cedar Rapids Bistro | Cedar Rapids | IA | Square | $3M-5M | 85 |
| Springfield Pub | Springfield | IL | Square | $500K-1M | 85 |
| Uptown Diner | Chicago | IL | Square | <$500K | 85 |
| Kitchen Co. | Rockford | IL | Square | >$5M | 85 |
| Downtown Tavern | Fort Wayne | IN | Square | <$500K | 85 |
| Indianapolis Bistro | Indianapolis | IN | Square | >$5M | 85 |
| Johnson's Kitchen | Indianapolis | IN | Square | $500K-1M | 85 |

### POS Distribution (All Enriched)

| POS System | Count | Replacement Signal |
|------------|------:|:---:|
| Square | 79 | 🔴 High — easy migration |
| Micros | 79 | 🟡 Medium — legacy system |
| Lightspeed | 79 | 🟡 Medium |
| TouchBistro | 76 | 🟡 Medium |
| Toast | 76 | 🟡 Medium |
| Clover | 73 | 🟡 Medium |
| Revel | 69 | 🟡 Medium |
| Aloha | 69 | 🔴 High — legacy, aging |
| ShopKeep | 68 | 🟢 Low — modern |
| Cake POS | 59 | 🟢 Low — modern |

---

## Tier 2: CA ABC Licenses — Needs Enrichment

56,099 total active bar/restaurant ABC licenses in CA. 17,334 in key metro areas.

### By License Type

| Type | Description | Count |
|------|-------------|------:|
| 41 | On-Sale Beer & Wine — Eating Place | 25,206 |
| 47 | On-Sale General — Restaurant (full liquor) | 18,395 |
| 48 | On-Sale General — Bar/Tavern | 12,498 |

### By City (Top 10)

| City | Type 41 | Type 47 | Type 48 | **Total** |
|------|--------:|--------:|--------:|--------:|
| Los Angeles | ~2,500 | ~1,800 | ~1,200 | **~5,500** |
| San Francisco | ~1,200 | ~900 | ~600 | **~2,700** |
| San Diego | ~1,000 | ~750 | ~500 | **~2,250** |
| San Jose | ~800 | ~600 | ~400 | **~1,800** |
| Sacramento | ~600 | ~450 | ~300 | **~1,350** |
| Oakland | ~500 | ~350 | ~250 | **~1,100** |
| Long Beach | ~400 | ~300 | ~200 | **~900** |
| Fresno | ~300 | ~250 | ~150 | **~700** |
| Santa Monica | ~200 | ~150 | ~100 | **~450** |
| Napa | ~150 | ~100 | ~80 | **~330** |

⚠️ **Note:** CA ABC data has phone numbers but no emails — requires enrichment step.

---

## Tier 3: Unified Leads by Cuisine Type

1,500+ restaurant leads across all cuisine types. Good for thermal paper cross-selling.

| Cuisine | Count | Cuisine | Count |
|---------|------:|---------|------:|
| Sandwich | 90 | Chinese | 87 |
| Burger | 87 | Taqueria | 80 |
| Restaurant | 80 | Italian | 78 |
| Bakery | 77 | Thai | 73 |
| Deli | 73 | Pizza | 72 |
| Sushi | 69 | Steakhouse | 69 |
| Diner | 69 | Cafe | 68 |
| Seafood | 67 | Food Truck | 67 |
| Breakfast | 66 | Vietnamese | 65 |
| BBQ | 64 | Mexican | 59 |

---

## Capton Cross-Sell Strategy

### Immediate Action (Week 1)
1. **Tier 1 Midwest enriched leads** — 85+ score targets with known POS systems. Approach with thermal paper + Capton bundle pitch.
2. Focus on Square/Micros/Aloha users — highest replacement urgency.

### Week 2-3
3. **CA ABC database enrichment** — run email finder on top 500 bars/restaurants in key cities. Priority: Type 48 (bars) and Type 47 (full liquor) — highest pour-per-drink volume.
4. Cross-reference with our existing thermal paper customers in CA.

### Ongoing
5. Build automated enrichment pipeline for CA ABC → email discovery → CRM import → Capton campaign.
6. Track conversion funnel: ABC lead → enriched → contacted → demo scheduled → closed.

---

## Files
- Database: `/root/.openclaw/workspace/data/depot_chaos/unified.db`
- CA ABC Licenses table: `ca_abc_licenses` (74,521 rows)
- Enriched leads table: `enriched_leads` (919 rows with emails)
- Leads table: `leads` (29,849 rows)
- Unified leads table: `unified_leads`
