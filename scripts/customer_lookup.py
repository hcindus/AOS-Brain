#!/usr/bin/env python3
"""
Customer lookup against the existing client store (DepotChaos).

Primary source:  DepotChaos/depot_chaos.db -> vendors (data_class='real').
Fallback source: data/backfill_clients.json.

lookup_customer(phone=, email=, name=) -> best-match dict (with '_source' key) or None.

Used by Clerk (voice order-taking) to identify existing vs. new customers so the
payment-before-vendor rule can be applied correctly.
"""
import json
import re
import sqlite3

BASE = "/root/.openclaw/workspace"
LIVE_DB = f"{BASE}/DepotChaos/depot_chaos.db"
BACKFILL = f"{BASE}/data/backfill_clients.json"


def _norm_phone(p):
    if not p:
        return ""
    digits = re.sub(r"\D", "", str(p))
    return digits[-10:] if len(digits) >= 10 else digits


def _norm_email(e):
    return (e or "").strip().lower()


def _norm_name(n):
    return re.sub(r"[^a-z0-9]", "", (n or "").lower())


def _score(phone, email, name, np, ne, nn, cand_phone, cand_email, cand_name):
    s = 0
    if np and _norm_phone(cand_phone) == np:
        s += 100
    if ne and _norm_email(cand_email) == ne:
        s += 80
    if nn and _norm_name(cand_name) == nn:
        s += 60
    return s


def _db_lookup(np, ne, nn):
    try:
        conn = sqlite3.connect(LIVE_DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM vendors WHERE data_class='real'")
        best = None
        for r in cur.fetchall():
            s = _score(r["phone"], r["email"], r["name"], np, ne, nn,
                       r["phone"], r["email"], r["name"])
            if s and (best is None or s > best[0]):
                best = (s, dict(r))
        conn.close()
        return best[1] if best else None
    except Exception:
        return None


def _backfill_lookup(np, ne, nn):
    try:
        data = json.load(open(BACKFILL))
    except Exception:
        return None
    best = None
    for c in data:
        name = c.get("client_name") or c.get("vendor_name") or ""
        s = _score(c.get("phone"), c.get("email"), name, np, ne, nn,
                   c.get("phone"), c.get("email"), name)
        if s and (best is None or s > best[0]):
            best = (s, c)
    return best[1] if best else None


def lookup_customer(phone=None, email=None, name=None):
    """Return the best-matching existing client (dict with '_source') or None."""
    np = _norm_phone(phone)
    ne = _norm_email(email)
    nn = _norm_name(name)
    if not (np or ne or nn):
        return None
    m = _db_lookup(np, ne, nn)
    if m:
        m["_source"] = "depotchaos.vendors"
        return m
    b = _backfill_lookup(np, ne, nn)
    if b:
        b["_source"] = "backfill_clients.json"
        return b
    return None


if __name__ == "__main__":
    import sys
    phone = sys.argv[1] if len(sys.argv) > 1 else None
    name = sys.argv[2] if len(sys.argv) > 2 else None
    r = lookup_customer(phone=phone, name=name)
    print(json.dumps(r, indent=2, default=str) if r else "NO MATCH")
