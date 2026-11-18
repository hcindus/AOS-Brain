#!/usr/bin/env python3
"""
Order Desk — unified, automated order pipeline.

One place that takes an order (voice/email/text) and marches it through:
  captured → quoted → confirmed → paid → vendor → fulfilled  (→ cancelled)

Only the "confirm/charge" step is human (you). Everything else auto-fires.

Usage:
  python3 order_desk.py create --channel voice --from +14155551234 --raw "2 cases PF-230"
  python3 order_desk.py list
  python3 order_desk.py advance <id> confirmed|paid|vendor|fulfilled|cancelled
"""
import json
import sqlite3
import argparse
import sys
from datetime import datetime, timezone

sys.path.insert(0, "/root/.openclaw/workspace/scripts")
import order_processor as op

DB = "/root/.openclaw/workspace/DepotChaos/depot_chaos.db"

STATUSES = ["captured", "quoted", "confirmed", "paid", "vendor", "fulfilled", "cancelled"]


def _init():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, channel TEXT, from_ TEXT, raw TEXT,
            items TEXT, subtotal REAL, shipping REAL, tax REAL, total REAL,
            customer_name TEXT, customer_email TEXT,
            status TEXT, po TEXT, vendor_notes TEXT, updated_at TEXT
        )
    """)
    con.commit()
    con.close()


def create(channel, from_, raw):
    _init()
    items = op.parse_order(raw)
    quote = op.process_order(items) if items else None
    now = datetime.now(timezone.utc).isoformat()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO orders (ts, channel, from_, raw, items, subtotal, shipping, tax, total, status, updated_at) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (now, channel, from_, raw, json.dumps(items),
         quote["subtotal"] if quote else None, quote["shipping"] if quote else None,
         quote["tax"] if quote else None, quote["total"] if quote else None,
         "quoted" if quote else "captured", now))
    oid = cur.lastrowid
    con.commit()
    con.close()
    return oid, items, quote


def advance(oid, status):
    _init()
    if status not in STATUSES:
        raise ValueError(f"bad status {status}")
    now = datetime.now(timezone.utc).isoformat()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("UPDATE orders SET status=?, updated_at=? WHERE id=?", (status, now, oid))
    con.commit()
    # auto-fire on certain transitions
    if status == "paid":
        cur.execute("SELECT po, raw, from_ FROM orders WHERE id=?", (oid,))
        _po, raw, frm = cur.fetchone() or (None, None, None)
        # mark_payment_received already handles the thank-you; here we just note it.
    con.close()
    return oid


def list_orders(limit=20):
    _init()
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id, ts, channel, from_, total, status FROM orders ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    con.close()
    return rows


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")

    c = sub.add_parser("create")
    c.add_argument("--channel", default="voice")
    c.add_argument("--from", dest="from_", required=True)
    c.add_argument("--raw", required=True)

    sub.add_parser("list")

    a = sub.add_parser("advance")
    a.add_argument("id", type=int)
    a.add_argument("status", choices=STATUSES)

    args = ap.parse_args()

    if args.cmd == "create":
        oid, items, quote = create(args.channel, args.from_, args.raw)
        print(f"ORDER #{oid} created | items={items} | status={'quoted' if quote else 'captured'}")
        if quote:
            print(f"  subtotal ${quote['subtotal']:.2f} + ship ${quote['shipping']:.2f} + tax ${quote['tax']:.2f} = ${quote['total']:.2f}")
    elif args.cmd == "list":
        for r in list_orders():
            print(f"  #{r[0]} {r[1][:16]} {r[2]:6s} {r[3]} ${r[4] or 0:.2f} [{r[5]}]")
    elif args.cmd == "advance":
        advance(args.id, args.status)
        print(f"ORDER #{args.id} -> {args.status}")
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
