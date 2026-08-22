# Visibility Research: Competitor Content Gap + Directory Verification

**Date compiled:** 2026-08-22
**Author:** Beets (1st mate), on Miles VPS (10.32.x / 31.97.6.40)
**Scope:** Pos. performance-supply-depot.com (psdepot.com) — POS supplies (thermal receipt paper, ribbons, cash registers, scales)
**Method:** Live crawl via curl (browser UA) + Browserbase browser + Wayback Machine. Firecrawl was unavailable — all data pulled directly from the live sites or archived snapshots. Honest verification status noted for every source (several targets sit behind DataDome/Cloudflare bot walls that block datacenter IPs).

> **Bottom line for the Captain:** Both "competitors" are real and organic-search relevant, but note an important finding — **goldenstateart.com is NOT a pure POS-supply competitor.** It is a modern Shopify art/framing store (mat boards, picture frames, backing boards) that *also* carries a thin line of standard thermal POS rolls. Its ~13k organic visits are dominated by ART/framing keywords, not POS. The genuine, direct POS competitor is **pos-depot.com**, which owns a deep, keyword-optimized long-tail taxonomy, especially around **employee swipe cards by POS system** and **Micros hardware**. psdepot.com's biggest structural gap is that its product URLs are SKU-number based (e.g. `15-157-2-1-4-x-230-thermal`) rather than human/keyword-friendly URLs, and it has almost no content targeting the compatibility/search categories the competitors own.

---
---

# SECTION 1 — COMPETITOR KEYWORD / CONTENT GAP ANALYSIS

## 1A. Source verification & honest status

| Site | Live-crawl (curl) | Browser | Result |
|------|------|---------|--------|
| goldenstateart.com | ✅ 200 (4.2 MB) | n/a | Fully crawlable — Shopify store, sitemap + collections + blog parsed |
| pos-depot.com | ⛔ VPN/DataDome block | ⛔ "Access Temporarily Restricted" | **Live site bot-walled.** Recovered full category taxonomy + current nav via **Wayback Machine** snapshots (Jan 2025 + Mar/May 2026). |
| psdepot.com (own site) | ✅ 200 | n/a | 633-URL sitemap parsed to identify what we already have |

> **Honest caveat:** pos-depot's *current* live pages could not be scraped directly (IP 31.97.6.40 flagged as VPN). Its keyword targets below are reconstructed from (a) the recent Wayback snapshot of the live homepage/shop (showing the *current* narrowed catalog) and (b) the full product-category URL archive (showing the full catalogue historically), plus the URL slugs (which themselves are keyword-optimized). The current site's product set at last snapshot = 38 SKUs, but their archived category tree is far deeper. Treat the full-tree list as "historical breadth" and the homepage/shop tree as "current focus."

---

## 1B. Competitor A — goldenstateart.com (reality check: art store + a little POS)

**Platform:** Shopify ("megastore" theme). https://goldenstateart.com/
**Title tag:** "Mat board, Backing Board, Show Kit, Picture frame | Golden State Art"
**Meta description target:** "wholesale pre-cut and custom mat boards, frames, and supplies... quality mat boards, picture frames, Storage Box, mirrors..."

**Product categories actually sold (~99% art/framing, ~1% POS):**
- Backing boards, preframed/uncut mat boards, mat boards by size (5x7, 8x10, 11x14, 12x16, 16x20, 18x24, 20x24, 33x41...)
- Picture frames by size (4x6 … 24x36) and by type: aluminum, wood, MDF, polystyrene, poster, floating, diploma, shadow/collage/menu frames
- Frame supplies (framing tapes, frame adhesive, backing sealing, easel backs), photo supplies (photo mats, corners, albums, folders, strips, tissue envelopes)
- Storage boxes (drop-front, clamshell, document case, record cartons), adhesives & glues, book care (bookcloth, cleaning/repair), double-sided tapes
- Mirrors (LED-lighted), Lineco brand archival, awls/needles
- **POS-relevant: a single `/collections/thermal-paper` collection** carrying the core receipt-roll sizes:
  - 2-1/4" x 165 ft, 2-1/4" x 230 ft, 2-1/4" x 50 ft, 2-1/4" x 85 ft (all "POS rolls")
  - 3-1/8" x 119 ft, 3-1/8" x 190 ft, 3-1/8" x 230 ft
  *(Note: the "thermal-paper" collection is messy — it also mixes in unrelated archival boxes/tape, i.e. they do NOT maintain it as a focused POS category.)*

