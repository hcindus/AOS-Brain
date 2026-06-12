#!/usr/bin/env python3
"""
Email Priority Router
Routes emails to appropriate SMTP relay based on content/priority
"""

import sys
import re
from pathlib import Path

CRITICAL_PATTERNS = [
    r'lead[s]?.*generated',
    r'brain.*(down|alert|error)',
    r'.*scraper.*(failed|error)',
    r'security.*alert',
    r'.*urgent.*',
    r'.*critical.*',
]

BULK_PATTERNS = [
    r'cron.*daemon',
    r'daily.*report',
    r'status.*check',
    r'backup.*complete',
]

def classify_email(subject, body=""):
    """Classify email priority based on content"""
    text = f"{subject} {body}".lower()
    
    for pattern in CRITICAL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "CRITICAL", "sendgrid"
    
    for pattern in BULK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "BULK", "hostinger"
    
    # Default to SendGrid for unknown (better delivery)
    return "NORMAL", "sendgrid"

if __name__ == "__main__":
    # Test classification
    test_emails = [
        ("Lead Generated: 500 new leads today", "CRITICAL"),
        ("Brain Health Alert: WebSocket down", "CRITICAL"),
        ("Cron Daemon daily status", "BULK"),
        ("CA SOS Scraper failed", "CRITICAL"),
        ("Daily backup complete", "BULK"),
    ]
    
    print("Email Classification Test:")
    for subject, expected in test_emails:
        priority, relay = classify_email(subject)
        status = "✅" if priority == expected else "❌"
        print(f"{status} '{subject[:40]}...' → {priority} ({relay})")
