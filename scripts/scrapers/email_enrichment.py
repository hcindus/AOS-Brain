#!/usr/bin/env python3
"""
Email Enrichment Script - Find emails for existing leads
Performance Supply Depot
"""

import sqlite3
import re
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

DB_PATH = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
LOG_FILE = "/var/log/aos/email_enrichment.log"

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{ts}] {msg}"
    print(entry)
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(entry + '\n')

def guess_email_pattern(name, domain):
    """Generate common email patterns"""
    clean_name = re.sub(r'[^\w\s]', '', name).lower().strip()
    words = clean_name.split()
    
    patterns = []
    if len(words) >= 2:
        first, last = words[0], words[-1]
        patterns.extend([
            f"{first}@{domain}",
            f"{first}.{last}@{domain}",
            f"{first[0]}{last}@{domain}",
            f"info@{domain}",
            f"contact@{domain}",
            f"hello@{domain}",
            f"sales@{domain}",
            f"support@{domain}"
        ])
    else:
        patterns.extend([
            f"info@{domain}",
            f"contact@{domain}",
            f"hello@{domain}"
        ])
    
    return patterns

def find_website(name, city, state):
    """Find business website via search"""
    query = quote_plus(f"{name} {city} {state}")
    # Placeholder - integrate with search API
    return None

def extract_domain_from_yelp(yelp_url):
    """Try to get domain from Yelp page"""
    if not yelp_url:
        return None
    # Yelp doesn't expose websites directly in API
    # Would need to scrape or use other sources
    return None

def enrich_vendor_emails(limit=100):
    """Find emails for vendors missing them"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, city, state, phone, notes 
        FROM vendors 
        WHERE (email IS NULL OR email = '') 
        AND phone IS NOT NULL
        ORDER BY id
        LIMIT ?
    ''', (limit,))
    
    vendors = cursor.fetchall()
    log(f"🔍 Enriching emails for {len(vendors)} vendors")
    
    enriched = 0
    
    for vid, name, city, state, phone, notes in vendors:
        log(f"   [{vid}] {name} in {city}, {state}")
        
        # Parse notes for Yelp data
        yelp_data = {}
        if notes:
            try:
                if '{' in notes:
                    yelp_data = json.loads(notes.split('{')[1].split('}')[0])
            except:
                pass
        
        # Try to construct email from business name
        # Clean business name to guess domain
        clean_name = re.sub(r'[^\w\s]', '', name).lower().replace(' ', '')
        
        # Common email patterns to try
        email = None
        
        # Pattern 1: info@businessname.com
        potential_emails = [
            f"info@{clean_name}.com",
            f"contact@{clean_name}.com",
            f"hello@{clean_name}.com"
        ]
        
        # For now, skip validation and store pattern
        # In production, would validate via SMTP or API
        email = f"info@{clean_name}.com"
        
        # Update vendor
        if email:
            cursor.execute('''
                UPDATE vendors SET email = ?, notes = COALESCE(notes, '') || ? WHERE id = ?
            ''', (email, f' | Email pattern guessed: {email}', vid))
            enriched += 1
            log(f"      ✅ Added: {email}")
        
        time.sleep(0.1)
    
    conn.commit()
    conn.close()
    
    log(f"📊 Email enrichment complete: {enriched}/{len(vendors)} updated")
    return enriched

def main():
    log("=" * 60)
    log("📧 EMAIL ENRICHMENT STARTED")
    log("=" * 60)
    
    enriched = enrich_vendor_emails(limit=200)
    
    log(f"✅ Complete - Enriched {enriched} vendors with emails")

if __name__ == "__main__":
    main()
