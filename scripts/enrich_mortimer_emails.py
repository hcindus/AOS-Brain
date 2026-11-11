#!/usr/bin/env python3
"""
Enrich the Mortimer Hwy4/680 leads with missing emails — scrape each restaurant's
website (homepage + /contact) for a published email, then update DepotChaos.

Resumable via a state file. Reads website URL from the vendor's notes field.
"""
import sqlite3, re, sys, os, time, argparse, subprocess, json
from urllib.parse import urljoin

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
STATE = "/root/.openclaw/workspace/datadepot/data/mortimer_email_state.json"
SOURCE = "mortimer-hwy4-680"

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
# junk emails to skip
JUNK = re.compile(r'(sentry|example|wordpress|wixpress|godaddy|squarespace|schema|'
                  r'\.png|\.jpg|\.gif|\.jpeg|\.svg|\.webp|\.css|\.js|\.ico|'
                  r'yourdomain|@2x|@3x|wixpress\.com|sentry\.io|@sentry|noreply|no-reply)',
                  re.I)

PRIORITY = ['info@', 'contact@', 'hello@', 'reservations@', 'orders@', 'sales@']


def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {"done": [], "failed": []}


def save_state(s):
    json.dump(s, open(STATE, "w"), indent=2)


def fetch(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "20", "-A",
                        "Mozilla/5.0 (PSD Lead Enrichment)", url],
                       capture_output=True, text=True)
    return r.stdout


def emails_from(html):
    found = set()
    for m in EMAIL_RE.findall(html or ""):
        e = m.lower().strip('.')
        if JUNK.search(e):
            continue
        found.add(e)
    # sort: priority domains first
    def rank(e):
        for i, p in enumerate(PRIORITY):
            if e.startswith(p):
                return i
        return 99
    return sorted(found, key=rank)


def scrape_email(website):
    if not website or 'http' not in website:
        return ""
    base = website if website.startswith('http') else 'http://' + website
    pages = [base, urljoin(base.rstrip('/') + '/', 'contact'),
             urljoin(base.rstrip('/') + '/', 'contact-us'),
             urljoin(base.rstrip('/') + '/', 'about')]
    for p in pages:
        try:
            html = fetch(p)
            em = emails_from(html)
            if em:
                return em[0]
        except Exception:
            pass
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()
    if args.reset and os.path.exists(STATE):
        os.remove(STATE)

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id, name, notes FROM vendors WHERE source_file=? AND (email IS NULL OR email='')",
                (SOURCE,))
    rows = cur.fetchall()

    state = load_state()
    done = set(state["done"])
    failed = set(state["failed"])

    todo = [r for r in rows if r[0] not in done and r[0] not in failed]
    if args.limit:
        todo = todo[: args.limit]

    print(f"no-email leads={len(rows)} done={len(done)} failed={len(failed)} todo={len(todo)}")

    found_count = 0
    for vid, name, notes in todo:
        m = re.search(r'website=(\S+)', notes or "")
        website = m.group(1) if m else ""
        email = scrape_email(website)
        if email:
            cur.execute("UPDATE vendors SET email=? WHERE id=?", (email, vid))
            state["done"].append(vid)
            found_count += 1
            print(f"  FOUND {name[:30]} -> {email}")
        else:
            state["failed"].append(vid)
        time.sleep(0.6)
        if found_count % 10 == 0 and found_count:
            con.commit()
            save_state(state)

    con.commit()
    save_state(state)
    print(f"COMPLETE: found={found_count} done={len(state['done'])} failed={len(state['failed'])}")
    con.close()


if __name__ == "__main__":
    main()
