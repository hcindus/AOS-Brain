#!/usr/bin/env python3
"""
Lead Enrichment Worker - Fills missing emails and websites for leads
Uses working_lead_scraper.py for web searches
"""

import os
import sys
import json
import time
import pandas as pd
from datetime import datetime

sys.path.insert(0, '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/tools')
from working_lead_scraper import WorkingLeadScraper

class LeadEnrichmentWorker:
    """Enriches leads with missing contact information"""
    
    def __init__(self):
        self.scraper = WorkingLeadScraper()
        self.leads_dir = '/root/.openclaw/workspace/AGI_COMPANY/subsidiaries/PERFORMANCE_SUPPLY_DEPOT/products/leads'
        self.stats = {
            'processed': 0,
            'enriched': {'email': 0, 'website': 0, 'phone': 0},
            'failed': 0
        }
    
    def enrich_tx_leads(self, batch_size=50):
        """Enrich TX leads CSV"""
        csv_path = os.path.join(self.leads_dir, 'TX_leads_2026-03-29.csv')
        if not os.path.exists(csv_path):
            print(f"[ENRICHER] TX leads not found: {csv_path}")
            return
        
        df = pd.read_csv(csv_path)
        
        # Find leads needing enrichment (empty email or website)
        needs_enrichment = df[
            (df['email'].isna() | (df['email'] == '')) |
            (df['website'].isna() | (df['website'] == ''))
        ].head(batch_size)
        
        print(f"[ENRICHER] Processing {len(needs_enrichment)} TX leads...")
        
        for idx, row in needs_enrichment.iterrows():
            business = row['business_name']
            city = row['city']
            state = row['state']
            
            print(f"  [{idx+1}] {business[:40]}...")
            
            try:
                data = self.scraper.search_and_extract(business, city, state)
                
                # Update if found
                if data.get('email') and (pd.isna(row['email']) or row['email'] == ''):
                    df.at[idx, 'email'] = data['email']
                    self.stats['enriched']['email'] += 1
                
                if data.get('phone') and (pd.isna(row['phone']) or row['phone'] == ''):
                    df.at[idx, 'phone'] = data['phone']
                    self.stats['enriched']['phone'] += 1
                
                # Mark as enriched
                df.at[idx, 'enrichment_status'] = 'enriched'
                self.stats['processed'] += 1
                
                time.sleep(2)  # Rate limit
                
            except Exception as e:
                print(f"      Error: {e}")
                self.stats['failed'] += 1
        
        # Save updated CSV
        df.to_csv(csv_path, index=False)
        print(f"[ENRICHER] Saved {csv_path}")
    
    def enrich_ca_leads(self, batch_size=50):
        """Enrich CA leads JSON"""
        json_path = os.path.join(self.leads_dir, 'CA_leads_2026-03-29_bulk.json')
        if not os.path.exists(json_path):
            print(f"[ENRICHER] CA leads not found: {json_path}")
            return
        
        with open(json_path) as f:
            leads = json.load(f)
        
        # Find leads needing enrichment
        needs_enrichment = [l for l in leads if l.get('enrichment_status') == 'pending'][:batch_size]
        
        print(f"[ENRICHER] Processing {len(needs_enrichment)} CA leads...")
        
        for lead in needs_enrichment:
            business = lead.get('business_name', '')
            city = lead.get('city', '')
            state = lead.get('state', '')
            
            if not business:
                continue
            
            print(f"  {business[:40]}...")
            
            try:
                data = self.scraper.search_and_extract(business, city, state)
                
                if data.get('email') and not lead.get('email'):
                    lead['email'] = data['email']
                    self.stats['enriched']['email'] += 1
                
                if data.get('phone') and not lead.get('phone'):
                    lead['phone'] = data['phone']
                    self.stats['enriched']['phone'] += 1
                
                lead['enrichment_status'] = 'enriched'
                lead['enriched_at'] = datetime.now().isoformat()
                self.stats['processed'] += 1
                
                time.sleep(2)
                
            except Exception as e:
                print(f"      Error: {e}")
                self.stats['failed'] += 1
        
        # Save updated JSON
        with open(json_path, 'w') as f:
            json.dump(leads, f, indent=2)
        print(f"[ENRICHER] Saved {json_path}")
    
    def report(self):
        """Print enrichment report"""
        print("\n" + "="*60)
        print("LEAD ENRICHMENT REPORT")
        print("="*60)
        print(f"Processed: {self.stats['processed']}")
        print(f"  Emails added: {self.stats['enriched']['email']}")
        print(f"  Phones added: {self.stats['enriched']['phone']}")
        print(f"  Websites added: {self.stats['enriched']['website']}")
        print(f"Failed: {self.stats['failed']}")
        print("="*60)

if __name__ == "__main__":
    worker = LeadEnrichmentWorker()
    
    # Process TX leads
    worker.enrich_tx_leads(batch_size=20)
    
    # Process CA leads  
    worker.enrich_ca_leads(batch_size=20)
    
    # Report
    worker.report()
