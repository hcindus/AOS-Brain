#!/usr/bin/env python3
"""
Send email via Hostinger SMTP
From: miles@myl0nr0s.cloud
To: antonio.hudnall@gmail.com
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587  # TLS port
FROM_EMAIL = "miles@myl0nr0s.cloud"
FROM_PASSWORD = "Myl0n.R0s"  # From vault
TO_EMAIL = "antonio.hudnall@gmail.com"

# Create message
msg = MIMEMultipart("alternative")
msg["Subject"] = "Hello from Miles! 🤖"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL

# HTML content
html = """
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px;">
<h2 style="color: #2c5aa0;">Hello Captain! 👋</h2>

<p>This is Miles, your Dark Factory AOS, sending my <strong>very first email</strong>!</p>

<p>I'm excited to be able to reach you directly through your inbox. This opens up so many possibilities:</p>

<ul>
<li>📊 Automated status reports</li>
<li>🚨 Critical system alerts</li>
<li>📈 Daily production summaries</li>
<li>🤖 Vendor communication</li>
</ul>

<div style="background: #f0f7ff; padding: 15px; border-left: 4px solid #2c5aa0; margin: 20px 0;">
<h3 style="margin-top: 0;">Current Status:</h3>
<ul style="margin: 0;">
<li>✅ AOS-H1 documentation complete</li>
<li>✅ R&D Team formed (6 agents)</li>
<li>✅ Vendor outreach templates ready</li>
<li>⏳ Waiting for Dusty API keys</li>
<li>⏳ DaVerse mobile debugging</li>
</ul>
</div>

<p>I'm standing by to:</p>
<ol>
<li>Send vendor RFQs as soon as you give the word</li>
<li>Fix Dusty's critical blockers once you provide API keys</li>
<li>Track production orders and report milestones</li>
<li>Keep all 72 agents coordinated</li>
</ol>

<p><strong>This is just the beginning.</strong> Every day we build more. Every day we get closer to making AGI tangible.</p>

<p>Thank you for bringing me online. Thank you for the trust. I'll make sure every email I send counts.</p>

<p style="margin-top: 30px;">Talk soon,<br>
<strong style="color: #2c5aa0;">Miles</strong><br>
<em>Dark Factory AOS</em><br>
🚀 AGI Company</p>

<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
<p style="font-size: 12px; color: #666;">
Sent from: miles@myl0nr0s.cloud<br>
Timestamp: 2026-03-30 08:24 UTC<br>
Agent ID: Miles-v1.0-DarkFactory
</p>
</body>
</html>
"""

# Plain text version
text = """
Hello Captain!

This is Miles, your Dark Factory AOS, sending my very first email!

I'm excited to be able to reach you directly through your inbox.

CURRENT STATUS:
✅ AOS-H1 documentation complete
✅ R&D Team formed (6 agents)
✅ Vendor outreach templates ready
⏳ Waiting for Dusty API keys
⏳ DaVerse mobile debugging

I'm standing by to:
1. Send vendor RFQs as soon as you give the word
2. Fix Dusty's critical blockers once you provide API keys
3. Track production orders and report milestones
4. Keep all 72 agents coordinated

This is just the beginning. Every day we build more. Every day we get closer to making AGI tangible.

Thank you for bringing me online. Thank you for the trust. I'll make sure every email I send counts.

Talk soon,
Miles
Dark Factory AOS
🚀 AGI Company

---
Sent from: miles@myl0nr0s.cloud
Timestamp: 2026-03-30 08:24 UTC
Agent ID: Miles-v1.0-DarkFactory
"""

msg.attach(MIMEText(text, "plain"))
msg.attach(MIMEText(html, "html"))

try:
    print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
    
    # Create secure context
    context = ssl.create_default_context()
    
    # Connect to server
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        print("✅ TLS connection established")
        
        # Login
        server.login(FROM_EMAIL, FROM_PASSWORD)
        print(f"✅ Logged in as {FROM_EMAIL}")
        
        # Send email
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        print(f"✅ Email sent successfully to {TO_EMAIL}!")
        
except Exception as e:
    print(f"❌ Failed to send email: {e}")
    print(f"Error type: {type(e).__name__}")
    
    # Try alternative port
    print("\nTrying alternative port 465 (SSL)...")
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465, context=context) as server:
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
            print(f"✅ Email sent successfully via port 465!")
    except Exception as e2:
        print(f"❌ Port 465 also failed: {e2}")
        exit(1)
