#!/usr/bin/env python3
"""
PSD Quote Agent — internal (staff) + external (customer) quoting engine.
Builds a full POS station quote: terminal + peripherals + software + programming + delivery.
Internal view shows cost/margin/profit; external view shows retail only.

Serve on port 8087 (alongside chipp_leads_api on 8086).
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
import uvicorn

BASE = Path(__file__).resolve().parent
CATALOG_FILE = BASE / "quote_catalog.json"
PRODUCTS_FILE = Path("/var/www/psdepot.com/products.json")
QUOTES_FILE = Path("/var/lib/psdepot/quotes.json")

STAFF_PASSWORD = "psd-staff-2026"  # TODO: move to env / .env

app = FastAPI(title="PSD Quote Agent", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Data loading ────────────────────────────────────────────

def load_catalog() -> dict:
    with open(CATALOG_FILE, "r") as f:
        return json.load(f)


def load_products() -> list:
    """Load the full site product list from products.json (fallback to empty)."""
    if not PRODUCTS_FILE.exists():
        return []
    try:
        with open(PRODUCTS_FILE, "r") as f:
            data = json.load(f)
        return data.get("products", [])
    except (json.JSONDecodeError, IOError):
        return []


def money(v) -> Optional[float]:
    if v is None:
        return None
    try:
        return round(float(v), 2)
    except (TypeError, ValueError):
        return None


def fmt(v) -> str:
    m = money(v)
    if m is None:
        return "—"
    return f"${m:,.2f}"


def read_quotes() -> list:
    if not QUOTES_FILE.exists():
        return []
    try:
        with open(QUOTES_FILE, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def write_quotes(quotes: list):
    QUOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = QUOTES_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(quotes, f, indent=2, default=str)
    tmp.replace(QUOTES_FILE)


# ─── Quote builder ───────────────────────────────────────────

def build_quote(spec: dict) -> dict:
    cat = load_catalog()
    cfg = cat["config"]
    tax_rate = float(spec.get("tax_rate", cfg["tax_rate"]))

    stations = max(1, int(spec.get("stations", 1)))
    terminal_key = spec.get("terminal", "SAP-630")
    printer_key = spec.get("printer", "TM-T88")
    include_drawer = bool(spec.get("cash_drawer", True))
    include_scanner = bool(spec.get("scanner", True))
    software_key = spec.get("software", "SAM4POS")
    add_ons = spec.get("add_ons", [])  # list of {"key": ..., "qty": ...} optional add-ons (e.g. scales)
    include_delivery = bool(spec.get("delivery", True))
    programming_hours = float(spec.get("programming_hours", 0))

    # Resolve hardware
    def find(category: str, key: str):
        for item in cat["hardware"].get(category, []):
            if item["key"] == key:
                return item
        return None

    terminal = find("terminals", terminal_key) or cat["hardware"]["terminals"][0]
    printer = find("printers", printer_key) or cat["hardware"]["printers"][0]
    drawer = find("cash_drawers", "DRAWER-FULL") or cat["hardware"]["cash_drawers"][0]
    scanner = find("scanners", "SCANNER") or cat["hardware"]["scanners"][0]

    software = next((s for s in cat["software"] if s["key"] == software_key), None)

    # Labor: in-house programming + on-site installation (fixed hours per order)
    prog = cat["services"]["programming"]
    install = cat["services"]["installation"]
    prog_rate = prog["rate_per_hour"]
    prog_hours = max(prog.get("hours", 2), programming_hours) if programming_hours > 0 else prog.get("hours", 2)
    install_rate = install["rate_per_hour"]
    install_hours = install.get("hours", 1)

    # Build line items (per station hardware × stations)
    lines = []  # one-time hardware/software
    recurring = []  # subscription items

    def add_line(key, name, sku, qty, price, cost, category, note=""):
        lines.append({
            "key": key, "name": name, "sku": sku, "qty": qty,
            "unit_price": money(price), "unit_cost": money(cost),
            "category": category, "note": note,
        })

    add_line(terminal_key, terminal["name"], terminal["sku"], stations, terminal["price"], terminal["cost"], "Terminal")
    if include_drawer:
        add_line("DRAWER-FULL", drawer["name"], drawer["sku"], stations, drawer["price"], drawer["cost"], "Peripheral")
    add_line(printer_key, printer["name"], printer["sku"], stations, printer["price"], printer["cost"], "Peripheral")
    if include_scanner:
        add_line("SCANNER", scanner["name"], scanner["sku"], stations, scanner["price"], scanner["cost"], "Peripheral")

    if software:
        if software.get("pricing_model") == "recurring":
            recurring.append({
                "key": software_key, "name": software["name"], "sku": software["sku"],
                "qty": stations, "monthly": money(software.get("monthly")),
                "note": software.get("note", ""),
            })
        else:
            add_line(software_key, software["name"], software["sku"], stations, software["price"], software["cost"], "Software")

    # Optional add-ons (e.g. scales)
    for a in add_ons:
        key = a.get("key")
        qty = int(a.get("qty", 1))
        item = next((x for x in cat["hardware"].get("scales", []) if x["key"] == key), None)
        if item:
            add_line(key, item["name"], item["sku"], qty, item["price"], item["cost"], "Add-on")

    # Programming line (labor, in-house)
    add_line("programming", prog["name"], "SERVICE", prog_hours, prog_rate, None, "Labor",
             note=f"{prog_hours:.1f} hrs @ ${prog_rate}/hr")

    # Installation line (labor, on-site)
    add_line("installation", install["name"], "SERVICE", install_hours, install_rate, None, "Labor",
             note=f"{install_hours:.1f} hrs @ ${install_rate}/hr")

    # Delivery line
    delivery = cat["services"]["delivery"]
    if include_delivery:
        add_line("delivery", delivery["name"], "SERVICE", 1, delivery["flat"], None, "Delivery")

    # Compute totals
    def line_totals(items):
        subtotal = 0.0
        total_cost = 0.0
        for l in items:
            p = l.get("unit_price")
            c = l.get("unit_cost")
            q = l["qty"]
            ext_price = (p * q) if p is not None else None
            ext_cost = (c * q) if c is not None else None
            l["ext_price"] = money(ext_price)
            l["ext_cost"] = money(ext_cost) if ext_cost is not None else None
            if ext_price is not None and ext_cost is not None:
                l["margin"] = money(ext_price - ext_cost)
                l["margin_pct"] = money((ext_price - ext_cost) / ext_price * 100) if ext_price > 0 else None
            else:
                l["margin"] = None
                l["margin_pct"] = None
            if ext_price is not None:
                subtotal += ext_price
            if ext_cost is not None:
                total_cost += ext_cost
        return subtotal, total_cost

    subtotal, total_cost = line_totals(lines)
    tax = money(subtotal * tax_rate)
    total = money(subtotal + tax)

    recurring_monthly = sum((r["monthly"] or 0.0) * r["qty"] for r in recurring)
    profit = money(subtotal - total_cost) if total_cost else None

    # Build two views
    internal = {
        "lines": [dict(l) for l in lines],
        "recurring": [dict(r) for r in recurring],
        "subtotal": money(subtotal),
        "total_cost": money(total_cost) if total_cost else None,
        "profit": profit,
        "tax": tax,
        "total": total,
        "recurring_monthly": money(recurring_monthly) if recurring else None,
    }

    # External view: retail only, no cost/margin fields
    external_lines = []
    for l in lines:
        external_lines.append({
            "name": l["name"], "sku": l["sku"], "qty": l["qty"],
            "unit_price": l["unit_price"], "ext_price": l["ext_price"],
            "note": l.get("note", ""),
        })

    external = {
        "lines": external_lines,
        "recurring": [dict(r) for r in recurring],
        "subtotal": money(subtotal),
        "tax": tax,
        "total": total,
        "recurring_monthly": money(recurring_monthly) if recurring else None,
    }

    return {
        "stations": stations,
        "terminal": terminal_key,
        "printer": printer_key,
        "programming_hours": prog_hours,
        "tax_rate": tax_rate,
        "internal": internal,
        "external": external,
    }


# ─── Endpoints ────────────────────────────────────────────

@app.get("/api/catalog")
async def get_catalog():
    cat = load_catalog()
    return JSONResponse({
        "hardware": cat["hardware"],
        "software": cat["software"],
        "services": cat["services"],
        "config": cat["config"],
        "products": load_products(),
    })


@app.post("/api/quote")
async def quote(request: Request):
    try:
        spec = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    return JSONResponse(build_quote(spec))


@app.post("/api/quote/save")
async def save_quote(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    qid = "q_" + str(int(time.time() * 1000))
    quote = {
        "id": qid,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "customer": data.get("customer", {}),
        "spec": data.get("spec", {}),
        "internal": data.get("internal"),
        "external": data.get("external"),
        "total": data.get("external", {}).get("total"),
    }
    quotes = read_quotes()
    quotes.insert(0, quote)
    write_quotes(quotes)
    return JSONResponse({"ok": True, "id": qid, "total": len(quotes)})


@app.get("/api/quotes")
async def list_quotes():
    return JSONResponse(read_quotes())


@app.get("/health")
async def health():
    return {"status": "ok", "quote_count": len(read_quotes())}


# ─── Static UI ────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def internal_ui():
    return FileResponse(BASE / "internal.html")


@app.get("/staff", response_class=HTMLResponse)
async def staff_ui():
    return FileResponse(BASE / "internal.html")


@app.get("/widget", response_class=HTMLResponse)
async def widget_ui():
    return FileResponse(BASE / "external.html")


@app.get("/widget.js")
async def widget_js():
    return FileResponse(BASE / "widget.js")


if __name__ == "__main__":
    QUOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Catalog: {CATALOG_FILE}")
    print(f"Quotes:  {QUOTES_FILE}")
    print(f"Staff password: {STAFF_PASSWORD}")
    uvicorn.run(app, host="127.0.0.1", port=8087, log_level="info")
