# Review Gate — Media & Advertising

**Principle:** Unbiased eyes before anything reaches a live account.

## The Three Layers

### Layer 1 — Jordan (`jordan_001`) · First Pass
**Model:** `qwen3.5` (operations analyst)
**Checks:**
- Factual accuracy (prices, specs, product claims)
- Tone consistency with brand voice
- Operational correctness (links, handles, CTAs)
- No typos, no broken references

### Layer 2 — Patricia (`patricia_001`) · Second Pass
**Model:** `qwen2.5:14b` (strategy / DMCIA)
**Checks:**
- On-brand? Elegant, professional, topical?
- Strategic alignment — does this serve PSD / AGI goals?
- "Is this a good idea?" — risk, timing, sensitivity
- Cross-platform coherence (same story, right framing per channel)

### Layer 3 — Captain · Final Approve
**Action:** Approve → post, or send back with notes.

---

## Workflow Status

| Stage | State |
|-------|-------|
| Draft | ✅ Ready (agents provisioned) |
| Jordan review | 🔒 Blocked on content pipeline wiring |
| Patricia review | 🔒 Blocked on content pipeline wiring |
| Captain approve | 🔒 Blocked on platform credentials |

## Blockers to go live

1. **Platform API credentials** — X, YouTube, Instagram (Meta), Facebook (Meta), TikTok *(only remaining blocker)*
2. ~~Brand assets~~ ✅ Resolved — press kit (`/docs/press_kit/`, see `brand_assets.md`)
3. ~~Voice~~ ✅ Resolved — `04_BRAND_VOICE_TRAINING.md`
4. ~~Names~~ ✅ Approved — Iris, Reed, Echo
5. **Content pipeline** — connect draft → review → approve → publish (ready to wire once credentials land)
