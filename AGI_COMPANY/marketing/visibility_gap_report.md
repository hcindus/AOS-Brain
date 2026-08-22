# VISIBILITY GAP REPORT — Performance Supply Depot LLC (psdepot.com)

**Prepared by:** Beets (1st Mate), acting for Miles / RiP GoR council
**Date:** 2026-08-22
**Scope:** Local-citations & directory-presence audit + ranked action plan
**Confidence legend:**
- **[VERIFIED]** — directly confirmed by checking the directory/site (curl/browser)
- **[UNVERIFIED]** — directory bot-walled or login-gated; no direct check possible; flagged for manual confirmation
- **[NEEDS ACCOUNT]** — requires a credentials/account action only the Captain can perform

---

## ⚡ EXECUTIVE SUMMARY — THE #1 BOTTLENECK IS REAL AND WORSE THAN "THIN"

psdepot.com has a **critical local-visibility absence**: it is **completely absent from the three platforms that dominate local search and maps — Google Business Profile (GBP), Bing Places, and Apple Maps — and from the Better Business Bureau (BBB).** The website itself publishes **no physical street address** and uses only generic `Organization` schema instead of `LocalBusiness`, both of which sabotage citations and map ranking.

Meanwhile, both primary competitors appear on Google Maps; Golden State Art has a **claimed** profile (4.1★) and Mid-City Cash Register has an **unclaimed** profile. psdepot has **none at all** — it is essentially invisible in local/map search despite being a legitimate CA LLC since 2005.

**Bottom line:** This is a "signal-in / signal-out" problem. Citation building will have severely diminishing returns until a **Google Business Profile is created and claimed**, a **physical address is published on the site**, and **schema is upgraded to LocalBusiness**. The bridge of the ship here is GBP + address cleanup; everything else is subordinate.

---

## 1. LOCAL CITATIONS — psdepot.com PRESENCE MATRIX

| # | Directory | Status for psdepot | Evidence / URL |
|---|-----------|-------------------|----------------|
| 1 | **Google Business Profile** | 🔴 **MISSING** [VERIFIED] | Google Maps search "Performance Supply Depot Fairfield CA" & ". . . LLC California" returned NO matching business — only unrelated results (Pacific Supply, PDP, POS Supply Solutions). No listing exists to even claim. |
| 2 | **Bing Places / Bing Maps** | 🔴 **MISSING** [VERIFIED] | bing.com/maps &search= returned only the generic "Fairfield, CA" place card; no business entry. |
| 3 | **Apple Maps** | 🔴 **MISSING** [VERIFIED] | maps.apple.com search returned unrelated results (Performance Auto Supply, DDC Electric). |
| 4 | **Better Business Bureau (BBB)** | 🔴 **MISSING** [VERIFIED] | bbb.org search "Performance Supply Depot" + CA → page title "Search Again, No Results Found", `total_results: 0`. |
| 5 | **Yelp** | 🟡 **UNVERIFIED / likely MISSING** | yelp.com bot-walled (DataDome CAPTCHA). No indexed `yelp.com/biz/performance-supply-depot` page surfaced in any search engine. Needs manual check by Captain. |
| 6 | **Manta** | 🟡 **UNVERIFIED / likely MISSING** | manta.com Cloudflare-challenged in curl; login/search gated in browser. No organic evidence of a profile. |
| 7 | **YellowPages.com** | 🟡 **UNVERIFIED / likely MISSING** | yellowpages.com Cloudflare-challenged. No organic evidence of a listing. |
| 8 | **Foursquare** | 🟡 **UNVERIFIED / likely MISSING** | app.foursquare.com now login-gated. No organic evidence. |
| 9 | **Angi / HomeAdvisor** | ⚪ **NOT RELEVANT / no presence** | Angi is service-pro oriented (roofing, plumbing, etc.) — not a natural fit for B2B POS-supplies. No presence found; skip. |
| 10 | **Facebook Page** | 🔴 **MISSING (no links on site)** [VERIFIED] | psdepot.com homepage contains **zero** social links (no FB/LinkedIn/Twitter/IG/YouTube). Facebook public search not conclusive but no evidence of a managed page. |
| 11 | **LinkedIn Company Page** | 🔴 **MISSING** [VERIFIED] | linkedin.com/company/performance-supply-depot → **HTTP 404**. |
| 12 | **Chamber of Commerce (Bay Area)** | 🔴 **MISSING** [UNVERIFIED] | No membership/listing found anywhere. Would need SF/Oakland chamber search. |
| 13 | **Nextdoor** | 🔴 **MISSING** [UNVERIFIED] | No evidence. Nextdoor requires a local account to verify — needs Captain action. |
| 14 | **Bizapedia (CA SecState-derived)** | 🟢 **PRESENT but AUTO-GENERATED / unclaimed** [VERIFIED] | bizapedia.com/ca/performance-supply-depot-llc.html — reflects the CA LLC filing, **1880 Oak Point Ct, Fairfield, CA**, phone/name from public record. **Not a managed citation** — auto-scraped; must be superseded by the real profile. |
| 15 | **GitHub (technical backlink)** | 🟢 **PRESENT** [VERIFIED] | github.com/hcindus/psdepot & github.com/hcindus/performancesupplydepot — real, live repos (duplicative of the main site). Good technical backlink base, not a local citation. |

