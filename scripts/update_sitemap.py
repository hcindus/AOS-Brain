#!/usr/bin/env python3
"""Update psdepot.com sitemap with all current pages"""

import os
from datetime import datetime
from urllib.parse import quote

BASE_DIR = "/var/www/psdepot.com"
SITEMAP_FILE = f"{BASE_DIR}/sitemap.xml"
DOMAIN = "https://psdepot.com"

def get_file_date(filepath):
    """Get last modified date of file"""
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')

def get_priority(url_path):
    """Determine priority based on URL structure"""
    if url_path == "" or url_path == "index.html":
        return "1.0"
    elif "products/" in url_path:
        if "index.html" in url_path:
            return "0.9"  # Category pages
        else:
            return "0.8"  # Product pages
    elif any(city in url_path for city in ['california', 'texas', 'florida', 'new-york', 'illinois']):
        return "0.9"  # State pages
    elif any(city in url_path for city in ['los-angeles', 'chicago', 'houston', 'phoenix', 'philadelphia', 
                                             'san-antonio', 'san-diego', 'dallas', 'san-jose', 'austin',
                                             'jacksonville', 'fort-worth', 'columbus', 'charlotte',
                                             'indianapolis', 'san-francisco', 'seattle', 'denver',
                                             'washington', 'boston', 'el-paso', 'detroit', 'nashville',
                                             'portland', 'oklahoma-city', 'las-vegas', 'louisville',
                                             'baltimore', 'milwaukee', 'albuquerque', 'tucson', 'fresno',
                                             'sacramento', 'mesa', 'kansas-city', 'atlanta', 'miami']):
        return "0.9"  # Major city pages
    elif url_path in ['about.html', 'contact.html', 'checkout.html', 'booking.html']:
        return "0.8"
    else:
        return "0.7"

def get_changefreq(url_path):
    """Determine change frequency"""
    if url_path == "" or url_path == "index.html":
        return "daily"
    elif "products/" in url_path:
        return "weekly"
    elif any(x in url_path for x in ['california', 'texas', 'florida', 'new-york', 'chicago', 'los-angeles']):
        return "weekly"
    else:
        return "monthly"

def generate_sitemap():
    """Generate complete sitemap"""
    urls = []
    
    # Scan root directory
    for filename in os.listdir(BASE_DIR):
        if filename.endswith('.html') and not filename.startswith('.'):
            filepath = os.path.join(BASE_DIR, filename)
            if os.path.isfile(filepath):
                url_path = filename if filename != 'index.html' else ''
                urls.append({
                    'loc': f"{DOMAIN}/{url_path}" if url_path else DOMAIN,
                    'lastmod': get_file_date(filepath),
                    'changefreq': get_changefreq(url_path),
                    'priority': get_priority(url_path)
                })
    
    # Scan products directory
    products_dir = os.path.join(BASE_DIR, 'products')
    if os.path.exists(products_dir):
        for root, dirs, files in os.walk(products_dir):
            for filename in files:
                if filename.endswith('.html'):
                    filepath = os.path.join(root, filename)
                    rel_path = os.path.relpath(filepath, BASE_DIR)
                    url_path = rel_path.replace('\\', '/')
                    
                    urls.append({
                        'loc': f"{DOMAIN}/{url_path}",
                        'lastmod': get_file_date(filepath),
                        'changefreq': get_changefreq(url_path),
                        'priority': get_priority(url_path)
                    })
    
    # Sort by priority (highest first), then alphabetically
    urls.sort(key=lambda x: (-float(x['priority']), x['loc']))
    
    # Generate XML
    today = datetime.now().strftime('%Y-%m-%d')
    
    xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''
    
    # Add homepage with language alternates
    xml += '''  <url>
    <loc>https://psdepot.com/</loc>
    <lastmod>{}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://psdepot.com/" />
    <xhtml:link rel="alternate" hreflang="es" href="https://psdepot.com/chinese.html" />
  </url>

'''.format(today)
    
    # Add all other URLs
    for url in urls:
        if url['loc'] == DOMAIN:  # Skip homepage, already added
            continue
            
        xml += '''  <url>
    <loc>{}</loc>
    <lastmod>{}</lastmod>
    <changefreq>{}</changefreq>
    <priority>{}</priority>
  </url>

'''.format(
            url['loc'],
            url['lastmod'],
            url['changefreq'],
            url['priority']
        )
    
    xml += '</urlset>\n'
    
    # Write to file
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(xml)
    
    # Generate statistics
    by_priority = {}
    for url in urls:
        p = url['priority']
        by_priority[p] = by_priority.get(p, 0) + 1
    
    return len(urls), by_priority

if __name__ == "__main__":
    count, stats = generate_sitemap()
    print(f"✅ Sitemap updated: {SITEMAP_FILE}")
    print(f"\nTotal URLs: {count}")
    print("\nBy Priority:")
    for priority in sorted(stats.keys(), reverse=True):
        print(f"  Priority {priority}: {stats[priority]} URLs")
