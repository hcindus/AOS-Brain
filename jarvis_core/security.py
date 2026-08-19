#!/usr/bin/env python3
"""Hotline PIN gate + token auth — multiple PINs, rate-limited, token issuance."""
import os
import time
import secrets
from collections import defaultdict

PIN_ENV = os.environ.get("JARVIS_PIN", "6666,3915")
RATE_LIMIT = 5          # max attempts
RATE_WINDOW = 60        # seconds
TOKEN_TTL = 3600        # 1 hour


class PinGate:
    """Enforces the JARVIS hotline PIN. Accepts multiple valid PINs."""

    def __init__(self, pins: str = PIN_ENV):
        self.pins = {p.strip() for p in pins.split(",") if p.strip()}
        self._attempts = defaultdict(list)   # client -> [timestamps]
        self._tokens = {}                    # token -> expiry epoch

    def check(self, code: str, client: str = "unknown") -> tuple[bool, str]:
        now = time.time()
        recent = [t for t in self._attempts[client] if now - t < RATE_WINDOW]
        self._attempts[client] = recent
        if len(recent) >= RATE_LIMIT:
            return False, "Too many attempts. Try again later."
        if code.strip() in self.pins:
            self._attempts[client] = []
            return True, "Access granted."
        self._attempts[client].append(now)
        return False, "I'm afraid I can't help without the code. Good day."

    def issue_token(self, code: str, client: str = "unknown") -> tuple[str | None, str]:
        ok, msg = self.check(code, client)
        if not ok:
            self._log_failure(client)
            return None, msg
        token = secrets.token_urlsafe(32)
        self._tokens[token] = time.time() + TOKEN_TTL
        return token, "Access granted."

    def validate_token(self, token: str) -> bool:
        if not token:
            return False
        return self._tokens.get(token, 0) > time.time()

    def _log_failure(self, client: str):
        os.makedirs("/var/log/jarvis", exist_ok=True)
        with open("/var/log/jarvis/access.log", "a") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}  PIN-FAILED ({client})\n")
