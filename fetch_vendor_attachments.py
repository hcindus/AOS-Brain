#!/usr/bin/env python3
"""
📧 IMAP Attachment Fetcher
Fetch attachments from vendor list emails
"""

import imaplib
import ssl
import email
from email.header import decode_header
import os

EMAIL_CONFIG = {
    'address': 'miles@myl0nr0s.cloud',
    'password': 'Myl0n.R0s',
    'server': 'imap.hostinger.com'
}

OUTPUT_DIR = '/root/.openclaw/workspace/data/vendor_attachments'

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

def fetch_attachments():
    """Fetch attachments from vendor emails"""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 80)
    print("📧 FETCHING VENDOR ATTACHMENTS")
    print("=" * 80)
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    imap = imaplib.IMAP4_SSL(EMAIL_CONFIG['server'], ssl_context=context)
    imap.login(EMAIL_CONFIG['address'], EMAIL_CONFIG['password'])
    imap.select('INBOX')
    
    # Target email IDs with vendor data
    target_ids = [b'655', b'657', b'659', b'660', b'661']
    
    for msg_id in target_ids:
        print(f"\n📨 Processing message {msg_id.decode()}...")
        
        status, msg_data = imap.fetch(msg_id, '(RFC822)')
        if status != 'OK':
            print(f"  ❌ Failed to fetch message {msg_id}")
            continue
        
        raw_email = msg_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        
        subject = decode_header_value(email_message['Subject'])
        from_addr = decode_header_value(email_message['From'])
        
        print(f"  Subject: {subject}")
        print(f"  From: {from_addr}")
        
        # Extract attachments
        attachment_count = 0
        if email_message.is_multipart():
            for part in email_message.walk():
                content_disposition = str(part.get("Content-Disposition", ""))
                
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        # Clean filename
                        filename = decode_header_value(filename)
                        filename = filename.replace('/', '_').replace('\\', '_')
                        
                        filepath = os.path.join(OUTPUT_DIR, f"msg{msg_id.decode()}_{filename}")
                        
                        # Save attachment
                        payload = part.get_payload(decode=True)
                        if payload:
                            with open(filepath, 'wb') as f:
                                f.write(payload)
                            print(f"  ✅ Saved: {filepath}")
                            attachment_count += 1
        
        if attachment_count == 0:
            print(f"  ℹ️  No attachments found")
        else:
            print(f"  📎 Total attachments: {attachment_count}")
    
    imap.close()
    imap.logout()
    
    print("\n" + "=" * 80)
    print(f"💾 All attachments saved to: {OUTPUT_DIR}")
    print("=" * 80)

if __name__ == '__main__':
    fetch_attachments()
