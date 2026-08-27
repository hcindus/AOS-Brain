"""OrderPort — SQLite schema + connection helpers.

Tables:
  accounts        — businesses (multi-tenant)
  users           — login for merchant/admin/rep roles
  categories      — per-account menu categories
  menu_items      — per-account items (editable by merchant)
  orders          — customer orders (pickup)
  order_items     — line items snapshot
  payouts         — per-order revenue split ledger (business/company/rep)
  subscriptions   — monthly billing for the business account
  notifications   — order notification log (email/sms/printer)
"""
import sqlite3
import os

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    slug          TEXT UNIQUE NOT NULL,
    business_name TEXT NOT NULL,
    email         TEXT,
    phone         TEXT,
    address       TEXT,
    timezone      TEXT DEFAULT 'America/Los_Angeles',
    pickup_hours  TEXT DEFAULT '',
    status        TEXT DEFAULT 'active',           -- active | suspended
    rep_id        INTEGER,                          -- FK -> reps.id (attribution)
    stripe_account_id TEXT,                         -- Stripe Connect destination
    plan          TEXT DEFAULT 'starter',           -- starter | pro | enterprise
    monthly_fee_cents INTEGER DEFAULT 0,
    created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS reps (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT,
    share_bps   INTEGER DEFAULT 500,                -- 5% default
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id    INTEGER,                          -- NULL for admin/rep-global
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role          TEXT DEFAULT 'merchant',          -- merchant | admin | rep
    rep_id        INTEGER,
    created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS categories (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    name       TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS menu_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id  INTEGER NOT NULL,
    category_id INTEGER,
    name        TEXT NOT NULL,
    description TEXT DEFAULT '',
    price_cents INTEGER NOT NULL,
    image_url   TEXT DEFAULT '',
    available   INTEGER DEFAULT 1,                  -- 1 = in stock
    sort_order  INTEGER DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS orders (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id         INTEGER NOT NULL,
    order_ref          TEXT UNIQUE NOT NULL,        -- human-readable e.g. PRM-1042
    customer_name      TEXT NOT NULL,
    customer_phone     TEXT,
    customer_email     TEXT,
    subtotal_cents     INTEGER NOT NULL,
    tax_cents          INTEGER DEFAULT 0,
    total_cents        INTEGER NOT NULL,
    status             TEXT DEFAULT 'new',          -- new | paid | ready | picked_up | cancelled
    pickup_time        TEXT,
    note               TEXT DEFAULT '',
    stripe_payment_intent TEXT,
    created_at         TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS order_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    INTEGER NOT NULL,
    item_name   TEXT NOT NULL,
    unit_price_cents INTEGER NOT NULL,
    quantity    INTEGER NOT NULL,
    modifiers   TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS payouts (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      INTEGER NOT NULL,
    account_id    INTEGER NOT NULL,
    total_cents   INTEGER NOT NULL,
    business_cents INTEGER NOT NULL,
    company_cents INTEGER NOT NULL,
    rep_cents     INTEGER NOT NULL,
    rep_id        INTEGER,
    settled       INTEGER DEFAULT 0,               -- 0 pending, 1 transferred
    created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id    INTEGER NOT NULL,
    plan          TEXT DEFAULT 'starter',
    amount_cents  INTEGER DEFAULT 0,
    status        TEXT DEFAULT 'active',           -- active | past_due | cancelled
    next_bill_at  TEXT,
    stripe_sub_id TEXT,
    created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS notifications (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    order_id   INTEGER,
    channel    TEXT NOT NULL,                       -- email | sms | printer
    target     TEXT DEFAULT '',
    status     TEXT DEFAULT 'pending',              -- pending | sent | failed
    detail     TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now'))
);
"""


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    os.makedirs(os.path.dirname(config.DB_PATH), exist_ok=True)
    conn = get_conn()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"✅ OrderPort DB initialized at {config.DB_PATH}")
