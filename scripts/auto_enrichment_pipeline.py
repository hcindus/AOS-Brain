#!/usr/bin/env python3
"""
Automated Lead Enrichment Pipeline
Runs every 4 hours, processes 100 leads per batch using Yelp API
"""

import sqlite3
import json
import time
import os
import requests
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
LOG_FILE = "/var/log/aos/auto_enrichment.log"
YELP_API_KEY = os.environ.get('YELP_API_KEY', '5DUaC-eBObfSXkjf4YfLNlViO-WqwwCk0UJYewfhav25gbTrCaPvPR_nhokKyfBNKnduMHkqd5Z_v_0RwHSj2fXs8ziaJ-O_RAkuRvc6L6Lt9dwEboKoYHBpBuL1aXYx')
BATCH_SIZE = 100

class AutoEnrichmentPipeline:
    def __init__(self):
        self.enriched_count = 0
        self.not_found = 0
        self.errors = 0
        
    def log(self, message):
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] {message}")
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{ts}] {message}\n")
    
    def get_leads_to_enrich(self) -> list:
        """Get leads needing enrichment"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute("""
            SELECT id, business_name, city, state, county
            FROM leads
            WHERE (phone IS NULL OR phone = '') 
              AND source_type IN ('CA_SOS_Scraper_V3', 'CA_ABC', 'CA_SOS')
              AND created_at > datetime('now', '-7 days')
            ORDER BY RANDOM()
            LIMIT ?
        """, (BATCH_SIZE,))
        
        leads = [dict(row) for row in c.fetchall()]
        conn.close()
        return leads
    
    def search_yelp(self, business_name: str, city: str) -> dict:
        """Search Yelp for business"""
        try:
            headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
            params = {
                'term': business_name,
                'location': f"{city}, CA" if city else "California",
                'limit': 1
            }
            
            response = requests.get(
                'https://api.yelp.com/v3/businesses/search',
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                businesses = data.get('businesses', [])
                if businesses:
                    b = businesses[0]
                    return {
                        'phone': b.get('phone', ''),
                        'rating': b.get('rating', 0),
                        'review_count': b.get('review_count', 0),
                        'address': ', '.join(b.get('location', {}).get('display_address', [])),
                        'yelp_url': b.get('url', '')
                    }
            return None
        except Exception as e:
            self.log(f"⚠️ Yelp error: {e}")
            return None
    
    def update_lead(self, lead_id: int, enrichment: dict):
        """Update lead with enriched data"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("""
            UPDATE leads 
            SET phone = ?, enrichment_data = ?, enriched_at = ?
            WHERE id = ?
        """, (
            enrichment.get('phone', ''),
            json.dumps(enrichment),
            datetime.now(timezone.utc).isoformat(),
            lead_id
        ))
        
        conn.commit()
        conn.close()
    
    def run(self):
        """Main pipeline execution"""
        self.log("="*60)
        self.log("🚀 AUTO ENRICHMENT PIPELINE STARTED")
        self.log("="*60)
        
        leads = self.get_leads_to_enrich()
        
        if not leads:
            self.log("✅ No leads need enrichment")
            return
        
        self.log(f"📊 Processing {len(leads)} leads...")
        
        for i, lead in enumerate(leads, 1):
            try:
                result = self.search_yelp(lead['business_name'], lead['city'])
                
                if result:
                    self.update_lead(lead['id'], result)
                    self.enriched_count += 1
                    self.log(f"✅ [{i}/{len(leads)}] Enriched: {lead['business_name']}")
                else:
                    self.not_found += 1
                    self.log(f"⚠️ [{i}/{len(leads)}] Not found: {lead['business_name']}")
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                self.errors += 1
                self.log(f"❌ [{i}/{len(leads)}] Error on {lead['business_name']}: {e}")
        
        self.log("="*60)
        self.log("✅ PIPELINE COMPLETE")
        self.log(f"   Enriched: {self.enriched_count}")
        self.log(f"   Not found: {self.not_found}")
        self.log(f"   Errors: {self.errors}")

if __name__ == "__main__":
    pipeline = AutoEnrichmentPipeline()
    pipeline.run()
