#!/usr/bin/env python3
"""
RiP GoR v2 — REAL LLM-backed council (replaces the stub roast_skill.py path).
Each persona is evaluated by qwen2.5:14b via the Ollama HTTP API, then
Patricia adds strategic context, then a GoR verdict is produced.

Usage: python3 gor_llm.py '<task_json>'
"""
import json, sys, os, urllib.request, re

# Load DeepSeek key from the standard env file(s)
for envfile in ("/root/.deepseek_env", "/root/.hermes/.env"):
    if os.path.exists(envfile):
        for line in open(envfile):
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = "deepseek-chat"

def call_llm(system, prompt, max_tokens=600):
    url = BASE_URL + "/chat/completions"
    body = {"model": MODEL,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": prompt}],
            "temperature": 0.7, "max_tokens": max_tokens}
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read().decode())
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[LLM ERROR: {e}]"

PERSONAS = {
    "Contrarian":   (0.25, "You are the Contrarian (Fatal Flaw Finder) on an adversarial review council. Find every fatal flaw, every reason this WILL fail, and every hidden/untested assumption. Be brutal, specific, and honest."),
    "Expansionist": (0.15, "You are the Expansionist (Upside Maximizer). Find the biggest possible upside, adjacent opportunities, and scale potential. Be optimistic but grounded."),
    "FirstPrinciples": (0.20, "You are the FirstPrinciples (Logic Purist). Strip away assumptions and find the core truth. What is actually required vs nice-to-have? What is the simplest path?"),
    "Researcher":   (0.20, "You are the Researcher (Market Intelligence). Bring real market data, competitor intel, and demand signals. Ground analysis in facts and numbers."),
    "Buyer":        (0.20, "You are the Buyer (Customer Proxy). Would you actually pay for this? What is your biggest objection? What would make you choose a competitor instead?"),
}

# Two-axis separation: "is the DIRECTION sound?" vs "is it RESOURCED?"
# A good direction with a low budget should be RESHAPE, not KILL.
DIRECTION_PERSONAS = ("Expansionist", "FirstPrinciples", "Researcher", "Buyer")
RESOURCE_PERSONAS  = ("Contrarian", "FirstPrinciples", "Researcher")

# BUSINESS DOCKET — injected into every roast so the council reasons about the
# REAL subject, not a hallucinated one. Fixes the "psdepot = PSD/Photoshop" error.
DOCKET = """BUSINESS CONTEXT (the actual subject being evaluated):
- psdepot.com = "Performance Supply Depot LLC" — a POS (Point-of-Sale) SUPPLY business. NOT Photoshop / "PSD" design files.
- Products: thermal receipt paper, printer ribbons, POS hardware, cash drawers, and repair services. Serving California since 2005.
- Competitors: pos-depot.com (The POS Depot — POS cards/cables, WooCommerce) and goldenstateart.com (receipt paper, ~13,000 organic visits/month).
- Current state: ~0 organic traffic, but on-page SEO is ALREADY strong (keyword-rich title/H1/meta, LocalBusiness + FAQPage + Product schema). The gap is domain authority + content depth + backlinks, NOT on-page basics.
- "psdepot" = POS depot. Never interpret it as "PSD depot" (Photoshop templates)."""

def parse(out):
    score = None
    m = re.search(r'SCORE\s*:\s*([\d.]+)', out)
    if m:
        try: score = float(m.group(1))
        except: score = None
    findings = re.findall(r'^\s*[-*]\s*(.+)$', out, re.M)
    if not findings:
        findings = [l.strip() for l in out.splitlines() if l.strip() and 'SCORE' not in l][:3]
    return score, findings[:3]

