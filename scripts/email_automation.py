#!/usr/bin/env python3
"""
📧 EMAIL AUTOMATION SYSTEM v1.0
Handles both incoming (IMAP) and outgoing (SMTP) email for Miles
- Retrieves Captain's directives from miles@myl0nr0s.cloud
- Sends brain waste reports to Captain automatically
- Runs as a continuous service with smart throttling
"""

import imaplib
import smtplib
import ssl
import json
import subprocess
import os
import sys
import time
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.parser import BytesParser
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
EMAIL_CONFIG = {
    'miles': {
        'name': 'Miles',
        'address': 'miles@myl0nr0s.cloud',
        'password': os.getenv('SMTP_PASS', 'Myl0n.R0s'),
        'imap_server': 'imap.hostinger.com',
        'imap_port': 993,
        'smtp_server': 'smtp.hostinger.com',
        'smtp_port': 465
    },
    'mortimer': {
        'name': 'Mortimer',
        'address': 'mortimer@myl0nr0s.cloud',
        'password': os.getenv('MORTIMER_EMAIL_PASS', 'Myl0n.r0s'),
        'imap_server': 'imap.hostinger.com',
        'imap_port': 993,
        'smtp_server': 'smtp.hostinger.com',
        'smtp_port': 465
    }
}

CAPTAIN_EMAIL = os.getenv('CAPTAIN_EMAIL', 'Antonio.hudnall@gmail.com')
LOG_FILE = '/var/log/aos/email_automation.log'
INBOX_DIR = Path('/root/.openclaw/workspace/memory/email_inbox')
ACTION_ITEMS_FILE = Path('/root/.openclaw/workspace/data/email_action_items.json')

# ═══════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════
def log(msg, level='INFO'):
    """Log with timestamp"""
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    # Append to log file
    try:
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except:
        pass

# ═══════════════════════════════════════════════════════════════════
# IMAP - EMAIL RETRIEVAL
# ═══════════════════════════════════════════════════════════════════
def check_imap_inbox(account_key='miles'):
    """Check inbox for new messages from Captain"""
    config = EMAIL_CONFIG[account_key]
    new_messages = []
    
    try:
        log(f"🔍 Checking {config['name']} inbox ({config['address']})...")
        
        # Create SSL context
        context = ssl.create_default_context()
        
        # Connect to IMAP
        with imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'], ssl_context=context) as imap:
            imap.login(config['address'], config['password'])
            imap.select('INBOX')
            
            # Search for unseen messages from Captain
            status, messages = imap.search(None, 'UNSEEN FROM', f'"{CAPTAIN_EMAIL}"')
            
            if status == 'OK' and messages[0]:
                msg_ids = messages[0].split()
                log(f"📨 Found {len(msg_ids)} unread messages from Captain")
                
                for msg_id in msg_ids:
                    # Fetch message
                    status, msg_data = imap.fetch(msg_id, '(RFC822)')
                    if status == 'OK':
                        raw_email = msg_data[0][1]
                        email_parser = BytesParser()
                        email_msg = email_parser.parsebytes(raw_email)
                        
                        # Extract content
                        subject = email_msg.get('Subject', 'No Subject')
                        from_addr = email_msg.get('From', '')
                        date = email_msg.get('Date', '')
                        
                        # Get body
                        body = ""
                        if email_msg.is_multipart():
                            for part in email_msg.walk():
                                if part.get_content_type() == 'text/plain':
                                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                    break
                        else:
                            body = email_msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                        
                        message_data = {
                            'id': msg_id.decode(),
                            'subject': subject,
                            'from': from_addr,
                            'date': date,
                            'body': body[:5000],  # Limit body size
                            'received_at': datetime.now(timezone.utc).isoformat()
                        }
                        new_messages.append(message_data)
                        
                        # Mark as seen
                        imap.store(msg_id, '+FLAGS', '\\Seen')
                        
            imap.close()
            
        return new_messages
        
    except Exception as e:
        log(f"❌ IMAP error: {e}", 'ERROR')
        return []

