#!/usr/bin/env python3
"""
Fix cart alignment on all SAM4S product pages to match psdepot.com main page
Cart goes in a contact-info div on the right side
"""

import re

# New header structure matching main page
new_header_html = '''<header class="header">
    <div class="header-content">
        <div class="logo">Performance <span>Supply Depot</span></div>
        <div class="contact-info">
            <a href="tel:888-881-6834">📞 (888) 881-6834</a>
            <a href="/checkout.html" class="cart-icon">
                🛒 Cart (<span id="cart-count">0</span>)
            </a>
        </div>
    </div>
</header>'''

# CSS to add for contact-info layout
css_addition = '''
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        
        .contact-info {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        .contact-info a {
            color: white;
            text-decoration: none;
            font-size: 0.95rem;
            transition: opacity 0.2s;
        }
        
        .contact-info a:hover { opacity: 0.8; }
        
        .cart-icon {
            background: rgba(255,255,255,0.1);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
'''

pages = [
    '/var/www/psdepot.com/products/sam4s-er-260.html',
    '/var/www/psdepot.com/products/sam4s-er-265.html',
    '/var/www/psdepot.com/products/sam4s-er-940.html',
    '/var/www/psdepot.com/products/sam4s-sap-630.html'
]

for filepath in pages:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find and replace the entire header section
    header_pattern = r'(<header class="header">.*?)</div>\s*</header>'
    
    if re.search(header_pattern, content, re.DOTALL):
        content = re.sub(header_pattern, new_header_html.strip(), content, flags=re.DOTALL)
        print(f"Fixed header: {filepath}")
    else:
        print(f"Header not found in: {filepath}")
        continue
    
    # Remove old nav styles and add contact-info styles
    # Find .header-nav styles and replace with .contact-info styles
    nav_styles = r'\.header-nav\s*\{[^}]*\}(?:\s*\.header-nav\s*a\s*\{[^}]*\}(?:\s*\.header-nav\s*a:hover\s*\{[^}]*\})?)?'
    
    if re.search(nav_styles, content):
        content = re.sub(nav_styles, css_addition.strip(), content)
        print(f"  Fixed CSS")
    
    with open(filepath, 'w') as f:
        f.write(content)

print("\nAll pages updated with:")
print("  • Cart in contact-info div on the right")
print("  • Phone number next to cart")
print("  • Matches psdepot.com main page layout")
