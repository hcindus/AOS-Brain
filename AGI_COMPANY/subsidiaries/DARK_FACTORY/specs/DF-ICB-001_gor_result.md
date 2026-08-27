# RiP GoR Result — DF-ICB-001 IC Browser

**Task:** IC Browser (Intelligence Collection browser agent)
**Date:** 2026-08-27
**Method:** Manual structured roast (automated GoR hung on slow Ollama — fallback to reasoned governance)

---

## Stage 1 — ROAST (6 personas)

### Contrarian (25%) — Fatal Flaw Finder
- ⚠️ **Bot detection is hard and moving.** abc.ca.gov and Google actively block scrapers. Stealth is cat-and-mouse; fingerprints change weekly.
- ⚠️ **TOS/legal risk.** Google Places + Yelp explicitly prohibit scraping their HTML. Scraping them = account ban + potential legal exposure.
- ⚠️ **Zero-return risk.** If sources block us, "honest no-fabrication" means ZERO leads — the exact problem we're trying to solve.

### Expansionist (15%) — Upside Maximizer
- 🚀 Unblocks the entire lead pipeline (112K vendors become verifiable → real leads → real revenue).
- 🚀 Fleet-reusable across domains (not just CA ABC — any registry).
- 🚀 Could become a product (IC browser as a service).

### FirstPrinciples (20%) — Logic Purist
- ✅ Core requirement sound: real data > synthetic, always.
- ⚠️ "Honest verification" needs a SECOND source for cross-check → doubles scraping load + bot risk.
- ✅ Architecture (modules + verifier + dedupe + provenance) is correct decomposition.

### Researcher (20%) — Market Intelligence
- 📊 **We're reinventing a wheel.** Firecrawl, Bright Data, ScrapingBee already solve anti-detection scraping.
- 📊 **Legit APIs exist and we already have keys:** Google Places API (paid, legit), Yelp Fusion API (key already in codebase). These are NOT scraping — no TOS risk.
- 📊 Firecrawl API key is a 1-char placeholder (broken since 2026-08-18).

### Buyer (20%) — Customer Proxy
- ✅ "Real leads, not fake" — exactly right.
- ✅ Provenance/verified flag is table stakes — must trust the data.
- ✅ Don't care about tech; care that it delivers verified phone/email.

### Judge (arbiter)
- Weighted score: **~6.0 / 10** → **RESHAPE**
- The NEED is real and urgent, but the "stealth-scrape everything" approach must pivot: **legit APIs first, stealth scraping only where no API exists.**

---

## Stage 2 — PATRICIA (DMCIA specialist)

- **Mode:** ALIGNED (directly resolves the 7-day synthetic halt — high org priority)
- **Context:** Unblocks DepotChaos lead quality; restores trust in data; enables real sales outreach.
- **Delegation:** Dark Factory (Forge) to build; Miles to spec + integration-test; fleet rollout after verified.

---

## Stage 3 — GoR VERDICT

**Roast:** RESHAPE (6.0/10)
**Patricia:** ALIGNED (urgent priority)
**Matrix:** RESHAPE × ALIGNED → **RESHAPE**

### Final Verdict: **RESHAPE** ✅ (with reshape notes baked in)

**Reshape guidance (mandatory, not optional):**
1. **APIs FIRST:** Google Places API + Yelp Fusion API as PRIMARY sources (legit, keys exist, no TOS risk). Stealth Playwright scraping ONLY for abc.ca.gov + public registries with no API.
2. **Fix Firecrawl key** OR drop it — don't build on a broken placeholder.
3. **Drop Yelp HTML scraping** — use Yelp Fusion API only (no TOS violation).
4. **Verification via API cross-check** (Google Places + Yelp agree → verified), not a second scrape.
5. Keep all the good parts: honest provenance, `verified` flag, `source_url`, zero-fabrication, dedupe.

---

## Action Items

1. [ ] Rewrite spec §3 (sources) to lead with APIs, demote stealth scraping
2. [ ] Confirm Google Places API key exists (or provision one)
3. [ ] Confirm Yelp Fusion key is valid (it's in the codebase — verify)
4. [ ] Dark Factory builds: engine + API scraper modules + verifier + CLI + systemd
5. [ ] Integration test: real scrape → real lead → DepotChaos insert
6. [ ] Fleet rollout after 2-node verified test
