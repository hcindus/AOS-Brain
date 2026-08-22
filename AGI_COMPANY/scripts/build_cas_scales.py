#!/usr/bin/env python3
"""Build 6 new CAS scale pages (from cas-pdn-series.html template) + recycle 5 'cash register' pages into SAM4S printers/kiosk."""
import os, re, json, shutil, copy

PROD = "/var/www/psdepot.com/products"
MCD = os.path.join(PROD, "mscashdrawer")
SCALE_TMPL = os.path.join(PROD, "cas-pdn-series.html")
ARCHIVE = os.path.join(MCD, "_archive")

# ---------------------------------------------------------------------------
# CAS SCALES
# ---------------------------------------------------------------------------
SCALES = [
    dict(
        slug="cas-cl7200", name="CAS CL7200 Touchscreen Label Printing Scale",
        sku="CL7200", price=3069.00,
        desc="The CAS CL7200 touchscreen label-printing scale delivers crisp, easy-to-read labels with a responsive 10.2-inch color touch display and a 7-inch customer display. Built for weighing and label printing in supermarkets, groceries, and retail.",
        features=[
            ("📱 10.2\" Color Touch Display", "Responsive full-color touchscreen with rich, colorful keyboard graphics."),
            ("🖨️ Thermal Label Printing", "Crisp labels with UPC-A, EAN13, Code39/93/128, Codabar barcodes."),
            ("🔗 Full Connectivity", "USB, Serial, Ethernet, and Wi-Fi interfaces."),
            ("✅ NTEP Certified", "NTEP approved (AM-6087, 17-096). Legal for trade."),
        ],
        specs=[("Display","LCD (dual range)"),("Units","LB, KG"),("Printer","Thermal label"),
               ("Barcode","UPC-A, EAN13, EAN13A5, I2OF5, Code39, Code93, Code128, Codabar"),
               ("Interface","USB, Serial, Ethernet, Wi-Fi"),("Platter","15\" x 9.75\" (380 x 250 mm)"),
               ("Measurement Canada","Yes"),("Warranty","One Year")],
        included=["CAS CL7200 Touchscreen Label Printing Scale","Power adapter","Quick start guide","One-year manufacturer warranty"],
    ),
    dict(
        slug="cas-cl3000", name="CAS CL3000 Label Printing Scale",
        sku="CL3000", price=1744.00,
        desc="The CAS CL3000 label-printing scale saves time and money while producing clear, professional product labels. Designed for today's fast-paced retail environment with CL Works Pro software support.",
        features=[
            ("🏷️ Professional Labels", "Clear, compliant product labels for retail and grocery."),
            ("💻 CL Works Pro", "Database and label management software."),
            ("⚖️ Retail Grade", "Built for supermarket and grocery weighing + labeling."),
            ("✅ NTEP Certified", "Legal for trade."),
        ],
        specs=[("Type","Label printing scale"),("Software","CL Works Pro"),
               ("Country","South Korea"),("Warranty","One Year")],
        included=["CAS CL3000 Label Printing Scale","Power adapter","Quick start guide","One-year manufacturer warranty"],
    ),
    dict(
        slug="cas-pd-2z", name="CAS PD-2Z POS Interface Scale",
        sku="PD-2Z", price=661.00,
        desc="The CAS PD-2Z POS interface scale connects with cash registers or POS systems in 15 to 150 lb capacities. Works with UPS Worldship software. Best for supermarkets, specialty stores, and shipping.",
        features=[
            ("🔌 POS Interface", "Links directly to cash registers and POS systems."),
            ("📦 UPS Worldship", "Works with UPS Worldship shipping software."),
            ("⚖️ 15–150 lb", "Multiple capacities for any operation."),
            ("✅ NTEP Certified", "Legal for trade (92-174A4)."),
        ],
        specs=[("Capacity","15 / 30 / 60 / 150 lb"),("Display","VFD (dual range)"),
               ("Units","LB, OZ"),("Platter","15.3\" x 11.06\""),
               ("Warranty","Two Years"),("Country","China")],
        included=["CAS PD-2Z POS Interface Scale","Power adapter","Quick start guide","Two-year manufacturer warranty"],
    ),
    dict(
        slug="cas-sw-rs", name="CAS SW-RS POS & Portion Control Scale",
        sku="SW-RS", price=486.00,
        desc="The CAS SW-RS functions as both a POS interface scale and a portion-control scale. Compact and easy to clean — perfect for restaurants, cafeterias, and farmers markets.",
        features=[
            ("🍽️ Dual Function", "POS interface + portion control in one compact unit."),
            ("🧼 Easy to Clean", "Compact footprint for food-service environments."),
            ("⚖️ Multiple Units", "Weighs in LB, KG, OZ, and grams."),
            ("✅ NTEP Certified", "Legal for trade (AM-5695, 99-002A1)."),
        ],
        specs=[("Capacity","10 / 20 lb, 10 / 5 kg"),("Display","5-digit LCD (1\")"),
               ("Units","LB, KG, OZ, Grams"),("Platter","9.1\" x 7.5\""),
               ("Measurement Canada","Yes"),("Warranty","One Year")],
        included=["CAS SW-RS POS & Portion Control Scale","AC adapter","Quick start guide","One-year manufacturer warranty"],
    ),
    dict(
        slug="cas-s2000-jr", name="CAS S2000 Jr Price Computing Scale",
        sku="S2000-JR", price=374.00,
        desc="The CAS S2000 Jr is a full-featured price-computing scale in three capacities. Dual displays show total price, weight, and unit price. Includes a rechargeable battery with up to 200 hours of run time — ideal for retail, farmers markets, and candy stores.",
        features=[
            ("💰 Price Computing", "Total price, weight, and unit price at a glance."),
            ("🔋 200-Hour Battery", "Rechargeable battery for locations without AC power."),
            ("📺 Dual Displays", "Operator and customer view simultaneously."),
            ("✅ NTEP Certified", "Legal for trade."),
        ],
        specs=[("Type","Price computing scale"),("Display","LCD (dual range)"),
               ("Battery","Rechargeable (200 hr)"),("Options","DT2X label printer, produce/fish platter"),
               ("Warranty","Two Years")],
        included=["CAS S2000 Jr Price Computing Scale","Stainless steel platter","AC/DC adapter","Owner's manual","Two-year manufacturer warranty"],
    ),
    dict(
        slug="cas-tracker-r457", name="CAS Tracker-R457 Label & Traceability System",
        sku="R457", price=None,
        desc="The CAS Tracker-R457 provides label printing, data collection, and traceability in one package for meat, seafood, poultry, produce, and distribution — built for washdown environments.",
        features=[
            ("🧾 Label + Traceability", "Piece, box, case, and pallet labeling."),
            ("🔖 Full Barcode Support", "UPC, EAN, Code39, Code128, QR, GTIN, GS1-128."),
            ("🧼 Stainless Washdown", "R457 SMART stainless enclosure."),
            ("📊 Data Export", "CSV transaction export for reporting."),
        ],
        specs=[("Indicator","R457 SMART stainless steel"),("Label Types","Piece / Box / Case / Pallet"),
               ("Barcode","UPC, EAN, Code39, Code128, QR, GTIN, GS1-128"),
               ("Environment","Washdown"),("Warranty","One Year")],
        included=["CAS Tracker-R457 controller","Configuration software","Quick start guide","One-year manufacturer warranty"],
    ),
]

