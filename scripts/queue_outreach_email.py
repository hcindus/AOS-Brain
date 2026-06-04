#!/usr/bin/env python3
"""
📧 QUEUE OUTREACH EMAIL
Agent-ready script for adding emails to DepotChaos queue

Usage:
    # Single email via CLI
    python3 queue_outreach_email.py --recipient "owner@restaurant.com" --subject "POS Supplies" --body "Hello..."
    
    # With lead ID and campaign
    python3 queue_outreach_email.py --recipient "owner@restaurant.com" --subject "POS Supplies" \
        --body "Hello..." --lead-id 5985 --campaign "teriyaki_madness_q2_2026"
    
    # Bulk mode from JSON file
    python3 queue_outreach_email.py --bulk emails.json
    
    # JSON mode via stdin (for piping)
    echo '{"recipient":"test@test.com","subject":"Hi","body":"Hello"}' | python3 queue_outreach_email.py --json

Author: Miles
Version: 1.0.0
"""

import argparse
import json
import sys
import os
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "https://psdepot.com"
QUEUE_FILE = "/root/.openclaw/workspace/datadepot/queue/pending_emails.json"
LOG_FILE = "/var/log/aos/queue_outreach.log"

# Templates
TEMPLATES = {
    'pos_intro': {
        'subject': 'Quick question about your POS supplies',
        'body': """Hi there,

I was just looking at your restaurant and wanted to reach out. I'm Miles with Performance Supply Depot — we help restaurants like yours save on POS supplies and streamline operations.

Quick question: Are you happy with your current POS setup? Most owners I talk to are overpaying on supplies or dealing with outdated systems.

If you're open to a quick conversation, I'd love to show you how we can help. No pressure, just wanted to check in.

Best,
Miles
Performance Supply Depot
miles@myl0nr0s.cloud
"""
    },
    'franchise': {
        'subject': 'Supply savings for {business_name}',
        'body': """Hi {contact_name},

My name is Miles — I work with restaurant franchises across the country on POS supply savings.

I noticed {business_name} and wanted to check in. We work with multi-location operators to:
• Cut POS supply costs by 15-30%
• Streamline ordering across all locations
• Provide dedicated account management

Would a brief call make sense to explore this? Happy to work around your schedule.

Thanks,
Miles
miles@myl0nr0s.cloud
"""
    },
    'ai_voice': {
        'subject': 'AI voice agents for {business_name}?',
        'body': """Hi {contact_name},

Quick question — have you considered AI voice agents for handling calls at {business_name}?

We're seeing restaurants cut phone labor costs by 40% while improving customer response times. The tech has gotten really good.

Worth a 10-minute conversation? No obligation, just want to see if it's a fit.

Miles
Performance Supply Depot
"""
    }
}

def log_action(message):
    """Log action to file"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def add_email_via_api(recipient, subject, body, lead_id=None, campaign=None, 
                     scheduled_time=None, from_name="Miles", from_email="miles@myl0nr0s.cloud"):
    """Add email via API endpoint"""
    try:
        payload = {
            "recipient_email": recipient,
            "subject": subject,
            "body": body,
            "from_name": from_name,
            "from_email": from_email
        }
        if lead_id:
            payload["lead_id"] = lead_id
        if campaign:
            payload["campaign"] = campaign
        if scheduled_time:
            payload["scheduled_time"] = scheduled_time
        
        response = requests.post(
            f"{API_BASE_URL}/api/queue",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            log_action(f"✅ Queued email to {recipient} (ID: {result.get('email_id')}, Position: {result.get('queue_position')})")
            return True, result
        else:
            log_action(f"❌ API error: {response.status_code} - {response.text}")
            return False, {"error": response.text}
            
    except Exception as e:
        log_action(f"❌ API call failed: {e}")
        return False, {"error": str(e)}

def add_email_direct(recipient, subject, body, lead_id=None, campaign=None,
                     scheduled_time=None, from_name="Miles", from_email="miles@myl0nr0s.cloud"):
    """Add email directly to queue file (fallback)"""
    import uuid
    
    try:
        os.makedirs(os.path.dirname(QUEUE_FILE), exist_ok=True)
        
        # Load existing queue
        queue = []
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, 'r') as f:
                queue = json.load(f)
        
        # Create entry
        email_id = str(uuid.uuid4())
        entry = {
            "id": email_id,
            "to_email": recipient,
            "subject": subject,
            "body": body,
            "from_name": from_name,
            "from_email": from_email,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        if lead_id:
            entry["lead_id"] = lead_id
        if campaign:
            entry["campaign_id"] = campaign
        if scheduled_time:
            entry["scheduled_time"] = scheduled_time
        
        queue.append(entry)
        
        # Save
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue, f, indent=2)
        
        log_action(f"✅ Queued email to {recipient} (ID: {email_id}, Position: {len(queue)}) [direct]")
        return True, {"email_id": email_id, "queue_position": len(queue)}
        
    except Exception as e:
        log_action(f"❌ Direct queue failed: {e}")
        return False, {"error": str(e)}

def queue_email(recipient, subject, body, lead_id=None, campaign=None, 
                scheduled_time=None, use_direct=False):
    """Queue an email (tries API first, falls back to direct)"""
    if not use_direct:
        success, result = add_email_via_api(recipient, subject, body, lead_id, campaign, scheduled_time)
        if success:
            return result
    
    # Fallback to direct
    success, result = add_email_direct(recipient, subject, body, lead_id, campaign, scheduled_time)
    return result

def process_bulk_file(filepath, delay_seconds=5):
    """Process bulk emails from JSON file"""
    try:
        with open(filepath, 'r') as f:
            emails = json.load(f)
        
        if not isinstance(emails, list):
            emails = [emails]
        
        log_action(f"📧 Processing {len(emails)} emails from {filepath}")
        
        results = []
        for i, email in enumerate(emails):
            recipient = email.get('recipient_email') or email.get('to_email')
            subject = email.get('subject')
            body = email.get('body')
            lead_id = email.get('lead_id')
            campaign = email.get('campaign') or email.get('campaign_id')
            scheduled_time = email.get('scheduled_time')
            
            if not all([recipient, subject, body]):
                log_action(f"⚠️  Skipping entry {i+1}: missing required fields")
                continue
            
            result = queue_email(recipient, subject, body, lead_id, campaign, scheduled_time)
            results.append(result)
            
            # Rate limiting
            if delay_seconds > 0 and i < len(emails) - 1:
                import time
                time.sleep(delay_seconds)
        
        log_action(f"✅ Bulk processing complete: {len(results)} emails queued")
        return results
        
    except Exception as e:
        log_action(f"❌ Bulk processing failed: {e}")
        return []

def get_teriyaki_leads():
    """Fetch Teriyaki Madness leads from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/leads?search=teriyaki&limit=100", timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get('leads', [])
        return []
    except Exception as e:
        log_action(f"❌ Failed to fetch leads: {e}")
        return []

