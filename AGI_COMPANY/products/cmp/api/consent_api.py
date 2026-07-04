#!/usr/bin/env python3
"""
AGI CMP Backend API
Handles consent recording, audit trails, and compliance reporting
"""

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import hashlib
import uuid
import json
from enum import Enum

app = FastAPI(
    title="AGI CMP API",
    description="Consent Management Platform API for GDPR/CCPA compliance",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (use database in production)
consent_records: Dict[str, dict] = {}
audit_log: List[dict] = []

class ConsentCategory(str, Enum):
    ESSENTIAL = "essential"
    FUNCTIONAL = "functional"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    SOCIAL = "social"

class ConsentPayload(BaseModel):
    essential: bool = True
    functional: bool = False
    analytics: bool = False
    marketing: bool = False
    social: bool = False

class ConsentRecord(BaseModel):
    consent: ConsentPayload
    timestamp: int
    url: str
    user_agent: Optional[str] = None
    ip_hash: Optional[str] = None  # Hashed for privacy

class ConsentResponse(BaseModel):
    record_id: str
    status: str
    recorded_at: datetime

class AuditEntry(BaseModel):
    record_id: str
    action: str
    timestamp: datetime
    ip_hash: str
    user_agent: str
    consent_version: str
    consent_snapshot: dict

# Helper functions
def hash_ip(ip: str) -> str:
    """One-way hash IP for audit without storing PII"""
    return hashlib.sha256(f"agi_salt_{ip}".encode()).hexdigest()[:16]

def generate_record_id() -> str:
    return str(uuid.uuid4())

def log_audit(entry: dict):
    audit_log.append(entry)

# Routes
@app.post("/api/consent", response_model=ConsentResponse)
async def record_consent(
    data: ConsentRecord,
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Record a new consent decision from the user
    """
    record_id = generate_record_id()
    
    # Get client IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else "unknown"
    
    ip_hash = hash_ip(client_ip)
    
    consent_data = {
        "record_id": record_id,
        "consent": data.consent.dict(),
        "timestamp": datetime.utcnow(),
        "url": data.url,
        "ip_hash": ip_hash,
        "user_agent": data.user_agent,
        "version": "1.0.0"
    }
    
    # Store consent
    consent_records[record_id] = consent_data
    
    # Create audit entry
    audit_entry = {
        "record_id": record_id,
        "action": "consent_given",
        "timestamp": datetime.utcnow(),
        "ip_hash": ip_hash,
        "user_agent": data.user_agent,
        "consent_version": "1.0.0",
        "consent_snapshot": data.consent.dict()
    }
    
    # Log audit in background
    background_tasks.add_task(log_audit, audit_entry)
    
    return ConsentResponse(
        record_id=record_id,
        status="recorded",
        recorded_at=datetime.utcnow()
    )

@app.get("/api/consent/{record_id}")
async def get_consent(record_id: str):
    """
    Retrieve a specific consent record
    """
    if record_id not in consent_records:
        raise HTTPException(status_code=404, detail="Consent record not found")
    
    return consent_records[record_id]

@app.post("/api/consent/{record_id}/withdraw")
async def withdraw_consent(record_id: str, request: Request):
    """
    Allow user to withdraw consent (GDPR right to withdraw)
    """
    if record_id not in consent_records:
        raise HTTPException(status_code=404, detail="Consent record not found")
    
    record = consent_records[record_id]
    
    # Mark as withdrawn
    record["withdrawn"] = True
    record["withdrawn_at"] = datetime.utcnow()
    
    # Audit log
    audit_entry = {
        "record_id": record_id,
        "action": "consent_withdrawn",
        "timestamp": datetime.utcnow(),
        "ip_hash": hash_ip(request.client.host if request.client else "unknown"),
        "user_agent": request.headers.get("User-Agent"),
        "consent_version": record.get("version", "1.0.0")
    }
    audit_log.append(audit_entry)
    
    return {"status": "withdrawn", "record_id": record_id}

@app.get("/api/consent/stats/summary")
async def get_consent_stats():
    """
    Get aggregate consent statistics (anonymized)
    """
    total = len(consent_records)
    if total == 0:
        return {"total": 0, "breakdown": {}}
    
    breakdown = {
        "analytics": sum(1 for r in consent_records.values() if r["consent"].get("analytics", False)),
        "marketing": sum(1 for r in consent_records.values() if r["consent"].get("marketing", False)),
        "functional": sum(1 for r in consent_records.values() if r["consent"].get("functional", False)),
        "social": sum(1 for r in consent_records.values() if r["consent"].get("social", False)),
    }
    
    return {
        "total": total,
        "breakdown": {k: {"count": v, "percentage": round(v/total*100, 2)} 
                      for k, v in breakdown.items()}
    }

@app.get("/api/consent/export/{record_id}")
async def export_user_data(record_id: str):
    """
    GDPR Data Portability - Export all data for a user
    """
    if record_id not in consent_records:
        raise HTTPException(status_code=404, detail="Record not found")
    
    # Get all audit entries for this record
    user_audits = [a for a in audit_log if a.get("record_id") == record_id]
    
    return {
        "record": consent_records[record_id],
        "audit_history": user_audits,
        "exported_at": datetime.utcnow()
    }

@app.get("/api/consent/audit/log")
async def get_audit_log(
    limit: int = 100,
    action: Optional[str] = None
):
    """
    Get audit log for compliance review
    """
    logs = audit_log
    
    if action:
        logs = [l for l in logs if l.get("action") == action]
    
    return {
        "total": len(logs),
        "entries": logs[-limit:]
    }

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "agi-cmp",
        "version": "1.0.0",
        "consent_records": len(consent_records),
        "audit_entries": len(audit_log)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)
