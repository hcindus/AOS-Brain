#!/usr/bin/env python3
"""
ACN-Tech.com Product Scraper
Scrapes ribbons and toner prices from acn-tech.com

Usage:
    python scraper.py --check-prices
    python scraper.py --full-scan
    python scraper.py --product ERC-32
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, quote

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Required packages: pip install requests beautifulsoup4")
    sys.exit(1)

# Configuration
BASE_URL = "https://acn-tech.com"
CONFIG_FILE = Path(__file__).parent.parent / "acn_tech_config.json"
OUTPUT_FILE = Path(__file__).parent.parent / "products" / "acn_tech_prices.json"
HISTORY_FILE = Path(__file__).parent.parent / "products" / "price_history.json"

# Product categories to scrape
RIBBON_SEARCHES = [
    "Epson ERC-32",
    "Epson ERC-38", 
    "Epson ERC-30",
    "Epson ERC-23",
    "Epson ERC-09",
    "Epson ERC-27",
    "Epson ERC-31"
]

TONER_SEARCHES = [
    "Brother TN-450",
    "Brother TN-660",
    "Brother TN-730",
    "Brother TN-760",
    "HP 83A CF283A",
    "HP 80A CF280A",
    "HP 85A CE285A",
    "HP 12A Q2612A",
    "HP 05A CE505A"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


def load_config():
    """Load ACN-Tech configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def ensure_dirs():
    """Ensure output directories exist"""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def parse_price(price_text):
    """Extract numeric price from text"""
    if not price_text:
        return None
    # Remove currency symbols and whitespace
    price_text = price_text.replace('$', '').replace(',', '').strip()
    # Extract first number
    match = re.search(r'[\d,]+\.?\d*', price_text)
    if match:
        try:
            return float(match.group().replace(',', ''))
        except ValueError:
            return None
    return None


