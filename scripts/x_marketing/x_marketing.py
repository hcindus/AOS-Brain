#!/usr/bin/env python3
"""
X (Twitter) Marketing Automation for Performance Supply Depot
Posts engaging content with psdepot.com links
"""

import os
import json
import random
import requests
import urllib.parse
from datetime import datetime
from pathlib import Path

# X API Configuration (URL-decoded Bearer Token)
BEARER_TOKEN = urllib.parse.unquote("AAAAAAAAAAAAAAAAAAAAAEws9QEAAAAAzy7mxVcLzYUsFdJMWc36TofwK%2FQ%3DC1j3hjxFfVyIIORCiKlFZTmXBP9Uz8ATI0qctVsBexVkvg68Tu")
API_BASE = "https://api.x.com/2"

# Content Templates - Focused on psdepot.com
TEMPLATES = {
    "product_highlight": [
        "Running low on receipt paper? 📄 We stock thermal rolls for every POS system. Same-day delivery in Vegas. Check prices: https://psdepot.com #POSsupplies #RestaurantLife",
        "Samsung POS systems starting at $495. Professional setup included. Upgrade your checkout: https://psdepot.com #POS #SmallBusiness",
        "Kitchen printer acting up? 🖨️ Our techs repair all major brands on-site. Book now: https://psdepot.com #PrinterRepair #LasVegas",
        "Save 20% on your first order. Thermal paper, ink ribbons, POS accessories — we beat most prices: https://psdepot.com #Deals",
    ],
    "tips": [
        "💡 Tip: Store thermal paper away from heat/sunlight to prevent premature darkening. Quality supplies = fewer reprints. https://psdepot.com #RestaurantTips",
        "Is your receipt printer streaking? Clean the thermal head monthly with isopropyl alcohol. More maintenance tips: https://psdepot.com #TechTips",
        "🍽️ Busy weekend ahead? Stock up on receipt paper Friday — avoid the Sunday night panic. Order now: https://psdepot.com #RestaurantLife",
    ],
    "social_proof": [
        "Local diner switched to us last month — now saving $200+/month on supplies. See how much you could save: https://psdepot.com 💰",
        "\"We went from 3 stockouts a month to zero.\" — Las Vegas Grill owner. Same-day delivery works. https://psdepot.com 🚚",
        "Our tech fixed 3 printers in one visit. That's the kind of service you get with a local supplier. https://psdepot.com 🔧 #LasVegas",
    ],
    "promotional": [
        "🚨 New customers: 20% off first order + free printer diagnostic. Mention code VEGAS20. https://psdepot.com #LimitedTime",
        "Running a restaurant in Vegas? We specialize in POS supplies with same-day delivery. Let's talk: https://psdepot.com 📞 888-881-6834",
    ]
}

def get_random_content():
    """Select random content from templates"""
    category = random.choice(list(TEMPLATES.keys()))
    return random.choice(TEMPLATES[category])

def post_tweet(text):
    """Post a tweet via X API v2"""
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {"text": text}
    
    try:
        response = requests.post(
            f"{API_BASE}/tweets",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Tweet posted: {data['data']['id']}")
            return True
        elif response.status_code == 401:
            print(f"❌ Auth failed: {response.text}")
            return False
        else:
            print(f"⚠️ API error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error posting tweet: {e}")
        return False

def test_connection():
    """Test X API connection"""
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    
    try:
        response = requests.get(
            f"{API_BASE}/users/me",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connected to X API as: @{data['data']['username']}")
            return True
        else:
            print(f"❌ Connection failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: x_marketing.py <test|post|status>")
        return
    
    command = sys.argv[1]
    
    if command == "test":
        test_connection()
    elif command == "post":
        content = get_random_content()
        print(f"Posting: {content[:60]}...")
        post_tweet(content)
    elif command == "status":
        test_connection()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
