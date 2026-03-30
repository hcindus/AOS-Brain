#!/usr/bin/env python3
"""
Daily Email Checker for Miles
Checks miles@myl0nr0s.cloud for new emails
Processes actionable emails from Captain
Routes business intelligence to appropriate teams
"""

import imaplib
import ssl
import email
from email.header import decode_header
import json
import os
from datetime import datetime, timedelta

# Configuration
EMAIL_ACCOUNT = "miles@myl0nr0s.cloud"
EMAIL_PASSWORD = "Myl0n.R0s"  # From vault
IMAP_SERVER = "imap.hostinger.com"
IMAP_PORT = 993

# Captain's email (only actionable source)
CAPTAIN_EMAIL = "antonio.hudnall@gmail.com"

# Teams for routing
TEAMS = {
    "rnd": ["proto@agi-company.ai", "lab@agi-company.ai"],
    "finance": ["ledger-9@agi-company.ai", "alpha-9@agi-company.ai"],
    "technical": ["stacktrace@agi-company.ai", "pipeline@agi-company.ai"],
    "sales": ["pulp@agi-company.ai", "jane@agi-company.ai"],
    "marketing": ["marketing@agi-company.ai"],
}

def log_message(msg):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] {msg}")

def check_emails():
    """Check inbox for new emails"""
    log_message("Starting daily email check...")
    
    try:
        # Connect to IMAP server
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT, ssl_context=context)
        
        # Login
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        log_message(f"✅ Connected to {IMAP_SERVER}")
        
        # Select inbox
        mail.select("inbox")
        
        # Search for unread emails
        status, messages = mail.search(None, "UNSEEN")
        
        if status != "OK":
            log_message("No new messages or error occurred")
            mail.logout()
            return
        
        message_ids = messages[0].split()
        
        if not message_ids:
            log_message("📭 No new emails")
            mail.logout()
            return
        
        log_message(f"📧 Found {len(message_ids)} new email(s)")
        
        actionable_count = 0
        
        for msg_id in message_ids:
            status, msg_data = mail.fetch(msg_id, "(RFC822)")
            
            if status != "OK":
                continue
            
            # Parse email
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Get sender
            from_header = decode_header(msg.get("From"))[0][0]
            if isinstance(from_header, bytes):
                from_email = from_header.decode()
            else:
                from_email = from_header
            
            # Get subject
            subject_header = decode_header(msg.get("Subject"))[0][0]
            if isinstance(subject_header, bytes):
                subject = subject_header.decode()
            else:
                subject = subject_header
            
            # Check if from Captain
            if CAPTAIN_EMAIL in from_email:
                actionable_count += 1
                log_message(f"🎯 ACTIONABLE from Captain: '{subject}'")
                
                # Extract body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            break
                else:
                    try:
                        body = msg.get_payload(decode=True).decode()
                    except:
                        pass
                
                # Analyze and route
                route_email(subject, body)
                
                # Mark as processed (but keep for reference)
                # mail.store(msg_id, '+FLAGS', '\\Seen')
            else:
                log_message(f"📧 Non-actionable from: {from_email}")
        
        log_message(f"✅ Processed {actionable_count} actionable email(s)")
        
        # Close connection
        mail.close()
        mail.logout()
        
    except Exception as e:
        log_message(f"❌ Error checking emails: {e}")

def route_email(subject, body):
    """Analyze email and route to appropriate team"""
    subject_lower = subject.lower()
    body_lower = body.lower()
    
    # Determine which team should handle this
    routes = []
    
    # R&D keywords
    if any(word in subject_lower or word in body_lower for word in 
           ["research", "development", "prototype", "innovation", "experiment", "test", "lab", "r&d"]):
        routes.append("rnd")
        log_message("   → Routed to: R&D Team (PROTO, LAB)")
    
    # Finance keywords
    if any(word in subject_lower or word in body_lower for word in 
           ["budget", "cost", "revenue", "profit", "expense", "pricing", "invoice", "payment", "money"]):
        routes.append("finance")
        log_message("   → Routed to: Finance (LEDGER-9, ALPHA-9)")
    
    # Technical keywords
    if any(word in subject_lower or word in body_lower for word in 
           ["code", "bug", "feature", "api", "database", "server", "deploy", "build", "software", "hardware"]):
        routes.append("technical")
        log_message("   → Routed to: Technical (STACKTRACE, PIPELINE)")
    
    # Sales keywords
    if any(word in subject_lower or word in body_lower for word in 
           ["lead", "prospect", "customer", "sale", "deal", "demo", "pricing", "contract", "order"]):
        routes.append("sales")
        log_message("   → Routed to: Sales (Pulp, Jane)")
    
    # Marketing keywords
    if any(word in subject_lower or word in body_lower for word in 
           ["marketing", "campaign", "ad", "content", "social", "brand", "website", "traffic"]):
        routes.append("marketing")
        log_message("   → Routed to: Marketing")
    
    # Default: Direct to Miles for review
    if not routes:
        log_message("   → Routed to: Miles (requires clarification)")
    
    # Create action item
    action_item = {
        "timestamp": datetime.now().isoformat(),
        "from": CAPTAIN_EMAIL,
        "subject": subject,
        "routes": routes,
        "status": "pending_review",
        "notes": "Awaiting processing"
    }
    
    # Save to action items
    action_file = "/root/.openclaw/workspace/data/email_action_items.json"
    os.makedirs(os.path.dirname(action_file), exist_ok=True)
    
    actions = []
    if os.path.exists(action_file):
        try:
            with open(action_file, 'r') as f:
                actions = json.load(f)
        except:
            pass
    
    actions.append(action_item)
    
    with open(action_file, 'w') as f:
        json.dump(actions, f, indent=2)
    
    log_message(f"   💾 Action item saved: {action_file}")

if __name__ == "__main__":
    check_emails()
    log_message("Email check complete.")
