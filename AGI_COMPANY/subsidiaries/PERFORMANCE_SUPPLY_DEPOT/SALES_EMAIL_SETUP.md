# Sales Email — Setup & Process

**Account:** Sales Performance Supply Depot — `performancesupplydepotsales@gmail.com`
**Purpose:** CLOSETER + sales department (outreach + order-form login)
**BCC:** every outgoing email BCCs `info@psdepot.com`

---

## Credentials (stored in `aocros/secrets/sales_email.env`, gitignored)

| Field | Value |
|---|---|
| Login email | performancesupplydepotsales@gmail.com |
| Login password | (login password) |
| App password (SMTP/IMAP) | *(stored in vault — `aocros/secrets/sales_email.env`)* |

- **Login password** = used for *web sign-in* (browser), and for CLOSETER's Google form login.
- **App password** = used for *programmatic* email (SMTP send / IMAP read). Gmail requires it; the login password won't work for scripts.

---

## How the app password was created (for future reference)

1. Turn on 2-Step Verification: `myaccount.google.com/security` → "How you sign in to Google" → "2-Step Verification" → Get started (add phone).
2. Create app password: `myaccount.google.com/apppasswords` → name "PSD sales" → Create → copy the 16 chars.

---

## SMTP send (as the sales account)

- Host: `smtp.gmail.com:587` (STARTTLS)
- Login: `performancesupplydepotsales@gmail.com` + **app password**
- From: `Sales Performance Supply Depot <performancesupplydepotsales@gmail.com>`
- BCC: `info@psdepot.com` (always)

## IMAP read (the sales inbox)

- Host: `imap.gmail.com:993` (SSL)
- Login: same email + app password

---

## Order form (CLOSETER)

- The Google order form requires **sign-in** ("Limit to 1 response" is ON).
- CLOSETER signs in as `performancesupplydepotsales@gmail.com` (web login) → fills the form → Apps Script fires (vendor email + invoice + margin).
- Blocker: Google blocks *automated* sign-in (anti-bot). Options: (a) one manual sign-in to reuse the session, or (b) uncheck "Limit to 1 response" (keeps "Collect email addresses" for the email + accountability).

---

## Future role-based inboxes (convention)

`orders@…`, `support@…`, etc. — one account per function, same app-password pattern.
