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

app = FastAPI(title="DepotChaos CRM", version="1.1.0")

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
    """Convert sqlite row to dict with enrichment parsing"""
    result = {key: row[key] for key in row.keys()}
    
    # Parse enrichment_data JSON if present
    if result.get('enrichment_data'):
        try:
            enrichment = json.loads(result['enrichment_data'])
            result['enrichment'] = enrichment
            # Flatten for easier frontend access
            result['contact_name'] = enrichment.get('contact_name', '')
            result['contact_title'] = enrichment.get('contact_title', '')
            result['phone'] = enrichment.get('phone', '')
            result['email'] = enrichment.get('email', '')
            result['city'] = enrichment.get('city', '')
        except:
            result['enrichment'] = {}
    
    return result

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
    state: Optional[str] = Query(None),
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
    
    if state:
        where_clauses.append("(county LIKE ? OR county LIKE ?)")
        params.extend([f'%, {state}%', f'%| {state}%'])
    
    if search:
        where_clauses.append("(company_name LIKE ? OR county LIKE ? OR pos_system LIKE ? OR enrichment_data LIKE ?)")
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'])
    
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
    """Get single lead details with enrichment"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = c.fetchone()
    
    conn.close()
    
    if row:
        return row_to_dict(row)
    else:
        return JSONResponse(status_code=404, content={'error': 'Lead not found'})

@app.put("/api/leads/{lead_id}")
async def update_lead(lead_id: str, data: dict):
    """Update lead information and enrichment data"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Build update query
    allowed_fields = ['status', 'assigned_agent', 'tier', 'pos_system', 
                      'email_sent', 'email_opened', 'email_clicked', 'demo_scheduled']
    
    updates = []
    params = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = ?")
            params.append(data[field])
    
    # Handle enrichment_data separately
    if 'enrichment_data' in data:
        # Get existing enrichment
        c.execute("SELECT enrichment_data FROM leads WHERE id = ?", (lead_id,))
        row = c.fetchone()
        existing = {}
        if row and row[0]:
            try:
                existing = json.loads(row[0])
            except:
                pass
        
        # Merge new enrichment
        try:
            new_enrichment = json.loads(data['enrichment_data'])
            existing.update(new_enrichment)
            updates.append("enrichment_data = ?")
            params.append(json.dumps(existing))
        except:
            pass
    
    if updates:
        params.append(lead_id)
        sql = f"UPDATE leads SET {', '.join(updates)} WHERE id = ?"
        c.execute(sql, params)
        
    conn.commit()
    updated = c.rowcount
    conn.close()
    
    return {'success': True, 'updated': updated}

@app.get("/api/intelligence/{record_id}")
async def get_intelligence_detail(record_id: int):
    """Get single intelligence record details"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM datadepot_intelligence WHERE id = ?", (record_id,))
    row = c.fetchone()
    
    conn.close()
    
    if row:
        return row_to_dict(row)
    else:
        return JSONResponse(status_code=404, content={'error': 'Record not found'})

@app.put("/api/intelligence/{record_id}")
async def update_intelligence(record_id: int, data: dict):
    """Update intelligence record"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Build update query
    allowed_fields = ['pos_system', 'pos_confidence', 'replacement_score', 'status']
    
    updates = []
    params = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = ?")
            params.append(data[field])
    
    if not updates:
        return JSONResponse(status_code=400, content={'error': 'No valid fields to update'})
    
    params.append(record_id)
    
    sql = f"UPDATE datadepot_intelligence SET {', '.join(updates)} WHERE id = ?"
    c.execute(sql, params)
    
    conn.commit()
    conn.close()
    
    return {'success': True, 'updated': c.rowcount}

