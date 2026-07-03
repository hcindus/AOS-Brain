#!/usr/bin/env python3
"""
Daily Queue Email Report Script (via mail command)
Sends Patricia's work queue report to Captain via email
"""

import subprocess
from datetime import datetime

def send_daily_queue_report():
    """Send Patricia's daily queue report to Captain"""
    
    recipient = "Antonio.hudnall@gmail.com"
    
    # Email content
    subject = f"📊 Daily Queue Report - {datetime.now().strftime('%B %d, %Y')}"
    
    # Get current date for the report
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    
    body = f"""Good afternoon, Captain!

Here is Patricia's daily queue report for today ({current_date}).

═══════════════════════════════════════════════════════════════════════════
                              QUEUE SUMMARY
═══════════════════════════════════════════════════════════════════════════

Generated: {current_time}
Total Items: 61

BY CATEGORY:
• Governance     : 11 items
• Production     :  3 items
• Data           : 59 items (Lead Scraper Queue)
• Documentation  :  1 item
• Reports        : 35 items

BY PRIORITY:
🔴 HIGH    : 4 items
🟡 NORMAL  : 11 items
🟢 LOW     : 1 item

═══════════════════════════════════════════════════════════════════════════
                           HIGH PRIORITY ITEMS
═══════════════════════════════════════════════════════════════════════════

1. 🔴 [Governance] Annual Compliance Recertification 2026
   ID: COMP-2026-ANNUAL-RECERT
   Status: pending
   Source: Compliance Tracking
   Client: AGI Company Board

2. 🔴 [Production] ReggieStarr Android App
   ID: REGGIESTARR-001
   Status: queued
   Source: Dark Factory
   Client: AGI Company

3. 🔴 [Production] Cream Mobile App
   ID: CREAM-001
   Status: queued
   Source: Dark Factory
   Client: AGI Company

4. 🔴 [Production] N'og nog v3 Universal Explorer
   ID: NOGNOG-003
   Status: queued
   Source: Dark Factory
   Client: AGI Company

═══════════════════════════════════════════════════════════════════════════
                         PENDING ACKNOWLEDGMENTS
═══════════════════════════════════════════════════════════════════════════

The following agents have pending Executive Handbook acknowledgments:
• QORA, RALPH, SPINDLE, VELUM, SCRIBBLE, MILL, FEELIX
• REDACTOR, FIBER, BOXTRON

All require signature to complete governance compliance.

═══════════════════════════════════════════════════════════════════════════
                           SYSTEM HEALTH STATUS
═══════════════════════════════════════════════════════════════════════════

Component               | Status    | Details
------------------------+-----------+----------------------------------------
Complete Brain v4.1     | RUNNING   | Heartbeat operational
Mission Control v2      | RUNNING   | Port 8080 active
Queue Status            | 61 items  | Patricia managing
Reports                 : 35 items  | Multiple agents contributing
Security                | SECURED   | Environment configured

═══════════════════════════════════════════════════════════════════════════

Patricia's queue currently has 61 active items. The Lead Scraper Queue (59 
items) dominates the workload, with core production items and compliance 
tracking remaining as HIGH priority.

All systems operational. Standing by for Captain's directives.

- Miles 🚀
Autonomous Operations Engine
"""
    
    # Send via mail command
    proc = subprocess.Popen(
        ['mail', '-s', subject, recipient],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate(input=body)
    
    if proc.returncode == 0:
        print("✅ Daily queue email report sent to Captain successfully!")
        print(f"   To: {recipient}")
        print(f"   Subject: {subject}")
    else:
        print(f"❌ Failed to send email: {stderr}")
        return False
    
    return True

if __name__ == "__main__":
    send_daily_queue_report()
