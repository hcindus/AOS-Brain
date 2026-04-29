# Mailgun API Integration Guide for DataDepot
## Email Sending Infrastructure

---

## What is Mailgun?

Mailgun is an email delivery service that provides:
- **Reliable delivery** to inboxes (not spam folders)
- **High-volume sending** (10,000+ emails/month)
- **Tracking** (opens, clicks, bounces, unsubscribes)
- **Webhooks** for real-time event notifications
- **Template management** (store email templates in Mailgun)

**Pricing:**
- Free tier: 5,000 emails/month (first 3 months)
- Paid: $0.80/1,000 emails (Foundation plan)
- Your volume: ~1,500 emails/month = ~$1.20/month

---

## Step 1: Mailgun Account Setup

### 1.1 Create Account
```
1. Go to https://www.mailgun.com/
2. Sign up with psdepot business email
3. Verify domain: psdepot.com
```

### 1.2 Domain Verification (CRITICAL)

Mailgun requires DNS records to verify you own psdepot.com:

**Add these DNS records to your domain registrar:**

| Type | Name | Value | Priority |
|------|------|-------|----------|
| TXT | @ | v=spf1 include:mailgun.org ~all | - |
| TXT | pic._domainkey | (Mailgun provides) | - |
| TXT | @ | (Mailgun domain verification) | - |
| MX | @ | mxa.mailgun.org | 10 |
| MX | @ | mxb.mailgun.org | 10 |

**Verification takes:** 24-48 hours after DNS propagation

---

## Step 2: API Integration Code

### 2.1 Install Mailgun Python SDK

```bash
pip install mailgun-python
# OR
pip install requests  # For manual API calls
```

### 2.2 Configuration File

Create `/datadepot/config/mailgun_config.py`:

```python
"""
Mailgun API Configuration for DataDepot
"""

import os

# Load from environment variables (secure)
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', '')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN', 'psdepot.com')
MAILGUN_API_URL = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}"

# From email address
FROM_EMAIL = "miles@psdepot.com"
FROM_NAME = "Miles - Performance Supply Depot"

# Send limits (per day/hour to avoid throttling)
DAILY_SEND_LIMIT = 500  # Conservative for warmup
HOURLY_SEND_LIMIT = 50

# Tracking settings
TRACK_OPENS = True
TRACK_CLICKS = True

# Webhook endpoint for events
WEBHOOK_URL = "https://psdepot.com/webhooks/mailgun"

# Test mode (set True to prevent actual sending)
TEST_MODE = os.getenv('MAILGUN_TEST_MODE', 'False').lower() == 'true'
```

### 2.3 Email Sender Class

Create `/datadepot/services/mailgun_sender.py`:

