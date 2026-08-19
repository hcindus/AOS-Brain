#!/usr/bin/env python3
"""Leads table — the persistent store JARVIS queries for client info."""
import sqlite3
import json
import os
from datetime import datetime
from typing import Optional

DB_PATH = os.environ.get("JARVIS_DB", "/var/lib/psdepot/jarvis.db")


class LeadsStore:
    """SQLite-backed leads table (name, email, phone, business, deal, value, status)."""

    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init()

    def _init(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                business TEXT,
                product TEXT,
                value REAL,
                status TEXT DEFAULT 'new',      -- new / quoted / won / lost
                created_at TEXT,
                date_contacted TEXT,
                notes TEXT
            )
        """)
        self.conn.commit()

    def add(self, name: str, email: str = "", phone: str = "", business: str = "",
            product: str = "", value: float = 0.0, notes: str = "") -> int:
        cur = self.conn.execute(
            "INSERT INTO leads (name, email, phone, business, product, value, status, created_at, notes) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (name, email, phone, business, product, value, "new",
             datetime.now().isoformat(), notes),
        )
        self.conn.commit()
        return cur.lastrowid

    def find(self, name: str = "", phone: str = "", email: str = "") -> list[dict]:
        q = "SELECT * FROM leads WHERE 1=1"
        args = []
        if name:
            q += " AND name LIKE ?"; args.append(f"%{name}%")
        if phone:
            q += " AND phone = ?"; args.append(phone)
        if email:
            q += " AND email = ?"; args.append(email)
        return [dict(r) for r in self.conn.execute(q, args).fetchall()]

    def get(self, lead_id: int) -> Optional[dict]:
        r = self.conn.execute("SELECT * FROM leads WHERE id=?", (lead_id,)).fetchone()
        return dict(r) if r else None

    def set_status(self, lead_id: int, status: str):
        self.conn.execute("UPDATE leads SET status=? WHERE id=?", (status, lead_id))
        self.conn.commit()

    def set_value(self, lead_id: int, value: float):
        self.conn.execute("UPDATE leads SET value=? WHERE id=?", (value, lead_id))
        self.conn.commit()

    def all(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()]
