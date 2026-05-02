#!/usr/bin/env python3
"""
Daily Lead Scraper - Performance Supply Depot
Runs daily to scrape new leads and import to DepotChaos
"""

import sqlite3
import csv
import json
import time
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
LOG_FILE = "/var/log/aos/daily_lead_scraper.log"
RAW_DATA_DIR = "/root/.openclaw/workspace/datadepot/data/raw"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + "\n")

def load_ca_abc_data():
    """Load CA ABC license data (placeholder for live scraper)"""
    abc_file = "/root/.openclaw/workspace/datadepot/data/ca_abc_licenses_raw.csv"
    businesses = []
    
    try:
        with open(abc_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                businesses.append({
                    'license': row.get('license_number', ''),
                    'name': row.get('business_name', ''),
                    'dba': row.get('dba', ''),
                    'address': row.get('address', ''),
                    'city': row.get('city', ''),
                    'county': row.get('county', ''),
                    'state': row.get('state', 'CA'),
                    'zip': row.get('zip', ''),
                    'license_type': row.get('license_type', ''),
                    'status': row.get('status', ''),
                    'capacity': row.get('capacity', '')
                })
    except Exception as e:
        log(f"ERROR loading ABC data: {e}")
    
    return businesses

def import_to_depotchaos(businesses, source="daily_scraper"):
    """Import businesses to DepotChaos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    for biz in businesses:
        # Check if already exists
        cursor.execute("SELECT id FROM vendors WHERE name = ? AND city = ?", 
                      (biz['name'], biz['city']))
        if cursor.fetchone():
            skipped += 1
            continue
        
        # Insert new vendor
        cursor.execute("""
            INSERT INTO vendors 
            (name, dba_name, address, city, state, zip, vendor_type, status, source_file, imported_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)
        """, (
            biz['name'],
            biz['dba'],
            biz['address'],
            biz['city'],
            biz['state'],
            biz['zip'],
            'restaurant',  # Default type
            'active',
            source,
            f"License: {biz['license']}, Capacity: {biz['capacity']}"
        ))
        imported += 1
    
    conn.commit()
    conn.close()
    
    return imported, skipped

def run_daily_scrape():
    """Main daily scrape function"""
    log("="*60)
    log("🚀 DAILY LEAD SCRAPER STARTED")
    log("="*60)
    
    # Get current count
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vendors")
    before_count = cursor.fetchone()[0]
    conn.close()
    
    log(f"📊 Current vendor count: {before_count}")
    
    # Load ABC data
    log("📋 Loading CA ABC license data...")
    businesses = load_ca_abc_data()
    log(f"   Found {len(businesses)} businesses in ABC dataset")
    
    # Import to DepotChaos
    log("💾 Importing to DepotChaos...")
    imported, skipped = import_to_depotchaos(businesses)
    log(f"   Imported: {imported}")
    log(f"   Skipped (duplicates): {skipped}")
    
    # Get final count
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM vendors")
    after_count = cursor.fetchone()[0]
    conn.close()
    
    log(f"📊 New total: {after_count} (+{after_count - before_count})")
    
    # Summary
    log("="*60)
    log("✅ DAILY SCRAPE COMPLETE")
    log(f"   New leads: {imported}")
    log(f"   Duplicates skipped: {skipped}")
    log("="*60)
    
    return imported

if __name__ == "__main__":
    run_daily_scrape()
