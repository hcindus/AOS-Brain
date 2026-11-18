#!/usr/bin/env python3
"""
Twilio SMS helper.

send_sms(to, body, from_=None) -> message SID or None.

From number defaults to +18557899606 (our Twilio number).
Creds from aocros/secrets/twilio.env.
"""
import requests

SECRETS = "/root/.openclaw/workspace/aocros/secrets/twilio.env"
FROM_NUMBER = "+18557899606"


def _creds():
    c = {}
    try:
        for line in open(SECRETS):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                c[k] = v
    except FileNotFoundError:
        pass
    return c


def send_sms(to, body, from_=None):
    c = _creds()
    sid = c.get("TWILIO_ACCOUNT_SID", "")
    token = c.get("TWILIO_AUTH_TOKEN", "")
    from_num = from_ or c.get("TWILIO_FROM_NUMBER", FROM_NUMBER)
    if not sid or not token:
        print("sms: missing twilio creds")
        return None
    if not to:
        return None
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    try:
        r = requests.post(url, auth=(sid, token),
                          data={"To": to, "From": from_num, "Body": body}, timeout=15)
        if r.ok:
            return r.json().get("sid")
        print("sms error:", r.status_code, r.text[:300])
        return None
    except Exception as e:
        print("sms exception:", e)
        return None


if __name__ == "__main__":
    import sys
    to = sys.argv[1] if len(sys.argv) > 1 else None
    body = sys.argv[2] if len(sys.argv) > 2 else "Test SMS from Miles."
    print("SID:", send_sms(to, body))
