#!/usr/bin/env python3
"""
Collections CLI - Manual update tool
Usage: python collections_cli.py [command] [args]
"""

import sys
import sqlite3
from datetime import datetime
from pathlib import Path
from collections_db import CollectionsDB

DB_PATH = Path("/root/.openclaw/workspace/collections/collections.db")


def show_help():
    print("Collections Database CLI v1.0")
    print("=" * 40)
    print("Commands:")
    print("  status                    - Show collections summary")
    print("  list [overdue|unpaid|paid] - List invoices by status")
    print("  search <name>             - Search by customer name")
    print("  update <invoice_id> <status> [notes] - Update invoice status")
    print("  add <invoice_id> <name> <amount> <status> [date] - Add new invoice")
    print("  delivered <location>      - Mark deliveries complete")
    print("  export [filename]         - Export to JSON")
    print("  priority                  - Show top 10 priority collections")
    print()


def show_status():
    db = CollectionsDB()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("COLLECTIONS STATUS")
    print("=" * 60)
    
    cursor.execute("""
        SELECT status, COUNT(*), SUM(amount) 
        FROM invoices 
        GROUP BY status 
        ORDER BY SUM(amount) DESC
    """)
    
    total_outstanding = 0
    for row in cursor.fetchall():
        status, count, amount = row
        amount = amount or 0
        print(f"{status:20} | {count:3} invoices | ${amount:>12,.2f}")
        if status in ['Unpaid', 'Overdue']:
            total_outstanding += amount
    
    print("-" * 60)
    print(f"{'TOTAL OUTSTANDING':20} |         | ${total_outstanding:>12,.2f}")
    
    # Age breakdown
    print("\n--- OVERDUE BY AGE ---")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN days_overdue IS NULL THEN 'No due date'
                WHEN days_overdue <= 7 THEN '1-7 days'
                WHEN days_overdue <= 30 THEN '8-30 days'
                ELSE '30+ days'
            END as age_bucket,
            COUNT(*),
            SUM(amount)
        FROM invoices
        WHERE status = 'Overdue'
        GROUP BY age_bucket
    """)
    
    for bucket, count, amount in cursor.fetchall():
        print(f"{bucket:20} | {count:3} invoices | ${amount:>12,.2f}")
    
    conn.close()


def list_invoices(filter_status=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if filter_status:
        cursor.execute("""
            SELECT invoice_id, customer_name, amount, status, days_overdue, notes
            FROM invoices
            WHERE status = ?
            ORDER BY amount DESC
        """, (filter_status,))
        print(f"\n--- {filter_status.upper()} INVOICES ---")
    else:
        cursor.execute("""
            SELECT invoice_id, customer_name, amount, status, days_overdue, notes
            FROM invoices
            ORDER BY status, amount DESC
        """)
        print("\n--- ALL INVOICES ---")
    
    print(f"{'Invoice ID':<12} {'Amount':>10} {'Status':<12} {'Days':>5} {'Customer'}")
    print("-" * 80)
    
    for row in cursor.fetchall():
        inv_id, customer, amount, status, days, notes = row
        days_str = str(days) if days else "-"
        customer_short = customer[:25] + "..." if len(customer) > 25 else customer
        print(f"{inv_id:<12} ${amount:>9,.2f} {status:<12} {days_str:>5} {customer_short}")
    
    conn.close()


def search_invoices(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT invoice_id, customer_name, amount, status, days_overdue, notes
        FROM invoices
        WHERE customer_name LIKE ?
        ORDER BY amount DESC
    """, (f'%{name}%',))
    
    results = cursor.fetchall()
    
    print(f"\n--- SEARCH RESULTS FOR '{name}' ---")
    print(f"Found {len(results)} matches")
    
    if results:
        print(f"{'Invoice ID':<12} {'Amount':>10} {'Status':<12} {'Customer'}")
        print("-" * 60)
        for row in results:
            inv_id, customer, amount, status, days, notes = row
            print(f"{inv_id:<12} ${amount:>9,.2f} {status:<12} {customer}")
    
    conn.close()


