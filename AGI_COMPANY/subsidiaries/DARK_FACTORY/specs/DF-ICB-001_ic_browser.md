# Project Spec — IC Browser (Intelligence Collection Browser)

**Project ID:** DF-ICB-001
**Type:** Fleet infrastructure component
**Requested by:** Captain (2026-08-27)
**Status:** SPEC — pending RiP GoR + Dark Factory build

---

## 1. Problem Statement

The DataDepot lead pipeline has been **synthetic for 7+ consecutive days**. Root cause: there is no real data-collection path. The current scraper (`collection_workflow.py`) fabricates records (`random` license numbers, fake names, `(555)` phones, `example.com` emails) instead of scraping real sources.

**No existing agent** is purpose-built for honest, real-world intelligence collection. We have:
- `agent-browser` (Vercel Labs) — generic headless browser, no stealth/anti-detection
- `browser_agent.py` (Playwright) — marketing/content automation, no structured lead extraction

**Gap:** a dedicated IC Browser that scrapes REAL public sources (abc.ca.gov, state registries, Google Places, Yelp) with anti-detection, rate limiting, and honest structured extraction — feeding REAL verified data into DepotChaos.

## 2. Objectives

Build a fleet-deployable Intelligence Collection browser agent that:

1. **Collects real data** from public business/registry sources (never fabricates).
2. **Verifies** business existence + contact data against real sources (no synthetic enrichment).
3. **Honors rate limits & anti-detection** — polite, stealthy, survivable against Cloudflare/CAPTCHA/bot-detection.
4. **Emits structured, schema-valid leads** into `unified.db` / `depot_chaos.db`, marked `verified=true` with a `source_url`.
5. **Is honest** — every record carries provenance; unverifiable records are flagged, never invented.

## 3. Target Data Sources (v1)

| Source | Data | Method |
|--------|------|--------|
| abc.ca.gov (CA ABC license search) | License type, business, address, owner, status | HTML scrape + official export |
| CA Secretary of State / state biz registries | Entity name, status, agent, date | Registry API/HTML |
| Google Places API | Business name, phone, address, rating, hours | API (real key) |
| Yelp Fusion API | Same + review counts, categories | API (existing key) |
| US state restaurant/food registries | License holders | Per-state scraper |

## 4. Technical Requirements

### 4.1 Core engine
- Playwright (Chromium) with **stealth plugin** (playwright-stealth / patched fingerprint)
- Rotating User-Agent pool + viewport/header randomization
- Optional rotating proxy support (HTTP/SOCKS5)
- CAPTCHA handling: 2captcha/anti-captcha hook (optional, off by default)
- Session persistence (cookies/localStorage) for logged-in sources

### 4.2 Intelligence features
- **Structured extraction** — per-source "scraper modules" that map HTML/JSON → normalized `Lead` schema
- **Verification layer** — cross-check phone/email/address against a second source before marking `verified`
- **Deduplication** — normalized name+city+state fingerprint
- **Provenance** — every lead carries `source_url`, `collected_at`, `verification_status`

### 4.3 Anti-detection & ethics
- Configurable delay between requests (default 2–5s) + per-domain rate budget
- `robots.txt` respect flag (default on for public registries)
- No CAPTCHA bypass by default — flag + requeue on challenge
- Honest provenance: never fabricate; unverifiable → `status=unverified`

### 4.4 Fleet rollout
- Ships as a Python package + a `systemd` service per VPS
- CLI: `icbrowser scrape --source abc.ca.gov --count 500`
- Output: SQLite writes + JSON report; optional email/Telegram alert on new qualified leads

## 5. Deliverables

1. `ic_browser/` Python package (engine + scraper modules + verifier + dedupe)
2. Scraper modules: `abc_ca.py`, `google_places.py`, `yelp.py`, `ca_sos.py`
3. `schema.sql` — normalized `verified_leads` table with provenance columns
4. `icbrowser` CLI + `ic-browser.service` systemd unit
5. Integration test proving real scrape → real lead → DepotChaos insert
6. Fleet rollout script (`deploy_fleet.sh`) + per-agent config

## 6. Success Criteria (Definition of Done)

- [ ] Scrapes 500 REAL CA ABC licenses without fabrication
- [ ] Google Places enrichment returns real phone/address (not `(555)`, not `example.com`)
- [ ] Every lead carries `source_url` + `verified=true/false`
- [ ] Zero synthetic records (spot-check: no `random` names, no fake zips)
- [ ] Survives a basic bot-detection page without crashing
- [ ] Deployed + running on at least 2 fleet VPS nodes

## 7. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Bot detection / IP ban | Stealth + proxies + rate limiting + polite delays |
| Source TOS/legal | Respect robots.txt, public data only, rate-limit, provenance |
| CAPTCHA | Optional solver hook; default flag-and-requeue |
| Data staleness | Scheduled re-scrape + freshness watermark |

## 8. Out of Scope (v1)

- Paid data brokers / dark-web sources
- Aggressive CAPTCHA bypass / credential stuffing
- Scraping gated/auth-walled sources without permission
- Social media scraping (TikTok/IG) — separate future module
