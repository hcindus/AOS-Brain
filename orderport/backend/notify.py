"""OrderPort notifications — email (SMTP), SMS (Twilio), and ESC/POS IP printer."""
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config


def send_email(to: str, subject: str, body: str) -> dict:
    if not config.SMTP_PASS:
        return {"ok": False, "error": "SMTP not configured"}
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = config.SMTP_FROM
        msg["To"] = to
        msg.attach(MIMEText(body, "plain"))
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=15) as s:
            s.starttls()
            s.login(config.SMTP_USER, config.SMTP_PASS)
            s.sendmail(config.SMTP_FROM, [to], msg.as_string())
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def send_sms(to: str, body: str) -> dict:
    if not config.TWILIO_ACCOUNT_SID or not config.TWILIO_AUTH_TOKEN:
        return {"ok": False, "error": "Twilio not configured"}
    try:
        from twilio.rest import Client
        client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        client.messages.create(body=body, from_=config.TWILIO_FROM, to=to)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def escpos_bytes(lines: list[str]) -> bytes:
    """Build a minimal ESC/POS receipt byte stream (58mm, no external lib).

    Uses a compact ASCII rendering — enough for most Epson/Star/clone printers.
    """
    out = bytearray()
    out += b"\x1b\x40"          # initialize
    out += b"\x1b\x21\x10"      # double-height text
    for line in lines:
        # cap line to 42 chars (58mm @ default font)
        out += (line[:42] + "\n").encode("ascii", "ignore")
    out += b"\x1b\x21\x00"      # normal text
    out += b"\n\n\n\n"          # feed + cut buffer
    out += b"\x1d\x56\x42\x00"  # partial cut
    return bytes(out)


def send_printer(ip: str, port: int, lines: list[str]) -> dict:
    data = escpos_bytes(lines)
    try:
        with socket.create_connection((ip, port), timeout=8) as s:
            s.sendall(data)
        return {"ok": True, "bytes": len(data)}
    except Exception as e:
        return {"ok": False, "error": str(e)}
