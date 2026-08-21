# SAM4S Line — Site Prep

## Carry policy (final, 2026-08-21)

- **Default stock:** Standalone ECR (proprietary firmware) + Android devices + printers/drawers.
- **Special order (on request):** Windows models (SAPPHIRE, FORZA, TITAN-S, ASTRA, SK). Not default — fetched when a customer explicitly wants Windows.
- **Rationale:** lowest-dependency default; Windows = licensing/update/driver overhead → special-order only.

---

# SAM4S ECR Line — Site Prep

**Source:** sam4s.com (ECR category, `KCA02` / legacy `ECA02`)
**Pulled:** 2026-08-21 · **Brand:** SAM4S (PSD authorized dealer)

---

## Line overview (5 models, 4 tiers)

| Model | Tier | Platform | Display | Printer | PLUs | E-Journal |
|-------|------|----------|---------|---------|------|-----------|
| **ER-180U** | Entry | Proprietary 32-bit | 8-digit LED | 2" thermal 65mm/s | 500 | ❌ |
| **ER-230EJ** | Mid fiscal | Proprietary | 16×2 LCD ×2 | 57.5mm thermal | 1,000 (8k) | ✅ SD |
| **NR-300/400** | Mid fiscal (compact) | Proprietary | 16×2 LCD / graphic | 57.5/80mm thermal | 1,000 (8k) | ✅ SD |
| **SAP-630** | High-end restaurant | Android 6 (Celeron) | 9.7" touch | 3" thermal 100mm/s | SQLite | ✅ |
| **ZETA-A50** | Modern Android (NEW) | Android 13 (RK3566) | 5" touch + LED | 58mm thermal 70mm/s | 50,000+ | ✅ 1M+ lines |

---

## Positioning (which customer each fits)

- **ER-180U** — entry fiscal register; minimal budget, single-station, no networking.
- **ER-230EJ** — full fiscal with Ethernet + e-journal; restaurants/retail needing tax compliance + audit trail.
- **NR-300/400** — compact full-fiscal; tighter counter space, NR-400 adds graphic display.
- **SAP-630** — touchscreen restaurant workhorse; check tracking, kitchen printer, MSR.
- **ZETA-A50** — the modern flagship; Android 13, 50k+ PLUs, Wi-Fi/Ethernet, IRC network.

**Key selling angle (honest):** these are *fiscal-grade* cash registers — built for tax/audit compliance — vs. a tablet POS that needs a separate fiscal solution. "Intelligence Engineered" voice: specific, no hype.

---

## Newsroom (topical angles for media team)

- **EuroShop 2026** (Feb 2026, Düsseldorf) — most recent notice.
- **NRF 2023** — SAM4S announced a push into **North America + Latin America** ("Kicking Its North American and Latin American Push into High Gear").
- Older: EuroCIS 2022, NRF 2022, EuroShop 2020, FORZA GOOD DESIGN award 2019.

**Content hook:** SAM4S is actively expanding NA/LATAM — timely for a PSD blog post on "fiscal cash registers for US restaurants/retail" or a "SAM4S ECRs vs tablet POS" comparison.

---

## What's still needed before building product pages

1. **Pricing** — none on sam4s.com; need PSD's dealer cost + MSRP per model.
2. **SKUs** — assign PSD SKU per model (match existing `SAM4S-*` or `ECR-*` convention).
3. **Images** — product photos/renders per model (sam4s.com has them; need to pull/save).
4. **Short descriptions** — 1-2 sentence value-led copy per model (in brand voice).
5. **Decision: which models to carry** — all 5, or focus (e.g., skip entry ER-180U if margins/pricing don't support it)?

## Next steps (when you're ready)

- Confirm carry list → I pull images + write descriptions → generate product pages (Schema.org, matching your existing template) → add to `products.json` + category nav.

---

---

## POS Terminal line (KCA03) — added 2026-08-21

| Model | OS | CPU | Display | RAM |
|-------|-----|-----|---------|-----|
| **SAPPHIRE** | Windows IoT LTSC | Intel N97 (3.6GHz) | 15" | DDR4 (32GB) |
| **TITAN-S** | Windows IoT LTSC | Celeron J6412 | 15" | DDR4 (32GB) |
| **FORZA** | Windows IoT | Celeron J6412 | 10.1"–18.5" | DDR4 (32GB) |
| **SAPPHIRE Android** | Android 9 | ARM A72+A53 | 15"/15.6"/FHD | 4GB |
| **SAP-6600** | Android 6 | Celeron N3160 | 15" | 2GB |

### Positioning
- **SAPPHIRE** (Intel N97) = Windows flagship; **TITAN-S** (Celeron J6412) = same chassis, mid-tier.
- **FORZA** = configurable Windows (4 display sizes, 4 install types).
- **SAPPHIRE Android** = current Android option; **SAP-6600** = legacy Android.

### Full SAM4S carry opportunity
Two categories staged: **ECR (5 models)** + **POS Terminal (5 models)** = 10 models total. Plus Receipt Printer (KCA04), Kiosk (KCA08), and Peripherals/Drawers (KCA05) available if we want the full catalog.

---

*Staged: `sam4s_ecr_line.json` + `sam4s_pos_line.json` (structured specs) + this doc.*
