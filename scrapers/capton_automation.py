#!/usr/bin/env python3
"""
Capton Automation Setup
Scheduled follow-up sequences for hospitality leads
"""

import sqlite3
import json
from datetime import datetime, timedelta
import os

DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

def setup_automation():
    """Setup cron job for automated follow-ups"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if email_queue table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='email_queue'")
    if not cursor.fetchone():
        print("Creating email_queue table...")
        cursor.execute("""
            CREATE TABLE email_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                to_email TEXT,
                subject TEXT,
                body TEXT,
                scheduled_at TEXT,
                sent_at TEXT,
                status TEXT DEFAULT 'pending',
                sequence_day INTEGER,
                campaign_id TEXT,
                FOREIGN KEY (lead_id) REFERENCES leads(id)
            )
        """)
        conn.commit()
    
    # Get enriched leads
    cursor.execute("""
        SELECT id, business_name, contact_name, email, business_type
        FROM leads
        WHERE enrichment_status = 'enriched'
        AND (source LIKE '%Casino%' OR source LIKE '%Hotel%')
        AND email IS NOT NULL
    """)
    
    leads = cursor.fetchall()
    
    print(f"Setting up automation for {len(leads)} leads")
    print("=" * 70)
    
    # Campaign setup
    campaign_id = f"capton_hospitality_{datetime.now().strftime('%Y%m')}"
    
    for lead_id, biz, contact, email, biz_type in leads:
        # Skip if already in queue
        cursor.execute("SELECT id FROM email_queue WHERE lead_id = ? LIMIT 1", (lead_id,))
        if cursor.fetchone():
            continue
        
        # Schedule sequence
        base_date = datetime.now()
        
        # Day 1: Initial outreach
        cursor.execute("""
            INSERT INTO email_queue (lead_id, to_email, subject, scheduled_at, sequence_day, campaign_id, status)
            VALUES (?, ?, ?, ?, ?, ?, 'ready')
        """, (lead_id, email, 
              f"Reduce Pour Costs by 30% - {biz}",
              (base_date + timedelta(days=1)).isoformat(),
              1, campaign_id))
        
        # Day 3: Follow-up
        cursor.execute("""
            INSERT INTO email_queue (lead_id, to_email, subject, scheduled_at, sequence_day, campaign_id, status)
            VALUES (?, ?, ?, ?, ?, ?, 'ready')
        """, (lead_id, email,
              f"Quick question about {biz}'s bar inventory",
              (base_date + timedelta(days=3)).isoformat(),
              3, campaign_id))
        
        # Day 7: Final follow-up
        cursor.execute("""
            INSERT INTO email_queue (lead_id, to_email, subject, scheduled_at, sequence_day, campaign_id, status)
            VALUES (?, ?, ?, ?, ?, ?, 'ready')
        """, (lead_id, email,
              f"Final follow-up: Bar efficiency at {biz}",
              (base_date + timedelta(days=7)).isoformat(),
              7, campaign_id))
        
        print(f"✓ Queued 3-email sequence for: {contact} at {biz}")
    
    conn.commit()
    
    # Summary
    cursor.execute("SELECT COUNT(*), sequence_day FROM email_queue WHERE campaign_id = ? GROUP BY sequence_day", (campaign_id,))
    queue_summary = cursor.fetchall()
    
    print("\n" + "=" * 70)
    print(f"AUTOMATION SETUP COMPLETE")
    print("=" * 70)
    print(f"Campaign ID: {campaign_id}")
    print("\nEmails Queued:")
    for count, day in queue_summary:
        print(f"  Day {day}: {count} emails")
    
    total = sum(c for c, _ in queue_summary)
    print(f"\nTotal: {total} emails across {len(leads)} leads")
    
    print("\n" + "=" * 70)
    print("TO ACTIVATE:")
    print("=" * 70)
    print("1. Add SendGrid API key to environment")
    print("2. Run: python3 send_capton_emails.py")
    print("3. Schedule in cron: 0 9 * * * /usr/bin/python3 /path/to/send_capton_emails.py")
    print("=" * 70)
    
    conn.close()

if __name__ == "__main__":
    setup_automation()
