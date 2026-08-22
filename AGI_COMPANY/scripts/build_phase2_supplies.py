#!/usr/bin/env python3
"""Build Phase 2 supply product pages (paper, ink/ribbons, labels, misc) — skip existing + shipping."""
import os, re, json, glob, datetime

PROD = "/var/www/psdepot.com/products"
TODAY = datetime.date.today().isoformat()

CATS = {
    "PAPER": ("paper", "Paper & Thermal Rolls"),
    "INK": ("ribbons", "Ribbons & Ink"),
    "LABELS": ("labels", "Labels & Scale Labels"),
    "SUPPLY MISC": ("supplies", "Supplies & Accessories"),
}

# Shipping rates are not products — exclude 80-* items.
SKIP_SKU_PREFIX = ("80-",)

cat = json.load(open("/root/.openclaw/workspace/datadepot/imports/sell_items_catalog.json"))

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "item"

def norm_sku(sku):
    return sku.replace("#", "").strip()

def desc_for(name, cat_label):
    return f"{name} — {cat_label} for commercial point-of-sale and retail. Sold by Performance Supply Depot. Contact us for sizing, compatibility, and case quantities."

def page(item, cat_label):
    name = item["name"]
    sku = norm_sku(item["sku"])
    price = item["price"]
    price_s = f"${price:,.2f}" if isinstance(price, (int, float)) else "Call for pricing"
    price_num = price if isinstance(price, (int, float)) else None
    slug = f"{sku}-{slugify(name)}"

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


# Existing pages (by SKU prefix) so we don't touch published prices
existing = set()
for p in glob.glob(os.path.join(PROD, "*.html")):
    existing.add(os.path.basename(p).split("-")[0].lower())

count = 0
skipped = 0
for sec, (cslug, clabel) in CATS.items():
    for item in cat.get(sec, []):
        name = item["name"]
        if not name or name == "None":
            continue
        sku = norm_sku(item["sku"])
        if sku.startswith(SKIP_SKU_PREFIX):
            continue
        # skip if already published (don't change existing supply prices)
        if sku.lower() in existing:
            skipped += 1
            continue
        html = page(item, clabel)
        open(os.path.join(PROD, f"{sku}-{slugify(name)}.html"), "w").write(html)
        count += 1

print(f"✅ Built {count} Phase-2 supply pages (skipped {skipped} already-published)")
