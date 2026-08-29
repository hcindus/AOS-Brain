#!/usr/bin/env python3
import smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
SUBJECT = "AI Cube — Pi 5 Parts List (with 'look for' notes)"

# (name, url, price, look_for)
items = [
    ("CORE — brain box", [
        ("Raspberry Pi 5 16GB", "https://www.amazon.com/s?k=raspberry+pi+5+16gb", "$120",
         "genuine (not clone); add official 27W USB-C PSU + active cooler"),
        ("Geekworm X735 UPS HAT", "https://www.amazon.com/s?k=geekworm+x735+ups+hat", "$33",
         "Pi 5 variant, safe-shutdown script, battery input"),
        ("128GB NVMe + M.2 HAT", "https://www.amazon.com/s?k=raspberry+pi+5+nvme+m.2+hat", "$40",
         "Pi 5 M.2 HAT + Gen3 NVMe 2280 (Gen4 downclocks)"),
    ]),
    ("ARM — grabber", [
        ("6-DOF metal arm kit", "https://www.amazon.com/s?k=6dof+metal+robotic+arm+kit+servo", "$60",
         "ALUMINUM frame (not acrylic), 6 servos + gripper"),
        ("PCA9685 16-ch PWM", "https://www.amazon.com/s?k=pca9685+16+channel+pwm+servo+driver", "$13",
         "16-ch, I2C addr selectable, 3.3V logic"),
        ("2x MG996R servos", "https://www.amazon.com/s?k=mg996r+servo", "$24",
         "METAL GEARS (plastic strips in days), high-torque"),
    ]),
    ("SENSORS — eyes & ears", [
        ("VL53L1X ToF", "https://www.amazon.com/s?k=vl53l1x+time+of+flight", "$13",
         "I2C breakout w/ voltage regulator, ~4m range"),
        ("HC-SR04 ultrasonic", "https://www.amazon.com/s?k=hc-sr04+ultrasonic+sensor", "$4",
         "5V — pair w/ voltage divider for Pi 3.3V logic"),
        ("BNO055 IMU", "https://www.amazon.com/s?k=bno055+imu+9+dof", "$20",
         "9-DOF w/ onboard fusion, I2C, 3.3V"),
        ("Pi Camera Module 3", "https://www.amazon.com/s?k=raspberry+pi+camera+module+3", "$28",
         "genuine, 12MP autofocus, ribbon included"),
        ("ReSpeaker 2-Mic HAT", "https://www.amazon.com/s?k=respeaker+2+mic+hat", "$25",
         "Pi 5 header, 2 mics, built-in DAC"),
        ("MAX98357A + speaker", "https://www.amazon.com/s?k=max98357a+i2s+amplifier", "$13",
         "I2S input, 3.3V logic, 3W speaker"),
    ]),
    ("MOBILITY", [
        ("DC motors + DRV8833", "https://www.amazon.com/s?k=dc+gear+motor+drv8833+driver", "$28",
         "motors WITH encoders, DRV8833 dual H-bridge, 6-12V"),
        ("Tank tracks + chassis", "https://www.amazon.com/s?k=robot+tank+track+chassis", "$25",
         "matching track+sprocket kit, sturdy frame"),
        ("Rotary encoders", "https://www.amazon.com/s?k=rotary+encoder+motor+wheel", "$12",
         "quadrature, shaft matches motor"),
    ]),
    ("POWER", [
        ("LiFePO4 / 18650 pack", "https://www.amazon.com/s?k=lifepo4+battery+pack+12v", "$40",
         "PROTECTED cells / BMS, voltage matches X735 input"),
    ]),
    ("MISC", [
        ("Jumper wires + breadboard", "https://www.amazon.com/s?k=jumper+wires+breadboard+kit", "$18",
         "Dupont male+female, solid-core, 20-40cm"),
        ("Make: Robotic Arms (book)", "https://www.amazon.com/s?k=make+robotic+arms+matthew+eaton", "$25",
         "Matthew Eaton edition (inverse-kinematics chapters)"),
    ]),
]

rows = ""
text = "AI CUBE — Pi 5 PARTS LIST (with 'look for' notes)\n\n"
for section, entries in items:
    rows += f'<tr><td colspan="2" style="background:#1a1a2e;color:#fff;font-weight:bold;padding:8px">{section}</td></tr>'
    text += f"\n[{section}]\n"
    for name, url, price, note in entries:
        rows += (f'<tr><td style="padding:6px"><a href="{url}">{name}</a> '
                 f'<span style="color:#888">({price})</span><br>'
                 f'<span style="color:#f0a500;font-size:12px">look for: {note}</span></td></tr>')
        text += f"  - {name}  {price}\n      look for: {note}\n      {url}\n"

html = f"""<html><body style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;color:#eee;background:#12121a;padding:20px">
<h2 style="color:#58a6ff">AI Cube — Pi 5 Parts List</h2>
<p style="color:#aaa">Amazon <i>search</i> links (land on exact category). Total ~$530–580.</p>
<table style="border-collapse:collapse;width:100%;max-width:720px" cellspacing="0">{rows}</table>
<p style="color:#f85149;margin-top:20px"><b>Don't cheap out on:</b> high-endurance storage + <b>metal-gear</b> servos.</p>
<p style="color:#888;font-size:12px">— Miles · AGI_COMPANY/subsidiaries/AI_CUBE</p>
</body></html>"""

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
