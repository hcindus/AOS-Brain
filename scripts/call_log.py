#!/usr/bin/env python3
"""
Call log — every inbound call recorded in DepotChaos (live DB).

Table: `calls` (created on first use) in DepotChaos/depot_chaos.db.

Written by GREET (voice_server.py) + Clerk; one row per call, updated as the
outcome resolves (open -> order / appointment / transferred / notified / ...).

Usage:
  import call_log
  call_log.log_call(call_sid=..., from_num=..., intent=..., transcript=..., outcome="open")
  call_log.update_call(call_sid, outcome="order", order_ref=po, ...)
  call_log.summary_since("2026-11-18T00:00:00+00:00")
"""
import sqlite3
from datetime import datetime, timezone

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS calls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  call_sid TEXT,
  ts TEXT,
  from_num TEXT,
  caller_name TEXT,
  business TEXT,
  intent TEXT,
  transcript TEXT,
  outcome TEXT,
  order_ref TEXT,
  appointment_ref TEXT,
  duration INTEGER,
  notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_calls_sid ON calls(call_sid);
CREATE INDEX IF NOT EXISTS idx_calls_ts ON calls(ts);
"""

_COLS = ["call_sid", "ts", "from_num", "caller_name", "business", "intent",
         "transcript", "outcome", "order_ref", "appointment_ref", "duration", "notes"]


def _conn():
    conn = sqlite3.connect(DB, timeout=30)
    conn.executescript(_SCHEMA)
    return conn


def log_call(**fields):
    """Insert a call row. Returns the new row id."""
    conn = _conn()
    cur = conn.cursor()
    vals = [fields.get(c) for c in _COLS]
    if not vals[1]:  # ts
        vals[1] = datetime.now(timezone.utc).isoformat()
    cur.execute(f"INSERT INTO calls ({','.join(_COLS)}) VALUES ({','.join('?' * len(_COLS))})", vals)
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return rid


def update_call(call_sid, **fields):
    """Update the most recent row for a call_sid (only non-None fields)."""
    if not call_sid:
        return None
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM calls WHERE call_sid=? ORDER BY id DESC LIMIT 1", (call_sid,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return None
    rid = row[0]
    sets, params = [], []
    for k, v in fields.items():
        if v is None or k not in _COLS:
            continue
        sets.append(f"{k}=?")
        params.append(v)
    if sets:
        params.append(rid)
        cur.execute(f"UPDATE calls SET {','.join(sets)} WHERE id=?", params)
        conn.commit()
    conn.close()
    return rid


def latest(call_sid):
    conn = _conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM calls WHERE call_sid=? ORDER BY id DESC LIMIT 1", (call_sid,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None


def summary_since(since_iso=None):
    """Counts grouped by (intent, outcome) since a timestamp (or all time)."""
    conn = _conn()
    cur = conn.cursor()
    if since_iso:
        cur.execute("SELECT intent, outcome, COUNT(*) FROM calls WHERE ts>=? GROUP BY intent, outcome ORDER BY 3 DESC",
                    (since_iso,))
    else:
        cur.execute("SELECT intent, outcome, COUNT(*) FROM calls GROUP BY intent, outcome ORDER BY 3 DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def count_since(since_iso=None):
    conn = _conn()
    cur = conn.cursor()
    if since_iso:
        cur.execute("SELECT COUNT(*) FROM calls WHERE ts>=?", (since_iso,))
    else:
        cur.execute("SELECT COUNT(*) FROM calls")
    n = cur.fetchone()[0]
    conn.close()
    return n


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        for intent, outcome, n in summary_since():
            print(f"{intent or '(none)'}\t{outcome or '(none)'}\t{n}")
    else:
        print("total calls:", count_since())
