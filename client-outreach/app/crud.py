import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime
from models import ClientCreate, ClientUpdate

DB_PATH = '/root/.openclaw/workspace/client-outreach/database/outreach.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema"""
    with open('/root/.openclaw/workspace/client-outreach/database/schema.sql', 'r') as f:
        schema = f.read()
    conn = get_db_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()

# Client CRUD Operations

def create_client(client: ClientCreate) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO clients (name, email, phone, company, business_type, city, state, 
                           tier, status, pos_system, replacement_score, last_contact, 
                           next_contact, notes, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (client.name, client.email, client.phone, client.company, client.business_type,
          client.city, client.state, client.tier, client.status, client.pos_system,
          client.replacement_score, client.last_contact, client.next_contact, 
          client.notes, datetime.now().isoformat()))
    
    conn.commit()
    client_id = cursor.lastrowid
    conn.close()
    
    return get_client(client_id)

def get_client(client_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_clients(
    status: Optional[str] = None,
    tier: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    per_page: int = 50
) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build WHERE clause
    where_clauses = ["1=1"]
    params = []
    
    if status:
        where_clauses.append("status = ?")
        params.append(status)
    if tier:
        where_clauses.append("tier = ?")
        params.append(tier)
    if search:
        where_clauses.append("(name LIKE ? OR email LIKE ? OR company LIKE ?)")
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    
    where_sql = " AND ".join(where_clauses)
    
    # Get total count
    cursor.execute(f'SELECT COUNT(*) FROM clients WHERE {where_sql}', params)
    total = cursor.fetchone()[0]
    
    # Get paginated results
    offset = (page - 1) * per_page
    cursor.execute(f'''
        SELECT * FROM clients 
        WHERE {where_sql}
        ORDER BY next_contact ASC, created_at DESC
        LIMIT ? OFFSET ?
    ''', params + [per_page, offset])
    
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return {
        'total': total,
        'clients': rows,
        'page': page,
        'per_page': per_page
    }

def update_client(client_id: int, updates: ClientUpdate) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build dynamic UPDATE
    update_fields = []
    params = []
    
    for field, value in updates.dict(exclude_unset=True).items():
        if value is not None:
            update_fields.append(f"{field} = ?")
            params.append(value)
    
    if not update_fields:
        return get_client(client_id)
    
    update_fields.append("updated_at = ?")
    params.append(datetime.now().isoformat())
    params.append(client_id)
    
    cursor.execute(f'''
        UPDATE clients 
        SET {', '.join(update_fields)}
        WHERE id = ?
    ''', params)
    
    conn.commit()
    conn.close()
    
    return get_client(client_id)

def delete_client(client_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def get_clients_needing_contact() -> List[dict]:
    """Get clients where next_contact is today or earlier"""
    conn = get_db_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT * FROM clients 
        WHERE next_contact <= ? AND status IN ('new', 'prospect', 'follow-up')
        ORDER BY replacement_score DESC, next_contact ASC
    ''', (today,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# Activity Operations

def add_activity(client_id: int, activity_type: str, description: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activities (client_id, type, description)
        VALUES (?, ?, ?)
    ''', (client_id, activity_type, description))
    conn.commit()
    activity_id = cursor.lastrowid
    
    # Also update last_contact on client
    cursor.execute('''
        UPDATE clients SET last_contact = ?, updated_at = ? WHERE id = ?
    ''', (datetime.now().strftime('%Y-%m-%d'), datetime.now().isoformat(), client_id))
    conn.commit()
    
    # Get the activity
    cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_client_activities(client_id: int, limit: int = 20) -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM activities 
        WHERE client_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (client_id, limit))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# Email Queue Operations

def schedule_email(client_id: int, template: str, subject: str, 
                   scheduled_at: str, body: Optional[str] = None) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO email_queue (client_id, template, subject, body, scheduled_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (client_id, template, subject, body, scheduled_at))
    conn.commit()
    email_id = cursor.lastrowid
    conn.close()
    return get_email(email_id)

def get_email(email_id: int) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM email_queue WHERE id = ?', (email_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_pending_emails(limit: int = 100) -> List[dict]:
    """Get emails ready to send (scheduled_at <= now)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute('''
        SELECT e.*, c.name as client_name, c.email as client_email, c.company
        FROM email_queue e
        JOIN clients c ON e.client_id = c.id
        WHERE e.status = 'pending' AND e.scheduled_at <= ?
        ORDER BY e.scheduled_at ASC
        LIMIT ?
    ''', (now, limit))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def mark_email_sent(email_id: int, error: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    status = 'failed' if error else 'sent'
    cursor.execute('''
        UPDATE email_queue 
        SET status = ?, sent_at = ?, error = ?
        WHERE id = ?
    ''', (status, now, error, email_id))
    conn.commit()
    conn.close()

def get_email_queue_stats() -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT status, COUNT(*) FROM email_queue GROUP BY status
    ''')
    stats = dict(cursor.fetchall())
    conn.close()
    return {
        'pending': stats.get('pending', 0),
        'sent': stats.get('sent', 0),
        'failed': stats.get('failed', 0)
    }
