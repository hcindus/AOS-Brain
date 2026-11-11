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
            "sku": p["sku"], "name": p["name"], "spec": p["spec"], "pack": p.get("pack",""),
            "qty": qty, "sell": sell, "cost": c, "vendor": p.get("vendor"),
        })
    tax = round(subtotal * tax_rate, 2)
    shipping = shipping_for(items)
    total = round(subtotal + tax + shipping, 2)
    margin = round(subtotal - cost, 2)
    return {
        "lines": lines, "subtotal": round(subtotal, 2), "tax": tax,
        "shipping": shipping, "total": total, "cost": round(cost, 2), "margin": margin,
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
    """PO number = SLS- + MMDDYY + 3-digit sequence (sales orders, distinct from customer POs)."""
    today = _dt.datetime.now()
    mmddyy = today.strftime("%m%d%y")
    try:
        seq = int(open(_PO_SEQ_FILE).read().strip())
    except Exception:
        seq = 0
    seq += 1
    open(_PO_SEQ_FILE, "w").write(str(seq))
    return f"SLS-{mmddyy}{seq:03d}"

def order_email(order):
    """Full order email in the production format."""
    lines = order["lines"]
    po = _next_po()
    order["po"] = po
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

    tax_pct = f"{order['tax_rate'] * 100:g}%"
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
Shipping: ${order['shipping']:.2f}
Tax ({tax_pct}): ${order['tax']:.2f}
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


# --- free-text order parser -> structured items ---
import re as _re

def parse_order(text):
    """Parse free-text order (e.g. '1 dozen 62245 ribbons') -> [{sku, qty}]."""
    if not text:
        return []
    catalog = load_catalog()
    items = []
    seen = set()
    for p in catalog["products"]:
        sku = p["sku"]
        pat = _re.compile(r'(?i)(?<![a-z0-9])' + _re.escape(sku) + r'(?![a-z0-9])')
        for m in pat.finditer(text):
            # quantity: nearest number within ~24 chars before the SKU
            prefix = text[max(0, m.start()-24):m.start()].lower()
            nums = _re.findall(r'\b(\d+)\b', prefix)
            qty = int(nums[-1]) if nums else 1
            if sku not in seen:
                items.append({"sku": sku, "qty": qty})
                seen.add(sku)
    return items


# --- shipping + customer-facing output ---
SHIPPING_PAPER = 17.72   # per item (paper: per pack/case)
RIBBON_SKUS = ("62245", "67240")

def shipping_for(items):
    """Shipping is per item. Ribbons (62245/67240) = $1 per dozen (up to qty 12 = $1);
    everything else = $17.72 per item."""
    total = 0.0
    for it in items:
        sku = it["sku"]; qty = it["qty"]
        if sku in RIBBON_SKUS:
            total += 1.00 * ((qty + 11) // 12)   # $1 per 12 ribbons
        else:
            total += SHIPPING_PAPER * qty
    return round(total, 2)

def _fmt(n):
    return f"${n:,.2f}"

def customer_email(order):
    """Customer thank-you email body (matches production wording)."""
    po = order.get("po")
    return (f"Thank you for your order!\n\n"
            f"Your order number is {po}. Please find a courtesy invoice attached.\n\n"
            f"We'll process your order and send tracking as soon as it ships.\n\n"
            f"Thank you,\nPerformance Supply Depot LLC")

def courtesy_invoice_html(order):
    """Courtesy invoice HTML (matches the production PDF layout)."""
    po = order.get("po")
    rows = "".join(
        f"<tr><td>{l['name']} {l['spec']} ({l['pack']})</td>"
        f"<td style='text-align:center'>{l['qty']}</td>"
        f"<td style='text-align:right'>{_fmt(l['sell']/l['qty'] if l['qty'] else l['sell'])}</td>"
        f"<td style='text-align:right'>{_fmt(l['sell'])}</td></tr>"
        for l in order["lines"]
    )
    ship = order.get("shipping", 0.0)
    grand = order["total"]
    tax_pct = f"{order['tax_rate']*100:g}%"
    return f"""<html><body style="font-family:Arial,sans-serif;font-size:13px;color:#111">
<div style="text-align:center;font-size:16px;font-weight:bold">Performance Supply Depot LLC</div>
<div style="text-align:center">1880 Oak Point Court, Fairfield, CA 94534</div>
<div style="text-align:center">888-881-6834 &bull; info@psdepot.com</div>
<hr>
<p><em>Please find a courtesy invoice for your order. Thank you!</em></p>
<p><strong>PO Number:</strong> {po}<br><strong>Order Date:</strong> {order.get('date','')}</p>
<p><strong>Bill To / Ship To:</strong><br>
{order.get('business_name','')}<br>
{order.get('address','')}<br>
{order.get('city','')}, {order.get('state','')} {order.get('zip','')}</p>
<table width="100%" cellpadding="6" style="border-collapse:collapse">
<tr style="background:#eee">
<th style="text-align:left">Description</th><th>Qty</th>
<th style="text-align:right">Unit Price</th><th style="text-align:right">Line Total</th></tr>
{rows}
</table>
<p style="text-align:right">
Subtotal {_fmt(order['subtotal'])}<br>
Shipping {_fmt(ship)}<br>
Tax ({tax_pct}) {_fmt(order['tax'])}<br>
<strong>Total {_fmt(grand)}</strong>
</p>
</body></html>"""


def courtesy_invoice_pdf(order, path):
    """Generate a courtesy-invoice PDF (matches the production PDF layout) via reportlab."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

    styles = getSampleStyleSheet()
    c = ParagraphStyle('c', parent=styles['Normal'], alignment=1, fontSize=9, leading=12)
    b = ParagraphStyle('b', parent=styles['Normal'], alignment=1, fontSize=14, leading=16)
    l = ParagraphStyle('l', parent=styles['Normal'], fontSize=9, leading=12)
    r = ParagraphStyle('r', parent=styles['Normal'], alignment=2, fontSize=9, leading=13)

    ship = order.get("shipping", 0.0)
    tax_pct = f"{order['tax_rate']*100:g}%"
    po = order.get("po")

    story = [
        Paragraph("Performance Supply Depot LLC", b),
        Paragraph("1880 Oak Point Court, Fairfield, CA 94534", c),
        Paragraph("888-881-6834 &bull; info@psdepot.com", c),
        Spacer(1, 8),
        HRFlowable(width="100%", thickness=0.7, color=colors.black),
        Spacer(1, 8),
        Paragraph("<i>Please find a courtesy invoice for your order. Thank you!</i>", l),
        Spacer(1, 8),
        Paragraph(f"<b>PO Number:</b> {po}", l),
        Paragraph(f"<b>Order Date:</b> {order.get('date','')}", l),
        Spacer(1, 8),
        Paragraph("<b>Bill To / Ship To:</b>", l),
        Paragraph(order.get("business_name",""), l),
        Paragraph(order.get("address",""), l),
        Paragraph(f"{order.get('city','')}, {order.get('state','')} {order.get('zip','')}", l),
        Spacer(1, 12),
    ]

    # order details table
    data = [[Paragraph("<b>Description</b>", l), Paragraph("<b>Qty</b>", c), Paragraph("<b>Unit Price</b>", r), Paragraph("<b>Line Total</b>", r)]]
    for ln in order["lines"]:
        unit = ln["sell"] / ln["qty"] if ln["qty"] else ln["sell"]
        data.append([
            Paragraph(f"{ln['name']} {ln['spec']} ({ln['pack']})", l),
            Paragraph(str(ln["qty"]), c),
            Paragraph(_fmt(unit), r),
            Paragraph(_fmt(ln["sell"]), r),
        ])
    tbl = Table(data, colWidths=[3.4*inch, 0.7*inch, 1.2*inch, 1.2*inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#eeeeee")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 12))

    # totals
    story.append(Paragraph(f"Subtotal {_fmt(order['subtotal'])}", r))
    story.append(Paragraph(f"Shipping {_fmt(ship)}", r))
    story.append(Paragraph(f"Tax ({tax_pct}) {_fmt(order['tax'])}", r))
    story.append(Paragraph(f"<b>Total {_fmt(order['total'])}</b>", r))

    SimpleDocTemplate(path, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch,
                      leftMargin=0.9*inch, rightMargin=0.9*inch).build(story)
    return path