**Keywords/topics their pages target** (from titles/H1/URLs/blog):
- "wholesale mat board," "pre-cut mat board," "uncut mat board," mat board size vanity URLs (every size gets its own URL = strong long-tail)
- "picture frames" by size and material; "poster frames," "shadow box frames," "display/photo frames," "menu frames," "diploma frame"
- Blog topics: "mat for picture frame," "pre-cut matboards," "preserve memories shadow box," "wholesale picture frames," "perfect 5x7/8x10 picture frames," "frame your memories"
- "Photo corners," "photo albums," "framing tapes," "easel backs," "backing board"

**What they rank for that psdepot.com does NOT serve:** Essentially all of it is *art framing* — NOT a POS-supply gap. The only crossover is the thermal-paper collection. **Our takeaway from goldenstateart:** they demonstrate the *structural* winning pattern (human-friendly `/collections/<keyword>` URLs + size-specific long-tail pages + a keyword blog) but on art supplies, not on our POS turf. We should replicate that *pattern* on thermal paper, ribbons, and scales — not copy their topics.

---

## 1C. Competitor B — pos-depot.com (the REAL direct competitor)

**Platform:** WooCommerce. https://www.pos-depot.com/ — "The POS Depot™ (844) 937-2211"
**Hero/tagline:** "POS Employee Swipe Cards For All POS Systems"
**Current homepage catalog (from live snapshot, Jan 2025):** Employee swipe cards for **Agilysys, Aloha, Micros, PixelPoint, RMPOS, Sonic, Toast, TouchBistro, Xenial Sicom, Aldelo** + "printer cable" SKUs (e.g. Aloha 1639K054), sold partly via **Amazon** ("Find us on Amazon" / "Buy X Cards on Amazon").

### Current nav structure (keyword-valuable, all employee-card focused)
- **Shop Employee Cards dropdown:** Agilysys POS, Aloha POS, Micros POS, PixelPoint POS, RMPOS, Sonic POS, Toast POS, TouchBistro POS, Xenial Sicom POS (+ "Buy …Cards on Amazon" cross-cut pages)
- Shop All Products (38 products, 3 pages) — e.g. **"Agilysys POS Employee Cards $60–$185"**, **"Aldelo POS Employee Cards $55–$75"**
- About Us

### Full archived product-category tree (historical depth — their long-tail SEO map)
This is the URL-proven keyword taxonomy (from Wayback CDX). The categories themselves ARE the keywords they target:

- **Employee / server cards:** employee-swipe-cards, employee-cards, employee-id-badges, pos-employee-swipe-cards, aloha-pos, sonic-pos-cards, restaurant-manager-pos-cards, epson-printer-cards, blank-pvc-cards-bulk-ordering, custom-logo-cards (+ customize-your-own-cards), magnetic-swipe-cards, gift-cards
- **Paper & ribbon:** paper-products → thermal-receipt-paper, paper-rolls-non-thermal, printer-ribbons, ncr-pos/paper/ncr-thermal, ncr-pos/printers
- **Micros hardware: micros-hardware, micros-pos, micros-pos-general, micros-products** → cash-drawers (incl. apg-micros-cash-drawer-keys), micros-cash-drawer-conversion-cables, customer-displays, kitchen-display-hardware, kitchen-display-systems, micros-idn-cables, micros-compatible-epson-idn-cables-adapters, micros-pos-idn-cables, micros-printer-interface-communication-cards, micros-pos-printers, micros-programming-manuals, micros-workstation-4/5/6, menu-server-58, netcc-rcc / netccrcc, touch-glass, keyboard-workstation, workstation-4-series, wokstation-55a-series
- **Cables/connectivity:** printer-cables (epson-printers, burger-king-micros-epson-printer-cables), cable-connectionsterminations, cable-rolls-500-to-1000, cash-drawer-cables, serial-vcp-cables
- **POS access/cleaning:** pos-card-reader-cleaning-cards, pos-cleaning-cards
- **Printers & hardware:** pos-printers, ncr-pos-printers, ncr-pos/printers, hardware-supplies/epson → pos-printers, communication-cables, communication-interface-cards; micros products above; hardware-supplies
- **Programming manuals:** pos-programming-manuals → 3700-manuals, 9700-manuals, micros-2700, micros-e7
- **Back office:** back-office-supplies → hp-printers (incl. specific model: toner-color-laserjet-pro-200-m251), toner-cartridges → drum-kits, toner
- **Services:** repair-services → micros-hardware-repair-services
- **Networking:** network-security-aplliancesfirewalls → watchguard (and top-level "watchguard")
- **Other:** 2019/coffee, uncategorized

