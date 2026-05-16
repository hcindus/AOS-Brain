#!/usr/bin/env python3
"""
Daily DNS Reminder Emailer
Sends reminder about pending DNS tasks for pos.psdepot.com
"""

import subprocess
import sys
from datetime import datetime

RECIPIENT = "Antonio.Hudnall@gmail.com"

def send_email(subject, body):
    """Send email using mail command"""
    try:
        proc = subprocess.Popen(
            ['mail', '-s', subject, RECIPIENT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=body)
        
        if proc.returncode == 0:
            return True, "Email sent"
        else:
            return False, f"mail command failed: {stderr}"
    except Exception as e:
        return False, str(e)

def main():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    
    subject = f"🔧 REMINDER: Add DNS A Record for pos.psdepot.com - {today}"
    
    body = f"""Hi Captain,

This is your daily reminder about the pending DNS record for pos.psdepot.com.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 ACTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNS RECORD TO ADD:
  Type:  A
  Name:  pos
  Value: 31.97.6.40
  TTL:   3600

WHERE TO ADD IT:
  • Log into your domain registrar (psdepot.com provider)
  • Navigate to DNS Management / DNS Zone Editor
  • Add the A record above
  • Wait 5-10 minutes for propagation

WHEN DONE, RUN:
  sudo certbot --nginx -d pos.psdepot.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CURRENT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ReggieStarr API: Running on port 5001
✅ Nginx config: Deployed at /etc/nginx/sites-enabled/pos.psdepot.com
⚠️  DNS record: Waiting for A record
⏳ SSL certificate: Will issue after DNS propagates

ACCESS LINKS:
  • HTTP (temporary): http://31.97.6.40:5001
  • HTTPS (after cert): https://pos.psdepot.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 RELATED FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • docs/DNS_REMINDER_pos.psdepot.com.md
  • config/nginx/pos.psdepot.com
  • scripts/add_pos_dns_record.sh

Reply STOP when done to unsubscribe from these reminders.

Cheers,
Miles
AOS Brain v4.5
"""
    
    success, msg = send_email(subject, body)
    if success:
        print(f"✅ Daily DNS reminder sent to {RECIPIENT}")
        return 0
    else:
        print(f"❌ Failed to send: {msg}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
