#!/usr/bin/env python3
"""
JARVIS Core — Performance Supply Depot AI assistant foundation.

Phase 1 (no external keys): the "second brain" building blocks that JARVIS
uses to turn leads/voice into polished PDF quotes & invoices.

Modules:
- leads_store.py  — SQLite leads table (the "leads table" JARVIS queries)
- documents.py    — PDF quote + invoice generator (reportlab)
- security.py     — hotline PIN gate (2 attempts, logs failures)
- demo.py         — end-to-end demo
"""

from .leads_store import LeadsStore
from .documents import QuoteEngine, InvoiceEngine
from .security import PinGate

__all__ = ["LeadsStore", "QuoteEngine", "InvoiceEngine", "PinGate"]