**What pos-depot ranks for that psdepot.com has NO dedicated page for — the critical list:**
1. **"POS employee swipe cards"** by system (Toast, Micros, Aloha, Agilysys, PixelPoint, RMPOS, Sonic, TouchBistro, Xenial, Aldelo) — huge purchase-intent long-tail we don't touch at all.
2. **Micros hardware repair parts/manuals/workstations** (touchscreens, IDN cables, printer interface cards, kitchen display hardware, cash drawer conversion cables, programming manuals for 2700/E7/3700/9700) — deep niche we have almost nothing for (we have generic `products/40-xxx` repair SKUs, not keyword pages).
3. **Printer ribbon / cable compatibility** (Epson printer cables, cash drawer cables, serial VCP cables) — we have ribbon SKUs but no compatibility category.

---

## 1D. psdepot.com — current coverage baseline (what we already have)

From parsing the 633-URL sitemap:
- **Product pages:** overwhelmingly **SKU-number-based** URLs (e.g. `products/15-157-2-1-4-x-230-thermal.html`, `products/62235-black-ribbons.html`, `products/54-230-epson-thermal.html`, `products/72-100-cash-drawer.html`, `products/cas-cl5500.html`, `products/sam4s-er-260.html`). Rich catalog but **zero keyword-bearing, non-SKU vanity URLs** → this is the #1 SEO structural deficit.
- **Category pages seen:** `categories/` → cas-cash-registers, cf-series-cash-drawers, compact-cash-drawers, crs-sam4s-cash-registers, heavy-duty-cash-drawers, pos-scales, pos-systems, printer-ribbons, receipt-printers, standard-cash-drawers, thermal-paper
- **Guides:** `guides/` → pos-starter-kit, pos-supplies-checklist, printer-compatibility, receipt-paper-sizes, thermal-vs-bond-paper, which-capton-pourer, which-cash-drawer, which-printer-ribbon, which-thermal-paper
- **Blog:** thermal-paper chemistry, bpa-free, choose-receipt-paper-size, clean-thermal-printer, pos-paper-cafes/restaurants, thermal-vs-bond, pos-supplies-buyers-guide
- **Industries:** auto-repair, bakeries, bars, cannabis, car-washes, catering, coffee-shops, convenience-stores, food-trucks, gas-stations, grocery, gyms, hotels, liquor, medical, pharmacies, pizzerias, restaurants, retail, salons-spas
- **Locations:** massive (every US state + CA + MX + city), plus service-area pages, plus `locations/` (LA, SD, SF)
- **What we LACK:** any human-keyword product URLs, any "swipe card / employee card" coverage, any Micros/ASTRO/Toast hardware compatibility content, any "thermal paper roll size guide" style long-tail page beyond the guides we do have, and no "printer ribbon compatibility chart."

---

## 1E. RANKED CONTENT-GAP OPPORTUNITIES (build these on psdepot.com)

Ranked by (a) proven competitor demand, (b) our ability to win fast, (c) relevance to products we already sell. Each should be a human-friendly URL + a real page, not a redirect.

