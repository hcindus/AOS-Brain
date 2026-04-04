#!/usr/bin/env python3
"""
📧 EMAIL PROCESSOR WITH ATTACHMENTS
Fetches emails, extracts content + attachments, generates summaries
For: Captain's email handoff to Architect
Date: 2026-04-02
"""

import imaplib
import ssl
import email
import os
import json
from datetime import datetime
from email.header import decode_header
from pathlib import Path

# Configuration
EMAIL_CONFIG = {
    'address': 'miles@myl0nr0s.cloud',
    'password': 'Myl0n.R0s',
    'server': 'imap.hostinger.com'
}

OUTPUT_DIR = Path('/root/.openclaw/workspace/data/email_attachments')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def decode_subject(subject):
    """Decode email subject"""
    if subject is None:
        return "(No Subject)"
    decoded, charset = decode_header(subject)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or 'utf-8', errors='ignore')
    return decoded

def get_body(msg):
    """Extract email body text"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                except:
                    pass
            elif content_type == "text/html":
                try:
                    html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    # Simple HTML stripping
                    import re
                    body = re.sub('<[^<]+?>', '', html)
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        except:
            pass
    return body[:5000]  # Limit body size

def extract_attachments(msg, email_id):
    """Extract attachments from email"""
    attachments = []
    
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = part.get("Content-Disposition", "")
            
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    # Clean filename
                    safe_name = "".join(c for c in filename if c.isalnum() or c in '._-')
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    safe_name = f"{email_id}_{timestamp}_{safe_name}"
                    
                    filepath = OUTPUT_DIR / safe_name
                    
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            with open(filepath, 'wb') as f:
                                f.write(payload)
                            attachments.append({
                                'filename': filename,
                                'saved_as': str(filepath),
                                'size': len(payload),
                                'type': part.get_content_type()
                            })
                    except Exception as e:
                        print(f"    ⚠️  Failed to save attachment {filename}: {e}")
    
    return attachments

def process_emails():
    """Fetch and process emails from IMAP"""
    print("=" * 60)
    print("📧 EMAIL PROCESSOR WITH ATTACHMENTS")
    print("=" * 60)
    print(f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Output: {OUTPUT_DIR}")
    print()
    
    try:
        # Connect to IMAP
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        print(f"🔍 Connecting to {EMAIL_CONFIG['server']}...")
        imap = imaplib.IMAP4_SSL(EMAIL_CONFIG['server'], ssl_context=context)
        imap.login(EMAIL_CONFIG['address'], EMAIL_CONFIG['password'])
        imap.select('INBOX')
        
        # Search for all messages
        status, messages = imap.search(None, 'FROM', 'antonio.hudnall@gmail.com')
        
        if status != 'OK' or not messages[0]:
            print("  ❌ No messages found")
            return []
        
        email_ids = messages[0].split()
        print(f"  ✅ Found {len(email_ids)} messages from Captain")
        print()
        
        processed = []
        
        for eid in email_ids[-20:]:  # Last 20 emails
            status, msg_data = imap.fetch(eid, '(RFC822)')
            
            if status != 'OK':
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract info
            subject = decode_subject(msg.get('Subject', ''))
            date = msg.get('Date', '')
            from_addr = msg.get('From', '')
            
            print(f"📧 Processing: {subject[:50]}...")
            
            # Get body and attachments
            body = get_body(msg)
            attachments = extract_attachments(msg, eid.decode())
            
            email_data = {
                'id': eid.decode(),
                'subject': subject,
                'from': from_addr,
                'date': date,
                'body_preview': body[:1000] if body else "(No text body)",
                'body_full': body,
                'attachments': attachments,
                'attachment_count': len(attachments)
            }
            
            processed.append(email_data)
            
            if attachments:
                print(f"    📎 {len(attachments)} attachment(s) saved:")
                for att in attachments:
                    print(f"       • {att['filename']} ({att['size']} bytes)")
            else:
                print(f"    ✉️  No attachments")
        
        imap.close()
        imap.logout()
        
        # Save processed data
        output_file = OUTPUT_DIR / 'processed_emails.json'
        with open(output_file, 'w') as f:
            json.dump(processed, f, indent=2)
        
        print()
        print("=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        print(f"  Emails processed: {len(processed)}")
        print(f"  Total attachments: {sum(e['attachment_count'] for e in processed)}")
        print(f"  Data saved to: {output_file}")
        print(f"  Attachments in: {OUTPUT_DIR}")
        
        return processed
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def list_attachments():
    """List all saved attachments"""
    print("\n📎 SAVED ATTACHMENTS:")
    print("-" * 60)
    
    files = list(OUTPUT_DIR.glob('*'))
    files = [f for f in files if f.is_file() and f.name != 'processed_emails.json']
    
    if not files:
        print("  No attachments found")
        return
    
    # Group by email ID
    by_email = {}
    for f in files:
        parts = f.name.split('_')
        if len(parts) >= 2:
            email_id = parts[0]
            if email_id not in by_email:
                by_email[email_id] = []
            by_email[email_id].append(f)
    
    for email_id, attachments in by_email.items():
        print(f"\n  Email {email_id}:")
        for att in attachments:
            size = att.stat().st_size
            print(f"    • {att.name} ({size:,} bytes)")

if __name__ == '__main__':
    processed = process_emails()
    list_attachments()
