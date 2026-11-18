#!/usr/bin/env python3
"""
One-time OAuth flow for the Google Calendar scope (performancesupplydepotsales@gmail.com).

Step 1 — generate the auth URL (prints it; Captain opens it and clicks Allow):
    python3 google_calendar_auth.py

Step 2 — exchange the redirect code for a token (Captain pastes the code):
    python3 google_calendar_auth.py --code <PASTE_CODE_HERE>

Token saved to aocros/secrets/google_calendar_token.json (calendar + spreadsheets scopes).
"""
import sys
import os
import json
import base64
import hashlib
import secrets
import urllib.parse
import requests

BASE = "/root/.openclaw/workspace"
CLIENT = f"{BASE}/aocros/secrets/google_oauth_client.json"
STATE = f"{BASE}/aocros/secrets/google_calendar_state.json"
TOKEN = f"{BASE}/aocros/secrets/google_calendar_token.json"

SCOPES = " ".join([
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/spreadsheets",
])

REDIRECT_URI = "http://localhost"


def _client():
    return json.load(open(CLIENT))["installed"]


def _b64url(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _code_challenge(verifier):
    return _b64url(hashlib.sha256(verifier.encode()).digest())


def gen_url():
    c = _client()
    verifier = secrets.token_urlsafe(64)
    challenge = _code_challenge(verifier)
    params = {
        "client_id": c["client_id"],
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode(params)
    json.dump({"code_verifier": verifier, "client_id": c["client_id"]}, open(STATE, "w"), indent=2)
    return url


def exchange(code):
    c = _client()
    state = json.load(open(STATE))
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "code": code,
        "client_id": c["client_id"],
        "client_secret": c["client_secret"],
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": state["code_verifier"],
    }, timeout=30)
    r.raise_for_status()
    tok = r.json()
    tok.setdefault("scope", SCOPES)
    json.dump(tok, open(TOKEN, "w"), indent=2)
    return tok


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--code":
        tok = exchange(sys.argv[2])
        print("TOKEN SAVED")
        print("scope:", tok.get("scope"))
        print("has refresh:", bool(tok.get("refresh_token")))
    else:
        print("Open this URL and click Allow, then paste the 'code' param back:\n")
        print(gen_url())
        print()
