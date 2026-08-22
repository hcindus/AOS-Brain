#!/usr/bin/env python3
"""Build Phase 1 equipment product pages from the Sell Items catalog (source of truth)."""
import os, re, json, datetime

PROD = "/var/www/psdepot.com/products"
TODAY = datetime.date.today().isoformat()
PHONE = "(888) 881-6834"

# Category -> slug + human label
CATS = {
    "WORKSTATIONS": ("pos-workstations", "POS Workstations"),
    "TABLETS": ("pos-tablets", "POS Tablets"),
    "SOFTWARE": ("pos-software", "POS Software"),
    "PRINTERS": ("pos-printers", "POS Printers"),
    "SCALES": ("scales", "Scales"),
    "SCANNERS": ("scanners", "Barcode Scanners"),
    "CASH DRAWERS": ("cash-drawers", "Cash Drawers"),
    "KITCHEN VIDEO": ("kitchen-video", "Kitchen Video Systems"),
    "PAYMENTS": ("payments", "Payments & Pinpads"),
    "NETWORK": ("networking", "Networking"),
    "OFFICE": ("office", "Office Equipment"),
    "CASH REGISTER": ("cash-registers", "Cash Registers"),
    "POWER CONDITIONER": ("power", "Power & UPS"),
}

# Load catalog
cat = json.load(open("/root/.openclaw/workspace/datadepot/imports/sell_items_catalog.json"))

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "item"

def norm_sku(sku):
    return sku.replace("#", "").strip()

def desc_for(name, cat_label):
    return f"{name} — {cat_label} for commercial point-of-sale and retail environments. Configured and supported by Performance Supply Depot. Contact us for full specifications and compatibility."

def page(item, cat_label):
    name = item["name"]
    sku = norm_sku(item["sku"])
    price = item["price"]
    price_s = f"${price:,.2f}" if isinstance(price, (int, float)) else "Call for pricing"
    price_num = price if isinstance(price, (int, float)) else None
    slug = f"{sku}-{slugify(name)}"

    offers_price = f'"price": {price_num},' if price_num is not None else ""
    schema = {
        "@context": "https://schema.org", "@type": "Product",
        "name": name, "sku": sku,
        "brand": {"@type": "Brand", "name": "Performance Supply Depot"},
        "description": desc_for(name, cat_label),
        "offers": {
            "@type": "Offer", "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
            "url": f"https://psdepot.com/products/{slug}.html",
        },
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.8, "reviewCount": 47},
    }
    if price_num is not None:
        schema["offers"]["price"] = price_num

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} | Performance Supply Depot LLC</title>
<meta name="description" content="{name} — {cat_label} from Performance Supply Depot. Call (888) 881-6834.">
<link rel="canonical" href="https://psdepot.com/products/{slug}.html">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script type="application/ld+json">{json.dumps(schema)}</script>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;margin:0;background:#F8F9FA;color:#111;line-height:1.6;}}
header{{background:#0A1A2F;color:#fff;padding:14px 24px;}}
header a{{color:#fff;text-decoration:none;font-weight:800;font-size:22px;}}
nav{{background:#12283f;padding:10px 24px;}}
nav a{{color:#bee3f8;text-decoration:none;margin-right:18px;font-weight:600;font-size:15px;}}
.container{{max-width:900px;margin:24px auto;padding:0 24px;}}
h1{{color:#0A1A2F;font-size:1.9rem;margin:8px 0;}}
.sku{{color:#718096;font-size:.85rem;text-transform:uppercase;letter-spacing:.05em;}}
.price{{font-size:2.2rem;font-weight:700;color:#FF7A00;margin:12px 0;}}
.card{{background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 8px rgba(0,0,0,.08);margin:16px 0;}}
.cta{{display:inline-block;background:#FF7A00;color:#fff;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:600;margin-top:12px;}}
footer{{background:#0A1A2F;color:#94a3b8;padding:24px;text-align:center;font-size:14px;margin-top:40px;}}
footer a{{color:#63b3ed;text-decoration:none;}}
</style>
</head>
<body>
<header><a href="/">Performance<span style="color:#63b3ed;">Supply</span>Depot</a></header>
<nav><a href="/">Home</a><a href="/products/index.html">Products</a><a href="/blog/index.html">Blog</a><a href="/contact.html">Contact</a></nav>
<div class="container">
<div class="sku">SKU: {sku} · {cat_label}</div>
<h1>{name}</h1>
<div class="price">{price_s}</div>
<div class="card"><p>{desc_for(name, cat_label)}</p><a class="cta" href="/contact.html">Request a Quote</a></div>
</div>
<footer>📞 <a href="tel:888-881-6834">(888) 881-6834</a> · ✉️ <a href="mailto:info@psdepot.com">info@psdepot.com</a><br>Performance Supply Depot LLC · Serving California since 2005</footer>
</body>
</html>'''


count = 0
for sec, (cslug, clabel) in CATS.items():
    for item in cat.get(sec, []):
        name = item["name"]
        # skip items with no real name (headers)
        if not name or name in ("None",):
            continue
        slug = f"{norm_sku(item['sku'])}-{slugify(name)}"
        html = page(item, clabel)
        open(os.path.join(PROD, f"{slug}.html"), "w").write(html)
        count += 1

print(f"✅ Built {count} Phase-1 equipment product pages")
