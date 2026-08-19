#!/usr/bin/env python3
"""
JARVIS — Performance Supply Depot AI Assistant (API).

A sellable "AI second brain" for clients: leads management + polished
PDF quotes/invoices + a security-PIN gate. Runs as a self-contained service.

Endpoints:
  POST /api/leads        create a lead
  GET  /api/leads        list leads
  GET  /api/leads/{id}   get one lead
  POST /api/quote        generate a quote PDF (returns URL)
  POST /api/invoice      generate an invoice PDF (returns URL)
  POST /api/auth         hotline PIN check
  GET  /docs             Swagger UI
"""
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Tuple
import os

from jarvis_core import LeadsStore, QuoteEngine, InvoiceEngine, PinGate

app = FastAPI(title="JARVIS — Performance Supply Depot AI Assistant", version="1.0.0")

store = LeadsStore()
quote_engine = QuoteEngine()
invoice_engine = InvoiceEngine()
pin_gate = PinGate()

DOCS_DIR = os.environ.get("JARVIS_OUT", "/var/lib/psdepot/documents")
PUBLIC_DOCS = "/documents"  # served route


def require_auth(authorization: str = Header(default="")):
    """Token-based auth — protected endpoints require a valid issued token."""
    token = authorization.removeprefix("Bearer ").strip()
    if not pin_gate.validate_token(token):
        raise HTTPException(401, "Unauthorized — valid PIN required")
    return token


class LeadIn(BaseModel):
    name: str
    email: str = ""
    phone: str = ""
    business: str = ""
    product: str = ""
    value: float = 0.0
    notes: str = ""


class DocIn(BaseModel):
    lead_id: int
    items: List[Tuple[str, int, float]]
    terms: str = ""
    notes: str = ""


class AuthIn(BaseModel):
    code: str


@app.post("/api/leads", dependencies=[Depends(require_auth)])
def create_lead(lead: LeadIn):
    lid = store.add(lead.name, lead.email, lead.phone, lead.business,
                    lead.product, lead.value, lead.notes)
    return {"id": lid, **store.get(lid)}


@app.get("/api/leads", dependencies=[Depends(require_auth)])
def list_leads():
    return store.all()


@app.get("/api/leads/{lid}", dependencies=[Depends(require_auth)])
def get_lead(lid: int):
    lead = store.get(lid)
    if not lead:
        raise HTTPException(404, "Lead not found")
    return lead


@app.post("/api/quote", dependencies=[Depends(require_auth)])
def make_quote(doc: DocIn):
    lead = store.get(doc.lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    path = quote_engine.generate(lead, doc.items, terms=doc.terms or QuoteEngine.DEFAULT_TERMS,
                                 notes=doc.notes)
    store.set_status(doc.lead_id, "quoted")
    return {"pdf": f"{PUBLIC_DOCS}/{os.path.basename(path)}"}


@app.post("/api/invoice", dependencies=[Depends(require_auth)])
def make_invoice(doc: DocIn):
    lead = store.get(doc.lead_id)
    if not lead:
        raise HTTPException(404, "Lead not found")
    path = invoice_engine.generate(lead, doc.items, terms=doc.terms or InvoiceEngine.DEFAULT_TERMS,
                                   notes=doc.notes)
    return {"pdf": f"{PUBLIC_DOCS}/{os.path.basename(path)}"}


@app.post("/api/auth")
def auth(a: AuthIn):
    token, msg = pin_gate.issue_token(a.code)
    return {"granted": token is not None, "message": msg, "token": token}


@app.get("/health")
def health():
    return {"status": "ok", "leads": len(store.all())}


# Serve generated documents + frontend
os.makedirs(DOCS_DIR, exist_ok=True)
app.mount("/documents", StaticFiles(directory=DOCS_DIR), name="documents")

STATIC = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC):
    app.mount("/", StaticFiles(directory=STATIC, html=True), name="frontend")