def scrape_search_page(search_term):
    """Scrape search results for a product"""
    search_url = f"{BASE_URL}/search"
    params = {'q': search_term}
    
    try:
        response = requests.get(search_url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        
        # Common e-commerce selectors
        product_selectors = [
            '.product-item',
            '.product',
            '.search-result',
            '[data-product]',
            '.item',
            '.grid-item'
        ]
        
        for selector in product_selectors:
            items = soup.select(selector)
            if items:
                for item in items[:5]:  # Limit to first 5 results
                    product = extract_product_data(item, search_term)
                    if product:
                        products.append(product)
                break
        
        # If no structured products found, try generic extraction
        if not products:
            products = extract_generic_products(soup, search_term)
        
        return products
        
    except requests.RequestException as e:
        print(f"⚠️  Error fetching {search_term}: {e}")
        return []


def extract_product_data(item, search_term):
    """Extract product data from a search result item"""
    product = {
        'source': 'acn-tech.com',
        'search_term': search_term,
        'scraped_at': datetime.now().isoformat()
    }
    
    # Try to find name
    name_selectors = ['.product-name', '.name', 'h2', 'h3', 'h4', '.title', '[data-name]']
    for selector in name_selectors:
        name_elem = item.select_one(selector)
        if name_elem:
            product['name'] = name_elem.get_text(strip=True)
            break
    
    # Try to find price
    price_selectors = ['.price', '.product-price', '.amount', '[data-price]', '.cost']
    for selector in price_selectors:
        price_elem = item.select_one(selector)
        if price_elem:
            price = parse_price(price_elem.get_text())
            if price:
                product['price'] = price
                break
    
    # Try to find SKU
    sku_selectors = ['.sku', '[data-sku]', '.product-sku', '.code']
    for selector in sku_selectors:
        sku_elem = item.select_one(selector)
        if sku_elem:
            product['sku'] = sku_elem.get_text(strip=True)
            break
    
    # Try to find link
    link = item.find('a', href=True)
    if link:
        product['url'] = urljoin(BASE_URL, link['href'])
    
    # Only return if we have name and price
    if 'name' in product and 'price' in product:
        return product
    
    return None


def extract_generic_products(soup, search_term):
    """Generic extraction when no structured data found"""
    products = []
    
    # Look for common patterns
    text = soup.get_text()
    
    # Find price patterns near the search term
    lines = text.split('\n')
    for line in lines:
        if any(term.lower() in line.lower() for term in search_term.split()):
            price = parse_price(line)
            if price:
                products.append({
                    'name': search_term,
                    'price': price,
                    'source': 'acn-tech.com',
                    'search_term': search_term,
                    'scraped_at': datetime.now().isoformat()
                })
    
    return products


def scrape_product_page(url):
    """Scrape detailed product page"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product = {
            'url': url,
            'source': 'acn-tech.com',
            'scraped_at': datetime.now().isoformat()
        }
        
        # Extract name
        name_elem = soup.select_one('h1, .product-title, .product-name')
        if name_elem:
            product['name'] = name_elem.get_text(strip=True)
        
        # Extract price
        price_elem = soup.select_one('.price, .product-price, .current-price')
        if price_elem:
            price = parse_price(price_elem.get_text())
            if price:
                product['price'] = price
        
        # Extract SKU
        sku_elem = soup.select_one('.sku, [data-sku], .product-sku')
        if sku_elem:
            product['sku'] = sku_elem.get_text(strip=True)
        
        # Extract availability
        avail_elem = soup.select_one('.availability, .stock, .in-stock')
        if avail_elem:
            product['availability'] = avail_elem.get_text(strip=True)
        
        return product
        
    except requests.RequestException as e:
        print(f"⚠️  Error fetching product page {url}: {e}")
        return None


def check_prices():
    """Quick price check for configured products"""
    print("🔍 ACN-Tech Price Check")
    print("=" * 60)
    
    config = load_config()
    products = config.get('products', {})
    
    all_results = []
    
    # Check ribbons
    print("\n🎀 Checking Ribbons...")
    for ribbon in products.get('ribbons', []):
        results = scrape_search_page(ribbon['name'])
        if results:
            print(f"   ✓ {ribbon['name']}: ${results[0].get('price', 'N/A')}")
            all_results.extend(results)
        else:
            print(f"   ✗ {ribbon['name']}: Not found")
    
    # Check toner
    print("\n🖨️ Checking Toner...")
    for toner in products.get('toner', []):
        results = scrape_search_page(toner['name'])
        if results:
            print(f"   ✓ {toner['name']}: ${results[0].get('price', 'N/A')}")
            all_results.extend(results)
        else:
            print(f"   ✗ {toner['name']}: Not found")
    
    # Save results
    ensure_dirs()
    price_data = {
        'scraped_at': datetime.now().isoformat(),
        'total_products': len(all_results),
        'products': all_results
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(price_data, f, indent=2)
    
    print(f"\n💾 Saved {len(all_results)} products to {OUTPUT_FILE}")
    
    return all_results


def full_scan():
    """Full catalog scan"""
    print("🔍 ACN-Tech Full Catalog Scan")
    print("=" * 60)
    
    all_results = []
    
    print("\n🎀 Scanning Ribbons...")
    for search in RIBBON_SEARCHES:
        results = scrape_search_page(search)
        all_results.extend(results)
        print(f"   {search}: {len(results)} results")
    
    print("\n🖨️ Scanning Toner...")
    for search in TONER_SEARCHES:
        results = scrape_search_page(search)
        all_results.extend(results)
        print(f"   {search}: {len(results)} results")
    
    # Save results
    ensure_dirs()
    price_data = {
        'scraped_at': datetime.now().isoformat(),
        'total_products': len(all_results),
        'products': all_results
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(price_data, f, indent=2)
    
    print(f"\n💾 Total products saved: {len(all_results)}")
    print(f"📁 Output: {OUTPUT_FILE}")
    
    return all_results


def search_product(sku):
    """Search for specific product by SKU"""
    print(f"🔍 Searching for: {sku}")
    
    results = scrape_search_page(sku)
    
    if results:
        print(f"\n✓ Found {len(results)} results:")
        for r in results:
            print(f"   - {r.get('name', 'N/A')}: ${r.get('price', 'N/A')}")
    else:
        print(f"\n✗ No results found for {sku}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='ACN-Tech Product Scraper')
    parser.add_argument('--check-prices', action='store_true', help='Quick price check')
    parser.add_argument('--full-scan', action='store_true', help='Full catalog scan')
    parser.add_argument('--product', help='Search specific product SKU')
    
    args = parser.parse_args()
    
    if args.full_scan:
        full_scan()
    elif args.product:
        search_product(args.product)
    else:
        check_prices()


if __name__ == '__main__':
    main()
