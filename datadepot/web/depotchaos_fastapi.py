#!/usr/bin/env python3
"""
DepotChaos Web Interface - FastAPI Backend
Serves database content to web frontend
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
import uvicorn

app = FastAPI(title="DepotChaos CRM", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database paths
DEPOT_CHAOS_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
DATADEPOT_DIR = Path("/root/.openclaw/workspace/datadepot")
STATIC_DIR = "/var/www/psdepot.com/depotchaos"

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DEPOT_CHAOS_DB)
    conn.row_factory = sqlite3.Row  # Return dict-like rows
    return conn

def row_to_dict(row):
    """Convert sqlite row to dict"""
    return {key: row[key] for key in row.keys()}

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def index():
    """Serve the main web interface"""
    return FileResponse(f"{STATIC_DIR}/index.html")

# ===== API ENDPOINTS =====

@app.get("/api/stats")
async def get_stats():
    """Get overall database statistics"""
    conn = get_db_connection()
    c = conn.cursor()
    
    stats = {}
    
    # Total leads
    c.execute("SELECT COUNT(*) FROM leads")
    stats['total_leads'] = c.fetchone()[0]
    
    # DataDepot-specific leads (those with POS data)
    c.execute("SELECT COUNT(*) FROM leads WHERE pos_system IS NOT NULL")
    stats['datadepot_leads'] = c.fetchone()[0]
    
    # By status
    c.execute("SELECT status, COUNT(*) FROM leads GROUP BY status")
    stats['by_status'] = dict(c.fetchall())
    
    # By tier
    c.execute("SELECT tier, COUNT(*) FROM leads WHERE tier IS NOT NULL GROUP BY tier")
    stats['by_tier'] = dict(c.fetchall())
    
    # Intelligence records
    c.execute("SELECT COUNT(*) FROM datadepot_intelligence")
    stats['intelligence_records'] = c.fetchone()[0]
    
    # Today's activity
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute("SELECT COUNT(*) FROM leads WHERE DATE(created_at) = ?", (today,))
    stats['new_today'] = c.fetchone()[0]
    
    conn.close()
    
    return stats

@app.get("/api/leads")
async def get_leads(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    tier: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    datadepot: bool = Query(False)
):
    """Get leads with filtering and pagination"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Build query
    where_clauses = []
    params = []
    
    if status:
        where_clauses.append("status = ?")
        params.append(status)
    
    if tier:
        where_clauses.append("tier = ?")
        params.append(tier)
    
    if source:
        where_clauses.append("source_type = ?")
        params.append(source)
    
    if search:
        where_clauses.append("(company_name LIKE ? OR county LIKE ?)")
        params.extend([f'%{search}%', f'%{search}%'])
    
    if datadepot:
        where_clauses.append("pos_system IS NOT NULL")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Get total count
    count_sql = f"SELECT COUNT(*) FROM leads WHERE {where_sql}"
    c.execute(count_sql, params)
    total = c.fetchone()[0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    query_sql = f"""
        SELECT * FROM leads 
        WHERE {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """
    c.execute(query_sql, params + [per_page, offset])
    
    leads = [dict(row) for row in c.fetchall()]
    
    conn.close()
    
    return {
        'leads': leads,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

@app.get("/api/leads/{lead_id}")
async def get_lead(lead_id: str):
    """Get single lead details"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = c.fetchone()
    
    conn.close()
    
    if row:
        return dict(row)
    else:
        return JSONResponse(status_code=404, content={'error': 'Lead not found'})

@app.put("/api/leads/{lead_id}")
async def update_lead(lead_id: str, data: dict):
    """Update lead information"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Build update query
    allowed_fields = ['status', 'assigned_agent', 'notes', 'tier', 'pos_system', 
                      'email_sent', 'email_opened', 'email_clicked', 'demo_scheduled']
    
    updates = []
    params = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = ?")
            params.append(data[field])
    
    if not updates:
        return JSONResponse(status_code=400, content={'error': 'No valid fields to update'})
    
    params.append(lead_id)
    
    sql = f"UPDATE leads SET {', '.join(updates)} WHERE id = ?"
    c.execute(sql, params)
    
    conn.commit()
    conn.close()
    
    return {'success': True, 'updated': c.rowcount}

@app.get("/api/intelligence")
async def get_intelligence(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    county: Optional[str] = Query(None)
):
    """Get CA ABC intelligence data"""
    conn = get_db_connection()
    c = conn.cursor()
    
    where_sql = "1=1"
    params = []
    
    if county:
        where_sql += " AND county = ?"
        params.append(county)
    
    # Get total
    c.execute(f"SELECT COUNT(*) FROM datadepot_intelligence WHERE {where_sql}", params)
    total = c.fetchone()[0]
    
    # Get data
    offset = (page - 1) * per_page
    c.execute(f"""
        SELECT * FROM datadepot_intelligence
        WHERE {where_sql}
        ORDER BY replacement_score DESC, county
        LIMIT ? OFFSET ?
    """, params + [per_page, offset])
    
    records = [dict(row) for row in c.fetchall()]
    
    conn.close()
    
    return {
        'records': records,
        'total': total,
        'page': page,
        'per_page': per_page
    }

@app.get("/api/counties")
async def get_counties():
    """Get list of all counties with counts"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # From leads
    c.execute("SELECT county, COUNT(*) FROM leads WHERE county IS NOT NULL GROUP BY county ORDER BY COUNT(*) DESC")
    lead_counties = dict(c.fetchall())
    
    # From intelligence
    c.execute("SELECT county, COUNT(*) FROM datadepot_intelligence WHERE county IS NOT NULL GROUP BY county ORDER BY COUNT(*) DESC")
    intel_counties = dict(c.fetchall())
    
    conn.close()
    
    return {
        'lead_counties': lead_counties,
        'intelligence_counties': intel_counties
    }

@app.get("/api/pos-systems")
async def get_pos_systems():
    """Get breakdown by POS system"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("""
        SELECT pos_system, COUNT(*), AVG(replacement_score) 
        FROM leads 
        WHERE pos_system IS NOT NULL 
        GROUP BY pos_system
    """)
    
    systems = [{'name': row[0], 'count': row[1], 'avg_score': row[2]} for row in c.fetchall()]
    
    conn.close()
    
    return systems

@app.get("/api/queue")
async def get_email_queue():
    """Get pending email queue"""
    queue_file = DATADEPOT_DIR / 'queue' / 'pending_emails.json'
    
    if not queue_file.exists():
        return {'queue': [], 'total': 0, 'ready_to_send': 0}
    
    with open(queue_file, 'r') as f:
        queue = json.load(f)
    
    now = datetime.now()
    ready = [e for e in queue if datetime.fromisoformat(e['scheduled_time'].replace('Z', '+00:00').replace('+00:00', '')) <= now]
    
    return {
        'queue': queue,
        'total': len(queue),
        'ready_to_send': len(ready)
    }

@app.get("/api/activities")
async def get_activities():
    """Get recent activities from logs"""
    activities = []
    
    # Check recent email sends
    sent_file = DATADEPOT_DIR / 'queue' / 'sent_emails.json'
    if sent_file.exists():
        with open(sent_file, 'r') as f:
            sent = json.load(f)
            activities.extend([{
                'type': 'email_sent',
                'description': f"Email sent to {e['to_email']}",
                'timestamp': e.get('sent_at', ''),
                'campaign': e.get('campaign_id', '')
            } for e in sent[-10:]])
    
    # Sort by timestamp
    activities.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return activities[:20]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")