def roast(task):
    print("=" * 70)
    print(f"  RiP GoR — REAL COUNCIL — {task.get('title','Untitled')}")
    print("=" * 70)
    print("\n[Stage 1] 🔥 ROAST COUNCIL (qwen2.5:14b)\n")
    evals = {}
    tpl = (DOCKET + "\n\nEvaluate this business initiative and give your honest assessment.\n\n"
           "TITLE: {title}\nOBJECTIVE: {objective}\nBUDGET: ${budget}\nTIME ESTIMATE: {time_estimate} hours\n\n"
           "Respond in EXACTLY this format (no preamble):\n"
           "SCORE: <number 0-10>\nFINDINGS:\n- <specific finding 1>\n- <specific finding 2>\n- <specific finding 3>")
    prompt = tpl.format(**task)
    weighted = 0.0; total_w = 0.0
    for name, (w, sysp) in PERSONAS.items():
        out = call_llm(sysp, prompt)
        score, findings = parse(out)
        if score is None: score = 5.0
        score = max(0.0, min(10.0, score))
        evals[name] = {"score": round(score,1), "findings": findings}
        weighted += score * w; total_w += w
        print(f"  🎭 {name:16s} → {score:.1f}/10")
        for f in findings:
            print(f"        • {f}")
        print()
    ws = weighted / total_w if total_w else 5.0
    verdict = "GREEN_LIGHT" if ws >= 7.0 else ("RESHAPE" if ws >= 5.0 else "KILL")
    # Direction score: average of the "is this a good idea?" personas (excludes Contrarian's resourcing bias)
    dir_scores = [evals[n]["score"] for n in DIRECTION_PERSONAS if n in evals]
    dir_score = sum(dir_scores) / len(dir_scores) if dir_scores else ws
    return ws, verdict, evals, round(dir_score, 1)

def patricia(task, ws, verdict):
    print("[Stage 2] 🎯 PATRICIA (DMCIA specialist)\n")
    sysp = ("You are Patricia, a DMCIA (Decision-Making, Coordination, Intelligence, and Alignment) specialist / strategic chief of staff. "
            "You MUST pick exactly ONE alignment: ALIGNED, URGENT, DEFERRED, or MISALIGNED. "
            "NEEDS_CLARITY is FORBIDDEN unless the objective is genuinely unparseable. "
            "Then give the single most important change that would move this initiative forward (one sentence).")
    tpl = (DOCKET + "\n\nAssess strategic alignment for:\nTITLE: {title}\nOBJECTIVE: {objective}\n"
           "Roast weighted score: {ws:.1f}/10 (verdict {verdict})\n\n"
           "Output format:\nALIGNMENT: <ALIGNED|URGENT|DEFERRED|MISALIGNED>\nCHANGE: <one concrete sentence>")
    out = call_llm(sysp, tpl.format(**task, ws=ws, verdict=verdict))
    mode = "NEEDS_CLARITY"
    for m in ("MISALIGNED","DEFERRED","URGENT","ALIGNED","NEEDS_CLARITY"):
        if m in out.upper():
            mode = m; break
    # If it still says NEEDS_CLARITY, force a decision based on roast score
    if mode == "NEEDS_CLARITY":
        mode = "ALIGNED" if ws >= 5.0 else "MISALIGNED"
    print("  " + out)
    return mode, out

def gor_verdict(ws, verdict, pat_mode, dir_score):
    # Two-axis: direction quality + resourcing, not a single collapsed score.
    if pat_mode == "MISALIGNED":
        final = "KILL"
    elif pat_mode == "DEFERRED":
        final = "RESHAPE"
    elif verdict == "GREEN_LIGHT":
        final = "GO"
    elif dir_score >= 6.0:
        # Good direction but under-resourced / needs polish → RESHAPE (resourcing), not KILL
        final = "RESHAPE"
    elif ws >= 5.0:
        final = "RESHAPE"
    else:
        final = "KILL"
    return final

if __name__ == "__main__":
    task = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {
        "title": "psdepot.com SEO — Organic Traffic Acquisition",
        "objective": "Grow psdepot.com organic traffic from ~0 to 1,000+/mo in 90 days by ranking top-5 for thermal receipt paper, POS paper rolls, and Epson printer ribbon keywords vs goldenstateart.com (13k/mo) and pos-depot.com.",
        "budget": 2000, "time_estimate": 40}
    ws, verdict, evals, dir_score = roast(task)
    pmode, pctx = patricia(task, ws, verdict)
    final = gor_verdict(ws, verdict, pmode, dir_score)
    # Surface top actionable findings (Contrarian + Researcher = the "what to fix" personas)
    actionable = []
    for n in ("Contrarian", "Researcher", "Buyer"):
        for f in evals.get(n, {}).get("findings", []):
            actionable.append(f"({n}) {f}")
    print("\n" + "=" * 70)
    print(f"  ⚖️  GoR VERDICT: {final}   (Roast {ws:.1f}/10 → {verdict} | dir {dir_score}/10 | Patricia {pmode})")
    print("=" * 70)
    print("\n  🎯 TOP ACTIONABLE FINDINGS:")
    for f in actionable[:5]:
        print(f"    • {f}")
    print(json.dumps({"roast_score": round(ws,2), "direction_score": dir_score,
                      "roast_verdict": verdict, "patricia_mode": pmode,
                      "gor_verdict": final, "personas": evals}, indent=2, default=str))
