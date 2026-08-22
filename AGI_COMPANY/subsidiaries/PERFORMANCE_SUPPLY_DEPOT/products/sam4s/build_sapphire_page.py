#!/usr/bin/env python3
"""Generate the SAM4s Sapphire Android POS Terminal page in /products/mscashdrawer/,
based on the existing SAP-630-FT template."""
import shutil, re

SRC = "/var/www/psdepot.com/products/mscashdrawer/sam4s-sap-630-ft-flat-keyboard-android-terminal.html"
DST = "/var/www/psdepot.com/products/mscashdrawer/sam4s-sapphire-android-pos-terminal.html"

html = open(SRC).read()

# --- Simple string swaps ---
repl = [
    ("SAM4s SAP-630-FT Flat Keyboard Android Terminal | Performance Supply Depot LLC",
     "SAM4s Sapphire Android POS Terminal | Performance Supply Depot LLC"),
    ('Sam4s SAP-630-FT flat keyboard Android based Terminal. Needs software. CRS Dealer line required.',
     "SAM4s Sapphire Android POS terminal — 15\" Android 9 touchscreen, runs SAM4POS. CRS dealer line."),
    ("https://psdepot.com/products/mscashdrawer/sam4s-sap-630-ft-flat-keyboard-android-terminal.html",
     "https://psdepot.com/products/mscashdrawer/sam4s-sapphire-android-pos-terminal.html"),
    ('src="/images/mscashdrawer/sam4s-sap-630-ft-flat-keyboard-android-terminal.png" alt="SAM4s SAP-630-FT Flat Keyboard Android Terminal"',
     'src="/images/mscashdrawer/sam4s-sapphire-android-pos-terminal.webp" alt="SAM4s Sapphire Android POS Terminal"'),
    ("SKU: PSD-CRS-SAP-630-FT | MPN: CRS-SAP-630-FT",
     "SKU: PSD-CRS-SAPPHIRE-ANDROID | MPN: CRS-SAPPHIRE-ANDROID"),
    ("<h1 class=\"product-title\">SAM4s SAP-630-FT Flat Keyboard Android Terminal</h1>",
     "<h1 class=\"product-title\">SAM4s Sapphire Android POS Terminal</h1>"),
    ("SAM4s SAP-630-FT Flat Keyboard Android Terminal",
     "SAM4s Sapphire Android POS Terminal"),
    ("const sku = 'PSD-CRS-SAP-630-FT';",
     "const sku = 'PSD-CRS-SAPPHIRE-ANDROID';"),
    ("const name = 'SAM4s SAP-630-FT Flat Keyboard Android Terminal';",
     "const name = 'SAM4s Sapphire Android POS Terminal';"),
    ("const price = 1331.67;",
     "const price = 0;"),
]

for old, new in repl:
    html = html.replace(old, new)

# --- Features grid (replace 4 items) ---
old_features = re.search(
    r'<div class="features-grid">.*?</div>\s*</div>\s*<div class="price-section">',
    html, re.S
)
new_features = '''<div class="features-grid">

                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">Android 9</span>
                </div>

                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">15" touchscreen</span>
                </div>

                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">Runs SAM4POS</span>
                </div>

                <div class="feature-item">
                    <div class="feature-icon">✓</div>
                    <span class="feature-text">Wi-Fi + Bluetooth 5.0</span>
                </div>
            </div>
            
            <div class="price-section">'''
if old_features:
    html = html.replace(old_features.group(0), new_features)

# --- Price section ---
html = html.replace(
    '<div class="price">$1331.67</div>\n                <div class="price-note">MSRP: $1665.00 — You save $333.33</div>',
    '<div class="price">Call for Pricing</div>\n                <div class="price-note">Pricing available on request</div>'
)
html = html.replace('Out of Stock', 'Call for availability')

# --- Specs table ---
old_specs = re.search(r'<table class="specs-table">.*?</table>', html, re.S)
new_specs = '''<table class="specs-table">
                <tr><td>OS</td><td>Android 9</td></tr>
                <tr><td>CPU</td><td>ARM Cortex-A72 1.8GHz + A53 1.4GHz</td></tr>
                <tr><td>RAM / Storage</td><td>4GB LPDDR4 / 64GB eMMC</td></tr>
                <tr><td>Display</td><td>15" (1024x768) / 15.6" (1366x768) / FHD option</td></tr>
                <tr><td>Touch</td><td>10-point PCAP</td></tr>
                <tr><td>Interfaces</td><td>3x Serial, 6x USB, GbE, Wi-Fi ac, BT 5.0, DP</td></tr>
                <tr><td>Drawer</td><td>1 port / 2CH (12V/24V)</td></tr>
                <tr><td>Software</td><td>SAM4POS (Android)</td></tr>
                <tr><td>Options</td><td>MSR 1/2/3, rear display, VESA mount</td></tr>
                <tr><td>Warranty</td><td>1 year</td></tr>
            </table>'''
if old_specs:
    html = html.replace(old_specs.group(0), new_specs)

# --- Description overview paragraph ---
html = html.replace(
    "<p>Sam4s SAP-630-FT flat keyboard Android based Terminal. Needs software. CRS Dealer line required.</p>",
    "<p>The SAM4s Sapphire Android is a 15\" Android 9 POS terminal with a 10-point capacitive touchscreen and the full SAM4POS software suite. One application configurable for food, beverage, and retail — remotely manageable via TeamViewer, no site visit required.</p>"
)

# --- Key features list (description tab) ---
html = html.replace(
    """<li>Android based</li>
                    <li>Flat keyboard</li>
                    <li>Touchscreen</li>
                    <li>Modern POS</li>""",
    """<li>Android 9 (ARM big.LITTLE)</li>
                    <li>15" / 15.6" touchscreen (10-point PCAP)</li>
                    <li>Runs SAM4POS — one software for every business type</li>
                    <li>Wi-Fi ac + Bluetooth 5.0 + Ethernet</li>"""
)

# --- What's included (support tab) ---
html = html.replace(
    "SAM4s SAP-630-FT Flat Keyboard Android Terminal",
    "SAM4s Sapphire Android POS Terminal"
)

open(DST, "w").write(html)
print(f"✅ wrote {DST}")
print(f"   size: {len(html)} bytes")
