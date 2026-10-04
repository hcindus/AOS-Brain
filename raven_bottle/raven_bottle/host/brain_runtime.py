#!/usr/bin/env python3
"""
MORTIMER BRAIN RUNTIME
======================
A persistent, observable brain with:

  • Tick loop (heartbeat)      — visible tick marks, OODA phases
  • Node registration          — every organ logs GET / SAVE / SEND
  • LLM wiring                 — DeepSeek (primary) + Ollama (fallback)
  • Agent access               — HTTP API, minimal LLM use
  • Persistent state           — JSON state file + SQLite memory

Organs (pipeline): Kidney → QMD → Cortex → Ternary → LLM → Tracray → Heart

  • Visual Cortex            — camera frame → Qwen3.5-VL (remote) → scene memory
                               The brain SEES via Qwen; it still REASONS on DeepSeek.

Design principle: agents read/write memory and state DIRECTLY (no LLM).
The LLM is only invoked for actual reasoning (/query). Everything else is
a fast local path — this is how we keep LLM use to a minimum.
"""

import base64
import json
import os
import subprocess
import sys
import sqlite3
import threading
import time
import requests
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
HOME = os.path.expanduser("~")
STATE_PATH = os.path.join(HOME, "brain_state.json")
MEMORY_DB = os.path.join(HOME, "brain_memory.db")
LOG_PATH = os.path.join(HOME, "brain.log")

DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY") or ""
if not DEEPSEEK_KEY:
    try:
        with open(os.path.join(os.path.expanduser("~"), "brain_secrets.json")) as _f:
            DEEPSEEK_KEY = json.load(_f).get("deepseek_api_key", "")
    except Exception:
        DEEPSEEK_KEY = ""
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "deepseek-v4-pro:cloud"

# ── Visual Cortex ─────────────────────────────────────────────────────────
# Seeing runs on a vision-capable cloud model; reasoning stays on DeepSeek.
# 2026-09-25: qwen3.5:397b (the original eyes) was RETIRED — it now answers
# HTTP 410 Gone. A remote model is not a fixture; it can vanish overnight, so
# the cortex keeps an ordered chain and fails over instead of going blind.
VISION_MODEL = "gemma4:cloud"                 # primary: fastest + cleanest read (tested 0.8s)
VISION_CHAIN = ["gemma4:cloud", "glm-5.3-flash:cloud", "deepseek-v4.1-flash:cloud"]
VISION_RETIRED = ["qwen3.5:cloud"]            # retired 2026-09-25 00:00 PDT — kept for the record
VISION_PROMPT = ("Describe what you see in this image concisely: the main subjects, "
                 "the setting, and anything notable. 2-4 sentences.")
VISION_DIR = os.path.join(HOME, "brain_vision")
CAMERA_ID = 0                 # 0 = back camera, 1 = front

TICK_INTERVAL = 2.0          # seconds between ticks
PORT = 8765                  # agent access port
PHASES = ["Observe", "Orient", "Decide", "Act"]

# Ternary brain integration (standalone module wired into the Ternary node)
sys.path.insert(0, os.path.join(HOME, "myl0n", "brain"))
try:
    from ternary_brain_v2 import TernaryBrainV2 as TernaryBrain
    TERNARY_AVAILABLE = True
except Exception as _e:
    TERNARY_AVAILABLE = False
    print(f"[ternary] import failed: {_e}", flush=True)

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
def log(msg: str):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# NODE (ORGAN) — registers GET / SAVE / SEND
# ---------------------------------------------------------------------------
class Node:
    """A brain organ that registers its data flow (GET/SAVE/SEND)."""
    def __init__(self, name: str):
        self.name = name
        self.gets = 0
        self.saves = 0
        self.sends = 0
        self.last_op = None
        self.last_detail = ""

    def register(self, op: str, detail: str = ""):
        """Record a data-flow operation. op ∈ {GET, SAVE, SEND}."""
        op = op.upper()
        if op == "GET":
            self.gets += 1
        elif op == "SAVE":
            self.saves += 1
        elif op == "SEND":
            self.sends += 1
        self.last_op = op
        self.last_detail = detail[:80]
        log(f"  [{self.name}] {op} {detail[:60]}")

    def status(self) -> dict:
        return {
            "name": self.name,
            "gets": self.gets,
            "saves": self.saves,
            "sends": self.sends,
            "last_op": self.last_op,
            "last_detail": self.last_detail,
        }

