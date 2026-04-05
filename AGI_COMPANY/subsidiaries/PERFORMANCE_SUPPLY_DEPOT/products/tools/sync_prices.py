#!/usr/bin/env python3
"""
PSDepot Price Sync Tool
Automatically updates index.html from psdepot_prices.json
"""

import json
import re
from datetime import datetime

PRICE_FILE = '/root/.openclaw/workspace/aocros/performance_supply_depot/prices/psdepot_prices.json'
HTML_FILE = '/root/.openclaw/workspace/aocros/projects/websites/performance-supply-depot/index.html'

def load_prices():
    """Load prices from JSON file"""
    with open(PRICE_FILE, 'r') as f:
        return json.load(f)

def generate_product_card(product):
    """Generate HTML for a single product card"""
    sku = product['sku']
    desc = product['description']
    price = product['price']
    qty = product.get('qty', 'ea')
    category = product.get('category', 'Other')
    
    # Determine icon based on category
    icons = {
        'Paper': '📄',
        'Ribbons': '🎀',
        'Hardware': '🖥️',
        'Software': '💻',
        'Accessories': '🔧',
        'Labels': '🏷️',
        'Services': '🔧'
    }
    icon = icons.get(category, '📦')
    
    # Format price display
    if qty in ['per hour', 'per roll', 'per dozen']:
        price_display = f"${price:,.2f}"
        unit_display = f"({qty})"
    elif qty == 'flat rate':
        price_display = f"${price:,.2f}"
        unit_display = "(flat rate)"
    else:
        price_display = f"${price:,.2f}"
        unit_display = f"({qty})"
    
    return f'''            <div class="product-card">
                <div class="product-image">{icon}</div>
                <div class="product-content">
                    <h3>{desc.split("-")[0].strip() if "-" in desc else desc[:30]}</h3>
                    <p class="sku">SKU: {sku}</p>
                    <p>{desc}</p>
                    <ul class="product-features">
                        <li>Professional grade</li>
                        <li>In stock</li>
                        <li>Fast shipping</li>
                    </ul>
                    <p class="price">{price_display} <span class="unit">{unit_display}</span></p>
                </div>
            </div>'''

def generate_category_section(category, products):
    """Generate HTML for a category section"""
    icons = {
        'Paper': '📄',
        'Ribbons': '🎀',
        'Hardware': '🖥️',
        'Software': '💻',
        'Accessories': '🔧',
        'Labels': '🏷️',
        'Services': '🔧',
        'Other': '📦'
    }
    icon = icons.get(category, '📦')
    
    cards = '\n'.join(generate_product_card(p) for p in products)
    
    return f'''        <!-- {category} -->
        <h3 class="category-title">{icon} {category}</h3>
        <div class="products-grid">
{cards}
        </div>'''

def generate_products_section(data):
    """Generate complete products section HTML"""
    # Group by category
    categories = {}
    for p in data['products']:
        cat = p.get('category', 'Other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)
    
    # Define category order
    order = ['Paper', 'Ribbons', 'Hardware', 'Software', 'Accessories', 'Labels', 'Services', 'Other']
    
    sections = []
    for cat in order:
        if cat in categories:
            sections.append(generate_category_section(cat, categories[cat]))
    
    sections_html = '\n\n'.join(sections)
    
    return f'''<!-- Products Section -->
<section id="products" class="products">
    <div class="container">
        <div class="section-header">
            <h2>Our Product Line</h2>
            <p>Premium quality POS supplies designed for high-volume environments. All products tested for compatibility and reliability.</p>
            <p class="last-updated"><small>Prices updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</small></p>
        </div>

{sections_html}
    </div>
</section>'''

def update_website():
    """Update the website HTML with current prices"""
    # Load prices
    data = load_prices()
    
    # Generate new products section
    new_section = generate_products_section(data)
    
    # Read current HTML
    with open(HTML_FILE, 'r') as f:
        content = f.read()
    
    # Replace products section
    pattern = r'(<!-- Products Section -->\s*<section id="products".*?)</section\u003e'
    new_content = re.sub(pattern, new_section.strip(), content, flags=re.DOTALL)
    
    # Write back
    with open(HTML_FILE, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Website updated with {data['total_products']} products!")
    print(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    
    return True

if __name__ == '__main__':
    update_website()