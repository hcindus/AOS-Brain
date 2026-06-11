from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from datetime import datetime
import uvicorn
import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import ClientCreate, ClientUpdate, ClientList, Client, Activity, EmailScheduleRequest
from crud import (
    init_db, create_client, get_client, get_clients, update_client, delete_client,
    get_clients_needing_contact, add_activity, get_client_activities,
    schedule_email, get_pending_emails, mark_email_sent, get_email_queue_stats
)

app = FastAPI(
    title="Client Outreach",
    description="Mobile-first client outreach and email scheduling app",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="/root/.openclaw/workspace/client-outreach/static"), name="static")
templates = Jinja2Templates(directory="/root/.openclaw/workspace/client-outreach/templates")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    db_path = '/root/.openclaw/workspace/client-outreach/database/outreach.db'
    if not os.path.exists(db_path):
        init_db()
        print("Database initialized with demo data")

# Web Interface Routes

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard - mobile-optimized"""
    stats = {
        'total_clients': get_clients(per_page=1)['total'],
        'email_stats': get_email_queue_stats(),
        'follow_up_needed': len(get_clients_needing_contact())
    }
    return templates.TemplateResponse("index.html", {"request": request, "stats": stats})

@app.get("/clients", response_class=HTMLResponse)
async def clients_page(request: Request):
    """Client list page"""
    return templates.TemplateResponse("clients.html", {"request": request})

@app.get("/clients/{client_id}", response_class=HTMLResponse)
async def client_detail_page(request: Request, client_id: int):
    """Single client detail page"""
    client = get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return templates.TemplateResponse("client_detail.html", {"request": request, "client": client})

@app.get("/scheduler", response_class=HTMLResponse)
async def scheduler_page(request: Request):
    """Email scheduler page"""
    return templates.TemplateResponse("scheduler.html", {"request": request})

# API Routes - Clients

@app.get("/api/clients", response_model=ClientList)
async def api_get_clients(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    tier: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Get clients with filtering and pagination"""
    return get_clients(status=status, tier=tier, search=search, page=page, per_page=per_page)

@app.post("/api/clients", response_model=dict)
async def api_create_client(client: ClientCreate):
    """Create a new client"""
    return create_client(client)

@app.get("/api/clients/{client_id}", response_model=dict)
async def api_get_client(client_id: int):
    """Get single client"""
    client = get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/api/clients/{client_id}", response_model=dict)
async def api_update_client(client_id: int, updates: ClientUpdate):
    """Update client"""
    client = update_client(client_id, updates)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.delete("/api/clients/{client_id}")
async def api_delete_client(client_id: int):
    """Delete client"""
    deleted = delete_client(client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"status": "deleted", "id": client_id}

@app.get("/api/clients/need-contact/today", response_model=List[dict])
async def api_get_clients_needing_contact():
    """Get clients needing contact today"""
    return get_clients_needing_contact()

# API Routes - Activities

@app.post("/api/clients/{client_id}/activities")
async def api_add_activity(client_id: int, activity_type: str, description: str = ""):
    """Add activity to client"""
    activity = add_activity(client_id, activity_type, description)
    if not activity:
        raise HTTPException(status_code=404, detail="Client not found")
    return activity

@app.get("/api/clients/{client_id}/activities")
async def api_get_activities(client_id: int, limit: int = Query(20, le=100)):
    """Get client activities"""
    return get_client_activities(client_id, limit)

# API Routes - Email Queue

@app.post("/api/email-queue")
async def api_schedule_email(request: EmailScheduleRequest):
    """Schedule an email"""
    email = schedule_email(
        client_id=request.client_id,
        template=request.template,
        subject=request.subject,
        scheduled_at=request.scheduled_at,
        body=request.body
    )
    return email

@app.get("/api/email-queue/pending")
async def api_get_pending_emails(limit: int = Query(100, le=500)):
    """Get pending emails ready to send"""
    return get_pending_emails(limit)

@app.get("/api/email-queue/stats")
async def api_email_stats():
    """Get email queue statistics"""
    return get_email_queue_stats()

@app.post("/api/email-queue/{email_id}/mark-sent")
async def api_mark_sent(email_id: int, error: Optional[str] = None):
    """Mark email as sent or failed"""
    mark_email_sent(email_id, error)
    return {"status": "marked"}

# Health check

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)
