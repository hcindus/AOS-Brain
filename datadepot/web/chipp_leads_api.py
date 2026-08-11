#!/usr/bin/env python3
"""
Chipp Leads API — Shared backend for PSD × Chipp lead portal & dashboard.
Stores leads as JSON, serves on port 8086.
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

LEADS_FILE = Path("/var/lib/psdepot/chipp_leads.json")
LOCK_FILE = Path("/var/lib/psdepot/chipp_leads.lock")

app = FastAPI(title="Chipp Leads API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _acquire_lock(timeout=5):
    """Simple file-based lock."""
    start = time.time()
    while LOCK_FILE.exists():
        if time.time() - start > timeout:
            LOCK_FILE.unlink(missing_ok=True)
            break
        time.sleep(0.05)
    LOCK_FILE.touch()


def _release_lock():
    LOCK_FILE.unlink(missing_ok=True)


def read_leads():
    """Read leads from JSON file, return list."""
    if not LEADS_FILE.exists():
        return []
    try:
        with open(LEADS_FILE, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def write_leads(leads):
    """Atomically write leads to JSON file."""
    _acquire_lock()
    try:
        tmp = LEADS_FILE.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(leads, f, indent=2, default=str)
        tmp.replace(LEADS_FILE)
    finally:
        _release_lock()


# ─── Endpoints ────────────────────────────────────────────

@app.get("/api/leads")
async def get_leads():
    """Return all leads."""
    return JSONResponse(read_leads())


@app.post("/api/leads")
async def add_lead(request: Request):
    """Add a single lead."""
    try:
        lead = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    required = ["businessName", "contactName", "email"]
    for field in required:
        if not lead.get(field):
            return JSONResponse({"error": f"Missing required field: {field}"}, status_code=422)

    # Ensure required fields
    lead.setdefault("id", "lead_" + str(int(time.time() * 1000)))
    lead.setdefault("source", lead.get("source", "psd"))
    lead.setdefault("destination", lead.get("destination", "psd"))
    lead.setdefault("status", lead.get("status", "open"))
    lead.setdefault("createdAt", lead.get("createdAt", datetime.utcnow().isoformat() + "Z"))
    lead.setdefault("phone", lead.get("phone", ""))
    lead.setdefault("city", lead.get("city", ""))
    lead.setdefault("state", lead.get("state", ""))
    lead.setdefault("product", lead.get("product", ""))
    lead.setdefault("notes", lead.get("notes", ""))
    lead.setdefault("dateContacted", lead.get("dateContacted", ""))
    lead.setdefault("otherReason", lead.get("otherReason", ""))

    leads = read_leads()
    leads.insert(0, lead)
    write_leads(leads)

    return JSONResponse({"ok": True, "id": lead["id"], "total": len(leads)})


@app.post("/api/leads/bulk")
async def bulk_sync(request: Request):
    """Replace all leads (used by dashboard for full sync)."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    if not isinstance(data, list):
        return JSONResponse({"error": "Expected a list of leads"}, status_code=422)

    write_leads(data)
    return JSONResponse({"ok": True, "total": len(data)})


@app.post("/api/leads/reminders")
async def send_reminders(request: Request):
    """Receive reminder request — stub for now."""
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    stale_count = data.get("totalStale", 0) if isinstance(data, dict) else 0
    return JSONResponse({"ok": True, "message": f"Reminder request received for {stale_count} leads.", "sent": False})


@app.post("/api/leads/update")
async def update_lead(request: Request):
    """Update a single lead status/notes."""
    try:
        update = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    lead_id = update.get("id")
    if not lead_id:
        return JSONResponse({"error": "Missing lead id"}, status_code=422)

    leads = read_leads()
    found = False
    for lead in leads:
        if lead.get("id") == lead_id:
            for key in ("status", "dateContacted", "notes", "otherReason"):
                if key in update:
                    lead[key] = update[key]
            found = True
            break

    if not found:
        return JSONResponse({"error": "Lead not found"}, status_code=404)

    write_leads(leads)
    return JSONResponse({"ok": True, "id": lead_id})


@app.get("/health")
async def health():
    leads = read_leads()
    return {"status": "ok", "lead_count": len(leads)}


if __name__ == "__main__":
    print(f"Leads file: {LEADS_FILE}")
    uvicorn.run(app, host="127.0.0.1", port=8086, log_level="info")
