#!/usr/bin/env python3
"""Shopify Integration Agent for PSD"""
import csv
from datetime import datetime
from pathlib import Path

DIR = "/root/.openclaw/workspace/aocros/marketing/social_assets/shopify"
Path(DIR).mkdir(parents=True, exist_ok=True)

products = [
    ("PF-230", "PF-230 Phenol Free Thermal Paper", "BPA-free thermal receipt paper. 3 1/8" x 230 ft. 50 rolls/case.", "Thermal Paper", 124.10, 89.00),
    ("ER-940", "SAM4S ER-940 Cash Register", "Dual-station flat keyboard. Electronic journal.", "Cash Registers", 895.00, 650.00),
    ("ER-265", "SAM4S ER-265 Cash Register", "Flat keyboard. 99 departments.", "Cash Registers", 495.00, 380.00),
    ("SAP-630", "SAM4S SAP-630 POS Terminal", "Android POS terminal. 10.1" touchscreen.", "POS Systems", 1395.00, 1100.00),
    ("CC-410", "M-S Cash Drawer CC-410", "Heavy-duty 16" cash drawer.", "Cash Drawers", 189.00, 145.00),
    ("CAP-1OZ", "Capton 1oz Pourer", "Precision portion control.", "Bar Supplies", 24.99, 18.00),
]

out = DIR + "/shopify_import_" + datetime.now().strftime("%Y-%m-%d") + ".csv"
with open(out, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(["Handle","Title","Body (HTML)","Type","Variant SKU","Variant Price","Variant Compare At Price"])
    for sku, title, desc, ptype, price, compare in products:
        w.writerow([sku.lower(), title, f"<p>{desc}</p>", ptype, sku, price, compare])
print(f"Shopify import: {len(products)} products → {out}")
