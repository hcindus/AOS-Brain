# Trend Radar — social/industry trend detection

**Purpose:** Give Echo + Sage a daily "what's worth paying attention to" feed so content is topical, without chasing every trend. Dusty does the deeper sweep; Max filters against the 10% topical pillar.

## Sources (all no-auth, no credentials needed)

| Source | What it gives | Status |
|--------|---------------|--------|
| **Google Trends** (pytrends) | 7-day interest trend for brand keywords → flags rising/falling | ✅ works |
| **Hacker News** (Algolia API) | Front page + targeted queries (AI agents, POS, restaurant, retail) | ✅ works |
| **RSS** (feedparser) | Industry headlines — AI (MIT TR, VentureBeat, Ars) + retail/POS (Retail Dive, Payments Dive, PYMNTS) | ✅ works |

## What's deliberately NOT here (and why)

- **Reddit** — public `.json` API now returns 403 (auth wall).
- **Google Trends "trending topics"** — endpoint returns 404 (pytrends is semi-broken); keyword *interest* still works.
- **TikTok / X live trends** — need platform credentials (blocked until Captain provides). This is the one real gap; the radar is a strong proxy until then.

## Run

```bash
# Manual
cd AGI_COMPANY/media_advertising/trend_radar && ./run.sh

# Scheduled: crontab, daily 07:00 UTC
0 7 * * * .../trend_radar/run.sh >> /var/log/trend_radar.log 2>&1
```

## Output

- `reports/YYYY-MM-DD.md` — human-readable (Echo/Sage/Dusty/Max)
- `reports/YYYY-MM-DD.json` — machine-readable

## Files

- `trend_radar.py` — main radar
- `config.json` — brand keywords, HN queries, RSS feeds
- `run.sh` — daily runner
- `.venv/` — deps (pytrends, feedparser)

## Owners

- **Echo** ⚡ — TikTok/consumer trend signals
- **Sage** 🐦 — X/industry chatter signals
- **Dusty** 🔭 — weekly deeper competitive sweep
- **Max** 🎬 — filters into the editorial calendar
