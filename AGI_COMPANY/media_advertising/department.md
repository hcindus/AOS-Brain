# Media & Advertising Department

**Status:** ✅ OPERATIONAL (agents provisioned)
**Version:** 1.0 — 2026-08-21
**Head:** Max (`max_001`) — Director of Media & Advertising
**Reports to:** Aurora (Creative) → Captain

---

## Mission

Own the public voice and paid reach for two brands across five platforms:

1. **Performance Supply Depot LLC** — POS supplies, hardware, operational reliability
2. **AGI Company Services** — AI agents, autonomy, thought leadership

**Voice:** elegant · professional · topical
**Rule:** No hype, no cringe. Understated authority. Ride relevant industry moments without chasing every trend.

**Brand source:** `brand_assets.md` ← `/docs/press_kit/` (colors, fonts, logo, social assets, boilerplate, tagline "Intelligence Engineered.")

---

## Roster

| Agent | Platform | Model | Focus |
|-------|----------|-------|-------|
| **Max** (`max_001`) | — (lead) | `qwen2.5:14b` | Strategy, calendar, brand voice, cross-post routing |
| **Sage** (`sage_001`) | X | `nous-hermes2` | Short-form, threads, engagement |
| **Nova** (`nova_001`) | YouTube | `qwen3.5` | Scripts, titles, thumbnails, shorts + long-form |
| **Iris** (`iris_001`) | Instagram | `qwen3.5` | Reels, grid, Stories, captions |
| **Reed** (`reed_001`) | Facebook | `nous-hermes2` | Posts, Groups, paid-ad copy |
| **Echo** (`echo_001`) | TikTok | `qwen3.5` | Trending clips, hooks, short video |

---

## Content Pillars

| Pillar | Brand | Example |
|--------|-------|---------|
| **Operational excellence** | PSD | "Why your cash drawer jams — and the $0 fix" |
| **AI thought leadership** | AGI | "What we learned running 58 autonomous agents" |
| **Customer / community stories** | Both | Testimonials, use cases, behind-the-scenes |
| **Topical moments** (selective) | Both | Industry shifts, relevant news — no bandwagoning |

---

## Review Gate (nothing posts without clearance)

```
Content drafted (platform agent)
        │
        ▼
[1] Jordan (jordan_001) — factual accuracy, tone, ops consistency
        │
        ▼
[2] Patricia (patricia_001) — on-brand, strategic alignment, "is this a good idea"
        │
        ▼
[3] Captain — final approve → POST
```

- **Current mode:** 100% human-in-the-loop. Captain reviews every piece.
- **Escalation:** platforms flip to auto-post **one at a time**, only after Captain confirms comfort.

---

## Cadence (starting point, all for review)

| Platform | Frequency |
|----------|-----------|
| X | 1–2 / day |
| Instagram | 1 / day |
| TikTok | 3–4 / week |
| Facebook | 1 / day |
| YouTube | 1 short / week + 1 long-form / 2 weeks |

---

## Files

| Path | Purpose |
|------|---------|
| `manifest.json` | Machine-readable department manifest |
| `agents/*.md` | Per-agent role/skill/tool docs |
| `review_gate.md` | Full review workflow |
| `content_calendar.md` | Editorial calendar + cadence |
| `build_department.py` | Provisioning script (idempotent) |
| `/var/lib/aos/agents/crew-{agent}_001/` | Crew workspaces |
| `/var/lib/aos/agent_keys/{agent}.json` | Crypto identities |
