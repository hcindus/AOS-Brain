"""Graduation gate — decides whether a pilot leaves the Training Room.

Routes through the RiP GoR council when the AOS brain socket is available
(real GO / RESHAPE / KILL / ESCALATE verdict); otherwise falls back to a
deterministic score threshold. Either way the verdict is logged.
"""
from __future__ import annotations

import json
import os
import socket
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "runs", "graduation_log.jsonl")
SOCKET = "/tmp/aos_brain.sock"


def _ensure_log():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)


def _log(entry: dict):
    _ensure_log()
    with open(LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def _try_gor(pilot_id: str, score: dict) -> str | None:
    """Ask the RiP GoR council via the AOS brain socket. Returns verdict or None."""
    if not os.path.exists(SOCKET):
        return None
    try:
        task = {
            "title": f"Graduate pilot {pilot_id}",
            "objective": "Deploy RP1 policy after blind hold-out",
            "budget": 0,
            "time_estimate": 0,
            "score": round(score["overall"], 3),
        }
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect(SOCKET)
            s.sendall(json.dumps({"cmd": "gor", "task": task}).encode())
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
        resp = json.loads(data.decode())
        return resp.get("verdict") or (resp.get("result", {}) or {}).get("verdict")
    except Exception:
        return None


def graduate(pilot_id: str, score: dict, min_score: float = 0.5, require_gor: bool = True) -> dict:
    overall = score["overall"]
    verdict = None

    if require_gor:
        verdict = _try_gor(pilot_id, score)

    if verdict is None:
        verdict = "GO" if overall >= min_score else "BACK_TO_TRAINING"

    decision = {
        "ts": time.time(),
        "pilot": pilot_id,
        "overall": round(overall, 4),
        "scenarios": score["scenarios"],
        "verdict": verdict,
    }
    _log(decision)
    return decision
