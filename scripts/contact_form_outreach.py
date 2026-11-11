#!/usr/bin/env python3
"""
Website contact-form outreach for the no-phone Mortimer leads.

For each lead with a website, discover the contact page + form (action + fields),
then produce a ready-to-submit plan (JSON). Resumable.
"""
import sqlite3, re, json, os, time, argparse, subprocess
from urllib.parse import urljoin

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"
SOURCE = "mortimer-hwy4-680"
OUT = "/root/.openclaw/workspace/datadepot/data/contact_form_plans.json"

INTRO = ("Hello, I'm reaching out from Performance Supply Depot. We supply restaurants "
         "with thermal receipt paper, POS printer ribbons, and a full line of compatible "
         "toner and ink. Could you share the best email address so we can send a quick "
         "quote? Thank you!")

MSG_FIELD = ["message", "comments", "comment", "body", "your-message", "enquiry", "notes", "description"]
NAME_FIELD = ["name", "your-name", "fullname", "full-name", "contact-name"]
EMAIL_FIELD = ["email", "your-email", "email-address", "mail"]


def fetch(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "20", "-A",
                        "Mozilla/5.0 (PSD Outreach)", url], capture_output=True, text=True)
    return r.stdout


def find_contact(website):
    base = website if website.startswith("http") else "http://" + website
    html = fetch(base)
    # find a contact link
    contact = None
    for m in re.finditer(r'href=["\']([^"\']*contact[^"\']*)["\']', html or "", re.I):
        u = urljoin(base, m.group(1))
        contact = u
        break
    return base, contact or base, html


def parse_form(html, page_url):
    """Extract form action + input fields (name attr) from HTML."""
    forms = []
    for fm in re.finditer(r'<form[^>]*>', html or "", re.I):
        tag = fm.group(0)
        action = re.search(r'action=["\']([^"\']*)["\']', tag, re.I)
        action = action.group(1) if action else ""
        action = urljoin(page_url, action) if action else page_url
        fields = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', html[fm.end():], re.I)
        fields += re.findall(r'<textarea[^>]*name=["\']([^"\']+)["\']', html[fm.end():], re.I)
        forms.append({"action": action, "fields": fields})
    return forms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""SELECT id, name, notes FROM vendors WHERE source_file=? AND status != 'duplicate'
                   AND (phone IS NULL OR phone='')""", (SOURCE,))
    rows = cur.fetchall()
    con.close()

    try:
        plans = json.load(open(OUT))
    except Exception:
        plans = []
    done_names = {p["name"] for p in plans}

    todo = [r for r in rows if r[1] not in done_names]
    if args.limit:
        todo = todo[: args.limit]

    print(f"no-phone leads={len(rows)} planned={len(plans)} todo={len(todo)}")

    for vid, name, notes in todo:
        m = re.search(r'website=(\S+)', notes or "")
        website = m.group(1) if m else ""
        if not website:
            plans.append({"name": name, "website": "", "contact_url": "", "forms": [], "note": "no website"})
            continue
        base, contact_url, html = find_contact(website)
        ch = fetch(contact_url) if contact_url != base else html
        forms = parse_form(ch, contact_url)
        plans.append({"name": name, "website": website, "contact_url": contact_url,
                      "forms": forms, "intro": INTRO})
        time.sleep(0.5)
        if len(plans) % 10 == 0:
            json.dump(plans, open(OUT, "w"), indent=2)

    json.dump(plans, open(OUT, "w"), indent=2)
    print(f"PLANS={len(plans)} -> {OUT}")


if __name__ == "__main__":
    main()
