#!/usr/bin/env python3
"""
Jenny's Giant Burger — Online Ordering API

Fresh build. Cloud ordering portal for a food-truck / counter-service setup.

Flow (mirrors ReggieStarr POS KDS + receipt printer, but SMS instead of paper):
  1. Customer browses the interactive menu, adds items, sees totals.
  2. Customer submits order with name + phone.
  3. Backend validates, computes subtotal / tax / total.
  4. SMS → cook's device (kitchen order).
  5. SMS → customer (receipt / confirmation).

Payment: "pay at pickup" (cash/card on arrival) — no online card processor wired.
SMS is sent via Twilio REST API (no `twilio` lib needed). Falls back to
log-only "dry-run" mode when credentials are missing/placeholder.
"""

import os
import json
import uuid
import base64
from datetime import datetime, timezone
from typing import List, Optional

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ----------------------------------------------------------------------------
# CONFIG (env-driven)
# ----------------------------------------------------------------------------
def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

TAX_RATE = float(_env("JENNY_TAX_RATE", "0.0875"))          # Fort Bragg, CA
BUSINESS_NAME = _env("JENNY_BUSINESS_NAME", "Jenny's Giant Burger")
BUSINESS_PHONE = _env("JENNY_BUSINESS_PHONE", "(707) 964-2235")
BUSINESS_ADDRESS = _env("JENNY_BUSINESS_ADDRESS", "940 Main St N, Fort Bragg, CA 95437")

# Ordering options (best-practice delivery/pickup flow)
DELIVERY_FEE = float(_env("JENNY_DELIVERY_FEE", "3.99"))       # flat delivery fee
DELIVERY_MIN_ORDER = float(_env("JENNY_DELIVERY_MIN", "0.0"))  # 0 = no minimum
PICKUP_ETA_MIN = int(_env("JENNY_PICKUP_ETA", "15"))           # minutes
DELIVERY_ETA_MIN = int(_env("JENNY_DELIVERY_ETA", "35"))       # minutes
BUSINESS_HOURS = _env("JENNY_BUSINESS_HOURS", "Open daily 10:30am–9:00pm")

