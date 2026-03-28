#!/usr/bin/env python3
"""
psdepot.com Price Updater
Updates POS supplies prices from client.xls spreadsheet

Usage:
    python psdepot_price_updater.py --source client.xls --output prices.json
    python psdepot_price_updater.py --update-website

Required columns in client.xls:
    - SKU (product code)
    - Description
    - Cost (our cost)
    - Retail (MSRP/suggested retail)
    - WebPrice (price to display on psdepot.com)

Ribbon SKUs to prioritize:
    - 62245 (Epson ERC-32)
    - 67240 (Epson ERC-38)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Try to import pandas/openpyxl for Excel reading
try:
    import pandas as pd
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False
    print("⚠️  pandas not installed. Install with: pip install pandas openpyxl")

# Configuration
DEFAULT_SOURCE = "client.xls"
DEFAULT_OUTPUT = "/root/.openclaw/workspace/aocros/performance_supply_depot/prices/psdepot_prices.json"
PRICE_HISTORY = "/root/.openclaw/workspace/aocros/performance_supply_depot/prices/price_history.json"
FIRST_5_PAPERS = [
    {"sku": "PAPER-1", "name": "Thermal Paper Roll 3-1/8" x 230'", "priority": 1},
    {"sku": "PAPER-2", "name": "Thermal Paper Roll 2-1/4" x 85'", "priority": 2},
    {"sku": "PAPER-3", "name": "Bond Paper 8.5" x 11"", "priority": 3},
    {"sku": "PAPER-4", "name": "Thermal Receipt Paper 3" x 150'", "priority": 4},
    {"sku": "PAPER-5", "name": "Carbonless Paper 2-Part", "priority": 5},
]
RIBBONS = [
    {"sku": "62245", "name": "Epson ERC-32 Ribbon", "type": "ribbon", "priority": 1},
    {"sku": "67240", "name": "Epson ERC-38 Ribbon", "type": "ribbon", "priority": 2},
]

def ensure_dirs():
    """Ensure required directories exist"""
    Path(DEFAULT_OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    Path(PRICE_HISTORY).parent.mkdir(parents=True, exist_ok=True)

def read_excel_prices(source_file):
    """Read prices from client.xls"""
    if not EXCEL_SUPPORT:
        print("❌ Cannot read Excel. pandas not available.")
        return None
    
    if not os.path.exists(source_file):
        print(f"❌ Source file not found: {source_file}")
        print("💡 Place client.xls in the workspace root or provide full path")
        return None
    
    try:
        print(f"📂 Reading: {source_file}")
        
        # Try different engines
        try:
            df = pd.read_excel(source_file, engine='openpyxl')
        except:
            df = pd.read_excel(source_file, engine='xlrd')
        
        prices = []
        for _, row in df.iterrows():
            sku = str(row.get('SKU', '')).strip()
            if not sku or sku.lower() in ['nan', 'none']:
                continue
            
            price_entry = {
                'sku': sku,
                'description': str(row.get('Description', '')).strip(),
                'cost': float(row.get('Cost', 0) or 0),
                'retail': float(row.get('Retail', 0) or 0),
                'web_price': float(row.get('WebPrice', 0) or 0),
                'category': str(row.get('Category', 'General')).strip(),
                'last_updated': datetime.now().isoformat(),
                'source_file': source_file
            }
            prices.append(price_entry)
        
        print(f"✅ Loaded {len(prices)} products from Excel")
        return prices
        
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return None

def get_priority_products(prices):
    """Extract first 5 paper products and ribbons 62245, 67240"""
    priority_skus = {p['sku'] for p in FIRST_5_PAPERS + RIBBONS}
    
    priority_products = []
    for price in prices:
        if price['sku'] in priority_skus:
            priority_products.append(price)
    
    return priority_products

def calculate_markups(prices):
    """Calculate markup percentages"""
    for price in prices:
        cost = price.get('cost', 0)
        web_price = price.get('web_price', 0)
        
        if cost > 0 and web_price > 0:
            price['markup_percent'] = round(((web_price - cost) / cost) * 100, 2)
            price['margin_percent'] = round(((web_price - cost) / web_price) * 100, 2)
        else:
            price['markup_percent'] = 0
            price['margin_percent'] = 0
    
    return prices

def save_prices(prices, output_file):
    """Save prices to JSON"""
    price_data = {
        'generated_at': datetime.now().isoformat(),
        'total_products': len(prices),
        'source': 'client.xls',
        'prices': prices
    }
    
    with open(output_file, 'w') as f:
        json.dump(price_data, f, indent=2)
    
    print(f"💾 Saved prices to: {output_file}")
    return output_file

def save_price_history(prices):
    """Append to price history for tracking changes"""
    history_entry = {
        'date': datetime.now().isoformat(),
        'product_count': len(prices),
        'products': [{'sku': p['sku'], 'price': p.get('web_price')} for p in prices]
    }
    
    history = []
    if os.path.exists(PRICE_HISTORY):
        with open(PRICE_HISTORY, 'r') as f:
            history = json.load(f)
    
    history.append(history_entry)
    
    # Keep last 90 days
    history = history[-90:]
    
    with open(PRICE_HISTORY, 'w') as f:
        json.dump(history, f, indent=2)

def generate_web_output(prices):
    """Generate output for psdepot.com website"""
    web_prices = {}
    for price in prices:
        web_prices[price['sku']] = {
            'price': price.get('web_price', 0),
            'description': price.get('description', ''),
            'retail': price.get('retail', 0)
        }
    
    output_file = "/root/.openclaw/workspace/aocros/performance_supply_depot/prices/psdepot_web_prices.json"
    with open(output_file, 'w') as f:
        json.dump(web_prices, f, indent=2)
    
    print(f"🌐 Web prices saved: {output_file}")
    return output_file

def print_summary(prices):
    """Print summary of prices"""
    print("\n" + "="*60)
    print("  PSDEPOT PRICE UPDATE SUMMARY")
    print("="*60)
    print(f"Total products: {len(prices)}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("-"*60)
    
    # Priority products
    priority = get_priority_products(prices)
    print(f"\n🎯 Priority Products ({len(priority)}):")
    for p in priority[:7]:
        print(f"   {p['sku']}: ${p.get('web_price', 0):.2f} - {p['description'][:40]}...")
    
    # Price ranges
    if prices:
        web_prices = [p.get('web_price', 0) for p in prices if p.get('web_price', 0) > 0]
        if web_prices:
            print(f"\n💰 Price Range:")
            print(f"   Lowest: ${min(web_prices):.2f}")
            print(f"   Highest: ${max(web_prices):.2f}")
            print(f"   Average: ${sum(web_prices)/len(web_prices):.2f}")
    
    print("="*60)

def create_template_excel(output_path="client_template.xls"):
    """Create template Excel file showing required format"""
    if not EXCEL_SUPPORT:
        print("⚠️  Cannot create template without pandas")
        return None
    
    template_data = {
        'SKU': ['PAPER-1', 'PAPER-2', 'PAPER-3', 'PAPER-4', 'PAPER-5', '62245', '67240'],
        'Description': [
            'Thermal Paper Roll 3-1/8" x 230\'',
            'Thermal Paper Roll 2-1/4" x 85\'',
            'Bond Paper 8.5" x 11"',
            'Thermal Receipt Paper 3" x 150\'',
            'Carbonless Paper 2-Part',
            'Epson ERC-32 Ribbon',
            'Epson ERC-38 Ribbon'
        ],
        'Cost': [2.50, 1.20, 5.00, 3.00, 8.00, 4.50, 5.00],
        'Retail': [4.99, 2.49, 9.99, 5.99, 15.99, 8.99, 9.99],
        'WebPrice': [3.99, 1.99, 7.99, 4.99, 12.99, 6.99, 7.99],
        'Category': ['Paper', 'Paper', 'Paper', 'Paper', 'Paper', 'Ribbon', 'Ribbon']
    }
    
    df = pd.DataFrame(template_data)
    
    try:
        df.to_excel(output_path, index=False, engine='openpyxl')
    except:
        df.to_excel(output_path, index=False, engine='xlwt')
    
    print(f"📄 Template created: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Update psdepot.com prices from client.xls')
    parser.add_argument('--source', '-s', default=DEFAULT_SOURCE, help='Source Excel file')
    parser.add_argument('--output', '-o', default=DEFAULT_OUTPUT, help='Output JSON file')
    parser.add_argument('--update-website', action='store_true', help='Update website prices')
    parser.add_argument('--create-template', action='store_true', help='Create template Excel file')
    parser.add_argument('--priority-only', action='store_true', help='Only update first 5 papers + ribbons')
    
    args = parser.parse_args()
    
    ensure_dirs()
    
    if args.create_template:
        create_template_excel()
        return
    
    # Read prices from Excel
    prices = read_excel_prices(args.source)
    
    if prices is None:
        print("\n❌ Cannot proceed without source file.")
        print("💡 Options:")
        print("   1. Provide client.xls file")
        print("   2. Run with --create-template to see required format")
        print("   3. Check if file exists in: /root/.openclaw/workspace/")
        sys.exit(1)
    
    # Calculate markups
    prices = calculate_markups(prices)
    
    # Filter to priority products if requested
    if args.priority_only:
        prices = get_priority_products(prices)
        print(f"🎯 Filtering to {len(prices)} priority products")
    
    # Save outputs
    save_prices(prices, args.output)
    save_price_history(prices)
    
    if args.update_website:
        generate_web_output(prices)
    
    # Print summary
    print_summary(prices)

if __name__ == '__main__':
    main()