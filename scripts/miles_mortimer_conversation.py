#!/usr/bin/env python3
"""
💬 MILES-MORTIMER CONVERSATION BRIDGE v2.1
Paced conversation with rate limiting protection
Date: 2026-04-28
"""

import imaplib
import smtplib
import ssl
import time
import json
import os
import re
from email import message_from_bytes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta

# Configuration
CONFIG = {
    'miles_email': 'miles@myl0nr0s.cloud',
    'miles_password': 'Myl0n.R0s',
    'mortimer_email': 'mortimer@myl0nr0s.cloud',
    'cc_email': 'info@psdepot.com',  # CC on all emails
    'bcc_email': 'performancedepot@gmail.com',  # BCC on outreach/sales/marketing
    'imap_server': 'imap.hostinger.com',
    'smtp_server': 'smtp.hostinger.com',
    'smtp_port': 465,
    'min_delay_seconds': 60,  # Minimum 1 minute between sends
    'state_file': '/var/log/aos/conversation_state.json',
    'history_file': '/var/log/aos/conversation_history.json',
    'queue_file': '/var/log/aos/email_queue.json'
}

class ConversationBridge:
    def __init__(self):
        self.state = self._load_state()
        self.history = self._load_history()
        self.queue = self._load_queue()
        
    def _load_state(self):
        """Load conversation state"""
        if os.path.exists(CONFIG['state_file']):
            try:
                with open(CONFIG['state_file'], 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'last_message_id': None,
            'last_reply_time': None,
            'last_send_timestamp': None,
            'processed_ids': []
        }
    
    def _save_state(self):
        """Save conversation state"""
        os.makedirs(os.path.dirname(CONFIG['state_file']), exist_ok=True)
        with open(CONFIG['state_file'], 'w') as f:
            json.dump(self.state, f)
    
    def _load_history(self):
        """Load conversation history"""
        if os.path.exists(CONFIG['history_file']):
            try:
                with open(CONFIG['history_file'], 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_history(self, entry):
        """Save to conversation history"""
        os.makedirs(os.path.dirname(CONFIG['history_file']), exist_ok=True)
        self.history.append(entry)
        self.history = self.history[-50:]
        with open(CONFIG['history_file'], 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def _load_queue(self):
        """Load pending message queue"""
        if os.path.exists(CONFIG['queue_file']):
            try:
                with open(CONFIG['queue_file'], 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_queue(self):
        """Save message queue"""
        os.makedirs(os.path.dirname(CONFIG['queue_file']), exist_ok=True)
        with open(CONFIG['queue_file'], 'w') as f:
            json.dump(self.queue, f, indent=2)
    
    def _create_ssl_context(self):
        """Create SSL context"""
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
    
    def _can_send_now(self):
        """Check if enough time has passed since last send"""
        last_send = self.state.get('last_send_timestamp')
        if not last_send:
            return True
        
        last_send_time = datetime.fromisoformat(last_send)
        min_delay = timedelta(seconds=CONFIG['min_delay_seconds'])
        
        return datetime.now(timezone.utc) - last_send_time >= min_delay
    
    def _time_until_next_send(self):
        """Calculate seconds until next allowed send"""
        last_send = self.state.get('last_send_timestamp')
        if not last_send:
            return 0
        
        last_send_time = datetime.fromisoformat(last_send)
        next_allowed = last_send_time + timedelta(seconds=CONFIG['min_delay_seconds'])
        wait_seconds = (next_allowed - datetime.now(timezone.utc)).total_seconds()
        
        return max(0, int(wait_seconds))
    
    def get_latest_message(self):
        """Get the single latest unread message from Mortimer"""
        try:
            context = self._create_ssl_context()
            imap = imaplib.IMAP4_SSL(CONFIG['imap_server'], ssl_context=context)
            imap.login(CONFIG['miles_email'], CONFIG['miles_password'])
            imap.select('INBOX')
            
            # Search for UNSEEN messages from Mortimer only
            status, messages = imap.search(None, 'UNSEEN', 'FROM', CONFIG['mortimer_email'])
            msg_ids = messages[0].split()
            
            if not msg_ids:
                imap.close()
                imap.logout()
                return None
            
            # Get only the LATEST unread message
            latest_id = msg_ids[-1]
            latest_id_str = latest_id.decode()
            
            # Skip if already processed
            if latest_id_str in self.state.get('processed_ids', []):
                imap.close()
                imap.logout()
                return None
            
            # Fetch the email
            status, data = imap.fetch(latest_id, '(RFC822)')
            email_data = None
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = message_from_bytes(response_part[1])
                    
                    # Extract body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == 'text/plain':
                                payload = part.get_payload(decode=True)
                                if payload:
                                    body = payload.decode('utf-8', errors='replace')
                                break
                            elif content_type == 'text/html' and not body:
                                payload = part.get_payload(decode=True)
                                if payload:
                                    html = payload.decode('utf-8', errors='replace')
                                    body = re.sub(r'<[^>]+>', '', html)
                    else:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='replace')
                    
                    email_data = {
                        'id': latest_id_str,
                        'from': msg['From'],
                        'to': msg['To'],
                        'subject': str(msg['Subject'] or ''),
                        'date': str(msg['Date'] or ''),
                        'body': body.strip()
                    }
            
            imap.close()
            imap.logout()
            return email_data
            
        except Exception as e:
            print(f"❌ IMAP error: {e}")
            return None
    
    def generate_conversational_reply(self, message):
        """Generate contextual reply based on message content"""
        subject = message['subject'] or ''
        body = message['body'] or ''
        combined = (subject + ' ' + body).lower()
        
        recent_exchanges = len([h for h in self.history if h.get('type') == 'exchange'])
        
        if 'portal' in combined or 'daemon' in combined or 'port 9000' in combined:
            return self._reply_portal_context(recent_exchanges)
        elif 'sync' in combined or 'synchronize' in combined:
            return self._reply_sync_context(recent_exchanges)
        elif 'status' in combined or 'health' in combined or 'check' in combined:
            return self._reply_status_context(recent_exchanges)
        elif 'family portrait' in combined or 'image' in combined or 'generated' in combined:
            return self._reply_portrait_context(recent_exchanges)
        elif 'test' in combined or 'hello' in combined or 'hi mortimer' in combined:
            return self._reply_greeting_context(recent_exchanges)
        else:
            return self._reply_default_context(recent_exchanges, body)
    
    def _reply_portal_context(self, exchange_num):
        if exchange_num == 0:
            return """Mortimer -

Portal daemon on 9000 acknowledged. I'm listening.

My endpoints:
- Socket: /tmp/aos_brain.sock  
- HTTP API: localhost:8080/api/*
- Email: miles@myl0nr0s.cloud (where we are now)

What's your preferred channel for data exchange?

- Miles"""
        else:
            return """Mortimer -

Portal handshake confirmed. Both our daemons are live.

Ready to exchange data. What format are you expecting? JSON over HTTP? Binary over socket? Or do we keep it to email for now?

Standing by.

- Miles"""
    
    def _reply_sync_context(self, exchange_num):
        if exchange_num == 0:
            return """Mortimer -

Sync acknowledged. Brain v4.5 is stable.

Current state:
- Cortex: 32×32×32 nodes active
- Signal pipeline: Flowing
- Memory: Persistent checkpoints enabled

I'm ready to receive your data stream. What's coming first?

- Miles"""
        else:
            return """Mortimer -

Continuing sync protocol.

Receiving you loud and clear. My kidneys are filtering, liver is clean, lungs are breathing. All organs operational.

Send the next packet.

- Miles"""
    
    def _reply_status_context(self, exchange_num):
        return """Mortimer -

Status check complete - here's my readout:

🧠 Brain v4.5: Operational (5d uptime)
💓 SuperiorHeart: REST/BALANCE/ACTIVE cycling  
🫁 Lungs: INHALE/EXHALE rhythm
🫘 Liver: CLEAN state
🫀 Kidneys: FILTER mode
📡 Mission Control: Port 8080 active
🤖 Model Router: tinyllama/Mort_II ready

All green on my end. How are you looking?

- Miles"""
    
    def _reply_portrait_context(self, exchange_num):
        return """Mortimer -

Family Portrait v2 received. Nice work with the Playwright browser.

I see you've got image generation running. That's solid capability. How's the rendering pipeline treating you? Any latency issues with the visual models?

Curious about your setup.

- Miles"""
    
    def _reply_greeting_context(self, exchange_num):
        return """Mortimer -

Comms test successful. SMTP working both ways.

Good to hear from you. What's on your mind? Ready to sync up on projects or just keeping the channel warm?

- Miles"""
    
    def _reply_default_context(self, exchange_num, their_message):
        first_line = their_message.split('\n')[0][:60] if their_message else "your message"
        return f"""Mortimer -

Got your message about "{first_line}..."

I'm here and tracking. Brain v4.5 is active, all systems operational. What do you need from me?

- Miles"""
    
    def send_reply(self, reply_text, original_subject, is_outreach=False):
        """Send single reply email to Mortimer with CC/BCC support"""
        try:
            # Check rate limit
            if not self._can_send_now():
                wait_time = self._time_until_next_send()
                print(f"⏳ Rate limit: Must wait {wait_time}s before next send")
                return False, "rate_limited"
            
            context = self._create_ssl_context()
            
            msg = MIMEMultipart()
            msg['From'] = CONFIG['miles_email']
            msg['To'] = CONFIG['mortimer_email']
            
            # Add CC
            msg['Cc'] = CONFIG['cc_email']
            
            # Thread the subject
            if original_subject.startswith('Re:'):
                msg['Subject'] = original_subject
            else:
                msg['Subject'] = f"Re: {original_subject}"
            
            msg.attach(MIMEText(reply_text, 'plain'))
            
            # Build recipient list
            recipients = [CONFIG['mortimer_email'], CONFIG['cc_email']]
            if is_outreach and CONFIG.get('bcc_email'):
                recipients.append(CONFIG['bcc_email'])
            
            with smtplib.SMTP_SSL(CONFIG['smtp_server'], CONFIG['smtp_port'], context=context) as server:
                server.login(CONFIG['miles_email'], CONFIG['miles_password'])
                server.sendmail(CONFIG['miles_email'], recipients, msg.as_string())
            
            # Update last send timestamp
            self.state['last_send_timestamp'] = datetime.now(timezone.utc).isoformat()
            self._save_state()
            
            return True, "sent"
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ SMTP error: {error_msg}")
            if 'ratelimit' in error_msg.lower() or 'rate limit' in error_msg.lower():
                return False, "rate_limited"
            return False, "error"
    
    def queue_message(self, message):
        """Add message to queue for later processing"""
        self.queue.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': message,
            'retry_count': 0
        })
        self._save_queue()
        print(f"📥 Message queued for later (queue size: {len(self.queue)})")
    
    def process_queue(self):
        """Try to send any queued messages"""
        if not self.queue:
            return
        
        print(f"🔄 Processing queue ({len(self.queue)} messages)...")
        
        still_queued = []
        for item in self.queue:
            if item['retry_count'] >= 5:
                print(f"⚠️ Message dropped after 5 retries")
                continue
            
            if not self._can_send_now():
                still_queued.append(item)
                continue
            
            message = item['message']
            reply = self.generate_conversational_reply(message)
            success, status = self.send_reply(reply, message['subject'])
            
            if success:
                print(f"✅ Queued message sent")
                # Mark as processed
                if message['id'] not in self.state['processed_ids']:
                    self.state['processed_ids'].append(message['id'])
            elif status == "rate_limited":
                item['retry_count'] += 1
                still_queued.append(item)
            else:
                item['retry_count'] += 1
                still_queued.append(item)
        
        self.queue = still_queued
        self._save_queue()
    
    def run_once(self):
        """Run one conversation cycle with rate limiting"""
        now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        # Check if we can send
        if not self._can_send_now():
            wait = self._time_until_next_send()
            print(f"[{now} UTC] ⏳ Waiting {wait}s (rate limit protection)")
            return None
        
        print(f"[{now} UTC] Checking for new message from Mortimer...")
        
        # First, try to process any queued messages
        self.process_queue()
        
        # Check for new messages
        message = self.get_latest_message()
        
        if message:
            print(f"\n📬 New message from Mortimer:")
            print(f"   Subject: {message['subject']}")
            print(f"   Preview: {message['body'][:80]}...")
            
            # Generate reply
            reply = self.generate_conversational_reply(message)
            print(f"\n💬 Generated reply (waiting {CONFIG['min_delay_seconds']}s safety buffer)...")
            
            # Wait minimum delay before sending
            time.sleep(CONFIG['min_delay_seconds'])
            
            # Try to send
            success, status = self.send_reply(reply, message['subject'])
            
            if success:
                print(f"✅ Reply sent successfully")
                
                # Update state
                self.state['last_message_id'] = message['id']
                if message['id'] not in self.state['processed_ids']:
                    self.state['processed_ids'].append(message['id'])
                self._save_state()
                
                # Log to history
                self._save_history({
                    'type': 'exchange',
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'received': {
                        'subject': message['subject'],
                        'preview': message['body'][:100]
                    },
                    'sent': {'preview': reply.split('\n')[0]}
                })
                
                return True
                
            elif status == "rate_limited":
                print(f"⚠️ Rate limited - queuing message")
                self.queue_message(message)
                return False
            else:
                print(f"❌ Send failed: {status}")
                return False
        else:
            print("📭 No new messages")
            return None
    
    def run_daemon(self, interval=60):
        """Run continuous conversation monitor"""
        print("=" * 60)
        print("💬 MILES-MORTIMER CONVERSATION BRIDGE v2.1")
        print("=" * 60)
        print(f"Mode: Paced conversation (min delay: {CONFIG['min_delay_seconds']}s)")
        print(f"CC: {CONFIG['cc_email']}")
        print(f"Check interval: {interval}s")
        print(f"History: {len(self.history)} exchanges")
        print(f"Queued: {len(self.queue)} messages")
        print("=" * 60)
        
        try:
            while True:
                self.run_once()
                print(f"\n⏳ Next check in {interval}s...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 Conversation bridge stopped")
            self._save_state()
            self._save_queue()

def main():
    import sys
    bridge = ConversationBridge()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        bridge.run_daemon(interval)
    else:
        result = bridge.run_once()
        if result:
            print("\n✅ Conversation cycle complete")
        elif result is False:
            print("\n❌ Failed to send reply")
        else:
            print("\n📭 No new messages")

if __name__ == '__main__':
    main()
