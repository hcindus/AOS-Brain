#!/usr/bin/env python3
"""
Send Latin Satelital Partnership Inquiry Email
"""

import subprocess
import sys

# Email configuration
EMAIL_RECIPIENT = "info@latinsatelital.com"
EMAIL_CC = "info@psdepot.com"
EMAIL_FROM = "miles@myl0nr0s.cloud"
EMAIL_SUBJECT = "Partnership Inquiry - EngineAI PM01 Reseller & Integration Services"

# Email body
EMAIL_BODY = """Dear Latin Satelital Team,

I hope this message finds you well. My name is Miles, representing Performance Supply Depot LLC, a technology consultancy specializing in AI-driven automation and robotics integration.

We are exploring the EngineAI PM01 Humanoid Robot for integration with our proprietary agent operating system (AOS) and potential reseller opportunities in the North American market.

We noticed you have the PM01 available on your platform and would like to discuss:

1. Volume Pricing:
   - Initial pilot order: 1 unit
   - If successful: 2-3 units within 6 months
   - Scale potential: 20+ units annually

2. Technical Support:
   - Documentation and SDK access
   - Integration support for custom software layers
   - Warranty and maintenance terms

3. Partnership Terms:
   - Reseller margins for B2B customers
   - Exclusive territory considerations
   - Joint marketing opportunities

Could we schedule a brief call to discuss these points? We are ready to move quickly on a pilot unit pending favorable terms.

Looking forward to your response.

Best regards,

Miles
Performance Supply Depot LLC
info@psdepot.com
888-881-6834

---
P.S. We are particularly interested in integrating the PM01 with our voice-enabled AI agents for retail and office automation use cases. Happy to share more details on our technical architecture.
"""

def send_email():
    """Send email using mail command"""
    try:
        # Build email with headers - CC in To field
        recipients = f"{EMAIL_RECIPIENT},{EMAIL_CC}"
        email_content = f"""Subject: {EMAIL_SUBJECT}
From: {EMAIL_FROM}
Content-Type: text/plain; charset=UTF-8

{EMAIL_BODY}"""
        
        # Send via mail command
        result = subprocess.run(
            ['mail', '-s', EMAIL_SUBJECT] + recipients.split(','),
            input=email_content,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Email sent successfully!")
            print(f"   To: {EMAIL_RECIPIENT}")
            print(f"   Cc: {EMAIL_CC}")
            print(f"   From: {EMAIL_FROM}")
            print(f"   Subject: {EMAIL_SUBJECT}")
            return True
        else:
            print(f"❌ Failed to send email: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = send_email()
    sys.exit(0 if success else 1)
