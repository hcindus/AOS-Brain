#!/usr/bin/env python3
"""
📧 IMAP Email Fetcher - Mortimer
Fetch unread emails from mortimer@myl0nr0s.cloud
"""

import imaplib
import ssl
import email
from email.header import decode_header
from datetime import datetime

EMAIL_CONFIG = {
    'address': 'mortimer@myl0nr0s.cloud',
    'password': 'Myl0n.r0s',
    'server': 'imap.hostinger.com'
}

def decode_header_value(header_value):
    """Decode email header value"""
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

def fetch_unread_emails():
    """Fetch unread emails from Mortimer's inbox"""
    
    print("=" * 60)
    print("📧 FETCHING UNREAD EMAILS - Mortimer")
    print("=" * 60)
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    imap = imaplib.IMAP4_SSL(EMAIL_CONFIG['server'], ssl_context=context)
    imap.login(EMAIL_CONFIG['address'], EMAIL_CONFIG['password'])
    imap.select('INBOX')
    
    # Search for unread messages
    status, messages = imap.search(None, 'UNSEEN')
    
    if status != 'OK' or not messages[0]:
        print("No unread messages found.")
        imap.close()
        imap.logout()
        return
    
    msg_ids = messages[0].split()
    print(f"Found {len(msg_ids)} unread message(s)\n")
    
    for msg_id in msg_ids:
        status, msg_data = imap.fetch(msg_id, '(RFC822)')
        
        if status != 'OK':
            continue
            
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        
        # Extract headers
        subject = decode_header_value(email_message['Subject'])
        from_addr = decode_header_value(email_message['From'])
        date = email_message['Date']
        
        print(f"From: {from_addr}")
        print(f"Subject: {subject}")
        print(f"Date: {date}")
        print("-" * 60)
        
        # Try to get body
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                        break
                    except:
                        pass
        else:
            try:
                body = email_message.get_payload(decode=True).decode('utf-8', errors='replace')
            except:
                pass
        
        # Show preview of body (first 500 chars)
        if body:
            preview = body[:500].replace('\n', ' ').replace('\r', '')
            print(f"Preview: {preview}...")
        
        print("=" * 60)
    
    imap.close()
    imap.logout()

if __name__ == '__main__':
    fetch_unread_emails()
