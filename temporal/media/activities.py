"""Media & Advertising activities — generate + review (Jordan → Patricia)."""
import subprocess
import os
from datetime import datetime, timezone
from temporalio import activity

REVIEW_DIR = "/root/.openclaw/workspace/AGI_COMPANY/media_advertising/content/review"

# Agent -> (model, cadence description)
AGENTS = {
    "max":   ("qwen2.5:14b",   "Director — weekly calendar + cross-post routing"),
    "sage":  ("nous-hermes2",  "X/Twitter — 2 short-form posts"),
    "nova":  ("qwen3.5",       "YouTube — video idea + title"),
    "iris":  ("qwen3.5",       "Instagram — caption + visual concept"),
    "reed":  ("nous-hermes2",  "Facebook — community post + ad copy"),
    "echo":  ("qwen3.5",       "TikTok — hook + 30s script"),
}

# Review gate: Jordan (first-pass) -> Patricia (second-pass) -> Captain (manual)
JORDAN_MODEL = "qwen3.5"
PATRICIA_MODEL = "qwen2.5:14b"


def _ollama(model: str, prompt: str, timeout: int = 400) -> str:
    env = dict(os.environ)
    env.setdefault("HOME", "/root")
    env.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")
    r = subprocess.run(
        ["ollama", "run", model, prompt],
        capture_output=True, text=True, timeout=timeout, env=env,
    )
    out = r.stdout.strip()
    if not out:
        out = f"(empty — stderr: {r.stderr[:200]})"
    return out


def _prompt_for(agent: str) -> str:
    brand = ("Performance Supply Depot (POS supplies, cash registers, scales, receipt printers) "
             "and AGI Company Services (AI agents, autonomy).")
    voice = ("Voice: 'Intelligence Engineered.' Specific, measurable, no hype. "
             "Banned words: revolutionary, game-changing, disruptive, synergy, leverage.")
    prompts = {
        "sage": f"You are Sage, X/Twitter content strategist for {brand} {voice} "
                "Write 2 short, punchy posts (under 280 chars each). One about POS supplies, one about AI agents. Numbered list.",
        "nova": f"You are Nova, YouTube producer for {brand} {voice} "
                "Propose 1 video idea with a hook title and a 3-point outline.",
        "iris": f"You are Iris, Instagram creative lead for {brand} {voice} "
                "Write 1 caption + describe the visual concept.",
        "reed": f"You are Reed, Facebook community & ads manager for {brand} {voice} "
                "Write 1 community post AND 1 short paid-ad headline + body.",
        "echo": f"You are Echo, TikTok creator for {brand} {voice} "
                "Write 1 hook (first 2 seconds) + a 30-second script outline.",
        "max":  f"You are Max, Director of Media & Advertising for {brand} {voice} "
                "Draft the week's content calendar: 3 ideas per brand, mapped to platform.",
    }
    return prompts[agent]


@activity.defn
async def generate_content(agent: str) -> str:
    model, _ = AGENTS[agent]
    prompt = _prompt_for(agent)
    output = _ollama(model, prompt)

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    d = os.path.join(REVIEW_DIR, day)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{agent}.md")
    with open(path, "w") as f:
        f.write(f"# {agent.title()} — draft ({day})\n\nModel: {model}\n\n{output}\n")

    activity.logger.info(f"✅ {agent} draft -> {path}")
    return path


@activity.defn
async def jordan_review(agent: str, draft_path: str) -> str:
    """Jordan (first-pass): factual accuracy, tone, ops consistency."""
    draft = open(draft_path).read()
    prompt = ("You are Jordan, Sales Operations reviewer for Performance Supply Depot. "
              "Review this content draft for factual accuracy, tone, and operational consistency. "
              "Be concise. Output: (1) what's solid, (2) what needs fixing, (3) verdict APPROVE or REVISE.\n\n"
              f"DRAFT:\n{draft}")
    notes = _ollama(JORDAN_MODEL, prompt)

    with open(draft_path, "a") as f:
        f.write(f"\n\n---\n## Jordan Review (first-pass)\n\n{notes}\n")
    activity.logger.info(f"✅ Jordan reviewed {agent}")
    return notes


@activity.defn
async def patricia_review(agent: str, draft_path: str) -> str:
    """Patricia (second-pass): on-brand, strategic alignment, 'is this a good idea'."""
    draft = open(draft_path).read()
    prompt = ("You are Patricia, strategic advisor for Performance Supply Depot (voice: 'Intelligence Engineered'). "
              "Review this content draft for brand alignment and strategic fit. Is it on-brand? Is it a good idea? "
              "Be concise. Output: (1) brand fit, (2) strategic concern (if any), (3) verdict APPROVE or REVISE.\n\n"
              f"DRAFT:\n{draft}")
    notes = _ollama(PATRICIA_MODEL, prompt)

    with open(draft_path, "a") as f:
        f.write(f"\n\n---\n## Patricia Review (second-pass)\n\n{notes}\n")
    activity.logger.info(f"✅ Patricia reviewed {agent}")
    return notes
