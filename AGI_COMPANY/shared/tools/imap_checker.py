#!/usr/bin/env python3
"""
📧 IMAP EMAIL CHECKER
Check Miles and Mortimer email accounts
Date: 2026-02-22
"""

import imaplib
import ssl
import sys
from datetime import datetime

# Email configuration
EMAIL_ACCOUNTS = [
    {
        'name': 'Miles',
        'address': 'miles@myl0nr0s.cloud',
        'password': 'Myl0n.R0s',
        'server': 'mail.myl0nr0s.cloud'
    },
    {
        'name': 'Mortimer',
        'address': 'mortimer@myl0nr0s.cloud',
        'password': 'Myl0n.r0s',
        'server': 'mail.myl0nr0s.cloud'
    }
]

def check_imap(account):
    """Check IMAP account for new messages"""
    try:
        print(f"\n🔍 Checking {account['name']} ({account['address']})...")
        
        # Create SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Connect to IMAP server
        imap = imaplib.IMAP4_SSL(account['server'], ssl_context=context)
        
        # Login
        imap.login(account['address'], account['password'])
        
        # Select inbox
        status, _ = imap.select('INBOX')
        if status != 'OK':
            print(f"  ❌ Failed to select inbox")
            return False
        
        # Get message count
        status, messages = imap.search(None, 'ALL')
        if status != 'OK':
            print(f"  ❌ Failed to search messages")
            return False
        
        msg_count = len(messages[0].split()) if messages[0] else 0
        
        # Check for unseen messages
        status, unseen = imap.search(None, 'UNSEEN')
        unseen_count = len(unseen[0].split()) if unseen[0] else 0
        
        # Get quota info if available
        try:
            status, quota = imap.quota('INBOX')
            quota_info = f"Quota: {quota}"
        except:
            quota_info = "Quota: N/A"
        
        # Close and logout
        imap.close()
        imap.logout()
        
        print(f"  ✅ Connected successfully!")
        print(f"  📨 Total messages: {msg_count}")
        print(f"  🔴 Unread messages: {unseen_count}")
        print(f"  📊 {quota_info}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("📧 FLEET IMAP EMAIL CHECK")
    print("=" * 60)
    print(f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    results = []
    for account in EMAIL_ACCOUNTS:
        success = check_imap(account)
        results.append((account['name'], success))
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ OK" if success else "❌ FAILED"
        print(f"  {name}: {status}")
    
    # Return exit code based on success
    if all(r[1] for r in results):
        print("\n🎉 All accounts accessible!")
        return 0
    else:
        print("\n⚠️  Some accounts failed (check credentials/server)")
        return 1

if __name__ == '__main__':
    sys.exit(main())
