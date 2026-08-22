"""Media & Advertising activities — each agent's job calls a local Ollama model."""
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

def _prompt_for(agent: str) -> str:
    brand = ("Performance Supply Depot (POS supplies, cash registers, scales, receipt printers) "
             "and AGI Company Services (AI agents, autonomy).")
    voice = ("Voice: 'Intelligence Engineered.' Specific, measurable, no hype. "
             "Banned words: revolutionary, game-changing, disruptive, synergy, leverage.")
    prompts = {
        "sage": f"You are Sage, X/Twitter content strategist for {brand} {voice} "
                "Write 2 short, punchy posts (under 280 chars each). One about POS supplies, one about AI agents. "
                "Output as a numbered list.",
        "nova": f"You are Nova, YouTube producer for {brand} {voice} "
                "Propose 1 video idea with a hook title and a 3-point outline.",
        "iris": f"You are Iris, Instagram creative lead for {brand} {voice} "
                "Write 1 caption + describe the visual concept (what image/visual to pair).",
        "reed": f"You are Reed, Facebook community & ads manager for {brand} {voice} "
                "Write 1 community post AND 1 short paid-ad headline + body.",
        "echo": f"You are Echo, TikTok creator for {brand} {voice} "
                "Write 1 hook (first 2 seconds) + a 30-second script outline.",
        "max":  f"You are Max, Director of Media & Advertising for {brand} {voice} "
                "Draft the week's content calendar: 3 ideas per brand, mapped to platform (X/IG/FB/TikTok/YouTube).",
    }
    return prompts[agent]


@activity.defn
async def generate_content(agent: str) -> str:
    model, _ = AGENTS[agent]
    prompt = _prompt_for(agent)
    try:
        env = dict(os.environ)
        env.setdefault("HOME", "/root")
        env.setdefault("PATH", "/usr/local/bin:/usr/bin:/bin")
        r = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, timeout=300, env=env,
        )
        output = r.stdout.strip() or f"(empty — stderr: {r.stderr[:200]})"
    except Exception as e:
        output = f"(ollama error: {e})"

    # Save to review queue (Jordan -> Patricia -> Captain)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    d = os.path.join(REVIEW_DIR, day)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{agent}.md")
    with open(path, "w") as f:
        f.write(f"# {agent.title()} — draft ({day})\n\nModel: {model}\n\n{output}\n")

    activity.logger.info(f"✅ {agent} draft saved to {path}")
    return path