def update_invoice(invoice_id, new_status, notes=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Validate status
    valid_statuses = ['Paid', 'Unpaid', 'Overdue', 'Draft', 'Canceled', 'Payment pending', 'Undelivered', 'Refunded']
    if new_status not in valid_statuses:
        print(f"Error: Invalid status. Must be one of: {', '.join(valid_statuses)}")
        return
    
    cursor.execute("SELECT * FROM invoices WHERE invoice_id = ?", (invoice_id,))
    existing = cursor.fetchone()
    
    if not existing:
        print(f"Error: Invoice {invoice_id} not found")
        return
    
    updates = ["status = ?", "last_updated = CURRENT_TIMESTAMP"]
    params = [new_status]
    
    if notes:
        updates.append("notes = ?")
        params.append(notes)
    
    if new_status == 'Paid':
        updates.append("paid_date = ?")
        params.append(datetime.now().strftime('%m/%d/%Y'))
    
    params.append(invoice_id)
    
    cursor.execute(f"""
        UPDATE invoices 
        SET {', '.join(updates)}
        WHERE invoice_id = ?
    """, params)
    
    conn.commit()
    print(f"Updated invoice {invoice_id} → {new_status}")
    conn.close()


def mark_delivered(location):
    """Mark deliveries as complete - for Captain's route updates"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"\n--- MARKING DELIVERIES FOR {location.upper()} ---")
    
    # Find invoices associated with this delivery location
    # This is a simplified version - in practice you'd match by customer name or have a delivery table
    
    # Update Tacos Sinaloa for Oakland delivery
    if 'oakland' in location.lower():
        cursor.execute("""
            UPDATE invoices 
            SET notes = COALESCE(notes, '') || '; Proposal delivered 06/19/2026',
                last_updated = CURRENT_TIMESTAMP
            WHERE customer_name LIKE '%Tacos Sinaloa%'
        """)
        print("Marked: Tacos Sinaloa - Oakland Marlem (Proposal delivered)")
    
    if 'roseville' in location.lower():
        cursor.execute("""
            UPDATE invoices 
            SET notes = COALESCE(notes, '') || '; Proposal delivered 06/19/2026',
                last_updated = CURRENT_TIMESTAMP
            WHERE customer_name LIKE '%Tomatina%'
        """)
        print("Marked: Tomatina - Roseville (Proposal delivered)")
    
    conn.commit()
    conn.close()
    print(f"\nDelivery logged for {location}")


def show_priority():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("TOP 10 PRIORITY COLLECTIONS")
    print("=" * 70)
    
    cursor.execute("""
        SELECT invoice_id, customer_name, amount, status, days_overdue, notes
        FROM invoices
        WHERE status IN ('Overdue', 'Unpaid')
        ORDER BY amount DESC
        LIMIT 10
    """)
    
    print(f"{'#':<3} {'Amount':>10} {'Status':<10} {'Days':>5} {'Customer / Notes'}")
    print("-" * 70)
    
    for i, row in enumerate(cursor.fetchall(), 1):
        inv_id, customer, amount, status, days, notes = row
        days_str = f"{days}d" if days else "-"
        note_short = notes[:30] + "..." if notes and len(notes) > 30 else (notes or "")
        print(f"{i:<3} ${amount:>9,.2f} {status:<10} {days_str:>5} {customer}")
        if note_short:
            print(f"    Notes: {note_short}")
        print()
    
    conn.close()


def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'status':
        show_status()
    elif command == 'list':
        filter_status = sys.argv[2] if len(sys.argv) > 2 else None
        list_invoices(filter_status)
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Usage: search <name>")
            return
        search_invoices(sys.argv[2])
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Usage: update <invoice_id> <status> [notes]")
            return
        notes = sys.argv[4] if len(sys.argv) > 4 else None
        update_invoice(sys.argv[2], sys.argv[3], notes)
    elif command == 'delivered':
        if len(sys.argv) < 3:
            print("Usage: delivered <location>")
            return
        mark_delivered(sys.argv[2])
    elif command == 'priority':
        show_priority()
    elif command == 'export':
        filename = sys.argv[2] if len(sys.argv) > 2 else f"export_{datetime.now().strftime('%Y-%m-%d')}.json"
        db = CollectionsDB()
        db.export_to_json(f"/root/.openclaw/workspace/collections/{filename}")
    else:
        show_help()


if __name__ == "__main__":
    main()
