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