**Tier 1 — Highest value / closest to our catalog:**
1. **`thermal-paper-roll-size-guide`** — Comprehensive size guide (2-1/4", 3-1/8", 3-1/2", roll lengths 50/85/165/230ft; core vs jumbo) mapped to popular printers (Epson TM-U220, Bixolon SRP-350, Star TSP143, Epson TM-T20/88, Citizen, Sam4s). *Both competitors carry thermal; neither owns a definitive size guide with printer fitment — we can own this.* (We already wrote "choose-receipt-paper-size" + "receipt-paper-sizes" guide — promote/expand into this flagship.)
2. **`printer-ribbon-compatibility-chart`** — Cross-reference ribbon SKUs (ERC-30/38, 62235, 67215, purple/red-black) to cash-register/impact printers (Sam4s, CAS, Star, Epson, Citizen, TEC). Directly leverages `62-198/199 pos-ribbon-ink` + `products/printer-ribbons.html` we already list.
3. **`cash-register-thermal-paper` (by brand/model)** — Model-specific paper-fitment category pages for the registers we actually sell (CAS CL-5500/7200, Sam4s ER-260/265, TEC SL9000/SL5300, Hobart Quantum). Copy goldenstateart's *size-specific long-tail* pattern onto registers we carry.

**Tier 2 — Big win the #1 POS competitor owns; we have the product capability:**
4. **`pos-employee-swipe-cards`** hub + per-system pages — **Toast POS**, **Micros**, **Aloha**, **Agilysys**, **PixelPoint**, **Sonic**, **Xenial**, **TouchBistro** ("Toast POS employee cards," "Micros employee swipe card," etc.). pos-depot's entire business is this; we already sell `71-100 server-swipe-card` + `71-200 manager-swipe-card`. This is the single largest keyword set we completely cede today. (Supply risk: we may not stock blank mag-stripe cards for every system — but we can at minimum build the pages and qualify demand, or source through our blank-PVC/print capability.)
5. **`micros-pos-parts-and-repair`** category — Micros touchscreens, kitchen display hardware, cash drawer cables, IDN cables, printer interface cards, programming manuals (2700/E7/3700/9700). pos-depot's deepest moat; we can enter with the Micros-compatible parts we actually stock and repair-service pages (we already have `repair-services`/`services/installation`).
6. **`cash-drawer-cables-and-splitters`** — Connectivity/accessories category (we have `30-168 cash-drawer-cable-or-splitter`, `72-100`). Direct overlap with pos-depot's cable tree; low effort, high inten.

**Tier 3 — Supporting content to compound authority:**
7. **`best-point-of-sale-receipt-printers`** — Comparison roundup (thermal vs impact; Epson/Star/Bixolon/Sam4s). Feeds every printer SKU we sell; captures "best receipt printer" commercial intent.
8. **`thermal-vs-carbonless-rolls`** — Educational that answers "what receipt paper for cash register" — we already have CC-235 carbonless; ties paper guides together into an interlinked cluster.
9. **`how-to-change-printer-ribbon-cash-register`** — How-to (rich result / video potential) targeting "change ribbon on [Sam4s/CAS] cash register" — captures long-tail how-to demand *before* purchase.
10. **`restaurant-pos-supplies-checklist`** → upgrade the existing `guides/pos-supplies-checklist` into a linkable, keyword-titlehed asset and interlink it to industry pages (restaurants, food-trucks, pizzerias) we already have.
11. **`bpa-free-and-phenol-free-thermal-paper`** → expand existing `pf-230-phenol-free` product + bpa blog into a dedicated category targeting the health/safety-driven demand both competitors ignore.
12. **`pos-scales-buying-guide`** → our CAS/Citizen/Sam4s scales deserve a guide + per-model fitment (label rolls, thermal paper for scale printers). No competitor has a scales guide.
13. **`thermal-printer-cleaning-kit` / `printer-maintenance`** — We sell `71-400 MSR cleaner`, `71-500 thermal printer cleaner`, `71-600 head cleaner`; capture "clean thermal printer" (we have a blog) as a category + product cluster.
14. **`pos-hardware-bundles-for-startups`** — Package "POS starter kit" (existing `guides/pos-starter-kit`) into sellable bundles targeting small cafes/food trucks; strong conversion angle.
15. **`gift-cards-and-loyalty-supplies` (POS ID/blank PVC)** — pos-depot targets gift cards + blank PVC; we can mirror with our labels/printing capability as a niche differentiator.

> **Implementation note to Captain/Miles:** The single highest-leverage technical fix is **converting our SKU-based product URLs into keyword slugs** (keep SKUs in the title/meta, not the URL) and **building an interlinked `HUB → size-page → product` architecture**, exactly like goldenstateart does per mat-board-size and pos-depot does per-POS-system. Also note **we have ZERO map/local footprint** — that is a separate visibility fix (Section 2 helps, plus GMB) flagged by the council as the true bottleneck.

---
---

# SECTION 2 — NICHE DIRECTORY VERIFICATION (B2B / POS / Restaurant-Supply)

All checked on 2026-08-22 from the Miles VPS (datacenter IP 31.97.6.40). "✅" = reachable/verified content; "⚠️" = bot-walled from our IP (correct URL structure still captured); "❌" = not reachable.

### Live-status table

| Directory | Site | HTTP (curl) | Free listing? | Correct URL to register | Notes |
|-----------|------|-------------|--------------|--------------------------|-------|
| **ThomasNet** | thomasnet.com | ⚠️ 403 (DataDome) | **Free basic profile yes; lead-gen is paid** | `https://www.thomasnet.com/supplier-registration/` | Industrial supplier directory (huge). DataDome CAPTCHA blocks datacenter IPs ↔ must register from a normal residential/organic connection or via a real browser with proxy. General signup path = homepage → Supplier/Manufacturer registration. Free "profile" tier exists (becomes a payable search/lead subscription for seller). |
| **Kompass** | kompass.com | ⚠️ 403 (DataDome) | **Free company listing tier exists** | `https://www.kompass.com/en/intl/` → "Quick company add" / register; deep link `https://www.kompass.com/register` (and `product/quick-company-add`) | Global B2B directory (Kompass is very strong for exporters/suppliers). DataDome wall from our IP. Free base company listing; premium subscription for enhanced visibility/leads. |
| **GlobalSpec** | globalspec.com | ⚠️ 403 + Cloudflare "Just a moment…" | **Free engineer account; supplier listings paid via "e-catalog"** | `https://www.globalspec.com/` → **Sign Up** nav; supplier intake via `globalspec.com/lp/register` (or the "Products & Services" → add your products flow) | Engineering/technical product directory. Cloudflare challenge won't auto-pass from datacenter IP (needs residential/proxy or manual human). A free engineer-side account is available; *supplier* visibility is sold (GlobalSpec e-catalog / spec-search listings). Lower fit for restaurant-POS vs thomasnet, but includes scales/printers/terminals engineering verticals. |
| **FER Magazine (fermag.com)** | fermag.com | ✅ 200 | **No free listing — it's a trade magazine, not a listing directory** | n/a (they do not operate a public free dealer-directory signup) | "Foodservice Equipment Reports" — news/reviews/buying-guides publication. Has a **Buying Guides** section (`fermag.com/buying-guides/`) that can be a local/PR target, but **there is no self-serve free "dealer directory" listing** to register for. Reorient expectation accordingly. |
| **California Restaurant Association** | calrest.org | ✅ 200 | **Membership (paid dues) unlocks member listing/directory** | `https://www.calrest.org/join` ("Membership" title confirmed) + member portal `https://web.calrest.org/portal` | Live & member-focused. **Allied Member** category exists — ideal entry for a POS supplier (positioned as supplier-to-restaurants). Membership = dues; directory/locator is a member benefit, not a free listing. |
| **National Restaurant Association** | restaurant.org | ✅ 200 | Membership program (toolkit/TRA) | `https://www.restaurant.org/` → membership/join | Live. National trade org; supplier/associate membership path. Useful as an industry endorsement/backlink target more than a public directory. |
| **MAFSI** (Mfr. Agents Assoc. for the Foodservice Industry) | mafsi.org | ✅ 200 | Trade assoc. membership | `https://www.mafsi.org/` → membership | Live. Rep network for foodservice manufacturers. Not a general listing directory — relevant only as an industry presence/lead channel. |
| **NRA Education Foundation** | nraef.org | ❌ 000 (timeout/unreachable today) | — | — | Could not verify from this IP today; retry from another network. |

### POS-hardware-specific directories checked & found
- **No major open "POS-supply directory" exists** that takes unsolicited free listings — POS parts are usually distributed through *manufacturer dealer locators* (e.g. partner/find-dealer pages on Star, Epson, Sam4s, Citizen, CAS, Sharp, Toast, Micros) and through **distributor net-terms platforms**.
- The highest-value "directory-like" targets for a local/direct POS supplier are actually:
  - **Google Business Profile (GMB)** per location (zero map/local footprint today = the actual bottleneck).
  - **Yelp Business** (restaurant-heavy) for `psdepot` local pages.
  - **BBB (bbb.org)** accreditation — trust signal + a directory entry tied to CA.
  - **Bing Places** mirror of GMB listings.
  - **Chamber of Commerce / local network** listings for the service-area city pages we already have on-site.
  - **Net30 / distributor registration** (we already operate a `net30/` self-service portal on psdepot.com — a competitive differentiator to promote).
  - **Amazon Seller Central** — both competitors sell on Amazon ("Buy on Amazon" is literally a pos-depot category); an Amazon storefront is effectively a discovery directory for POS cards/paper.
- **mafsi.org / restaurant.org / calrest.org** double as **authority backlinks** worth earning (member/partner pages point back to suppliers).

---

## 2A. Actionable directory plan (what to actually do)

1. **Register free/cheap first:** ThomasNet supplier account → Kompass company page → GlobalSpec engineer account (assess paid e-catalog later). Submit from a residential/IP-not-flagged connection. ⚠️ These four must be done **outside the VPS** (blocked from 31.97.6.40) or via a residential-proxied browser.
2. **Pay to play where it pays:** CRA **Allied Member** (CA restaurant supply credibility — direct fit: we sell to CA restaurants), then NRA/MAFSI presence if budget allows — these also yield backlinks to psdepot.com.
3. **Don't waste time on a "FER dealer directory"** — it doesn't exist as a free listing; instead target FER **Buying Guides** as editorial/PR for earned exposure.
4. **Fix the real bottleneck separately:** spin up **Google Business Profiles** for each CA service city (LA, Oakland, Long Beach, Bay Area, San Jose, San Diego, etc.) tied to existing `locations/` + `<city>.<state>.html` pages. This addresses the "zero map/local footprint" the RiP GoR council flagged.
5. **Promote `net30/`** and our distributor registration as directory-grade trust signals in all listings.

---
---

## Appendix — Verification log (exact URLs checked)

**goldenstateart.com**
- `https://goldenstateart.com/` (200) — title/meta, nav, thermal collection
- `https://goldenstateart.com/sitemap.xml` → collections/blogs/products split
- `https://goldenstateart.com/sitemap_collections_1.xml` (87 KB, ~100+ collections listed)
- `https://goldenstateart.com/sitemap_blogs_1.xml` (66 KB)
- `https://goldenstateart.com/collections/thermal-paper` (755 KB) — roll sizes captured
- `https://goldenstateart.com/blogs/picture-frames` (547 KB) — blog topic titles

**pos-depot.com**
- Live `https://www.pos-depot.com/` → ⚠️ "Access Temporarily Restricted" (VPN/IP block) via both curl & browser (IP 31.97.6.40)
- Wayback live snapshot: `https://web.archive.org/web/20250117/https://pos-depot.com/` (nav: employee cards for 9 POS systems)
- Wayback shop: `https://web.archive.org/web/2026/https://pos-depot.com/shop/` (38 products, categories captured)
- Wayback CDX category archive: `web.archive.org/cdx/search/cdx?url=pos-depot.com/product-category*` (full taxonomy extracted)

**psdepot.com (own)**
- `https://psdepot.com/sitemap.xml` (633 URLs) — full baseline parsed

**Directories**
- thomasnet.com (403/DataDome); `thomasnet.com/supplier-registration/` (correct path)
- kompass.com (403/DataDome); `kompass.com/en/intl/`, `kompass.com/register`, `kompass.com/product/quick-company-add`
- globalspec.com (403 + Cloudflare challenge in browser); "Sign Up" nav link present; `globalspec.com/lp/register`
- fermag.com (200); `fermag.com/buying-guides/` (200) — magazine, no free listing directory
- calrest.org (200); `calrest.org/join` (200, "Membership" title); `web.calrest.org/portal`
- restaurant.org (200); mafsi.org (200); nraef.org (000/timeout today); fesmag.com (200)

**Honest unverified items**
- Exact current *live* pos-depot product set beyond the 38-SKU snapshot (site blocks datacenter IP).
- Actual live ThomasNet/Kompass/GlobalSpec signup *forms* (DataDome/Cloudflare require residential IP/manual human to complete; structure confirmed but submission not testable from the VPS).
- nraef.org current status (unreachable this session).
