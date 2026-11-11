#!/usr/bin/env python3
"""
Aggregate the individual per-vendor catalogs into the unified order-pipeline
catalog (datadepot/data/psdepot_catalog.json). Run after updating any catalog.
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # workspace root (parent of scripts/)
OUT = os.path.join(BASE, "datadepot/data/psdepot_catalog.json")

def load_products(path):
    data = json.load(open(path))
    return data.get("products", data) if isinstance(data, dict) else data

# Note: ms-cashdrawer-catalog uses a different schema (cash drawers) and is
# kept separate. Only paper + ACM share the order-pipeline schema (sku/cost/sell/vendor).
catalogs = [
    os.path.join(BASE, "paper-catalog/products-catalog.json"),
    os.path.join(BASE, "acm-catalog/products-catalog.json"),
]

products = []
for c in catalogs:
    if os.path.exists(c):
        products.extend(load_products(c))

# preserve tax_rate if present in existing unified
tax_rate = 0.09
if os.path.exists(OUT):
    try:
        tax_rate = json.load(open(OUT)).get("tax_rate", 0.09)
    except Exception:
        pass

out = {"tax_rate": tax_rate, "products": products}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(out, open(OUT, "w"), indent=2)
print(f"AGGREGATED {len(products)} products -> {OUT}")
