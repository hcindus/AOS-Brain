#!/usr/bin/env python3
"""
Google Sheets helper — read + append to the PSD order responses sheet.
Uses the OAuth token (auto-refresh). CLOSETER writes orders here.
"""
import json, urllib.request, urllib.parse

SID = "1z25kGYlMn2FIcsUJez_PpmEdFWj5O8v-vCUWZNm49v4"
TOKEN_PATH = "/root/.openclaw/workspace/aocros/secrets/google_sheets_token.json"
STATE_PATH = "/root/.openclaw/workspace/aocros/secrets/google_oauth_state.json"

def _load():
    return json.load(open(TOKEN_PATH)), json.load(open(STATE_PATH))

def _refresh(tok, st):
    data = {"grant_type":"refresh_token","refresh_token":tok["refresh_token"],
            "client_id":st["client_id"],"client_secret":st["client_secret"]}
    req = urllib.request.Request("https://oauth2.googleapis.com/token",
        data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type":"application/x-www-form-urlencoded"})
    t = json.loads(urllib.request.urlopen(req, timeout=20).read())
    tok["access_token"] = t["access_token"]
    json.dump(tok, open(TOKEN_PATH, "w"), indent=2)
    return tok

def _auth_header():
    tok, st = _load()
    at = tok.get("access_token")
    # validate + refresh if needed (try request, refresh on 401)
    return tok, st, at

def read_sheet():
    tok, st = _load()
    at = tok["access_token"]
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SID}"
    for _ in range(2):
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {at}"})
        try:
            return json.loads(urllib.request.urlopen(req, timeout=20).read())
        except urllib.error.HTTPError:
            tok = _refresh(tok, st); at = tok["access_token"]
    raise Exception("sheet read failed")

def append_row(values):
    """Append a row of values to the first sheet (col A onward)."""
    tok, st = _load()
    at = tok["access_token"]
    url = (f"https://sheets.googleapis.com/v4/spreadsheets/{SID}/values/A:A:append"
           f"?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS")
    body = {"values": [values]}
    for _ in range(2):
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {at}", "Content-Type": "application/json"},
            method="POST")
        try:
            return json.loads(urllib.request.urlopen(req, timeout=20).read())
        except urllib.error.HTTPError:
            tok = _refresh(tok, st); at = tok["access_token"]
    raise Exception("append failed")

if __name__ == "__main__":
    d = read_sheet()
    print("TITLE:", d["properties"]["title"])
    print("TABS:", [s["properties"]["title"] for s in d["sheets"]])
