#!/usr/bin/env python3
"""
WASTE EMAILER v1.1
Packages Miles' brain waste and emails it to configured recipients.
Runs every time kidneys flush (or on cron schedule).
"""

import json
import smtplib
import ssl
import subprocess
import os
import sys
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION - Multiple Recipients
# ═══════════════════════════════════════════════════════════════════
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.hostinger.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "miles@myl0nr0s.cloud")
SMTP_PASS = os.getenv("SMTP_PASS", "")  # Set via env var

# Multiple waste recipients
WASTE_RECIPIENTS = [
    "antonio.hudnall@gmail.com",  # Captain
    "mortimer@myl0nr0s.cloud",    # Mortimer
]

# ═══════════════════════════════════════════════════════════════════
# WASTE COLLECTION
# ═══════════════════════════════════════════════════════════════════

def collect_waste_from_kidneys():
    """Pull waste data from the running brain via Mission Control API."""
    import urllib.request
    
    try:
        # Query the brain API
        req = urllib.request.Request("http://localhost:8080/api/brain")
        req.add_header("Accept", "application/json")
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            
            # Extract waste-relevant data
            waste_package = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "Miles_Brain_v4.4",
                "kidneys": data.get("kidneys", {}),
                "qmd": data.get("qmd", {}),
                "router": data.get("router", {}),
                "thyroid": data.get("thyroid", {}),
                "consciousness": data.get("consciousness", {}),
                "cortex": data.get("cortex", {}),
                "tracray": data.get("tracray", {}),
                "liver": data.get("liver", {}),
                "signal_quality": data.get("signal_quality_20avg", 0)
            }
            return waste_package
            
    except Exception as e:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e),
            "source": "Miles_Brain_v4.4",
            "status": "collection_failed"
        }

def collect_from_sespool():
    """Collect any queued sespool waste."""
    sespool_dir = Path("/root/.openclaw/workspace/memory/sespool")
    waste_items = []
    
    if sespool_dir.exists():
        for waste_type in ["periodic-waste", "urban-waste", "webster-waste", "thesaurus-waste"]:
            waste_dir = sespool_dir / waste_type
            if waste_dir.exists():
                for waste_file in waste_dir.glob("*.json"):
                    if ".transferred." not in waste_file.name:
                        try:
                            with open(waste_file) as f:
                                waste_items.append(json.load(f))
                                # Mark as collected
                                waste_file.rename(waste_file.with_suffix(".collected.json"))
                        except Exception as e:
                            pass
    
    return waste_items

# ═══════════════════════════════════════════════════════════════════
# EMAIL SENDING
# ═══════════════════════════════════════════════════════════════════

def send_waste_email(waste_data, sespool_items=None):
    """Send waste package to all configured recipients."""
    
    results = {}
    
    for recipient in WASTE_RECIPIENTS:
        result = _send_single_waste_email(waste_data, sespool_items, recipient)
        results[recipient] = result
    
    # Return True only if ALL succeeded
    return all(results.values()), results

def _send_single_waste_email(waste_data, sespool_items, recipient):
    """Send waste package to a single recipient."""
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🗑️ Miles Brain Waste Drop - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC"
    msg["From"] = f"Miles Waste System <{SMTP_USER}>"
    msg["To"] = recipient
    msg["Bcc"] = "info@psdepot.com"  # BCC info@psdepot.com on all waste emails
    
    # Plain text summary
    kidneys = waste_data.get("kidneys", {})
    text_body = f"""
BRAIN WASTE REPORT
==================
Timestamp: {waste_data.get('timestamp')}
Source: {waste_data.get('source')}
Signal Quality: {waste_data.get('signal_quality', 'N/A')}

KIDNEYS STATUS:
- Bladder Level: {kidneys.get('bladder_level', 'N/A')} / {kidneys.get('bladder_capacity', 'N/A')}
- Total Processed: {kidneys.get('total_processed', 'N/A')}
- Noise Estimate: {kidneys.get('noise_estimate', 'N/A')}
- Unique Patterns: {kidneys.get('unique_patterns_seen', 'N/A')}
- State: {kidneys.get('state', 'N/A')}

QMD CYCLES: {waste_data.get('qmd', {}).get('total_cycles', 'N/A')}
ROUTER CALLS: {waste_data.get('router', {}).get('stats', {}).get('decision', {}).get('calls', 'N/A')}
THYROID: {waste_data.get('thyroid', {}).get('state', 'N/A')} ({waste_data.get('thyroid', {}).get('secretions_today', 'N/A')} secretions)

Full JSON attached. Feed this to Mortimer's brain.
    """.strip()
    
    msg.attach(MIMEText(text_body, "plain"))
    
    # Attach full waste JSON
    waste_json = json.dumps(waste_data, indent=2)
    attachment = MIMEApplication(waste_json.encode())
    attachment.add_header("Content-Disposition", "attachment", filename="miles_waste.json")
    msg.attach(attachment)
    
    # Attach sespool items if any
    if sespool_items:
        sespool_json = json.dumps({"sespool_batch": sespool_items}, indent=2)
        sespool_attachment = MIMEApplication(sespool_json.encode())
        sespool_attachment.add_header("Content-Disposition", "attachment", filename="sespool_waste.json")
        msg.attach(sespool_attachment)
    
    # Send email (Hostinger: 465=SSL, 587=STARTTLS)
    try:
        context = ssl.create_default_context()
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        
        print(f"✅ Waste emailed to {recipient} at {datetime.now(timezone.utc).isoformat()}")
        return True
        
    except Exception as e:
        print(f"❌ Email to {recipient} failed: {e}")
        # Save to retry queue
        retry_dir = Path("/var/log/aos/email_retry")
        retry_dir.mkdir(parents=True, exist_ok=True)
        safe_recipient = recipient.replace('@', '_at_').replace('.', '_')
        retry_file = retry_dir / f"waste_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{safe_recipient}.json"
        with open(retry_file, 'w') as f:
            json.dump(waste_data, f)
        print(f"   Saved to retry queue: {retry_file}")
        return False

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("MILES WASTE EMAILER v1.1")
    print(f"Recipients: {', '.join(WASTE_RECIPIENTS)}")
    print("=" * 60)
    
    # Collect waste
    print("📊 Collecting waste from kidneys...")
    waste = collect_waste_from_kidneys()
    
    print("🗑️  Checking sespool backlog...")
    sespool = collect_from_sespool()
    print(f"   Found {len(sespool)} sespool items")
    
    # Check if we have meaningful waste to send
    kidneys = waste.get("kidneys", {})
    bladder_level = kidneys.get("bladder_level", 0)
    bladder_capacity = kidneys.get("bladder_capacity", 500)
    
    # Send if bladder > 50% OR sespool has items OR force flag
    if bladder_level > (bladder_capacity * 0.5) or sespool or "--force" in sys.argv:
        print(f"📧 Sending waste email to {len(WASTE_RECIPIENTS)} recipients...")
        print(f"   Bladder: {bladder_level}/{bladder_capacity} ({bladder_level/bladder_capacity*100:.1f}%)")
        success, results = send_waste_email(waste, sespool if sespool else None)
        
        if success:
            print(f"✅ Waste successfully sent to all {len(WASTE_RECIPIENTS)} recipients")
        else:
            failed = [r for r, ok in results.items() if not ok]
            print(f"⚠️  Failed for: {', '.join(failed)}")
    else:
        print(f"🔄 Bladder at {bladder_level}/{bladder_capacity} — below threshold, skipping email")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
