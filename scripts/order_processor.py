#!/usr/bin/env python3
"""
PSD Order Processor — my own pipeline (separate from the Google form).
Computes subtotal + tax (flat 9%) + margin, and generates a vendor-format order
block, from a structured order (SKU + quantity).
"""
import json

CATALOG_PATH = "/root/.openclaw/workspace/datadepot/data/psdepot_catalog.json"

def load_catalog():
    return json.load(open(CATALOG_PATH))

def process_order(items):
    """items = list of {sku, qty}. Returns full order summary."""
    cat = load_catalog()
    tax_rate = cat["tax_rate"]
    lines = []
    subtotal = 0.0
    cost = 0.0
    for it in items:
        p = next((x for x in cat["products"] if x["sku"] == it["sku"]), None)
        if not p:
            continue
        qty = it["qty"]
        sell = round(p["sell"] * qty, 2)
        c = round(p["cost"] * qty, 2) if p.get("cost") is not None else 0.0
        subtotal += sell
        cost += c
        lines.append({
            "sku": p["sku"], "name": p["name"], "spec": p["spec"],
            "qty": qty, "sell": sell, "cost": c, "vendor": p.get("vendor"),
        })
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)
    margin = round(subtotal - cost, 2)
    return {
        "lines": lines, "subtotal": round(subtotal, 2), "tax": tax,
        "total": total, "cost": round(cost, 2), "margin": margin,
        "margin_pct": round((margin / subtotal * 100), 1) if subtotal else 0,
        "tax_rate": tax_rate,
    }

def vendor_lines(order):
    """Vendor copy-paste order block (vendor part # + qty + cost)."""
    out = []
    for l in order["lines"]:
        if l["vendor"]:
            out.append(f"{l['vendor']} {l['name'].upper()} ({l['spec']})\n{qty_str(l)}")
    return "\n".join(out)

def qty_str(l):
    return f"{l['qty']}.00 CT {l['cost']:.2f}"

if __name__ == "__main__":
    o = process_order([{"sku": "62245", "qty": 1}, {"sku": "67240", "qty": 1}])
    print(json.dumps(o, indent=2))


# --- PO number + full email (matches the production form's output format) ---
import datetime as _dt

_PO_SEQ_FILE = "/root/.openclaw/workspace/datadepot/data/po_seq.txt"

def _next_po():
    """PO number = MMDDYY + 3-digit daily sequence (e.g. 110926002)."""
    today = _dt.datetime.now()
    mmddyy = today.strftime("%m%d%y")
    try:
        seq = int(open(_PO_SEQ_FILE).read().strip())
    except Exception:
        seq = 0
    seq += 1
    open(_PO_SEQ_FILE, "w").write(str(seq))
    return f"{mmddyy}{seq:03d}"

def order_email(order):
    """Full order email in the production format."""
    lines = order["lines"]
    po = _next_po()
    ship = f"{order.get('address','')}\n{order.get('city','')}, {order.get('state','')} {order.get('zip','')}"
    ordered_items = "\n".join(f"{l['name']} ({l['pack']}): {l['qty']}" for l in lines)

    profit_blocks = []
    for l in lines:
        p = l["sell"] - l["cost"]
        pct = round(p / l["sell"] * 100, 1) if l["sell"] else 0
        profit_blocks.append(
            f"{l['name']} ({l['pack']})\nQty: {l['qty']}\nCost: ${l['cost']:.2f}\n"
            f"Sell: ${l['sell']:.2f}\nLine Profit: ${p:.2f} ({pct}%)"
        )
    profit = "\n\n".join(profit_blocks)

    vendor = "\n".join(
        f"{l['vendor']} {l['name'].upper()}\n{l['qty']}.00 CT {l['cost']:.2f}" for l in lines if l.get("vendor")
    )

    tax_pct = int(order["tax_rate"] * 100)
    return f"""Performance Supply Depot LLC
psdepot.com • 888-881-6834 • info@psdepot.com

PO Number:
{po}

New Customer Order Submitted

Business Name:
{order.get('business_name','')}

Manager:
{order.get('manager_name','')}
{order.get('email','')}

Ship To:
{ship}

Order Date:
{order.get('date','')}

Ordered Items:
{ordered_items}

----------------------------------------
PROFIT SUMMARY (INTERNAL ONLY)
----------------------------------------

{profit}

----------------------------------------
TOTALS
----------------------------------------
Subtotal (Sell): ${order['subtotal']:.2f}
Shipping: $0.00
Tax ({tax_pct}%): ${order['tax']:.2f}
Grand Total: ${order['total']:.2f}

Total Cost: ${order['cost']:.2f}
Total Profit: ${order['margin']:.2f} ({order['margin_pct']}%)

Special Instructions:
{order.get('special_instructions','')}

----------------------------------------
VENDOR ORDER FORMAT (COPY & PASTE BELOW)
----------------------------------------

{vendor}

Thank you,
Performance Supply Depot LLC"""