```python
"""
Mailgun Email Service for DataDepot
Handles personalized email sending with tracking
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import mailgun_config as config

class MailgunSender:
    def __init__(self):
        self.api_key = config.MAILGUN_API_KEY
        self.domain = config.MAILGUN_DOMAIN
        self.base_url = f"https://api.mailgun.net/v3/{self.domain}"
        self.auth = ("api", self.api_key)
        
        # Rate limiting
        self.hourly_sent = 0
        self.daily_sent = 0
        self.last_hour_reset = datetime.now()
        self.last_day_reset = datetime.now()
        
        # Statistics tracking
        self.stats = {
            'sent': 0,
            'delivered': 0,
            'opened': 0,
            'clicked': 0,
            'bounced': 0,
            'complained': 0,
            'failed': 0
        }
    
    def _check_rate_limits(self) -> bool:
        """Check if we can send more emails"""
        now = datetime.now()
        
        # Reset hourly counter
        if (now - self.last_hour_reset).seconds >= 3600:
            self.hourly_sent = 0
            self.last_hour_reset = now
        
        # Reset daily counter  
        if (now - self.last_day_reset).days >= 1:
            self.daily_sent = 0
            self.last_day_reset = now
        
        if self.hourly_sent >= config.HOURLY_SEND_LIMIT:
            print(f"[RATE LIMIT] Hourly limit reached ({config.HOURLY_SEND_LIMIT})")
            return False
            
        if self.daily_sent >= config.DAILY_SEND_LIMIT:
            print(f"[RATE LIMIT] Daily limit reached ({config.DAILY_SEND_LIMIT})")
            return False
        
        return True
    
    def send_template_email(
        self,
        to_email: str,
        to_name: str,
        template_name: str,
        merge_data: Dict[str, str],
        subject: str = None,
        campaign_id: Optional[str] = None,
        tags: List[str] = None
    ) -> Dict:
        """
        Send personalized email using template
        
        Args:
            to_email: Recipient email
            to_name: Recipient name  
            template_name: Template file name (without .txt)
            merge_data: Dictionary of merge tag values
            subject: Override subject (or use template first line)
            campaign_id: Tracking ID for this campaign
            tags: List of tags for segmentation
        """
        if not self._check_rate_limits():
            return {'success': False, 'error': 'Rate limit exceeded'}
        
        if config.TEST_MODE:
            print(f"[TEST MODE] Would send to: {to_email}")
            return {'success': True, 'test_mode': True, 'id': 'test_123'}
        
        try:
            # Load and render template
            template = self._load_template(template_name)
            rendered_html = self._render_template(template, merge_data)
            
            # Extract subject from template if not provided
            if subject is None:
                subject = self._extract_subject(template)
            
            # Prepare API call
            data = {
                'from': f"{config.FROM_NAME} <{config.FROM_EMAIL}>",
                'to': f"{to_name} <{to_email}>",
                'subject': subject,
                'html': rendered_html,
                'o:tracking': 'yes' if config.TRACK_OPENS else 'no',
                'o:tracking-clicks': 'yes' if config.TRACK_CLICKS else 'no',
                'v:campaign_id': campaign_id or 'default',
                'v:recipient_email': to_email,
                'v:template': template_name,
            }
            
            # Add tags
            if tags:
                for tag in tags[:3]:  # Mailgun allows max 3 tags
                    data[f'o:tag'] = tag
            
            # Send via Mailgun API
            response = requests.post(
                f"{self.base_url}/messages",
                auth=self.auth,
                data=data,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Update counters
            self.hourly_sent += 1
            self.daily_sent += 1
            self.stats['sent'] += 1
            
            return {
                'success': True,
                'id': result.get('id'),
                'message': result.get('message'),
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            self.stats['failed'] += 1
            return {'success': False, 'error': str(e)}
        except Exception as e:
            self.stats['failed'] += 1
            return {'success': False, 'error': str(e)}
    
    def send_batch(
        self,
        recipients: List[Dict],
        template_name: str,
        campaign_id: str,
        throttle_seconds: float = 1.0
    ) -> Dict:
        """
        Send batch emails with throttling
        
        Args:
            recipients: List of dicts with email, name, merge_data
            template_name: Template to use
            campaign_id: Campaign tracking ID
            throttle_seconds: Delay between sends
        """
        results = {
            'total': len(recipients),
            'sent': 0,
            'failed': 0,
            'errors': []
        }
        
        for idx, recipient in enumerate(recipients, 1):
            print(f"[BATCH] Sending {idx}/{len(recipients)} to {recipient['email']}")
            
            result = self.send_template_email(
                to_email=recipient['email'],
                to_name=recipient['name'],
                template_name=template_name,
                merge_data=recipient['merge_data'],
                campaign_id=campaign_id,
                tags=recipient.get('tags', [])
            )
            
            if result['success']:
                results['sent'] += 1
            else:
                results['failed'] += 1
                results['errors'].append({
                    'email': recipient['email'],
                    'error': result.get('error', 'Unknown error')
                })
            
            # Throttle to avoid overwhelming API
            if idx < len(recipients):
                time.sleep(throttle_seconds)
        
        return results
    
    def _load_template(self, template_name: str) -> str:
        """Load email template from file"""
        template_path = f"/root/.openclaw/workspace/datadepot/templates/email/{template_name}.txt"
        
        with open(template_path, 'r') as f:
            return f.read()
    
    def _render_template(self, template: str, merge_data: Dict) -> str:
        """Replace merge tags with actual values"""
        rendered = template
        
        for tag, value in merge_data.items():
            rendered = rendered.replace(tag, str(value))
        
        # Convert plain text to HTML (basic)
        html = self._text_to_html(rendered)
        
        return html
    
    def _extract_subject(self, template: str) -> str:
        """Extract subject line from template (first line after 'Subject:')"""
        lines = template.split('\n')
        for line in lines:
            if line.startswith('Subject:'):
                return line.replace('Subject:', '').strip()
        return "DataDepot Intelligence - California Restaurant POS Data"
    
    def _text_to_html(self, text: str) -> str:
        """Convert plain text email to HTML"""
        # Simple conversion - wrap in HTML structure
        lines = text.split('\n')
        html_lines = []
        
        in_list = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip subject line
            if stripped.startswith('Subject:'):
                continue
            
            # Handle list items
            if stripped.startswith('→') or stripped.startswith('-') or stripped.startswith('•'):
                if not in_list:
                    html_lines.append('<ul style="margin: 10px 0; padding-left: 20px;">')
                    in_list = True
                item_text = stripped.lstrip('→-• ').strip()
                html_lines.append(f'<li style="margin: 5px 0; color: #333;">{item_text}</li>')
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                
                # Handle empty lines
                if not stripped:
                    html_lines.append('<br>')
                else:
                    # Regular paragraph
                    html_lines.append(f'<p style="margin: 10px 0; color: #333; line-height: 1.6;">{stripped}</p>')
        
        if in_list:
            html_lines.append('</ul>')
        
        body = '\n'.join(html_lines)
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            {body}
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            
            <p style="font-size: 12px; color: #999;">
                Performance Supply Depot LLC | DataDepot Intelligence<br>
                <a href="https://psdepot.com/unsubscribe?email={{Email}}" style="color: #999;">Unsubscribe</a>
            </p>
        </body>
        </html>
        """
    
    def get_stats(self) -> Dict:
        """Get sending statistics"""
        return {
            **self.stats,
            'hourly_sent': self.hourly_sent,
            'daily_sent': self.daily_sent,
            'hourly_limit': config.HOURLY_SEND_LIMIT,
            'daily_limit': config.DAILY_SEND_LIMIT
        }


# Webhook handler for Mailgun events
class MailgunWebhookHandler:
    """
    Handle Mailgun webhooks for tracking opens, clicks, bounces
    """
    
    @staticmethod
    def handle_event(event_data: Dict) -> Dict:
        """
        Process incoming Mailgun webhook
        """
        event_type = event_data.get('event')
        recipient = event_data.get('recipient')
        message_id = event_data.get('message-id')
        campaign_id = event_data.get('campaign-id', 'unknown')
        
        # Log the event
        print(f"[MAILGUN EVENT] {event_type}: {recipient} (Campaign: {campaign_id})")
        
        # Update CRM with event
        if event_type == 'opened':
            MailgunWebhookHandler._record_open(recipient, message_id, campaign_id)
        elif event_type == 'clicked':
            MailgunWebhookHandler._record_click(recipient, message_id, campaign_id, event_data.get('url'))
        elif event_type == 'delivered':
            MailgunWebhookHandler._record_delivery(recipient, message_id)
        elif event_type == 'bounced':
            MailgunWebhookHandler._record_bounce(recipient, message_id, event_data.get('reason'))
        elif event_type == 'complained':
            MailgunWebhookHandler._record_complaint(recipient, message_id)
        
        return {'status': 'processed'}
    
    @staticmethod
    def _record_open(email: str, message_id: str, campaign_id: str):
        """Record email open in CRM"""
        # Update stripe customer metadata
        # Update datadepot crm
        pass
    
    @staticmethod
    def _record_click(email: str, message_id: str, campaign_id: str, url: str):
        """Record link click in CRM"""
        # Update engagement score
        # Trigger sales notification if high-value link
        pass
    
    @staticmethod
    def _record_delivery(email: str, message_id: str):
        """Record successful delivery"""
        pass
    
    @staticmethod
    def _record_bounce(email: str, message_id: str, reason: str):
        """Record bounce and flag invalid email"""
        # Mark email as invalid in database
        # Stop sending to this address
        pass
    
    @staticmethod
    def _record_complaint(email: str, message_id: str):
        """Record spam complaint"""
        # Immediately unsubscribe
        # Flag in CRM
        pass


# Usage example
if __name__ == "__main__":
    # Initialize sender
    sender = MailgunSender()
    
    # Single email example
    result = sender.send_template_email(
        to_email="john@bayareapos.com",
        to_name="John Smith",
        template_name="email_1_hook",
        merge_data={
            '{{First_Name}}': 'John',
            '{{Company}}': 'Bay Area POS Solutions',
            '{{POS_Focus}}': 'Toast',
            '{{County}}': 'San Francisco',
            '{{Email}}': 'john@bayareapos.com'
        },
        campaign_id="cold_outbound_april_2026",
        tags=['cold_outbound', 'segment_a', 'day_1']
    )
    
    print(f"Send result: {result}")
    
    # Batch example
    recipients = [
        {
            'email': 'john@example.com',
            'name': 'John Smith',
            'merge_data': {'{{First_Name}}': 'John', '{{Company}}': 'Example Co'},
            'tags': ['hardware_buyer']
        },
        {
            'email': 'jane@example.com',
            'name': 'Jane Doe',
            'merge_data': {'{{First_Name}}': 'Jane', '{{Company}}': 'Another Co'},
            'tags': ['supply_recurring']
        }
    ]
    
    batch_result = sender.send_batch(
        recipients=recipients,
        template_name="email_1_hook",
        campaign_id="batch_test_april_2026",
        throttle_seconds=1.0
    )
    
    print(f"Batch results: {batch_result}")
```

