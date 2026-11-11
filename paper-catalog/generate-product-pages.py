#!/usr/bin/env python3
"""
Generate product pages + category pages + search-index entries for the
Ribbon & Toner division (ACM catalog). Reads datadepot/data/psdepot_catalog.json
and writes HTML into /var/www/psdepot.com/products/ + /categories/ + search-index.
"""
import json, os, re, html

CATALOG = "/root/.openclaw/workspace/datadepot/data/psdepot_catalog.json"
WEBROOT = "/var/www/psdepot.com"
PRODUCTS_DIR = os.path.join(WEBROOT, "products")
CATEGORIES_DIR = os.path.join(WEBROOT, "categories")
SEARCH_INDEX = os.path.join(WEBROOT, "search-index.json")

BASE = "https://psdepot.com"

def slugify(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def esc(t):
    return html.escape(str(t), quote=True)

def product_page(p):
    sku = p['sku']
    name = p['name']
    spec = p.get('spec','')
    sell = p['sell']
    category = p.get('category','')
    division = p.get('division','')
    slug = slugify(sku)
    url = f"{BASE}/products/{slug}.html"
    title = f"{name} {spec} | Performance Supply Depot LLC".strip()
    desc = f"{name} — {spec}. {category} from Performance Supply Depot LLC. Ships fast across the US."
    keywords = f"{name}, {spec}, {category}, {division}, ACM, Performance Supply Depot"
    image = f"{BASE}/assets/images/products/{slug}.jpg"

    ld = {
        "@context": "https://schema.org", "@type": "Product",
        "name": f"{name} {spec}".strip(), "sku": sku,
        "brand": {"@type": "Brand", "name": "Performance Supply Depot"},
        "offers": {"@type": "Offer", "price": sell, "priceCurrency": "USD",
                   "availability": "https://schema.org/InStock"},
        "description": desc,
    }
    ld_json = json.dumps(ld)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(keywords)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{image}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script type="application/ld+json">{ld_json}</script>
<style>
:root{{--primary:#0A1A2F;--accent:#d69e2e;--bg:#F8F9FA;--card:#fff;--text:#111;--muted:#718096;--border:#e2e8f0}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}}
.header{{background:var(--primary);color:#fff;padding:14px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
.logo{{font-size:22px;font-weight:800;color:#fff;text-decoration:none}}.logo span{{color:#63b3ed}}
.header a{{color:#bee3f8;text-decoration:none;font-size:14px}}
.breadcrumb{{max-width:1100px;margin:1rem auto;padding:0 24px;font-size:14px;color:var(--muted)}}.breadcrumb a{{color:var(--primary)}}
.container{{max-width:1100px;margin:0 auto;padding:24px;display:grid;grid-template-columns:1fr 1fr;gap:32px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px}}
.sku{{display:inline-block;background:var(--primary);color:#fff;padding:4px 10px;border-radius:4px;font-size:12px;font-weight:600;text-transform:uppercase}}
h1{{font-size:26px;color:var(--primary);margin:12px 0 4px}}
.spec{{color:var(--muted);font-size:15px}}
.price{{font-size:32px;font-weight:700;color:var(--primary);margin:16px 0 4px}}
.price-unit{{font-size:14px;color:var(--muted)}}
.btn{{display:inline-block;background:#c53030;color:#fff;border:none;padding:12px 24px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;text-decoration:none;margin-top:12px}}
.btn:hover{{background:#9b2c2c}}
table{{width:100%;border-collapse:collapse;margin-top:12px}}
td{{padding:8px 0;border-bottom:1px solid var(--border);font-size:14px}}
td:first-child{{color:var(--muted)}}
h3{{font-size:17px;color:var(--primary);margin-bottom:8px}}
footer{{background:var(--primary);color:#fff;padding:24px;text-align:center;font-size:13px;margin-top:40px}}
@media(max-width:768px){{.container{{grid-template-columns:1fr}}}}
</style>
<script src="/js/search.js" defer></script><script src="/js/raven-widget.js" defer></script>
</head>
<body>
<header class="header">
<a href="/" class="logo">Performance<span>Supply</span>Depot</a>
<div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
<a href="tel:888-881-6834">📞 (888) 881-6834</a>
<a href="mailto:info@psdepot.com">✉️ info@psdepot.com</a>
<a href="/checkout.html" style="background:#c53030;color:#fff;padding:8px 16px;border-radius:20px;font-weight:600;text-decoration:none">🛒 Cart</a>
</div>
</header>
<div class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/products/index.html">Products</a> &rsaquo; <a href="/categories/{slugify(category or division)}/index.html">{esc(category or division)}</a> &rsaquo; {esc(name)}</div>
<div class="container">
<div class="card" style="text-align:center;display:flex;align-items:center;justify-content:center;min-height:280px">
<div style="color:var(--muted)">[Image placeholder]<br><span style="font-size:13px">{esc(name)}</span></div>
</div>
<div>
<span class="sku">SKU {esc(sku)}</span>
<h1>{esc(name)}</h1>
<p class="spec">{esc(spec)}</p>
<div class="price">${sell:.2f}<span class="price-unit"> / each</span></div>
<p style="color:var(--muted);font-size:13px">Plus shipping &amp; tax. Quantity pricing available.</p>
<a class="btn" href="/checkout.html?sku={esc(sku)}">Add to Cart</a>
<div class="card" style="margin-top:20px">
<h3>Specifications</h3>
<table>
<tr><td>SKU</td><td>{esc(sku)}</td></tr>
<tr><td>Category</td><td>{esc(category)}</td></tr>
<tr><td>Division</td><td>{esc(division)}</td></tr>
<tr><td>Compatibility</td><td>{esc(spec)}</td></tr>
</table>
</div>
</div>
</div>
<footer>Performance Supply Depot LLC &bull; 1880 Oak Point Court, Fairfield, CA 94534 &bull; (888) 881-6834 &bull; info@psdepot.com</footer>
</body>
</html>"""

def category_page(category, products):
    slug = slugify(category)
    url = f"{BASE}/categories/{slug}/index.html"
    title = f"{category} | Performance Supply Depot LLC"
    desc = f"Shop {category} from Performance Supply Depot LLC. Fast shipping across the US."
    items = ""
    for p in products:
        pslug = slugify(p['sku'])
        items += (f'<a href="/products/{pslug}.html" style="display:flex;justify-content:space-between;'
                  f'padding:12px 16px;border:1px solid var(--border);border-radius:8px;margin-bottom:10px;'
                  f'text-decoration:none;color:var(--text);background:var(--card)">'
                  f'<span><strong>{esc(p["name"])}</strong><br><span style="color:var(--muted);font-size:13px">{esc(p.get("spec",""))}</span></span>'
                  f'<span style="font-weight:700;color:var(--primary)">${p["sell"]:.2f}</span></a>')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>
:root{{--primary:#0A1A2F;--accent:#d69e2e;--bg:#F8F9FA;--card:#fff;--text:#111;--muted:#718096;--border:#e2e8f0}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}}
.header{{background:var(--primary);color:#fff;padding:14px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
.logo{{font-size:22px;font-weight:800;color:#fff;text-decoration:none}}.logo span{{color:#63b3ed}}
.header a{{color:#bee3f8;text-decoration:none;font-size:14px}}
.wrap{{max-width:1100px;margin:0 auto;padding:24px}}
h1{{font-size:26px;color:var(--primary);margin:16px 0 4px}}
.count{{color:var(--muted);font-size:14px;margin-bottom:20px}}
footer{{background:var(--primary);color:#fff;padding:24px;text-align:center;font-size:13px;margin-top:40px}}
</style>
<script src="/js/search.js" defer></script><script src="/js/raven-widget.js" defer></script>
</head>
<body>
<header class="header"><a href="/" class="logo">Performance<span>Supply</span>Depot</a>
<div style="display:flex;gap:16px"><a href="tel:888-881-6834">📞 (888) 881-6834</a><a href="mailto:info@psdepot.com">✉️ info@psdepot.com</a></div></header>
<div class="wrap">
<h1>{esc(category)}</h1>
<p class="count">{len(products)} products</p>
{items}
</div>
<footer>Performance Supply Depot LLC &bull; 1880 Oak Point Court, Fairfield, CA 94534 &bull; (888) 881-6834</footer>
</body>
</html>"""

def main():
    cat = json.load(open(CATALOG))
    products = [p for p in cat['products'] if p.get('division') == 'Ribbon & Toner']
    os.makedirs(PRODUCTS_DIR, exist_ok=True)
    os.makedirs(CATEGORIES_DIR, exist_ok=True)

    # 1. product pages + search entries
    new_entries = []
    for p in products:
        slug = slugify(p['sku'])
        path = os.path.join(PRODUCTS_DIR, f"{slug}.html")
        open(path, "w").write(product_page(p))
        new_entries.append({
            "url": f"{BASE}/products/{slug}.html",
            "title": f"{p['name']} {p.get('spec','')}".strip(),
            "description": f"{p['name']} — {p.get('spec','')}. {p.get('category','')} from Performance Supply Depot.",
        })

    # 2. category pages
    from collections import defaultdict
    by_cat = defaultdict(list)
    for p in products:
        by_cat[p.get('category') or p.get('division')].append(p)
    for category, plist in by_cat.items():
        slug = slugify(category)
        cdir = os.path.join(CATEGORIES_DIR, slug)
        os.makedirs(cdir, exist_ok=True)
        open(os.path.join(cdir, "index.html"), "w").write(category_page(category, plist))
        new_entries.append({
            "url": f"{BASE}/categories/{slug}/index.html",
            "title": f"{category} | Performance Supply Depot LLC",
            "description": f"Shop {category} from Performance Supply Depot LLC.",
        })

    # 3. update search index (dedupe by url)
    idx = json.load(open(SEARCH_INDEX))
    existing_urls = {e['url'] for e in idx}
    added = 0
    for e in new_entries:
        if e['url'] not in existing_urls:
            idx.append(e); existing_urls.add(e['url']); added += 1
    json.dump(idx, open(SEARCH_INDEX, "w"), indent=2)

    print(f"PRODUCT_PAGES={len(products)} CATEGORIES={len(by_cat)} SEARCH_ADDED={added} SEARCH_TOTAL={len(idx)}")

if __name__ == "__main__":
    main()
