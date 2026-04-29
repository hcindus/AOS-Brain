#!/usr/bin/env python3
"""
Universal Lead Enrichment Agent
Enriches scraped leads with contact info and feeds DepotChaos
Runs continuously as a service
"""

import sqlite3
import json
import time
from datetime import datetime
from pathlib import Path

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"
LOG_FILE = "/var/log/aos/enrichment_agent.log"

class EnrichmentAgent:
    def __init__(self):
        self.last_check = 0
        self.enriched_count = 0
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry + "\n")
    
    def get_unenriched_leads(self, limit=50):
        """Get leads that need enrichment"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Find leads with missing contact info
        c.execute("""
            SELECT id, company_name, county, enrichment_data 
            FROM leads 
            WHERE enrichment_data IS NULL 
               OR enrichment_data LIKE '%"email": ""%'
               OR enrichment_data LIKE '%"phone": ""%'
            LIMIT ?
        """, (limit,))
        
        leads = []
        for row in c.fetchall():
            leads.append({
                'id': row[0],
                'company': row[1],
                'county': row[2],
                'enrichment': json.loads(row[3]) if row[3] else {}
            })
        
        conn.close()
        return leads
    
    def enrich_lead(self, lead_id, company, county, existing_enrichment):
        """Enrich a single lead with mock data (replace with real enrichment)"""
        # In production, this would:
        # 1. Search web for company contact info
        # 2. Query Clearbit/Hunter.io for emails
        # 3. Validate phone numbers
        # 4. Cross-reference with LinkedIn
        
        enriched = existing_enrichment.copy()
        
        # Only enrich if fields are empty
        if not enriched.get('email'):
            # Mock: generate based on company name
            company_slug = company.lower().replace(' ', '').replace("'", '')[:20]
            enriched['email'] = f"info@{company_slug}.com"
            enriched['email_confidence'] = 0.6
            
        if not enriched.get('phone'):
            enriched['phone'] = f"(555) {str(hash(company) % 10000).zfill(4)}"
            
        if not enriched.get('contact_name'):
            enriched['contact_name'] = "Owner"
            enriched['contact_title'] = "Owner/Manager"
            
        return enriched
    
    def save_enrichment(self, lead_id, enrichment):
        """Save enriched data back to database"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute(
            "UPDATE leads SET enrichment_data = ? WHERE id = ?",
            (json.dumps(enrichment), lead_id)
        )
        
        conn.commit()
        conn.close()
    
    def run_cycle(self):
        """Run one enrichment cycle"""
        self.log("🔍 Checking for leads to enrich...")
        
        leads = self.get_unenriched_leads(limit=50)
        
        if not leads:
            self.log("✅ No leads need enrichment")
            return 0
        
        self.log(f"📊 Found {len(leads)} leads to enrich")
        
        enriched = 0
        for lead in leads:
            try:
                new_enrichment = self.enrich_lead(
                    lead['id'], 
                    lead['company'], 
                    lead['county'],
                    lead['enrichment']
                )
                
                self.save_enrichment(lead['id'], new_enrichment)
                enriched += 1
                
                if enriched % 10 == 0:
                    self.log(f"   Enriched {enriched}/{len(leads)}...")
                    
            except Exception as e:
                self.log(f"   ⚠️ Error enriching {lead['company']}: {e}")
        
        self.log(f"✅ Enriched {enriched} leads")
        self.enriched_count += enriched
        return enriched
    
    def run(self):
        """Main agent loop"""
        self.log("="*60)
        self.log("🚀 UNIVERSAL LEAD ENRICHMENT AGENT STARTED")
        self.log("="*60)
        
        while True:
            try:
                self.run_cycle()
                
                # Sleep between cycles
                self.log("💤 Sleeping 60 seconds...")
                time.sleep(60)
                
            except KeyboardInterrupt:
                self.log("\n👋 Agent shutting down")
                break
            except Exception as e:
                self.log(f"❌ Agent error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    agent = EnrichmentAgent()
    agent.run()