---

## Step 3: Environment Setup

### 3.1 Secure API Key Storage

```bash
# Add to /root/.bashrc or /etc/environment
export MAILGUN_API_KEY="key-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export MAILGUN_DOMAIN="psdepot.com"
export MAILGUN_TEST_MODE="False"  # Set "True" for testing

# Reload environment
source /root/.bashrc
```

### 3.2 Webhook Endpoint (Flask)

Create `/datapdepot/webhook_server.py`:

```python
from flask import Flask, request, jsonify
from mailgun_sender import MailgunWebhookHandler
import os

app = Flask(__name__)

@app.route('/webhooks/mailgun', methods=['POST'])
def mailgun_webhook():
    """Receive Mailgun event webhooks"""
    event_data = request.form.to_dict()
    
    # Verify webhook signature (recommended)
    # timestamp = event_data.get('timestamp')
    # token = event_data.get('token')
    # signature = event_data.get('signature')
    
    result = MailgunWebhookHandler.handle_event(event_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
```

---

## Step 4: Testing Before Production

### 4.1 Test Mode
```python
# Set test mode
os.environ['MAILGUN_TEST_MODE'] = 'True'

# Run test sends
sender = MailgunSender()
result = sender.send_template_email(...)
# Output: "[TEST MODE] Would send to: john@bayareapos.com"
```

