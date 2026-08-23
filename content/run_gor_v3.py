#!/usr/bin/env python3
"""Run v3 (post-council) tasks through the upgraded RiP GoR council."""
import sys, json
sys.path.insert(0, "/root/.aos/aos")
import gor_llm

AGI_DOCKET = """BUSINESS CONTEXT (the actual subject being evaluated):
- "AGI Company" = the autonomous AI operations company run by the Captain. NOT a supply depot.
- Builds autonomous AI agents, AI voice agents, robotics, and agent manifests/personas.
- Real differentiator: FRACTIONAL-HORSEPOWER AI — small local models (tinyllama, gemma2:2b, Mort_II voice) on cheap hardware vs big cloud GPU clusters.
- Positioning (Steve Jobs '83): "do it great or do it so-so" + "the reason we exist is fractional-horsepower AI, five years early"."""

PSD_DOCKET = """BUSINESS CONTEXT (the actual subject being evaluated):
- psdepot.com = "Performance Supply Depot LLC" — a POS (Point-of-Sale) SUPPLY business. NOT Photoshop.
- Products: thermal receipt paper, printer ribbons, POS hardware, cash drawers, Capton bottle pourers, repair services. California since 2005.
- Competitors: pos-depot.com and goldenstateart.com (~13k organic visits/month, ALL from SEO, zero from video).
- On-page SEO already strong; the gap is domain authority + content depth + backlinks + capturing high-intent search."""

tasks = [
    {
        "title": "AGI Company — Contrast-Hook Shorts (RESHAPED v2)",
        "objective": "Short-form channel whose hook is a concrete CONTRAST, not a thesis: 'my billing agent runs on 2GB RAM, not a $10K GPU cluster' / 'I run a company on a $99 mini-PC'. Show REAL screen-recordings of autonomous agents (support/billing/docs) doing work, with a clear offer as CTA ('we run your support for $X/mo' + book-a-demo lead magnet). Jobs '83 'do it great or so-so' as brand positioning anchor (not the hook). Mathis Bolt framework (hook->tension->payoff). KPI = LEAD QUALITY not vanity reach: 20 qualified inbound leads + 10 booked demo calls in 90 days. Validate with a 10-video pilot ($0 ad spend) before scaling.",
        "budget": 2500,
        "time_estimate": 70,
    },
    {
        "title": "psdepot.com SEO + Google Ads (PIVOTED from shorts)",
        "objective": "Capture existing high-intent search demand instead of creating it via Shorts. Optimize product pages + run Google Ads on high-intent keywords ('thermal paper 3 1/8 x 230', 'Capton pourer 1.5oz', 'cash drawer repair', 'Epson printer ribbon') against pos-depot.com and goldenstateart.com (~13k organic visits/mo). On-page SEO is already strong; the gap is domain authority, content depth, backlinks, and paid capture of transactional queries. KPI: organic 0 -> 1,000/mo + 3% paid ROAS-positive on Capton pourer + cash drawer in 90 days.",
        "budget": 1500,
        "time_estimate": 35,
    },
]

dockets = [AGI_DOCKET, PSD_DOCKET]

for task, docket in zip(tasks, dockets):
    gor_llm.DOCKET = docket
    ws, verdict, evals, dir_score = gor_llm.roast(task)
    pmode, pctx = gor_llm.patricia(task, ws, verdict)
    final = gor_llm.gor_verdict(ws, verdict, pmode, dir_score)
    print("\n" + "=" * 70)
    print(f"  ⚖️  GoR VERDICT: {final}   (Roast {ws:.1f}/10 -> {verdict} | dir {dir_score}/10 | Patricia {pmode})")
    print("=" * 70)
    actionable = []
    for n in ("Contrarian", "Researcher", "Buyer"):
        for f in evals.get(n, {}).get("findings", []):
            actionable.append(f"({n}) {f}")
    print("\n  🎯 TOP ACTIONABLE FINDINGS:")
    for f in actionable[:6]:
        print(f"    • {f}")
    print("\n---")
