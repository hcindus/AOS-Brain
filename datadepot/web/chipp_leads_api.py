#!/usr/bin/env python3
"""
Chipp Leads API — Shared backend for PSD × Chipp lead portal & dashboard.
Stores leads as JSON, serves on port 8086.
"""

import json
import os
import time
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

LEADS_FILE = Path("/var/lib/psdepot/chipp_leads.json")
LOCK_FILE = Path("/var/lib/psdepot/chipp_leads.lock")

# ─── Email notification routing ───────────────────────────────
# Which partner gets notified when a lead is logged for their destination.
DESTINATION_EMAILS = {
    "psd": "info@psdepot.com",
    "chipp": "steven@chipp.cc",
    "witzend": "lisa@witzendbeverages.com",
}

SMTP_SERVER = os.getenv("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com")
SMTP_PORT = int(os.getenv("HOSTINGER_SMTP_PORT", "587"))
SMTP_USER = os.getenv("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud")
SMTP_PASS = os.getenv("HOSTINGER_SMTP_PASS", "")
FROM_EMAIL = os.getenv("SMTP_FROM", "miles@myl0nr0s.cloud")
FROM_NAME = "Performance Supply Depot — Lead Portal"

DEST_LABELS = {"psd": "PSDepot", "chipp": "Chipp", "witzend": "WitzEnd"}


def notify_new_lead(lead: dict):
    """Email the destination partner when a new lead is logged.
    Fires ONLY here (new-lead path), never on bulk sync or update."""
    dest = lead.get("destination", "psd")
    to_email = DESTINATION_EMAILS.get(dest)
    if not to_email:
        return

    biz = lead.get("businessName", "Unknown")
    contact = lead.get("contactName", "")
    product = lead.get("product", "")
    city = lead.get("city", "")
    state = lead.get("state", "")
    address = lead.get("address", "")
    zip_ = lead.get("zip", "")
    phone = lead.get("phone", "")
    email = lead.get("email", "")
    notes = lead.get("notes", "")

    subject = f"New Lead → {DEST_LABELS.get(dest, dest)}: {biz}"

    html = f"""<div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;color:#1a1a1a;">
<h2 style="margin:0 0 4px;">🎯 New Lead Logged</h2>
<p style="color:#666;margin:0 0 20px;">Routed to <strong>{DEST_LABELS.get(dest, dest)}</strong></p>
<table cellpadding="8" style="border-collapse:collapse;width:100%;">
<tr><td style="background:#f5f5f5;font-weight:bold;width:140px;">Business</td><td>{biz}</td></tr>
<tr><td style="background:#f5f5f5;font-weight:bold;">Contact</td><td>{contact}</td></tr>
<tr><td style="background:#f5f5f5;font-weight:bold;">Email</td><td>{email}</td></tr>
<tr><td style="background:#f5f5f5;font-weight:bold;">Phone</td><td>{phone or '—'}</td></tr>
<tr><td style="background:#f5f5f5;font-weight:bold;">Address</td><td>{', '.join(x for x in [address, city, state, zip_] if x) or '—'}</td></tr>
<tr><td style="background:#f5f5f5;font-weight:bold;">Product</td><td>{product or '—'}</td></tr>
<tr><td style="background:#f5f5f5;font-weight:bold;">Notes</td><td>{notes or '—'}</td></tr>
</table>
<p style="color:#999;font-size:12px;margin-top:20px;">Sent by the PSDepot × Chipp × WitzEnd lead portal.</p>
</div>"""

    text = f"New Lead -> {DEST_LABELS.get(dest, dest)}: {biz}\nContact: {contact}\nEmail: {email}\nPhone: {phone}\nAddress: {', '.join(x for x in [address, city, state, zip_] if x)}\nProduct: {product}\nNotes: {notes}"

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"] = to_email
        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        print(f"[lead-notify] sent -> {to_email} ({biz})")
    except Exception as e:
        # Never fail the lead-save because email couldn't send.
        print(f"[lead-notify] FAILED -> {to_email}: {e}")


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
    lead.setdefault("address", lead.get("address", ""))
    lead.setdefault("zip", lead.get("zip", ""))
    lead.setdefault("product", lead.get("product", ""))
    lead.setdefault("notes", lead.get("notes", ""))
    lead.setdefault("dateContacted", lead.get("dateContacted", ""))
    lead.setdefault("otherReason", lead.get("otherReason", ""))

    leads = read_leads()
    leads.insert(0, lead)
    write_leads(leads)

    # Notify destination partner (new lead only — not on bulk sync/update)
    notify_new_lead(lead)

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
