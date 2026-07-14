#!/usr/bin/env python3
"""Generate SAM4S SAP-630 product page"""

template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAM4S SAP-630 Android POS Terminal | Performance Supply Depot LLC</title>
    <meta name="description" content="SAM4S SAP-630 Android touchscreen POS terminal. 10-inch display, raised programmable keyboard, cloud-ready. Professional-grade Android POS solution.">
    <link rel="canonical" href="https://psdepot.com/products/sam4s-sap-630.html">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    
    <style>
        :root {
            --primary: #1a365d;
            --primary-dark: #0f2744;
            --accent: #d69e2e;
            --accent-hover: #b7791f;
            --bg: #f7fafc;
            --card: #ffffff;
            --text: #2d3748;
            --text-muted: #718096;
            --border: #e2e8f0;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }
        
        .header {
            background: var(--primary);
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo { font-size: 1.5rem; font-weight: 700; }
        .logo span { color: var(--accent); }
        
        .header-nav a {
            color: white;
            text-decoration: none;
            margin-left: 2rem;
            opacity: 0.9;
            transition: opacity 0.2s;
        }
        .header-nav a:hover { opacity: 1; }
        
        .breadcrumb {
            max-width: 1200px;
            margin: 1rem auto;
            padding: 0 2rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        .breadcrumb a { color: var(--primary); text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }
        
        .product-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
        }
        
        @media (max-width: 768px) {
            .product-container { grid-template-columns: 1fr; gap: 2rem; padding: 1rem; }
        }
        
        .product-image-section {
            background: var(--card);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .product-image {
            width: 100%;
            height: auto;
            border-radius: 8px;
            display: block;
        }
        
        .image-gallery {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
            justify-content: center;
        }
        
        .gallery-thumb {
            width: 80px;
            height: 60px;
            object-fit: cover;
            border-radius: 4px;
            border: 2px solid transparent;
            cursor: pointer;
        }
        
        .gallery-thumb.active { border-color: var(--accent); }
        
        .image-caption {
            text-align: center;
            margin-top: 1rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        
        .product-info { display: flex; flex-direction: column; gap: 1.5rem; }
        
        .sku-badge {
            display: inline-block;
            background: #edf2f7;
            color: var(--text-muted);
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .product-title { font-size: 2rem; font-weight: 700; color: var(--primary); line-height: 1.2; }
        .product-subtitle { font-size: 1.125rem; color: var(--text-muted); }
        
        .price-section {
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .price { font-size: 2.5rem; font-weight: 700; color: var(--primary); }
        .price-note { font-size: 0.875rem; color: var(--text-muted); margin-top: 0.25rem; }
        
        .stock-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 1rem;
            color: #38a169;
            font-weight: 500;
        }
        
        .stock-dot {
            width: 8px;
            height: 8px;
            background: #38a169;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .cta-buttons { display: flex; gap: 1rem; margin-top: 1.5rem; }
        
        .btn-primary {
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
        }
        .btn-primary:hover { background: var(--accent-hover); transform: translateY(-1px); }
        
        .btn-secondary {
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
        }
        .btn-secondary:hover { border-color: var(--primary); background: rgba(26, 54, 93, 0.05); }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-top: 1rem;
        }
        
        @media (max-width: 768px) { .features-grid { grid-template-columns: 1fr; } }
        
        .feature-item {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding: 0.75rem;
            background: #f7fafc;
            border-radius: 8px;
        }
        
        .feature-icon {
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
        }
        
        .feature-text { font-size: 0.9rem; }
        
        .tabs-section { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid var(--border);
            margin-bottom: 1.5rem;
        }
        
        .tab {
            padding: 1rem 2rem;
            background: none;
            border: none;
            font-size: 1rem;
            font-weight: 500;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.2s;
        }
        .tab.active { color: var(--primary); border-bottom-color: var(--accent); }
        
        .tab-content {
            background: var(--card);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .specs-table {
            width: 100%;
            border-collapse: collapse;
        }
        .specs-table tr { border-bottom: 1px solid var(--border); }
        .specs-table tr:last-child { border-bottom: none; }
        .specs-table td { padding: 1rem; }
        .specs-table td:first-child { font-weight: 600; color: var(--text-muted); width: 40%; }
        
        .description-content { line-height: 1.8; }
        .description-content h3 { color: var(--primary); margin: 1.5rem 0 0.75rem; font-size: 1.25rem; }
        .description-content p { margin-bottom: 1rem; }
        .description-content ul { margin-left: 1.5rem; margin-bottom: 1rem; }
        .description-content li { margin-bottom: 0.5rem; }
        
        .footer-cta {
            max-width: 1200px;
            margin: 3rem auto;
            padding: 2rem;
            background: var(--primary);
            color: white;
            border-radius: 12px;
            text-align: center;
        }
        .footer-cta h3 { font-size: 1.5rem; margin-bottom: 0.5rem; }
        .footer-cta p { opacity: 0.9; margin-bottom: 1.5rem; }
        .footer-cta .phone { font-size: 1.75rem; font-weight: 700; color: var(--accent); text-decoration: none; }
        
        .footer {
            background: var(--primary-dark);
            color: white;
            padding: 2rem;
            text-align: center;
            font-size: 0.875rem;
            opacity: 0.8;
        }
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
        <a href="/">Home</a> / <a href="/#hardware">POS Hardware</a> / SAM4S SAP-630
    </div>
    
    <main class="product-container">
        <div class="product-image-section">
            <img src="/assets/images/sam4s-sap-630.jpg" alt="SAM4S SAP-630 Android POS Terminal with 10-inch touchscreen and raised programmable keyboard" class="product-image">
            <p class="image-caption">SAM4S SAP-630 — Android POS Terminal with 10" Touchscreen Display</p>
        </div>
        
        <div class="product-info">
            <div>
                <span class="sku-badge">SKU: 30-214</span>
                <h1 class="product-title">SAM4S SAP-630 Android POS Terminal</h1>
                <p class="product-subtitle">10" Touchscreen • Android OS • Raised Programmable Keyboard</p>
            </div>
            
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">Android 7.1 operating system</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">10-inch capacitive touchscreen</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">Raised programmable keyboard</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">Cloud-ready with WiFi/Ethernet</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">Built-in receipt printer</span>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">App ecosystem support</span>
                </div>
            </div>
            
            <div class="price-section">
                <div class="price">$1,395.00</div>
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
                <h3>Android-Powered Modern POS</h3>
                <p>The SAM4S SAP-630 combines the reliability of traditional POS hardware with the flexibility of Android. This hybrid terminal features a bright 10-inch touchscreen running Android 7.1, paired with a raised programmable keyboard for the best of both worlds — touch-based efficiency plus tactile key feedback for high-volume transactions.</p>
                
                <h3>Key Features</h3>
                <ul>
                    <li><strong>Android 7.1 OS:</strong> Access to Google Play Store apps, cloud connectivity, and modern software</li>
                    <li><strong>10" Capacitive Touchscreen:</strong> Responsive multi-touch display with adjustable angle</li>
                    <li><strong>Raised Programmable Keyboard:</strong> Color-coded keys for quick item entry with tactile feedback</li>
                    <li><strong>Cloud-Ready:</strong> Built-in WiFi and Ethernet for real-time data sync</li>
                    <li><strong>Integrated Receipt Printer:</strong> High-speed thermal printer with auto-cutter</li>
                    <li><strong>Multiple Payment Support:</strong> EMV, NFC/contactless, mobile wallet ready</li>
                </ul>
                
                <h3>Ideal For</h3>
                <ul>
                    <li>Restaurants needing cloud-based reporting</li>
                    <li>Retail stores wanting app integration</li>
                    <li>Businesses upgrading from traditional registers</li>
                    <li>Multi-location operations requiring centralized data</li>
                    <li>Anyone wanting modern POS without monthly SaaS fees</li>
                </ul>
                
                <h3>Why Choose the SAP-630?</h3>
                <p>Unlike tablet-based POS systems that require separate peripherals, the SAP-630 is an all-in-one solution. The Android OS means you're not locked into proprietary software — install the apps you need. Yet the built-in keyboard and receipt printer give you the speed and reliability of dedicated POS hardware. It's the bridge between traditional registers and modern cloud POS.</p>
            </div>
        </div>
        
        <div id="specs" class="tab-content" style="display: none;">
            <table class="specs-table">
                <tr><td>Model</td><td>SAM4S SAP-630</td></tr>
                <tr><td>Operating System</td><td>Android 7.1 (upgradeable)</td></tr>
                <tr><td>Display</td><td>10.1" capacitive touchscreen (1280x800)</td></tr>
                <tr><td>Processor</td><td>Quad-core 1.8GHz</td></tr>
                <tr><td>Memory</td><td>2GB RAM / 8GB storage</td></tr>
                <tr><td>Keyboard</td><td>Raised programmable (66 keys)</td></tr>
                <tr><td>Receipt Printer</td><td>Thermal, 250mm/sec, auto-cutter</td></tr>
                <tr><td>Customer Display</td><td>Adjustable 7" LCD or secondary touchscreen</td></tr>
                <tr><td>Connectivity</td><td>WiFi 802.11ac, Ethernet, 4x USB, 2x RS-232</td></tr>
                <tr><td>Power</td><td>120V AC, 60W</td></tr>
                <tr><td>Dimensions</td><td>15.7" W x 15.4" D x 16.5" H (with display)</td></tr>
                <tr><td>Weight</td><td>Approx. 24 lbs</td></tr>
                <tr><td>Warranty</td><td>1 year manufacturer</td></tr>
            </table>
        </div>
        
        <div id="support" class="tab-content" style="display: none;">
            <div class="description-content">
                <h3>What's Included</h3>
                <ul>
                    <li>SAM4S SAP-630 Android POS Terminal</li>
                    <li>Large cash drawer with locking lid</li>
                    <li>Power adapter and cord</li>
                    <li>Setup guide and quick start manual</li>
                    <li>Programming keys</li>
                </ul>
                
                <h3>Software Options</h3>
                <p>The SAP-630 runs Android, giving you flexibility to choose your POS software:</p>
                <ul>
                    <li>SAM4S native POS apps</li>
                    <li>Third-party Android POS solutions</li>
                    <li>Custom app development</li>
                    <li>Cloud synchronization tools</li>
                </ul>
                
                <h3>Optional Add-Ons</h3>
                <ul>
                    <li>Barcode scanner (USB or Bluetooth)</li>
                    <li>Kitchen printer (impact or thermal)</li>
                    <li>Secondary customer-facing display</li>
                    <li>Extended warranty (2 or 3 years)</li>
                    <li>Professional setup and training</li>
                </ul>
                
                <h3>Service & Support</h3>
                <p>Performance Supply Depot provides:</p>
                <ul>
                    <li>Pre-configured software installation</li>
                    <li>Free phone support</li>
                    <li>Remote troubleshooting</li>
                    <li>Repair services and spare parts</li>
                    <li>Software migration assistance</li>
                </ul>
            </div>
        </div>
    </section>
    
    <section class="footer-cta">
        <h3>Questions About the SAP-630?</h3>
        <p>Our team can help you choose the right Android POS setup. Call for a free consultation.</p>
        <a href="tel:8888816834" class="phone">(888) 881-6834</a>
    </section>
    
    <footer class="footer">
        <p>&copy; 2026 Performance Supply Depot LLC. Serving California since 2005.</p>
    </footer>
    
    <script>
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(content => {
                content.style.display = 'none';
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.getElementById(tabName).style.display = 'block';
            event.target.classList.add('active');
        }
    </script>
</body>
</html>'''

with open('/var/www/psdepot.com/products/sam4s-sap-630.html', 'w') as f:
    f.write(template)

print("Generated: /var/www/psdepot.com/products/sam4s-sap-630.html")
