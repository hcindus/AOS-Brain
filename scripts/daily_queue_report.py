#!/usr/bin/env python3
"""
Daily Queue Email Report Script
Generates and emails a daily status report of all queues to Captain
"""

import json
import subprocess
import os
from datetime import datetime, timedelta

# Configuration
RECIPIENT = "Antonio.hudnall@gmail.com"
REPORT_DATE = datetime.utcnow().strftime("%Y-%m-%d")


def load_json_safe(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        return []


def count_json_items(filepath):
    """Count items in a JSON array file"""
    data = load_json_safe(filepath)
    return len(data) if isinstance(data, list) else 0


def get_recent_sent_emails(filepath, days=1):
    """Get emails sent in the last N days"""
    data = load_json_safe(filepath)
    if not isinstance(data, list):
        return 0
    
    cutoff = datetime.utcnow() - timedelta(days=days)
    recent = 0
    for item in data:
        sent_at = item.get('sent_at') or item.get('created_at')
        if sent_at:
            try:
                sent_dt = datetime.fromisoformat(sent_at.replace('Z', '+00:00').replace('+00:00', ''))
                if sent_dt >= cutoff:
                    recent += 1
            except:
                pass
    return recent


def get_campaigns_pending(pending_emails):
    """Get campaign summary from pending emails"""
    campaigns = {}
    for email in pending_emails:
        campaign = email.get('campaign_id', 'unknown')
        campaigns[campaign] = campaigns.get(campaign, 0) + 1
    return campaigns


def generate_report():
    """Generate the daily queue report"""
    
    # File paths
    pending_file = "/root/.openclaw/workspace/datadepot/queue/pending_emails.json"
    sent_file = "/root/.openclaw/workspace/datadepot/queue/sent_emails.json"
    followup_file = "/root/.openclaw/workspace/datadepot/queue/followup_queue_20260429.json"
    
    # Load data
    pending_emails = load_json_safe(pending_file)
    followup_queue = load_json_safe(followup_file)
    
    # Counts
    pending_count = len(pending_emails) if isinstance(pending_emails, list) else 0
    followup_count = len(followup_queue) if isinstance(followup_queue, list) else 0
    sent_count = count_json_items(sent_file)
    sent_last_24h = get_recent_sent_emails(sent_file, days=1)
    sent_last_7d = get_recent_sent_emails(sent_file, days=7)
    
    # Campaign breakdown
    campaigns = get_campaigns_pending(pending_emails) if isinstance(pending_emails, list) else {}
    
    # Generate report
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    report = f"""
╔════════════════════════════════════════════════════════════════════╗
║         📊 DAILY QUEUE EMAIL REPORT — {REPORT_DATE}               ║
╠════════════════════════════════════════════════════════════════════╣
║ Generated: {timestamp:<51} ║
╚════════════════════════════════════════════════════════════════════╝

📧 EMAIL QUEUE STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Pending Emails:     {pending_count}
• Follow-up Queue:    {followup_count}
• Total Sent (All Time): {sent_count}
• Sent (Last 24h):    {sent_last_24h}
• Sent (Last 7 Days): {sent_last_7d}

📋 PENDING BY CAMPAIGN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    if campaigns:
        for campaign, count in sorted(campaigns.items(), key=lambda x: -x[1]):
            report += f"  • {campaign}: {count}\n"
    else:
        report += "  No pending campaigns\n"
    
    # Sample of pending emails (first 5)
    report += """
📨 RECENT PENDING EMAILS (First 5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    if pending_count > 0 and isinstance(pending_emails, list):
        for email in pending_emails[:5]:
            to = email.get('to_email', 'unknown')
            subject = email.get('subject', 'No subject')[:40]
            campaign = email.get('campaign_id', 'unknown')
            report += f"  → {to}\n"
            report += f"    Subject: {subject}...\n"
            report += f"    Campaign: {campaign}\n\n"
    else:
        report += "  No pending emails\n"
    
    # System health check
    report += """
🔧 SYSTEM HEALTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # Check if queue files exist
    for label, path in [
        ("Pending emails", pending_file),
        ("Sent emails", sent_file),
        ("Follow-up queue", followup_file)
    ]:
        exists = "✅" if os.path.exists(path) else "❌"
        size = os.path.getsize(path) / 1024 if os.path.exists(path) else 0
        report += f"  {exists} {label}: {size:.1f} KB\n"
    
    # Action items
    report += """
⚡ ACTION ITEMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    if pending_count > 0:
        report += f"  ⏳ {pending_count} emails awaiting delivery\n"
    if sent_last_24h == 0 and pending_count > 0:
        report += "  ⚠️  No emails sent in last 24h — check SMTP status\n"
    if followup_count > 100:
        report += f"  📌 Follow-up queue has {followup_count} items — may need review\n"
    
    report += """
📁 FILE LOCATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Pending:   /root/.openclaw/workspace/datadepot/queue/pending_emails.json
  • Sent:      /root/.openclaw/workspace/datadepot/queue/sent_emails.json
  • Follow-up: /root/.openclaw/workspace/datadepot/queue/followup_queue_20260429.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Miles (AOS Operations)
Report schedule: Daily at 1:23 PM UTC
Contact: miles@myl0nr0s.cloud
"""
    
    return report


def send_email(recipient, subject, body):
    """Send email using mail command"""
    try:
        proc = subprocess.Popen(
            ['mail', '-s', subject, recipient],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=body)
        
        if proc.returncode == 0:
            return True, "Email sent successfully"
        else:
            return False, f"mail command failed: {stderr}"
    except Exception as e:
        return False, str(e)


def main():
    print("📊 Generating Daily Queue Email Report...")
    print("=" * 60)
    
    # Generate report
    report = generate_report()
    
    # Save to file
    report_file = f"/root/.openclaw/workspace/daily_reports/queue_status_{REPORT_DATE}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"✅ Report saved to: {report_file}")
    
    # Send email
    subject = f"📊 Daily Queue Report — {REPORT_DATE}"
    print(f"\n📧 Sending email to {RECIPIENT}...")
    
    success, message = send_email(RECIPIENT, subject, report)
    
    if success:
        print(f"✅ {message}")
        print(f"   To: {RECIPIENT}")
        print(f"   Subject: {subject}")
    else:
        print(f"❌ Failed to send email: {message}")
        return 1
    
    print("\n" + "=" * 60)
    print("📊 Queue Report Complete!")
    return 0


if __name__ == "__main__":
    exit(main())
