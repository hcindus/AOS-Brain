"""
Collections API Endpoints for DepotChaos FastAPI
Add these endpoints to depotchaos_fastapi.py
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Collections database path
COLLECTIONS_DB = "/root/.openclaw/workspace/datadepot/data/collections.db"

# Pydantic models
class ContactUpdateRequest(BaseModel):
    invoice_number: str
    contact_method: str  # 'phone', 'email', 'letter', 'visit'
    notes: Optional[str] = ""
    result: Optional[str] = ""  # 'no_answer', 'promised_payment', 'disputed', 'paid', 'other'

class PaymentRecordRequest(BaseModel):
    invoice_number: str
    amount: float
    payment_method: Optional[str] = "check"  # 'check', 'credit_card', 'ach', 'cash'
    reference_number: Optional[str] = ""
    notes: Optional[str] = ""

class CollectionsAccount(BaseModel):
    id: int
    customer: str
    invoice: str
    date: str
    amount: float
    status: str
    days: int
    address: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    viewed: bool
    notes: Optional[str] = ""
    priority: str
    last_contacted: Optional[str] = None
    contact_method: Optional[str] = None
    payment_received: float = 0.0

def get_collections_db():
    """Get collections database connection"""
    conn = sqlite3.connect(COLLECTIONS_DB)
    conn.row_factory = sqlite3.Row
    return conn

# API Endpoints to add to depotchaos_fastapi.py:

@app.get("/api/collections/summary")
async def get_collections_summary():
    """Get collections summary statistics"""
    try:
        conn = get_collections_db()
        cursor = conn.cursor()
        
        # Critical (>30 days)
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(amount - payment_received), 0) 
            FROM collections_accounts 
            WHERE days_overdue > 30 AND status NOT IN ('paid', 'canceled')
        """)
        critical = cursor.fetchone()
        
        # Overdue (1-30 days)
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(amount - payment_received), 0) 
            FROM collections_accounts 
            WHERE days_overdue > 0 AND days_overdue <= 30 AND status NOT IN ('paid', 'canceled')
        """)
        overdue = cursor.fetchone()
        
        # Due soon
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(amount - payment_received), 0) 
            FROM collections_accounts 
            WHERE days_overdue <= 0 AND days_overdue >= -14 AND status NOT IN ('paid', 'canceled')
        """)
        due_soon = cursor.fetchone()
        
        # Total outstanding
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(amount - payment_received), 0) 
            FROM collections_accounts 
            WHERE status NOT IN ('paid', 'canceled')
        """)
        total = cursor.fetchone()
        
        conn.close()
        
        return {
            'success': True,
            'summary': {
                'critical': {'count': critical[0], 'amount': round(critical[1], 2)},
                'overdue': {'count': overdue[0], 'amount': round(overdue[1], 2)},
                'due_soon': {'count': due_soon[0], 'amount': round(due_soon[1], 2)},
                'total': {'count': total[0], 'amount': round(total[1], 2)}
            }
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.get("/api/collections/accounts")
async def get_collections_accounts(
    status: Optional[str] = Query(None, description="Filter by status: open, contacted, promised, paid, disputed, canceled"),
    priority: Optional[str] = Query(None, description="Filter by priority: critical, high, medium, low"),
    min_days: Optional[int] = Query(None, description="Minimum days overdue"),
    limit: int = Query(100, ge=1, le=500)
):
    """Get collection accounts with optional filtering"""
    try:
        conn = get_collections_db()
        cursor = conn.cursor()
        
        query = """
            SELECT id, customer_name, invoice_number, invoice_date, amount,
                   status, days_overdue, address, email, phone, viewed, notes,
                   priority, last_contacted, contact_method, payment_received,
                   contact_result
            FROM collections_accounts
            WHERE 1=1
        """
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if priority:
            query += " AND priority = ?"
            params.append(priority)
            
        if min_days is not None:
            query += " AND days_overdue >= ?"
            params.append(min_days)
        
        query += " ORDER BY days_overdue DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        accounts = []
        for row in rows:
            accounts.append({
                'id': row[0],
                'customer': row[1],
                'invoice': row[2],
                'date': row[3],
                'amount': row[4],
                'status': row[5],
                'days': row[6],
                'address': row[7] or '',
                'email': row[8] or '',
                'phone': row[9] or '',
                'viewed': bool(row[10]),
                'notes': row[11] or '',
                'priority': row[12],
                'last_contacted': row[13],
                'contact_method': row[14],
                'payment_received': row[15] or 0.0,
                'contact_result': row[16] or ''
            })
        
        conn.close()
        
        return {
            'success': True,
            'count': len(accounts),
            'accounts': accounts
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.post("/api/collections/contact")
async def update_contact_status(request: ContactUpdateRequest):
    """Update account status after contact"""
    try:
        conn = get_collections_db()
        cursor = conn.cursor()
        
        # Get account ID
        cursor.execute(
            "SELECT id FROM collections_accounts WHERE invoice_number = ?",
            (request.invoice_number,)
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        collections_id = row[0]
        
        # Determine new status based on result
        new_status = 'contacted'
        if request.result == 'promised_payment':
            new_status = 'promised'
        elif request.result == 'paid':
            new_status = 'paid'
        elif request.result == 'disputed':
            new_status = 'disputed'
        
        # Update account
        cursor.execute("""
            UPDATE collections_accounts 
            SET status = ?, 
                last_contacted = CURRENT_TIMESTAMP,
                contact_method = ?,
                contact_result = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_status, request.contact_method, request.result, collections_id))
        
        # Add to contact history
        cursor.execute("""
            INSERT INTO contact_history 
            (collections_id, contact_method, notes, result)
            VALUES (?, ?, ?, ?)
        """, (collections_id, request.contact_method, request.notes, request.result))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'message': f'Contact recorded for invoice {request.invoice_number}',
            'status': new_status
        }
    except HTTPException:
        raise
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.post("/api/collections/payment")
async def record_payment(request: PaymentRecordRequest):
    """Record a payment received"""
    try:
        conn = get_collections_db()
        cursor = conn.cursor()
        
        # Get account
        cursor.execute(
            "SELECT id, amount FROM collections_accounts WHERE invoice_number = ?",
            (request.invoice_number,)
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        collections_id, total_amount = row
        
        # Add payment record
        cursor.execute("""
            INSERT INTO payment_tracking 
            (collections_id, payment_amount, payment_method, reference_number, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (collections_id, request.amount, request.payment_method, 
              request.reference_number, request.notes))
        
        # Update totals
        cursor.execute("""
            SELECT SUM(payment_amount) FROM payment_tracking 
            WHERE collections_id = ?
        """, (collections_id,))
        total_paid = cursor.fetchone()[0] or 0
        
        new_status = 'paid' if total_paid >= total_amount else 'partial'
        
        cursor.execute("""
            UPDATE collections_accounts 
            SET status = ?, payment_received = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_status, total_paid, collections_id))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'message': f'Payment of ${request.amount} recorded',
            'status': new_status,
            'total_paid': total_paid,
            'balance': total_amount - total_paid
        }
    except HTTPException:
        raise
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.get("/api/collections/account/{invoice_number}")
async def get_account_details(invoice_number: str):
    """Get detailed information about a specific account"""
    try:
        conn = get_collections_db()
        cursor = conn.cursor()
        
        # Get account details
        cursor.execute("""
            SELECT * FROM collections_accounts WHERE invoice_number = ?
        """, (invoice_number,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        account = dict(row)
        
        # Get contact history
        cursor.execute("""
            SELECT * FROM contact_history 
            WHERE collections_id = ? ORDER BY contact_date DESC
        """, (account['id'],))
        contacts = [dict(row) for row in cursor.fetchall()]
        
        # Get payment history
        cursor.execute("""
            SELECT * FROM payment_tracking 
            WHERE collections_id = ? ORDER BY payment_date DESC
        """, (account['id'],))
        payments = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'success': True,
            'account': account,
            'contact_history': contacts,
            'payment_history': payments
        }
    except HTTPException:
        raise
    except Exception as e:
        return {'success': False, 'error': str(e)}

print("""
Collections API Endpoints Ready

Add these to depotchaos_fastapi.py:

1. Import statements (add to existing imports)
2. Copy the function definitions above
3. Restart the service

Endpoints:
- GET /api/collections/summary - Get summary statistics
- GET /api/collections/accounts - List accounts with filters
- POST /api/collections/contact - Record contact attempt
- POST /api/collections/payment - Record payment received
- GET /api/collections/account/{invoice_number} - Get account details

Example usage:
curl -X POST http://localhost:8082/api/collections/contact \
  -H "Content-Type: application/json" \
  -d '{"invoice_number": "5126103", "contact_method": "phone", "result": "promised_payment"}'
""")
