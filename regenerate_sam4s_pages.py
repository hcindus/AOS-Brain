#!/usr/bin/env python3
"""
Regenerate SAM4S ER-260 and ER-265 with full polish + checkout functionality
"""

# Full polished template with cart integration
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
        
        /* Header */
        .header {
            background: var(--primary);
            color: white;
            padding: 1rem 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
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
        
        /* Cart Icon */
        .cart-icon {
            position: relative;
            cursor: pointer;
            padding: 0.5rem;
        }
        
        .cart-count {
            position: absolute;
            top: -5px;
            right: -5px;
            background: var(--accent);
            color: white;
            font-size: 0.75rem;
            font-weight: 700;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Breadcrumb */
        .breadcrumb {
            max-width: 1200px;
            margin: 1rem auto;
            padding: 0 2rem;
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        
        .breadcrumb a {
            color: var(--primary);
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .breadcrumb a:hover { text-decoration: underline; }
        
        /* Product Container */
        .product-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
        }
        
        @media (max-width: 768px) {
            .product-container {
                grid-template-columns: 1fr;
                gap: 2rem;
                padding: 1rem;
            }
        }
        
        /* Image Section */
        .product-image-section {
            background: var(--card);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            position: sticky;
            top: 80px;
            height: fit-content;
        }
        
        .product-image {
            width: 100%;
            height: auto;
            border-radius: 8px;
            display: block;
            transition: transform 0.3s ease;
        }
        
        .product-image:hover { transform: scale(1.02); }
        
        .image-caption {
            text-align: center;
            margin-top: 1rem;
            font-size: 0.875rem;
            color: var(--text-muted);
            font-style: italic;
        }
        
        /* Info Section */
        .product-info { display: flex; flex-direction: column; gap: 1.5rem; }
        
        .sku-badge {
            display: inline-block;
            background: linear-gradient(135deg, #edf2f7 0%, #e2e8f0 100%);
            color: var(--text-muted);
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            width: fit-content;
        }
        
        .product-title {
            font-size: 2.25rem;
            font-weight: 700;
            color: var(--primary);
            line-height: 1.2;
            letter-spacing: -0.02em;
        }
        
        .product-subtitle {
            font-size: 1.125rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .product-subtitle span {
            background: #f7fafc;
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.875rem;
        }
        
        /* Price Section */
        .price-section {
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid var(--border);
        }
        
        .price-row {
            display: flex;
            align-items: baseline;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }
        
        .price {
            font-size: 2.75rem;
            font-weight: 700;
            color: var(--primary);
            line-height: 1;
        }
        
        .price-original {
            font-size: 1.5rem;
            color: var(--text-muted);
            text-decoration: line-through;
            opacity: 0.7;
        }
        
        .price-note {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .stock-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 1rem;
            padding: 0.75rem 1rem;
            background: #f0fff4;
            border-radius: 8px;
            color: #38a169;
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        .stock-dot {
            width: 10px;
            height: 10px;
            background: #38a169;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.1); }
        }
        
        /* Quantity Selector */
        .quantity-selector {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin: 1.5rem 0;
            padding: 1rem;
            background: #f7fafc;
            border-radius: 8px;
        }
        
        .quantity-label { font-weight: 500; color: var(--text); }
        
        .quantity-controls {
            display: flex;
            align-items: center;
            border: 1px solid var(--border);
            border-radius: 6px;
            overflow: hidden;
        }
        
        .quantity-btn {
            width: 36px;
            height: 36px;
            border: none;
            background: white;
            cursor: pointer;
            font-size: 1.25rem;
            color: var(--text);
            transition: background 0.2s;
        }
        
        .quantity-btn:hover { background: #edf2f7; }
        
        .quantity-input {
            width: 50px;
            height: 36px;
            border: none;
            text-align: center;
            font-size: 1rem;
            font-weight: 600;
        }
        
        /* CTA Buttons */
        .cta-buttons {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .btn-primary {
            flex: 1;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 6px rgba(214, 158, 46, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(214, 158, 46, 0.4);
        }
        
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
        
        .btn-secondary:hover {
            border-color: var(--primary);
            background: rgba(26, 54, 93, 0.05);
        }
        
        /* Features Grid */
        .features-section {
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .features-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
        }
        
        @media (max-width: 768px) { .features-grid { grid-template-columns: 1fr; } }
        
        .feature-item {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding: 0.75rem;
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        
        .feature-icon {
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.75rem;
            flex-shrink: 0;
        }
        
        .feature-text { font-size: 0.9rem; color: var(--text); }
        
        /* Tabs */
        .tabs-section {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .tabs {
            display: flex;
            border-bottom: 2px solid var(--border);
            margin-bottom: 1.5rem;
            gap: 0.5rem;
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
            border-radius: 4px 4px 0 0;
        }
        
        .tab:hover { background: rgba(26, 54, 93, 0.05); }
        
        .tab.active {
            color: var(--primary);
            border-bottom-color: var(--accent);
            background: rgba(214, 158, 46, 0.1);
        }
        
        .tab-content {
            background: var(--card);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        /* Specs Table */
        .specs-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }
        
        .specs-table tr {
            border-bottom: 1px solid var(--border);
            transition: background 0.2s;
        }
        
        .specs-table tr:hover { background: #f7fafc; }
        
        .specs-table tr:last-child { border-bottom: none; }
        
        .specs-table td {
            padding: 1rem 1.25rem;
        }
        
        .specs-table td:first-child {
            font-weight: 600;
            color: var(--primary);
            width: 40%;
            background: #f7fafc;
        }
        
        /* Description Content */
        .description-content { line-height: 1.8; }
        
        .description-content h3 {
            color: var(--primary);
            margin: 1.5rem 0 0.75rem;
            font-size: 1.35rem;
            font-weight: 600;
        }
        
        .description-content p {
            margin-bottom: 1rem;
            color: var(--text);
        }
        
        .description-content ul {
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .description-content li {
            margin-bottom: 0.75rem;
            position: relative;
            padding-left: 0.5rem;
        }
        
        .description-content li::marker { color: var(--accent); }
        
        /* Related Products */
        .related-section {
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 2rem;
        }
        
        .related-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 1.5rem;
        }
        
        .related-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }
        
        @media (max-width: 768px) { .related-grid { grid-template-columns: 1fr; } }
        
        .related-card {
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s, box-shadow 0.2s;
            border: 1px solid var(--border);
        }
        
        .related-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        }
        
        .related-sku {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .related-name {
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }
        
        .related-price {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--accent);
        }
        
        /* Footer CTA */
        .footer-cta {
            max-width: 1200px;
            margin: 3rem auto;
            padding: 2.5rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            border-radius: 12px;
            text-align: center;
        }
        
        .footer-cta h3 {
            font-size: 1.75rem;
            margin-bottom: 0.75rem;
            font-weight: 700;
        }
        
        .footer-cta p {
            opacity: 0.9;
            margin-bottom: 1.5rem;
            font-size: 1.1rem;
        }
        
        .footer-cta .phone {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .footer-cta .phone:hover { color: #e6b84d; }
        
        /* Footer */
        .footer {
            background: var(--primary-dark);
            color: white;
            padding: 2rem;
            text-align: center;
            font-size: 0.875rem;
            opacity: 0.8;
        }
        
        /* Cart Sidebar */
        .cart-sidebar {
            position: fixed;
            top: 0;
            right: -400px;
            width: 400px;
            height: 100vh;
            background: white;
            box-shadow: -4px 0 20px rgba(0,0,0,0.15);
            z-index: 1000;
            transition: right 0.3s ease;
            display: flex;
            flex-direction: column;
        }
        
        .cart-sidebar.open { right: 0; }
        
        .cart-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .cart-title { font-size: 1.25rem; font-weight: 600; }
        
        .cart-close {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-muted);
        }
        
        .cart-items {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }
        
        .cart-item {
            display: flex;
            gap: 1rem;
            padding: 1rem;
            border-bottom: 1px solid var(--border);
        }
        
        .cart-item-info { flex: 1; }
        
        .cart-item-name { font-weight: 600; margin-bottom: 0.25rem; }
        
        .cart-item-price { color: var(--accent); font-weight: 600; }
        
        .cart-footer {
            padding: 1.5rem;
            border-top: 1px solid var(--border);
            background: #f7fafc;
        }
        
        .cart-total {
            display: flex;
            justify-content: space-between;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        .cart-checkout {
            width: 100%;
            padding: 1rem;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
        }
        
        .cart-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 999;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
        }
        
        .cart-overlay.open {
            opacity: 1;
            visibility: visible;
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
                <div class="cart-icon" onclick="toggleCart()">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="9" cy="21" r="1"></circle>
                        <circle cx="20" cy="21" r="1"></circle>
                        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                    </svg>
                    <span class="cart-count" id="cartCount">0</span>
                </div>
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
                <p class="product-subtitle">
                    <span>{KEYBOARD_TYPE} Keyboard</span>
                    <span>{PLU_CAPACITY} PLUs</span>
                    <span>{DEPARTMENTS} Departments</span>
                </p>
            </div>
            
            <div class="features-section">
                <div class="features-title">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" style="vertical-align: middle;">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                    Key Features
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
            </div>
            
            <div class="price-section">
                <div class="price-row">
                    <div class="price">${PRICE}</div>
                </div>
                <div class="price-note">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle;">
                        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                    </svg>
                    Free shipping within California
                </div>
                <div class="stock-status">
                    <span class="stock-dot"></span>
                    In Stock — Ships within 24 hours
                </div>
                
                <div class="quantity-selector">
                    <span class="quantity-label">Quantity:</span>
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="updateQuantity(-1)">−</button>
                        <input type="number" class="quantity-input" id="quantity" value="1" min="1" max="10" readonly>
                        <button class="quantity-btn" onclick="updateQuantity(1)">+</button>
                    </div>
                </div>
                
                <div class="cta-buttons">
                    <button class="btn-primary" onclick="addToCart()">Add to Cart</button>
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
                <h3>What's Included</h3>
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
                
                <h3>Service & Support</h3>
                <p>Performance Supply Depot provides:</p>
                <ul>
                    <li>Free phone support for programming questions</li>
                    <li>Repair services available</li>
                    <li>Ribbon and paper supplies in stock</li>
                    <li>Training available (in-person or remote)</li>
                </ul>
                
                <h3>Programming Services</h3>
                <p>Don't want to program it yourself? We offer complete menu programming services starting at $150. Send us your menu or product list, and we'll configure everything before shipping.</p>
            </div>
        </div>
    </section>
    
    <section class="related-section">
        <h2 class="related-title">You May Also Like</h2>
        <div class="related-grid">
            {RELATED_CARDS}
        </div>
    </section>
    
    <section class="footer-cta">
        <h3>Questions About the {MODEL}?</h3>
        <p>Our team has 20+ years of experience with SAM4S registers. Call for a free consultation.</p>
        <a href="tel:8888816834" class="phone">(888) 881-6834</a>
    </section>
    
    <footer class="footer">
        <p>&copy; 2026 Performance Supply Depot LLC. Serving California since 2005.</p>
    </footer>
    
    <!-- Cart Sidebar -->
    <div class="cart-overlay" id="cartOverlay" onclick="toggleCart()"></div>
    <div class="cart-sidebar" id="cartSidebar">
        <div class="cart-header">
            <div class="cart-title">Shopping Cart</div>
            <button class="cart-close" onclick="toggleCart()">×</button>
        </div>
        <div class="cart-items" id="cartItems">
            <p style="text-align: center; color: var(--text-muted); padding: 2rem;">Your cart is empty</p>
        </div>
        <div class="cart-footer">
            <div class="cart-total">
                <span>Total</span>
                <span id="cartTotal">$0.00</span>
            </div>
            <button class="cart-checkout" onclick="goToCheckout()">Proceed to Checkout</button>
        </div>
    </div>
    
    <script>
        // Product data
        const product = {
            sku: '{SKU}',
            name: 'SAM4S {MODEL} Cash Register',
            price: {PRICE_RAW},
            image: '/assets/images/sam4s-{MODEL_LOWER}.jpg'
        };
        
        // Cart from localStorage
        let cart = JSON.parse(localStorage.getItem('psd_cart') || '[]');
        updateCartUI();
        
        function updateQuantity(change) {
            const input = document.getElementById('quantity');
            let value = parseInt(input.value) + change;
            if (value < 1) value = 1;
            if (value > 10) value = 10;
            input.value = value;
        }
        
        function addToCart() {
            const quantity = parseInt(document.getElementById('quantity').value);
            
            // Check if item already in cart
            const existingItem = cart.find(item => item.sku === product.sku);
            if (existingItem) {
                existingItem.quantity += quantity;
            } else {
                cart.push({
                    ...product,
                    quantity: quantity
                });
            }
            
            // Save to localStorage
            localStorage.setItem('psd_cart', JSON.stringify(cart));
            
            // Update UI
            updateCartUI();
            
            // Open cart sidebar
            toggleCart();
        }
        
        function updateCartUI() {
            const cartCount = document.getElementById('cartCount');
            const cartItems = document.getElementById('cartItems');
            const cartTotal = document.getElementById('cartTotal');
            
            const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
            const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            
            cartCount.textContent = totalItems;
            cartTotal.textContent = '$' + totalPrice.toFixed(2);
            
            if (cart.length === 0) {
                cartItems.innerHTML = '<p style="text-align: center; color: var(--text-muted); padding: 2rem;">Your cart is empty</p>';
            } else {
                cartItems.innerHTML = cart.map(item => `
                    <div class="cart-item">
                        <div class="cart-item-info">
                            <div class="cart-item-name">${item.name}</div>
                            <div class="cart-item-price">$${item.price.toFixed(2)} x ${item.quantity}</div>
                        </div>
                        <button onclick="removeFromCart('${item.sku}')" style="background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 1.25rem;">×</button>
                    </div>
                `).join('');
            }
        }
        
        function removeFromCart(sku) {
            cart = cart.filter(item => item.sku !== sku);
            localStorage.setItem('psd_cart', JSON.stringify(cart));
            updateCartUI();
        }
        
        function toggleCart() {
            document.getElementById('cartSidebar').classList.toggle('open');
            document.getElementById('cartOverlay').classList.toggle('open');
        }
        
        function goToCheckout() {
            if (cart.length === 0) {
                alert('Your cart is empty!');
                return;
            }
            // Save cart and redirect to checkout
            localStorage.setItem('psd_cart_checkout', JSON.stringify(cart));
            window.location.href = '/checkout.html';
        }
        
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

def get_related_cards(exclude_model):
    """Generate related product cards, excluding the current model"""
    products = [
        {'sku': '30-210', 'name': 'SAM4S ER-260 Cash Register (Raised Keyboard)', 'price': 495.00, 'model': 'er-260'},
        {'sku': '30-211', 'name': 'SAM4S ER-265 Cash Register (Flat Keyboard)', 'price': 495.00, 'model': 'er-265'},
        {'sku': '30-212', 'name': 'SAM4S ER-940 Cash Register (Flat Keyboard)', 'price': 895.00, 'model': 'er-940'},
        {'sku': '30-214', 'name': 'SAM4S SAP-630 POS Terminal (Raised Keyboard)', 'price': 1395.00, 'model': 'sap-630'},
    ]
    
    related = [p for p in products if p['model'] != exclude_model][:3]
    
    cards = []
    for p in related:
        cards.append(f'''<a href="/products/sam4s-{p['model']}.html" class="related-card">
            <div class="related-sku">SKU: {p['sku']}</div>
            <div class="related-name">{p['name']}</div>
            <div class="related-price">${p['price']:,.2f}</div>
        </a>''')
    
    return '\n            '.join(cards)

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
    'PRICE_RAW': '495.00',
    'DIMENSIONS': '16.5" W x 16.9" D x 13.4" H',
    'DESCRIPTION_TITLE': 'Entry-Level Professional Cash Management',
    'RELATED_CARDS': get_related_cards('er-260')
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
    'PRICE_RAW': '495.00',
    'DIMENSIONS': '16.5" W x 16.9" D x 13.4" H',
    'DESCRIPTION_TITLE': 'Entry-Level Professional Cash Management',
    'RELATED_CARDS': get_related_cards('er-265')
}

def generate_page(data):
    """Generate HTML page from template and data"""
    html = template
    for key, value in data.items():
        html = html.replace(f'{{{key}}}', str(value))
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

print("\nAll SAM4S product pages upgraded with:")
print("  ✓ Full polished styling matching ER-940/SAP-630")
print("  ✓ Working 'Add to Cart' with quantity selector")
print("  ✓ Cart sidebar with item management")
print("  ✓ Checkout flow (saves cart, redirects to checkout.html)")
print("  ✓ 'You May Also Like' cross-sell section")
print("  ✓ Persistent cart using localStorage")
