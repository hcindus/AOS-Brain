#!/usr/bin/env python3
"""PSD Order API — CLOSETER posts orders here. Stores to a JSON ledger + emails the Captain.
No Google, no PHP. Served via FastAPI/uvicorn on 8087."""
import json, os, smtplib, sys
sys.path.insert(0, "/root/.openclaw/workspace/scripts")
from datetime import datetime, timezone
from email.mime.text import MIMEText
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

LEDGER = "/root/.openclaw/workspace/datadepot/data/psdepot_orders.json"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def _smtp():
    c = {}
    for line in open("/root/.openclaw/workspace/aocros/secrets/smtp.env"):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1); c[k] = v
    return c

def notify_captain(order):
    try:
        c = _smtp()
        body = (f"New order received:\n\n"
                f"Manager: {order.get('manager_name','')}\n"
                f"Business: {order.get('business_name','')}\n"
                f"Email: {order.get('email','')}\n"
                f"Address: {order.get('address','')}, {order.get('city','')} {order.get('state','')} {order.get('zip','')}\n"
                f"Date: {order.get('date','')}\n"
                f"Products: {order.get('products','')}\n"
                f"Special instructions: {order.get('special_instructions','')}\n")
        summ = order.get("summary")
        if summ:
            body += "\n--- ORDER SUMMARY ---\n"
            for l in summ.get("lines", []):
                body += f"  {l['qty']} x {l['sku']} {l['name']} = ${l['sell']:.2f}\n"
            body += (f"Subtotal: ${summ['subtotal']:.2f}\n"
                     f"Tax ({int(summ['tax_rate']*100)}%): ${summ['tax']:.2f}\n"
                     f"Total: ${summ['total']:.2f}\n"
                     f"Cost: ${summ['cost']:.2f}\n"
                     f"Profit: ${summ['margin']:.2f} ({summ['margin_pct']}%)\n")
            v = order.get("vendor_lines", "")
            if v:
                body += f"\n--- VENDOR ORDER ---\n{v}\n"
        msg = MIMEText(body)
        msg["From"] = f"Performance Supply Depot <{c['HOSTINGER_SMTP_USER']}>"
        msg["To"] = "antonio.hudnall@gmail.com"
        msg["Subject"] = f"New order — {order.get('business_name') or order.get('manager_name') or 'customer'}"
        s = smtplib.SMTP(c.get("HOSTINGER_SMTP_SERVER","smtp.hostinger.com"),
                         int(c.get("HOSTINGER_SMTP_PORT","587")), timeout=30)
        s.starttls(); s.login(c["HOSTINGER_SMTP_USER"], c["HOSTINGER_SMTP_PASS"])
        s.sendmail(c["HOSTINGER_SMTP_USER"], ["antonio.hudnall@gmail.com", "info@psdepot.com"], msg.as_string())
        s.quit()
        return True
    except Exception as e:
        return False

@app.post("/api/order")
async def receive_order(request: Request):
    try:
        data = await request.json()
    except Exception:
        return {"success": False, "error": "invalid JSON"}
    items = data.get("items")
    summary = None
    vendor_lines = ""
    if items:
        try:
            import order_processor
            summary = order_processor.process_order(items)
            vendor_lines = order_processor.vendor_lines(summary)
        except Exception:
            summary = None
    order = {
        "manager_name": data.get("manager_name", ""),
        "business_name": data.get("business_name", ""),
        "email": data.get("email", ""),
        "address": data.get("address", ""),
        "city": data.get("city", ""),
        "state": data.get("state", ""),
        "zip": data.get("zip", ""),
        "date": data.get("date", ""),
        "products": data.get("products", ""),
        "special_instructions": data.get("special_instructions", ""),
        "source": data.get("source", "closeter"),
        "summary": summary,
        "vendor_lines": vendor_lines,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }
    orders = []
    if os.path.exists(LEDGER):
        try: orders = json.load(open(LEDGER))
        except Exception: orders = []
    orders.append(order)
    json.dump(orders, open(LEDGER, "w"), indent=2)
    emailed = notify_captain(order)
    return {"success": True, "message": "Order received", "emailed": emailed}

@app.get("/api/order")
async def list_orders():
    if os.path.exists(LEDGER):
        try: return json.load(open(LEDGER))
        except Exception: return []
    return []

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
