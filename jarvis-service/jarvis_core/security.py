#!/usr/bin/env python3
"""Hotline PIN gate — 2 attempts, logs failures, never reveals sensitive data."""
import os
from datetime import datetime

PIN = os.environ.get("JARVIS_PIN", "4435")
MAX_ATTEMPTS = 2


class PinGate:
    """Enforces the JARVIS hotline PIN. Returns (granted, message, attempts)."""

    def __init__(self, pin: str = PIN, max_attempts: int = MAX_ATTEMPTS):
        self.pin = pin
        self.max_attempts = max_attempts
        self.attempts = 0

    def check(self, code: str) -> tuple[bool, str]:
        self.attempts += 1
        if code.strip() == self.pin:
            self.attempts = 0
            return True, "Access granted."
        if self.attempts >= self.max_attempts:
            self.attempts = 0
            self._log_failure()
            return False, "I'm afraid I can't help without the code. Good day."
        return False, "May I have the code, please?"

    def _log_failure(self):
        os.makedirs("/var/log/jarvis", exist_ok=True)
        with open("/var/log/jarvis/access.log", "a") as f:
            f.write(f"{datetime.now().isoformat()}  PIN-FAILED (unknown caller)\n")
