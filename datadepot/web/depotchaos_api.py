#!/usr/bin/env python3
"""
DepotChaos Web Interface - Flask Backend API
Serves database content to web frontend
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database paths
DEPOT_CHAOS_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
DATADEPOT_DIR = Path("/root/.openclaw/workspace/datadepot")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DEPOT_CHAOS_DB)
    conn.row_factory = sqlite3.Row  # Return dict-like rows
    return conn

@app.route('/')
def index():
    """Serve the main web interface"""
    return send_from_directory('/var/www/psdepot.com/depotchaos', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files"""
    return send_from_directory('/var/www/psdepot.com/depotchaos', path)

# ===== API ENDPOINTS =====

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall database statistics"""
    conn = get_db_connection()
    c = conn.cursor()
    
    stats = {}
    
    # Total leads
    c.execute("SELECT COUNT(*) FROM leads")
    stats['total_leads'] = c.fetchone()[0]
    
    # DataDepot-specific leads
    c.execute("SELECT COUNT(*) FROM leads WHERE tags LIKE '%datadepot%'")
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
    
    return jsonify(stats)

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Get leads with filtering and pagination"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get query parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    status = request.args.get('status', '')
    tier = request.args.get('tier', '')
    source = request.args.get('source', '')
    search = request.args.get('search', '')
    datadepot_only = request.args.get('datadepot', 'false').lower() == 'true'
    
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
    
    if datadepot_only:
        where_clauses.append("tags LIKE '%datadepot%'")
    
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
    
    return jsonify({
        'leads': leads,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    })

@app.route('/api/leads/<lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get single lead details"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = c.fetchone()
    
    conn.close()
    
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({'error': 'Lead not found'}), 404

@app.route('/api/leads/<lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Update lead information"""
    data = request.json
    
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
        return jsonify({'error': 'No valid fields to update'}), 400
    
    params.append(lead_id)
    
    sql = f"UPDATE leads SET {', '.join(updates)} WHERE id = ?"
    c.execute(sql, params)
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'updated': c.rowcount})

@app.route('/api/intelligence', methods=['GET'])
def get_intelligence():
    """Get CA ABC intelligence data"""
    conn = get_db_connection()
    c = conn.cursor()
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    county = request.args.get('county', '')
    
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
    
    return jsonify({
        'records': records,
        'total': total,
        'page': page,
        'per_page': per_page
    })

@app.route('/api/counties', methods=['GET'])
def get_counties():
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
    
    return jsonify({
        'lead_counties': lead_counties,
        'intelligence_counties': intel_counties
    })

@app.route('/api/pos-systems', methods=['GET'])
def get_pos_systems():
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
    
    return jsonify(systems)

@app.route('/api/queue', methods=['GET'])
def get_email_queue():
    """Get pending email queue"""
    queue_file = DATADEPOT_DIR / 'queue' / 'pending_emails.json'
    
    if not queue_file.exists():
        return jsonify({'queue': [], 'total': 0})
    
    with open(queue_file, 'r') as f:
        queue = json.load(f)
    
    return jsonify({
        'queue': queue,
        'total': len(queue),
        'ready_to_send': len([e for e in queue if datetime.fromisoformat(e['scheduled_time']) <= datetime.now()])
    })

@app.route('/api/activities', methods=['GET'])
def get_activities():
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
    
    return jsonify(activities[:20])

if __name__ == '__main__':
    # Production: Run with gunicorn
    # gunicorn -w 4 -b 0.0.0.0:8081 depotchaos_api:app
    
    # Development: Direct flask
    app.run(host='0.0.0.0', port=8081, debug=False)
