#!/usr/bin/env python3
"""
ACN-Tech Order Automation
Monitors prices and generates orders when conditions are met

Usage:
    python order_automation.py --check
    python order_automation.py --create-order --sku ERC-32 --qty 10
    python order_automation.py --monitor
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configuration paths
CONFIG_FILE = Path(__file__).parent.parent / "acn_tech_config.json"
PRICE_FILE = Path(__file__).parent.parent / "products" / "acn_tech_prices.json"
ORDERS_DIR = Path(__file__).parent.parent / "orders"
PSDEPOT_PRICE_FILE = Path("/root/.openclaw/workspace/aocros/performance_supply_depot/prices/psdepot_prices.json")


def load_config():
    """Load ACN-Tech configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def load_acn_prices():
    """Load scraped ACN-Tech prices"""
    if PRICE_FILE.exists():
        with open(PRICE_FILE, 'r') as f:
            return json.load(f)
    return {'products': []}


def load_psdepot_prices():
    """Load PSDEPOT pricing for comparison"""
    if PSDEPOT_PRICE_FILE.exists():
        with open(PSDEPOT_PRICE_FILE, 'r') as f:
            return json.load(f)
    return {'prices': []}


def calculate_our_price(acn_price: float, markup_percent: float = 25) -> float:
    """Calculate our selling price with markup"""
    return round(acn_price * (1 + markup_percent / 100), 2)


def check_profitable(acn_price: float, our_price: float, min_margin: float = 15) -> bool:
    """Check if the deal is profitable"""
    margin = ((our_price - acn_price) / our_price) * 100
    return margin >= min_margin


def analyze_opportunities():
    """Analyze current prices for opportunities"""
    print("📊 ACN-Tech Opportunity Analysis")
    print("=" * 60)
    
    config = load_config()
    acn_data = load_acn_prices()
    psdepot_data = load_psdepot_prices()
    
    acn_products = acn_data.get('products', [])
    psdepot_prices = {p['sku']: p for p in psdepot_data.get('prices', [])}
    
    if not acn_products:
        print("⚠️  No ACN-Tech prices found. Run scraper first.")
        return []
    
    opportunities = []
    
    print(f"\n🔍 Analyzing {len(acn_products)} products...")
    print("-" * 60)
    
    for product in acn_products:
        acn_price = product.get('price', 0)
        if not acn_price:
            continue
        
        name = product.get('name', 'Unknown')
        search_term = product.get('search_term', '')
        
        # Calculate our price
        our_price = calculate_our_price(
            acn_price, 
            config.get('pricing', {}).get('markup_percent', 25)
        )
        
        # Check profitability
        min_margin = config.get('pricing', {}).get('min_margin_percent', 15)
        is_profitable = check_profitable(acn_price, our_price, min_margin)
        
        # Check against PSDEPOT pricing if available
        psdepot_price = None
        psdepot_match = None
        for sku, pdata in psdepot_prices.items():
            if sku.lower() in search_term.lower() or sku.lower() in name.lower():
                psdepot_price = pdata.get('web_price')
                psdepot_match = sku
                break
        
        opportunity = {
            'name': name,
            'acn_price': acn_price,
            'our_price': our_price,
            'margin_percent': round(((our_price - acn_price) / our_price) * 100, 1),
            'profitable': is_profitable,
            'psdepot_price': psdepot_price,
            'psdepot_match': psdepot_match,
            'url': product.get('url', '')
        }
        
        opportunities.append(opportunity)
        
        # Display
        status = "✅" if is_profitable else "❌"
        psdepot_info = f" | PSDEPOT: ${psdepot_price}" if psdepot_price else ""
        print(f"{status} {name[:40]:<40}")
        print(f"   ACN: ${acn_price:.2f} | Us: ${our_price:.2f} | Margin: {opportunity['margin_percent']:.1f}%{psdepot_info}")
    
    # Summary
    profitable = [o for o in opportunities if o['profitable']]
    print(f"\n📈 Summary: {len(profitable)}/{len(opportunities)} products are profitable")
    
    return opportunities


