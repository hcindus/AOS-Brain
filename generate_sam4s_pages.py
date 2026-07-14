#!/usr/bin/env python3
"""
Generate SAM4S ER-260 and ER-265 product pages from ER-940 template
"""

template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAM4S {MODEL} Cash Register | Performance Supply Depot LLC</title>
    <meta name="description" content="SAM4S {MODEL} {KEYBOARD_TYPE} keyboard cash register. {PLU_CAPACITY} PLUs, {DEPARTMENTS} departments, integrated receipt printer. Professional-grade POS solution for retail and food service.">
    <link rel="canonical" href="https://psdepot.com/products/sam4s-{MODEL_LOWER}.html">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    
    <style>
        :root {{
            --primary: #1a365d;
            --primary-dark: #0f2744;
            --accent: #d69e2e;
            --accent-hover: #b7791f;
            --bg: #f7fafc;
            --card: #ffffff;
            --text: #2d3748;
            --text-muted: #718096;
            --border: #e2e8f0;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        
        .header {{
            background: var(--primary);
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
        }}
        
        .logo span {{
            color: var(--accent);
        }}
        
        .header-nav a {{
            color: white;
            text-decoration: none;
            margin-left: 2rem;
            opacity: 0.9;
            transition: opacity 0.2s;
        }}
        
        .header-nav a:hover {{
            opacity: 1;
        }}
        
        .breadcrumb {{
            max-width: 1200px;
            margin: 1rem auto;
            padding: 0 2rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }}
        
        .breadcrumb a {{
            color: var(--primary);
            text-decoration: none;
        }}
        
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        
        .product-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
        }}
        
        @media (max-width: 768px) {{
            .product-container {{
                grid-template-columns: 1fr;
                gap: 2rem;
                padding: 1rem;
            }}
        }}
        
        .product-image-section {{
            background: var(--card);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .product-image {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            display: block;
        }}
        
        .image-caption {{
            text-align: center;
            margin-top: 1rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }}
        
        .product-info {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        .sku-badge {{
            display: inline-block;
            background: #edf2f7;
            color: var(--text-muted);
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .product-title {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            line-height: 1.2;
        }}
        
        .product-subtitle {{
            font-size: 1.125rem;
            color: var(--text-muted);
        }}
        
        .price-section {{
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .price {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
        }}
        
        .price-note {{
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }}
        
        .stock-status {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 1rem;
            color: #38a169;
            font-weight: 500;
        }}
        
        .stock-dot {{
            width: 8px;
            height: 8px;
            background: #38a169;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        .cta-buttons {{
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .btn-primary {{
            flex: 1;
            background: var(--accent);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .btn-primary:hover {{
            background: var(--accent-hover);
            transform: translateY(-1px);
        }}
        
        .btn-secondary {{
            flex: 1;
            background: transparent;
            color: var(--primary);
            border: 2px solid var(--border);
            padding: 1rem 2rem;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            text-align: center;
        }}
        
        .btn-secondary:hover {{
            border-color: var(--primary);
            background: rgba(26, 54, 93, 0.05);
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        @media (max-width: 768px) {{
            .features-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .feature-item {{
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding: 0.75rem;
            background: #f7fafc;
            border-radius: 8px;
        }}
        
        .feature-icon {{
            width: 24px;
            height: 24px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.75rem;
            flex-shrink: 0;
        }}
        
        .feature-text {{
            font-size: 0.9rem;
        }}
        
        .tabs-section {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        
        .tabs {{
            display: flex;
            border-bottom: 2px solid var(--border);
            margin-bottom: 1.5rem;
        }}
        
        .tab {{
            padding: 1rem 2rem;
            background: none;
            border: none;
            font-size: 1rem;
            font-weight: 500;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
        }}
        
        .tab.active {{
            color: var(--primary);
            border-bottom-color: var(--accent);
        }}
        
        .tab-content {{
            background: var(--card);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .specs-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .specs-table tr {{
            border-bottom: 1px solid var(--border);
        }}
        
        .specs-table tr:last-child {{
            border-bottom: none;
        }}
        
        .specs-table td {{
            padding: 1rem;
        }}
        
        .specs-table td:first-child {{
            font-weight: 600;
            color: var(--text-muted);
            width: 40%;
        }}
        
        .description-content {{
            line-height: 1.8;
        }}
        
        .description-content h3 {{
            color: var(--primary);
            margin: 1.5rem 0 0.75rem;
            font-size: 1.25rem;
        }}
        
        .description-content p {{
            margin-bottom: 1rem;
        }}
        
        .description-content ul {{
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        .description-content li {{
            margin-bottom: 0.5rem;
        }}
        
        .footer-cta {{
            max-width: 1200px;
            margin: 3rem auto;
            padding: 2rem;
            background: var(--primary);
            color: white;
            border-radius: 12px;
            text-align: center;
        }}
        
        .footer-cta h3 {{
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .footer-cta p {{
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }}
        
        .footer-cta .phone {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--accent);
            text-decoration: none;
        }}
        
        .footer {{
            background: var(--primary-dark);
            color: white;
            padding: 2rem;
            text-align: center;
            font-size: 0.875rem;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">Performance <span>Supply Depot</span></div>
            <nav class="header-nav">
                <a href="/">Home</a>
                <a href="/#products">Products</a>
                <a href="/contact.html">Contact</a>
            </nav>
        </div>
    </header>
    
    <div class="breadcrumb">
        <a href="/">Home</a> / <a href="/#hardware">POS Hardware</a> / SAM4S {MODEL}
    </div>
    
    <main class="product-container">
        <div class="product-image-section">
            <img src="/assets/images/sam4s-{MODEL_LOWER}.jpg" alt="SAM4S {MODEL} Cash Register with {KEYBOARD_TYPE_DESC} keyboard" class="product-image">
            <p class="image-caption">SAM4S {MODEL} — Professional Cash Register with {KEYBOARD_TYPE} Keyboard</p>
        </div>
        
        <div class="product-info">
            <div>
                <span class="sku-badge">SKU: {SKU}</span>
                <h1 class="product-title">SAM4S {MODEL} Cash Register</h1>
                <p class="product-subtitle">{KEYBOARD_TYPE} Keyboard • {PLU_CAPACITY} PLUs • {DEPARTMENTS} Departments</p>
            </div>
            
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">{PLU_CAPACITY} PLU capacity</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">{DEPARTMENTS} departments</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">{KEYBOARD_TYPE} keyboard design</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">Integrated receipt printer</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">POP-up customer display</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">No monthly fees</span>
                </div>
            </div>
            
            <div class="price-section">
                <div class="price">${PRICE}</div>
                <div class="price-note">Free shipping within California</div>
                <div class="stock-status">
                    <span class="stock-dot"></span>
                    In Stock — Ships within 24 hours
                </div>
                <div class="cta-buttons">
                    <button class="btn-primary" onclick="alert('Call (888) 881-6834 to order or request a quote')">Order Now</button>
                    <a href="/contact.html" class="btn-secondary">Request Quote</a>
                </div>
            </div>
        </div>
    </main>
    
    <section class="tabs-section">
        <div class="tabs">
            <button class="tab active" onclick="showTab('description')">Description</button>
            <button class="tab" onclick="showTab('specs')">Specifications</button>
            <button class="tab" onclick="showTab('support')">Support</button>
        </div>
        
        <div id="description" class="tab-content">
            <div class="description-content">
                <h3>{DESCRIPTION_TITLE}</h3>
                <p>The SAM4S {MODEL} is a reliable electronic cash register designed for small to medium businesses. With its {KEYBOARD_TYPE_DESC} keyboard and POP-up customer display, it delivers the functionality you need at an affordable price point.</p>
                
                <h3>Key Features</h3>
                <ul>
                    <li><strong>{PLU_CAPACITY} PLU Capacity:</strong> Handle your product catalog with ease</li>
                    <li><strong>{DEPARTMENTS} Departments:</strong> Organize sales by category for detailed reporting</li>
                    <li><strong>{KEYBOARD_TYPE} Keyboard:</strong> {KEYBOARD_BENEFIT}</li>
                    <li><strong>Dual Receipt Printer:</strong> Journal + receipt printer with auto-cutter</li>
                    <li><strong>POP-up Customer Display:</strong> Clear visibility with item name and price</li>
                    <li><strong>Multiple Payment Options:</strong> Cash, check, credit, and multiple tender types</li>
                </ul>
                
                <h3>Ideal For</h3>
                <ul>
                    <li>Small restaurants and cafes</li>
                    <li>Retail stores</li>
                    <li>Convenience stores</li>
                    <li>Quick-service establishments</li>
                    <li>Pop-up shops and seasonal businesses</li>
                </ul>
                
                <h3>Why Choose the {MODEL}?</h3>
                <p>Unlike cloud-based POS systems with recurring monthly fees, the {MODEL} is a one-time purchase. Program it once, and it runs independently — no internet required, no subscription costs, no surprises. Perfect for businesses that need reliable, offline-capable transaction processing at an entry-level price.</p>
            </div>
        </div>
        
        <div id="specs" class="tab-content" style="display: none;">
            <table class="specs-table">
                <tr><td>Model</td><td>SAM4S {MODEL}</td></tr>
                <tr><td>Keyboard Type</td><td>{KEYBOARD_TYPE}</td></tr>
                <tr><td>PLU Capacity</td><td>{PLU_CAPACITY} items</td></tr>
                <tr><td>Departments</td><td>{DEPARTMENTS}</td></tr>
                <tr><td>Clerks</td><td>10</td></tr>
                <tr><td>Receipt Printer</td><td>2-station thermal (journal + receipt)</td></tr>
                <tr><td>Customer Display</td><td>POP-up display</td></tr>
                <tr><td>Operator Display</td><td>10-line LCD</td></tr>
                <tr><td>Connectivity</td><td>2 RS-232 ports, 1 drawer kick</td></tr>
                <tr><td>Dimensions</td><td>{DIMENSIONS}</td></tr>
                <tr><td>Weight</td><td>Approx. 18 lbs</td></tr>
                <tr><td>Power</td><td>120V AC</td></tr>
                <tr><td>Warranty</td><td>1 year manufacturer</td></tr>
            </table>
        </div>
        
        <div id="support" class="tab-content" style="display: none;">
            <div class="description-content">
                <h3>What&apos;s Included</h3>
                <ul>
                    <li>SAM4S {MODEL} Cash Register</li>
                    <li>Cash drawer with 4 bill / 5 coin compartments</li>
                    <li>Power cord</li>
                    <li>Operator manual</li>
                    <li>Programming keys</li>
                </ul>
                
                <h3>Optional Add-Ons</h3>
                <ul>
                    <li>External barcode scanner</li>
                    <li>Additional cash drawer</li>
                    <li>Extended warranty</li>
                    <li>On-site setup and training</li>
                </ul>
                
                <h3>Service &amp; Support</h3>
                <p>Performance Supply Depot provides:</p>
                <ul>
                    <li>Free phone support for programming questions</li>
                    <li>Repair services available</li>
                    <li>Ribbon and paper supplies in stock</li>
                    <li>Training available (in-person or remote)</li>
                </ul>
                
                <h3>Programming Services</h3>
                <p>Don&apos;t want to program it yourself? We offer complete menu programming services starting at $150. Send us your menu or product list, and we&apos;ll configure everything before shipping.</p>
            </div>
        </div>
    </section>
    
    <section class="footer-cta">
        <h3>Questions About the {MODEL}?</h3>
        <p>Our team has 20+ years of experience with SAM4S registers. Call for a free consultation.</p>
        <a href="tel:8888816834" class="phone">(888) 881-6834</a>
    </section>
    
    <footer class="footer">
        <p>&amp;copy; 2026 Performance Supply Depot LLC. Serving California since 2005.</p>
    </footer>
    
    <script>
        function showTab(tabName) {{
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.style.display = 'none';
            }});
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.getElementById(tabName).style.display = 'block';
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>'''

# ER-260 Data
er260_data = {
    'MODEL': 'ER-260',
    'MODEL_LOWER': 'er-260',
    'SKU': '30-210',
    'KEYBOARD_TYPE': 'Raised',
    'KEYBOARD_TYPE_DESC': 'raised',
    'KEYBOARD_BENEFIT': 'Tactile feedback with individual mechanical keys for fast, accurate entry',
    'PLU_CAPACITY': '2,000',
    'DEPARTMENTS': '20',
    'PRICE': '495.00',
    'DIMENSIONS': '16.5" W x 16.9" D x 13.4" H',
    'DESCRIPTION_TITLE': 'Entry-Level Professional Cash Management'
}

# ER-265 Data
er265_data = {
    'MODEL': 'ER-265',
    'MODEL_LOWER': 'er-265',
    'SKU': '30-211',
    'KEYBOARD_TYPE': 'Flat',
    'KEYBOARD_TYPE_DESC': 'flat',
    'KEYBOARD_BENEFIT': 'Easy to clean, ideal for food service environments with spill resistance',
    'PLU_CAPACITY': '2,000',
    'DEPARTMENTS': '20',
    'PRICE': '495.00',
    'DIMENSIONS': '16.5" W x 16.9" D x 13.4" H',
    'DESCRIPTION_TITLE': 'Entry-Level Professional Cash Management'
}

def generate_page(data):
    """Generate HTML page from template and data"""
    html = template
    for key, value in data.items():
        html = html.replace(f'{{{key}}}', value)
    return html

# Generate pages
pages = [
    ('/var/www/psdepot.com/products/sam4s-er-260.html', er260_data),
    ('/var/www/psdepot.com/products/sam4s-er-265.html', er265_data)
]

for filepath, data in pages:
    html = generate_page(data)
    with open(filepath, 'w') as f:
        f.write(html)
    print(f"Generated: {filepath}")

print("\nAll product pages created successfully!")
