#!/usr/bin/env python3
"""
Generate HTML product pages from M-S Cash Drawer catalog JSON
Usage: python3 generate-product-pages.py
"""

import json
import os
import re
from datetime import datetime

def load_catalog():
    """Load the product catalog JSON"""
    with open('products-catalog.json', 'r') as f:
        return json.load(f)

def load_template():
    """Load the HTML template"""
    with open('product-page-template.html', 'r') as f:
        return f.read()

def generate_product_schema(product, category):
    """Generate JSON-LD Product schema"""
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{product['name']}",
  "image": "{product['images']['primary']}",
  "description": "{product['description']}",
  "sku": "{product['sku']}",
  "mpn": "{product['mpn']}",
  "brand": {{
    "@type": "Brand",
    "name": "{product['brand']}"
  }},
  "category": "{category['name']}",
  "offers": {{
    "@type": "Offer",
    "url": "https://psdepot.com/products/{slugify(product['name'])}.html",
    "price": "{product['price']['msrp']}",
    "priceCurrency": "USD",
    "availability": "https://schema.org/{product['availability']}",
    "priceValidUntil": "2027-12-31",
    "seller": {{
      "@type": "Organization",
      "name": "Performance Supply Depot LLC"
    }},
    "shippingDetails": {{
      "@type": "OfferShippingDetails",
      "shippingRate": {{
        "@type": "MonetaryAmount",
        "value": "0",
        "currency": "USD"
      }},
      "deliveryTime": {{
        "@type": "ShippingDeliveryTime",
        "handlingTime": {{
          "@type": "QuantitativeValue",
          "minValue": "0",
          "maxValue": "1",
          "unitCode": "DAY"
        }},
        "transitTime": {{
          "@type": "QuantitativeValue",
          "minValue": "1",
          "maxValue": "5",
          "unitCode": "DAY"
        }}
      }}
    }},
    "hasMerchantReturnPolicy": {{
      "@type": "MerchantReturnPolicy",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 30,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/FreeReturn"
    }}
  }},
  "itemCondition": "https://schema.org/NewCondition",
  "manufacturer": {{
    "@type": "Organization",
    "name": "{product['brand']}"
  }}
}}
</script>'''

def generate_features_list(features):
    """Generate HTML for features list"""
    return '\n'.join([f'<li>{feature}</li>' for feature in features])

def generate_specs_table(specs):
    """Generate HTML for specifications table"""
    rows = []
    for key, value in specs.items():
        label = key.replace('_', ' ').title()
        rows.append(f'<tr><th>{label}</th><td>{value}</td></tr>')
    return '\n'.join(rows)

def generate_compatibility_tags(compatibility):
    """Generate HTML for compatibility tags"""
    return '\n'.join([f'<span class="compatibility-tag">{item}</span>' for item in compatibility])

def generate_rating_stars(rating):
    """Generate star rating HTML"""
    full_stars = int(float(rating))
    has_half = float(rating) - full_stars >= 0.5
    stars = '★' * full_stars
    if has_half:
        stars += '½'
    stars += '☆' * (5 - full_stars - (1 if has_half else 0))
    return stars

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower().replace(' ', '-')
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def generate_product_page(product, category, template):
    """Generate a single product page"""
    
    # Basic replacements
    page = template
    page = page.replace('{{PRODUCT_NAME}}', product['name'])
    page = page.replace('{{PRODUCT_DESCRIPTION_SHORT}}', product['description'][:160])
    page = page.replace('{{PRODUCT_DESCRIPTION_FULL}}', f'<p>{product["description"]}</p>')
    page = page.replace('{{PRODUCT_KEYWORDS}}', ', '.join(product.get('tags', []) + [product['brand'], category['name']]))
    page = page.replace('{{PRODUCT_IMAGE}}', product['images']['primary'])
    page = page.replace('{{PRODUCT_SLUG}}', slugify(product['name']))
    page = page.replace('{{CATEGORY_NAME}}', category['name'])
    page = page.replace('{{CATEGORY_SLUG}}', slugify(category['name']))
    page = page.replace('{{BRAND_NAME}}', product['brand'])
    page = page.replace('{{BRAND_SLUG}}', slugify(product['brand']))
    page = page.replace('{{SKU}}', product['sku'])
    page = page.replace('{{MPN}}', product['mpn'])
    page = page.replace('{{PRICE}}', product['price']['msrp'])
    page = page.replace('{{MSRP}}', product['price']['msrp'])
    page = page.replace('{{WARRANTY}}', product['warranty'])
    page = page.replace('{{RATING_STARS}}', generate_rating_stars(product.get('rating', '4.5')))
    page = page.replace('{{REVIEW_COUNT}}', product.get('reviews', '0'))
    
    # Schema
    page = page.replace('{{PRODUCT_SCHEMA}}', generate_product_schema(product, category))
    
    # Features
    page = page.replace('{{FEATURES_LIST}}', generate_features_list(product['features']))
    
    # Specifications
    page = page.replace('{{SPECIFICATIONS_TABLE}}', generate_specs_table(product['specs']))
    
    # Compatibility
    page = page.replace('{{COMPATIBILITY_TAGS}}', generate_compatibility_tags(product['compatibility']))
    
    # Availability
    avail_class = product['availability'].lower().replace(' ', '-')
    avail_text = 'In Stock' if product['availability'] == 'InStock' else product['availability']
    page = page.replace('{{AVAILABILITY_CLASS}}', avail_class)
    page = page.replace('{{AVAILABILITY_TEXT}}', avail_text)
    page = page.replace('{{HAS_MSRP}}', 'false')
    page = page.replace('{{SAVINGS}}', '')
    page = page.replace('{{SAVINGS_PERCENT}}', '')
    
    # Clean up template tags
    page = re.sub(r'\{\{#if\s+.*?\}\}', '', page)
    page = re.sub(r'\{\{/if\}\}', '', page)
    page = re.sub(r'\{\{#each\s+.*?\}\}', '', page)
    page = re.sub(r'\{\{/each\}\}', '', page)
    page = re.sub(r'\{\{.*?\}\}', '', page)
    
    return page

def generate_related_product_card(product):
    """Generate a related product card"""
    return f'''
