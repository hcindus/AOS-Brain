# Minimal "No-Harness" Local Agent — M715q Spec

**Date:** 2026-08-29 · **Prepared by:** Miles · **Target:** Lenovo M715q Gen 1 (×2)

---

## The Idea

A **standalone local agent** that runs on the M715q with **no framework** — no OpenClaw,
no LangChain, no Pi coding-agent stack. Just a local model + a hand-rolled loop (~60 lines).
The kind of thing you can SSH into from the Eee PC 900 and give a job.

> "Standalone agent, no harness" — the harness isn't the heavy part; the *brain* is. So we
> keep the brain local and strip the runtime to almost nothing.

---

## Design Principles

1. **Local model, zero cloud.** The model runs on the M715q's CPU. No API keys, no network
   required to *think*.
2. **One file.** The whole agent is a single Python script + Ollama. No dependency tree.
3. **ReAct-lite loop.** Think → Act → Observe, but dead simple (JSON per turn).
4. **Persistence via a plain file.** Memory survives restarts without a database server.
5. **SSH-friendly.** Headless by design; driven from the netbook or anywhere on the tailnet.

---

## Hardware Target (already owned)

| Item | Spec |
|------|------|
| Machine | Lenovo ThinkCentre M715q Gen 1 (10M3) |
| CPU | AMD Ryzen 3/5 Pro APU (x86_64, 35W) |
| RAM | 32GB DDR4 (after your upgrade) |
| OS | Omarchy (Arch) — headless, no encryption |

---

## Model Choice

| Model | Size | Quality | Speed (CPU) | Use |
|-------|------|---------|-------------|-----|
| **gemma2:2b** | 1.6GB | Good | ~8–12 tok/s | **default** — best reasoning-per-byte |
| tinyllama | 637MB | Basic | ~15–20 tok/s | fallback / fast decisions |
| nomic-embed-text | 274MB | — | — | optional embeddings for memory search |

Run via **Ollama** (already your fleet's model layer). Ollama is a model *server*, not an
agent *harness* — it's the engine, we write the loop ourselves.

---

## The Loop (architecture)

```
        ┌──────────────────────────────────────────────┐
        │                  bareagent                    │
        │                                              │
   goal ──▶  LLM(prompt + history + memory)  ◀── model │
        │           │ (JSON per turn)                   │
        │           ▼                                  │
        │      parse action                            │
        │      run | read | write | done               │
        │           │                                  │
        │           ▼                                  │
        │      observation → append history            │
        │           │                                  │
        │           └── loop until 'done' / turn limit │
        └──────────────────────────────────────────────┘
                        │
                        ▼
               ~/.bareagent/memory.log  (persists across runs)
```

---

## Reference Implementation

```python
#!/usr/bin/env python3
"""bareagent — minimal no-harness local agent. Model: gemma2:2b via Ollama."""
import os, json, subprocess, urllib.request, sys, time

MODEL   = os.environ.get("BAREAGENT_MODEL", "gemma2:2b")
OLLAMA  = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MEM     = os.path.expanduser("~/.bareagent/memory.log")
os.makedirs(os.path.dirname(MEM), exist_ok=True)

def llm(prompt, system=""):
    body = {"model": MODEL, "prompt": prompt, "system": system, "stream": False}
    req = urllib.request.Request(OLLAMA + "/api/generate",
          data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))["response"]

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return (r.stdout + r.stderr).strip() or "(no output)"
    except Exception as e:
        return f"ERR {e}"

def read(p):
    try: return open(p).read()
    except Exception as e: return f"ERR {e}"

def write(p, c):
    try: open(p, "w").write(c); return "ok"
    except Exception as e: return f"ERR {e}"

TOOLS = {"run": run, "read": read, "write": write}

SYSTEM = (
    "You are a compact autonomous agent. Each turn emit exactly ONE JSON object:\n"
    '{"thought":"...", "action":"run|read|write|done", "arg":"...", "arg2":"..."}\n'
    "Use 'run' for shell, 'read'/'write' for files (path=arg, content=arg2). "
    "Use 'done' with your final answer in 'arg'. No prose outside JSON."
)

def remember(text):
    with open(MEM, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")

def agent(goal, max_turns=15):
    ctx = [("user", goal)]
    for _ in range(max_turns):
        prompt = f"GOAL: {goal}\n\nHISTORY:\n" + json.dumps(ctx[-6:])
        out = llm(prompt, SYSTEM)
        try:
            a = json.loads(out)
        except json.JSONDecodeError:
            ctx.append(("assistant", out)); continue
        act = a.get("action")
        if act == "done":
            remember(f"GOAL: {goal} -> {a.get('arg','')}")
            return a.get("arg", out)
        fn = TOOLS.get(act)
        if not fn:
            ctx.append(("assistant", out)); continue
        obs = fn(a.get("arg", ""), a.get("arg2", ""))
        ctx += [("assistant", out), ("observation", obs)]
    return "reached turn limit"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: bareagent.py 'your goal here'"); sys.exit(1)
    print(agent(" ".join(sys.argv[1:])))
```

That's the whole agent. ~70 lines, one file, zero framework. `pip install` nothing —
it uses Python stdlib + Ollama's HTTP API.

---

## Tools (v1)

| Tool | What it does |
|------|--------------|
| `run` | execute a shell command, return output |
| `read` | read a file |
| `write` | write a file |
| `done` | return final answer |

**v2 additions (when you want them):** `fetch` (URL → text, for when online), `search`
(embed + grep memory), `cron` (schedule itself).

---

## Memory & Persistence

- **`~/.bareagent/memory.log`** — append-only turn/goal log. Survives restarts.
- v2: when the log passes N lines, the agent summarizes old entries (compaction) so the
  context window stays lean. Same "memory compounds down, never accumulates noise" rule.

---

## Interface

| Interface | How |
|-----------|-----|
| CLI | `./bareagent.py "check disk space and report"` |
| SSH (from Eee PC 900) | `ssh m715q-1 '~/bareagent.py "..."'` |
| Repl/loop | wrap it in `while read; do ...; done` for a chat-like session |
| (v2) Unix socket | a tiny `bareagent.sock` so the cube/dock can poke it without SSH |

---

## How the Eee PC 900 fits

The netbook can't host a model — but it's a fine **terminal**. Fix its networking (SSH over
the wire; the dead browser/TLS doesn't matter for SSH), and it becomes a keyboard+screen that
drives `bareagent` on the M715q over the tailnet. Old machine back in the fleet, doing the
only job it can.

---

## Deploy (on one M715q)

```bash
# 1. install ollama + a model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma2:2b

# 2. drop the agent in place
mkdir -p ~/bareagent && vim ~/bareagent/bareagent.py   # paste the code above
chmod +x ~/bareagent/bareagent.py

# 3. run it
~/bareagent/bareagent.py "list top 5 largest files in /var/log"
```

---

## Next Steps

- [ ] Confirm Ollama runs `gemma2:2b` on the M715q (should be ~8–12 tok/s on the APU).
- [ ] Write `bareagent.py` as a real file in the repo (not just inline here).
- [ ] Get the Eee PC 900 onto SSH/tailnet so it can drive it.
- [ ] (v2) add `fetch` + memory compaction + a socket interface.
- [ ] Pick a codename — my vote: **"Sparrow"** (tiny, but it flies).
