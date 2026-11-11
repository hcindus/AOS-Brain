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
SHIPPING_RATE = 17.72   # base rate, applied per unit (paper = per case; ribbons = per 2 dozen)
RIBBON_SKUS = ("62245", "67240")

def shipping_for(items):
    """Shipping:
      - Paper: $17.72 per case (1 item = 1 case).
      - Ribbons (62245/67240): $17.72 flat for up to 1 gross (144 ribbons = 12 dozen),
        then $17.72 per additional gross, rounded up."""
    total = 0.0
    for it in items:
        sku = it["sku"]; qty = it["qty"]
        if sku in RIBBON_SKUS:
            total += SHIPPING_RATE * ((qty + 143) // 144)   # $17.72 per gross (144 ribbons)
        else:
            total += SHIPPING_RATE * qty
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

    def _footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(letter[0]/2, 0.5*inch,
            "Performance Supply Depot LLC \u2022 1880 Oak Point Court, Fairfield, CA 94534")
        canvas.drawCentredString(letter[0]/2, 0.35*inch,
            "888-881-6834 \u2022 info@psdepot.com \u2022 psdepot.com")
        canvas.drawCentredString(letter[0]/2, 0.2*inch,
            "Thank you for your business!")
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.9*inch,
                            leftMargin=0.9*inch, rightMargin=0.9*inch)
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return path


# --- payment thank-you (post-collection) ---
from urllib.parse import urlencode as _urlencode

def payment_thank_you_link(date, ref, amount, method, name):
    """Build the thank-you-payment.html URL with the customer's fields pre-filled."""
    params = _urlencode({
        "date": date, "ref": ref, "amount": amount,
        "method": method, "name": name,
    })
    return f"https://psdepot.com/thank-you-payment.html?{params}"

def payment_thank_you_email_html(date, ref, amount, method, name):
    """HTML email body: thank-you + link to the pre-filled thank-you page."""
    link = payment_thank_you_link(date, ref, amount, method, name)
    amt = f"${float(amount):,.2f}" if amount else ""
    return f"""<html><body style="font-family:Arial,sans-serif;color:#111;font-size:14px">
<p>Dear {name},</p>
<p>Thank you for your payment of <strong>{amt}</strong> on {date}.</p>
<p>We truly appreciate your business. Your transaction is confirmed:</p>
<ul>
<li><strong>Reference:</strong> {ref}</li>
<li><strong>Amount:</strong> {amt}</li>
<li><strong>Method:</strong> {method}</li>
</ul>
<p style="margin:24px 0">
<a href="{link}" style="background:#2d5a87;color:#fff;padding:12px 24px;border-radius:8px;
text-decoration:none;font-weight:bold;display:inline-block">View Your Payment Receipt</a>
</p>
<p>Or copy this link:<br><a href="{link}">{link}</a></p>
<p>— Performance Supply Depot LLC<br>
psdepot.com &bull; 888-881-6834 &bull; info@psdepot.com</p>
</body></html>"""


# --- vendor order routing ---
VENDORS = {
    "DOMTAR": {"to": "customersupport.pos@domtar.com", "cc": "arlene.belarde@domtar.com"},
    "ACM":    {"api": "https://api.acm.com/orders", "mode": "demo"},  # placeholder, no real key yet
}

VENDOR_BY_SKU = {
    "PF-230": "DOMTAR", "PF-157": "DOMTAR", "18-333": "DOMTAR",
    "CC-235": "DOMTAR", "13-305": "DOMTAR", "PF-175": "DOMTAR",
    "62245": "ACM", "67240": "ACM",
}

DESC_VENDOR = {
    "PF-230": "9078-2489 3 1/8 X 230 48G NP 50RL/CTN",
    "PF-157": "9078-0473 2 1/4 X 230 48G NP 50RL/CTN",
    "18-333": "3-PLY 3\" 50RL/CTN",
    "CC-235": "9077-0047 3 X 90 MULTI PLY W/C 50 RLS/CTN",
    "13-305": "9074-0243 3 x 165' BOND 50 RL/CTN",
    "PF-175": "9078-0175 2 1/4 X 74 48G NP 50RL/CTN",
    "62245": "38619ERC30BR EPSON COMPATIBLE RIBBON (ERC-30/34/38)",
    "67240": "51619RC700BR STAR SP700 COMPATIBLE RIBBON",
}

def vendor_order_email(order):
    """Build blind-drop vendor PO emails (Domtar for paper; ACM items flagged for API)."""
    po = order.get("po")
    ship_to = order.get("business_name") or order.get("address") or ""
    attention = order.get("manager_name") or ""
    notes = order.get("special_instructions") or ""

    _cat = {p["sku"]: p for p in load_catalog()["products"]}
    domtar_lines = []
    acm_lines = []
    for l in order["lines"]:
        sku = l["sku"]
        p = _cat.get(sku, {})
        v = p.get("vendor_name") or VENDOR_BY_SKU.get(sku, "DOMTAR")
        desc = DESC_VENDOR.get(sku, f"{p.get('vendor', l.get('vendor',''))} {p.get('name', l['name'])}")
        if v == "ACM":
            acm_lines.append((l, desc))
        else:
            domtar_lines.append((l, desc))

    out = {"domtar": None, "acm": acm_lines}

    if domtar_lines:
        items = "".join(f"{desc}\nQty: {l['qty']} {('dozen' if l['sku'] in ('62245','67240') else 'case')}\n\n"
                        for l, desc in domtar_lines)
        body = (f"Please process the following blind drop order:\n\n"
                f"PO Number: {po}\n"
                f"Ship To: {ship_to}\n"
                f"Attention: {attention}\n\n"
                f"Items:\n------\n{items}"
                f"Special Instructions: {notes or 'None'}\n\n"
                f"Thank you,\nPerformance Supply Depot LLC")
        out["domtar"] = {
            "to": VENDORS["DOMTAR"]["to"], "cc": VENDORS["DOMTAR"]["cc"],
            "subject": f"Blind Drop PO {po} - {ship_to}",
            "body": body,
        }
    return out


# --- vendor email switch (default OFF for safety) ---
import os as _os
_VENDOR_SWITCH = "/root/.openclaw/workspace/datadepot/data/vendor_email_switch.json"

def vendor_emails_enabled():
    """True only if the vendor-email switch is explicitly flipped on."""
    try:
        return bool(json.load(open(_VENDOR_SWITCH)).get("vendor_emails_enabled", False))
    except Exception:
        return False

def set_vendor_emails(enabled):
    json.dump({"vendor_emails_enabled": bool(enabled)}, open(_VENDOR_SWITCH, "w"), indent=2)
    return bool(enabled)
