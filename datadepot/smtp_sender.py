#!/usr/bin/env python3
"""
SMTP EMAIL SENDER - Hostinger Integration
Sends queued emails via Hostinger SMTP
"""

import smtplib
import ssl
import json
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import time

class HostingerEmailSender:
    def __init__(self):
        # Hostinger SMTP configuration
        self.smtp_server = "smtp.hostinger.com"
        self.smtp_port = 587  # TLS
        
        # Credentials from environment or config
        self.username = os.getenv("HOSTINGER_SMTP_USER", "Miles@myl0nr0s.cloud")
        self.password = os.getenv("HOSTINGER_SMTP_PASS", "")
        
        # Paths
        self.queue_dir = Path("/root/.openclaw/workspace/datadepot/queue")
        self.pending_file = self.queue_dir / "pending_emails.json"
        self.sent_file = self.queue_dir / "sent_emails.json"
        self.failed_file = self.queue_dir / "failed_emails.json"
        self.log_file = self.queue_dir / "smtp_log.txt"
        
        # Rate limiting
        self.emails_per_minute = 10  # Hostinger limit: ~200/hour = ~3/min, using 10 for safety
        self.last_send_time = 0
        
    def log(self, message):
        """Log activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")
    
    def load_pending_emails(self):
        """Load emails ready to send"""
        if not self.pending_file.exists():
            return []
        
        try:
            with open(self.pending_file, 'r') as f:
                queue = json.load(f)
            
            # Filter to emails ready to send (scheduled_time <= now)
            now = datetime.now()
            ready = []
            still_pending = []
            
            for email in queue:
                scheduled = datetime.fromisoformat(
                    email['scheduled_time'].replace('Z', '+00:00').replace('+00:00', '')
                )
                if scheduled <= now and not email.get('sent', False):
                    ready.append(email)
                elif not email.get('sent', False):
                    still_pending.append(email)
            
            return ready, still_pending
        except Exception as e:
            self.log(f"ERROR loading queue: {e}")
            return [], []
    
    def create_email_message(self, email_data):
        """Create MIME message from email data"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = email_data['subject']
        msg['From'] = email_data['from']
        msg['To'] = email_data['to_email']
        msg['Reply-To'] = email_data['from']
        
        # Add text version
        text_part = MIMEText(email_data.get('text_body', ''), 'plain')
        msg.attach(text_part)
        
        # Add HTML version
        html_body = email_data.get('html_body', '')
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        return msg
    
    def send_email(self, email_data):
        """Send single email via Hostinger SMTP"""
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_send_time
        min_interval = 60.0 / self.emails_per_minute
        
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            self.log(f"   Rate limiting: sleeping {sleep_time:.1f}s...")
            time.sleep(sleep_time)
        
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                
                msg = self.create_email_message(email_data)
                server.sendmail(
                    email_data['from'],
                    email_data['to_email'],
                    msg.as_string()
                )
            
            self.last_send_time = time.time()
            self.log(f"   ✅ SENT: {email_data['to_email']} - {email_data['subject'][:50]}...")
            return True
            
        except Exception as e:
            self.log(f"   ❌ FAILED: {email_data['to_email']} - {str(e)[:100]}")
            return False
    
    def process_queue(self, limit=None):
        """Process the email queue"""
        self.log("=" * 60)
        self.log("SMTP EMAIL SENDER - STARTING")
        self.log("=" * 60)
        
        if not self.password:
            self.log("⚠️  WARNING: No SMTP password configured")
            self.log("   Set HOSTINGER_SMTP_PASS environment variable")
            self.log("   Continuing in DRY RUN mode (no actual emails sent)")
            dry_run = True
        else:
            dry_run = False
        
        ready_emails, still_pending = self.load_pending_emails()
        
        self.log(f"\n📧 Queue Status:")
        self.log(f"   Ready to send: {len(ready_emails)}")
        self.log(f"   Still pending (future): {len(still_pending)}")
        
        if not ready_emails:
            self.log("\n✅ No emails ready to send")
            return
        
        if limit:
            to_send = ready_emails[:limit]
            self.log(f"\n🚀 Sending {len(to_send)} emails (limited to {limit})")
        else:
            to_send = ready_emails
            self.log(f"\n🚀 Sending {len(to_send)} emails")
        
        sent_emails = []
        failed_emails = []
        
        for i, email in enumerate(to_send, 1):
            self.log(f"\n[{i}/{len(to_send)}] {email['to_name']} <{email['to_email']}>")
            
            if dry_run:
                self.log(f"   🔵 DRY RUN: Would send to {email['to_email']}")
                email['sent'] = True
                email['sent_at'] = datetime.now().isoformat()
                email['dry_run'] = True
                sent_emails.append(email)
            else:
                if self.send_email(email):
                    email['sent'] = True
                    email['sent_at'] = datetime.now().isoformat()
                    sent_emails.append(email)
                else:
                    email['failed'] = True
                    email['failed_at'] = datetime.now().isoformat()
                    failed_emails.append(email)
        
        # Update queue files
        self.update_queue_files(sent_emails, failed_emails, still_pending)
        
        # Summary
        self.log("\n" + "=" * 60)
        self.log("SEND COMPLETE - SUMMARY")
        self.log("=" * 60)
        self.log(f"📤 Sent: {len(sent_emails)}")
        self.log(f"❌ Failed: {len(failed_emails)}")
        self.log(f"⏳ Still pending: {len(still_pending)}")
        
        if dry_run:
            self.log(f"\n⚠️  DRY RUN MODE - No emails actually sent")
            self.log(f"   To enable real sending, set HOSTINGER_SMTP_PASS")
        
        self.log("=" * 60)
        
        return sent_emails, failed_emails
    
    def update_queue_files(self, sent, failed, pending):
        """Update queue files after sending"""
        # Save sent emails
        existing_sent = []
        if self.sent_file.exists():
            try:
                with open(self.sent_file, 'r') as f:
                    existing_sent = json.load(f)
            except:
                pass
        
        all_sent = existing_sent + sent
        with open(self.sent_file, 'w') as f:
            json.dump(all_sent, f, indent=2)
        
        # Save failed emails
        if failed:
            existing_failed = []
            if self.failed_file.exists():
                try:
                    with open(self.failed_file, 'r') as f:
                        existing_failed = json.load(f)
                except:
                    pass
            
            all_failed = existing_failed + failed
            with open(self.failed_file, 'w') as f:
                json.dump(all_failed, f, indent=2)
        
        # Update pending file (remove sent ones)
        with open(self.pending_file, 'w') as f:
            json.dump(pending, f, indent=2)
        
        self.log(f"\n💾 Updated:")
        self.log(f"   Total sent history: {len(all_sent)}")
        self.log(f"   Failed count: {len(all_failed) if failed else 0}")
        self.log(f"   Remaining pending: {len(pending)}")

if __name__ == "__main__":
    sender = HostingerEmailSender()
    
    # Check for password from environment
    import sys
    
    # Accept limit from command line
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    sent, failed = sender.process_queue(limit=limit)
    
    if sent:
        print(f"\n✅ Sent {len(sent)} emails successfully")
    if failed:
        print(f"\n⚠️  {len(failed)} emails failed - check {sender.log_file}")
