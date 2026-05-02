#!/usr/bin/env python3
"""
Auto-Enrichment Trigger
Runs after lead imports to automatically enrich missing data
"""

import sqlite3
import subprocess
import sys
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN phone IS NULL OR phone = '' THEN 1 END) as missing_phone,
            COUNT(CASE WHEN email IS NULL OR email = '' THEN 1 END) as missing_email
        FROM vendors
    ''')
    
    total, missing_phone, missing_email = cursor.fetchone()
    conn.close()
    
    return total, missing_phone, missing_email

def trigger_enrichment():
    """Trigger enrichment if thresholds met"""
    total, missing_phone, missing_email = get_stats()
    
    print(f"📊 Current DB Stats:")
    print(f"   Total vendors: {total}")
    print(f"   Missing phone: {missing_phone}")
    print(f"   Missing email: {missing_email}")
    
    # Trigger phone enrichment if >100 missing
    if missing_phone > 100:
        print(f"\n🔍 Triggering phone enrichment for {missing_phone} vendors...")
        result = subprocess.run([
            sys.executable, 
            "/root/.openclaw/workspace/DepotChaos/yelp_enrichment.py"
        ], capture_output=True, text=True)
        print(result.stdout)
    
    # Trigger email enrichment if >500 missing
    if missing_email > 500:
        print(f"\n📧 Triggering email enrichment for {missing_email} vendors...")
        result = subprocess.run([
            sys.executable,
            "/root/.openclaw/workspace/scripts/scrapers/email_enrichment.py"
        ], capture_output=True, text=True)
        print(result.stdout)
    
    print("\n✅ Auto-enrichment complete")

if __name__ == "__main__":
    trigger_enrichment()
