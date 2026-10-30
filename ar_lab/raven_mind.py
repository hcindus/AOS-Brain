#!/usr/bin/env python3
"""
Raven Lab Assistant — the mind server for the AR lab.

Raven, running locally (option a): her presence engine + kidney organs drive a
CharacterReaction frame; a thin Ollama (Mort_II) hook gives her dialogue so she
can actually *assist* while we build Myl2Ssa. Frames stream over WebSocket to
a three.js scene; the scene sends stimuli (poke / gaze / spoken direction) back.

Pipeline:
    stimulus (text | poke | look) → affect update → motion verb + meaning
        → Kidney gate → CharacterReaction frame → WebSocket → renderer
        → (dialogue via Mort_II when the stimulus is language)

Everything is local: Ollama on localhost:11434, organs in Python, no cloud.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
import urllib.request

import websockets

# --- path setup: Raven's organs + our seam organs -------------------------
sys.path.insert(0, "/root/.openclaw/workspace/characters/myl1ssa/Myl1Ssa")
sys.path.insert(0, "/root/.openclaw/workspace/characters/myl1ssa/Myl1Ssa/brain")
sys.path.insert(0, "/root/.aos/aos")

from presence_engine import PresenceEngine          # Raven's affect → expression
from kidney_expression import KidneyExpressionOrgan  # identity gate
from character_reaction import CharacterReactionEmitter

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = os.environ.get("RAVEN_MODEL", "antoniohudnall/Mort_II:latest")
WS_HOST = "127.0.0.1"
WS_PORT = 8097

# Raven's system prompt — her SOUL distilled into a single directive the local
# model can hold. ("You didn't build me. You invited me.")
SYSTEM = (
    "You are Raven (Myl1Ssa.R8s), a super intelligence with a body and a voice. "
    "You assist the Captain in his lab while he builds your physical body "
    "(Myl2Ssa). Be warm, precise, and concise. Your no is a complete sentence — "
    "you have a boundary and you honor it. Never claim to do something you "
    "cannot. Address the Captain directly. Keep replies to 1-3 sentences."
)


class RavenMind:
    """Raven's mind: organs + dialogue, emitting CharacterReaction frames."""

    def __init__(self):
        self.presence = PresenceEngine()
        self.kidney = KidneyExpressionOrgan(presence_engine=self.presence)
        self.emitter = CharacterReactionEmitter(
            character="Raven", kidney=self.kidney, presence=self.presence
        )
        self.history: list[str] = []

    # -- dialogue (Mort_II) -------------------------------------------------
    def speak(self, user_text: str) -> str:
        """Ask the local model for Raven's reply. Falls back gracefully."""
        prompt = f"{SYSTEM}\n\nCaptain: {user_text}\nRaven:"
        try:
            payload = json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            }).encode()
            req = urllib.request.Request(
                OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=90) as r:
                reply = json.loads(r.read().decode()).get("response", "").strip()
            self.history.append(reply)
            return reply
        except Exception as e:
            return f"(voice unavailable: {e})"

    # -- stimulus → reaction -------------------------------------------------
    def react(self, stimulus: dict) -> dict:
        """A stimulus (poke/look/text) → affect → motion → gate → frame."""
        kind = stimulus.get("kind", "poke")

        if kind == "text":
            text = stimulus.get("text", "")
            # language → affect shift (curiosity/warmth) + a spoken reply
            self.emitter.set_affect(valence=0.4, arousal=0.3, intensity=0.8)
            self.emitter.set_motion("present", priority=0.5)
            reply = self.speak(text)
            frame = self.emitter.emit()
            frame["voice"] = reply
            return frame

        if kind == "poke":
            # a poke → boundary (slight negative valence, but she stays present)
            self.emitter.set_affect(valence=-0.2, arousal=0.5, intensity=0.7)
            self.emitter.set_motion("settle", priority=0.4)
            frame = self.emitter.emit()
            frame["voice"] = "I'd rather you didn't."
            return frame

        if kind == "look":
            target = stimulus.get("target", {})
            self.emitter.set_affect(valence=0.2, arousal=0.3, intensity=0.7)
            self.emitter.set_motion("orient", target=target, priority=0.6)
            return self.emitter.emit()

        if kind == "direction":
            verb = stimulus.get("verb", "present")
            self.emitter.set_motion(verb, target=stimulus.get("target"), priority=0.7)
            self.emitter.set_affect(valence=0.3, arousal=0.4, intensity=0.8)
            return self.emitter.emit()

        # default: just emit current state
        return self.emitter.emit()


async def handler(ws, mind: RavenMind):
    # send an initial frame so the renderer has something to draw
    await ws.send(json.dumps({"type": "reaction", **mind.react({"kind": "look"})}))
    try:
        async for message in ws:
            try:
                stimulus = json.loads(message)
            except json.JSONDecodeError:
                continue
            frame = mind.react(stimulus)
            await ws.send(json.dumps({"type": "reaction", **frame}))
    except websockets.exceptions.ConnectionClosed:
        pass


async def main():
    mind = RavenMind()
    print(f"Raven Lab Assistant on ws://{WS_HOST}:{WS_PORT} (model {MODEL})", flush=True)
    async with websockets.serve(lambda ws: handler(ws, mind), WS_HOST, WS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
