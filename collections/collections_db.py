#!/usr/bin/env python3
"""
Collections Database Manager v1.0
Permanent fix for invoice/collections tracking
"""

import sqlite3
import re
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = Path("/root/.openclaw/workspace/collections/collections.db")

class CollectionsDB:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_db()
    
    def init_db(self):
        """Initialize database with proper schema"""
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id TEXT UNIQUE NOT NULL,
                customer_name TEXT,
                amount REAL,
                status TEXT CHECK(status IN ('Paid', 'Unpaid', 'Overdue', 'Draft', 'Canceled', 'Payment pending', 'Undelivered', 'Refunded')),
                invoice_date TEXT,
                due_date TEXT,
                paid_date TEXT,
                days_overdue INTEGER,
                notes TEXT,
                viewed BOOLEAN DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sync_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                records_processed INTEGER,
                errors TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def upsert_invoice(self, record):
        """Insert or update an invoice record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO invoices 
                (invoice_id, customer_name, amount, status, invoice_date, due_date, paid_date, 
                 days_overdue, notes, viewed, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(invoice_id) DO UPDATE SET
                    customer_name=excluded.customer_name,
                    amount=excluded.amount,
                    status=excluded.status,
                    invoice_date=excluded.invoice_date,
                    due_date=excluded.due_date,
                    paid_date=excluded.paid_date,
                    days_overdue=excluded.days_overdue,
                    notes=excluded.notes,
                    viewed=excluded.viewed,
                    last_updated=CURRENT_TIMESTAMP
            ''', (
                record.get('invoice_id'),
                record.get('customer_name'),
                record.get('amount'),
                record.get('status'),
                record.get('invoice_date'),
                record.get('due_date'),
                record.get('paid_date'),
                record.get('days_overdue'),
                record.get('notes'),
                record.get('viewed', False)
            ))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error upserting {record.get('invoice_id')}: {e}")
            return False
        finally:
            conn.close()
    
    def parse_text_dump(self, text):
        """Parse invoice data from text dump format"""
        records = []
        lines = text.strip().split('\n')
        
        current_record = {}
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for amount and date pattern (e.g., "$425.61", "06/19/2026")
            amount_match = re.match(r'^\$([\d,]+\.\d{2})$', line)
            date_match = re.match(r'^(\d{2}/\d{2}/\d{4})$', line)
            
            if amount_match and i + 1 < len(lines):
                # This looks like a record start
                amount = float(amount_match.group(1).replace(',', ''))
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                
                # Check if next line is a date (invoice date)
                if re.match(r'^\d{2}/\d{2}/\d{4}$', next_line):
                    current_record = {
                        'amount': amount,
                        'invoice_date': next_line,
                        'raw_lines': [line, next_line]
                    }
                    i += 2
                    
                    # Parse remaining fields until next amount
                    while i < len(lines):
                        field_line = lines[i].strip()
                        
                        # Check if we've hit next record
                        if re.match(r'^\$[\d,]+\.\d{2}$', field_line) and i + 1 < len(lines):
                            if re.match(r'^\d{2}/\d{2}/\d{4}$', lines[i + 1].strip()):
                                break
                        
                        current_record['raw_lines'].append(field_line)
                        
                        # Extract fields
                        if 'invoice_id' not in current_record:
                            # Next line after date is usually customer name or invoice ID
                            if re.match(r'^\d{6,}$', field_line):
                                current_record['invoice_id'] = field_line
                            else:
                                current_record['customer_name'] = field_line
                        elif 'customer_name' not in current_record:
                            current_record['customer_name'] = field_line
                        elif 'status' not in current_record:
                            if field_line in ['Paid', 'Unpaid', 'Overdue', 'Draft', 'Canceled', 'Payment pending', 'Undelivered', 'Not viewed', 'Viewed']:
                                current_record['status'] = field_line if field_line not in ['Not viewed', 'Viewed'] else 'Unpaid'
                                current_record['viewed'] = field_line == 'Viewed'
                        elif 'paid_date' not in current_record and field_line.startswith('On '):
                            current_record['paid_date'] = field_line.replace('On ', '')
                        elif 'due_date' not in current_record and field_line.startswith('Due '):
                            if 'today' in field_line.lower():
                                current_record['due_date'] = datetime.now().strftime('%m/%d/%Y')
                            elif 'in ' in field_line:
                                days = re.search(r'(\d+) days', field_line)
                                if days:
                                    due = datetime.now() + timedelta(days=int(days.group(1)))
                                    current_record['due_date'] = due.strftime('%m/%d/%Y')
                            else:
                                current_record['due_date'] = field_line.replace('Due ', '')
                        elif 'days_overdue' not in current_record and 'By' in field_line:
                            days = re.search(r'(\d+) days', field_line)
                            if days:
                                current_record['days_overdue'] = int(days.group(1))
                                current_record['status'] = 'Overdue'
                        elif 'notes' not in current_record and len(field_line) > 10:
                            current_record['notes'] = field_line
                        
                        i += 1
                    
                    # Validate and save record
                    if 'invoice_id' in current_record and 'customer_name' in current_record:
                        records.append(current_record)
                        logger.debug(f"Parsed: {current_record['invoice_id']} - {current_record['customer_name']}")
                    
                    continue
            
            i += 1
        
        return records
    
    def get_summary(self):
        """Get collections summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT status, COUNT(*), SUM(amount) FROM invoices GROUP BY status")
        summary = cursor.fetchall()
        
        cursor.execute("SELECT * FROM invoices WHERE status IN ('Overdue', 'Unpaid') ORDER BY amount DESC LIMIT 10")
        priority = cursor.fetchall()
        
        conn.close()
        return summary, priority
    
    def export_to_json(self, filepath):
        """Export database to JSON for backup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM invoices ORDER BY last_updated DESC")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        data = [dict(zip(columns, row)) for row in rows]
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        conn.close()
        logger.info(f"Exported {len(data)} records to {filepath}")


def main():
    db = CollectionsDB()
    
    print("Collections Database Manager v1.0")
    print("=" * 40)
    print(f"Database: {DB_PATH}")
    print()
    
    # Show current summary
    summary, priority = db.get_summary()
    print("Current Summary:")
    for status, count, total in summary:
        print(f"  {status}: {count} invoices, ${total:,.2f}")
    print()
    
    print("Top 10 Priority Collections:")
    for row in priority:
        print(f"  {row[1]}: ${row[3]:,.2f} - {row[4]} ({row[2]})")


if __name__ == "__main__":
    main()
