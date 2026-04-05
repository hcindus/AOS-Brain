#!/usr/bin/env python3
"""
📧 SEND EMAIL REPORT
Sends the email verification test report to Captain
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Read the report
report_file = "/root/.openclaw/workspace/reports/email_verification_report_20260405_060834.md"

try:
    with open(report_file, 'r') as f:
        report_content = f.read()
except Exception as e:
    print(f"❌ Could not read report file: {e}")
    exit(1)

# Email configuration
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
FROM_EMAIL = "miles@myl0nr0s.cloud"
FROM_PASSWORD = "Myl0n.R0s"
TO_EMAIL = "antonio.hudnall@gmail.com"

# Create message
msg = MIMEMultipart('alternative')
msg['Subject'] = f"📧 Email Verification Test Report - {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL

# Attach report
text_part = MIMEText(report_content, 'plain', 'utf-8')
msg.attach(text_part)

print("📧 Sending email report...")
print(f"   From: {FROM_EMAIL}")
print(f"   To: {TO_EMAIL}")
print(f"   Server: {SMTP_SERVER}:{SMTP_PORT}")

try:
    # Create context
    context = ssl.create_default_context()
    
    # Connect and send
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.send_message(msg)
    
    print("\n✅ Email report sent successfully!")
    print(f"   Report delivered to {TO_EMAIL}")
    
except Exception as e:
    print(f"\n❌ Failed to send email: {e}")
    print("\n📄 Report saved locally:")
    print(f"   {report_file}")
    exit(1)
