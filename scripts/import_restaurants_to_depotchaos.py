#!/usr/bin/env python3
"""
Import Restaurant Leads into DepotChaos Database
Imports CA and Multi-State restaurant leads into unified CRM
"""

import sqlite3
import csv
import json
from pathlib import Path
from datetime import datetime

# Paths
DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
RESTAURANT_DIR = Path("/root/.openclaw/workspace/AGI_COMPANY/data/restaurants")

class RestaurantImporter:
    def __init__(self):
        self.db_path = Path(DB_PATH)
        self.imported_count = 0
        
    def ensure_schema(self):
        """Ensure customers table exists"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Customers/Contacts table for restaurant leads
        c.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone TEXT,
                company TEXT,
                address TEXT,
                city TEXT,
                county TEXT,
                state TEXT,
                zip TEXT,
                business_type TEXT,
                website TEXT,
                source TEXT,
                priority TEXT,
                tags TEXT,
                notes TEXT,
                import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_contact TIMESTAMP,
                status TEXT DEFAULT 'new',
                assigned_sales_rep TEXT,
                yelp_rating TEXT,
                yelp_reviews TEXT,
                est_revenue TEXT,
                employees TEXT,
                pos_urgency TEXT,
                region TEXT
            )
        ''')
        
        # Create indexes for fast lookups
        c.execute('CREATE INDEX IF NOT EXISTS idx_state ON customers(state)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_city ON customers(city)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_type ON customers(business_type)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_status ON customers(status)')
        
        conn.commit()
        conn.close()
        print("✅ Database schema ready")
    
    def import_ca_enriched(self):
        """Import California enriched restaurant leads"""
        ca_file = RESTAURANT_DIR / "CA_restaurants_enriched_20260428_0340.csv"
        
        if not ca_file.exists():
            print(f"⚠️ CA file not found: {ca_file}")
            return 0
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        count = 0
        with open(ca_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                c.execute('''
                    INSERT OR IGNORE INTO customers 
                    (first_name, last_name, email, phone, company, address, city, county, state, zip,
                     business_type, website, source, priority, tags, notes, status, assigned_sales_rep,
                     yelp_rating, yelp_reviews, est_revenue, employees, pos_urgency, region)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('First Name', ''),
                    row.get('Last Name', ''),
                    row.get('Email', ''),
                    row.get('Phone', ''),
                    row.get('Company', ''),
                    row.get('Address', ''),
                    row.get('City', ''),
                    row.get('County', ''),
                    row.get('State', ''),
                    row.get('Zip', ''),
                    row.get('Business Type', ''),
                    row.get('Website', ''),
                    row.get('Source', ''),
                    row.get('Priority', ''),
                    row.get('Tags', ''),
                    row.get('Notes', ''),
                    'new',  # status
                    '',  # assigned_sales_rep
                    row.get('Yelp Rating', ''),
                    row.get('Yelp Reviews', ''),
                    row.get('Est. Revenue', ''),
                    row.get('Employees', ''),
                    row.get('POS Urgency', ''),
                    row.get('Region', '')
                ))
                count += 1
        
        conn.commit()
        conn.close()
        print(f"✅ Imported {count} CA restaurant leads")
        return count
    
    def import_multi_state(self):
        """Import multi-state restaurant leads"""
        ms_file = RESTAURANT_DIR / "MULTI_STATE_restaurants_20260428_0344.csv"
        
        if not ms_file.exists():
            print(f"⚠️ Multi-state file not found: {ms_file}")
            return 0
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        count = 0
        with open(ms_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                c.execute('''
                    INSERT OR IGNORE INTO customers 
                    (first_name, last_name, email, phone, company, address, city, county, state, zip,
                     business_type, website, source, priority, tags, notes, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('First Name', ''),
                    row.get('Last Name', ''),
                    row.get('Email', ''),
                    row.get('Phone', ''),
                    row.get('Company', ''),
                    row.get('Address', ''),
                    row.get('City', ''),
                    row.get('County', ''),
                    row.get('State', ''),
                    row.get('Zip', ''),
                    row.get('Business Type', ''),
                    row.get('Website', ''),
                    row.get('Source', ''),
                    row.get('Priority', ''),
                    row.get('Tags', ''),
                    row.get('Notes', ''),
                    'new'  # status
                ))
                count += 1
        
        conn.commit()
        conn.close()
        print(f"✅ Imported {count} multi-state restaurant leads")
        return count
    
    def get_stats(self):
        """Get import statistics"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Total customers
        c.execute('SELECT COUNT(*) FROM customers')
        total = c.fetchone()[0]
        
        # By state
        c.execute('SELECT state, COUNT(*) FROM customers GROUP BY state ORDER BY COUNT(*) DESC')
        by_state = c.fetchall()
        
        # By business type
        c.execute('SELECT business_type, COUNT(*) FROM customers GROUP BY business_type ORDER BY COUNT(*) DESC LIMIT 10')
        by_type = c.fetchall()
        
        conn.close()
        
        return {
            'total': total,
            'by_state': by_state,
            'by_type': by_type
        }
    
    def export_summary(self):
        """Export summary for email"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT first_name, last_name, email, phone, company, city, state, 
                   business_type, website, pos_urgency, region
            FROM customers 
            WHERE import_date > date('now', '-1 day')
            ORDER BY state, city
        ''')
        
        leads = c.fetchall()
        conn.close()
        
        return leads

if __name__ == "__main__":
    print("=" * 60)
    print("RESTAURANT LEADS → DEPOTCHAOS IMPORT")
    print("=" * 60)
    print()
    
    importer = RestaurantImporter()
    importer.ensure_schema()
    
    ca_count = importer.import_ca_enriched()
    ms_count = importer.import_multi_state()
    
    stats = importer.get_stats()
    
    print()
    print("=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)
    print(f"📊 Total customers in DepotChaos: {stats['total']}")
    print(f"   • CA leads: {ca_count}")
    print(f"   • Multi-state leads: {ms_count}")
    print()
    print("📍 By State:")
    for state, count in stats['by_state']:
        print(f"   • {state}: {count}")
    print()
    print("🏢 Top Business Types:")
    for btype, count in stats['by_type']:
        print(f"   • {btype}: {count}")
    print()
    print("✅ Ready for sales outreach!")
