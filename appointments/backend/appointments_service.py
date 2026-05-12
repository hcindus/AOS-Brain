#!/usr/bin/env python3
"""
Appointment Service - FastAPI Backend
Port 8083 - Standalone from DepotChaos
Integrates with Sentinel-Dusty auth system
"""

from fastapi import FastAPI, Depends, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sqlite3
import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, List
import httpx
import uvicorn

app = FastAPI(title="PSD Appointments", version="1.0.0")

# CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database paths
APPOINTMENTS_DB = "/root/.openclaw/workspace/appointments/data/appointments.db"
DEPOT_CHAOS_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# Auth service URL (Sentinel-Dusty)
AUTH_SERVICE_URL = "http://localhost:3000/api/auth"

security = HTTPBearer()

def get_db_connection():
    """Get appointments database connection"""
    conn = sqlite3.connect(APPOINTMENTS_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Core appointments table
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id TEXT PRIMARY KEY,
            lead_id INTEGER,
            customer_name TEXT NOT NULL,
            customer_email TEXT,
            customer_phone TEXT,
            service_type TEXT DEFAULT 'consultation',
            scheduled_at TIMESTAMP NOT NULL,
            duration_minutes INTEGER DEFAULT 60,
            status TEXT DEFAULT 'confirmed',
            notes TEXT,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            google_event_id TEXT,
            reminder_sent BOOLEAN DEFAULT 0
        )
    """)
    
    # Availability slots
    c.execute("""
        CREATE TABLE IF NOT EXISTS availability_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_date DATE NOT NULL,
            slot_time TIME NOT NULL,
            duration_minutes INTEGER DEFAULT 60,
            is_available BOOLEAN DEFAULT 1,
            appointment_id TEXT,
            buffer_before INTEGER DEFAULT 15,
            buffer_after INTEGER DEFAULT 15,
            recurring_pattern TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Google Calendar sync tokens
    c.execute("""
        CREATE TABLE IF NOT EXISTS google_sync_tokens (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            credential_json TEXT,
            refresh_token TEXT,
            calendar_id TEXT,
            last_sync_at TIMESTAMP,
            next_sync_token TEXT
        )
    """)
    
    # Sync queue for async operations
    c.execute("""
        CREATE TABLE IF NOT EXISTS sync_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT NOT NULL,
            appointment_id TEXT,
            google_event_id TEXT,
            status TEXT DEFAULT 'pending',
            retry_count INTEGER DEFAULT 0,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User sessions for mobile app
    c.execute("""
        CREATE TABLE IF NOT EXISTS mobile_sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            device_fingerprint TEXT,
            access_token TEXT,
            refresh_token TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

async def verify_token(credentials: HTTPAuthorizationCredentials) -> dict:
    """Verify JWT token with Sentinel-Dusty auth service"""
    token = credentials.credentials
    
    # In production, call Sentinel-Dusty verify endpoint
    # For now, decode and validate structure
    try:
        import jwt
        # Verify token with auth service secret
        # This is a placeholder - actual implementation calls auth service
        return {"userId": "demo_user", "email": "demo@psdepot.com"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# ===== API ENDPOINTS =====

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "appointments", "version": "1.0.0"}

@app.get("/api/v1/availability")
async def get_availability(
    date: Optional[str] = Query(None),
    days: int = Query(7, ge=1, le=30),
    service_type: Optional[str] = Query(None)
):
    """Get available appointment slots"""
    conn = get_db_connection()
    c = conn.cursor()
    
    if date:
        # Get slots for specific date
        c.execute("""
            SELECT * FROM availability_slots 
            WHERE slot_date = ? AND is_available = 1
            ORDER BY slot_time
        """, (date,))
    else:
        # Get slots for next N days
        c.execute("""
            SELECT * FROM availability_slots 
            WHERE slot_date >= date('now') 
            AND slot_date <= date('now', ?)
            AND is_available = 1
            ORDER BY slot_date, slot_time
        """, (f'+{days} days',))
    
    slots = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {
        "slots": slots,
        "count": len(slots),
        "date": date,
        "days_requested": days
    }

@app.post("/api/v1/bookings")
async def create_booking(
    data: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create new appointment booking"""
    user = await verify_token(credentials)
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Generate appointment ID
    appt_id = str(uuid.uuid4())
    
    # Extract data
    lead_id = data.get('lead_id')
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')
    customer_phone = data.get('customer_phone')
    service_type = data.get('service_type', 'consultation')
    scheduled_at = data.get('scheduled_at')
    duration = data.get('duration_minutes', 60)
    notes = data.get('notes', '')
    
    # Check slot availability
    c.execute("""
        SELECT id FROM availability_slots 
        WHERE slot_date = date(?) AND slot_time = time(?)
        AND is_available = 1
    """, (scheduled_at, scheduled_at))
    
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Slot no longer available")
    
    # Create appointment
    c.execute("""
        INSERT INTO appointments 
        (id, lead_id, customer_name, customer_email, customer_phone,
         service_type, scheduled_at, duration_minutes, notes, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (appt_id, lead_id, customer_name, customer_email, customer_phone,
          service_type, scheduled_at, duration, notes, user.get('userId')))
    
    # Mark slot as taken
    c.execute("""
        UPDATE availability_slots 
        SET is_available = 0, appointment_id = ?
        WHERE slot_date = date(?) AND slot_time = time(?)
    """, (appt_id, scheduled_at, scheduled_at))
    
    # Queue for Google Calendar sync
    c.execute("""
        INSERT INTO sync_queue (operation, appointment_id, status)
        VALUES ('create', ?, 'pending')
    """, (appt_id,))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "appointment_id": appt_id,
        "message": f"Appointment booked for {customer_name}"
    }

@app.get("/api/v1/bookings")
async def get_bookings(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get appointments list"""
    await verify_token(credentials)
    
    conn = get_db_connection()
    c = conn.cursor()
    
    where_clauses = []
    params = []
    
    if status:
        where_clauses.append("status = ?")
        params.append(status)
    
    if start_date:
        where_clauses.append("date(scheduled_at) >= ?")
        params.append(start_date)
    
    if end_date:
        where_clauses.append("date(scheduled_at) <= ?")
        params.append(end_date)
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Get total
    c.execute(f"SELECT COUNT(*) FROM appointments WHERE {where_sql}", params)
    total = c.fetchone()[0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    c.execute(f"""
        SELECT * FROM appointments 
        WHERE {where_sql}
        ORDER BY scheduled_at DESC
        LIMIT ? OFFSET ?
    """, params + [per_page, offset])
    
    appointments = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {
        "appointments": appointments,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

@app.get("/api/v1/bookings/{appointment_id}")
async def get_booking_detail(
    appointment_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get single appointment details"""
    await verify_token(credentials)
    
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment = dict(row)
    
    # If linked to lead, get lead info from DepotChaos (read-only)
    if appointment.get('lead_id'):
        try:
            dc_conn = sqlite3.connect(DEPOT_CHAOS_DB)
            dc_conn.row_factory = sqlite3.Row
            dc_c = dc_conn.cursor()
            dc_c.execute("""
                SELECT company_name, contact_name, phone, email, county, state
                FROM leads WHERE id = ? AND deleted = 0
            """, (appointment['lead_id'],))
            lead = dc_c.fetchone()
            if lead:
                appointment['lead_info'] = dict(lead)
            dc_conn.close()
        except:
            pass
    
    conn.close()
    return appointment

@app.put("/api/v1/bookings/{appointment_id}")
async def update_booking(
    appointment_id: str,
    data: dict,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update appointment"""
    await verify_token(credentials)
    
    conn = get_db_connection()
    c = conn.cursor()
    
    allowed_fields = ['status', 'notes', 'customer_name', 'customer_email', 
                      'customer_phone', 'scheduled_at', 'duration_minutes']
    
    updates = []
    params = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = ?")
            params.append(data[field])
    
    if not updates:
        conn.close()
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(appointment_id)
    
    sql = f"UPDATE appointments SET {', '.join(updates)} WHERE id = ?"
    c.execute(sql, params)
    
    # Queue for Google Calendar update
    c.execute("""
        INSERT INTO sync_queue (operation, appointment_id, status)
        VALUES ('update', ?, 'pending')
    """, (appointment_id,))
    
    conn.commit()
    updated = c.rowcount
    conn.close()
    
    return {"success": True, "updated": updated}

@app.delete("/api/v1/bookings/{appointment_id}")
async def cancel_booking(
    appointment_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Cancel/delete appointment"""
    await verify_token(credentials)
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Soft delete - mark as cancelled
    c.execute(
        "UPDATE appointments SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (appointment_id,)
    )
    
    # Free up slot
    c.execute(
        "UPDATE availability_slots SET is_available = 1, appointment_id = NULL WHERE appointment_id = ?",
        (appointment_id,)
    )
    
    # Queue for Google Calendar delete
    c.execute("""
        INSERT INTO sync_queue (operation, appointment_id, status)
        VALUES ('delete', ?, 'pending')
    """, (appointment_id,))
    
    conn.commit()
    deleted = c.rowcount
    conn.close()
    
    return {"success": True, "deleted": deleted}

@app.get("/api/v1/leads/search")
async def search_leads(
    q: str = Query(..., min_length=2),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Search leads from DepotChaos (read-only)"""
    await verify_token(credentials)
    
    try:
        conn = sqlite3.connect(DEPOT_CHAOS_DB)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute("""
            SELECT id, company_name, contact_name, phone, email, county, state, status, tier
            FROM leads 
            WHERE deleted = 0 
            AND (company_name LIKE ? OR contact_name LIKE ? OR email LIKE ?)
            ORDER BY company_name
            LIMIT 20
        """, (f'%{q}%', f'%{q}%', f'%{q}%'))
        
        leads = [dict(row) for row in c.fetchall()]
        conn.close()
        
        return {"leads": leads, "count": len(leads)}
    except Exception as e:
        return {"leads": [], "count": 0, "error": str(e)}

if __name__ == "__main__":
    init_database()
    uvicorn.run(app, host="0.0.0.0", port=8083, log_level="info")
