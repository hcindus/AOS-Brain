#!/usr/bin/env python3
"""
EMAIL PROCESSOR - Urgent + Seeking Alpha
"""

import imaplib
import ssl
from datetime import datetime
import re

EMAIL = "miles@myl0nr0s.cloud"
PASSWORD = "Myl0n.R0s"
SERVER = "imap.hostinger.com"

URGENT_KEYWORDS = ["urgent", "critical", "asap", "immediate", "emergency"]

def connect():
    ctx = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(SERVER, 993, ssl_context=ctx)
    imap.login(EMAIL, PASSWORD)
    return imap

def process():
    imap = connect()
    imap.select("INBOX")
    
    urgent = []
    insights = []
    
    _, data = imap.search(None, "ALL")
    ids = data[0].split()[-50:]
    
    for eid in reversed(ids):
        _, msg = imap.fetch(eid, "(RFC822.HEADER)")
        hdr = msg[0][1].decode("utf-8", errors="ignore")
        
        subj = ""
        frm = ""
        
        for line in hdr.split("\n"):
            if line.startswith("Subject:"):
                subj = line[8:].strip()
            elif line.startswith("From:"):
                frm = line[5:].strip()
        
        # Check urgent
        if any(k in subj.lower() for k in URGENT_KEYWORDS):
            urgent.append({"from": frm, "subject": subj})
        
        # Seeking Alpha
        if "seekingalpha" in frm.lower():
            m = re.search(r"([A-Z]{2,5}):", subj)
            if m:
                ticker = m.group(1)
                action = "BUY" if "buy" in subj.lower() else "SELL" if "sell" in subj.lower() else "NEWS"
                insights.append({"ticker": ticker, "action": action})
    
    imap.close()
    imap.logout()
    
    # Report
    print("=" * 70)
    print("EMAIL REPORT", datetime.now().strftime("%Y-%m-%d %H:%M UTC"))
    print("=" * 70)
    print()
    
    if urgent:
        print("URGENT:")
        for u in urgent[:5]:
            print(f"  {u['from'][:30]}: {u['subject'][:50]}")
    else:
        print("No urgent emails")
    print()
    
    if insights:
        print("SEEKING ALPHA:")
        for i in insights[:10]:
            print(f"  {i['ticker']}: {i['action']}")
    else:
        print("No trading insights")
    print()

if __name__ == "__main__":
    process()
