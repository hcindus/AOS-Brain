#!/usr/bin/env python3
"""
Trend Radar — lightweight social/industry trend detection for the Media & Advertising dept.

Sources:
  1. Google Trends (pytrends) — realtime + daily trending, plus keyword interest over time
  2. Reddit (public JSON API) — hot posts in relevant subreddits
  3. RSS (feedparser) — industry headlines (AI + POS/retail)

Output:
  reports/YYYY-MM-DD.md   (human-readable, for Echo/Sage/Dusty/Max)
  reports/YYYY-MM-DD.json (machine-readable)

Owners:
  Echo (TikTok trends) + Sage (X chatter) pull this daily; Dusty does the deeper sweep;
  Max filters against the 10% topical pillar.
"""
import json, os, sys, time, datetime
from urllib.parse import quote

import requests
import feedparser

try:
    from pytrends.request import TrendReq
    HAVE_PYTRENDS = True
except Exception:
    HAVE_PYTRENDS = False

HERE = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(HERE, "reports")
os.makedirs(REPORTS, exist_ok=True)

with open(os.path.join(HERE, "config.json")) as f:
    CFG = json.load(f)

UA = {"User-Agent": "Mozilla/5.0 (TrendRadar/1.0; contact: miles@myl0nr0s.cloud)"}


def g_keyword_interest():
    """Interest-over-time (7d) for brand keywords; flag rising keywords."""
    if not HAVE_PYTRENDS:
        return []
    out = []
    try:
        pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 20))
        all_kw = CFG["brand_keywords"]["PSD"] + CFG["brand_keywords"]["AGI"]
        # pytrends max 5 kw per request
        for i in range(0, len(all_kw), 5):
            batch = all_kw[i:i + 5]
            pytrends.build_payload(batch, timeframe="now 7-d", geo="US")
            df = pytrends.interest_over_time()
            if df.empty:
                continue
            df = df.drop(columns=["isPartial"], errors="ignore")
            for kw in batch:
                if kw not in df.columns:
                    continue
                series = df[kw].dropna()
                if len(series) < 2:
                    continue
                first = series.iloc[: len(series) // 2].mean()
                second = series.iloc[len(series) // 2:].mean()
                delta = round(float(second - first), 1)
                out.append({"keyword": kw, "first_half": round(float(first), 1),
                            "second_half": round(float(second), 1), "delta": delta,
                            "trend": "rising" if delta > 3 else ("falling" if delta < -3 else "flat")})
            time.sleep(2)
    except Exception as e:
        out.append({"keyword": "__error__", "trend": f"keyword interest unavailable: {e}"})
    return out


def hn_stories():
    """Hacker News (Algolia API, no auth) — front page pulse + targeted tech/AI/retail queries."""
    out = []
    # Front page
    try:
        r = requests.get("https://hn.algolia.com/api/v1/search",
                         params={"tags": "front_page", "hitsPerPage": CFG["hn_front_page_limit"]},
                         headers=UA, timeout=15)
        for h in r.json().get("hits", []):
            out.append({"scope": "front page", "title": h.get("title", ""),
                        "points": h.get("points", 0), "comments": h.get("num_comments", 0),
                        "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"})
        time.sleep(1)
    except Exception as e:
        out.append({"scope": "front page", "title": f"[error: {e}]", "points": 0, "comments": 0, "url": ""})
    # Targeted queries
    for q in CFG["hn_queries"]:
        try:
            r = requests.get("https://hn.algolia.com/api/v1/search",
                             params={"query": q, "tags": "story", "hitsPerPage": CFG["hn_search_limit"]},
                             headers=UA, timeout=15)
            for h in r.json().get("hits", []):
                out.append({"scope": f'search: "{q}"', "title": h.get("title", ""),
                            "points": h.get("points", 0), "comments": h.get("num_comments", 0),
                            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"})
            time.sleep(1)
        except Exception as e:
            out.append({"scope": f'search: "{q}"', "title": f"[error: {e}]", "points": 0, "comments": 0, "url": ""})
    # dedupe + sort by points
    seen = set()
    dedup = []
    for x in out:
        k = x["title"][:80]
        if k in seen:
            continue
        seen.add(k)
        dedup.append(x)
    dedup.sort(key=lambda x: x.get("points", 0), reverse=True)
    return dedup


def rss_headlines():
    out = []
    for name, url in CFG["rss_feeds"].items():
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[: CFG["rss_item_limit"]]:
                out.append({"source": name, "title": e.get("title", ""),
                            "link": e.get("link", "")})
        except Exception as e:
            out.append({"source": name, "error": str(e)})
    return out


def build_markdown(ts, kw, hn, rss):
    L = []
    L.append(f"# Trend Radar — {ts}")
    L.append("")
    L.append("**Owners:** Echo (TikTok) + Sage (X) pull daily · Dusty (deep sweep) · Max (filter)")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 📈 Brand Keyword Interest (7d, US) — Google Trends")
    L.append("")
    rising = [k for k in kw if k.get("trend") == "rising"]
    falling = [k for k in kw if k.get("trend") == "falling"]
    if rising:
        L.append("**Rising:** " + ", ".join(k["keyword"] for k in rising))
    if falling:
        L.append("**Falling:** " + ", ".join(k["keyword"] for k in falling))
    L.append("")
    for k in kw:
        L.append(f"- {k.get('keyword','?')}: {k.get('trend','?')} (Δ {k.get('delta','?')})")
    if not kw:
        L.append("- (unavailable)")
    L.append("")
    L.append("## 🗣️ Hacker News — tech/AI/retail pulse")
    L.append("")
    for p in hn[:40]:
        L.append(f"- **{p['scope']}** (▲{p['points']}, {p['comments']}c) — {p['title']} — {p['url']}")
    if not hn:
        L.append("- (unavailable)")
    L.append("")
    L.append("## 📰 RSS — industry headlines")
    L.append("")
    for h in rss:
        if "error" in h:
            L.append(f"- ⚠️ {h.get('source')}: {h['error']}")
        else:
            L.append(f"- **{h['source']}** — {h['title']} — {h['link']}")
    if not rss:
        L.append("- (unavailable)")
    L.append("")
    L.append("---")
    L.append(f"*Generated {ts} · trend_radar.py*")
    return "\n".join(L)


def main():
    ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
    print(f"[trend_radar] running for {ts} ...")

    kw = g_keyword_interest()
    hn = hn_stories()
    rss = rss_headlines()

    payload = {
        "date": ts,
        "keyword_interest": kw,
        "hacker_news": hn,
        "rss": rss,
    }

    md_path = os.path.join(REPORTS, f"{ts}.md")
    json_path = os.path.join(REPORTS, f"{ts}.json")

    with open(md_path, "w") as f:
        f.write(build_markdown(ts, kw, hn, rss))
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"[trend_radar] wrote {md_path}")
    print(f"[trend_radar] wrote {json_path}")
    print(f"[trend_radar] kw={len(kw)} hn={len(hn)} rss={len(rss)}")


if __name__ == "__main__":
    main()
