#!/usr/bin/env python3
"""split_body — the Eee PC 900 "body". Executes code locally, borrows a brain remotely.

Brain = Ollama on an M715q (over the 5-port switch). Body = this machine (the netbook).
No model runs here — it's pure hands. Set BRAIN_URL to the brain node's LAN IP.
"""
import os, json, subprocess, urllib.request, sys, time

BRAIN_URL = os.environ.get("BRAIN_URL", "http://192.168.1.10:11434")  # <- set to M715q IP
MODEL     = os.environ.get("BAREAGENT_MODEL", "gemma2:2b")
MEM       = os.path.expanduser("~/.bareagent/memory.log")
os.makedirs(os.path.dirname(MEM), exist_ok=True)

def think(prompt, system=""):
    body = {"model": MODEL, "prompt": prompt, "system": system, "stream": False}
    req = urllib.request.Request(BRAIN_URL + "/api/generate",
          data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))["response"]

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
    "You are an agent whose body is on a remote machine. Each turn emit exactly ONE JSON:\n"
    '{"thought":"...", "action":"run|read|write|done", "arg":"...", "arg2":"..."}\n'
    "Your actions execute on the body (not on you). Use 'done' with final answer in 'arg'. "
    "No prose outside JSON."
)

def remember(text):
    with open(MEM, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")

def agent(goal, max_turns=15):
    ctx = [("user", goal)]
    for _ in range(max_turns):
        out = think(f"GOAL: {goal}\n\nHISTORY:\n" + json.dumps(ctx[-6:]), SYSTEM)
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
        print("usage: split_body.py 'your goal here'"); sys.exit(1)
    print(agent(" ".join(sys.argv[1:])))
