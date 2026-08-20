#!/usr/bin/env python3
"""
Testimonials API — Performance Supply Depot
Stores customer testimonials + star ratings as JSON, serves on port 8087.

Rules:
- Rating >= 3  → status "published" (shows on the public testimonials page).
- Rating  <  3 → status "flagged"  → NOT shown publicly; email management for intervention.
- Every submission requires name + rating + text.
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

TESTIMONIALS_FILE = Path("/var/lib/psdepot/testimonials.json")
LOCK_FILE = Path("/var/lib/psdepot/testimonials.lock")

# Management email — flagged (sub-3-star) reviews go here for intervention.
MANAGEMENT_EMAIL = "Antonio.hudnall@gmail.com"

SMTP_SERVER = os.getenv("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com")
SMTP_PORT = int(os.getenv("HOSTINGER_SMTP_PORT", "587"))
SMTP_USER = os.getenv("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud")
SMTP_PASS = os.getenv("HOSTINGER_SMTP_PASS", "")
FROM_EMAIL = os.getenv("SMTP_FROM", "miles@myl0nr0s.cloud")
FROM_NAME = "Performance Supply Depot — Testimonials"


def notify_flag(testimonial: dict):
    """Email management when a customer leaves a rating below 3 stars."""
    rating = testimonial.get("rating")
    name = testimonial.get("name", "Unknown")
    business = testimonial.get("business", "")
    text = testimonial.get("text", "")
    email = testimonial.get("email", "")
    phone = testimonial.get("phone", "")

    subject = f"⚠️ {rating}-Star Review Flagged — Management Intervention Needed"

    body_text = (
        f"FLAGGED TESTIMONIAL ({rating}/5 stars)\n"
        f"Name: {name}\nBusiness: {business or '—'}\n"
        f"Email: {email or '—'}\nPhone: {phone or '—'}\n"
        f"Review: {text}\n\n"
        f"This review is BELOW 3 stars and has been hidden from the public site. "
        f"Please review and follow up to make things right."
    )

    body_html = f"""<div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;color:#1a1a1a;">
<h2 style="margin:0 0 4px;color:#b91c1c;">⚠️ {rating}-Star Review Flagged</h2>
<p style="color:#666;margin:0 0 20px;">This review is below 3 stars and has been hidden from the public site. Management intervention requested.</p>
<table cellpadding="8" style="border-collapse:collapse;width:100%;">
<tr><td style="background:#fef2f2;font-weight:bold;width:130px;">Rating</td><td>{'★' * int(rating)}{'☆' * (5 - int(rating))}</td></tr>
<tr><td style="background:#fef2f2;font-weight:bold;">Name</td><td>{name}</td></tr>
<tr><td style="background:#fef2f2;font-weight:bold;">Business</td><td>{business or '—'}</td></tr>
<tr><td style="background:#fef2f2;font-weight:bold;">Email</td><td>{email or '—'}</td></tr>
<tr><td style="background:#fef2f2;font-weight:bold;">Phone</td><td>{phone or '—'}</td></tr>
<tr><td style="background:#fef2f2;font-weight:bold;">Review</td><td>{text}</td></tr>
</table>
<p style="color:#999;font-size:12px;margin-top:20px;">Sent automatically by the PSDepot testimonials system.</p>
</div>"""

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"] = MANAGEMENT_EMAIL
        msg.attach(MIMEText(body_text, "plain"))
        msg.attach(MIMEText(body_html, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, MANAGEMENT_EMAIL, msg.as_string())
        print(f"[testimonial-flag] sent -> {MANAGEMENT_EMAIL} ({rating} stars)")
    except Exception as e:
        print(f"[testimonial-flag] FAILED -> {MANAGEMENT_EMAIL}: {e}")


app = FastAPI(title="PSDepot Testimonials API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _acquire_lock(timeout=5):
    start = time.time()
    while LOCK_FILE.exists():
        if time.time() - start > timeout:
            LOCK_FILE.unlink(missing_ok=True)
            break
        time.sleep(0.05)
    LOCK_FILE.touch()


def _release_lock():
    LOCK_FILE.unlink(missing_ok=True)


def read_testimonials():
    if not TESTIMONIALS_FILE.exists():
        return []
    try:
        with open(TESTIMONIALS_FILE, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def write_testimonials(items):
    _acquire_lock()
    try:
        tmp = TESTIMONIALS_FILE.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(items, f, indent=2, default=str)
        tmp.replace(TESTIMONIALS_FILE)
    finally:
        _release_lock()


@app.get("/api/testimonials")
async def get_testimonials():
    """Return only published (rating >= 3) testimonials for public display."""
    items = read_testimonials()
    published = [t for t in items if t.get("status") == "published"]
    return JSONResponse(published)


@app.get("/api/testimonials/all")
async def get_all_testimonials():
    """Return ALL testimonials incl. flagged (management/dashboard use)."""
    return JSONResponse(read_testimonials())


@app.post("/api/testimonials")
async def add_testimonial(request: Request):
    try:
        t = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    # Required fields
    name = (t.get("name") or "").strip()
    text = (t.get("text") or "").strip()
    try:
        rating = int(t.get("rating", 0))
    except (TypeError, ValueError):
        rating = 0

    if not name:
        return JSONResponse({"error": "Missing required field: name"}, status_code=422)
    if not text:
        return JSONResponse({"error": "Missing required field: text"}, status_code=422)
    if rating < 1 or rating > 5:
        return JSONResponse({"error": "Rating must be 1–5"}, status_code=422)

    now = datetime.utcnow().isoformat() + "Z"

    # Rating < 3 → flag for management intervention (hidden from public).
    if rating < 3:
        status = "flagged"
    else:
        status = "published"

    testimonial = {
        "id": "t_" + str(int(time.time() * 1000)),
        "name": name,
        "business": (t.get("business") or "").strip(),
        "email": (t.get("email") or "").strip(),
        "phone": (t.get("phone") or "").strip(),
        "rating": rating,
        "text": text,
        "status": status,
        "createdAt": now,
    }

    items = read_testimonials()
    items.insert(0, testimonial)
    write_testimonials(items)

    if status == "flagged":
        notify_flag(testimonial)

    return JSONResponse({"ok": True, "id": testimonial["id"], "status": status})


@app.get("/health")
async def health():
    items = read_testimonials()
    return {
        "status": "ok",
        "total": len(items),
        "published": sum(1 for t in items if t.get("status") == "published"),
        "flagged": sum(1 for t in items if t.get("status") == "flagged"),
    }


if __name__ == "__main__":
    print(f"Testimonials file: {TESTIMONIALS_FILE}")
    uvicorn.run(app, host="127.0.0.1", port=8087, log_level="info")
