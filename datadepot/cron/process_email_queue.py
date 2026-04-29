#!/usr/bin/env python3
"""
DataDepot Email Queue Processor
Processes scheduled emails from queue and sends via Mailgun API
Triggered by cron: 0 * * * * (every hour)
"""

import json
import os
import sys
import time
from datetime import datetime

# Add services to path
sys.path.insert(0, '/root/.openclaw/workspace/datadepot/services')

# Configuration
QUEUE_FILE = '/root/.openclaw/workspace/datadepot/queue/pending_emails.json'
SENT_FILE = '/root/.openclaw/workspace/datadepot/queue/sent_emails.json'
FAILED_FILE = '/root/.openclaw/workspace/datadepot/queue/failed_emails.json'
LOG_FILE = '/var/log/datadepot/emails.log'

# Mailgun settings (load from environment)
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', '')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN', 'psdepot.com')
TEST_MODE = os.getenv('MAILGUN_TEST_MODE', 'True').lower() == 'true'

class EmailQueueProcessor:
    def __init__(self):
        self.stats = {
            'processed': 0,
            'sent': 0,
            'failed': 0,
            'skipped': 0
        }
        
    def log(self, message, level='INFO'):
        """Write to log file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        print(log_entry.strip())
        
        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
    
    def load_queue(self):
        """Load pending emails from queue"""
        if not os.path.exists(QUEUE_FILE):
            return []
        
        try:
            with open(QUEUE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.log("Queue file is empty or corrupted", 'ERROR')
            return []
    
    def save_queue(self, queue):
        """Save remaining emails to queue"""
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue, f, indent=2)
    
    def save_sent(self, email_record):
        """Add to sent emails log"""
        sent_list = []
        if os.path.exists(SENT_FILE):
            with open(SENT_FILE, 'r') as f:
                sent_list = json.load(f)
        
        sent_list.append(email_record)
        
        with open(SENT_FILE, 'w') as f:
            json.dump(sent_list, f, indent=2)
    
    def save_failed(self, email_record, error):
        """Add to failed emails log"""
        failed_list = []
        if os.path.exists(FAILED_FILE):
            with open(FAILED_FILE, 'r') as f:
                failed_list = json.load(f)
        
        email_record['error'] = str(error)
        email_record['failed_at'] = datetime.now().isoformat()
        
        failed_list.append(email_record)
        
        with open(FAILED_FILE, 'w') as f:
            json.dump(failed_list, f, indent=2)
    
    def is_ready_to_send(self, email):
        """Check if scheduled time has been reached"""
        scheduled_time = datetime.fromisoformat(email.get('scheduled_time', '2099-01-01'))
        return datetime.now() >= scheduled_time
    
    def send_email(self, email):
        """
        Send email via Mailgun API
        In TEST_MODE, logs what would be sent without actually sending
        """
        if TEST_MODE:
            self.log(f"[TEST MODE] Would send to: {email['to_email']} | Template: {email['template']} | Campaign: {email.get('campaign_id', 'unknown')}")
            time.sleep(0.1)  # Simulate API call delay
            return {'success': True, 'test_mode': True, 'id': f'test_{int(time.time())}'}
        
        # Real Mailgun API call (implement when ready)
        try:
            import requests
            
            api_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
            
            data = {
                'from': email.get('from', 'Miles - Performance Supply Depot <miles@psdepot.com>'),
                'to': f"{email['to_name']} <{email['to_email']}>",
                'bcc': 'info@psdepot.com',  # BCC info@psdepot.com on all emails
                'subject': email.get('subject', 'DataDepot Intelligence - California Restaurant POS Data'),
                'html': email.get('html_body', ''),
                'o:tracking': 'yes',
                'o:tracking-clicks': 'yes',
                'v:campaign_id': email.get('campaign_id', 'default'),
                'v:template': email.get('template', 'unknown'),
            }
            
            response = requests.post(
                api_url,
                auth=('api', MAILGUN_API_KEY),
                data=data,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            return {
                'success': True,
                'id': result.get('id'),
                'message': result.get('message')
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def process_queue(self):
        """Main processing loop"""
        self.log("=" * 60)
        self.log("EMAIL QUEUE PROCESSOR STARTING")
        self.log("=" * 60)
        
        # Check if Mailgun is configured
        if not TEST_MODE and not MAILGUN_API_KEY:
            self.log("MAILGUN_API_KEY not set. Running in TEST_MODE.", 'WARNING')
            TEST_MODE = True
        
        # Load queue
        queue = self.load_queue()
        
        if not queue:
            self.log("No emails in queue")
            return
        
        self.log(f"Loaded {len(queue)} emails from queue")
        
        # Filter ready to send
        ready_emails = [e for e in queue if self.is_ready_to_send(e)]
        future_emails = [e for e in queue if not self.is_ready_to_send(e)]
        
        self.log(f"{len(ready_emails)} emails ready to send")
        self.log(f"{len(future_emails)} emails scheduled for later")
        
        # Process ready emails
        sent_emails = []
        failed_emails = []
        
        for idx, email in enumerate(ready_emails, 1):
            self.log(f"Processing {idx}/{len(ready_emails)}: {email['to_email']}")
            
            # Send email
            result = self.send_email(email)
            
            if result['success']:
                self.stats['sent'] += 1
                
                # Record sent
                email['sent_at'] = datetime.now().isoformat()
                email['mailgun_id'] = result.get('id', 'unknown')
                email['test_mode'] = result.get('test_mode', False)
                
                self.save_sent(email)
                sent_emails.append(email)
                
                self.log(f"✓ Sent: {email['to_email']}")
                
            else:
                self.stats['failed'] += 1
                
                # Record failed
                self.save_failed(email, result.get('error', 'Unknown error'))
                failed_emails.append(email)
                
                self.log(f"✗ Failed: {email['to_email']} - {result.get('error')}", 'ERROR')
            
            # Throttle to avoid rate limits
            if idx < len(ready_emails):
                time.sleep(1.0)  # 1 second between sends
        
        # Update queue with remaining emails
        self.save_queue(future_emails)
        
        # Summary
        self.log("")
        self.log("=" * 60)
        self.log("PROCESSING COMPLETE")
        self.log("=" * 60)
        self.log(f"Total processed: {len(ready_emails)}")
        self.log(f"Successfully sent: {self.stats['sent']}")
        self.log(f"Failed: {self.stats['failed']}")
        self.log(f"Remaining in queue: {len(future_emails)}")
        self.log("=" * 60)
        
        # Write stats file for dashboard
        stats_file = f"/root/.openclaw/workspace/datadepot/cron/stats_{datetime.now().strftime('%Y%m%d_%H')}.json"
        with open(stats_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'stats': self.stats,
                'queue_size': len(future_emails),
                'sent_count': len(sent_emails),
                'failed_count': len(failed_emails)
            }, f, indent=2)

def main():
    processor = EmailQueueProcessor()
    processor.process_queue()

if __name__ == '__main__':
    main()
