#!/usr/bin/env python3
"""
Performance Supply Depot — Frontline SOA (Service Oriented Assistant)

FastAPI service exposing the front-desk intake engine + a live operations
dashboard. One entry point for every inbound channel (voice / email / text /
web / dm): classify intent -> route to fleet agents -> persist -> alert.

Run:
  python3 server.py                 # uvicorn on 127.0.0.1:8120
  FRONTLINE_PORT=8120 python3 server.py
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from engine import Engine, InboundEvent
from store import Store
from alert import Alert

BASE_DIR = Path(__file__).parent
CONFIG = yaml.safe_load(open(BASE_DIR / "config.yaml"))

VERSION = "1.0.0"
engine = Engine(CONFIG)
store = Store(CONFIG["store"]["db_path"])
alert = Alert(CONFIG)
STARTED = datetime.now(timezone.utc)

app = FastAPI(
    title="Frontline SOA",
    version=VERSION,
    description="Performance Supply Depot — Service Oriented Assistant (front-desk intake engine).",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


class InboundPayload(BaseModel):
    channel: str = Field("voice", description="voice|email|text|web|dm")
    from_: str = Field("", alias="from")
    body: str = Field(..., description="raw message / transcript")


# ---------------------------------------------------------------------------
# pages
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(str(BASE_DIR / "static" / "index.html"))


# ---------------------------------------------------------------------------
# health
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    uptime = (datetime.now(timezone.utc) - STARTED).total_seconds()
    return {
        "status": "ok",
        "service": "frontline-soa",
        "version": VERSION,
        "uptime_seconds": round(uptime),
        "started": STARTED.isoformat(),
        "model": engine.llm.model,
    }


# ---------------------------------------------------------------------------
# intake (core) + dry-run classify
# ---------------------------------------------------------------------------
def _classify(channel: str, from_: str, body: str):
    event = InboundEvent(channel=channel, from_=from_, body=body)
    route = engine.classify(event)
    return event, route


@app.post("/api/inbound")
def inbound(payload: InboundPayload):
    """Full intake: classify -> persist -> alert -> return the Route."""
    event, route = _classify(payload.channel, payload.from_, payload.body)
    store.log(event, route)
    alert.dispatch(event, route)
    return {
        "route": {
            "intent": route.intent,
            "urgency": route.urgency,
            "entity": route.entity,
            "qualified": route.qualified,
            "agents": route.agents,
            "summary": route.summary,
        },
        "stored": True,
        "alerted": bool(alert.bot_token and alert.chat_id),
    }


@app.post("/api/classify")
def classify(payload: InboundPayload):
    """Dry-run: classify + route only (no persistence, no alert)."""
    _, route = _classify(payload.channel, payload.from_, payload.body)
    return {
        "intent": route.intent,
        "urgency": route.urgency,
        "entity": route.entity,
        "qualified": route.qualified,
        "agents": route.agents,
        "summary": route.summary,
    }


# ---------------------------------------------------------------------------
# read endpoints (feed, stats, config surfaces)
# ---------------------------------------------------------------------------
def _rows():
    con = sqlite3.connect(CONFIG["store"]["db_path"])
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        "SELECT id, ts, channel, from_, body, intent, urgency, entity, "
        "qualified, agents, summary FROM inbound ORDER BY ts DESC LIMIT 200"
    )
    rows = [dict(r) for r in cur.fetchall()]
    con.close()
    for r in rows:
        r["entity"] = json.loads(r["entity"]) if r["entity"] else {}
        r["agents"] = json.loads(r["agents"]) if r["agents"] else []
    return rows


@app.get("/api/inbound")
def list_inbound(limit: int = 50, intent: str = None, qualified: str = None):
    rows = _rows()
    if intent:
        rows = [r for r in rows if r["intent"] == intent]
    if qualified:
        rows = [r for r in rows if r["qualified"] == qualified]
    return {"count": len(rows), "items": rows[:limit]}


@app.get("/api/stats")
def stats():
    rows = _rows()
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    by_intent, by_qualified, by_channel = {}, {}, {}
    today_count = 0
    for r in rows:
        by_intent[r["intent"]] = by_intent.get(r["intent"], 0) + 1
        by_qualified[r["qualified"]] = by_qualified.get(r["qualified"], 0) + 1
        by_channel[r["channel"]] = by_channel.get(r["channel"], 0) + 1
        if (r["ts"] or "").startswith(today):
            today_count += 1

    return {
        "total": len(rows),
        "today": today_count,
        "by_intent": by_intent,
        "by_qualified": by_qualified,
        "by_channel": by_channel,
        "agents": _agent_count(rows),
    }


def _agent_count(rows):
    counts = {}
    for r in rows:
        for a in r["agents"]:
            counts[a] = counts.get(a, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


@app.get("/api/suites")
def suites():
    return {
        "suites": CONFIG.get("suites", {}),
        "routing": CONFIG.get("routing", {}),
        "model": engine.llm.model,
    }


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("FRONTLINE_PORT", "8120"))
    uvicorn.run("server:app", host="127.0.0.1", port=port, reload=False)
