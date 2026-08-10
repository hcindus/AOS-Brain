#!/usr/bin/env python3
"""X/Twitter + Grok Marketing Agent for PSD Marketing Division"""

import json, random, os
from datetime import datetime
from pathlib import Path

CONTENT_DIR = "/root/.openclaw/workspace/aocros/marketing/social_assets/x_twitter"
Path(CONTENT_DIR).mkdir(parents=True, exist_ok=True)

THREAD_TOPICS = [
    "Why every restaurant needs a backup thermal printer roll stash",
    "The hidden cost of cheap receipt paper (and why PF-230 is different)",
    "How to choose between a flat keyboard and raised keyboard cash register",
    "Cash drawer buying guide: CC-330 vs CC-410 vs CC-460",
    "The real reason your bar is losing money on overpouring",
]

QUICK_POSTS = [
    "New shipment of SAM4S ER-940s just landed. DM for pricing. 📦",
    "PF-230 thermal paper restocked. Free shipping on case orders. 🧾",
    "Repair bench open. SAM4S, CAS, Epson — we fix them all. 🔧",
    "California restaurants: your POS supplier since 2005. 🇺🇸",
    "Did you know? Phenol-free paper is better for your staff AND your customers.",
]

def generate_daily_posts():
    posts = []
    for _ in range(3):
        posts.append({
            "text": random.choice(QUICK_POSTS),
            "time": datetime.now().strftime("%H:%M"),
            "hashtags": "#POS #RestaurantTech #SmallBusiness"
        })
    output = CONTENT_DIR + "/posts_" + datetime.now().strftime("%Y-%m-%d") + ".json"
    with open(output, 'w') as f:
        json.dump(posts, f, indent=2)
    print(f"✅ Generated {len(posts)} X posts → {output}")

if __name__ == "__main__":
    generate_daily_posts()
