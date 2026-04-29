# SMTP Configuration Guide

**Hostinger Email Setup for AOS Brain**

## Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| **SMTP Server** | `smtp.hostinger.com` | Hostinger Business Email |
| **Port** | `587` | TLS encrypted connection |
| **Username** | `Miles@myl0nr0s.cloud` | System email address |
| **Password** | (environment variable) | `HOSTINGER_SMTP_PASS` |
| **Rate Limit** | 10 emails/minute | Configured for safety |
| **Hourly Limit** | ~200 emails/hour | Hostinger business tier |

## Environment Variables

Set these in your shell or `.env` file:

```bash
export HOSTINGER_SMTP_USER="Miles@myl0nr0s.cloud"
export HOSTINGER_SMTP_PASS="your_password_here"
```

## Code Location

- **SMTP sender:** `/root/.openclaw/workspace/datadepot/smtp_sender.py`
- **Queue directory:** `/root/.openclaw/workspace/datadepot/queue/`
- **Pending:** `pending_emails.json`
- **Sent:** `sent_emails.json`
- **Failed:** `failed_emails.json`

## Usage

The `HostingerEmailSender` class handles:
- Queuing emails with rate limiting
- TLS-encrypted SMTP transmission
- Automatic retry on failure
- JSON-based queue management

## Example

```python
from datadepot.smtp_sender import HostingerEmailSender

sender = HostingerEmailSender()
email_data = {
    'to_email': 'customer@example.com',
    'from': 'Miles@myl0nr0s.cloud',
    'subject': 'Hello from Miles',
    'text_body': 'Plain text version',
    'html_body': '<p>HTML version</p>'
}
sender.send_email(email_data)
```

---

*Last updated: 2026-04-29*
