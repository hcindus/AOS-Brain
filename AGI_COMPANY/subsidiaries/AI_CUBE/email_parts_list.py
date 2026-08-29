#!/usr/bin/env python3
import os, re, smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load SMTP creds from .env
env_path = "/root/.openclaw/workspace/.env"
creds = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip()

smtp_server = creds.get("HOSTINGER_SMTP_SERVER", "smtp.hostinger.com")
smtp_port = int(creds.get("HOSTINGER_SMTP_PORT", "587"))
smtp_user = creds.get("HOSTINGER_SMTP_USER", "miles@myl0nr0s.cloud")
smtp_pass = creds.get("HOSTINGER_SMTP_PASS", "")

TO = "Antonio.hudnall@gmail.com"
FROM = smtp_user
SUBJECT = "AI Cube — Pi 5 Parts List (Amazon links)"

# Build the links list
items = [
    ("CORE — brain box", [
        ("Raspberry Pi 5 16GB", "https://www.amazon.com/s?k=raspberry+pi+5+16gb", "$120"),
        ("Geekworm X735 UPS HAT", "https://www.amazon.com/s?k=geekworm+x735+ups+hat", "$33"),
        ("128GB NVMe SSD + M.2 HAT", "https://www.amazon.com/s?k=raspberry+pi+5+nvme+m.2+hat", "$40"),
    ]),
    ("ARM — grabber", [
        ("6-DOF metal arm kit", "https://www.amazon.com/s?k=6dof+metal+robotic+arm+kit+servo", "$60"),
        ("PCA9685 16-ch PWM driver", "https://www.amazon.com/s?k=pca9685+16+channel+pwm+servo+driver", "$13"),
        ("2x genuine MG996R servos", "https://www.amazon.com/s?k=mg996r+servo", "$24"),
    ]),
    ("SENSORS — eyes & ears", [
        ("VL53L1X ToF distance", "https://www.amazon.com/s?k=vl53l1x+time+of+flight", "$13"),
        ("HC-SR04 ultrasonic", "https://www.amazon.com/s?k=hc-sr04+ultrasonic+sensor", "$4"),
        ("BNO055 IMU (9-DOF)", "https://www.amazon.com/s?k=bno055+imu+9+dof", "$20"),
        ("Pi Camera Module 3", "https://www.amazon.com/s?k=raspberry+pi+camera+module+3", "$28"),
        ("ReSpeaker 2-Mic HAT", "https://www.amazon.com/s?k=respeaker+2+mic+hat", "$25"),
        ("MAX98357A amp + speaker", "https://www.amazon.com/s?k=max98357a+i2s+amplifier", "$13"),
    ]),
    ("MOBILITY", [
        ("DC gear motors + DRV8833", "https://www.amazon.com/s?k=dc+gear+motor+drv8833+driver", "$28"),
        ("Tank tracks + chassis", "https://www.amazon.com/s?k=robot+tank+track+chassis", "$25"),
        ("Rotary encoders", "https://www.amazon.com/s?k=rotary+encoder+motor+wheel", "$12"),
    ]),
    ("POWER", [
        ("LiFePO4 / 18650 pack", "https://www.amazon.com/s?k=lifepo4+battery+pack+12v", "$40"),
    ]),
    ("MISC", [
        ("Jumper wires + breadboard", "https://www.amazon.com/s?k=jumper+wires+breadboard+kit", "$18"),
        ("Make: Robotic Arms (book)", "https://www.amazon.com/s?k=make+robotic+arms+matthew+eaton", "$25"),
    ]),
]

# HTML body
rows = ""
for section, entries in items:
    rows += f'<tr><td colspan="3" style="background:#1a1a2e;color:#fff;font-weight:bold;padding:8px">{section}</td></tr>'
    for name, url, price in entries:
        rows += (f'<tr><td style="padding:6px"><a href="{url}">{name}</a></td>'
                 f'<td style="padding:6px;color:#888">amazon search</td>'
                 f'<td style="padding:6px;text-align:right">{price}</td></tr>')

html = f"""<html><body style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;color:#eee;background:#12121a;padding:20px">
<h2 style="color:#58a6ff">AI Cube — Pi 5 Parts List</h2>
<p style="color:#aaa">Links are Amazon <i>search</i> links (land on the exact category). Exact ASINs rotate — pick the top-reviewed Prime listing on each page. Total ~$530–580.</p>
<table style="border-collapse:collapse;width:100%;max-width:680px" cellspacing="0">
{rows}
</table>
<p style="color:#f85149;margin-top:20px"><b>Don't cheap out on:</b> high-endurance storage + genuine MG996R servos (the two things that fail/corrupt first).</p>
<p style="color:#888;font-size:12px">— Miles · AI Cube spec · AGI_COMPANY/subsidiaries/AI_CUBE/MISSION.md</p>
</body></html>"""

text = "AI CUBE — Pi 5 PARTS LIST\n\n"
for section, entries in items:
    text += f"\n[{section}]\n"
    for name, url, price in entries:
        text += f"  - {name}  {price}  ->  {url}\n"
text += "\nTotal ~$530-580. Don't cheap out on storage + servos.\n"

msg = MIMEMultipart("alternative")
msg["Subject"] = SUBJECT
msg["From"] = f"Miles <{FROM}>"
msg["To"] = TO
msg.attach(MIMEText(text, "plain"))
msg.attach(MIMEText(html, "html"))

try:
    s = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
    s.starttls()
    s.login(smtp_user, smtp_pass)
    s.sendmail(FROM, [TO], msg.as_string())
    s.quit()
    print("EMAIL_SENT_OK to", TO)
except Exception as e:
    print("EMAIL_SEND_FAILED:", repr(e))
    sys.exit(1)
