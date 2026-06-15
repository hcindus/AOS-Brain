#!/usr/bin/env python3
"""
Setup Collections Status Tracking in DepotChaos
Simple integration for updating contact status
"""

import sqlite3
from datetime import datetime
from pathlib import Path

COLLECTIONS_DB = "/root/.openclaw/workspace/datadepot/data/collections.db"

def mark_account_contacted(invoice_number, contact_method, result, notes=""):
    """
    Mark a collection account as contacted
    
    Args:
        invoice_number: The invoice number
        contact_method: 'phone', 'email', 'letter', 'visit'
        result: 'no_answer', 'promised_payment', 'disputed', 'paid', 'other'
        notes: Optional notes
    """
    conn = sqlite3.connect(COLLECTIONS_DB)
    cursor = conn.cursor()
    
    # Check if account exists
    cursor.execute(
        "SELECT id FROM collections_accounts WHERE invoice_number = ?",
        (invoice_number,)
    )
    row = cursor.fetchone()
    
    if not row:
        print(f"❌ Invoice {invoice_number} not found")
        conn.close()
        return False
    
    collections_id = row[0]
    
    # Update account status
    new_status = 'contacted'
    if result == 'promised_payment':
        new_status = 'promised'
    elif result == 'paid':
        new_status = 'paid'
    elif result == 'disputed':
        new_status = 'disputed'
    
    cursor.execute("""
        UPDATE collections_accounts 
        SET status = ?,
            contact_method = ?,
            contact_result = ?,
            last_contacted = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (new_status, contact_method, result, collections_id))
    
    # Record in contact history
    cursor.execute("""
        INSERT INTO contact_history 
        (collections_id, contact_method, notes, result)
        VALUES (?, ?, ?, ?)
    """, (collections_id, contact_method, notes, result))
    
    conn.commit()
    conn.close()
    
    print(f"✅ {invoice_number}: Marked as {result} via {contact_method}")
    return True

def show_all_accounts():
    """Display all collection accounts"""
    conn = sqlite3.connect(COLLECTIONS_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT customer_name, invoice_number, amount, days_overdue, 
               status, last_contacted, contact_result
        FROM collections_accounts
        ORDER BY days_overdue DESC
    """)
    
    accounts = cursor.fetchall()
    conn.close()
    
    print("\n📊 COLLECTIONS ACCOUNTS")
    print("=" * 80)
    print(f"{'Customer':<25} {'Invoice':<12} {'Amount':>10} {'Days':>6} {'Status':<15}")
    print("-" * 80)
    
    for acct in accounts:
        print(f"{acct['customer_name']:<25} {acct['invoice_number']:<12} "
              f"${acct['amount']:>8.2f} {acct['days_overdue']:>6} "
              f"{acct['status']:<15}")
    
    print(f"\nTotal: {len(accounts)} accounts")
    return accounts

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # Show all accounts
        show_all_accounts()
        
        print("\n" + "=" * 80)
        print("Usage to update status:")
        print("  python3 setup_collections_status.py update INVOICE_NUMBER METHOD RESULT [NOTES]")
        print("\nExample:")
        print("  python3 setup_collections_status.py update 5126103 phone promised_payment 'Will pay Friday'")
        
    elif sys.argv[1] == "update" and len(sys.argv) >= 5:
        # Update status
        invoice = sys.argv[2]
        method = sys.argv[3]
        result = sys.argv[4]
        notes = sys.argv[5] if len(sys.argv) > 5 else ""
        
        mark_account_contacted(invoice, method, result, notes)
        
        # Show updated list
        print("\n")
        show_all_accounts()
