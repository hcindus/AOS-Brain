#!/usr/bin/env python3
"""
📧 Mylsixs Email Manager v1.0
Dedicated email management system for Captain
Filters, classifies, routes, and protects inbox
"""

import imaplib
import smtplib
import ssl
import email
import json
import os
from email.header import decode_header
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
CONFIG = {
    'imap_server': 'imap.gmail.com',
    'smtp_server': 'smtp.gmail.com',
    'captain_email': 'Antonio.hudnall@gmail.com',
    'check_interval': 3600,  # Check every hour
    'workspace': '/root/.openclaw/workspace',
    'mylsixs_workspace': '/root/.openclaw/workspace/AGI_COMPANY/agents/tier3/mylsixs',
    'log_file': '/var/log/aos/mylsixs_email.log'
}

class EmailManager:
    def __init__(self):
        self.emails_processed = 0
        self.emails_by_category = {}
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories"""
        dirs = [
            f"{CONFIG['mylsixs_workspace']}/emails",
            f"{CONFIG['mylsixs_workspace']}/emails/inbox",
            f"{CONFIG['mylsixs_workspace']}/emails/sorted",
            f"{CONFIG['mylsixs_workspace']}/emails/sorted/action_required",
            f"{CONFIG['mylsixs_workspace']}/emails/sorted/info_only",
            f"{CONFIG['mylsixs_workspace']}/emails/sorted/promotions",
            f"{CONFIG['mylsixs_workspace']}/emails/sorted/captain_only",
            f"{CONFIG['mylsixs_workspace']}/reports",
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def log(self, message):
        """Log activity"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(CONFIG['log_file'], 'a') as f:
            f.write(f"{log_entry}\n")
    
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
    
    def classify_email(self, from_addr, subject, body_preview):
        """Classify email into categories"""
        from_lower = from_addr.lower()
        subject_lower = subject.lower()
        
        # HIGH PRIORITY - From Captain's email
        if 'antonio.hudnall' in from_lower or 'hcindus' in from_lower:
            return 'captain_only', 'CRITICAL'
        
        # URGENT keywords
        urgent_keywords = ['urgent', 'asap', 'immediately', 'critical', 'emergency', 'deadline', 'action required']
        if any(k in subject_lower for k in urgent_keywords):
            return 'action_required', 'URGENT'
        
        # From AGI Company domain or known contacts
        agi_domains = ['@myl0nr0s.cloud', '@performance', '@agi-company']
        if any(d in from_lower for d in agi_domains):
            return 'action_required', 'HIGH'
        
        # Informational emails
        info_keywords = ['newsletter', 'update', 'report', 'summary', 'digest', 'notification']
        if any(k in subject_lower for k in info_keywords):
            return 'info_only', 'NORMAL'
        
        # Promotions/Spam indicators
        promo_keywords = ['unsubscribe', 'offer', 'sale', 'discount', 'promo', 'marketing', 'newsletter@']
        if any(k in subject_lower for k in promo_keywords) or 'unsubscribe' in body_preview.lower():
            return 'promotions', 'LOW'
        
        # Default - needs review
        return 'action_required', 'NORMAL'
    
    def process_emails(self):
        """Main email processing function"""
        self.log("📧 MYLSIXS: Starting email check...")
        
        # Check if email credentials exist
        creds_file = f"{CONFIG['mylsixs_workspace']}/.email_creds"
        if not os.path.exists(creds_file):
            self.log("⚠️ Email credentials not configured. Waiting for Captain to provide access.")
            self.create_setup_instructions()
            return
        
        with open(creds_file) as f:
            creds = json.load(f)
        
        try:
            # Connect to IMAP
            context = ssl.create_default_context()
            imap = imaplib.IMAP4_SSL(CONFIG['imap_server'], ssl_context=context)
            imap.login(creds['email'], creds['password'])
            imap.select('INBOX')
            
            # Search for unread messages
            status, messages = imap.search(None, 'UNSEEN')
            
            if status != 'OK' or not messages[0]:
                self.log("📭 No new unread messages")
                imap.close()
                imap.logout()
                return
            
            msg_ids = messages[0].split()
            self.log(f"📨 Found {len(msg_ids)} unread message(s)")
            
            daily_summary = {
                'date': datetime.now().isoformat(),
                'total_unread': len(msg_ids),
                'categorized': {},
                'action_required': [],
                'captain_messages': []
            }
            
            for msg_id in msg_ids:
                status, msg_data = imap.fetch(msg_id, '(RFC822)')
                
                if status != 'OK':
                    continue
                
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                # Extract details
                subject = self.decode_header_value(email_message['Subject'])
                from_addr = self.decode_header_value(email_message['From'])
                date = email_message['Date']
                msg_id_header = email_message['Message-ID'] or f"generated_{datetime.now().timestamp()}"
                
                # Get body preview
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
                
                body_preview = body[:500] if body else ""
                
                # Classify email
                category, priority = self.classify_email(from_addr, subject, body_preview)
                
                # Save email to file
                safe_msg_id = msg_id_header.replace('<', '').replace('>', '').replace('@', '_').replace('.', '_')[:50]
                email_file = f"{CONFIG['mylsixs_workspace']}/emails/sorted/{category}/{safe_msg_id}.json"
                
                email_data = {
                    'msg_id': msg_id_header,
                    'from': from_addr,
                    'subject': subject,
                    'date': date,
                    'category': category,
                    'priority': priority,
                    'body_preview': body_preview[:1000],
                    'processed_by': 'mylsixs',
                    'processed_at': datetime.now().isoformat(),
                    'status': 'pending_review'
                }
                
                with open(email_file, 'w') as f:
                    json.dump(email_data, f, indent=2)
                
                # Update tracking
                self.emails_processed += 1
                self.emails_by_category[category] = self.emails_by_category.get(category, 0) + 1
                
                # Add to daily summary
                if category not in daily_summary['categorized']:
                    daily_summary['categorized'][category] = []
                daily_summary['categorized'][category].append(email_data)
                
                if category == 'action_required':
                    daily_summary['action_required'].append(email_data)
                
                if category == 'captain_only':
                    daily_summary['captain_messages'].append(email_data)
                
                self.log(f"  [{priority}] {category}: {subject[:60]}...")
                
                # Mark as read (optional - can keep unread for Captain)
                # imap.store(msg_id, '+FLAGS', '\\Seen')
            
            imap.close()
            imap.logout()
            
            # Save daily report
            report_file = f"{CONFIG['mylsixs_workspace']}/reports/daily_email_report_{datetime.now().strftime('%Y%m%d')}.json"
            with open(report_file, 'w') as f:
                json.dump(daily_summary, f, indent=2)
            
            self.log(f"✅ Processed {self.emails_processed} emails")
            self.log(f"📊 Categories: {self.emails_by_category}")
            self.log(f"📝 Report saved: {report_file}")
            
            # Update daily report for Captain
            self.update_daily_report(daily_summary)
            
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
    
    def create_setup_instructions(self):
        """Create instructions for Captain to set up email access"""
        instructions = f"""# Email Access Setup Required

**Agent:** Mylsixs (Mail Clerk)
**Date:** {datetime.now().isoformat()}
**Status:** AWAITING EMAIL CREDENTIALS

## Setup Instructions

To enable email management, Captain needs to create credentials file:

```bash
# Create credentials file
cat > /root/.openclaw/workspace/AGI_COMPANY/agents/tier3/mylsixs/.email_creds << 'EOF'
{{
    "email": "Antonio.hudnall@gmail.com",
    "password": "YOUR_APP_PASSWORD",
    "provider": "gmail"
}}
EOF

# Secure the file
chmod 600 /root/.openclaw/workspace/AGI_COMPANY/agents/tier3/mylsixs/.email_creds
```

**Note:** For Gmail, use an App Password instead of your regular password.
Go to: Google Account > Security > 2-Step Verification > App passwords

## Mylsixs Responsibilities

Once configured, Mylsixs will:

1. **Check email hourly** for new messages
2. **Classify and sort** into categories:
   - 🔴 CRITICAL: Direct from Captain (you)
   - 🟠 URGENT: Action required ASAP
   - 🟡 HIGH: From AGI Company/team members
   - 🟢 NORMAL: Information only
   - ⚪ LOW: Promotions/spam

3. **Update daily reports** with email summary
4. **Alert Captain** to urgent messages
5. **Maintain inbox** clean and organized

## Categories

- `captain_only/` - Messages from you (highest priority)
- `action_required/` - Needs Captain's attention
- `info_only/` - Read and archive
- `promotions/` - Low priority/optional

---
*Setup required before email management can begin*
"""
        
        setup_file = f"{CONFIG['mylsixs_workspace']}/EMAIL_SETUP_REQUIRED.md"
        with open(setup_file, 'w') as f:
            f.write(instructions)
        
        self.log(f"📋 Created setup instructions: {setup_file}")
    
    def update_daily_report(self, summary):
        """Update the daily report with email summary"""
        report_date = datetime.now().strftime('%Y-%m-%d')
        daily_report_file = f"{CONFIG['workspace']}/memory/{report_date}_email_summary.md"
        
        report_content = f"""# Daily Email Summary - {report_date}
**Agent:** Mylsixs (Mail Clerk)
**Generated:** {datetime.now().isoformat()}

## 📧 Email Statistics

- **Total Unread:** {summary['total_unread']}
- **From Captain (You):** {len(summary.get('captain_messages', []))}
- **Action Required:** {len(summary.get('action_required', []))}

## 📂 Categories

"""
        
        for category, emails in summary.get('categorized', {}).items():
            report_content += f"\n### {category.upper()} ({len(emails)} emails)\n"
            for email in emails[:5]:  # Top 5 per category
                report_content += f"- [{email['priority']}] {email['subject'][:60]}\n"
            if len(emails) > 5:
                report_content += f"- ... and {len(emails) - 5} more\n"
        
        report_content += f"""
## 🚨 Urgent Items Requiring Attention

"""
        
        if summary.get('action_required'):
            for email in summary['action_required'][:10]:
                report_content += f"- **[{email['priority']}]** {email['subject']}\n"
                report_content += f"  From: {email['from']}\n\n"
        else:
            report_content += "No urgent items requiring action.\n"
        
        report_content += f"""
---
*Next check: {(datetime.now() + timedelta(hours=1)).strftime('%H:%M')} UTC*
*Full email details: {CONFIG['mylsixs_workspace']}/reports/*
"""
        
        with open(daily_report_file, 'w') as f:
            f.write(report_content)
        
        self.log(f"📊 Updated daily report: {daily_report_file}")

def main():
    manager = EmailManager()
    manager.process_emails()

if __name__ == '__main__':
    main()
