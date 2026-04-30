#!/usr/bin/env python3
"""
📧 IMAP Full Email Fetcher
Fetch ALL email details including attachments from miles@myl0nr0s.cloud
"""

import imaplib
import ssl
import email
from email.header import decode_header
from datetime import datetime
import json

EMAIL_CONFIG = {
    'address': 'miles@myl0nr0s.cloud',
    'password': 'Myl0n.R0s',
    'server': 'imap.hostinger.com'
}

def decode_header_value(header_value):
    if header_value is None:
        return ""
    decoded = decode_header(header_value)
    result = ""
    for part, charset in decoded:
        if isinstance(part, bytes):
            try:
                result += part.decode(charset or 'utf-8', errors='replace')
            except:
                result += part.decode('utf-8', errors='replace')
        else:
            result += part
    return result

def get_email_body(msg):
    """Extract email body text"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            
            # Skip attachments
            if "attachment" in content_disposition:
                continue
                
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
                except:
                    pass
            elif content_type == "text/html" and not body:
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            pass
    return body

def has_attachment(msg):
    """Check if email has attachments"""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                return True
            cd = str(part.get("Content-Disposition", ""))
            if "attachment" in cd:
                return True
    return False

def list_recent_emails(days=7):
    """List emails from last N days"""
    
    print("=" * 80)
    print(f"📧 SEARCHING RECENT EMAILS (last {days} days)")
    print("=" * 80)
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    imap = imaplib.IMAP4_SSL(EMAIL_CONFIG['server'], ssl_context=context)
    imap.login(EMAIL_CONFIG['address'], EMAIL_CONFIG['password'])
    imap.select('INBOX')
    
    # Search for emails since date
    from datetime import timedelta
    since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    status, messages = imap.search(None, f'SINCE {since_date}')
    
    if status != 'OK' or not messages[0]:
        print("No recent messages found.")
        imap.close()
        imap.logout()
        return
    
    msg_ids = messages[0].split()
    print(f"Found {len(msg_ids)} message(s)\n")
    
    results = []
    
    for msg_id in msg_ids[-20:]:  # Last 20 emails
        status, msg_data = imap.fetch(msg_id, '(RFC822)')
        
        if status != 'OK':
            continue
            
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        
        subject = decode_header_value(email_message['Subject'])
        from_addr = decode_header_value(email_message['From'])
        date = email_message['Date']
        body = get_email_body(email_message)
        has_attach = has_attachment(email_message)
        
        # Skip test emails and rate limit notifications
        if subject == "Rate limit test" or "Ratelimit" in subject:
            continue
            
        email_info = {
            'id': msg_id.decode(),
            'from': from_addr,
            'subject': subject,
            'date': date,
            'has_attachment': has_attach,
            'body_preview': body[:1000].replace('\n', ' ').replace('\r', '') if body else ""
        }
        results.append(email_info)
        
        print(f"From: {from_addr}")
        print(f"Subject: {subject}")
        print(f"Date: {date}")
        print(f"Attachments: {'YES' if has_attach else 'No'}")
        print(f"Body Preview: {email_info['body_preview'][:300]}...")
        print("-" * 80)
    
    imap.close()
    imap.logout()
    
    # Save results
    output_path = '/root/.openclaw/workspace/miles_recent_emails.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Saved to: {output_path}")
    
    return results

if __name__ == '__main__':
    list_recent_emails(days=14)