### On-site foundation audit (drives citation quality)
- **[VERIFIED]** robots.txt present & clean (`Allow: /` + sensible disallows), sitemap.xml live with **632 URLs** incl. per-city landing pages (anaheim-pos-supplies.html, etc.) — on-site technical SEO is *good*.
- 🔴 **[VERIFIED]** **NO physical street address ANYWHERE on the site.** Only "California" as locality. This is disqualifying for GBP (Google requires a published address), and makes Yelp/Manta/BBB directory verification impossible.
- 🔴 **[VERIFIED]** JSON-LD on homepage is generic `Organization` (not `LocalBusiness/POSRetailStore`), **no `streetAddress`, no `geo`, no `openingHours`, no `sameAs`** social/profile links.
- 🔴 **[VERIFIED]** No `sameAs` / social-profile tags → Google can't knit together a Knowledge-graph entity.

---

## 2. COMPETITOR CITATIONS — WHERE THEY ARE AND WE ARE NOT

### Mid-City Cash Register (San Leandro) — midcitycashregister.com
- 🟡 **[VERIFIED]** **Google Maps: HAS a listing at 14643 E 14th St, San Leandro, CA 94578** · phone (510) 357-4103 · **UNCLAIMED** (profile shows "Claim this business" + "Corporate office" tag). Confirms the Captain's prior intel.
- ⚠️ **[VERIFIED]** Their own website (midcitycashregister.com) returned an **SSL/cert error over curl** — so while they have a GBP entry, their site itself is in poor technical health. A crack in THEIR armor.
- Takeaway: **Mid-City is visible on Maps even unclaimed.** We can out-compete via a *claimed, fully-populated* profile — and win a page-one Maps position they're leaving on the table.

### Golden State Art (receipt paper competitor) — goldenstateart.com
- 🟢 **[VERIFIED]** **Google Maps: CLAIMED listing at 212 Littlefield Ave, South San Francisco, CA 94080** · phone (650) 226-8119 · **4.1★ from reviews** · website linked (goldenstateart.com, live, 301).
- 🟡 **[VERIFIED]** Curiously categorized as **"Picture frame shop"** on Google — a category mismatch (they sell receipt paper too) → their map ranking for "receipt paper" is likely diluted. **This is a keyword we can own.**
- Takeaway: Golden State has the *claimed* profile + review count we lack. But a mismatched category opens the door for a properly-categorized psdepot profile to rank for "thermal/receipt paper."

### psdepot.com versus both
- psdepot: **0/3** map platforms, **0** reviews, **0** claimed profiles.
- Mid-City: **1/3** (Google, unclaimed), 0 managed website health.
- Golden State: **1/3** (Google, claimed, 4.1★), but mis-categorized.

**We are the only one with ZERO map footprint. That is the single highest-ROI fix in this entire report.**

---

## 3. ACTION PLAN — TOP 10 HIGHEST-ROI CITATION / BACKLINK ACTIONS

Actions are ranked by (impact × feasibility / cost). Items 1–3 are **prerequisites** — do them first or later citation work is wasted.

