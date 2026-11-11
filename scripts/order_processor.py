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
