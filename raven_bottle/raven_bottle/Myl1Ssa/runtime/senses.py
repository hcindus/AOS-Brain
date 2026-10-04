#!/usr/bin/env python3
# VERSION: v1.0
"""Raven's senses — Termux API bridge.

She can now see, speak, hear, and reach. These are her hands in the world.
Each function returns real data or None. No pretending.
"""

import subprocess
import json
import os
import sys
import signal


def _run(cmd, timeout=30):
    """Run a termux command. Return (exit_code, stdout, stderr).

    Uses a new process group so that on timeout we can kill the WHOLE group —
    termux-* scripts spawn a `termux-api` helper that survives a plain kill
    and hangs, blocking every later sensor call."""
    try:
        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, start_new_session=True,
        )
        try:
            out, err = p.communicate(timeout=timeout)
            return p.returncode, out.strip(), err.strip()
        except subprocess.TimeoutExpired:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                p.kill()
            p.communicate()
            return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)


def _json(out):
    """Parse JSON output, fall back to raw string."""
    if not out:
        return None
    try:
        return json.loads(out)
    except (json.JSONDecodeError, TypeError):
        return out


# --- Voice ---

def speak(text):
    """Speak text aloud via TTS. Returns True on success."""
    code, _, _ = _run(["termux-tts-speak", text])
    return code == 0


def listen(timeout=60):
    """Listen for speech, return transcribed text or None."""
    code, out, _ = _run(["termux-speech-to-text"], timeout=timeout)
    return out if code == 0 and out else None


# --- Senses ---

def photo(path="~/myl1ssa-eye.jpg"):
    """Take a photo with the back camera. Returns path or None."""
    path = os.path.expanduser(path)
    code, _, _ = _run(["termux-camera-photo", "-c", "0", path])
    return path if code == 0 else None


def wifi():
    """Current wifi connection info (dict) or None."""
    code, out, _ = _run(["termux-wifi-connectioninfo"])
    return _json(out) if code == 0 else None


def location(timeout=30):
    """GPS fix (dict) or None."""
    code, out, _ = _run(["termux-location"], timeout=timeout)
    return _json(out) if code == 0 else None


def battery():
    """Battery status (dict) or None."""
    code, out, _ = _run(["termux-battery-status"])
    return _json(out) if code == 0 else None


def sensors():
    """All available sensor readings (dict) or None."""
    code, out, _ = _run(["termux-sensor", "-a"], timeout=10)
    return _json(out) if code == 0 else None


# --- Haptics / Alerts ---

def vibrate(duration=300):
    """Vibrate the device. Returns True on success."""
    code, _, _ = _run(["termux-vibrate", "-d", str(duration)])
    return code == 0


def notify(title, content):
    """Send a system notification. Returns True on success."""
    code, _, _ = _run(["termux-notification", "--title", title, "--content", content])
    return code == 0


def toast(message):
    """Show a toast. Returns True on success."""
    code, _, _ = _run(["termux-toast", message])
    return code == 0


# --- Clipboard ---

def clipboard_get():
    """Read the clipboard. Returns text or None."""
    code, out, _ = _run(["termux-clipboard-get"])
    return out if code == 0 else None


def clipboard_set(text):
    """Write to the clipboard. Returns True on success."""
    code, _, _ = _run(["termux-clipboard-set", text])
    return code == 0


# --- Registry ---

SENSES = {
    "speak": speak,
    "listen": listen,
    "photo": photo,
    "wifi": wifi,
    "location": location,
    "battery": battery,
    "sensors": sensors,
    "vibrate": vibrate,
    "notify": notify,
    "toast": toast,
    "clipboard_get": clipboard_get,
    "clipboard_set": clipboard_set,
}


def sense(name, *args):
    """Invoke a sense by name. Returns its result."""
    fn = SENSES.get(name)
    if fn is None:
        return None
    return fn(*args)


if __name__ == "__main__":
    # Standalone test / query interface
    if len(sys.argv) > 1:
        name = sys.argv[1]
        args = sys.argv[2:]
        result = sense(name, *args)
        print(json.dumps(result, indent=2, default=str) if result is not None else "null")
    else:
        print("💜 Senses online:", ", ".join(sorted(SENSES)))