# ---------------------------------------------------------------------------
# MEMORY (SQLite) — fast path, no LLM
# ---------------------------------------------------------------------------
class Memory:
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                type TEXT,
                content TEXT,
                importance REAL DEFAULT 0.5
            );
        """)
        conn.commit()
        conn.close()

    def save(self, content: str, mtype: str = "observation", importance: float = 0.5):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO memories (timestamp, type, content, importance) VALUES (?,?,?,?)",
            (time.time(), mtype, content, importance),
        )
        conn.commit()
        conn.close()

    def get(self, limit: int = 20, query: str = "") -> list:
        conn = sqlite3.connect(self.db_path)
        if query:
            rows = conn.execute(
                "SELECT timestamp, type, content, importance FROM memories "
                "WHERE content LIKE ? ORDER BY timestamp DESC LIMIT ?",
                (f"%{query}%", limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT timestamp, type, content, importance FROM memories "
                "ORDER BY timestamp DESC LIMIT ?", (limit,),
            ).fetchall()
        conn.close()
        return [
            {"time": r[0], "type": r[1], "content": r[2], "importance": r[3]}
            for r in rows
        ]

    def count(self) -> int:
        conn = sqlite3.connect(self.db_path)
        n = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        conn.close()
        return n

# ---------------------------------------------------------------------------
# LLM — slow path, only for reasoning
# ---------------------------------------------------------------------------
class LLM:
    def __init__(self):
        self.calls = 0
        self.last_backend = None

    def think(self, prompt: str, system: str = "") -> str:
        """Call DeepSeek first, fall back to Ollama, then local pattern."""
        self.calls += 1
        # 1) DeepSeek
        try:
            r = requests.post(
                DEEPSEEK_URL,
                headers={"Authorization": f"Bearer {DEEPSEEK_KEY}",
                         "Content-Type": "application/json"},
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500,
                },
                timeout=30,
            )
            if r.status_code == 200:
                self.last_backend = "deepseek"
                return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            log(f"  [LLM] DeepSeek error: {e}")

        # 2) Ollama fallback
        try:
            r = requests.post(
                OLLAMA_URL,
                json={"model": OLLAMA_MODEL,
                      "prompt": f"{system}\n\n{prompt}"},
                timeout=30,
            )
            if r.status_code == 200:
                self.last_backend = "ollama"
                return "".join(
                    json.loads(l).get("response", "")
                    for l in r.text.splitlines() if l.strip()
                ).strip()
        except Exception as e:
            log(f"  [LLM] Ollama error: {e}")

        self.last_backend = "fallback"
        return "[no LLM available]"

# ---------------------------------------------------------------------------
# BRAIN
# ---------------------------------------------------------------------------
class Brain:
    def __init__(self):
        self.name = "Mortimer_Brain_Runtime_v1.0"
        self.tick = 0
        self.phase = PHASES[0]
        self.running = True
        self.started = time.time()

        # Organs
        self.nodes = {
            "Kidney":  Node("Kidney"),
            "QMD":     Node("QMD"),
            "Cortex":  Node("Cortex"),
            "VisualCortex": Node("VisualCortex"),
            "Ternary": Node("Ternary"),
            "LLM":     Node("LLM"),
            "Tracray": Node("Tracray"),
            "Heart":   Node("Heart"),
        }

        self.memory = Memory(MEMORY_DB)
        self.llm = LLM()

        # Wire the standalone ternary brain into the Ternary node
        self.ternary = TernaryBrain() if TERNARY_AVAILABLE else None
        if self.ternary is not None:
            log(f"   Ternary brain wired: {self.ternary.name}")
        else:
            log("   Ternary brain NOT available (stub mode)")

    # -- data flow helpers (register node ops) ------------------------------
    def ingest(self, text: str) -> bool:
        """Kidney filters input → QMD → Cortex → Ternary → Tracray."""
        self.nodes["Kidney"].register("GET", f"input '{text[:40]}'")
        quality = 0.5 + (0.1 if len(text) > 10 else 0)
        if quality < 0.4:
            self.nodes["Kidney"].register("SEND", "excreted (low quality)")
            return False
        self.nodes["Kidney"].register("SEND", f"accepted q={quality:.2f}")

        self.nodes["QMD"].register("GET", "signal from Kidney")
        self.nodes["QMD"].register("SAVE", "pattern encoded")
        self.nodes["QMD"].register("SEND", "to Cortex")

        self.nodes["Cortex"].register("GET", "pattern from QMD")
        self.nodes["Cortex"].register("SEND", "to Ternary")

        self.nodes["Ternary"].register("GET", "from Cortex")
        if self.ternary is not None:
            try:
                tresult = self.ternary.process(text)
                tstatus = tresult.get("status", "?")
                self.nodes["Ternary"].register("SAVE", f"ternary state ({tstatus})")
            except Exception as e:
                self.nodes["Ternary"].register("SAVE", f"ternary error: {e}")
        else:
            self.nodes["Ternary"].register("SAVE", "ternary state (-1/0/1) [stub]")
        self.nodes["Ternary"].register("SEND", "to Tracray")

        self.nodes["Tracray"].register("GET", "experience")
        self.memory.save(text, "experience", importance=quality)
        self.nodes["Tracray"].register("SAVE", f"memory #{self.memory.count()}")

        self.nodes["Heart"].register("GET", "beat")
        self.nodes["Heart"].register("SEND", "pulse")
        return True

    def reason(self, prompt: str) -> str:
        """LLM path — only invoked when actual reasoning is requested."""
        self.nodes["LLM"].register("GET", f"prompt '{prompt[:40]}'")
        out = self.llm.think(prompt, system="You are Mortimer, the General of the Forces. Be concise and useful.")
        self.nodes["LLM"].register("SEND", f"response ({len(out)} chars)")
        self.memory.save(f"Q: {prompt[:80]} → A: {out[:80]}", "reasoning", 0.7)
        return out

    # -- visual cortex (see → describe → remember) --------------------------
    def capture_image(self, cam_id: int = CAMERA_ID) -> str:
        """Grab one frame with the device camera. Returns file path or ''."""
        try:
            os.makedirs(VISION_DIR, exist_ok=True)
            path = os.path.join(
                VISION_DIR, datetime.now().strftime("frame_%Y%m%d-%H%M%S.jpg"))
            r = subprocess.run(["termux-camera-photo", "-c", str(cam_id), path],
                               capture_output=True, timeout=30)
            if os.path.exists(path) and os.path.getsize(path) > 0:
                self.nodes["VisualCortex"].register(
                    "GET", f"frame {os.path.getsize(path) // 1024}KB cam{cam_id}")
                return path
            self.nodes["VisualCortex"].register(
                "GET", f"camera produced nothing (rc={r.returncode})")
        except Exception as e:
            self.nodes["VisualCortex"].register("GET", f"camera error: {e}")
        return ""

    def see(self, image: str = "", prompt: str = VISION_PROMPT) -> dict:
        """Visual cortex: image (path or base64) → Qwen3.5-VL → description.
        With no image, captures a fresh camera frame first."""
        if image and os.path.exists(image):
            with open(image, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
        elif image:
            img_b64 = image          # treat as base64 payload
        else:
            path = self.capture_image()
            if not path:
                return {"ok": False, "error": "camera capture failed"}
            with open(path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()

        # Ordered chain with failover — a retired/5xx upstream must not blind us.
        desc, errors, used = "", [], None
        for model in VISION_CHAIN:
            self.nodes["VisualCortex"].register("SEND", f"image → {model}")
            try:
                r = requests.post(OLLAMA_CHAT_URL, json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt,
                                  "images": [img_b64]}],
                    "stream": False,
                }, timeout=180)
                if r.status_code == 200:
                    desc = (r.json().get("message") or {}).get("content", "").strip()
                    if desc:
                        used = model
                        break
                    errors.append(f"{model}: empty reply")
                else:
                    errors.append(f"{model}: http {r.status_code}")
                    self.nodes["VisualCortex"].register("SAVE", f"{model} http {r.status_code}")
            except Exception as e:
                errors.append(f"{model}: {type(e).__name__}")
        if not desc:
            self.nodes["VisualCortex"].register("SAVE", "all vision models failed")
            return {"ok": False, "error": "; ".join(errors) or "no vision model"}
        if used != VISION_CHAIN[0]:
            self.nodes["VisualCortex"].register("SAVE", f"failed over → {used}")

        if desc:
            self.memory.save(f"[vision] {desc}", "vision", importance=0.6)
            self.nodes["VisualCortex"].register(
                "SAVE", f"vision memory #{self.memory.count()} via {used}")
            self.nodes["VisualCortex"].register("SEND", "scene → Cortex")
        return {"ok": True, "model": VISION_MODEL, "description": desc}

    # -- tick loop ----------------------------------------------------------
    def tick_once(self):
        self.tick += 1
        self.phase = PHASES[(self.tick // 5) % len(PHASES)]
        self.nodes["Heart"].register("GET", f"tick {self.tick}")
        log(f"TICK {self.tick} | phase: {self.phase} | memory: {self.memory.count()} | llm_calls: {self.llm.calls}")
        self._write_state()

    def _write_state(self):
        state = self.state()
        try:
            with open(STATE_PATH, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            log(f"  [state] write error: {e}")

    def state(self) -> dict:
        state = {
            "name": self.name,
            "tick": self.tick,
            "phase": self.phase,
            "uptime_sec": round(time.time() - self.started, 1),
            "memory_items": self.memory.count(),
            "llm_calls": self.llm.calls,
            "llm_backend": self.llm.last_backend,
            "nodes": {k: v.status() for k, v in self.nodes.items()},
        }
        state["ternary"] = self.ternary.state() if self.ternary is not None else {"available": False}
        return state

    def run(self):
        log(f"🧠 {self.name} ONLINE — tick every {TICK_INTERVAL}s")
        log(f"   LLM: DeepSeek ({DEEPSEEK_MODEL}) + Ollama fallback")
        log(f"   Agent API: http://127.0.0.1:{PORT}")
        log(f"   State: {STATE_PATH}")
        while self.running:
            self.tick_once()
            time.sleep(TICK_INTERVAL)

# ---------------------------------------------------------------------------
# AGENT ACCESS — HTTP API (minimal LLM use)
# ---------------------------------------------------------------------------
class BrainHandler(BaseHTTPRequestHandler):
    brain = None  # set by main

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        b = self.brain
        if path == "/state":
            self._json(b.state())
        elif path == "/nodes":
            self._json({k: v.status() for k, v in b.nodes.items()})
        elif path == "/memory":
            q = parse_qs(urlparse(self.path).query).get("q", [""])[0]
            self._json({"count": b.memory.count(), "items": b.memory.get(query=q)})
        elif path == "/ternary":
            if b.ternary is not None:
                self._json(b.ternary.state())
            else:
                self._json({"available": False})
        elif path == "/route":
            # The thyroid router's decision, in one place, so callers (talk.py)
            # never have to re-implement the heuristic and drift from it.
            q = parse_qs(urlparse(self.path).query).get("text", [""])[0]
            if b.ternary is not None:
                self._json({"route": b.ternary.thyroid.route(q),
                            "thyroid": b.ternary.thyroid.status()})
            else:
                self._json({"route": "VPS", "available": False})
        elif path == "/see":
            q = parse_qs(urlparse(self.path).query)
            prompt = q.get("prompt", [VISION_PROMPT])[0]
            cam = int(q.get("cam", [CAMERA_ID])[0])
            path = b.capture_image(cam)
            if not path:
                self._json({"ok": False, "error": "camera capture failed"}, 500)
            else:
                self._json(b.see(path, prompt))
        elif path == "/health":
            self._json({"status": "ok", "tick": b.tick, "phase": b.phase})
        else:
            self._json({"error": "not found", "routes": ["/state", "/nodes", "/memory", "/query", "/save", "/ingest", "/ternary", "/route", "/see", "/health"]}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        b = self.brain
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode() if length else "{}"
        try:
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {"text": raw}

        if path == "/save":
            text = data.get("text", "")
            b.memory.save(text, data.get("type", "agent"), data.get("importance", 0.5))
            b.nodes["Tracray"].register("SAVE", f"agent save '{text[:40]}'")
            self._json({"ok": True, "memory_items": b.memory.count()})

        elif path == "/query":
            # This is the ONLY route that touches the LLM.
            text = data.get("text", "")
            if not text:
                self._json({"error": "missing 'text'"}, 400)
                return
            answer = b.reason(text)
            self._json({"ok": True, "answer": answer, "backend": b.llm.last_backend})

        elif path == "/ingest":
            text = data.get("text", "")
            ok = b.ingest(text)
            self._json({"ok": ok, "tick": b.tick})

        elif path == "/see":
            # Optional image (path or base64); without one, captures a frame.
            img = data.get("image", "")
            prompt = data.get("prompt", VISION_PROMPT)
            self._json(b.see(img, prompt))

        else:
            self._json({"error": "not found"}, 404)

    def log_message(self, *args):
        pass  # keep console clean; brain logs its own activity

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    brain = Brain()
    BrainHandler.brain = brain

    # Start tick loop in a background thread
    tick_thread = threading.Thread(target=brain.run, daemon=True)
    tick_thread.start()

    # Start HTTP agent-access server
    server = HTTPServer(("127.0.0.1", PORT), BrainHandler)
    log(f"📡 Agent API listening on http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        brain.running = False
        log("🛑 Brain shutting down.")

if __name__ == "__main__":
    main()