def build_scale(s):
    html = open(SCALE_TMPL).read()
    slug = s["slug"]
    price_s = f'${s["price"]:,.2f}' if s["price"] is not None else "Call for Pricing"
    price_num = s["price"] if s["price"] is not None else 0

    # title + meta + canonical
    html = html.replace("<title>CAS PDN Series POS Interface Scale | Performance Supply Depot LLC</title>",
                        f"<title>{s['name']} | Performance Supply Depot LLC</title>")
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{s["desc"]}">', html, count=1)
    html = html.replace("https://psdepot.com/products/cas-pdn-series.html",
                        f"https://psdepot.com/products/{slug}.html")

    # schema: name, sku, price, image, description
    html = html.replace('"name": "CAS PDN Series POS Interface Scale"', f'"name": "{s["name"]}"')
    html = html.replace('"sku": "PDN-12"', f'"sku": "{s["sku"]}"')
    html = re.sub(r'"price": \d+\.\d+', f'"price": {price_num}', html, count=1)
    html = html.replace('"image": "https://psdepot.com/assets/images/scale-pdn.jpg"',
                        f'"image": "https://psdepot.com/assets/images/{slug}.jpg"')
    html = re.sub(r'"description": "CAS PDN Series[^"]*"', f'"description": "{s["desc"]}"', html, count=1)

    # image placeholder + caption
    html = html.replace('<div style="font-size: 18px; font-weight: 600;">CAS PDN Series</div>',
                        f'<div style="font-size: 18px; font-weight: 600;">{s["name"]}</div>')
    html = html.replace('<div style="font-size: 14px; margin-top: 8px;">POS Interface Scale</div>',
                        '<div style="font-size: 14px; margin-top: 8px;">CAS Scale</div>')
    html = html.replace('<p class="image-caption">CAS PDN Series — USB Powered POS Interface Scale with LED Display</p>',
                        f'<p class="image-caption">{s["name"]}</p>')

    # sku + h1
    html = html.replace('<div class="product-sku">SKU: PDN-12/30/60</div>',
                        f'<div class="product-sku">SKU: {s["sku"]}</div>')
    html = html.replace('<h1>CAS PDN Series POS Interface Scale</h1>',
                        f'<h1>{s["name"]}</h1>')

    # price display
    html = html.replace('<span class="current-price">$599.00</span>', f'<span class="current-price">{price_s}</span>')
    html = re.sub(r'<span class="original-price">\$[0-9.,]+</span>', '', html, count=1)
    html = re.sub(r'<span class="discount-badge">[^<]*</span>', '', html, count=1)

    # features grid (4 cards)
    features_html = "".join(
        f'<div class="feature-card"><h3>{t}</h3><p>{d}</p></div>' for t, d in s["features"]
    )
    html = re.sub(r'<div class="features-grid">.*?</div>\s*</section>', 
                  f'<div class="features-grid">{features_html}</div>\n        </section>', html, count=1, flags=re.S)

    # description text
    html = html.replace("Say goodbye to complicated weighing processes and hello to seamless transactions with the CAS PDN POS Interface Scale. The CAS PDN scale works together with your Point of Sale (POS) system or ECR. Product weights are transferred directly into the transaction. No manual entry, no delays – just a swift and accurate sale.",
                        s["desc"])

    # specs table (replace the whole thead+tbody with a simple 2-col table)
    rows = "".join(f'<tr><td><strong>{k}</strong></td><td>{v}</td></tr>' for k, v in s["specs"])
    specs_table = f'<table><thead><tr><th>Specification</th><th>Details</th></tr></thead><tbody>{rows}</tbody></table>'
    html = re.sub(r'<div class="specs-table">.*?</div>\s*</div>', 
                  f'<div class="specs-table">{specs_table}</div>\n        </div>', html, count=1, flags=re.S)

    # what's included
    included = "".join(f"<li>{x}</li>" for x in s["included"])
    html = re.sub(r'<h3>What\'s Included</h3>\s*<ul>.*?</ul>',
                  f'<h3>What\'s Included</h3><ul>{included}</ul>', html, count=1, flags=re.S)

    # addToCart JS
    html = html.replace("sku: 'PDN-12'", f"sku: '{s['sku']}'")
    html = html.replace("name: 'CAS PDN Series POS Interface Scale'", f"name: '{s['name']}'")
    html = html.replace("price: 599.00", f"price: {price_num}")

    # remove stale related-products LP-1000 link (leave as-is, harmless)

    out = os.path.join(PROD, f"{slug}.html")
    open(out, "w").write(html)
    return out

for s in SCALES:
    out = build_scale(s)
    print(f"✅ {os.path.basename(out)}  ({s['name']})  price={s['price']}")

print(f"\nDone: {len(SCALES)} CAS scale pages written to {PROD}/")