def create_order(sku: str, quantity: int, notes: str = ""):
    """Create a draft order"""
    print(f"📝 Creating Order: {sku} x{quantity}")
    print("=" * 60)
    
    ORDERS_DIR.mkdir(parents=True, exist_ok=True)
    
    acn_data = load_acn_prices()
    
    # Find product
    product = None
    for p in acn_data.get('products', []):
        if sku.lower() in p.get('name', '').lower() or sku.lower() in p.get('search_term', '').lower():
            product = p
            break
    
    if not product:
        print(f"❌ Product not found: {sku}")
        return None
    
    acn_price = product.get('price', 0)
    total_cost = acn_price * quantity
    
    order = {
        'order_id': f"ACN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        'created_at': datetime.now().isoformat(),
        'status': 'draft',
        'product': {
            'name': product.get('name'),
            'sku': sku,
            'acn_price': acn_price,
            'url': product.get('url')
        },
        'quantity': quantity,
        'total_cost': total_cost,
        'notes': notes,
        'auto_submit': False,
        'notification_sent': False
    }
    
    # Save order
    order_file = ORDERS_DIR / f"{order['order_id']}.json"
    with open(order_file, 'w') as f:
        json.dump(order, f, indent=2)
    
    print(f"✅ Order created: {order['order_id']}")
    print(f"   Product: {product.get('name')}")
    print(f"   Quantity: {quantity}")
    print(f"   Unit Price: ${acn_price:.2f}")
    print(f"   Total Cost: ${total_cost:.2f}")
    print(f"   File: {order_file}")
    
    return order


def list_orders():
    """List all pending orders"""
    print("📋 Order Queue")
    print("=" * 60)
    
    if not ORDERS_DIR.exists():
        print("No orders directory found.")
        return []
    
    orders = []
    for order_file in sorted(ORDERS_DIR.glob("ACN-*.json")):
        with open(order_file, 'r') as f:
            order = json.load(f)
            orders.append(order)
            status_icon = "🟡" if order['status'] == 'draft' else "✅"
            print(f"{status_icon} {order['order_id']}: {order['product']['name'][:30]} x{order['quantity']} = ${order['total_cost']:.2f}")
    
    if not orders:
        print("No orders found.")
    
    return orders


def monitor_loop():
    """Continuous monitoring loop"""
    import time
    
    config = load_config()
    interval = config.get('automation', {}).get('check_interval_minutes', 60)
    
    print(f"🔁 Starting Monitor Loop (interval: {interval} minutes)")
    print("=" * 60)
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            print(f"\n⏰ Check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check for opportunities
            opportunities = analyze_opportunities()
            profitable = [o for o in opportunities if o['profitable']]
            
            if profitable:
                print(f"\n🎯 {len(profitable)} profitable opportunities found!")
                # Here we could auto-create orders or just notify
                # For now, just list them
            else:
                print("\n😴 No profitable opportunities right now.")
            
            print(f"\n💤 Sleeping for {interval} minutes...")
            time.sleep(interval * 60)
            
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped.")


def main():
    parser = argparse.ArgumentParser(description='ACN-Tech Order Automation')
    parser.add_argument('--check', action='store_true', help='Analyze current opportunities')
    parser.add_argument('--create-order', action='store_true', help='Create a new order')
    parser.add_argument('--sku', help='Product SKU for order')
    parser.add_argument('--qty', type=int, default=1, help='Quantity for order')
    parser.add_argument('--notes', default='', help='Order notes')
    parser.add_argument('--list', action='store_true', help='List pending orders')
    parser.add_argument('--monitor', action='store_true', help='Start monitoring loop')
    
    args = parser.parse_args()
    
    if args.create_order:
        if not args.sku:
            print("❌ --sku required for order creation")
            sys.exit(1)
        create_order(args.sku, args.qty, args.notes)
    elif args.list:
        list_orders()
    elif args.monitor:
        monitor_loop()
    else:
        analyze_opportunities()


if __name__ == '__main__':
    main()
