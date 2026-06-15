#!/usr/bin/env python3
"""
Collections Integration for DepotChaos
Manages accounts receivable and payment tracking
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class CollectionsManager:
    def __init__(self, db_path: str = "/root/.openclaw/workspace/datadepot/data/collections.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize collections database with proper schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Collections accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collections_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                invoice_number TEXT UNIQUE NOT NULL,
                invoice_date TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'open',
                days_overdue INTEGER DEFAULT 0,
                address TEXT,
                email TEXT,
                phone TEXT,
                viewed BOOLEAN DEFAULT 0,
                notes TEXT,
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_contacted TIMESTAMP,
                contact_method TEXT,
                contact_result TEXT,
                payment_received REAL DEFAULT 0.0,
                payment_date TIMESTAMP,
                lead_id INTEGER,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        """)
        
        # Contact history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collections_id INTEGER NOT NULL,
                contact_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                contact_method TEXT,
                notes TEXT,
                result TEXT,
                follow_up_date TIMESTAMP,
                FOREIGN KEY (collections_id) REFERENCES collections_accounts(id)
            )
        """)
        
        # Payment tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collections_id INTEGER NOT NULL,
                payment_amount REAL NOT NULL,
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method TEXT,
                reference_number TEXT,
                notes TEXT,
                FOREIGN KEY (collections_id) REFERENCES collections_accounts(id)
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"✅ Collections database initialized at {self.db_path}")
    
    def import_collection_accounts(self, accounts: List[Dict]):
        """Import collection accounts into the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        imported = 0
        updated = 0
        
        for account in accounts:
            # Check if account already exists
            cursor.execute(
                "SELECT id FROM collections_accounts WHERE invoice_number = ?",
                (account['invoice'],)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing
                cursor.execute("""
                    UPDATE collections_accounts 
                    SET customer_name = ?, invoice_date = ?, amount = ?,
                        status = ?, days_overdue = ?, address = ?, email = ?,
                        viewed = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE invoice_number = ?
                """, (
                    account['customer'], account['date'], account['amount'],
                    account['status'], account['days'], account.get('address', ''),
                    account.get('email', ''), account.get('viewed', False),
                    account.get('note', ''), account['invoice']
                ))
                updated += 1
            else:
                # Insert new
                priority = 'critical' if account['days'] > 30 else 'high' if account['days'] > 0 else 'medium'
                
                cursor.execute("""
                    INSERT INTO collections_accounts 
                    (customer_name, invoice_number, invoice_date, amount, status,
                     days_overdue, address, email, viewed, notes, priority)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    account['customer'], account['invoice'], account['date'],
                    account['amount'], account['status'], account['days'],
                    account.get('address', ''), account.get('email', ''),
                    account.get('viewed', False), account.get('note', ''), priority
                ))
                imported += 1
        
        conn.commit()
        conn.close()
        
        return {'imported': imported, 'updated': updated}
    
    def update_contact_status(self, invoice_number: str, contact_method: str, 
                              notes: str = "", result: str = "") -> bool:
        """Update account status after contact"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get the collections account ID
        cursor.execute(
            "SELECT id FROM collections_accounts WHERE invoice_number = ?",
            (invoice_number,)
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        collections_id = row[0]
        
        # Update the account
        cursor.execute("""
            UPDATE collections_accounts 
            SET status = 'contacted', 
                last_contacted = CURRENT_TIMESTAMP,
                contact_method = ?,
                contact_result = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (contact_method, result, collections_id))
        
        # Add to contact history
        cursor.execute("""
            INSERT INTO contact_history 
            (collections_id, contact_method, notes, result)
            VALUES (?, ?, ?, ?)
        """, (collections_id, contact_method, notes, result))
        
        conn.commit()
        conn.close()
        return True
    
    def record_payment(self, invoice_number: str, amount: float, 
                       payment_method: str = "", reference: str = "") -> bool:
        """Record a payment received"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get the collections account ID
        cursor.execute(
            "SELECT id, amount FROM collections_accounts WHERE invoice_number = ?",
            (invoice_number,)
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return False
        
        collections_id, total_amount = row
        
        # Add payment record
        cursor.execute("""
            INSERT INTO payment_tracking 
            (collections_id, payment_amount, payment_method, reference_number)
            VALUES (?, ?, ?, ?)
        """, (collections_id, amount, payment_method, reference))
        
        # Update totals
        cursor.execute("""
            SELECT SUM(payment_amount) FROM payment_tracking 
            WHERE collections_id = ?
        """, (collections_id,))
        total_paid = cursor.fetchone()[0] or 0
        
        new_status = 'paid' if total_paid >= total_amount else 'partial'
        
        cursor.execute("""
            UPDATE collections_accounts 
            SET status = ?, payment_received = ?, payment_date = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_status, total_paid, collections_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_collections_summary(self) -> Dict:
        """Get summary statistics"""
        conn = sqlite3.connect(self.db_path)
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
            'critical_count': critical[0],
            'critical_amount': critical[1],
            'overdue_count': overdue[0],
            'overdue_amount': overdue[1],
            'due_soon_count': due_soon[0],
            'due_soon_amount': due_soon[1],
            'total_count': total[0],
            'total_amount': total[1]
        }
    
    def get_all_accounts(self, status_filter: str = None) -> List[Dict]:
        """Get all collection accounts with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT id, customer_name, invoice_number, invoice_date, amount,
                   status, days_overdue, address, email, phone, viewed, notes,
                   priority, last_contacted, contact_method, payment_received
            FROM collections_accounts
        """
        
        if status_filter:
            query += f" WHERE status = '{status_filter}'"
        
        query += " ORDER BY days_overdue DESC"
        
        cursor.execute(query)
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
                'address': row[7],
                'email': row[8],
                'phone': row[9],
                'viewed': row[10],
                'notes': row[11],
                'priority': row[12],
                'last_contacted': row[13],
                'contact_method': row[14],
                'payment_received': row[15]
            })
        
        conn.close()
        return accounts

# Collection accounts data from sales log
COLLECTION_ACCOUNTS = [
    # Critical (>30 days overdue)
    {'date': '04/11/2026', 'customer': 'Emmanual', 'email': '', 'invoice': '000008', 'amount': 675.00, 'status': 'Overdue', 'days': 65, 'viewed': False, 'note': 'CONNECTION ISSUES - MICROSALE - HIGHEST PRIORITY', 'address': '1234 Tech Blvd, Los Angeles, CA 90012'},
    {'date': '05/13/2026', 'customer': 'Fernando', 'email': '', 'invoice': '5126103', 'amount': 421.56, 'status': 'Overdue', 'days': 33, 'viewed': True, 'note': 'CRITICAL - Priority follow-up', 'address': '5678 Main Street, Los Angeles, CA 90012'},
    
    # Overdue (1-30 days)
    {'date': '05/12/2026', 'customer': 'Becky NCC', 'email': '', 'invoice': '5126101', 'amount': 312.24, 'status': 'Overdue', 'days': 4, 'viewed': True, 'address': '9012 Newport Center Dr, Newport Beach, CA 92660'},
    {'date': '05/07/2026', 'customer': 'Scott Walsh', 'email': '', 'invoice': '05056101', 'amount': 382.30, 'status': 'Overdue', 'days': 9, 'viewed': True, 'address': '3456 Van Ness Ave, Fresno, CA 93721'},
    {'date': '05/07/2026', 'customer': 'Jen Yang SUPPLY ONLY', 'email': '', 'invoice': '4306104', 'amount': 520.86, 'status': 'Overdue', 'days': 10, 'viewed': True, 'address': '7890 Harbor Blvd, Anaheim, CA 92802'},
    {'date': '05/05/2026', 'customer': 'Travis Hauffman', 'email': '', 'invoice': '4306102', 'amount': 163.24, 'status': 'Overdue', 'days': 11, 'viewed': True, 'address': '1234 Palm Canyon Dr, Palm Springs, CA 92264'},
    {'date': '04/30/2026', 'customer': 'Heather Manager', 'email': '', 'invoice': '4276102', 'amount': 434.09, 'status': 'Overdue', 'days': 16, 'viewed': True, 'note': 'Courtesy invoice', 'address': '5678 Mission St, Sacramento, CA 95814'},
    {'date': '04/22/2026', 'customer': 'Bo Thompson SUPPLY ONLY', 'email': '', 'invoice': '4166114', 'amount': 329.75, 'status': 'Overdue', 'days': 24, 'viewed': True, 'address': '9012 Broadway, Oakland, CA 94607'},
    {'date': '04/23/2026', 'customer': 'Travis Hauffman', 'email': '', 'invoice': '4166108', 'amount': 242.67, 'status': 'Overdue', 'days': 26, 'viewed': True, 'address': '1234 Palm Canyon Dr, Palm Springs, CA 92264'},
]

if __name__ == "__main__":
    # Initialize manager and import data
    manager = CollectionsManager()
    result = manager.import_collection_accounts(COLLECTION_ACCOUNTS)
    
    print(f"\n✅ Collections Integration Complete")
    print(f"   Imported: {result['imported']}")
    print(f"   Updated: {result['updated']}")
    
    # Show summary
    summary = manager.get_collections_summary()
    print(f"\n📊 Collections Summary:")
    print(f"   Critical (>30 days): {summary['critical_count']} accounts, ${summary['critical_amount']:,.2f}")
    print(f"   Overdue (1-30 days): {summary['overdue_count']} accounts, ${summary['overdue_amount']:,.2f}")
    print(f"   Total Outstanding: {summary['total_count']} accounts, ${summary['total_amount']:,.2f}")
