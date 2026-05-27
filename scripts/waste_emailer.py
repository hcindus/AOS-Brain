#!/usr/bin/env python3
"""
WASTE EMAILER v1.3 - Updated for Mortimer Only
Packages Miles' brain waste and emails it to mortimer@myl0nr0s.cloud
"""

import json
import smtplib
import ssl
import subprocess
import os
import sys
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMimeMultipart
from email.mime.application import MIMEApplication
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# LOAD ENVIRONMENT FROM SECRETS FILE
# ═══════════════════════════════════════════════════════════════════
def load_env_file(filepath):
    """Load environment variables from a .env file."""
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Try to load SMTP credentials from secrets file
env_file = '/root/.openclaw/workspace/aocros/secrets/smtp.env'
load_env_file(env_file)

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION - ONLY Mortimer receives waste now
# ═══════════════════════════════════════════════════════════════════
SMTP_HOST = os.getenv("SMTP_HOST", os.getenv("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com"))
SMTP_PORT = int(os.getenv("SMTP_PORT", os.getenv("HOSTINGER_SMTP_PORT", "587")))
SMTP_USER = os.getenv("SMTP_USER", os.getenv("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud"))
SMTP_PASS = os.getenv("SMTP_PASS", os.getenv("HOSTINGER_SMTP_PASS", ""))  # Set via env var

# UPDATED: Only Mortimer receives waste emails
WASTE_RECIPIENTS = [
    "mortimer@myl0nr0s.cloud",  # ONLY Mortimer - no more Captain or info@psdepot.com
]

# ═══════════════════════════════════════════════════════════════════
# WASTE PACKAGING
# ═══════════════════════════════════════════════════════════════════

def get_brain_status():
    """Query brain socket for status."""
    try:
        import socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect('/tmp/aos_brain.sock')
        sock.send(b'{"cmd":"status"}')
        response = sock.recv(4096).decode()
        sock.close()
        return json.loads(response)
    except Exception as e:
        return {"error": str(e), "status": "unavailable"}

def get_kidneys_status():
    """Query kidneys status via brain socket."""
    try:
        import socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect('/tmp/aos_brain.sock')
        sock.send(b'{"cmd":"kidneys"}')
        response = sock.recv(4096).decode()
        sock.close()
        return json.loads(response)
    except Exception as e:
        return {"error": str(e), "status": "unavailable"}

def package_waste():
    """Collect and package waste data from brain."""
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # Collect brain status
    brain = get_brain_status()
    kidneys = get_kidneys_status()
    
    waste_package = {
        "timestamp": timestamp,
        "source": "Miles_Brain_Kidneys",
        "type": "waste_report",
        "brain_status": brain,
        "kidneys_status": kidneys,
        "message": "Brain waste package from Miles"
    }
    
    return waste_package

# ═══════════════════════════════════════════════════════════════════
# EMAIL SENDING
# ═══════════════════════════════════════════════════════════════════

def send_waste_email(waste_data):
    """Send waste package to Mortimer only."""
    if not SMTP_PASS:
        print("ERROR: SMTP password not configured", file=sys.stderr)
        return False
    
    # Create email
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = ", ".join(WASTE_RECIPIENTS)
    msg['Subject'] = f"🗑️ Brain Waste Report - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
    
    # Body
    body = f"""Brain Waste Report
==================

Timestamp: {waste_data['timestamp']}
Source: {waste_data['source']}

Brain Status:
{json.dumps(waste_data['brain_status'], indent=2)}

Kidneys Status:
{json.dumps(waste_data['kidneys_status'], indent=2)}

---
This is an automated waste report from Miles' brain.
Only Mortimer receives these reports now.
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach JSON data
    json_attachment = MIMEApplication(json.dumps(waste_data, indent=2))
    json_attachment.add_header('Content-Disposition', 'attachment', filename='waste_report.json')
    msg.attach(json_attachment)
    
    # Send
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, WASTE_RECIPIENTS, msg.as_string())
        print(f"✅ Waste email sent to Mortimer at {datetime.now(timezone.utc).isoformat()}")
        return True
    except Exception as e:
        print(f"❌ Failed to send waste email: {e}", file=sys.stderr)
        return False

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print("🗑️ Packaging brain waste...")
    waste = package_waste()
    print(f"📦 Waste packaged at {waste['timestamp']}")
    
    print(f"📧 Sending to: {WASTE_RECIPIENTS}")
    success = send_waste_email(waste)
    
    if success:
        print("✅ Waste email complete")
    else:
        print("❌ Waste email failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