# Twilio (SMS)
TWILIO_SID = _env("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = _env("TWILIO_AUTH_TOKEN")
TWILIO_FROM = _env("TWILIO_FROM_NUMBER")
COOK_PHONE = _env("JENNY_COOK_PHONE")                        # kitchen / cook's device

# Order storage
DATA_DIR = _env("JENNY_DATA_DIR", "/var/lib/jennysgiantburger")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

_IS_DRY_RUN = (
    not TWILIO_SID
    or "your_" in TWILIO_SID.lower()
    or "your_" in TWILIO_TOKEN.lower()
    or "your_" in TWILIO_FROM.lower()
    or TWILIO_FROM == "+15551234567"
)

# ----------------------------------------------------------------------------
# MENU (single source of truth — real Jenny's prices from Locallya, Mar 2026)
# ----------------------------------------------------------------------------
MENU = {
    "giant_burgers": {
        "label": "Giant Burgers",
        "emoji": "🍔",
        "items": [
            {"id": "giant_hamburger", "name": "Giant Hamburger", "desc": "1/3 lb jumbo patty, old-fashioned style", "price": 5.40, "fan": True},
            {"id": "giant_cheeseburger", "name": "Giant Cheeseburger", "desc": "1/3 lb giant with melty cheese", "price": 5.80},
            {"id": "double_giant_hamburger", "name": "Double Giant Hamburger", "desc": "Two jumbo patties", "price": 6.75},
            {"id": "double_giant_cheeseburger", "name": "Double Giant Cheeseburger", "desc": "Two jumbo patties, double cheese", "price": 6.95, "fan": True},
        ],
    },
    "classic_burgers": {
        "label": "Classic Burgers",
        "emoji": "🧀",
        "items": [
            {"id": "regular_hamburger", "name": "Regular Hamburger", "desc": "Classic single patty", "price": 3.90},
            {"id": "regular_cheeseburger", "name": "Regular Cheeseburger", "desc": "Classic patty with cheese", "price": 4.10},
            {"id": "double_regular_hamburger", "name": "Double Regular Hamburger", "desc": "Two classic patties", "price": 5.20},
            {"id": "double_regular_cheeseburger", "name": "Double Regular Cheeseburger", "desc": "Two classic patties, cheese", "price": 5.35},
        ],
    },
    "veggie": {
        "label": "Veggie",
        "emoji": "🥬",
        "items": [
            {"id": "gardenburger", "name": "Gardenburger", "desc": "Grilled meat-free patty", "price": 4.95},
            {"id": "gardenburger_cheese", "name": "Gardenburger With Cheese", "desc": "Garden patty + melty cheese", "price": 5.35},
            {"id": "veggie_sandwich", "name": "Veggie Sandwich", "desc": "Fresh veggie stack", "price": 2.50},
            {"id": "veggie_sandwich_cheese", "name": "Veggie Sandwich With Cheese", "desc": "Fresh veggie stack + cheese", "price": 2.75},
        ],
    },
    "sides": {
        "label": "Sides",
        "emoji": "🍟",
        "items": [
            {"id": "french_fries", "name": "French Fries", "desc": "Golden & crisp", "price": 2.20},
            {"id": "cookies", "name": "Cookies", "desc": "A sweet little something", "price": 1.25},
        ],
    },
    "ice_cream": {
        "label": "Ice Cream",
        "emoji": "🍦",
        "items": [
            {"id": "shakes", "name": "Shakes", "desc": "Thick, made to order", "price": 3.55, "fan": True},
            {"id": "malts", "name": "Malts", "desc": "Classic malted shake", "price": 3.75},
            {"id": "sundaes", "name": "Sundaes", "desc": "Ice cream with the good stuff", "price": 3.55},
            {"id": "cone", "name": "Cone", "desc": "Old-fashioned scoop", "price": 1.95},
        ],
    },
    "soft_drinks": {
        "label": "Soft Drinks",
        "emoji": "🥤",
        "items": [
            {"id": "pepsi", "name": "Pepsi", "desc": "", "price": 2.75},
            {"id": "diet_pepsi", "name": "Diet Pepsi", "desc": "", "price": 2.75},
            {"id": "mountain_dew", "name": "Mountain Dew", "desc": "", "price": 2.75},
            {"id": "root_beer", "name": "Root Beer", "desc": "", "price": 2.75},
            {"id": "lemonade", "name": "Lemonade", "desc": "", "price": 2.75},
            {"id": "ice_tea", "name": "Ice Tea", "desc": "", "price": 2.75},
        ],
    },
}

# Flattened lookup: id -> (item, category_label)
_LOOKUP = {}
for cat_key, cat in MENU.items():
    for it in cat["items"]:
        _LOOKUP[it["id"]] = (it, cat["label"])

# ----------------------------------------------------------------------------
# APP
# ----------------------------------------------------------------------------
app = FastAPI(title=f"{BUSINESS_NAME} Ordering API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_orders() -> List[dict]:
    _ensure_data_dir()
    if not os.path.exists(ORDERS_FILE):
        return []
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save_orders(orders: List[dict]):
    _ensure_data_dir()
    tmp = ORDERS_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(orders, f, indent=2)
    os.replace(tmp, ORDERS_FILE)


def _money(v: float) -> str:
    return f"${v:,.2f}"


# ----------------------------------------------------------------------------
# SMS
# ----------------------------------------------------------------------------
def send_sms(to: str, body: str) -> dict:
    """Send an SMS via Twilio REST API. Returns a status dict.

    Falls back to dry-run (log only) when credentials are missing/placeholder.
    """
    if not to:
        return {"ok": False, "dry_run": _IS_DRY_RUN, "error": "no destination number"}

    if _IS_DRY_RUN:
        print(f"[SMS DRY-RUN] -> {to}:\n{body}\n" + "-" * 40)
        return {"ok": True, "dry_run": True, "to": to}

    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    auth = base64.b64encode(f"{TWILIO_SID}:{TWILIO_TOKEN}".encode()).decode()
    try:
        r = requests.post(
            url,
            data={"To": to, "From": TWILIO_FROM, "Body": body},
            headers={"Authorization": f"Basic {auth}"},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        return {"ok": True, "dry_run": False, "sid": data.get("sid"), "to": to}
    except Exception as e:
        print(f"[SMS ERROR] -> {to}: {e}")
        return {"ok": False, "dry_run": False, "error": str(e), "to": to}


def _kitchen_sms(order: dict) -> str:
    is_delivery = order.get("order_type") == "delivery"
    lines = [f"🔥 NEW ORDER #{order['id']}", ""]
    lines.append(f"{order['customer_name']} · {'DELIVERY' if is_delivery else 'PICKUP'}")
    if is_delivery and order.get("delivery_address"):
        lines.append(f"Deliver to: {order['delivery_address']}")
    if order.get("pickup_time") and not is_delivery:
        lines.append(f"Pickup: {order['pickup_time']}")
    lines.append("")
    for it in order["items"]:
        lines.append(f"  {it['qty']}x {it['name']}")
    lines.append("")
    lines.append(f"TOTAL: {_money(order['total'])}")
    if order.get("notes"):
        lines.append(f"NOTE: {order['notes']}")
    return "\n".join(lines)


def _receipt_sms(order: dict) -> str:
    is_delivery = order.get("order_type") == "delivery"
    eta = order.get("eta_minutes", PICKUP_ETA_MIN)
    lines = [f"{BUSINESS_NAME}", "Your order receipt", ""]
    lines.append(f"Order #{order['id']}")
    lines.append(f"{'Delivery' if is_delivery else 'Pickup'} · ~{eta} min")
    if is_delivery and order.get("delivery_address"):
        lines.append(f"To: {order['delivery_address']}")
    lines.append("")
    for it in order["items"]:
        lines.append(f"  {it['qty']}x {it['name']}  {_money(it['line_total'])}")
    lines.append("")
    lines.append(f"Subtotal: {_money(order['subtotal'])}")
    lines.append(f"Tax:      {_money(order['tax'])}")
    if order.get("delivery_fee", 0) > 0:
        lines.append(f"Delivery: {_money(order['delivery_fee'])}")
    lines.append(f"TOTAL:    {_money(order['total'])}")
    lines.append("")
    lines.append(f"Pay at {'delivery' if is_delivery else 'pickup'} · {BUSINESS_PHONE}")
    lines.append("Thank you!")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# MODELS
# ----------------------------------------------------------------------------
class OrderItem(BaseModel):
    id: str
    qty: int = Field(..., gt=0, le=99)


class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=80)
    phone: str = Field(..., min_length=7, max_length=20)
    order_type: str = Field("pickup")           # "pickup" | "delivery"
    pickup_time: Optional[str] = None
    delivery_address: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=300)
    items: List[OrderItem]


# ----------------------------------------------------------------------------
# ROUTES
# ----------------------------------------------------------------------------
@app.get("/api/health")
def health():
    return {
        "ok": True,
        "business": BUSINESS_NAME,
        "tax_rate": TAX_RATE,
        "sms": "dry-run" if _IS_DRY_RUN else "twilio-live",
        "cook_phone_configured": bool(COOK_PHONE),
        "time": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/menu")
def menu():
    return {
        "business": BUSINESS_NAME,
        "tax_rate": TAX_RATE,
        "categories": [
            {
                "key": k,
                "label": v["label"],
                "emoji": v["emoji"],
                "items": v["items"],
            }
            for k, v in MENU.items()
        ],
    }


@app.post("/api/order")
def create_order(req: OrderRequest):
    # Validate order type
    order_type = (req.order_type or "pickup").strip().lower()
    if order_type not in ("pickup", "delivery"):
        raise HTTPException(status_code=400, detail="order_type must be 'pickup' or 'delivery'")

    is_delivery = order_type == "delivery"
    delivery_address = (req.delivery_address or "").strip() if is_delivery else ""
    if is_delivery and not delivery_address:
        raise HTTPException(status_code=400, detail="Delivery address is required")

    # Validate items
    resolved = []
    for line in req.items:
        hit = _LOOKUP.get(line.id)
        if not hit:
            raise HTTPException(status_code=400, detail=f"Unknown item: {line.id}")
        item, cat_label = hit
        resolved.append({
            "id": item["id"],
            "name": item["name"],
            "category": cat_label,
            "qty": line.qty,
            "unit_price": item["price"],
            "line_total": round(item["price"] * line.qty, 2),
        })

    if not resolved:
        raise HTTPException(status_code=400, detail="Cart is empty")

    subtotal = round(sum(i["line_total"] for i in resolved), 2)
    tax = round(subtotal * TAX_RATE, 2)
    delivery_fee = round(DELIVERY_FEE, 2) if is_delivery else 0.0

    if is_delivery and DELIVERY_MIN_ORDER > 0 and subtotal < DELIVERY_MIN_ORDER:
        raise HTTPException(
            status_code=400,
            detail=f"Delivery orders require a minimum of {_money(DELIVERY_MIN_ORDER)}",
        )

    total = round(subtotal + tax + delivery_fee, 2)
    eta_minutes = DELIVERY_ETA_MIN if is_delivery else PICKUP_ETA_MIN

    order_id = str(uuid.uuid4())[:6].upper()
    now = datetime.now(timezone.utc).isoformat()

    order = {
        "id": order_id,
        "customer_name": req.customer_name.strip(),
        "phone": req.phone.strip(),
        "order_type": order_type,
        "pickup_time": (req.pickup_time or "").strip() if not is_delivery else "",
        "delivery_address": delivery_address,
        "notes": (req.notes or "").strip(),
        "items": resolved,
        "subtotal": subtotal,
        "tax": tax,
        "delivery_fee": delivery_fee,
        "total": total,
        "eta_minutes": eta_minutes,
        "status": "new",
        "created_at": now,
    }

    # Persist
    orders = _load_orders()
    orders.insert(0, order)
    _save_orders(orders)

    # SMS: kitchen order + customer receipt
    kitchen_result = send_sms(COOK_PHONE, _kitchen_sms(order)) if COOK_PHONE else {"ok": False, "error": "no cook phone configured"}
    receipt_result = send_sms(order["phone"], _receipt_sms(order))

    return {
        "ok": True,
        "order": order,
        "notifications": {
            "kitchen": kitchen_result,
            "receipt": receipt_result,
        },
    }


@app.get("/api/orders")
def list_orders(limit: int = 50):
    orders = _load_orders()
    return {"count": len(orders), "orders": orders[:limit]}


@app.post("/api/orders/{order_id}/status")
def set_status(order_id: str, request: Request):
    """Mark an order ready/completed (cook dashboard action)."""
    body = request.json if hasattr(request, "json") else {}
    new_status = (body or {}).get("status", "completed")
    orders = _load_orders()
    for o in orders:
        if o["id"] == order_id:
            o["status"] = new_status
            _save_orders(orders)
            return {"ok": True, "order": o}
    raise HTTPException(status_code=404, detail="Order not found")


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(_env("JENNY_PORT", "8089"))
    uvicorn.run(app, host="0.0.0.0", port=port)
