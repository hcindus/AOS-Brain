#!/usr/bin/env python3
"""
CLOSETER inbox monitor — polls the Hostinger IMAP inbox for new/unseen emails
(replies to outreach), and logs them for CLOSETER to process. Safe to run on a
cron (idempotent: deduped by Message-ID).
"""
import imaplib, email, json
from email.header import decode_header
from datetime import datetime

LOG = "/root/.openclaw/workspace/datadepot/data/closeter_inbox.json"

def decode(s):
    if not s:
        return ""
    out = []
    for data, enc in decode_header(s):
        if isinstance(data, bytes):
            out.append(data.decode(enc or "utf-8", errors="replace"))
        else:
            out.append(data)
    return "".join(out)

def main():
    creds = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            creds[k] = v
    USER = creds["HOSTINGER_SMTP_USER"]
    PASS = creds["HOSTINGER_SMTP_PASS"]
    SERVER = creds.get("HOSTINGER_IMAP_SERVER", "imap.hostinger.com")
    PORT = int(creds.get("HOSTINGER_IMAP_PORT", "993"))

    try:
        seen = json.load(open(LOG))
    except Exception:
        seen = {}

    M = imaplib.IMAP4_SSL(SERVER, PORT)
    M.login(USER, PASS)
    M.select("INBOX")

    new_count = 0
    new_list = []
    typ, data = M.search(None, "UNSEEN")
    if typ == "OK" and data[0]:
        for num in data[0].split():
            typ, msg_data = M.fetch(num, "(RFC822)")
            if typ != "OK":
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            msg_id = msg["Message-ID"] or f"<{num}@{datetime.utcnow().strftime('%Y%m%d%H%M%S')}>"
            if msg_id in seen:
                continue
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                        except Exception:
                            body = ""
                        break
            else:
                try:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
                except Exception:
                    body = ""
            seen[msg_id] = {
                "from": decode(msg["From"]),
                "subject": decode(msg["Subject"]),
                "date": msg["Date"],
                "body": body[:3000],
                "received_at": datetime.utcnow().isoformat(),
            }
            new_count += 1
            new_list.append((decode(msg["From"]), decode(msg["Subject"])))

    M.logout()

    json.dump(seen, open(LOG, "w"), indent=2)

    print(f"NEW_EMAILS={new_count}")
    for frm, subj in new_list:
        print(f"  NEW: {frm} | {subj}")

if __name__ == "__main__":
    main()