def generate_teriyaki_emails(count=5):
    """Generate emails for Teriyaki Madness locations"""
    leads = get_teriyaki_leads()
    
    if not leads:
        log_action("❌ No Teriyaki Madness leads found")
        return []
    
    # Take first N leads
    selected = leads[:count]
    
    emails = []
    template = TEMPLATES['franchise']
    
    for lead in selected:
        business_name = lead.get('business_name', 'Teriyaki Madness')
        city = lead.get('city', '')
        state = lead.get('state', '')
        
        # Personalize
        subject = template['subject'].format(business_name=business_name)
        body = template['body'].format(
            contact_name="there",
            business_name=business_name
        )
        
        # Use enrichment email if available
        enrichment = lead.get('enrichment', {})
        recipient = enrichment.get('email') or f"info@{business_name.lower().replace(' ', '').replace('-','')}.com"
        
        email = {
            "recipient_email": recipient,
            "subject": subject,
            "body": body,
            "lead_id": lead.get('id'),
            "campaign": "teriyaki_madness_q2_2026"
        }
        emails.append(email)
    
    return emails

def main():
    parser = argparse.ArgumentParser(description='Queue outreach emails for DepotChaos')
    parser.add_argument('--recipient', help='Recipient email address')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body (or use --template)')
    parser.add_argument('--template', choices=list(TEMPLATES.keys()), help='Use a template')
    parser.add_argument('--lead-id', type=int, help='Associated lead ID')
    parser.add_argument('--campaign', help='Campaign name')
    parser.add_argument('--scheduled-time', help='Scheduled send time (ISO format)')
    parser.add_argument('--bulk', help='Process bulk emails from JSON file')
    parser.add_argument('--json', action='store_true', help='Read email from stdin JSON')
    parser.add_argument('--direct', action='store_true', help='Use direct file write (no API)')
    parser.add_argument('--teriyaki', action='store_true', help='Generate Teriyaki Madness test batch')
    parser.add_argument('--teriyaki-count', type=int, default=5, help='Number of Teriyaki emails to generate')
    parser.add_argument('--delay', type=int, default=1, help='Delay between bulk emails (seconds)')
    
    args = parser.parse_args()
    
    log_action(f"🚀 Queue Outreach Email v1.0 started")
    
    # Handle Teriyaki Madness test batch
    if args.teriyaki:
        log_action(f"🍜 Generating Teriyaki Madness batch ({args.teriyaki_count} emails)...")
        emails = generate_teriyaki_emails(args.teriyaki_count)
        
        if not emails:
            print("❌ Failed to generate emails")
            sys.exit(1)
        
        # Save to temp file for bulk processing
        temp_file = "/tmp/teriyaki_emails.json"
        with open(temp_file, 'w') as f:
            json.dump(emails, f, indent=2)
        
        results = process_bulk_file(temp_file, args.delay)
        print(f"\n✅ Queued {len(results)} Teriyaki Madness emails")
        return
    
    # Handle bulk file
    if args.bulk:
        results = process_bulk_file(args.bulk, args.delay)
        print(f"\n✅ Queued {len(results)} emails from {args.bulk}")
        return
    
    # Handle JSON from stdin
    if args.json:
        try:
            data = json.load(sys.stdin)
            recipient = data.get('recipient_email') or data.get('to_email')
            subject = data.get('subject')
            body = data.get('body')
            lead_id = data.get('lead_id')
            campaign = data.get('campaign') or data.get('campaign_id')
            scheduled_time = data.get('scheduled_time')
            
            if not all([recipient, subject, body]):
                print("❌ Missing required fields: recipient_email, subject, body")
                sys.exit(1)
            
            result = queue_email(recipient, subject, body, lead_id, campaign, 
                                scheduled_time, use_direct=args.direct)
            print(json.dumps(result, indent=2))
            return
            
        except Exception as e:
            print(f"❌ JSON parsing error: {e}")
            sys.exit(1)
    
    # Handle single email via CLI
    if args.recipient and args.subject:
        body = args.body
        if args.template and not body:
            body = TEMPLATES[args.template]['body']
        
        if not body:
            print("❌ Must provide --body or --template")
            sys.exit(1)
        
        result = queue_email(args.recipient, args.subject, body, args.lead_id, 
                            args.campaign, args.scheduled_time, use_direct=args.direct)
        print(json.dumps(result, indent=2))
        return
    
    # No valid mode selected
    parser.print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
