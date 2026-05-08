#!/usr/bin/env python3
"""
Send SOP Document via Email
Created: 2026-05-08
Purpose: Email the Database Operations SOP to Captain
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

# Load credentials from environment
SMTP_USER = os.getenv('HOSTINGER_SMTP_USER', 'miles@myl0nr0s.cloud')
SMTP_PASS = os.getenv('HOSTINGER_SMTP_PASS', 'Myl0n.R0s')
SMTP_SERVER = os.getenv('HOSTINGER_SMTP_SERVER', 'smtp.hostinger.com')
SMTP_PORT = int(os.getenv('HOSTINGER_SMTP_PORT', '587'))

# Recipient
TO_EMAIL = "Antonio.Hudnall@gmail.com"
FROM_EMAIL = SMTP_USER

# Read the SOP document
sop_path = "/root/.openclaw/workspace/SOP_DATABASE_OPERATIONS.md"
with open(sop_path, 'r') as f:
    sop_content = f.read()

# Create message
msg = MIMEMultipart()
msg['From'] = f"Miles <{FROM_EMAIL}>"
msg['To'] = TO_EMAIL
msg['Subject'] = "📊 Database Operations SOP - Complete Beginner's Guide"
msg['Reply-To'] = FROM_EMAIL

# Email body (HTML)
html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
            text-align: center;
        }}
        .content {{
            background: #f9f9f9;
            padding: 30px;
            border-radius: 0 0 10px 10px;
        }}
        h1 {{
            margin: 0;
            font-size: 24px;
        }}
        h2 {{
            color: #667eea;
            font-size: 18px;
            margin-top: 25px;
        }}
        .highlight {{
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }}
        .cta {{
            background: #667eea;
            color: white;
            padding: 15px 25px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin-top: 20px;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        .footer {{
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Database Operations SOP</h1>
        <p>Complete Beginner's Guide</p>
    </div>
    
    <div class="content">
        <p>Hey Captain,</p>
        
        <p>I've prepared a comprehensive Standard Operating Procedure for working with your databases. This document assumes <strong>zero prior knowledge</strong> and will take you from complete beginner to confidently adding and updating records.</p>
        
        <div class="highlight">
            <strong>📎 Attachment:</strong> SOP_DATABASE_OPERATIONS.md (17+ pages of detailed documentation)
        </div>
        
        <h2>What's Inside:</h2>
        <ul>
            <li><strong>Part 1:</strong> Database basics explained simply</li>
            <li><strong>Part 2:</strong> Command line operations (SQLite)</li>
            <li><strong>Part 3:</strong> Python operations (recommended)</li>
            <li><strong>Part 4:</strong> Common use cases by workflow</li>
            <li><strong>Part 5:</strong> Best practices and safety rules</li>
            <li><strong>Part 6:</strong> Quick reference cheat sheet</li>
            <li><strong>Part 7:</strong> Troubleshooting guide</li>
        </ul>
        
        <h2>Your Databases:</h2>
        <ul>
            <li><code>/data/depot_chaos/unified.db</code> - Sales leads & customer data</li>
            <li><code>/AGI_COMPANY/subsidiaries/DATADEPOT_INTELLIGENCE/database/datadepot.db</code> - Business intelligence</li>
            <li><code>/DepotChaos/depot_chaos.db</code> - Vendor management</li>
        </ul>
        
        <div class="highlight">
            <strong>💡 Pro Tip:</strong> Start with Part 1 (The Basics) and Part 7 (Quick Reference Cheat Sheet). You can dig into the detailed sections as needed.
        </div>
        
        <h2>Quick Start Commands:</h2>
        <p><strong>Connect to database:</strong></p>
        <code>sqlite3 /root/.openclaw/workspace/data/depot_chaos/unified.db</code>
        
        <p><strong>View all tables:</strong></p>
        <code>.tables</code>
        
        <p><strong>See table structure:</strong></p>
        <code>.schema leads</code>
        
        <p><strong>Exit:</strong></p>
        <code>.quit</code>
        
        <p>Review the attached document and let me know if you need any clarifications or have questions!</p>
        
        <p>Best,<br>
        <strong>Miles</strong><br>
        Autonomous Operations Engine</p>
    </div>
    
    <div class="footer">
        <p>Performance Supply Depot LLC | AGI Company</p>
        <p>Sent: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
    </div>
</body>
</html>
"""

# Attach HTML body
msg.attach(MIMEText(html_body, 'html'))

# Attach the SOP file
with open(sop_path, 'rb') as f:
    attachment = MIMEApplication(f.read(), _subtype='md')
    attachment.add_header('Content-Disposition', 'attachment', filename='SOP_DATABASE_OPERATIONS.md')
    msg.attach(attachment)

# Send email
try:
    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    print(f"Logging in as {SMTP_USER}...")
    server.login(SMTP_USER, SMTP_PASS)
    
    print(f"Sending email to {TO_EMAIL}...")
    server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
    server.quit()
    
    print("✅ Email sent successfully!")
    print(f"   To: {TO_EMAIL}")
    print(f"   Subject: {msg['Subject']}")
    print(f"   Attachment: SOP_DATABASE_OPERATIONS.md ({len(sop_content)} bytes)")
    
except Exception as e:
    print(f"❌ Error sending email: {e}")
    exit(1)
