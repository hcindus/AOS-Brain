#!/usr/bin/env python3
"""
Update Collections with new sales log data
Extracts only accounts requiring collection action
"""

import sqlite3
from datetime import datetime

COLLECTIONS_DB = "/root/.openclaw/workspace/datadepot/data/collections.db"

# New collection accounts from sales log
# Format: date, customer, invoice, amount, status, days, viewed, note
NEW_COLLECTIONS = [
    # CRITICAL - Overdue by 24+ days
    {'date': '05/26/2026', 'customer': 'Bo Thompson SUPPLY ONLY', 'invoice': '4166114', 'amount': 329.75, 'status': 'Overdue', 'days': 24, 'viewed': True, 'note': 'Supply only'},
    
    # Due Today (06/15/2026)
    {'date': '06/15/2026', 'customer': 'Kevin Manager', 'invoice': '061326005', 'amount': 402.90, 'status': 'Unpaid', 'days': 0, 'viewed': False, 'note': 'Due today'},
    {'date': '06/15/2026', 'customer': 'Kelly left msg', 'invoice': '061326004', 'amount': 300.73, 'status': 'Unpaid', 'days': 0, 'viewed': False, 'note': 'Due today - Left message'},
    {'date': '06/15/2026', 'customer': 'Morris Owner', 'invoice': '061326002', 'amount': 4883.85, 'status': 'Unpaid', 'days': 0, 'viewed': False, 'note': 'Due today - Sam4s POS system - LARGE AMOUNT'},
    {'date': '06/15/2026', 'customer': 'Sam Owner', 'invoice': '061326003', 'amount': 1272.00, 'status': 'Unpaid', 'days': 0, 'viewed': False, 'note': 'Due today'},
    
    # Overdue 1-3 days
    {'date': '06/15/2026', 'customer': 'Oona open store', 'invoice': '060826003', 'amount': 575.63, 'status': 'Overdue', 'days': 3, 'viewed': True, 'note': 'Yesterday - Open store'},
    {'date': '06/15/2026', 'customer': 'Ali Saleh', 'invoice': '061326001', 'amount': 500.00, 'status': 'Overdue', 'days': 1, 'viewed': True, 'note': 'Yesterday - Sam4s SPT 4740'},
    
    # Undelivered
    {'date': '06/15/2026', 'customer': 'Gabby Park Caféb Group', 'invoice': '061026002', 'amount': 410.19, 'status': 'Undelivered', 'days': -26, 'viewed': False, 'note': 'Undelivered - Due in 26 days'},
    {'date': '06/12/2026', 'customer': 'Gilbert General Manager', 'invoice': '060826009', 'amount': 539.67, 'status': 'Undelivered', 'days': -23, 'viewed': False, 'note': 'Undelivered - Due in 23 days'},
    
    # Due Soon (1-4 weeks out)
    {'date': '06/12/2026', 'customer': 'Cindy or Beth Cd @ 2 months', 'invoice': '061026005', 'amount': 756.01, 'status': 'Unpaid', 'days': -27, 'viewed': False, 'note': 'Cd @ 2 months'},
    {'date': '06/12/2026', 'customer': 'Francesco open', 'invoice': '061026004', 'amount': 938.35, 'status': 'Draft', 'days': -27, 'viewed': False, 'note': 'Draft - Send now'},
    {'date': '06/11/2026', 'customer': 'Laura', 'invoice': '061026003', 'amount': 213.68, 'status': 'Unpaid', 'days': -26, 'viewed': True, 'note': 'Due in 26 days'},
    {'date': '06/11/2026', 'customer': 'Tony Salinas', 'invoice': '052626007', 'amount': 457.99, 'status': 'Unpaid', 'days': -13, 'viewed': True, 'note': 'Due in 13 days'},
    {'date': '06/11/2026', 'customer': 'Myly', 'invoice': '061026001', 'amount': 929.23, 'status': 'Unpaid', 'days': -25, 'viewed': True, 'note': 'Due in 25 days'},
    {'date': '06/10/2026', 'customer': 'Sergio Frigerio NCC', 'invoice': '060826008', 'amount': 507.16, 'status': 'Canceled', 'days': -26, 'viewed': True, 'note': 'Canceled on 06/10'},
    {'date': '06/08/2026', 'customer': 'Maria Abundiz', 'invoice': '060826007', 'amount': 290.84, 'status': 'Unpaid', 'days': -23, 'viewed': True, 'note': 'Due in 23 days'},
    {'date': '06/08/2026', 'customer': 'Caffe Greco', 'invoice': '060826005', 'amount': 104.63, 'status': 'Unpaid', 'days': -23, 'viewed': True, 'note': 'Due in 23 days'},
    {'date': '06/08/2026', 'customer': 'John Caine', 'invoice': '060826002', 'amount': 928.98, 'status': 'Unpaid', 'days': -23, 'viewed': True, 'note': 'Due in 23 days'},
    {'date': '06/02/2026', 'customer': 'Renee loscaporalestaqueria@outlook.com', 'invoice': '000015', 'amount': 360.45, 'status': 'Unpaid', 'days': -17, 'viewed': False, 'note': 'NOT VIEWED - Due in 17 days'},
    {'date': '06/02/2026', 'customer': 'Ema Kye', 'invoice': '060226004', 'amount': 150.36, 'status': 'Unpaid', 'days': -17, 'viewed': True, 'note': 'Due in 17 days'},
    {'date': '06/02/2026', 'customer': 'Joycelin Magno', 'invoice': '060226003', 'amount': 230.93, 'status': 'Unpaid', 'days': -17, 'viewed': True, 'note': 'Due in 17 days'},
    {'date': '06/02/2026', 'customer': 'Salam Naser CASIO', 'invoice': '060126005', 'amount': 0.00, 'status': 'Draft', 'days': -17, 'viewed': False, 'note': 'Draft - Send now'},
    {'date': '06/02/2026', 'customer': 'John', 'invoice': '060126003', 'amount': 161.22, 'status': 'Unpaid', 'days': -17, 'viewed': False, 'note': 'NOT VIEWED - Due in 17 days'},
    {'date': '06/02/2026', 'customer': 'Margarito General Manager', 'invoice': '060126001', 'amount': 512.41, 'status': 'Unpaid', 'days': -14, 'viewed': True, 'note': 'Due in 14 days'},
    
    # Overdue from May
    {'date': '05/29/2026', 'customer': 'Sam Owner', 'invoice': '052626008', 'amount': 285.00, 'status': 'Overdue', 'days': 17, 'viewed': True, 'note': '17 days overdue'},
    {'date': '05/29/2026', 'customer': 'Cory Manager', 'invoice': '052226002', 'amount': 489.35, 'status': 'Unpaid', 'days': -6, 'viewed': True, 'note': 'Due in 6 days'},
    {'date': '05/27/2026', 'customer': 'Becky NCC', 'invoice': '052626006', 'amount': 249.14, 'status': 'Unpaid', 'days': -11, 'viewed': True, 'note': 'Due in 11 days'},
    {'date': '05/26/2026', 'customer': 'Travis Hauffman', 'invoice': '052626001', 'amount': 149.90, 'status': 'Unpaid', 'days': -10, 'viewed': True, 'note': 'Due in 10 days'},
    {'date': '05/26/2026', 'customer': 'Travis Hauffman', 'invoice': '052626002', 'amount': 149.90, 'status': 'Unpaid', 'days': -10, 'viewed': True, 'note': 'Due in 10 days'},
    {'date': '05/23/2026', 'customer': 'Michael General Manager', 'invoice': '052226003', 'amount': 386.90, 'status': 'Unpaid', 'days': -7, 'viewed': True, 'note': 'Due in 7 days'},
    {'date': '05/22/2026', 'customer': 'Katie Rondeau', 'invoice': '052226001', 'amount': 553.00, 'status': 'Unpaid', 'days': -6, 'viewed': True, 'note': 'Due in 6 days - ORDER # 639326'},
    {'date': '05/20/2026', 'customer': 'Katie Rondeau', 'invoice': '052026001', 'amount': 178.00, 'status': 'Unpaid', 'days': -4, 'viewed': True, 'note': 'Due in 4 days - ORDER # 642281'},
    {'date': '05/31/2026', 'customer': 'Robert Guerra', 'invoice': '052626010', 'amount': 3980.00, 'status': 'Draft', 'days': -15, 'viewed': False, 'note': 'Draft - Send now - LARGE AMOUNT'},
]