def process_incoming_emails(messages):
    """Process and categorize incoming emails"""
    if not messages:
        return
    
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    action_items = []
    
    for msg in messages:
        # Save to inbox directory
        filename = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{msg['id']}.json"
        inbox_path = INBOX_DIR / filename
        
        with open(inbox_path, 'w') as f:
            json.dump(msg, f, indent=2)
        
        log(f"💾 Saved email: {msg['subject']}")
        
        # Categorize for action items
        subject_lower = msg['subject'].lower()
        body_lower = msg['body'].lower()
        
        categories = []
        priority = 'normal'
        
        # Detect category
        if any(k in subject_lower + body_lower for k in ['mission', 'task', 'build', 'create', 'deploy']):
            categories.append('mission')
            priority = 'high'
        if any(k in subject_lower + body_lower for k in ['research', 'api', 'key', 'token']):
            categories.append('research')
        if any(k in subject_lower + body_lower for k in ['sales', 'lead', 'prospect', 'customer']):
            categories.append('sales')
        if any(k in subject_lower + body_lower for k in ['technical', 'bug', 'error', 'fix']):
            categories.append('technical')
        if any(k in subject_lower + body_lower for k in ['finance', 'money', 'payment', 'invoice']):
            categories.append('finance')
            
        if not categories:
            categories.append('general')
        
        action_items.append({
            'subject': msg['subject'],
            'categories': categories,
            'priority': priority,
            'received': msg['received_at'],
            'file': str(inbox_path)
        })
    
    # Update action items file
    if action_items:
        existing = []
        if ACTION_ITEMS_FILE.exists():
            try:
                with open(ACTION_ITEMS_FILE) as f:
                    existing = json.load(f)
            except:
                pass
        
        existing.extend(action_items)
        
        ACTION_ITEMS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(ACTION_ITEMS_FILE, 'w') as f:
            json.dump(existing, f, indent=2)
        
        log(f"📝 Added {len(action_items)} action items to queue")

# ═══════════════════════════════════════════════════════════════════
# SMTP - WASTE EMAIL SENDING
# ═══════════════════════════════════════════════════════════════════
def collect_waste_from_kidneys():
    """Pull waste data from the running brain via Mission Control API."""
    import urllib.request
    
    try:
        req = urllib.request.Request("http://localhost:8080/api/brain")
        req.add_header("Accept", "application/json")
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            
            waste_package = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "Miles_Brain_v4.4",
                "kidneys": data.get("kidneys", {}),
                "qmd": data.get("qmd", {}),
                "router": data.get("router", {}),
                "thyroid": data.get("thyroid", {}),
                "consciousness": data.get("consciousness", {}),
                "cortex": data.get("cortex", {}),
                "tracray": data.get("tracray", {}),
                "liver": data.get("liver", {}),
                "signal_quality": data.get("signal_quality_20avg", 0)
            }
            return waste_package
            
    except Exception as e:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e),
            "source": "Miles_Brain_v4.4",
            "status": "collection_failed"
        }

def collect_from_sespool():
    """Collect any queued sespool waste."""
    sespool_dir = Path("/root/.openclaw/workspace/memory/sespool")
    waste_items = []
    
    if sespool_dir.exists():
        for waste_type in ["periodic-waste", "urban-waste", "webster-waste", "thesaurus-waste"]:
            waste_dir = sespool_dir / waste_type
            if waste_dir.exists():
                for waste_file in waste_dir.glob("*.json"):
                    if ".transferred." not in waste_file.name and ".collected." not in waste_file.name:
                        try:
                            with open(waste_file) as f:
                                waste_items.append(json.load(f))
                                # Mark as collected
                                new_name = waste_file.stem + ".collected" + waste_file.suffix
                                waste_file.rename(waste_file.parent / new_name)
                        except Exception as e:
                            pass
    
    return waste_items

