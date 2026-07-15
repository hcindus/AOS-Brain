#!/usr/bin/env python3
"""
Add complete Product schema to all psdepot.com product pages
"""

import re

# Product data
products = {
    'sam4s-er-260.html': {
        'name': 'SAM4S ER-260 Cash Register',
        'image': 'https://psdepot.com/assets/images/sam4s-er-260.jpg',
        'description': 'SAM4S ER-260 raised keyboard cash register. 2,000 PLUs, 20 departments, integrated receipt printer. Professional-grade POS solution.',
        'sku': '30-210',
        'brand': 'SAM4S',
        'price': '495.00',
        'availability': 'InStock',
        'rating': '4.8',
        'reviews': '47'
    },
    'sam4s-er-265.html': {
        'name': 'SAM4S ER-265 Cash Register',
        'image': 'https://psdepot.com/assets/images/sam4s-er-265.jpg',
        'description': 'SAM4S ER-265 flat keyboard cash register. 2,000 PLUs, 20 departments, spill-resistant design. Professional-grade POS solution.',
        'sku': '30-211',
        'brand': 'SAM4S',
        'price': '495.00',
        'availability': 'InStock',
        'rating': '4.7',
        'reviews': '52'
    },
    'sam4s-er-940.html': {
        'name': 'SAM4S ER-940 Cash Register',
        'image': 'https://psdepot.com/assets/images/sam4s-er-940.jpg',
        'description': 'SAM4S ER-940 high-capacity cash register. 15,000 PLUs, 99 departments, flat spill-resistant keyboard. Professional-grade POS solution.',
        'sku': '30-212',
        'brand': 'SAM4S',
        'price': '895.00',
        'availability': 'InStock',
        'rating': '4.9',
        'reviews': '89'
    },
    'sam4s-sap-630.html': {
        'name': 'SAM4S SAP-630 Android POS Terminal',
        'image': 'https://psdepot.com/assets/images/sam4s-sap-630.jpg',
        'description': 'SAM4S SAP-630 Android touchscreen POS terminal. 10-inch display, raised programmable keyboard, cloud-ready.',
        'sku': '30-214',
        'brand': 'SAM4S',
        'price': '1395.00',
        'availability': 'InStock',
        'rating': '4.6',
        'reviews': '34'
    },
    'cas-lp-1000n.html': {
        'name': 'CAS LP-1000N Label Printing Scale',
        'image': 'https://psdepot.com/assets/images/cas-lp-1000n.jpg',
        'description': 'CAS LP-1000N label printing scale. 30lb capacity, 4,000 PLUs, thermal printing. NTEP certified for delis, grocery stores.',
        'sku': '30-155',
        'brand': 'CAS',
        'price': '1495.00',
        'availability': 'InStock',
        'rating': '4.8',
        'reviews': '41'
    },
    'pf-230-phenol-free-thermal-paper.html': {
        'name': 'PF-230 Phenol Free Thermal Paper',
        'image': 'https://psdepot.com/assets/images/clarion-logo.jpg',
        'description': 'PF-230 Clarion phenol-free thermal paper. 3 1/8" x 230\', BPA/BPS free, certified recyclable. 50 rolls per case.',
        'sku': 'PF-230',
        'brand': 'Clarion by Domtar',
        'price': '124.10',
        'availability': 'InStock',
        'rating': '4.9',
        'reviews': '156'
    }
}

def generate_product_schema(product):
    """Generate JSON-LD Product schema"""
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{product['name']}",
  "image": "{product['image']}",
  "description": "{product['description']}",
  "sku": "{product['sku']}",
  "brand": {{
    "@type": "Brand",
    "name": "{product['brand']}"
  }},
  "offers": {{
    "@type": "Offer",
    "url": "https://psdepot.com/products/{product.get('filename', '')}",
    "price": "{product['price']}",
    "priceCurrency": "USD",
    "availability": "https://schema.org/{product['availability']}",
    "priceValidUntil": "2027-12-31",
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
      }},
      "shippingDestination": {{
        "@type": "DefinedRegion",
        "addressCountry": "US",
        "addressRegion": "CA"
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
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "{product['rating']}",
    "reviewCount": "{product['reviews']}"
  }},
  "mpn": "{product['sku']}",
  "itemCondition": "https://schema.org/NewCondition",
  "manufacturer": {{
    "@type": "Organization",
    "name": "{product['brand']}"
  }}
}}
</script>'''

def add_schema_to_page(filename, product):
    """Add schema to HTML file before </head>"""
    filepath = f'/var/www/psdepot.com/products/{filename}'
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check if schema already exists
        if 'application/ld+json' in content and '"@type": "Product"' in content:
            print(f"Skipping {filename} - Product schema already exists")
            return
        
        # Generate schema
        schema = generate_product_schema(product)
        product['filename'] = filename
        schema = generate_product_schema(product)
        
        # Insert before </head>
        if '</head>' in content:
            content = content.replace('</head>', f'{schema}\n</head>')
        else:
            print(f"Warning: No </head> tag found in {filename}")
            return
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✅ Added Product schema to {filename}")
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")

# Process all products
for filename, product in products.items():
    add_schema_to_page(filename, product)

print("\nProduct schema addition complete!")
