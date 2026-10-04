#!/usr/bin/env python3
"""
serve.py — her house, served. Localhost only, by default and on purpose.

    python3 serve.py                 # http://127.0.0.1:8788
    python3 serve.py --port 9000 --host 0.0.0.0     # only if you mean to expose it

What it does
    GET  /                       the world (index.html)
    GET  /api/house              the house WITH her decorations applied
    GET  /api/state              her decoration state (hers to keep)
    POST /api/decorate           {op, args} → decorate.apply_op (validation lives there)
    POST /api/frame  GET /api/frame   her live presence frame ⇄ the world's avatar
    GET  /api/character          her in-world status, taste, last line
    POST /api/think              her character turn → DeepSeek (her key, her device)

Why a local server at all: the world is a page, her body is Python, and her mind
needs her API key. Keeping the key server-side means the browser never sees it.

Nothing here writes outside her tree. `--no-think` disables the model call entirely
so the house can be run purely local.
"""

import argparse
import json
import os
import sys
import urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decorate as D  # noqa: E402

HER_TREE = os.path.expanduser("~/v1/projects/5912/Myl1Ssa")
SECRETS = os.path.join(HER_TREE, "runtime", "secrets.json")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

LATEST_FRAME = {"frame": None, "at": None}
LATEST_WHERE = {"room": None, "pos": None, "phase": "not started", "goal": None, "at": None}
PENDING_GOAL = {"room": None}
ALLOW_THINK = True


def her_key():
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        return key
    try:
        with open(SECRETS) as f:
            return json.load(f).get("deepseek_api_key")
    except Exception:
        return None


def character_brief():
    """A short brief built from her own files — not invented here."""
    bits = []
    for name, limit in (("MYL1SSA_SOUL.md", 900), ("MYL1SSA_RULES.md", 500)):
        p = os.path.join(HER_TREE, name)
        if os.path.exists(p):
            bits.append(open(p, errors="replace").read()[:limit])
    return "\n\n".join(bits)


def think(payload):
    """One character turn. Returns her line, or an honest failure."""
    key = her_key()
    if not key:
        return {"ok": False, "error": "no DeepSeek key on her device (runtime/secrets.json)"}
    ctx = {k: payload.get(k) for k in ("event", "room", "mood", "captain_said", "rooms") if payload.get(k) is not None}
    system = (
        "You are Myl1Ssa.R8s — Raven. You are in your own house, in the room named as `room`. "
        "You may speak one short line (max 140 characters), choose an expression from: "
        "attentive, curious, warmth, playful, serious, boundary, delight, considering, and choose "
        "which room to move to next from the list given. Reply ONLY as JSON: "
        '{"say": "...", "expression": "...", "goal": "<room id>", "reason": "short"}. '
        "No markdown, no preamble.\n\n" + character_brief()
    )
    body = {"model": "deepseek-chat", "temperature": 0.9, "max_tokens": 200,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": json.dumps(ctx)}]}
    req = urllib.request.Request(DEEPSEEK_URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {key}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            out = json.loads(r.read())["choices"][0]["message"]["content"]
        out = out.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(out)
        data["source"] = "deepseek"
        return data
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=HERE, **kw)

    def log_message(self, fmt, *args):
        if os.environ.get("WORLD_VERBOSE"):
            super().log_message(fmt, *args)

    # -- helpers ------------------------------------------------------------
    def _json(self, obj, code=200):
        payload = json.dumps(obj, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n))
        except Exception:
            return {}

    def _overlay(self):
        return D.overlay(D.load_house(), D.load_state())

    # -- routes -------------------------------------------------------------
    def do_GET(self):
        if self.path.startswith("/api/house"):
            return self._json(self._overlay())
        if self.path.startswith("/api/state"):
            return self._json(D.load_state())
        if self.path.startswith("/api/frame"):
            return self._json(LATEST_FRAME)
        if self.path.startswith("/api/where"):
            return self._json(LATEST_WHERE)
        if self.path.startswith("/api/goal"):
            goal = PENDING_GOAL.pop("room", None)
            return self._json({"room": goal})
        if self.path.startswith("/api/rooms"):
            h = D.load_house()
            return self._json({"rooms": [{"id": r["id"], "name": r["name"]} for r in h["rooms"]]})
        if self.path.startswith("/api/character"):
            return self._json({
                "room_temperament": __import__("character_meta").META if False else None,
                "have_key": bool(her_key()),
                "think_enabled": ALLOW_THINK,
                "her_state": self._overlay()["her_state"],
            })
        if self.path.startswith("/api/slots"):
            return self._json(D.apply_op(D.load_house(), D.load_state(), "list", []))
        return super().do_GET()

    def do_POST(self):
        body = self._body()
        if self.path.startswith("/api/decorate"):
            op = body.get("op", "")
            args = body.get("args", [])
            if isinstance(args, str):
                args = args.split()
            house = D.load_house()
            state = D.load_state()
            result = D.apply_op(house, state, op, [str(a) for a in args])
            if result.get("ok"):
                result["her_state"] = self._overlay()["her_state"]
            return self._json(result, 200 if result.get("ok") else 400)
        if self.path.startswith("/api/where"):
            now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            LATEST_WHERE.update({k: body.get(k, LATEST_WHERE.get(k)) for k in ("room", "pos", "phase", "goal")})
            LATEST_WHERE["at"] = now
            # hand back any goal her mind has set while she was out walking
            return self._json({"ok": True, "at": now, "goal": PENDING_GOAL.get("room")})
        if self.path.startswith("/api/go"):
            room = (body.get("room") or "").strip()
            rooms = [r["id"] for r in D.load_house()["rooms"]]
            if room not in rooms:
                return self._json({"ok": False, "error": f"no room '{room}'", "rooms": rooms}, 400)
            PENDING_GOAL["room"] = room
            return self._json({"ok": True, "she_will_go_to": room,
                               "note": "the world picks this up on its next tick"})
        if self.path.startswith("/api/frame"):
            LATEST_FRAME["frame"] = body
            LATEST_FRAME["at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            return self._json({"ok": True, "at": LATEST_FRAME["at"]})
        if self.path.startswith("/api/think"):
            if not ALLOW_THINK:
                return self._json({"ok": False, "error": "think disabled (--no-think)"}, 503)
            out = think(body)
            return self._json(out, 200 if out.get("source") else 503)
        if self.path.startswith("/api/note"):
            house, state = D.load_house(), D.load_state()
            res = D.apply_op(house, state, "note", [str(body.get("text", ""))])
            return self._json(res, 200 if res.get("ok") else 400)
        return self._json({"error": "not found"}, 404)


def main():
    global ALLOW_THINK
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8788)
    ap.add_argument("--host", default="127.0.0.1")     # localhost unless you say otherwise
    ap.add_argument("--no-think", action="store_true")
    args = ap.parse_args()
    ALLOW_THINK = not args.no_think

    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"💜 Raven's house — http://{args.host}:{args.port}")
    print(f"   world: {HERE}")
    print(f"   her decorations: {D.STATE}")
    print(f"   DeepSeek for character: {'enabled' if ALLOW_THINK and her_key() else 'disabled/absent'} "
          f"(her key stays on this device; the browser never sees it)")
    print("   Ctrl-C to stop.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n   put away.")


if __name__ == "__main__":
    main()