@app.get("/api/intelligence")
async def get_intelligence(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    county: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    pos_system: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Get CA ABC intelligence data with filtering"""
    conn = get_db_connection()
    c = conn.cursor()
    
    where_clauses = ["1=1"]
    params = []
    
    if county:
        where_clauses.append("county = ?")
        params.append(county)
    
    if city:
        where_clauses.append("city LIKE ?")
        params.append(f'%{city}%')
    
    if pos_system:
        if pos_system == 'Unknown':
            where_clauses.append("(pos_system IS NULL OR pos_system = '' OR pos_system = 'Unknown')")
        else:
            where_clauses.append("pos_system = ?")
            params.append(pos_system)
    
    if search:
        where_clauses.append("(business_name LIKE ? OR dba LIKE ? OR city LIKE ? OR address LIKE ?)")
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'])
    
    where_sql = " AND ".join(where_clauses)
    
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

@app.post("/api/queue/{email_id}/send")
async def send_email_now(email_id: str):
    """Send a queued email immediately via Mailgun"""
    import os
    import requests
    
    # Load queue
    queue_file = DATADEPOT_DIR / 'queue' / 'pending_emails.json'
    sent_file = DATADEPOT_DIR / 'queue' / 'sent_emails.json'
    failed_file = DATADEPOT_DIR / 'queue' / 'failed_emails.json'
    
    if not queue_file.exists():
        return JSONResponse(status_code=404, content={'error': 'Queue file not found'})
    
    with open(queue_file, 'r') as f:
        queue = json.load(f)
    
    # Find email by ID
    email_to_send = None
    remaining_queue = []
    
    for email in queue:
        if email.get('id') == email_id:
            email_to_send = email
        else:
            remaining_queue.append(email)
    
    if not email_to_send:
        return JSONResponse(status_code=404, content={'error': 'Email not found in queue'})
    
    # Check if test mode
    TEST_MODE = os.getenv('MAILGUN_TEST_MODE', 'True').lower() == 'true'
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', '')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN', 'psdepot.com')
    
    if TEST_MODE or not MAILGUN_API_KEY:
        # Test mode - simulate send
        email_to_send['sent_at'] = datetime.now().isoformat()
        email_to_send['test_mode'] = True
        email_to_send['mailgun_id'] = f'test_{int(datetime.now().timestamp())}'
        
        # Add to sent log
        sent_list = []
        if sent_file.exists():
            with open(sent_file, 'r') as f:
                sent_list = json.load(f)
        
        sent_list.append(email_to_send)
        
        with open(sent_file, 'w') as f:
            json.dump(sent_list, f, indent=2)
        
        # Update queue
        with open(queue_file, 'w') as f:
            json.dump(remaining_queue, f, indent=2)
        
        return {
            'success': True,
            'test_mode': True,
            'message': f'Email to {email_to_send["to_email"]} simulated (TEST MODE)',
            'email_id': email_id
        }
    
    # Real Mailgun send
    try:
        api_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
        
        data = {
            'from': email_to_send.get('from', 'Miles - Performance Supply Depot <miles@psdepot.com>'),
            'to': f"{email_to_send['to_name']} <{email_to_send['to_email']}>",
            'bcc': 'info@psdepot.com',
            'subject': email_to_send.get('subject', 'Performance Supply Depot'),
            'html': email_to_send.get('html_body', ''),
            'o:tracking': 'yes',
            'o:tracking-clicks': 'yes',
            'v:campaign_id': email_to_send.get('campaign_id', 'default'),
            'v:template': email_to_send.get('template', 'unknown'),
        }
        
        response = requests.post(
            api_url,
            auth=('api', MAILGUN_API_KEY),
            data=data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Record as sent
        email_to_send['sent_at'] = datetime.now().isoformat()
        email_to_send['mailgun_id'] = result.get('id', 'unknown')
        
        sent_list = []
        if sent_file.exists():
            with open(sent_file, 'r') as f:
                sent_list = json.load(f)
        
        sent_list.append(email_to_send)
        
        with open(sent_file, 'w') as f:
            json.dump(sent_list, f, indent=2)
        
        # Update queue
        with open(queue_file, 'w') as f:
            json.dump(remaining_queue, f, indent=2)
        
        return {
            'success': True,
            'message': f'Email sent to {email_to_send["to_email"]}',
            'mailgun_id': result.get('id'),
            'email_id': email_id
        }
        
    except Exception as e:
        # Record as failed
        email_to_send['failed_at'] = datetime.now().isoformat()
        email_to_send['error'] = str(e)
        
        failed_list = []
        if failed_file.exists():
            with open(failed_file, 'r') as f:
                failed_list = json.load(f)
        
        failed_list.append(email_to_send)
        
        with open(failed_file, 'w') as f:
            json.dump(failed_list, f, indent=2)
        
        # Remove from queue even on failure
        with open(queue_file, 'w') as f:
            json.dump(remaining_queue, f, indent=2)
        
        return JSONResponse(status_code=500, content={
            'success': False,
            'error': str(e),
            'email_id': email_id
        })

@app.post("/api/queue/{email_id}/cancel")
async def cancel_queued_email(email_id: str):
    """Cancel a queued email"""
    queue_file = DATADEPOT_DIR / 'queue' / 'pending_emails.json'
    
    if not queue_file.exists():
        return JSONResponse(status_code=404, content={'error': 'Queue file not found'})
    
    with open(queue_file, 'r') as f:
        queue = json.load(f)
    
    # Find and remove email
    remaining = [e for e in queue if e.get('id') != email_id]
    
    if len(remaining) == len(queue):
        return JSONResponse(status_code=404, content={'error': 'Email not found'})
    
    # Update queue
    with open(queue_file, 'w') as f:
        json.dump(remaining, f, indent=2)
    
    return {
        'success': True,
        'message': f'Email {email_id} cancelled',
        'remaining_count': len(remaining)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082, log_level="info")
