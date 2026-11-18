"""Persistent inbound log + repeat-contact history (SQLite)."""
import json
import sqlite3
from datetime import datetime, timezone


class Store:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init()

    def _init(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS inbound (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT, channel TEXT, from_ TEXT, body TEXT,
                intent TEXT, urgency TEXT, entity TEXT,
                qualified TEXT, agents TEXT, summary TEXT
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_inbound_from ON inbound(from_)")
        con.commit()
        con.close()

    def log(self, event, route):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO inbound (ts, channel, from_, body, intent, urgency, entity, qualified, agents, summary) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            (event.timestamp, event.channel, event.from_, event.body,
             route.intent, route.urgency, json.dumps(route.entity),
             route.qualified, json.dumps(route.agents), route.summary))
        con.commit()
        con.close()

    def prior_contacts(self, from_, limit=5):
        """Repeat-contact history for a given phone/email/handle."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute(
            "SELECT ts, channel, intent, qualified, summary FROM inbound WHERE from_=? ORDER BY ts DESC LIMIT ?",
            (from_, limit))
        rows = cur.fetchall()
        con.close()
        return rows
