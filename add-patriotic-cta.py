#!/usr/bin/env python3
"""
Add patriotic CTA footer to all product pages
"""

import os
import re

PATRIOTIC_CSS = """
        .footer-cta {
            max-width: 1200px;
            margin: 3rem auto;
            padding: 2rem;
            background: var(--primary);
            color: white;
            border-radius: 12px;
            text-align: center;
        }
        .footer-cta h3 {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }
        .footer-cta p {
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }
        .footer-cta .phone {
            font-size: 2.5rem;
            font-weight: 800;
            text-decoration: none;
            display: inline-block;
            animation: patrioticBlink 1.5s infinite;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        @keyframes patrioticBlink {
            0%, 33% {
                color: #ff0000;
                text-shadow: 0 0 20px rgba(255,0,0,0.8), 2px 2px 4px rgba(0,0,0,0.3);
            }
            34%, 66% {
                color: #ffffff;
                text-shadow: 0 0 20px rgba(255,255,255,0.8), 2px 2px 4px rgba(0,0,0,0.3);
            }
            67%, 100% {
                color: #0000ff;
                text-shadow: 0 0 20px rgba(0,0,255,0.8), 2px 2px 4px rgba(0,0,0,0.3);
            }
        }

        .footer-cta .phone:hover {
            animation-duration: 0.5s;
        }
"""

PATRIOTIC_HTML = """
    <section class="footer-cta">
        <h3>Questions About This Product?</h3>
        <p>Our team can help you choose the right solution. Call for a free consultation.</p>
        <a href="tel:8888816834" class="phone">(888) 881-6834</a>
    </section>
"""

def add_patriotic_cta(filepath):
    """Add patriotic CTA to a single file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if already has patriotic CTA
    if 'patrioticBlink' in content or 'footer-cta' in content:
        return False, "Already has CTA"
    
    # Add CSS before </style>
    if '.footer-cta' not in content:
        content = content.replace('</style>', PATRIOTIC_CSS + '\n    </style>')
    
    # Add HTML before </body>
    if '<section class="footer-cta"' not in content:
        content = content.replace('</body>', PATRIOTIC_HTML + '\n</body>')
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return True, "Added CTA"

def main():
    products_dir = '/var/www/psdepot.com/products'
    updated = 0
    skipped = 0
    
    print("Adding patriotic CTA to product pages...\n")
    
    for filename in os.listdir(products_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(products_dir, filename)
            success, msg = add_patriotic_cta(filepath)
            if success:
                print(f"  ✅ {filename}")
                updated += 1
            else:
                print(f"  ⏭️ {filename} - {msg}")
                skipped += 1
    
    print(f"\n✅ Updated: {updated} pages")
    print(f"⏭️ Skipped: {skipped} pages (already had CTA)")

if __name__ == '__main__':
    main()