<div class="related-card">
    <div class="related-card-image">
        <img src="{product['images']['primary']}" alt="{product['name']}">
    </div>
    <div class="related-card-info">
        <h4>{product['name']}</h4>
        <div class="related-card-price">${product['price']['msrp']}</div>
    </div>
</div>'''

def main():
    """Main generation function"""
    print("=" * 60)
    print("M-S Cash Drawer Product Page Generator")
    print("=" * 60)
    
    # Load data
    print("\n📂 Loading catalog...")
    catalog = load_catalog()
    print(f"✅ Loaded catalog with {len(catalog['categories'])} categories")
    
    print("\n📂 Loading template...")
    template = load_template()
    print("✅ Template loaded")
    
    # Create output directory
    output_dir = '../psdepot/products/mscashdrawer'
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n📁 Output directory: {output_dir}")
    
    # Generate pages
    generated_count = 0
    all_products = []
    
    for category in catalog['categories']:
        print(f"\n📂 Processing category: {category['name']}")
        
        for product in category['products']:
            all_products.append((product, category))
            
            # Generate page
            page = generate_product_page(product, category, template)
            
            # Add related products
            related = [p for p, c in all_products[:-1]][-3:] if len(all_products) > 1 else []
            related_html = '\n'.join([generate_related_product_card(p) for p in related])
            page = page.replace('{{RELATED_PRODUCTS}}', related_html)
            page = page.replace('{{GALLERY_IMAGES}}', '')
            
            # Save file
            filename = f"{slugify(product['name'])}.html"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(page)
            
            generated_count += 1
            print(f"  ✅ Generated: {filename}")
    
    print("\n" + "=" * 60)
    print(f"🎉 Generation complete! Created {generated_count} product pages")
    print(f"📁 Location: {output_dir}/")
    print("=" * 60)
    
    # Generate summary report
    print("\n📊 Catalog Summary:")
    print(f"  Total Categories: {len(catalog['categories'])}")
    print(f"  Total Products: {generated_count}")
    
    for category in catalog['categories']:
        print(f"\n  📁 {category['name']}: {len(category['products'])} products")
        for product in category['products']:
            print(f"     • {product['name']} (${product['price']['msrp']})")

if __name__ == '__main__':
    main()
