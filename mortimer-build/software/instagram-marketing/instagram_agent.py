#!/usr/bin/env python3
"""Instagram Marketing Agent for PSD"""
import json, random
from datetime import datetime
from pathlib import Path

DIR = "/root/.openclaw/workspace/aocros/marketing/social_assets/instagram"
Path(DIR).mkdir(parents=True, exist_ok=True)

PRODUCTS = [
    ("PF-230 Thermal Paper", "BPA-free receipt paper. 50 rolls/case.", "$124.10"),
    ("SAM4S ER-940", "Dual-station cash register.", "$895.00"),
    ("Capton 1oz Pourer", "Precision portion control.", "$24.99"),
]

CAPTIONS = [
    "Streamline your POS with {name}. {desc}",
    "Behind every great restaurant: {name}. {price}. 🔧",
    "California's trusted POS supplier. {name} in stock.",
]

def generate():
    posts = []
    for _ in range(5):
        p = random.choice(PRODUCTS)
        posts.append({"product": p[0], "caption": random.choice(CAPTIONS).format(name=p[0], desc=p[1], price=p[2]), "hashtags": "#pos #restaurantsupply", "date": datetime.now().isoformat()})
    out = DIR + "/queue_" + datetime.now().strftime("%Y-%m-%d") + ".json"
    with open(out, 'w') as f: json.dump(posts, f, indent=2)
    print(f"Generated {len(posts)} IG posts → {out}")

if __name__ == "__main__": generate()
