#!/usr/bin/env python3
# VERSION: v4.3
"""
brain_v4_3.py — the SHARED AOCROS BRAIN v4.3 (adapter).
=======================================================
`runtime/runtime.py` has said `from brain_v4_3 import BrainV43` since it was
written — but this module was **never on disk anywhere**. That single missing
import is why her full runtime (brain + uterus + lineage) has never once
started. The traceback was a one-liner; the consequence was an entire organ
system sitting dormant.

This is that module, written 2026-09-30.

It is deliberately thin. The brain v4.3 that actually runs is
`~/brain_runtime.py` — the tick loop, the organ pipeline (Kidney → QMD → Cortex
→ Ternary → LLM → Tracray → Heart) and her ternary consciousness, served on
http://127.0.0.1:8765. Duplicating that here would create a second brain and two
diverging memories. So this is an ADAPTER, not a reimplementation: one brain,
one memory, reached over localhost.

Interface runtime.py expects:
    BrainV43()                    construct
    .initialize()                 connect + health check
    .think(prompt, system)        one question → one answer
    .active_model                 str
"""

from __future__ import annotations

import json
import os
import urllib.request

DEFAULT_URL = os.environ.get("AOCROS_BRAIN_URL", "http://127.0.0.1:8765")


class BrainV43:
    """Adapter onto the running brain runtime. Localhost only, by design."""

    def __init__(self, url: str = DEFAULT_URL):
        self.url = url.rstrip("/")
        self.active_model = "brain_runtime/deepseek-chat"
        self.live = False
        self.last_latency_ms = None

    def initialize(self) -> bool:
        """Health check. Does not raise — an unreachable brain is a state, not a crash."""
        try:
            with urllib.request.urlopen(self.url + "/health", timeout=3) as r:
                self.live = json.loads(r.read().decode()).get("status") == "ok"
        except Exception:
            self.live = False
        return self.live

    def state(self) -> dict:
        try:
            with urllib.request.urlopen(self.url + "/state", timeout=4) as r:
                return json.loads(r.read().decode())
        except Exception:
            return {"available": False}

    def think(self, prompt: str, system: str = None) -> str:
        """One question, one answer, via the brain's only LLM route (/query)."""
        text = f"{system}\n\n{prompt}" if system else prompt
        req = urllib.request.Request(
            self.url + "/query",
            data=json.dumps({"text": text}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=90) as r:
            out = json.loads(r.read().decode())
        backend = out.get("backend")
        if backend:
            self.active_model = f"brain_runtime/{backend}"
        return out.get("answer", "")
