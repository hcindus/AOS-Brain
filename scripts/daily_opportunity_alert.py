#!/usr/bin/env python3
"""
Daily Opportunity Alert — email Captain the top real DepotChaos opportunities.

Runs qualify_real_opportunities.py to refresh the report, then emails a summary
of the top opportunities per destination (PSD supplies / Chipp / WitzEnd).

Uses the Hostinger SMTP creds (miles@myl0nr0s.cloud) already configured.
"""
import json
import os
import smtplib
import subprocess
import sys
from email.mime.text import MIMEText
from pathlib import Path

WS = Path("/root/.openclaw/workspace")
REPORT = WS / "aocros/reports/real_opportunities.json"
QUALIFY = WS / "scripts/qualify_real_opportunities.py"

TO = ["Antonio.hudnall@gmail.com"]
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
SMTP_USER = "miles@myl0nr0s.cloud"


def load_smtp_pass():
    creds = WS / ".miles_email_creds"
    if creds.exists():
        try:
            return json.loads(creds.read_text()).get("password")
        except Exception:
            pass
    # fallback to .env
    env = WS / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("HOSTINGER_SMTP_PASS="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    # 1. Refresh the report
    print("Refreshing qualification...")
    r = subprocess.run([sys.executable, str(QUALIFY)],
                       capture_output=True, text=True, cwd=str(WS))
    if r.returncode != 0:
        print("qualify failed:", r.stderr[-500:])
        return 1

    if not REPORT.exists():
        print("No report generated.")
        return 1

    data = json.loads(REPORT.read_text())
    stats = data.get("stats", {})
    top = data.get("top_opportunities", {})

    def fmt(label, entries, n=8):
        if not entries:
            return f"\n{label}: (none)\n"
        lines = [f"\n{label} ({stats.get(label.lower(), '?')} total) — top {min(n, len(entries))}:"]
        for e in entries[:n]:
            name = e.get("business_name", "?")
            city = e.get("city") or ""
            state = e.get("state") or ""
            phone = e.get("phone") or ""
            email = e.get("email") or ""
            loc = f"{city}, {state}".strip(", ")
            contact = phone or email or ""
            lines.append(f"  • {name} — {loc} — {contact}".rstrip(" -"))
        return "\n".join(lines) + "\n"

    body = []
    body.append("Daily DepotChaos Opportunity Alert\n")
    body.append(f"Real vendors: {stats.get('real_vendors')} | "
                f"Teriyaki: {stats.get('teriyaki')}\n")
    body.append(f"Qualified → PSDepot (supplies): {stats.get('psd')} | "
                f"Chipp (restaurants): {stats.get('chipp')} | "
                f"WitzEnd (bars/mocktails): {stats.get('witzend')}\n")

    body.append(fmt("WITZEND", top.get("witzend", [])))
    body.append(fmt("CHIPP", top.get("chipp", [])))
    body.append(fmt("PSD", top.get("psd", [])))

    body.append("\n— Miles 🚀")

    text = "\n".join(body)

    password = load_smtp_pass()
    if not password:
        print("No SMTP password found.")
        return 1

    msg = MIMEText(text)
    msg["Subject"] = "Daily DepotChaos Opportunities — Real Businesses"
    msg["From"] = f"Performance Supply Depot <{SMTP_USER}>"
    msg["To"] = ", ".join(TO)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, password)
        s.sendmail(SMTP_USER, TO, msg.as_string())

    print("Alert emailed to", TO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
