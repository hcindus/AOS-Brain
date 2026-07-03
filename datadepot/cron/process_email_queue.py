#!/usr/bin/env python3
"""
Cron script to process DepotChaos email queue via SendGrid
Run every 15 minutes for ~96 emails/day (SendGrid free limit: 100/day)
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/datadepot/web')

from sendgrid_sender import process_email_queue, get_status

def main():
    # Check current status
    status = get_status()
    
    print(f"SendGrid Status:")
    print(f"  API Key Configured: {status.get('api_key_configured', False)}")
    print(f"  Pending Emails: {status.get('total_pending', 0)}")
    print(f"  Can Send Now: {status.get('can_send_now', False)}")
    
    if status.get('wait_seconds', 0) > 0:
        print(f"  Wait Time: {status['wait_seconds']}s")
    
    if not status.get('api_key_configured'):
        print("ERROR: SENDGRID_API_KEY not configured")
        sys.exit(1)
    
    if status.get('total_pending', 0) == 0:
        print("No emails to send")
        sys.exit(0)
    
    if not status.get('can_send_now', False):
        print(f"Rate limited - waiting {status.get('wait_seconds', 0)}s")
        sys.exit(0)
    
    # Process one email
    result = process_email_queue(max_emails=1)
    
    if result.get('success'):
        print(f"Success: {result.get('sent', 0)} sent, {result.get('failed', 0)} failed")
        print(f"Remaining in queue: {result.get('remaining', 0)}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
        sys.exit(1)

if __name__ == '__main__':
    main()