def update_collections_database():
    conn = sqlite3.connect(COLLECTIONS_DB)
    cursor = conn.cursor()
    
    imported = 0
    updated = 0
    
    for account in NEW_COLLECTIONS:
        # Check if invoice already exists
        cursor.execute(
            "SELECT id FROM collections_accounts WHERE invoice_number = ?",
            (account['invoice'],)
        )
        existing = cursor.fetchone()
        
        # Determine priority
        if account['days'] > 30:
            priority = 'critical'
        elif account['days'] > 0:
            priority = 'high'
        elif account['status'] == 'Draft':
            priority = 'medium'
        else:
            priority = 'low'
        
        if existing:
            # Update existing record
            cursor.execute("""
                UPDATE collections_accounts 
                SET customer_name = ?, invoice_date = ?, amount = ?,
                    status = ?, days_overdue = ?, viewed = ?, 
                    notes = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
                WHERE invoice_number = ?
            """, (
                account['customer'], account['date'], account['amount'],
                account['status'], account['days'], account['viewed'],
                account['note'], priority, account['invoice']
            ))
            updated += 1
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO collections_accounts 
                (customer_name, invoice_number, invoice_date, amount, status,
                 days_overdue, viewed, notes, priority)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                account['customer'], account['invoice'], account['date'],
                account['amount'], account['status'], account['days'],
                account['viewed'], account['note'], priority
            ))
            imported += 1
    
    conn.commit()
    
    # Get summary
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN days_overdue > 30 AND status NOT IN ('paid', 'canceled') THEN amount ELSE 0 END) as critical,
            SUM(CASE WHEN days_overdue > 0 AND days_overdue <= 30 AND status NOT IN ('paid', 'canceled') THEN amount ELSE 0 END) as overdue,
            SUM(CASE WHEN days_overdue <= 0 AND status NOT IN ('paid', 'canceled') THEN amount ELSE 0 END) as due_soon,
            COUNT(*) as total
        FROM collections_accounts
        WHERE status NOT IN ('paid', 'canceled')
    """)
    
    summary = cursor.fetchone()
    conn.close()
    
    return {
        'imported': imported,
        'updated': updated,
        'critical_amount': summary[0] or 0,
        'overdue_amount': summary[1] or 0,
        'due_soon_amount': summary[2] or 0,
        'total_accounts': summary[3]
    }

if __name__ == "__main__":
    print("🔄 Updating Collections Database...")
    print("=" * 60)
    
    result = update_collections_database()
    
    print(f"\n✅ Update Complete!")
    print(f"   New accounts added: {result['imported']}")
    print(f"   Accounts updated: {result['updated']}")
    print(f"\n💰 Financial Summary:")
    print(f"   Critical (>30 days): ${result['critical_amount']:,.2f}")
    print(f"   Overdue (1-30 days): ${result['overdue_amount']:,.2f}")
    print(f"   Due Soon/Future: ${result['due_soon_amount']:,.2f}")
    print(f"\n📊 Total active accounts: {result['total_accounts']}")
    
    print("\n⚠️  PRIORITY ACTIONS NEEDED:")
    print("   1. Morris Owner - $4,883.85 DUE TODAY (Sam4s POS)")
    print("   2. Robert Guerra - $3,980.00 DRAFT (Send now)")
    print("   3. Bo Thompson - $329.75 OVERDUE 24 days")
    print("   4. Sam Owner - $1,272.00 DUE TODAY")
