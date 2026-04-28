#!/usr/bin/env python3
"""
X (Twitter) Content Generator for Performance Supply Depot
Generates tweet content ready to copy/paste into X console
"""

import random
import sys
from datetime import datetime

# Content Templates - All linking to psdepot.com
TEMPLATES = {
    "product_highlight": [
        "Running low on receipt paper? 📄 We stock thermal rolls for every POS system. Same-day delivery in Vegas. Check prices: https://psdepot.com #POSsupplies #RestaurantLife",
        "Samsung POS systems starting at $495. Professional setup included. Upgrade your checkout: https://psdepot.com #POS #SmallBusiness",
        "Kitchen printer acting up? 🖨️ Our techs repair all major brands on-site. Book now: https://psdepot.com #PrinterRepair #LasVegas",
        "Save 20% on your first order. Thermal paper, ink ribbons, POS accessories — we beat most prices: https://psdepot.com #Deals",
        "Need scales for your restaurant? We carry CAS, AND, and Samsung models starting at $795: https://psdepot.com #Scales #RestaurantEquipment",
    ],
    "tips": [
        "💡 Tip: Store thermal paper away from heat/sunlight to prevent premature darkening. Quality supplies = fewer reprints. https://psdepot.com #RestaurantTips",
        "Is your receipt printer streaking? Clean the thermal head monthly with isopropyl alcohol. More maintenance tips: https://psdepot.com #TechTips",
        "🍽️ Busy weekend ahead? Stock up on receipt paper Friday — avoid the Sunday night panic. Order now: https://psdepot.com #RestaurantLife",
        "Pro tip: Bond paper for impact printers should be stored in a cool, dry place. We deliver fresh stock: https://psdepot.com #SupplyTips",
    ],
    "social_proof": [
        "Local diner switched to us last month — now saving $200+/month on supplies. See how much you could save: https://psdepot.com 💰",
        "\"We went from 3 stockouts a month to zero.\" — Las Vegas Grill owner. Same-day delivery works. https://psdepot.com 🚚",
        "Our tech fixed 3 printers in one visit. That's the kind of service you get with a local supplier. https://psdepot.com 🔧 #LasVegas",
    ],
    "promotional": [
        "🚨 New customers: 20% off first order + free printer diagnostic. Mention code VEGAS20. https://psdepot.com #LimitedTime",
        "Running a restaurant in Vegas? We specialize in POS supplies with same-day delivery. Let's talk: https://psdepot.com 📞 888-881-6834",
        "End-of-month stock check? 📋 We can get you same-day delivery on most items. Order by 2pm: https://psdepot.com #SameDayDelivery",
    ],
    "engagement": [
        "What POS system are you running? 💻 Samsung, Clover, Square — we service them all. Let us know in the replies! https://psdepot.com",
        "Poll: What's your biggest supply headache? 🗳️ A) Running out of receipt paper B) Printer breakdowns C) Delivery delays D) High costs https://psdepot.com",
        "Question for restaurant owners: How often does your receipt printer need service? 🤔 We're curious! https://psdepot.com #RestaurantTalk",
    ]
}

def get_random_tweet():
    """Generate a random tweet"""
    category = random.choice(list(TEMPLATES.keys()))
    return random.choice(TEMPLATES[category])

def get_tweet_by_category(category):
    """Get a tweet from specific category"""
    if category in TEMPLATES:
        return random.choice(TEMPLATES[category])
    return get_random_tweet()

def generate_daily_content():
    """Generate 3 tweets for the day"""
    tweets = []
    used = set()
    
    for _ in range(3):
        tweet = get_random_tweet()
        while tweet in used:
            tweet = get_random_tweet()
        used.add(tweet)
        tweets.append(tweet)
    
    return tweets

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("X Marketing Content Generator - Performance Supply Depot")
        print("=" * 60)
        print("\nCategories:")
        for cat in TEMPLATES.keys():
            print(f"  - {cat}")
        print("\nUsage:")
        print("  x_content.py daily       # Generate 3 tweets for today")
        print("  x_content.py random      # Get one random tweet")
        print("  x_content.py <category>  # Get tweet from category")
        return
    
    command = sys.argv[1]
    
    if command == "daily":
        tweets = generate_daily_content()
        print(f"\n📅 Daily Content for {datetime.now().strftime('%Y-%m-%d')}\n")
        print("=" * 60)
        for i, tweet in enumerate(tweets, 1):
            print(f"\n🐦 Tweet {i}:")
            print(f"{tweet}")
            print(f"\nLength: {len(tweet)} characters")
        print("\n" + "=" * 60)
        print("\n✅ Ready to copy/paste into X Agent console")
        
    elif command == "random":
        tweet = get_random_tweet()
        print(f"\n🐦 Random Tweet:")
        print(f"{tweet}")
        print(f"\nLength: {len(tweet)} characters")
        print("\n✅ Copy and paste into X Agent console")
        
    elif command in TEMPLATES:
        tweet = get_tweet_by_category(command)
        print(f"\n🐦 {command.replace('_', ' ').title()} Tweet:")
        print(f"{tweet}")
        print(f"\nLength: {len(tweet)} characters")
        
    else:
        print(f"❌ Unknown category: {command}")
        print(f"Available: {', '.join(TEMPLATES.keys())}")

if __name__ == "__main__":
    main()
