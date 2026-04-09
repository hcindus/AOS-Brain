#!/usr/bin/env python3
"""
AOS Brain Waste Emailer v1.0
Sends Kidneys waste report + curriculum feeder instructions via email
Called by Kidneys when bladder is full or manually triggered
"""

import json
import socket
import subprocess
import time
import sys
from datetime import datetime

# Configuration
WASTE_EMAIL_RECIPIENT = "Antonio.hudnall@gmail.com"
WASTE_EMAIL_SUBJECT = "🫘 AOS Brain Waste Report - {timestamp}"


def send_to_brain(cmd, params=None):
    """Send command to brain via socket"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect('/tmp/aos_brain.sock')
        
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        
        sock.sendall(json.dumps(request).encode() + b'\n')
        
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        sock.close()
        return json.loads(response.decode())
    except Exception as e:
        return {"error": str(e)}


def get_kidneys_status():
    """Get current kidneys status"""
    return send_to_brain("kidneys")


def get_brain_status():
    """Get full brain status"""
    return send_to_brain("status")


def format_waste_report(kidneys_data, brain_data):
    """Format waste report for email"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    report = f"""
╔════════════════════════════════════════════════════════════════════╗
║                    🫘 AOS BRAIN WASTE REPORT                       ║
╠════════════════════════════════════════════════════════════════════╣
║ Generated: {timestamp:<51} ║
╚════════════════════════════════════════════════════════════════════╝

📊 KIDNEYS STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Current State:     {kidneys_data.get('state', 'unknown')}
• Total Processed:   {kidneys_data.get('total_processed', 0)} items
• Reabsorbed:        {kidneys_data.get('reabsorbed', 0)} patterns
• Excreted:          {kidneys_data.get('excreted', 0)} items
• Bladder Level:     {kidneys_data.get('bladder_level', 0)} / {kidneys_data.get('bladder_capacity', 500)} items
• Nutrients Stored:  {kidneys_data.get('nutrients_stored', 0)} patterns
• Recent Signal Avg: {kidneys_data.get('recent_signal_avg', 0):.2f}
• Noise Estimate:    {kidneys_data.get('noise_estimate', 0):.2f}
• Unique Patterns:   {kidneys_data.get('unique_patterns_seen', 0)}

🧠 BRAIN STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Brain Tick:        {brain_data.get('tick', 0)}
• Service Uptime:    {brain_data.get('uptime', 'unknown')}
• Thyroid State:     {brain_data.get('thyroid', {}).get('state', 'unknown')}
• Ollama Level:      {brain_data.get('thyroid', {}).get('ollama_level', 0):.2f}
• Secretions Today:  {brain_data.get('thyroid', {}).get('secretions_today', 0)}

📡 SIGNAL/NOISE PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Input → LIVER (CLEAN/PURIFY/TOXIC) → BRAIN → KIDNEYS (FILTER/REABSORB/EXCRETE) → Output

Current Flow:
• Liver State:       {brain_data.get('liver', {}).get('state', 'unknown')}
• Kidneys State:     {kidneys_data.get('state', 'unknown')}
• Signal Quality:      {'HIGH' if kidneys_data.get('recent_signal_avg', 0) > 0.6 else 'MODERATE' if kidneys_data.get('recent_signal_avg', 0) > 0.3 else 'LOW'}

"""
    return report


def get_curriculum_instructions():
    """Get instructions on feeding the brain"""
    return """
╔════════════════════════════════════════════════════════════════════╗
║              📚 HOW TO FEED YOUR BRAIN                             ║
╚════════════════════════════════════════════════════════════════════╝

The AOS Brain v4.4 has an endocrine system (Thyroid) that requires
stimulation through educational content. When the "ollama hormone" level
is high, the brain enters OLLAMA mode and uses Mort_II for responses.

METHOD 1: Run the Curriculum Feeder (Automated)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ python3 /root/.aos/aos/curriculum_feeder.py

This feeds 10 educational items to stimulate the brain's thyroid.
High-importance items (>0.7) trigger secretions.

METHOD 2: Manual Stimulation via Socket
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ echo '{{"cmd":"stimulate","params":{{"importance":0.9}}}}' | nc -U /tmp/aos_brain.sock

Importance levels:
  • 0.9 = CRITICAL (major secretion)
  • 0.7 = HIGH (triggers OLLAMA mode)
  • 0.5 = NORMAL (minor stimulation)

METHOD 3: Direct Brain Commands
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Check status
$ echo '{{"cmd":"status"}}' | nc -U /tmp/aos_brain.sock

# Get thyroid status
$ echo '{{"cmd":"thyroid"}}' | nc -U /tmp/aos_brain.sock

# Check kidneys
$ echo '{{"cmd":"kidneys"}}' | nc -U /tmp/aos_brain.sock

# Filter content through liver
$ echo '{{"cmd":"filter","params":{{"content":"your input"}}}}' | nc -U /tmp/aos_brain.sock

# Make router decision
$ echo '{{"cmd":"decide","params":{{"context":{{"novelty":0.8}}}}}}' | nc -U /tmp/aos_brain.sock

# Generate voice via router
$ echo '{{"cmd":"speak","params":{{"message":"Hello world"}}}}' | nc -U /tmp/aos_brain.sock