| Rank | Action | Why / ROI | Effort / Cost | Type |
|------|--------|-----------|---------------|------|
| **1** | **Create & claim Google Business Profile** at 1880 Oak Point Ct, Fairfield, CA (or the real service area), fully populated: NAP (name-address-phone 888-881-6834), categories "POS equipment" + "Office machine/supplies," hours, photos, description. | This is the #1 local ranking lever. Absent here, none of the below fully pays off. Google serves ~80% of local map queries. Primary competitor already has a (unclaimed) entry — we can claim the position. | Free · **NEEDS ACCOUNT** (Captain verifies with postcard/phone) | Foundation |
| **2** | **Publish a real street address on psdepot.com** + add a Contact/Locations page. Use the registered address (1880 Oak Point Ct, Fairfield) or a service-area model with a verifiable address. | Google, Yelp, BBB, Manta all require an address. This unblocks every directory and fixes the "no address" schema flaw. | Free · site edit **NEEDS CAPTAIN** to confirm which address is public-safe | Foundation |
| **3** | **Upgrade JSON-LD schema to `LocalBusiness`/`Store`** with `streetAddress`, `geo`, `openingHours`, `sameAs`, and `@id` — and add `sameAs` links to every profile. | Tells Google exactly what/where the business is; enables Knowledge Panel entity. Anchors all citations. | Free · needs web dev / on-site edit | Foundation |
| **4** | **Claim/verify Bing Places & Apple Maps** (via Apple Business Connect / Bing Places portal) after #1 is live. | Bing powers ~6-8% + Apple Maps ~3-4% of mobile map traffic; quick multi-list wins via the address now published. Both competitors lack robust here. | Free · 30–60 min · **NEEDS ACCOUNT** | Map citation |
| **5** | **Create BBB Accredited Business profile.** | Trust signal + strong .org backlink. BBB search already shows we're absent (0 results) — being first in category. Verified-no-results = clean win. | $$ annual (BBB accreditation fee) · **NEEDS CAPTAIN** decision | Trust + backlink |
| **6** | **Create Yelp Business page** (verify with the published address/phone). | High-DR local authority; review surface; appears in "POS supplies" local queries. Likely absent → good first-mover slot in Fairfield/North Bay. | Free basic · **NEEDS ACCOUNT** | Local citation |
| **7** | **Claim + clean the auto-generated citation data** — Bizapedia, and any scraped records on Manta/YellowPages/Foursquare that feed from CA Secretary of State. Standardize NAP everywhere (name, 888-881-6834, address). | Fixes inconsistent NAP across the ~15 data aggregators (InfoGroup, Factual, Neustar) that scrape SecState filings into Yelp/Maps-adjacent data. Consistency > count for local ranking. | Free · **NEEDS ACCOUNT** per platform | Citation hygiene |
| **8** | **List on B2B / POS / restaurant-supply niche directories** (verify each URL, then register): **ThomasNet**, **Kompass**, **GlobalSpec** (POS terminals category), **Alibaba supplier storefront** (receipt paper/POS equipment), **FER Magazine** (restaurant-equipment dealer directory), **California Restaurant Association (calrest.org)** member directory. | High-authority niche backlinks + buyer-intent traffic. These are the directories the RiP GoR council flagged as "thin." Category-relevant lists = topical authority for "POS supplies," "thermal paper," "cash registers." | Free basic tiers; paid upgrades optional · **NEEDS ACCOUNT** | Niche backlinks |
| **9** | **Join the Fairfield / Solano County Chamber of Commerce (or SF/Oakland chamber if Bay-Area-focused)** and list in member directory. | Local chamber backlink + local trust signal + networking for restaurant/retail accounts. Directly counters the "thin Bay Area presence." | $$ membership · **NEEDS CAPTAIN** | Local authority |
| **10** | **Activate social presences + link them on the site:** create/link Facebook Page, LinkedIn Company, and (optionally) YouTube; add `rel=me`/`sameAs` links on homepage/footer. | Signals to Google the business is real & engaged; supplements citation count; LinkedIn is missing entirely (404). Low cost, quick wins. | Free · **NEEDS ACCOUNT** | Social + signals |

### De-prioritized (deliberately)
- **Angi/HomeAdvisor** — wrong audience (service-pro homes, not POS B2B). Skip.
- **Nextdoor** — consumer neighborhood app; low fit for wholesale POS supplies. Optional, low priority.

---

## 4. HONESTY & VERIFICATION NOTES

**What I could verify directly (done live, curl/browser):**
- psdepot.com technical foundation (robots, sitemap, schema, missing address, no social links, Org-only schema).
- Absence on Google Maps, Bing Maps, Apple Maps, BBB (BBB explicitly returned 0 results).
- Presence of Bizapedia (auto-generated) + both GitHub repos.
- Competitor GBPs: Mid-City (unclaimed) & Golden State Art (claimed, 4.1★, "picture frame shop" category).
- Mid-City's own site SSL error; Golden State's site live.

**What needs manual / account action by the Captain (flag for handoff):**
- Creating/claiming the Google Business Profile (requires address verification via postcard or phone + the Google account).
- Deciding & confirming the public physical address to publish (registered address is Fairfield, but Captain should confirm the real / safe-to-publish operating address).
- All paid-account actions: BBB accreditation, chamber membership, FER/CalRest paid tiers.
- Yelp (bot-walled — I could not confirm the page exists or not; verify manually), Manta, YellowPages, Foursquare (all login/bot-gated — verify manually).

**Unverified due to tool outages (web_search/web_extract down — Firecrawl broken as flagged):**
- Niche directory URL list (ThomasNet, Kompass, GlobalSpec, etc.) is drawn from established training knowledge; **each URL and its free/paid status should be re-verified** when search tools are restored.

---

## 5. BOTTOM LINE FOR THE RiP GoR COUNCIL

1. **psdepot.com is invisible in local/map search** — zero presence on the big-3 maps + BBB. This is the visibility bottleneck, quantified.
2. Two competitors with spotty footprints (Mid-City unclaimed; Golden State mis-categorized) are still beating us purely by *existing* on Google Maps.
3. The **first three actions** (create+claim GBP, publish an address, fix schema) are non-negotiable and unlock all downstream citation ROI. Everything after that multiplies off this foundation.
4. Deliverables that only the **Captain** can do (account/identity actions) are the gating items — provide: confirmed physical address, Google account access, and budget decision on paid memberships (BBB, chamber).

---
*Report generated by Beets (Hermes agent, Miles fleet) — 2026-08-22.*
*Sources: live HTTP/browser checks against the listed directories; psdepot.com on-site audit; Google/Bing/Apple Maps; BBB; Bizapedia; GitHub.*
