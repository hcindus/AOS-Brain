#!/usr/bin/env python3
"""Run reshaped viral-shorts tasks through the UPGRADED RiP GoR council (gor_llm.py)."""
import sys, json
sys.path.insert(0, "/root/.aos/aos")
import gor_llm

# Correct per-channel business docket (override the psdepot-SEO default)
AGI_DOCKET = """BUSINESS CONTEXT (the actual subject being evaluated):
- "AGI Company" = the autonomous AI operations company run by the Captain. NOT a supply depot.
- It builds autonomous AI agents, AI voice agents, robotics, and agent manifests/personas.
- Real, differentiated stack: runs FRACTIONAL-HORSEPOWER AI — small local models (tinyllama, gemma2:2b, Mort_II voice) on cheap hardware, not just big cloud models. This is the core differentiator.
- Positioning thesis (Steve Jobs '83): "do it great or do it so-so" + "the reason we exist is fractional-horsepower AI, five years early."
- Goal of this content: authority + inbound leads for agent/automation services."""

PSD_DOCKET = """BUSINESS CONTEXT (the actual subject being evaluated):
- psdepot.com = "Performance Supply Depot LLC" — a POS (Point-of-Sale) SUPPLY business. NOT Photoshop/"PSD" design files.
- Products: thermal receipt paper, printer ribbons, POS hardware, cash drawers, Capton bottle pourers, repair services. Serving California since 2005.
- Competitors: pos-depot.com and goldenstateart.com (~13k organic visits/month).
- Goal of this content: drive e-commerce traffic + brand awareness for POS supplies."""

tasks = [
    {
        "title": "AGI Company Viral Shorts Channel (RESHAPED)",
        "objective": "Launch a short-form channel with the Jobs '83 positioning 'the reason we exist is fractional-horsepower AI, five years early' + 'do it great or do it so-so'. Show REAL agent screen-recordings (support/billing/docs/trading running autonomously), not talking heads — this is the differentiation. Mathis Bolt framework (hook->tension->payoff), 3-4 videos/week, YouTube Shorts first then TikTok+Instagram. KPI: 500K views + 20 qualified inbound leads in 90 days. Validate with a 3-video pilot ($0 ad spend) before committing full hours/budget.",
        "budget": 2000,
        "time_estimate": 40,
    },
    {
        "title": "PSD Viral Shorts Channel (RESHAPED)",
        "objective": "Launch a short-form channel for Performance Supply Depot (POS supplies: receipt paper, ribbons, cash drawers, Capton pourers). Content: satisfying product close-ups + concrete ROI math ('your bartender is pouring away profit' -> Capton 1.5oz pourer). Mathis Bolt framework. 3-4 videos/week, YouTube Shorts first then TikTok+Instagram. KPI: 250K views + 15% lift in e-commerce CTR + 30 email signups in 90 days. Validate with a 3-video pilot before committing.",
        "budget": 1500,
        "time_estimate": 35,
    },
]

dockets = [AGI_DOCKET, PSD_DOCKET]

for task, docket in zip(tasks, dockets):
    gor_llm.DOCKET = docket  # correct context per channel
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
