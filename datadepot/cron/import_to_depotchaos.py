#!/usr/bin/env python3
"""
DataDepot Leads Importer for DepotChaos
Imports POS Intelligence prospects into the unified CRM database
"""

import sqlite3
import csv
import json
from pathlib import Path
from datetime import datetime

# Paths
DEPOT_CHAOS_DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
DATADEPOT_DIR = Path("/root/.openclaw/workspace/datadepot")

class DataDepotToDepotChaosImporter:
    """Import DataDepot leads into DepotChaos unified database"""
    
    def __init__(self):
        self.db_path = Path(DEPOT_CHAOS_DB)
        self.stats = {
            'imported': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def ensure_leads_schema(self):
        """Ensure leads table has DataDepot-specific columns"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Check if leads table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leads'")
        table_exists = c.fetchone()
        
        if not table_exists:
            print("Creating leads table with DataDepot schema...")
            c.execute('''
                CREATE TABLE leads (
                    id TEXT PRIMARY KEY,
                    company_name TEXT,
                    county TEXT,
                    entity_number TEXT,
                    sos_url TEXT,
                    status TEXT DEFAULT 'new',
                    assigned_agent TEXT,
                    assigned_dept TEXT,
                    enrichment_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    -- DataDepot-specific columns
                    pos_system TEXT,
                    pos_confidence TEXT,
                    equipment_age TEXT,
                    replacement_score INTEGER,
                    review_sentiment TEXT,
                    pos_mentions INTEGER,
                    tier TEXT,
                    source_type TEXT,
                    campaign_id TEXT,
                    sequence_day INTEGER,
                    email_sent BOOLEAN DEFAULT 0,
                    email_opened BOOLEAN DEFAULT 0,
                    email_clicked BOOLEAN DEFAULT 0,
                    demo_scheduled BOOLEAN DEFAULT 0,
                    converted BOOLEAN DEFAULT 0,
                    tags TEXT
                )
            ''')
            existing_columns = set()  # All columns are new
        else:
            # Get existing columns
            c.execute("PRAGMA table_info(leads)")
            existing_columns = {col[1] for col in c.fetchall()}
        
        # Add DataDepot-specific columns if not present
        datadepot_columns = {
            'pos_system': 'TEXT',
            'pos_confidence': 'TEXT',
            'equipment_age': 'TEXT',
            'replacement_score': 'INTEGER',
            'review_sentiment': 'TEXT',
            'pos_mentions': 'INTEGER',
            'tier': 'TEXT',
            'source_type': 'TEXT',
            'campaign_id': 'TEXT',
            'sequence_day': 'INTEGER',
            'email_sent': 'BOOLEAN DEFAULT 0',
            'email_opened': 'BOOLEAN DEFAULT 0',
            'email_clicked': 'BOOLEAN DEFAULT 0',
            'demo_scheduled': 'BOOLEAN DEFAULT 0',
            'converted': 'BOOLEAN DEFAULT 0'
        }
        
        for col_name, col_type in datadepot_columns.items():
            if col_name not in existing_columns:
                try:
                    c.execute(f"ALTER TABLE leads ADD COLUMN {col_name} {col_type}")
                    print(f"✅ Added column: {col_name}")
                except sqlite3.OperationalError:
                    # Column already exists, skip
                    pass
        
        # Create DataDepot-specific indexes
        c.execute('CREATE INDEX IF NOT EXISTS idx_datadepot_tier ON leads(tier)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_datadepot_score ON leads(replacement_score)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_datadepot_pos ON leads(pos_system)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_datadepot_campaign ON leads(campaign_id)')
        
        conn.commit()
        conn.close()
        print("✅ DepotChaos schema updated for DataDepot")
    
    def import_csv_leads(self, csv_file, source_type='cold_outbound'):
        """Import leads from CSV file"""
        if not csv_file.exists():
            print(f"⚠️ File not found: {csv_file}")
            return 0
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        imported = 0
        skipped = 0
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Check if lead already exists (by email or company)
                    email = row.get('email', '')
                    company = row.get('company', '')
                    
                    if email:
                        c.execute('SELECT id FROM leads WHERE id = ? OR company_name = ?', 
                                (email, company))
                    else:
                        c.execute('SELECT id FROM leads WHERE company_name = ?', (company,))
                    
                    existing = c.fetchone()
                    
                    if existing:
                        # Update existing lead with DataDepot data
                        c.execute('''
                            UPDATE leads SET
                                tier = COALESCE(tier, ?),
                                pos_system = COALESCE(pos_system, ?),
                                source_type = COALESCE(source_type, ?),
                                assigned_dept = COALESCE(assigned_dept, 'datadepot_sales'),
                                tags = COALESCE(tags, ?)
                            WHERE id = ?
                        ''', (
                            row.get('tier', 'Tier 2'),
                            row.get('pos_focus', ''),
                            source_type,
                            'datadepot,pos_intelligence',
                            existing[0]
                        ))
                        skipped += 1
                    else:
                        # Insert new lead
                        lead_id = f"dd_{datetime.now().strftime('%Y%m%d%H%M%S')}_{imported}"
                        
                        c.execute('''
                            INSERT INTO leads 
                            (id, company_name, sos_url, status, assigned_dept, assigned_agent,
                             enrichment_data, county, tier, pos_system, source_type, tags, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            lead_id,
                            company,
                            '',  # sos_url
                            'new',
                            'datadepot_sales',
                            'pulp',  # assigned to Pulp (Head of Sales)
                            json.dumps(row),
                            row.get('city', ''),
                            row.get('tier', 'Tier 2'),
                            row.get('pos_focus', ''),
                            source_type,
                            'datadepot,pos_intelligence,cold_outbound',
                            datetime.now().isoformat()
                        ))
                        imported += 1
                        
                except Exception as e:
                    self.stats['errors'] += 1
                    print(f"⚠️ Error importing {row.get('company', 'unknown')}: {e}")
        
        conn.commit()
        conn.close()
        
        self.stats['imported'] += imported
        self.stats['skipped'] += skipped
        
        print(f"✅ Imported {imported} new leads from {csv_file.name}")
        print(f"   Skipped {skipped} existing leads")
        return imported
    
    def import_week1_prospects(self):
        """Import the 100 week 1 prospects"""
        prospects_file = DATADEPOT_DIR / 'leads' / 'week1_prospects.csv'
        return self.import_csv_leads(prospects_file, source_type='cold_outbound_week1')
    
    def import_crm_pipeline(self):
        """Import CRM pipeline (contacted leads)"""
        # Read pipeline CSV and update lead status
        pipeline_file = DATADEPOT_DIR / 'crm' / 'pipeline.csv'
        
        if not pipeline_file.exists():
            print("⚠️ Pipeline file not found")
            return 0
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        updated = 0
        
        with open(pipeline_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get('Company', '')
                status = row.get('Status', 'new')
                
                # Update lead status
                c.execute('''
                    UPDATE leads SET
                        status = ?,
                        email_sent = CASE WHEN ? = 'Contacted' THEN 1 ELSE email_sent END,
                        assigned_agent = COALESCE(assigned_agent, 'pulp')
                    WHERE company_name = ?
                ''', (status.lower(), status, company))
                
                if c.rowcount > 0:
                    updated += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ Updated {updated} leads from CRM pipeline")
        return updated
    
    def import_abc_data(self):
        """Import CA ABC license data as background intelligence"""
        abc_file = DATADEPOT_DIR / 'data' / 'ca_abc_licenses_raw.csv'
        
        if not abc_file.exists():
            print("⚠️ ABC data file not found")
            return 0
        
        # This creates a separate table for restaurant intelligence
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create DataDepot intelligence table
        c.execute('''
            CREATE TABLE IF NOT EXISTS datadepot_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_number TEXT UNIQUE,
                business_name TEXT,
                dba TEXT,
                address TEXT,
                city TEXT,
                county TEXT,
                state TEXT,
                zip TEXT,
                license_type TEXT,
                status TEXT,
                issue_date TEXT,
                expiration TEXT,
                capacity INTEGER,
                pos_system TEXT,
                pos_confidence REAL,
                replacement_score INTEGER,
                enrichment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        imported = 0
        
        with open(abc_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    c.execute('''
                        INSERT OR IGNORE INTO datadepot_intelligence
                        (license_number, business_name, dba, address, city, county, state, zip,
                         license_type, status, issue_date, expiration, capacity)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('license_number', ''),
                        row.get('business_name', ''),
                        row.get('dba', ''),
                        row.get('address', ''),
                        row.get('city', ''),
                        row.get('county', ''),
                        row.get('state', ''),
                        row.get('zip', ''),
                        row.get('license_type', ''),
                        row.get('status', ''),
                        row.get('issue_date', ''),
                        row.get('expiration', ''),
                        int(row.get('capacity', 0)) if row.get('capacity') else 0
                    ))
                    if c.rowcount > 0:
                        imported += 1
                except Exception as e:
                    pass  # Skip problematic rows
        
        conn.commit()
        conn.close()
        
        print(f"✅ Imported {imported} CA ABC license records as intelligence data")
        return imported
    
    def get_datadepot_stats(self):
        """Get statistics on DataDepot leads in DepotChaos"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Total DataDepot leads
        c.execute("SELECT COUNT(*) FROM leads WHERE tags LIKE '%datadepot%'")
        total = c.fetchone()[0]
        
        # By tier
        c.execute('''
            SELECT tier, COUNT(*) FROM leads 
            WHERE tags LIKE '%datadepot%' 
            GROUP BY tier ORDER BY COUNT(*) DESC
        ''')
        by_tier = c.fetchall()
        
        # By status
        c.execute('''
            SELECT status, COUNT(*) FROM leads 
            WHERE tags LIKE '%datadepot%' 
            GROUP BY status ORDER BY COUNT(*) DESC
        ''')
        by_status = c.fetchall()
        
        # By POS focus
        c.execute('''
            SELECT pos_system, COUNT(*) FROM leads 
            WHERE tags LIKE '%datadepot%' AND pos_system IS NOT NULL
            GROUP BY pos_system ORDER BY COUNT(*) DESC
        ''')
        by_pos = c.fetchall()
        
        # Intelligence data count
        c.execute("SELECT COUNT(*) FROM datadepot_intelligence")
        intelligence_count = c.fetchone()[0]
        
        conn.close()
        
        return {
            'total': total,
            'by_tier': by_tier,
            'by_status': by_status,
            'by_pos': by_pos,
            'intelligence_count': intelligence_count
        }
    
    def sync_to_crm(self):
        """Sync DataDepot leads to unified CRM view"""
        # Ensure datadepot_sales department exists
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create departments table if not exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                head_agent TEXT,
                status TEXT DEFAULT 'active',
                priority INTEGER DEFAULT 5
            )
        ''')
        
        # Create agents table if not exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                department_id TEXT,
                role TEXT,
                level TEXT DEFAULT 'employee',
                status TEXT DEFAULT 'active'
            )
        ''')
        
        c.execute('''
            INSERT OR IGNORE INTO departments 
            (id, name, head_agent, status, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', ('datadepot_sales', 'DataDepot Sales', 'pulp', 'active', 8))
        
        # Ensure Pulp agent is assigned
        c.execute('''
            INSERT OR IGNORE INTO agents 
            (id, name, department_id, role, level, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('pulp', 'Pulp', 'datadepot_sales', 'Head of Sales', 'tier1', 'active'))
        
        conn.commit()
        conn.close()
        
        print("✅ Synced DataDepot to DepotChaos CRM structure")

def main():
    print("=" * 60)
    print("DATADEPOT → DEPOTCHAOS IMPORT")
    print("=" * 60)
    print()
    
    importer = DataDepotToDepotChaosImporter()
    
    # Step 1: Update schema
    print("📋 Step 1: Ensuring DepotChaos schema...")
    importer.ensure_leads_schema()
    print()
    
    # Step 2: Import week 1 prospects
    print("📥 Step 2: Importing Week 1 Prospects...")
    importer.import_week1_prospects()
    print()
    
    # Step 3: Import CRM pipeline updates
    print("🔄 Step 3: Updating from CRM Pipeline...")
    importer.import_crm_pipeline()
    print()
    
    # Step 4: Import ABC intelligence data
    print("📊 Step 4: Importing CA ABC Intelligence...")
    importer.import_abc_data()
    print()
    
    # Step 5: Sync to CRM structure
    print("🔄 Step 5: Syncing to CRM...")
    importer.sync_to_crm()
    print()
    
    # Get final stats
    stats = importer.get_datadepot_stats()
    
    print("=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)
    print(f"📊 DataDepot Leads in DepotChaos: {stats['total']}")
    print()
    print("📈 By Tier:")
    for tier, count in stats['by_tier']:
        print(f"   • {tier}: {count}")
    print()
    print("📊 By Status:")
    for status, count in stats['by_status']:
        print(f"   • {status}: {count}")
    print()
    print("🖥️  By POS System:")
    for pos, count in stats['by_pos']:
        print(f"   • {pos}: {count}")
    print()
    print(f"📚 Intelligence Records: {stats['intelligence_count']}")
    print()
    print("✅ DataDepot fully integrated into DepotChaos!")
    print("=" * 60)

if __name__ == "__main__":
    main()
