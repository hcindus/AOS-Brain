#!/usr/bin/env python3
"""
Fix cart system on all SAM4S product pages to match psdepot.com main page
Uses simple localStorage cart (psdepot_cart) with link to checkout.html
"""

import re

# Simple cart JavaScript that matches the main page
cart_js = '''
    <script>
        // Cart Management - Matches main psdepot.com
        function getCart() {
            return JSON.parse(localStorage.getItem('psdepot_cart') || '[]');
        }

        function saveCart(cart) {
            localStorage.setItem('psdepot_cart', JSON.stringify(cart));
            updateCartCount();
        }

        function updateCartCount() {
            const cart = getCart();
            const count = cart.reduce((sum, item) => sum + item.quantity, 0);
            const cartCountEl = document.getElementById('cart-count');
            if (cartCountEl) cartCountEl.textContent = count;
        }

        function addToCartFromPage() {
            const sku = '{SKU}';
            const name = 'SAM4S {MODEL} Cash Register';
            const price = {PRICE_RAW};
            const qty = parseInt(document.getElementById('quantity').value) || 1;
            
            let cart = getCart();
            const existing = cart.find(item => item.sku === sku);
            
            if (existing) {
                existing.quantity += qty;
            } else {
                cart.push({ sku, name, price, quantity: qty });
            }
            
            saveCart(cart);
            
            // Visual feedback
            const btn = document.getElementById('addToCartBtn');
            const originalText = btn.textContent;
            btn.textContent = '✓ Added!';
            btn.style.background = '#48bb78';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
            }, 1500);
        }

        function updateQuantity(change) {
            const input = document.getElementById('quantity');
            let value = parseInt(input.value) + change;
            if (value < 1) value = 1;
            if (value > 10) value = 10;
            input.value = value;
        }

        // Initialize cart count on load
        updateCartCount();
    </script>
'''

# Cart icon for header
cart_icon_html = '''<a href="/checkout.html" class="cart-icon" style="color: white; text-decoration: none; margin-left: 2rem; display: flex; align-items: center; gap: 0.5rem;">
                🛒 Cart (<span id="cart-count">0</span>)
            </a>'''

def fix_page(filepath, model, sku, price):
    """Fix a product page to use the standard cart system"""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace the entire cart sidebar and complex JS with simple version
    # Find where cart sidebar starts and script ends
    if 'cart-sidebar' in content:
        # Remove cart sidebar HTML
        content = re.sub(
            r'<div class="cart-overlay".*?\/script>\s*<\/body>',
            cart_js.replace('{SKU}', sku).replace('{MODEL}', model).replace('{PRICE_RAW}', price) + '\n</body>',
            content,
            flags=re.DOTALL
        )
    else:
        # Just replace the script section
        content = re.sub(
            r'<script>.*<\/script>\s*<\/body>',
            cart_js.replace('{SKU}', sku).replace('{MODEL}', model).replace('{PRICE_RAW}', price) + '\n</body>',
            content,
            flags=re.DOTALL
        )
    
    # Update the Add to Cart button to call new function
    content = content.replace(
        'onclick="addToCart()"',
        'onclick="addToCartFromPage()" id="addToCartBtn"'
    )
    
    # Replace cart icon in header
    if 'cart-icon' in content and 'onclick="toggleCart()"' in content:
        content = re.sub(
            r'<div class="cart-icon" onclick="toggleCart\(\)".*?</div>',
            cart_icon_html,
            content,
            flags=re.DOTALL
        )
    
    # Remove cart overlay if present
    content = re.sub(r'<div class="cart-overlay".*?<\/div>\s*<div class="cart-sidebar".*?<\/div>', '', content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Fixed: {filepath}")

# Fix all pages
pages = [
    ('/var/www/psdepot.com/products/sam4s-er-260.html', 'ER-260', '30-210', '495.00'),
    ('/var/www/psdepot.com/products/sam4s-er-265.html', 'ER-265', '30-211', '495.00'),
    ('/var/www/psdepot.com/products/sam4s-er-940.html', 'ER-940', '30-212', '895.00'),
    ('/var/www/psdepot.com/products/sam4s-sap-630.html', 'SAP-630', '30-214', '1395.00'),
]

for filepath, model, sku, price in pages:
    fix_page(filepath, model, sku, price)

print("\nAll pages now use the standard psdepot.com cart system:")
print("  • localStorage key: 'psdepot_cart'")
print("  • Cart links to /checkout.html")
print("  • Visual feedback: '✓ Added!' in green")
print("  • Cart count updates across all pages")