def send_waste_email(waste_data, sespool_items=None):
    """Send waste package to Captain via email."""
    config = EMAIL_CONFIG['miles']
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🗑️ Miles Brain Waste Drop — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC"
    msg["From"] = f"Miles Waste System <{config['address']}>"
    msg["To"] = CAPTAIN_EMAIL
    
    msg["Bcc"] = "info@psdepot.com"
    # Plain text summary
    kidneys = waste_data.get("kidneys", {})
    text_body = f"""
BRAIN WASTE REPORT
==================
Timestamp: {waste_data.get('timestamp')}
Source: {waste_data.get('source')}
Signal Quality: {waste_data.get('signal_quality', 'N/A')}

KIDNEYS STATUS:
- Bladder Level: {kidneys.get('bladder_level', 'N/A')} / {kidneys.get('bladder_capacity', 'N/A')}
- Total Processed: {kidneys.get('total_processed', 'N/A')}
- Noise Estimate: {kidneys.get('noise_estimate', 'N/A')}
- Unique Patterns: {kidneys.get('unique_patterns_seen', 'N/A')}
- State: {kidneys.get('state', 'N/A')}

QMD CYCLES: {waste_data.get('qmd', {}).get('total_cycles', 'N/A')}
ROUTER CALLS: {waste_data.get('router', {}).get('stats', {}).get('decision', {}).get('calls', 'N/A')}
THYROID: {waste_data.get('thyroid', {}).get('state', 'N/A')} ({waste_data.get('thyroid', {}).get('secretions_today', 'N/A')} secretions)

Full JSON attached. Feed this to Mortimer's brain.
    """.strip()
    
    msg.attach(MIMEText(text_body, "plain"))
    
    # Attach full waste JSON
    waste_json = json.dumps(waste_data, indent=2)
    attachment = MIMEApplication(waste_json.encode())
    attachment.add_header("Content-Disposition", "attachment", filename="miles_waste.json")
    msg.attach(attachment)
    
    # Attach sespool items if any
    if sespool_items:
        sespool_json = json.dumps({"sespool_batch": sespool_items}, indent=2)
        sespool_attachment = MIMEApplication(sespool_json.encode())
        sespool_attachment.add_header("Content-Disposition", "attachment", filename="sespool_waste.json")
        msg.attach(sespool_attachment)
    
    # Send email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'], context=context) as server:
            server.login(config['address'], config['password'])
            server.send_message(msg)
        
        log(f"✅ Waste emailed to {CAPTAIN_EMAIL}")
        return True
        
    except Exception as e:
        log(f"❌ Email failed: {e}", 'ERROR')
        # Save to retry queue
        retry_dir = Path("/var/log/aos/email_retry")
        retry_dir.mkdir(parents=True, exist_ok=True)
        retry_file = retry_dir / f"waste_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        with open(retry_file, 'w') as f:
            json.dump(waste_data, f)
        log(f"💾 Saved to retry queue: {retry_file}")
        return False

def check_and_send_waste(force=False):
    """Check if waste needs to be sent and send it"""
    log("📊 Collecting waste from kidneys...")
    waste = collect_waste_from_kidneys()
    
    log("🗑️ Checking sespool backlog...")
    sespool = collect_from_sespool()
    log(f"   Found {len(sespool)} sespool items")
    
    # Check if we should send
    kidneys = waste.get("kidneys", {})
    bladder_level = kidneys.get("bladder_level", 0)
    bladder_capacity = kidneys.get("bladder_capacity", 500)
    bladder_pct = (bladder_level / bladder_capacity * 100) if bladder_capacity > 0 else 0
    
    if bladder_pct > 50 or sespool or force:
        log(f"📧 Sending waste email (bladder: {bladder_pct:.1f}%)...")
        success = send_waste_email(waste, sespool if sespool else None)
        return success
    else:
        log(f"🔄 Bladder at {bladder_pct:.1f}% — below threshold, skipping email")
        return False

# ═══════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════
def run_email_cycle():
    """Run one complete email cycle: receive + send"""
    log("=" * 60)
    log("📧 EMAIL AUTOMATION CYCLE")
    log("=" * 60)
    
    # 1. Check for incoming emails
    new_messages = check_imap_inbox('miles')
    if new_messages:
        process_incoming_emails(new_messages)
    
    # 2. Check and send waste
    check_and_send_waste()
    
    log("=" * 60)

def main():
    """Main entry point"""
    # Check if running in daemon mode
    if '--daemon' in sys.argv:
        log("🚀 Email automation daemon starting...")
        while True:
            try:
                run_email_cycle()
            except Exception as e:
                log(f"❌ Cycle error: {e}", 'ERROR')
            
            # Sleep for 5 minutes between cycles
            log("💤 Sleeping 5 minutes...")
            time.sleep(300)
    else:
        # Single run mode
        force = '--force' in sys.argv
        if force:
            log("🔄 Force mode enabled")
        run_email_cycle()
        if force:
            check_and_send_waste(force=True)

if __name__ == "__main__":
    main()