### 4.2 Sandbox Domain
```
1. Use Mailgun sandbox: sandboxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.mailgun.org
2. Add authorized recipient: your-email@example.com
3. Send test emails to authorized recipients only
4. Verify template rendering
```

### 4.3 Production Checklist
- [ ] Domain DNS records verified in Mailgun dashboard
- [ ] API key stored in environment variable
- [ ] Test emails rendering correctly
- [ ] Webhook endpoint responding to events
- [ ] Bounce/complaint handling implemented
- [ ] Rate limits configured (50/hour for warmup)
- [ ] Unsubscribe link in all emails
- [ ] SPF/DKIM passing authentication

---

## Step 5: Integration with Automation

### 5.1 Cron-Triggered Batches

Modify `/datadepot/cron/process_queue.py`:

```python
#!/usr/bin/env python3
"""
Process email queue every hour
Triggered by: 0 * * * * in cron
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/datadepot/services')

from mailgun_sender import MailgunSender
from stripe_integration import get_customers_for_sequence
import json
from datetime import datetime

def main():
    sender = MailgunSender()
    
    # Load pending emails from queue
    with open('/datadepot/queue/pending_emails.json', 'r') as f:
        queue = json.load(f)
    
    # Filter: Only send if scheduled time reached
    now = datetime.now()
    ready_to_send = [
        e for e in queue 
        if datetime.fromisoformat(e['scheduled_time']) <= now
    ]
    
    if not ready_to_send:
        print(f"[{now}] No emails ready to send")
        return
    
    print(f"[{now}] Processing {len(ready_to_send)} emails")
    
    # Send batch
    results = sender.send_batch(
        recipients=ready_to_send,
        template_name=ready_to_send[0]['template'],
        campaign_id=ready_to_send[0]['campaign_id'],
        throttle_seconds=2.0  # Conservative for warmup
    )
    
    # Log results
    with open(f'/datadepot/logs/email_send_{now.strftime("%Y%m%d_%H")}.log', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Update queue (remove sent items)
    remaining = [e for e in queue if e not in ready_to_send]
    with open('/datadepot/queue/pending_emails.json', 'w') as f:
        json.dump(remaining, f, indent=2)
    
    print(f"Sent: {results['sent']}, Failed: {results['failed']}")

if __name__ == "__main__":
    main()
```

---

## Mailgun vs Alternatives

| Feature | Mailgun | SendGrid | Amazon SES |
|---------|---------|----------|------------|
| **Free tier** | 5,000/mo (3mo) | 100/day | 62,000/mo |
| **Price** | $0.80/1K | $0.90/1K | $0.10/1K |
| **Deliverability** | Excellent | Excellent | Good |
| **API** | REST | REST | AWS SDK |
| **Templates** | ✅ | ✅ | ❌ |
| **Webhooks** | ✅ | ✅ | ✅ |
| **Support** | Good | Good | AWS level |

**Recommendation:** Start with Mailgun for ease of setup, migrate to SES at scale for cost savings.

---

## Troubleshooting

### Issue: Emails going to spam
**Solution:**
1. Verify SPF/DKIM records
2. Warm up IP gradually (start 10/day, increase 2x weekly)
3. Clean bounced emails immediately
4. Use double opt-in for list building

### Issue: API rate limit errors
**Solution:**
1. Implement exponential backoff
2. Reduce throttle_seconds
3. Increase HOURLY_SEND_LIMIT in config
4. Upgrade Mailgun plan

### Issue: Webhooks not receiving
**Solution:**
1. Check firewall (port 8081 open)
2. Verify webhook URL in Mailgun dashboard
3. Check webhook signature verification
4. Review nginx proxy_pass config

---

**Next Steps:**
1. Sign up at mailgun.com
2. Add DNS records to psdepot.com
3. Set MAILGUN_API_KEY environment variable
4. Run test sends in TEST_MODE=True
5. Switch to production after DNS verification

**Last Updated:** 2026-04-29
**Status:** Ready for Implementation
