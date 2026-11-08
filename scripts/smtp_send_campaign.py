#!/usr/bin/env python3
"""
Send the DepotChaos email_queue via Hostinger SMTP (verified working path).

The SendGrid path is placeholder (no key). This sender reads the `email_queue`
table in unified.db and delivers `ready` emails whose scheduled_at <= now.

Usage:
  python3 smtp_send_campaign.py --reschedule   # reset sequence timing (day1 now, day3 +3d, day7 +7d)
  python3 smtp_send_campaign.py --send         # send all due 'ready' emails
  python3 smtp_send_campaign.py --status       # show queue state
"""
import argparse
import os
import re
import smtplib
import sqlite3
import sys
import time
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

DB = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
SMTP_USER = "miles@myl0nr0s.cloud"
SMTP_PASS = os.getenv("HOSTINGER_SMTP_PASS", "Myl0n.R0s")
FROM_EMAIL = "miles@myl0nr0s.cloud"
FROM_NAME = "Miles - Performance Supply Depot"

# Three-step copy, keyed by sequence_day. {first} = contact first name,
# {business} = business name.
BODIES = {
    1: """Hi {first},

I'll keep this short. I work with hospitality teams across California, and the one number most operators can't see is their pour cost.

Over-pouring, free pours, and breakage quietly eat 15-30% of liquor margin. Most spots only catch it at month-end variance — and by then the money's gone.

We supply the pour-control tools and POS supplies that make it measurable, so you catch the leak in a week instead of a quarter.

Worth a quick look?

- Miles
Performance Supply Depot
""",
    3: """Hi {first},

Quick question: do you know offhand what {business}'s bar ran for pour cost last month?

Food cost, most managers can quote to the penny. Liquor variance, not so much. If it's over ~20%, there's usually 10-15 points of easy margin hiding in over-pour and shrinkage.

Happy to send a short breakdown of where it typically leaks. No pitch, just the numbers.

- Miles
Performance Supply Depot
""",
    7: """Hi {first},

Last note from me — I know you're busy.

If {business}'s pour cost is already tight, ignore this, and my best to you and the team. If it's not, a 20-minute look at your variance usually finds the leak.

Either way, good luck this season.

- Miles
Performance Supply Depot
""",
}


def first_name(contact_name):
    if not contact_name:
        return "there"
    parts = str(contact_name).strip().split()
    return parts[0] if parts else "there"


def now_utc():
    return datetime.now(timezone.utc)


def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def reschedule(conn):
    """Reset scheduled_at by sequence_day so the sequence runs from now."""
    now = now_utc()
    cur = conn.cursor()
    cur.execute("SELECT id, sequence_day FROM email_queue WHERE status='ready'")
    rows = cur.fetchall()
    updated = 0
    for r in rows:
        day = r["sequence_day"] or 1
        offset = {1: 0, 3: 3, 7: 7}.get(day, 0)
        new_at = (now + timedelta(days=offset)).strftime("%Y-%m-%dT%H:%M:%S.%f")
        cur.execute("UPDATE email_queue SET scheduled_at=? WHERE id=?", (new_at, r["id"]))
        updated += 1
    conn.commit()
    print(f"Rescheduled {updated} 'ready' emails: day1=now, day3=+3d, day7=+7d")


def status(conn):
    cur = conn.cursor()
    cur.execute("SELECT status, sequence_day, COUNT(*) c FROM email_queue GROUP BY status, sequence_day ORDER BY status, sequence_day")
    for r in cur.fetchall():
        print(f"  {r['status']:8} day {r['sequence_day']}: {r['c']}")
    cur.execute("SELECT COUNT(*) c FROM email_queue WHERE sent_at IS NOT NULL")
    print(f"  total sent: {cur.fetchone()['c']}")


def send_due(conn, limit=None, delay=2.0, dry_run=False):
    now = now_utc()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id, q.lead_id, q.to_email, q.subject, q.sequence_day,
               l.business_name, l.contact_name
        FROM email_queue q LEFT JOIN leads l ON q.lead_id = l.id
        WHERE q.status='ready' AND q.scheduled_at <= ?
        ORDER BY q.sequence_day, q.id
    """, (now.strftime("%Y-%m-%dT%H:%M:%S.%f"),))
    rows = cur.fetchall()
    if not rows:
        print("No due emails.")
        return

    print(f"{len(rows)} due emails to send.")
    if limit:
        rows = rows[:limit]
        print(f"Limiting to {limit}.")

    sent = 0
    failed = 0
    for r in rows:
        body_template = BODIES.get(r["sequence_day"], BODIES[1])
        body = body_template.format(
            first=first_name(r["contact_name"]),
            business=r["business_name"] or "",
        )
        subject = r["subject"] or "Performance Supply Depot"
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"] = r["to_email"]

        if dry_run:
            print(f"[DRY] {r['to_email']}  |  {subject}")
            sent += 1
            continue

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as s:
                s.starttls()
                s.login(SMTP_USER, SMTP_PASS)
                s.sendmail(FROM_EMAIL, [r["to_email"]], msg.as_string())
            sent_at = now_utc().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(
                "UPDATE email_queue SET status='sent', sent_at=? WHERE id=?",
                (sent_at, r["id"]),
            )
            cur.execute(
                "UPDATE leads SET email_sent=1 WHERE id=?",
                (r["lead_id"],),
            )
            conn.commit()
            print(f"✓ {r['to_email']}  |  day {r['sequence_day']}")
            sent += 1
            time.sleep(delay)
        except Exception as e:
            print(f"✗ {r['to_email']}  |  {e}")
            failed += 1
            if "auth" in str(e).lower() or "login" in str(e).lower():
                print("Auth failure — stopping.")
                break

    print(f"\nDone: {sent} sent, {failed} failed.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reschedule", action="store_true")
    ap.add_argument("--send", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--delay", type=float, default=2.0)
    args = ap.parse_args()

    conn = connect()
    try:
        if args.reschedule:
            reschedule(conn)
        if args.status or (not args.send and not args.reschedule):
            status(conn)
        if args.send:
            send_due(conn, limit=args.limit, delay=args.delay, dry_run=args.dry_run)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
