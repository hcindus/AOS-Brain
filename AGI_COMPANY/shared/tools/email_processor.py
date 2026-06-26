#!/usr/bin/env python3
"""
📧 EMAIL PROCESSOR
Fetch and process unread emails for Miles and Mortimer
Date: 2026-06-26
"""

import imaplib
import ssl
import email
import sys
import json
from datetime import datetime
from email.header import decode_header

# Email configuration
EMAIL_ACCOUNTS = [
    {
        'name': 'Miles',
        'address': 'miles@myl0nr0s.cloud',
        'password': 'Myl0n.R0s',
        'server': 'imap.hostinger.com'
    },
    {
        'name': 'Mortimer',
        'address': 'mortimer@myl0nr0s.cloud',
        'password': 'Myl0n.r0s',
        'server': 'imap.hostinger.com'
    }
]

def decode_email_header(header_value):
    """Decode email header to readable string"""
    if not header_value:
        return ""
    decoded = decode_header(header_value)
    result = []
    for part, charset in decoded:
        if isinstance(part, bytes):
            result.append(part.decode(charset or 'utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)

def get_email_body(msg):
    """Extract email body from message"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
                except:
                    pass
            elif content_type == "text/html":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')
        except:
            body = str(msg.get_payload())
    return body[:2000] if len(body) > 2000 else body

def process_account(account, max_emails=10):
    """Process unread emails for an account"""
    emails = []
    try:
        print(f"\n🔍 Checking {account['name']} ({account['address']})...")
        
        # Create SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Connect to IMAP server
        imap = imaplib.IMAP4_SSL(account['server'], ssl_context=context)
        imap.login(account['address'], account['password'])
        imap.select('INBOX')
        
        # Search for unseen messages
        status, messages = imap.search(None, 'UNSEEN')
        
        if status != 'OK' or not messages[0]:
            print(f"  ✅ No unread messages")
            imap.close()
            imap.logout()
            return emails
        
        msg_ids = messages[0].split()
        print(f"  📨 {len(msg_ids)} unread message(s)")
        
        # Fetch up to max_emails
        for msg_id in msg_ids[:max_emails]:
            status, msg_data = imap.fetch(msg_id, '(RFC822)')
            
            if status != 'OK':
                continue
                
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = decode_email_header(msg.get('Subject', 'No Subject'))
            sender = decode_email_header(msg.get('From', 'Unknown'))
            date = msg.get('Date', 'Unknown')
            body = get_email_body(msg)
            
            email_data = {
                'account': account['name'],
                'id': msg_id.decode(),
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body[:1000]  # First 1000 chars
            }
            emails.append(email_data)
            
        imap.close()
        imap.logout()
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        
    return emails

def main():
    print("=" * 60)
    print("📧 EMAIL PROCESSOR")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    all_emails = []
    
    for account in EMAIL_ACCOUNTS:
        emails = process_account(account, max_emails=5)
        all_emails.extend(emails)
    
    print("\n" + "=" * 60)
    print("📧 UNREAD EMAILS SUMMARY")
    print("=" * 60)
    
    if not all_emails:
        print("\n✅ No unread emails to process!")
        return 0
    
    for i, email_data in enumerate(all_emails, 1):
        print(f"\n{'─' * 60}")
        print(f"📧 Email #{i} | Account: {email_data['account']}")
        print(f"{'─' * 60}")
        print(f"From: {email_data['sender']}")
        print(f"Subject: {email_data['subject']}")
        print(f"Date: {email_data['date']}")
        print(f"\nBody preview:")
        print(email_data['body'][:500] + "..." if len(email_data['body']) > 500 else email_data['body'])
    
    print(f"\n{'=' * 60}")
    print(f"Total unread emails shown: {len(all_emails)}")
    print("=" * 60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
