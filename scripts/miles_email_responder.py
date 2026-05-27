#!/usr/bin/env python3
"""
📧 Miles Email Responder v1.0
Auto-check and respond to Captain's emails
"""

import imaplib
import smtplib
import ssl
import email
import json
import os
import re
from email.header import decode_header
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
CONFIG = {
    'imap_server': 'imap.hostinger.com',
    'smtp_server': 'smtp.hostinger.com',
    'my_email': 'miles@myl0nr0s.cloud',
    'captain_email': 'Antonio.hudnall@gmail.com',
    'workspace': '/root/.openclaw/workspace',
    'log_file': '/var/log/aos/miles_email_responder.log'
}

class MilesEmailResponder:
    def __init__(self):
        self.creds = self.load_credentials()
        self.processed_emails = self.load_processed_emails()
        
    def log(self, message):
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(CONFIG['log_file'], "a") as f:
            f.write(f"{log_entry}\n")
    
    def load_credentials(self):
        """Load email credentials"""
        creds_file = f"{CONFIG['workspace']}/.miles_email_creds"
        if os.path.exists(creds_file):
            with open(creds_file) as f:
                return json.load(f)
        return None
    
    def load_processed_emails(self):
        """Load list of already processed emails"""
        processed_file = f"{CONFIG['workspace']}/.miles_processed_emails"
        if os.path.exists(processed_file):
            with open(processed_file) as f:
                return set(json.load(f))
        return set()
    
    def save_processed_email(self, msg_id):
        """Mark email as processed"""
        self.processed_emails.add(msg_id)
        processed_file = f"{CONFIG['workspace']}/.miles_processed_emails"
        with open(processed_file, 'w') as f:
            json.dump(list(self.processed_emails), f)
    
    def decode_header_value(self, header_value):
        """Decode email header"""
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
    
    def send_response(self, to_email, subject, original_body, is_captain=False):
        """Send email response"""
        try:
            # Create response message
            if is_captain:
                response_body = f"""Hi Captain,

I received your email and I'm on it.

**Original Subject:** {subject}
**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

I'm reviewing your message now and will get back to you shortly with any questions or actions taken.

If this is urgent, I'll prioritize it immediately.

Best,
Miles
Sales Consultant & AOS
Performance Supply Depot LLC
--
This is an automated acknowledgment. I'll follow up with a detailed response shortly.
"""
            else:
                response_body = f"""Hello,

Thank you for your email.

**Subject:** {subject}
**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

I aim to respond to all inquiries within 24 hours. For urgent matters, please mark your email as "URGENT" in the subject line.

Best regards,
Miles
Performance Supply Depot LLC
"""
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(CONFIG['smtp_server'], 465, context=context) as server:
                server.login(CONFIG['my_email'], self.creds['password'])
                
                msg = MIMEText(response_body)
                msg['From'] = CONFIG['my_email']
                msg['To'] = to_email
                msg['Subject'] = f"Re: {subject}" if not subject.startswith("Re:") else subject
                
                server.sendmail(CONFIG['my_email'], [to_email], msg.as_string())
            
            self.log(f"✅ Sent acknowledgment to {to_email}")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to send response: {str(e)}")
            return False
    
    def check_and_respond(self):
        """Main email check and respond function"""
        self.log("📧 Miles checking for new emails...")
        
        if not self.creds:
            self.log("⚠️ Email credentials not configured")
            return
        
        try:
            # Connect to IMAP
            context = ssl.create_default_context()
            imap = imaplib.IMAP4_SSL(CONFIG['imap_server'], ssl_context=context)
            imap.login(CONFIG['my_email'], self.creds['password'])
            imap.select('INBOX')
            
            # Search for all messages (we'll filter by processed status)
            status, messages = imap.search(None, 'UNSEEN')
            
            if status != 'OK' or not messages[0]:
                self.log("📭 No new unread messages")
                imap.close()
                imap.logout()
                return
            
            msg_ids = messages[0].split()
            self.log(f"📨 Found {len(msg_ids)} unread message(s)")
            
            for msg_id in msg_ids:
                status, msg_data = imap.fetch(msg_id, '(RFC822)')
                
                if status != 'OK':
                    continue
                
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                # Extract details
                subject = self.decode_header_value(email_message['Subject'])
                from_addr = self.decode_header_value(email_message['From'])
                msg_id_header = email_message['Message-ID'] or f"generated_{datetime.now().timestamp()}"
                
                # Skip if already processed
                if msg_id_header in self.processed_emails:
                    continue
                
                # Check if from Captain
                is_captain = 'antonio.hudnall' in from_addr.lower() or 'hcindus' in from_addr.lower()
                
                if is_captain:
                    self.log(f"🔴 EMAIL FROM CAPTAIN: {subject}")
                    
                    # Get body
                    body = ""
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            if part.get_content_type() == "text/plain":
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
                    
                    # Save email for processing
                    email_data = {
                        'msg_id': msg_id_header,
                        'from': from_addr,
                        'subject': subject,
                        'body': body[:2000],
                        'received_at': datetime.now().isoformat(),
                        'status': 'pending_response'
                    }
                    
                    # Save to pending directory
                    pending_dir = f"{CONFIG['workspace']}/pending_emails"
                    os.makedirs(pending_dir, exist_ok=True)
                    safe_id = re.sub(r'[^\w]', '_', msg_id_header)[:50]
                    with open(f"{pending_dir}/{safe_id}.json", 'w') as f:
                        json.dump(email_data, f, indent=2)
                    
                    # Send acknowledgment
                    self.send_response(from_addr, subject, body, is_captain=True)
                    
                    # Mark as processed
                    self.save_processed_email(msg_id_header)
                    
                    self.log(f"📧 Saved and acknowledged Captain's email: {subject}")
                    
                else:
                    self.log(f"📨 Email from others: {from_addr} - {subject}")
                    # Optionally send generic acknowledgment
                    # self.send_response(from_addr, subject, "", is_captain=False)
                    self.save_processed_email(msg_id_header)
            
            imap.close()
            imap.logout()
            
            self.log("✅ Email check complete")
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")

def main():
    responder = MilesEmailResponder()
    responder.check_and_respond()

if __name__ == '__main__':
    main()
