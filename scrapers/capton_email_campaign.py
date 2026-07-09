#!/usr/bin/env python3
"""
Capton Email Campaign Manager
Creates and sends personalized emails to hospitality leads
"""

import sqlite3
import json
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# Email Templates
EMAIL_TEMPLATES = {
    "day_1": {
        "subject": "Reduce Pour Costs by 30% - {business_name}",
        "body": """Hi {contact_name},

I'm reaching out because {business_name} is known for exceptional hospitality, and I noticed an opportunity to significantly improve your bar operations.

Capton helps properties like yours:
✓ Reduce pour variance by up to 30%
✓ Eliminate over-pouring and waste
✓ Track every pour in real-time
✓ Increase guest satisfaction

Our liquor pour spouts with built-in measurement technology integrate seamlessly with your existing POS system.

Would you be open to a brief 10-minute call to discuss how {business_name} could benefit?

Best regards,
Miles
Performance Supply Depot
miles@psdepot.com
https://captoninc.com

---
P.S. I can share case studies from similar {business_type} properties that saw ROI within 60 days.
"""
    },
    "day_3": {
        "subject": "Quick question about {business_name}'s bar inventory", 
        "body": """Hi {contact_name},

I hope this finds you well. I wanted to follow up on my email from Monday about Capton's pour control system.

Quick question: How does {business_name} currently track liquor inventory and pour variance?

Most properties I speak with either:
• Rely on periodic manual counts (time-consuming, inaccurate)
• Use basic POS data (misses over-pouring)
• Have no systematic tracking (leaving money on the table)

Capton provides real-time data on every single pour - no more guesswork.

Would a brief 10-minute call make sense to explore this for {business_name}?

Best,
Miles
Performance Supply Depot

P.S. Our system typically pays for itself in under 90 days through reduced waste alone.
"""
    },
    "day_7": {
        "subject": "Final follow-up: Bar efficiency at {business_name}",
        "body": """Hi {contact_name},

I haven't heard back, so I assume timing isn't right or this isn't a priority for {business_name} right now.

I'll stop reaching out after this email, but I wanted to leave you with one thought:

Properties using Capton typically save $15,000-$50,000 annually on liquor costs alone - not counting increased customer satisfaction from consistent pours.

If that sounds interesting for {business_name}, just reply "INFO" and I'll send details.

If not, no worries - I'll remove you from my outreach list.

Either way, I wish you continued success.

Best regards,
Miles
Performance Supply Depot
miles@psdepot.com
https://captoninc.com
"""
    }
}

class CaptonCampaign:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
    def get_enriched_hospitality_leads(self):
        """Get leads with enrichment data"""
        self.cursor.execute("""
            SELECT id, business_name, contact_name, contact_title, email, 
                   business_type, city, enrichment_data
            FROM leads
            WHERE enrichment_status = 'enriched'
            AND (source LIKE '%Casino%' OR source LIKE '%Hotel%')
            AND (email_sent IS NULL OR email_sent = 0)
            LIMIT 10
        """)
        return self.cursor.fetchall()
    
    def personalize_email(self, template: str, lead: dict) -> dict:
        """Personalize email template for lead"""
        subject = EMAIL_TEMPLATES[template]["subject"].format(
            business_name=lead['business_name'],
            contact_name=lead['contact_name'].split()[0]
        )
        
        body = EMAIL_TEMPLATES[template]["body"].format(
            contact_name=lead['contact_name'].split()[0],
            business_name=lead['business_name'],
            business_type=lead['business_type']
        )
        
        return {"subject": subject, "body": body}
    
    def queue_emails(self, dry_run=True):
        """Queue emails for sending"""
        leads = self.get_enriched_hospitality_leads()
        
        print(f"Found {len(leads)} enriched hospitality leads")
        print("=" * 70)
        
        queued = 0
        for lead in leads:
            lead_id, business_name, contact_name, title, email, biz_type, city, enrich_data = lead
            
            if not email:
                continue
            
            # Personalize Day 1 email
            email_data = self.personalize_email("day_1", {
                'business_name': business_name,
                'contact_name': contact_name,
                'business_type': biz_type or 'hospitality'
            })
            
            if dry_run:
                print(f"\nWould send to: {contact_name} at {business_name}")
                print(f"Email: {email}")
                print(f"Subject: {email_data['subject']}")
                print("-" * 50)
            else:
                # In production, insert into email queue
                self.cursor.execute("""
                    INSERT INTO email_queue (lead_id, to_email, subject, body, 
                    scheduled_at, sequence_day, campaign_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (lead_id, email, email_data['subject'], email_data['body'],
                      datetime.now().isoformat(), 1, 'capton_hospitality_2024'))
                
                # Mark as queued
                self.cursor.execute("""
                    UPDATE leads SET email_sent = 1 WHERE id = ?
                """, (lead_id,))
            
            queued += 1
        
        if not dry_run:
            self.conn.commit()
        
        print(f"\n{'Would queue' if dry_run else 'Queued'}: {queued} emails")
        return queued
    
    def generate_campaign_report(self):
        """Generate campaign status report"""
        self.cursor.execute("""
            SELECT COUNT(*), enrichment_status 
            FROM leads 
            WHERE source LIKE '%Casino%' OR source LIKE '%Hotel%'
            GROUP BY enrichment_status
        """)
        status_counts = self.cursor.fetchall()
        
        self.cursor.execute("""
            SELECT business_name, contact_name, email, business_type
            FROM leads
            WHERE enrichment_status = 'enriched'
            AND (source LIKE '%Casino%' OR source LIKE '%Hotel%')
            LIMIT 5
        """)
        sample_leads = self.cursor.fetchall()
        
        print("\n" + "=" * 70)
        print("CAPTON HOSPITALITY CAMPAIGN STATUS")
        print("=" * 70)
        print("\nLead Status:")
        for count, status in status_counts:
            print(f"  {status or 'pending'}: {count}")
        
        print("\nSample Enriched Leads:")
        for biz, contact, email, biz_type in sample_leads:
            print(f"  {biz} - {contact} ({email}) [{biz_type}]")
    
    def close(self):
        self.conn.close()

def main():
    campaign = CaptonCampaign()
    
    print("CAPTON EMAIL CAMPAIGN MANAGER")
    print("=" * 70)
    print("\n1. Campaign Report")
    campaign.generate_campaign_report()
    
    print("\n" + "=" * 70)
    print("\n2. Email Preview (Dry Run)")
    campaign.queue_emails(dry_run=True)
    
    # Uncomment to actually queue:
    # print("\n" + "=" * 70)
    # print("\n3. Queue Emails for Sending")
    # response = input("Queue emails for real sending? (yes/no): ")
    # if response.lower() == 'yes':
    #     campaign.queue_emails(dry_run=False)
    
    campaign.close()

if __name__ == "__main__":
    main()
