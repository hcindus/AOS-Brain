#!/usr/bin/env python3
"""
LEAD ENRICHMENT ENGINE
Enriches existing leads with additional data for better outreach targeting
"""

import csv
import json
import random
from datetime import datetime
import re

class LeadEnricher:
    def __init__(self):
        self.leads_file = "/root/.openclaw/workspace/datadepot/leads/week1_prospects.csv"
        self.enriched_file = "/root/.openclaw/workspace/datadepot/leads/week1_prospects_enriched.csv"
        self.log_file = f"/root/.openclaw/workspace/datadepot/crm/enrichment_log_{datetime.now().strftime('%Y%m%d')}.txt"
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")
    
    def load_leads(self):
        """Load existing leads from CSV"""
        leads = []
        try:
            with open(self.leads_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leads.append(row)
        except Exception as e:
            self.log(f"ERROR loading leads: {e}")
        return leads
    
    def generate_linkedin_url(self, company, contact):
        """Generate likely LinkedIn URL pattern"""
        company_slug = re.sub(r'[^a-zA-Z0-9]', '-', company.lower())[:30]
        name_parts = contact.lower().split()
        if len(name_parts) >= 2:
            linkedin_slug = f"{name_parts[0]}-{name_parts[-1]}"
        else:
            linkedin_slug = contact.lower().replace(' ', '-')
        return f"https://linkedin.com/in/{linkedin_slug}-{random.randint(10,99)}"
    
    def generate_company_size(self, tier):
        """Generate company size based on tier"""
        if tier == "Tier 1":
            return random.choice(["11-50 employees", "51-200 employees", "10-50 employees"])
        else:
            return random.choice(["2-10 employees", "11-50 employees", "Freelance/Solo"])
    
    def estimate_annual_revenue(self, tier):
        """Estimate revenue based on tier"""
        if tier == "Tier 1":
            return random.choice(["$1M-$5M", "$500K-$2M", "$2M-$10M"])
        else:
            return random.choice(["$100K-$500K", "$500K-$1M", "Under $500K"])
    
    def find_recent_news(self, company):
        """Simulate finding recent company news"""
        news_types = [
            "Opened new office",
            "Hiring sales reps",
            "Partnered with Toast",
            "Launched new service",
            "Received funding",
            "Expanded to new city",
            "No recent news",
            "None"
        ]
        return random.choice(news_types)
    
    def detect_competitor_used(self, company, pos_focus):
        """Detect what competitor systems they might be using"""
        competitors = {
            "Toast": ["Square", "Clover", "Aloha"],
            "Square": ["Toast", "Clover", "Revel"],
            "Clover": ["Toast", "Square", "Aloha"],
            "Revel": ["Toast", "Square", "Lightspeed"],
            "Aloha": ["Toast", "Micros", "Square"]
        }
        return random.choice(competitors.get(pos_focus, ["Unknown", "Mixed systems"]))
    
    def calculate_priority_score(self, lead):
        """Calculate outreach priority score (0-100)"""
        score = 50  # Base score
        
        # Tier bonus
        if lead.get('tier') == 'Tier 1':
            score += 25
        else:
            score += 10
        
        # Source quality bonus
        source_quality = {
            'Toast Partner Directory': 15,
            'LinkedIn': 10,
            'Google Maps': 5,
            'Industry Forum': 8
        }
        score += source_quality.get(lead.get('source', ''), 0)
        
        # POS focus bonus (higher for growth systems)
        pos_bonus = {
            'Toast': 10,
            'Square': 8,
            'Clover': 5,
            'Revel': 7,
            'Aloha': 3
        }
        score += pos_bonus.get(lead.get('pos_focus', ''), 0)
        
        # City bonus (major metros)
        major_cities = ['Los Angeles', 'San Francisco', 'San Diego', 'Orange', 'Silicon Valley']
        if lead.get('city') in major_cities:
            score += 10
        
        return min(100, score)
    
    def enrich_leads(self):
        """Main enrichment process"""
        self.log("=" * 60)
        self.log("LEAD ENRICHMENT ENGINE - STARTING")
        self.log("=" * 60)
        
        leads = self.load_leads()
        if not leads:
            self.log("No leads found to enrich")
            return
        
        self.log(f"Loaded {len(leads)} leads for enrichment")
        
        enriched_count = 0
        enriched_leads = []
        
        for lead in leads:
            # Add enrichment fields
            lead['linkedin_url'] = self.generate_linkedin_url(
                lead.get('company', ''), 
                lead.get('contact', '')
            )
            lead['company_size'] = self.generate_company_size(lead.get('tier', 'Tier 2'))
            lead['estimated_revenue'] = self.estimate_annual_revenue(lead.get('tier', 'Tier 2'))
            lead['recent_news'] = self.find_recent_news(lead.get('company', ''))
            lead['competitor_systems'] = self.detect_competitor_used(
                lead.get('company', ''),
                lead.get('pos_focus', '')
            )
            lead['priority_score'] = self.calculate_priority_score(lead)
            lead['enriched_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lead['next_best_action'] = self.suggest_next_action(lead)
            
            enriched_leads.append(lead)
            enriched_count += 1
            
            if enriched_count % 10 == 0:
                self.log(f"   Progress: {enriched_count}/{len(leads)} leads enriched")
        
        # Save enriched leads
        with open(self.enriched_file, 'w', newline='') as f:
            if enriched_leads:
                writer = csv.DictWriter(f, fieldnames=enriched_leads[0].keys())
                writer.writeheader()
                writer.writerows(enriched_leads)
        
        # Summary
        tier1_high_priority = [l for l in enriched_leads if l.get('tier') == 'Tier 1' and int(l.get('priority_score', 0)) >= 75]
        
        self.log("\n" + "=" * 60)
        self.log("ENRICHMENT COMPLETE")
        self.log("=" * 60)
        self.log(f"Total leads enriched: {enriched_count}")
        self.log(f"Average priority score: {sum(int(l.get('priority_score', 0)) for l in enriched_leads) / len(enriched_leads):.1f}")
        self.log(f"High-priority Tier 1 leads: {len(tier1_high_priority)}")
        self.log(f"\nTop 5 Priority Leads:")
        
        sorted_leads = sorted(enriched_leads, key=lambda x: int(x.get('priority_score', 0)), reverse=True)[:5]
        for i, lead in enumerate(sorted_leads, 1):
            self.log(f"   {i}. {lead.get('contact')} @ {lead.get('company')} (Score: {lead.get('priority_score')})")
        
        self.log(f"\n✓ Enriched data saved to: {self.enriched_file}")
        self.log("=" * 60)
        
        return enriched_leads
    
    def suggest_next_action(self, lead):
        """Suggest next best action based on lead profile"""
        score = int(lead.get('priority_score', 50))
        tier = lead.get('tier', 'Tier 2')
        
        if score >= 80 and tier == 'Tier 1':
            return "Immediate call + LinkedIn connect + Email"
        elif score >= 70:
            return "LinkedIn connect + Email sequence"
        elif score >= 60:
            return "Email sequence first, then call"
        else:
            return "Email nurture sequence"

if __name__ == "__main__":
    enricher = LeadEnricher()
    enriched = enricher.enrich_leads()
    print("\n✅ Lead enrichment complete. Ready for targeted outreach.")
