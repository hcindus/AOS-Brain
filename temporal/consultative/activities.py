"""Consultative Approach activities — partner-first sales recommendation engine."""
import subprocess
import os
from datetime import datetime, timezone
from temporalio import activity

SALES_MODEL = "nous-hermes2"  # consultative sales voice
OUT_DIR = "/root/.openclaw/workspace/AGI_COMPANY/sales/recommendations"


def _ollama(model, prompt, timeout=300):
    env = dict(os.environ)
    env.setdefault("HOME", "/root")
    env.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")
    r = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True, timeout=timeout, env=env)
    return r.stdout.strip() or f"(empty — {r.stderr[:150]})"


@activity.defn
async def consultative_recommend(prospect_context: str) -> str:
    """Apply the consultative framework (partner -> ask -> diagnose -> prescribe -> present) to a prospect."""
    prompt = (
        "You are a consultative sales advisor for Performance Supply Depot (POS supplies, cash registers, "
        "scales, receipt printers). Apply 'The Consultative Approach': partner, don't pitch; diagnose before "
        "prescribing; lead with the result, not the spec; handle objections with Feel-Felt-Found.\n\n"
        "Given this prospect context, output a concise consultative recommendation:\n"
        "1) The client's likely real need (diagnosis)\n"
        "2) The right solution + why (prescription)\n"
        "3) The result to lead with (outcome, not features)\n"
        "4) Likely objection + how to handle it (Feel-Felt-Found)\n\n"
        f"PROSPECT CONTEXT:\n{prospect_context}"
    )
    rec = _ollama(SALES_MODEL, prompt)

    os.makedirs(OUT_DIR, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    path = os.path.join(OUT_DIR, f"recommendation_{ts}.md")
    with open(path, "w") as f:
        f.write(f"# Consultative Recommendation\n\n**Context:**\n{prospect_context}\n\n**Recommendation:**\n{rec}\n")
    activity.logger.info(f"✅ consultative recommendation -> {path}")
    return path
