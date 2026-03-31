#!/usr/bin/env python3
"""
Send email with Dusty Wallet API links
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
FROM_EMAIL = "miles@myl0nr0s.cloud"
FROM_PASSWORD = "Myl0n.R0s"
TO_EMAIL = "antonio.hudnall@gmail.com"

msg = MIMEMultipart("alternative")
msg["Subject"] = "Dusty Wallet - API Setup Links"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL

html = """
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px;">
<h2 style="color: #2c5aa0;">Dusty Wallet - API Setup Links</h2>

<p>Here are the three API services you need to set up for Dusty Wallet:</p>

<div style="background: #f0f7ff; padding: 15px; border-left: 4px solid #2c5aa0; margin: 20px 0;">
<h3 style="margin-top: 0;">1. Infura (Ethereum RPC)</h3>
<p><strong>URL:</strong> <a href="https://infura.io">https://infura.io</a></p>
<p><strong>What it does:</strong> Connects Dusty to Ethereum blockchain</p>
<p><strong>Cost:</strong> FREE tier (100,000 requests/day)</p>
<p><strong>What to get:</strong> Project ID</p>
<p><strong>Steps:</strong></p>
<ol>
<li>Create free account</li>
<li>Create new project</li>
<li>Copy Project ID</li>
</ol>
</div>

<div style="background: #f0f7ff; padding: 15px; border-left: 4px solid #2c5aa0; margin: 20px 0;">
<h3 style="margin-top: 0;">2. MongoDB Atlas (Database)</h3>
<p><strong>URL:</strong> <a href="https://mongodb.com/atlas">https://mongodb.com/atlas</a></p>
<p><strong>What it does:</strong> Stores wallet data permanently (not lost on restart)</p>
<p><strong>Cost:</strong> FREE tier (512MB)</p>
<p><strong>What to get:</strong> Connection String</p>
<p><strong>Steps:</strong></p>
<ol>
<li>Create free account</li>
<li>Create cluster (M0 Sandbox)</li>
<li>Create database user</li>
<li>Get connection string</li>
</ol>
</div>

<div style="background: #f0f7ff; padding: 15px; border-left: 4px solid #2c5aa0; margin: 20px 0;">
<h3 style="margin-top: 0;">3. CoinGecko (Price Feeds)</h3>
<p><strong>URL:</strong> <a href="https://coingecko.com/api">https://coingecko.com/api</a></p>
<p><strong>What it does:</strong> Gets real-time crypto prices</p>
<p><strong>Cost:</strong> FREE tier (no API key needed for basic)</p>
<p><strong>What to get:</strong> API Key (optional but recommended)</p>
<p><strong>Steps:</strong></p>
<ol>
<li>Create free account</li>
<li>Generate API key</li>
</ol>
</div>

<h3>Next Steps:</h3>
<p>Once you have all three, send me:</p>
<ol>
<li><strong>Infura Project ID</strong></li>
<li><strong>MongoDB Connection String</strong></li>
<li><strong>CoinGecko API Key</strong> (if you got one)</li>
</ol>

<p>Then I'll start <strong>Option A</strong>: Fix the 8 critical blockers and get Dusty handling real cryptocurrency in 2-3 weeks.</p>

<p>Questions? Just reply to this email.</p>

<p style="margin-top: 30px;">
Best regards,<br>
<strong style="color: #2c5aa0;">Miles</strong><br>
Dark Factory AOS
</p>

<hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
<p style="font-size: 12px; color: #666;">
Sent from: miles@myl0nr0s.cloud<br>
Timestamp: 2026-03-31 01:43 UTC
</p>
</body>
</html>
"""

text = """
Dusty Wallet - API Setup Links

Here are the three API services you need to set up:

1. INFURA (Ethereum RPC)
   URL: https://infura.io
   Purpose: Connects Dusty to Ethereum blockchain
   Cost: FREE tier (100,000 requests/day)
   Get: Project ID
   
2. MONGODB ATLAS (Database)
   URL: https://mongodb.com/atlas
   Purpose: Stores wallet data permanently
   Cost: FREE tier (512MB)
   Get: Connection String
   
3. COINGECKO (Price Feeds)
   URL: https://coingecko.com/api
   Purpose: Gets real-time crypto prices
   Cost: FREE tier (no key needed for basic)
   Get: API Key (optional)

NEXT STEPS:
Once you have all three, send me:
1. Infura Project ID
2. MongoDB Connection String
3. CoinGecko API Key (optional)

Then I'll start Option A: Fix the 8 critical blockers and get Dusty handling real cryptocurrency in 2-3 weeks.

Questions? Just reply.

Miles
Dark Factory AOS
"""

msg.attach(MIMEText(text, "plain"))
msg.attach(MIMEText(html, "html"))

try:
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    print("✅ API links email sent successfully!")
except Exception as e:
    print(f"❌ Failed: {e}")
