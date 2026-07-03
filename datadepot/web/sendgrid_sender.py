#!/usr/bin/env python3
"""
SendGrid Email Sender for DepotChaos
Replaces SMTP with SendGrid API for better deliverability
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SendGridSender:
    """SendGrid email sender with rate limiting and queue management"""
    
    def __init__(self, api_key: Optional[str] = None, from_email: str = "info@psdepot.com", from_name: str = "Miles - Performance Supply Depot"):
        self.api_key = api_key or os.getenv('SENDGRID_API_KEY')
        self.from_email = from_email
        self.from_name = from_name
        
        # Rate limiting (SendGrid free: 100/day)
        self.rate_limit_file = Path('/tmp/depotchaos_sendgrid_last.txt')
        self.min_delay_seconds = 900  # 15 min between sends = 96/day (under limit)
        
        # Queue paths
        self.datadepot_dir = Path('/root/.openclaw/workspace/datadepot')
        self.queue_file = self.datadepot_dir / 'queue' / 'pending_emails.json'
        self.sent_file = self.datadepot_dir / 'queue' / 'sent_emails.json'
        self.failed_file = self.datadepot_dir / 'queue' / 'failed_emails.json'
        
        # Ensure queue directory exists
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"SendGridSender initialized: from={from_email}")
    
    def _check_rate_limit(self) -> tuple[bool, int]:
        """Check if we can send now. Returns (can_send, wait_seconds)"""
        now = time.time()
        
        if not self.rate_limit_file.exists():
            return True, 0
        
        try:
            last_send = float(self.rate_limit_file.read_text().strip())
            time_since = now - last_send
            
            if time_since < self.min_delay_seconds:
                wait_time = int(self.min_delay_seconds - time_since)
                return False, wait_time
            
            return True, 0
        except (ValueError, IOError) as e:
            logger.warning(f"Rate limit file error: {e}")
            return True, 0
    
    def _update_rate_limit(self):
        """Update last send timestamp"""
        self.rate_limit_file.write_text(str(time.time()))
    
    def _load_queue(self) -> List[Dict]:
        """Load pending email queue"""
        if not self.queue_file.exists():
            return []
        
        try:
            with open(self.queue_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse queue: {e}")
            return []
    
    def _save_queue(self, queue: List[Dict]):
        """Save pending email queue"""
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
    
    def _load_sent(self) -> List[Dict]:
        """Load sent email log"""
        if not self.sent_file.exists():
            return []
        
        try:
            with open(self.sent_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    
    def _save_sent(self, sent: List[Dict]):
        """Save sent email log"""
        with open(self.sent_file, 'w') as f:
            json.dump(sent, f, indent=2)
    
    def _load_failed(self) -> List[Dict]:
        """Load failed email log"""
        if not self.failed_file.exists():
            return []
        
        try:
            with open(self.failed_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    
    def _save_failed(self, failed: List[Dict]):
        """Save failed email log"""
        with open(self.failed_file, 'w') as f:
            json.dump(failed, f, indent=2)
    
    def send_email(self, email_data: Dict) -> Dict:
        """
        Send single email via SendGrid API
        
        Args:
            email_data: Dict with to_email, subject, html_body, text_body, etc.
        
        Returns:
            Dict with success status, message_id, error info
        """
        import uuid
        
        if not self.api_key:
            return {
                'success': False,
                'error': 'SENDGRID_API_KEY not configured',
                'test_mode': True
            }
        
        # Check rate limit
        can_send, wait_time = self._check_rate_limit()
        if not can_send:
            return {
                'success': False,
                'error': f'Rate limit: wait {wait_time}s before sending',
                'retry_after': wait_time,
                'rate_limited': True
            }
        
        # Prepare email data for SendGrid
        to_email = email_data.get('to_email') or email_data.get('recipient_email')
        if not to_email:
            return {'success': False, 'error': 'No recipient email'}
        
        subject = email_data.get('subject', 'Performance Supply Depot')
        html_content = email_data.get('html_body') or email_data.get('body', '')
        text_content = email_data.get('text_body', '')
        
        # Build SendGrid payload
        message_id = str(uuid.uuid4())
        
        payload = {
            'personalizations': [{
                'to': [{'email': to_email}],
                'subject': subject
            }],
            'from': {
                'email': self.from_email,
                'name': self.from_name
            },
            'reply_to': {
                'email': 'info@psdepot.com',
                'name': 'Performance Supply Depot Support'
            },
            'content': [],
            'custom_args': {
                'email_id': message_id,
                'campaign_id': email_data.get('campaign_id', 'default'),
                'lead_id': str(email_data.get('lead_id', ''))
            }
        }
        
        # Add content
        if html_content:
            payload['content'].append({
                'type': 'text/html',
                'value': html_content
            })
        if text_content:
            payload['content'].append({
                'type': 'text/plain',
                'value': text_content
            })
        elif not html_content:
            # Fallback
            payload['content'].append({
                'type': 'text/plain',
                'value': 'Email from Performance Supply Depot'
            })
        
        # Send via SendGrid API
        try:
            import http.client
            
            conn = http.client.HTTPSConnection("api.sendgrid.com")
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            conn.request("POST", "/v3/mail/send", json.dumps(payload), headers)
            response = conn.getresponse()
            
            if response.status in [200, 201, 202]:
                # Success
                self._update_rate_limit()
                
                return {
                    'success': True,
                    'message_id': message_id,
                    'sendgrid_message_id': response.getheader('X-Message-Id', 'unknown'),
                    'to_email': to_email
                }
            else:
                # API error
                error_body = response.read().decode('utf-8')
                logger.error(f"SendGrid error {response.status}: {error_body}")
                
                return {
                    'success': False,
                    'error': f'SendGrid API error {response.status}: {error_body[:200]}',
                    'status_code': response.status
                }
        
        except Exception as e:
            logger.error(f"SendGrid send error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_queue(self, max_emails: int = 1) -> Dict:
        """
        Process pending email queue
        
        Args:
            max_emails: Maximum emails to send (default 1 for rate limiting)
        
        Returns:
            Dict with processing results
        """
        queue = self._load_queue()
        
        if not queue:
            return {'success': True, 'processed': 0, 'message': 'Queue empty'}
        
        # Check rate limit first
        can_send, wait_time = self._check_rate_limit()
        if not can_send:
            return {
                'success': False,
                'rate_limited': True,
                'wait_seconds': wait_time,
                'message': f'Rate limited: wait {wait_time}s'
            }
        
        processed = []
        failed = []
        sent = []
        
        # Process up to max_emails
        remaining = []
        for i, email in enumerate(queue):
            if len(processed) >= max_emails:
                remaining.append(email)
                continue
            
            result = self.send_email(email)
            
            if result['success']:
                email['sent_at'] = datetime.now().isoformat()
                email['message_id'] = result['message_id']
                sent.append(email)
                processed.append(email['id'])
            else:
                email['failed_at'] = datetime.now().isoformat()
                email['error'] = result['error']
                failed.append(email)
                processed.append(email['id'])
                remaining.append(email)  # Keep in queue for retry
        
        # Add to sent log
        if sent:
            existing_sent = self._load_sent()
            existing_sent.extend(sent)
            self._save_sent(existing_sent)
        
        # Add to failed log
        if failed:
            existing_failed = self._load_failed()
            existing_failed.extend(failed)
            self._save_failed(existing_failed)
        
        # Save remaining queue
        self._save_queue(remaining)
        
        return {
            'success': True,
            'processed': len(processed),
            'sent': len(sent),
            'failed': len(failed),
            'remaining': len(remaining)
        }
    
    def get_queue_status(self) -> Dict:
        """Get current queue status"""
        queue = self._load_queue()
        sent = self._load_sent()
        failed = self._load_failed()
        
        today = datetime.now().strftime('%Y-%m-%d')
        sent_today = len([s for s in sent if s.get('sent_at', '').startswith(today)])
        failed_today = len([f for f in failed if f.get('failed_at', '').startswith(today)])
        
        can_send, wait_time = self._check_rate_limit()
        
        return {
            'total_pending': len(queue),
            'total_sent': len(sent),
            'total_failed': len(failed),
            'sent_today': sent_today,
            'failed_today': failed_today,
            'can_send_now': can_send,
            'wait_seconds': wait_time if not can_send else 0,
            'api_key_configured': bool(self.api_key)
        }


# Singleton instance
_sender = None

def get_sender() -> SendGridSender:
    """Get or create SendGrid sender singleton"""
    global _sender
    if _sender is None:
        _sender = SendGridSender()
    return _sender


def send_single_email(email_data: Dict) -> Dict:
    """Send a single email"""
    sender = get_sender()
    return sender.send_email(email_data)


def process_email_queue(max_emails: int = 1) -> Dict:
    """Process the pending email queue"""
    sender = get_sender()
    return sender.process_queue(max_emails)


def get_status() -> Dict:
    """Get queue and rate limit status"""
    sender = get_sender()
    return sender.get_queue_status()


if __name__ == '__main__':
    # CLI usage
    import argparse
    
    parser = argparse.ArgumentParser(description='SendGrid email sender')
    parser.add_argument('--status', action='store_true', help='Show queue status')
    parser.add_argument('--send', action='store_true', help='Send one pending email')
    parser.add_argument('--process', type=int, default=1, help='Process N emails')
    
    args = parser.parse_args()
    
    if args.status:
        status = get_status()
        print(json.dumps(status, indent=2))
    
    elif args.send or args.process > 0:
        result = process_email_queue(args.process)
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()
