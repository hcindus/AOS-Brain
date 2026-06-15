#!/usr/bin/env python3
"""
Complete Collections Integration for DepotChaos
Connects collections accounts to leads and tracks contact status
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Connect to both databases
COLLECTIONS_DB = "/root/.openclaw/workspace/datadepot/data/collections.db"
UNIFIED_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def connect_collections():
    conn = sqlite3.connect(COLLECTIONS_DB)
    conn.row_factory = sqlite3.Row
    return conn

def connect_unified():
    conn = sqlite3.connect(UNIFIED_DB)
    conn.row_factory = sqlite3.Row
    return conn

def link_collections_to_leads():
    """Link collection accounts to existing leads in DepotChaos"""
    
    collections_conn = connect_collections()
    unified_conn = connect_unified()
    
    c_cursor = collections_conn.cursor()
    u_cursor = unified_conn.cursor()
    
    # Get all collection accounts
    c_cursor.execute("SELECT id, customer_name, invoice_number FROM collections_accounts")
    accounts = c_cursor.fetchall()
    
    linked_count = 0
    
    for account in accounts:
        # Search for matching lead by name
        u_cursor.execute("""
            SELECT id, company_name, address, city, state, zip, 
                   contact_name, email, phone
            FROM leads 
            WHERE company_name LIKE ? OR contact_name LIKE ?
            LIMIT 1
        """, (f"%{account['customer_name']}%", f"%{account['customer_name']}%"))
        
        lead = u_cursor.fetchone()
        
        if lead:
            # Update collections account with lead info
            c_cursor.execute("""
                UPDATE collections_accounts 
                SET lead_id = ?,
                    address = COALESCE(NULLIF(address, ''), ?),
                    city = COALESCE(NULLIF(city, ''), ?),
                    state = COALESCE(NULLIF(state, ''), ?),
                    zip = COALESCE(NULLIF(zip, ''), ?),
                    email = COALESCE(NULLIF(email, ''), ?),
                    phone = COALESCE(NULLIF(phone, ''), ?)
                WHERE id = ?
            """, (
                lead['id'], 
                lead.get('address', ''),
                lead.get('city', ''),
                lead.get('state', ''),
                lead.get('zip', ''),
                lead.get('email', ''),
                lead.get('phone', ''),
                account['id']
            ))
            linked_count += 1
    
    collections_conn.commit()
    collections_conn.close()
    unified_conn.close()
    
    print(f"✅ Linked {linked_count} collection accounts to leads")
    return linked_count

def update_contact_status(invoice_number, status, notes=""):
    """Update contact status for a collection account"""
    
    conn = connect_collections()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE collections_accounts 
        SET status = ?,
            contact_result = ?,
            last_contacted = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE invoice_number = ?
    """, (status, notes, invoice_number))
    
    # Add to contact history
    cursor.execute("""
        INSERT INTO contact_history (collections_id, contact_method, notes, result)
        SELECT id, 'manual', ?, ?
        FROM collections_accounts 
        WHERE invoice_number = ?
    """, (notes, status, invoice_number))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Updated {invoice_number} to status: {status}")

def get_collection_accounts_needing_attention():
    """Get accounts that need collection follow-up"""
    
    conn = connect_collections()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            ca.*,
            l.company_name as lead_company,
            l.contact_name as lead_contact,
            l.email as lead_email,
            l.phone as lead_phone,
            l.address as lead_address
        FROM collections_accounts ca
        LEFT JOIN leads l ON ca.lead_id = l.id
        WHERE ca.status IN ('open', 'overdue', 'critical', 'contacted')
        AND ca.status NOT IN ('paid', 'canceled')
        ORDER BY ca.days_overdue DESC
    """)
    
    accounts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return accounts

def mark_as_contacted(invoice_number, contact_method="phone", result="no_answer", notes=""):
    """Mark an account as contacted"""
    
    valid_results = [
        'no_answer',          # Called, no one answered
        'promised_payment',   # Customer promised to pay
        'disputed',           # Customer disputes the charge
        'paid',               # Payment received
        'other'               # Other outcome
    ]
    
    if result not in valid_results:
        result = 'other'
    
    update_contact_status(invoice_number, result, notes)
    
    # Log to unified database activity
    unified_conn = connect_unified()
    u_cursor = unified_conn.cursor()
    
    u_cursor.execute("""
        INSERT INTO activities (activity_type, description, details, timestamp)
        VALUES ('collections_contact', ?, ?, datetime('now'))
    """, (
        f"Collections contact: {invoice_number}",
        json.dumps({
            'invoice': invoice_number,
            'method': contact_method,
            'result': result,
            'notes': notes
        })
    ))
    
    unified_conn.commit()
    unified_conn.close()

if __name__ == "__main__":
    print("🔄 Collections Integration")
    print("=" * 50)
    
    # Link to leads
    linked = link_collections_to_leads()
    
    # Show accounts needing attention
    print("\n📋 Accounts Needing Collection Follow-up:")
    print("-" * 50)
    
    accounts = get_collection_accounts_needing_attention()
    
    for acct in accounts:
        address = acct.get('address') or acct.get('lead_address') or 'NEED ADDRESS'
        print(f"\n🔸 {acct['customer_name']}")
        print(f"   Invoice: {acct['invoice_number']}")
        print(f"   Amount: ${acct['amount']:.2f}")
        print(f"   Days Overdue: {acct['days_overdue']}")
        print(f"   Address: {address}")
        print(f"   Status: {acct['status']}")
    
    print(f"\n✅ Total: {len(accounts)} accounts need attention")
    print(f"✅ {linked} accounts linked to existing leads")