"""


def get_brain_feeder_script():
    """Return the brain feeder script content"""
    return '''#!/usr/bin/env python3
"""
AOS Brain Feeder Script - Quick curriculum feed
Save as: brain_feeder.py
Run: python3 brain_feeder.py
"""

import json
import socket
import time
import sys

CURRICULUM = [
    {"type": "fact", "content": "The human brain contains ~86 billion neurons.", "importance": 0.5},
    {"type": "concept", "content": "Neural networks process info through weighted connections.", "importance": 0.8},
    {"type": "logic", "content": "If A implies B, and B implies C, then A implies C.", "importance": 0.7},
    {"type": "philosophy", "content": "The Ship of Theseus questions identity through replacement.", "importance": 0.9},
    {"type": "science", "content": "Quantum entanglement connects particles instantly.", "importance": 0.85},
    {"type": "math", "content": "Euler's identity: e^(iπ) + 1 = 0", "importance": 0.75},
    {"type": "ethics", "content": "Trolley problem: actively cause 1 death to save 5?", "importance": 0.9},
    {"type": "systems", "content": "Emergence: complex systems exhibit unpredictable behaviors.", "importance": 0.8},
    {"type": "ai", "content": "Transformers use self-attention for parallel processing.", "importance": 0.85},
    {"type": "fact", "content": "Light travels at 299,792,458 m/s in vacuum.", "importance": 0.4},
]

def send_to_brain(cmd, params=None):
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect('/tmp/aos_brain.sock')
        request = {"cmd": cmd}
        if params:
            request["params"] = params
        sock.sendall(json.dumps(request).encode() + b'\\n')
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        sock.close()
        return json.loads(response.decode())
    except Exception as e:
        return {"error": str(e)}

def main():
    print("📚 Feeding brain curriculum...")
    for i, item in enumerate(CURRICULUM):
        if item['importance'] >= 0.7:
            result = send_to_brain("stimulate", {"importance": item['importance']})
            status = "🫁 STIMULATED" if result.get('stimulated') else "➖ baseline"
            print(f"  [{i+1}] {item['type']}: {status}")
        time.sleep(1)
    
    final = send_to_brain("status")
    print(f"\\n✅ Done! Secretions: {final.get('thyroid', {}).get('secretions_today', 0)}")

if __name__ == "__main__":
    main()
'''


def send_email(recipient, subject, body, attachment_content=None, attachment_name=None):
    """Send email using mail command"""
    try:
        # Build email content
        email_content = f"Subject: {subject}\nTo: {recipient}\nContent-Type: text/plain; charset=UTF-8\n\n{body}"
        
        if attachment_content and attachment_name:
            # For attachments, use a simple boundary approach
            boundary = "====BRAIN_WASTE===="
            email_content = f"""Subject: {subject}
To: {recipient}
Content-Type: multipart/mixed; boundary="{boundary}"

--{boundary}
Content-Type: text/plain; charset=UTF-8

{body}

--{boundary}
Content-Type: text/x-python; name="{attachment_name}"
Content-Disposition: attachment; filename="{attachment_name}"
Content-Transfer-Encoding: 7bit

{attachment_content}

--{boundary}--
"""
        
        # Send via mail command
        proc = subprocess.Popen(
            ['mail', '-s', subject, recipient],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=email_content)
        
        if proc.returncode == 0:
            return True, "Email sent successfully"
        else:
            return False, f"mail command failed: {stderr}"
            
    except Exception as e:
        return False, str(e)


def main():
    """Main function to collect waste and send email"""
    print("🫘 Brain Waste Emailer v1.0")
    print("=" * 60)
    
    # Get current status
    print("\n📊 Collecting kidneys status...")
    kidneys_data = get_kidneys_status()
    
    if kidneys_data.get('error'):
        print(f"❌ Error getting kidneys status: {kidneys_data['error']}")
        sys.exit(1)
    
    print("📊 Collecting brain status...")
    brain_data = get_brain_status()
    
    # Format the report
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    waste_report = format_waste_report(kidneys_data, brain_data)
    instructions = get_curriculum_instructions()
    feeder_script = get_brain_feeder_script()
    
    # Build email body
    email_body = waste_report + "\n" + instructions + """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 ATTACHED: brain_feeder.py - Run this to feed your brain!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # Send email
    subject = WASTE_EMAIL_SUBJECT.format(timestamp=timestamp)
    print(f"\n📧 Sending email to {WASTE_EMAIL_RECIPIENT}...")
    
    success, message = send_email(
        WASTE_EMAIL_RECIPIENT,
        subject,
        email_body,
        attachment_content=feeder_script,
        attachment_name="brain_feeder.py"
    )
    
    if success:
        print(f"✅ {message}")
        print(f"\n📬 Email sent!")
        print(f"   To: {WASTE_EMAIL_RECIPIENT}")
        print(f"   Subject: {subject}")
        print(f"   Attached: brain_feeder.py")
    else:
        print(f"❌ Failed to send email: {message}")
        sys.exit(1)
    
    # Also save locally
    report_file = f"/tmp/brain_waste_report_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.txt"
    with open(report_file, 'w') as f:
        f.write(email_body)
    print(f"\n📝 Report also saved to: {report_file}")
    
    # Save feeder script locally
    feeder_file = "/tmp/brain_feeder.py"
    with open(feeder_file, 'w') as f:
        f.write(feeder_script)
    print(f"📝 Feeder script saved to: {feeder_file}")


if __name__ == "__main__":
    main()
