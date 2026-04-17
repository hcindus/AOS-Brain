#!/usr/bin/env python3
"""
📧 SEND DAILY QUEUE REPORT EMAIL
Sends the daily queue status report to Captain
"""

import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Report date
REPORT_DATE = datetime.utcnow().strftime('%Y-%m-%d')
REPORT_FILE = f"/root/.openclaw/workspace/queue/DAILY_STATUS_{REPORT_DATE}.md"

# Email configuration
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
FROM_EMAIL = "miles@myl0nr0s.cloud"
TO_EMAIL = "antonio.hudnall@gmail.com"

# Try to get password from environment, otherwise use stored credential
FROM_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'Myl0n.R0s')

# Read the report
try:
    with open(REPORT_FILE, 'r') as f:
        report_content = f.read()
except Exception as e:
    print(f"❌ Could not read report file: {e}")
    exit(1)

# Create message
msg = MIMEMultipart('alternative')
msg['Subject'] = f"📊 Daily Queue Status Report - {REPORT_DATE}"
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL

# Attach report as plain text
text_part = MIMEText(report_content, 'plain', 'utf-8')
msg.attach(text_part)

print("📧 Sending daily queue report...")
print(f"   From: {FROM_EMAIL}")
print(f"   To: {TO_EMAIL}")
print(f"   Report: {REPORT_FILE}")
print(f"   Server: {SMTP_SERVER}:{SMTP_PORT}")

try:
    # Create context
    context = ssl.create_default_context()
    
    # Connect and send
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.send_message(msg)
    
    print("\n✅ Daily queue report sent successfully!")
    print(f"   Report delivered to {TO_EMAIL}")
    print(f"   Date: {REPORT_DATE}")
    
except Exception as e:
    print(f"\n❌ Failed to send email: {e}")
    print(f"\n📄 Report saved locally at:")
    print(f"   {REPORT_FILE}")
    exit(1)
