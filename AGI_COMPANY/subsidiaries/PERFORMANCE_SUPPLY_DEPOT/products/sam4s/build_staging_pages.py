#!/usr/bin/env python3
"""Generate staged (no-index) SAM4S product pages on psdepot.com.

Output: /var/www/psdepot.com/staging/sam4s/*.html + index.html
Pricing/SKU are placeholders (Call for Pricing) until Captain provides real numbers.
"""
import os, json, datetime

OUT = "/var/www/psdepot.com/staging/sam4s"
os.makedirs(OUT, exist_ok=True)

TODAY = datetime.date.today().isoformat()
PHONE = "(888) 881-6834"

# ---------------------------------------------------------------------------
# Shared CSS (mirrors existing product pages)
# ---------------------------------------------------------------------------
CSS = """
        :root { --primary:#0A1A2F; --primary-dark:#070f1a; --accent:#FF7A00; --accent-hover:#e56d00;
                --secondary:#00E0FF; --success:#28a745; --bg:#F8F9FA; --card:#fff; --text:#111;
                --text-muted:#718096; --border:#e2e8f0; }
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:var(--bg); color:var(--text); line-height:1.6; }
        .header { background:var(--primary); color:#fff; padding:1rem 2rem; box-shadow:0 2px 4px rgba(0,0,0,.1); position:sticky; top:0; z-index:100; }
        .header-content { max-width:1200px; margin:0 auto; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }
        .logo { font-size:1.5rem; font-weight:700; text-decoration:none; color:#fff; }
        .logo span { color:var(--accent); }
        .contact-info { display:flex; align-items:center; gap:1.25rem; flex-wrap:wrap; }
        .contact-info a { color:#fff; text-decoration:none; font-size:.95rem; }
        .cart-icon { background:#c53030; color:#fff!important; padding:.5rem 1rem; border-radius:20px; font-weight:600; }
        .main-nav { background:#12283f; border-bottom:3px solid var(--accent); }
        .main-nav .container { display:flex; gap:4px; flex-wrap:wrap; max-width:1200px; margin:0 auto; padding:0 24px; }
        .main-nav a { display:inline-block; color:#bee3f8; text-decoration:none; font-weight:600; font-size:15px; padding:12px 18px; border-bottom:2px solid transparent; }
        .main-nav a:hover { color:#fff; background:rgba(255,255,255,.08); border-bottom-color:var(--accent); }
        .breadcrumb { max-width:1200px; margin:1rem auto; padding:0 2rem; font-size:.875rem; color:var(--text-muted); }
        .breadcrumb a { color:var(--primary); text-decoration:none; }
        .product-container { max-width:1200px; margin:0 auto; padding:2rem; display:grid; grid-template-columns:1fr 1fr; gap:3rem; }
        .product-info { display:flex; flex-direction:column; gap:1.5rem; }
        .sku-badge { display:inline-block; background:#edf2f7; color:var(--text-muted); padding:.35rem .85rem; border-radius:20px; font-size:.75rem; font-weight:600; text-transform:uppercase; letter-spacing:.05em; width:fit-content; }
        .product-title { font-size:2rem; font-weight:700; color:var(--primary); line-height:1.2; }
        .product-brand { font-size:1rem; color:var(--text-muted); }
        .price-section { background:var(--card); border-radius:12px; padding:1.5rem; box-shadow:0 4px 12px rgba(0,0,0,.08); border:1px solid var(--border); }
        .price-row { display:flex; align-items:baseline; gap:1rem; flex-wrap:wrap; margin-bottom:.5rem; }
        .price-current { font-size:2.2rem; font-weight:700; color:var(--accent); }
        .price-note { color:var(--text-muted); font-size:.9rem; }
        .condition-badge { display:inline-block; background:#edf2f7; border:1px solid var(--border); color:var(--text); padding:.3rem .7rem; border-radius:6px; font-size:.85rem; font-weight:600; }
        .stock-status { color:var(--success); font-weight:500; margin:.5rem 0; }
        .btn-call { display:inline-flex; align-items:center; gap:.5rem; background:var(--primary); color:#fff; border:none; padding:.85rem 1.75rem; border-radius:8px; font-size:1.05rem; font-weight:600; text-decoration:none; cursor:pointer; }
        .btn-call:hover { background:var(--primary-dark); }
        .btn-quote { display:inline-flex; align-items:center; gap:.5rem; background:var(--accent); color:#fff; border:none; padding:.85rem 1.75rem; border-radius:8px; font-size:1.05rem; font-weight:600; text-decoration:none; }
        .btn-quote:hover { background:var(--accent-hover); }
        .vendor-info { background:var(--bg); padding:1.5rem; border-radius:8px; }
        .vendor-info h4 { color:var(--primary); margin-bottom:.5rem; }
        .vendor-info p { color:var(--text-muted); font-size:.875rem; }
        .product-details { max-width:1200px; margin:0 auto; padding:2rem; background:var(--card); border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,.08); }
        .details-section { margin-bottom:2rem; }
        .details-title { font-size:1.25rem; font-weight:700; color:var(--primary); margin-bottom:1rem; padding-bottom:.5rem; border-bottom:2px solid var(--border); }
        .features-list { list-style:none; }
        .features-list li { padding:.75rem 0; padding-left:1.75rem; position:relative; border-bottom:1px solid var(--border); }
        .features-list li::before { content:"✓"; position:absolute; left:0; color:var(--success); font-weight:bold; }
        .specs-table { width:100%; border-collapse:collapse; }
        .specs-table tr:nth-child(even) { background:var(--bg); }
        .specs-table th, .specs-table td { padding:.75rem 1rem; text-align:left; border-bottom:1px solid var(--border); }
        .specs-table th { width:38%; font-weight:600; color:var(--primary); }
        .compat-tags { display:flex; flex-wrap:wrap; gap:.5rem; }
        .compat-tag { background:var(--bg); padding:.35rem .75rem; border-radius:15px; font-size:.875rem; border:1px solid var(--border); }
        .footer-cta { max-width:1200px; margin:3rem auto; padding:2rem; background:var(--primary); color:#fff; border-radius:12px; text-align:center; }
        .footer-cta a.phone { font-size:2rem; font-weight:800; color:#ff7a00; text-decoration:none; }
        .footer { background:var(--primary-dark); color:#fff; padding:2rem; text-align:center; margin-top:3rem; font-size:14px; }
        .footer a { color:var(--accent); text-decoration:none; }
        .staging-banner { background:#fff3cd; color:#856404; text-align:center; padding:6px 12px; font-size:13px; font-weight:600; }
        @media (max-width:768px){ .product-container{ grid-template-columns:1fr; } .product-title{ font-size:1.5rem; } }
"""

HEADER = """<div class="staging-banner">STAGING — internal preview, not public. Noindex.</div>
<header class="header"><div class="header-content"><a href="/" class="logo">Performance<span>Supply</span>Depot</a><div class="contact-info"><a href="tel:888-881-6834">📞 {phone}</a><a href="tel:415-571-9724">📞 (415) 571-9724</a><a href="mailto:info@psdepot.com">✉️ info@psdepot.com</a><a href="/checkout.html" class="cart-icon">🛒 Cart (<span id="cart-count">0</span>)</a></div></div></header>
<nav class="main-nav"><div class="container"><a href="/">Home</a><a href="/products/index.html">Products</a><a href="/blog/index.html">Blog</a><a href="/services.html">Services</a><a href="/testimonials.html">Testimonials</a><a href="/about.html">About</a><a href="/resources/faq.html">FAQ</a><a href="/contact.html">Contact</a><a href="/locations.html">Service Areas</a></div></nav>"""

FOOTER = """<section class="footer-cta"><h3>Questions About SAM4S?</h3><p>Authorized SAM4S dealer. Free consultation on ECR, POS, and receipt printers.</p><a href="tel:8888816834" class="phone">{phone}</a></section>
<footer class="footer"><p><strong>Performance Supply Depot LLC</strong></p><p>📞 <a href="tel:888-881-6834">{phone}</a> · ✉️ <a href="mailto:info@psdepot.com">info@psdepot.com</a></p><p style="color:#94a3b8;font-size:13px;">Authorized Dealer: <strong>SAM4S</strong> · CAS · ACM Technologies · TST Impresso · Capton</p><p style="color:#64748b;font-size:12px;">© 2026 Performance Supply Depot LLC. Serving California since 2005.</p></footer>"""


def specs_table(specs):
    rows = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in specs)
    return f'<table class="specs-table"><tbody>{rows}</tbody></table>'


def features_list(items):
    return '<ul class="features-list">' + "".join(f'<li>{x}</li>' for x in items) + '</ul>'


def compat_tags(tags):
    return '<div class="compat-tags">' + "".join(f'<span class="compat-tag">{t}</span>' for t in tags) + '</div>'


def page(m):
    sku = m.get("sku", f"SAM4S-{m['slug'].upper().replace('-','')}")
    condition = m.get("condition", "New")
    sam4pos = m.get("sam4pos", False)

    # Description: prepend SAM4POS angle if applicable
    desc = m["desc"]
    if sam4pos:
        desc = ("Runs <strong>SAM4POS</strong>, SAM4S's integrated Android POS software — one application "
                "configurable for food, beverage, and retail. " + desc)

    specs = list(m["specs"].items())
    specs.append(("Brand", "SAM4S"))
    specs.append(("Condition", condition))
    specs.append(("Pricing", "Call for pricing (placeholder)"))

    schema = {
        "@context": "https://schema.org", "@type": "Product",
        "name": m["name"], "sku": sku, "brand": {"@type": "Brand", "name": "SAM4S"},
        "description": m["meta"],
        "offers": {"@type": "Offer", "priceCurrency": "USD", "availability": "https://schema.org/InStock",
                   "itemCondition": "https://schema.org/NewCondition", "url": f"https://psdepot.com/staging/sam4s/{m['slug']}.html"},
    }

    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://psdepot.com/"},
            {"@type": "ListItem", "position": 2, "name": "Products", "item": "https://psdepot.com/products/"},
            {"@type": "ListItem", "position": 3, "name": "SAM4S", "item": "https://psdepot.com/staging/sam4s/"},
            {"@type": "ListItem", "position": 4, "name": m["name"], "item": f"https://psdepot.com/staging/sam4s/{m['slug']}.html"},
        ],
    }

    sam4pos_badge = ('<div style="background:#e0f7fa;border:1px solid #00bcd4;color:#006064;padding:.5rem .9rem;border-radius:8px;font-size:.9rem;font-weight:600;width:fit-content;">Runs SAM4POS Android POS software</div>' if sam4pos else '')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>{m['name']} | SAM4S Authorized Dealer | Performance Supply Depot</title>
<meta name="description" content="{m['meta']}">
<link rel="canonical" href="https://psdepot.com/staging/sam4s/{m['slug']}.html">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script type="application/ld+json">{json.dumps(schema)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb)}</script>
<style>{CSS}</style>
</head>
<body>
{HEADER.format(phone=PHONE)}
<div class="breadcrumb"><a href="/">Home</a> › <a href="/products/">Products</a> › <a href="/staging/sam4s/">SAM4S</a> › {m['name']}</div>
<div class="product-container">
  <div class="product-info">
    <span class="sku-badge">SKU: {sku} · MPN: {m['name']}</span>
    <h1 class="product-title">{m['name']} — {m['subtitle']}</h1>
    <div class="product-brand">Brand: <strong>SAM4S</strong> · {m['category']}</div>
    {sam4pos_badge}
    <div class="price-section">
      <div class="price-row"><span class="price-current">Call for Pricing</span></div>
      <div class="price-note">Pricing + SKU pending (staging placeholder)</div>
      <div style="margin:1rem 0;"><span class="condition-badge">Condition: {condition}</span></div>
      <div class="stock-status">✅ Authorized Dealer — SAM4S warranty</div>
      <div style="display:flex;gap:.75rem;flex-wrap:wrap;margin-top:1rem;">
        <a class="btn-quote" href="/contact.html">Request a Quote</a>
        <a class="btn-call" href="tel:8888816834">📞 {PHONE}</a>
      </div>
    </div>
    <div class="vendor-info"><h4>Authorized SAM4S Dealer</h4><p>Performance Supply Depot is an authorized SAM4S dealer. Android + standalone default; Windows available on special order.</p></div>
  </div>
</div>
<div class="product-details">
  <div class="details-section"><h3 class="details-title">Product Description</h3><div class="details-content"><p>{desc}</p></div></div>
  <div class="details-section"><h3 class="details-title">Key Features</h3>{features_list(m['features'])}</div>
  <div class="details-section"><h3 class="details-title">Technical Specifications</h3>{specs_table(specs)}</div>
  <div class="details-section"><h3 class="details-title">Ideal For</h3>{compat_tags(m['verticals'])}</div>
</div>
{FOOTER.format(phone=PHONE)}
</body>
</html>"""


# ---------------------------------------------------------------------------
# Model data (consolidated from staged research)
# ---------------------------------------------------------------------------
M = []

M.append(dict(slug="er-180u", name="ER-180U", subtitle="Entry Electronic Cash Register",
  category="Electronic Cash Register (ECR)", condition="New", sam4pos=False,
  sku="SAM4S-ER180U", meta="SAM4S ER-180U entry-level electronic cash register. 16 departments, 500 PLUs, thermal printer.",
  desc="An entry-level standalone electronic cash register for single-station retail and food counters. Proprietary firmware — no OS to manage, no Windows dependencies. Simple, reliable, and tax-ready with 4 VAT/tax rates.",
  features=["48 raised keys", "16 departments, 500 PLUs", "4 tax rates (VAT / add-on / tax table)", "90-day data storage", "2\" thermal printer (57.5mm, 65mm/s)", "Drawer port (3B4C / 4B4C)", "Euro currency conversion", "No network dependency — standalone"],
  specs={"Platform": "Proprietary 32-bit (NXP LPC1519)", "Printer": "1-station thermal 2\" (57.5mm), 65mm/s",
         "Display": "Operator 8-digit LED (customer optional)", "Departments": "16", "PLUs": "500", "Clerks": "10",
         "Tax": "4", "Electronic Journal": "No", "Data Storage": "90 days", "Interface": "RS-232C (firmware update only)"},
  verticals=["Retail", "Quick Service", "Convenience", "Bakery", "Deli", "Single-station counters"]))

M.append(dict(slug="er-230ej", name="ER-230EJ", subtitle="Full-Featured Fiscal Cash Register",
  category="Electronic Cash Register (ECR)", condition="New", sam4pos=False,
  sku="SAM4S-ER230EJ", meta="SAM4S ER-230EJ fiscal cash register with electronic journal, Ethernet, and 8,000 PLU capacity.",
  desc="A full-featured fiscal electronic cash register with electronic journal and Ethernet connectivity. Built for restaurants and retail that need tax/audit compliance and a traceable paper trail — every transaction logged, no OS to maintain.",
  features=["Electronic journal (SD card)", "Ethernet + 2× RS-232C + USB", "12 departments, 1,000 PLUs (up to 8,000)", "Fiscal memory (EPROM)", "Dual LCD — operator + customer", "90-day data storage", "Supports kitchen printer, scale, EFT, coin dispenser", "Drawer port (12V/24V)"],
  specs={"Platform": "Proprietary firmware", "Printer": "1-station thermal 57.5mm", "Display": "Dual 16-char × 2-line LCD",
         "Departments": "12", "PLUs": "1,000 (max 8,000)", "Groups": "20 (max 99)", "Clerks": "10 (max 99)",
         "Tax": "4", "Electronic Journal": "Yes (SD card)", "Fiscal Memory": "EPROM 2/4Mbit OTPROM",
         "Interfaces": "Ethernet, 2× RS-232C (RJ45), USB host+device, GPRS (opt.), SD ×2", "Drawer": "1 port RJ11 (12V/24V)"},
  verticals=["Restaurants", "Retail", "Bars", "Cafés", "Fiscal / tax compliance", "Hospitality"]))

M.append(dict(slug="nr-300-400", name="NR-300 / NR-400", subtitle="Compact Fiscal Cash Register",
  category="Electronic Cash Register (ECR)", condition="New", sam4pos=False,
  sku="SAM4S-NR300", meta="SAM4S NR-300/400 compact fiscal cash register. Electronic journal, Ethernet, 80mm thermal.",
  desc="A compact full-fiscal cash register for tight counter space. The NR-400 adds a graphic LCD. Same fiscal-grade electronic journal and Ethernet as the ER-230EJ in a smaller footprint, with 80mm paper support.",
  features=["Electronic journal (SD card)", "Ethernet + 2× RS-232C + USB", "57.5mm / 80mm paper", "1,000 PLUs (max 8,000)", "Fiscal memory (EPROM)", "NR-400 adds 192×64 graphic LCD", "90-day data storage"],
  specs={"Platform": "Proprietary firmware", "Printer": "1-station thermal 57.5mm / 80mm",
         "Display": "NR-300 16×2 LCD · NR-400 192×64 graphic LCD", "Departments": "4", "PLUs": "1,000 (max 8,000)",
         "Groups": "20 (max 99)", "Clerks": "10 (max 99)", "Tax": "4", "Electronic Journal": "Yes (SD card)",
         "Interfaces": "Ethernet, 2× RS-232C, USB host+device, GPRS (opt.), SD ×2", "Drawer": "1 port RJ11 (24V)"},
  verticals=["Compact counters", "Retail", "Cafés", "Kiosks", "Bars", "Fiscal compliance"]))

M.append(dict(slug="sap-630", name="SAP-630", subtitle="Android Restaurant POS / ECR",
  category="Electronic Cash Register (ECR)", condition="New", sam4pos=True,
  sku="SAM4S-SAP630", meta="SAM4S SAP-630 Android restaurant cash register running SAM4POS. 9.7\" touchscreen, kitchen printer support.",
  desc="An Android restaurant POS/ECR with a 9.7\" touchscreen, check tracking, and kitchen printer support. Runs SAM4POS, so one software covers table management, promotions, and reporting — supported remotely via TeamViewer, no site visit required.",
  features=["Runs SAM4POS Android POS software", "9.7\" LED touch (1024×768)", "3\" thermal printer (100mm/s)", "Check tracking — table management, add/split/merge", "MSR 1/2/3 + Dallas key", "Kitchen printer + video support", "VFD customer display (20ch × 2-line)", "Remote support via TeamViewer"],
  specs={"Platform": "Android 6 (Intel Celeron N3160 quad 2.24GHz)", "RAM": "DDR3 2GB", "Storage": "8GB eMMC",
         "Display": "9.7\" LED LCD (1024×768) resistive touch", "Keys": "160 flat / 90 raised",
         "Printer": "Internal 3\" thermal (100mm/s)", "I/O": "4× serial, 2× USB 2.0, Ethernet, WiFi/BT (opt.)",
         "Drawer": "Internal 1 + external 2 ports", "Software": "SAM4POS (SQLite)", "Power": "AC 100–240V"},
  verticals=["Restaurants", "Bars", "Cafés", "Quick Service", "Pizzerias", "Hospitality"]))

M.append(dict(slug="zeta-a50", name="ZETA-A50", subtitle="Modern Android Electronic Cash Register",
  category="Electronic Cash Register (ECR)", condition="New", sam4pos=True,
  sku="SAM4S-ZETAA50", meta="SAM4S ZETA-A50 Android 13 cash register with 50,000+ PLUs, Wi-Fi, and SAM4POS.",
  desc="SAM4S's newest Android 13 electronic cash register. 50,000+ PLUs, a 5\" touch operator display, and full networking (Wi-Fi, Ethernet, IRC). Runs SAM4POS for one-software operation across food, beverage, and retail — remotely manageable via TeamViewer.",
  features=["Android 13 (RK3566 quad-core)", "50,000+ PLUs, 100 groups, 100 clerks", "5\" TFT touch (1280×720) + LED customer display", "58mm thermal printer (70mm/s)", "1,000,000+ line electronic journal", "Wi-Fi + Ethernet + Bluetooth (opt.)", "Barcode / QR printing, mix & match promos", "IRC network — multi-station sync"],
  specs={"Platform": "Android 13 (RK3566 quad Cortex-A55)", "RAM": "2GB LPDDR4", "Storage": "16GB eMMC",
         "Display": "5\" TFT LCD touch (1280×720) + 8-digit LED", "Keys": "48 raised", "Printer": "58mm thermal (max 70mm/s)",
         "PLUs": ">50,000", "Tax": "10", "Electronic Journal": ">1,000,000 lines",
         "I/O": "2× serial (RJ45), 2× USB-A, GbE, Wi-Fi b/g/n, BT (opt.)", "Power": "DC 9V/5A",
         "Dimensions": "320 × 260 × 113 mm · 1.6kg"},
  verticals=["Restaurants", "Retail", "Bars", "Cafés", "Convenience", "Multi-station"]))

M.append(dict(slug="sapphire-android", name="SAPPHIRE Android", subtitle="Android POS Terminal",
  category="POS Terminal", condition="New", sam4pos=True,
  sku="SAM4S-SAPPHIRE-A", meta="SAM4S SAPPHIRE Android POS terminal — ARM big.LITTLE, 15\" touch, Android 9, SAM4POS.",
  desc="An Android POS terminal with a 15\" touchscreen and 10-point PCAP. Runs SAM4POS for one-software operation with remote TeamViewer support — no Windows licensing, no site visits. Ideal for a modern counter that wants tablet-like ease with full POS capability.",
  features=["Android 9 (ARM Cortex-A72 + A53)", "15\" / 15.6\" / FHD touch display", "10-point PCAP touch", "4GB LPDDR4 / 64GB eMMC", "3× serial + 6× USB + GbE + Wi-Fi ac + BT 5.0", "Runs SAM4POS", "MSR + rear display options", "VESA mount"],
  specs={"Platform": "Android 9 (Dual A72 1.8GHz + Quad A53 1.4GHz)", "RAM": "4GB LPDDR4", "Storage": "64GB eMMC",
         "Display": "15\" (1024×768) / 15.6\" (1366×768) / FHD (1920×1080) opt.", "Touch": "10-point PCAP",
         "I/O": "Serial 3 (+1 opt), USB 6, GbE, Wi-Fi ac, BT 5.0, DP 1", "Drawer": "1 port / 2CH (12V/24V)",
         "Options": "MSR 1/2/3, rear display", "Power": "AC 100–240V / DC 12V 5A (60W)"},
  verticals=["Retail", "Restaurants", "Bars", "Cafés", "Boutiques", "Multi-lane"]))

M.append(dict(slug="sap-6600", name="SAP-6600", subtitle="Android POS Terminal (budget / used available)",
  category="POS Terminal", condition="Used available · New on request", sam4pos=True,
  sku="SAM4S-SAP6600", meta="SAM4S SAP-6600 Android POS terminal. 15\" touch, Android 6. Used units available.",
  desc="A budget Android POS terminal with a 15\" touchscreen. Runs SAM4POS. Newer ZETA-A50 and SAPPHIRE Android are its modern successors, but the SAP-6600 remains a cost-effective option — and we currently have a used unit in stock.",
  features=["15\" LCD touch (1024×768), 10-point PCAP", "Android 6 (Intel Celeron N3160)", "3× serial + 6× USB + GbE + Wi-Fi ac", "Runs SAM4POS", "MSR + rear display (VFD/LCD) options", "VESA mount", "Used unit available now"],
  specs={"Platform": "Android 6 (Intel Celeron N3160 quad 2.24GHz)", "RAM": "DDR3 2GB", "Storage": "64GB M.2 SSD",
         "Display": "15\" LCD 1024×768, 10-point PCAP", "I/O": "Serial 3 (+1 opt), USB 6, GbE, Wi-Fi ac, BT 4.0, VGA",
         "Drawer": "1 port / 2CH (12V/24V)", "Options": "MSR 1/2/3, rear display", "Dimensions": "379 × 264 × 362 mm · 6kg"},
  verticals=["Budget-conscious retail", "Cafés", "Bars", "Used/refurb", "Entry POS"]))

M.append(dict(slug="astra-android", name="ASTRA Android", subtitle="Self-Service Kiosk (Android 13)",
  category="Kiosk", condition="New", sam4pos=False,
  sku="SAM4S-ASTRA-A", meta="SAM4S ASTRA Android self-service kiosk — 21.5\" FHD touch, Android 13, integrated payment options.",
  desc="A 21.5\" full-HD self-service kiosk running Android 13. Ideal for self-ordering and self-checkout with an integrated receipt printer option, 2D barcode scanner, and MSR/IC/NFC payment support. No Windows dependency.",
  features=["Android 13 (ARM Cortex-A72 + A53)", "21.5\" Full HD (1920×1080) touch, 10-point PCAP", "4GB LPDDR4 / 64GB eMMC", "Integrated / external receipt printer", "2D barcode scanner (opt.)", "MSR / IC / NFC + 2MP camera", "Floor-standing or wall-mount"],
  specs={"Platform": "Android 13 (ARM Cortex-A72 1.8GHz + A53 1.4GHz)", "RAM": "4GB LPDDR4", "Storage": "64GB eMMC",
         "Display": "21.5\" Full HD (1920×1080), 10-pt PCAP", "I/O": "Serial 5, USB 4, GbE, Wi-Fi ac, BT 5.0, NFC (opt.)",
         "Peripherals": "2D scanner, receipt printer (integrated/external), 2MP camera, MSR/IC/NFC", "Install": "Floor-standing / wall-mount"},
  verticals=["Self-service ordering", "QSR", "Retail self-checkout", "Cafés", "Ticketing"]))

# Printers
M.append(dict(slug="hcube", name="Hcube", subtitle="Entry Receipt Printer",
  category="Receipt Printer", condition="New", sam4pos=False,
  sku="SAM4S-HCUBE", meta="SAM4S Hcube entry receipt printer — direct thermal 203dpi, 230mm/s, ESC/POS.",
  desc="A slim, entry-level direct thermal receipt printer. 72mm print width, auto cutter, and USB + Serial + Ethernet out of the box. A dependable workhorse for simple receipt printing at a low price point.",
  features=["Direct thermal, 203 dpi", "230mm/s print speed", "72mm print width (576 dots)", "Auto cutter (partial cut)", "USB + Serial + Ethernet", "ESC/POS emulation", "Compact 140×179×117mm"],
  specs={"Method": "Direct thermal, 203 dpi", "Print width": "72mm (576 dots)", "Speed": "Max 230mm/s",
         "Interfaces": "USB + Serial + Ethernet", "Cutter": "Auto (partial cut)", "Emulation": "ESC/POS",
         "Memory": "4MB RAM / 4MB Flash", "Paper": "79.5±0.5mm / 57.5±0.5mm, Ø83mm", "Dimensions": "140 × 179 × 117 mm · 0.92kg"},
  verticals=["Receipt printing", "Retail", "Cafés", "Kitchen (basic)", "Low-volume"]))

M.append(dict(slug="gcube", name="Gcube", subtitle="Compact Receipt / POS Printer",
  category="Receipt Printer", condition="New", sam4pos=False,
  sku="SAM4S-GCUBE", meta="SAM4S Gcube compact receipt printer — 250mm/s, kitchen bell + under-shelf mount, EPSON/STAR emulation.",
  desc="A compact 123mm-cube receipt printer built for kitchens and bars. 250mm/s on 80mm paper, auto cutter, and kitchen options (kitchen bell, under-shelf mount) that make it the go-to for restaurant and bar environments.",
  features=["Thermal line, 180/203 dpi", "80mm @ 250mm/s (fast)", "Drop-in paper loading, Ø83mm roll", "Auto cutter (1.5M cuts)", "Kitchen bell + under-shelf / wall mount", "EPSON + STAR emulation", "USB / Serial / BT / Wi-Fi / Ethernet variants", "2 drawer ports (+24V)"],
  specs={"Method": "Thermal line, 180/203 dpi", "Speed": "80mm @250mm/s; 58mm @150mm/s; 2-color @100mm/s",
         "Paper": "Drop-in, max 80mm/58mm, Ø83mm", "Cutter": "Auto 1.5M cuts · MCBF 70M lines",
         "Interfaces": "USB+Serial / USB+BT+Eth / USB+Wi-Fi+Eth / USB+Serial(9)+Eth", "Drawer": "2 ports (+24V)",
         "Emulation": "EPSON, STAR", "Barcodes": "Full set + PDF417 + QR", "Options": "Kitchen bell, wall/under-shelf, near-end sensor",
         "Dimensions": "123 × 123 × 123 mm · 750g"},
  verticals=["Bars", "Restaurants", "Kitchens", "Cafés", "Food trucks"]))

M.append(dict(slug="giant-100", name="GIANT-100", subtitle="Splash-Proof Receipt Printer",
  category="Receipt Printer", condition="New", sam4pos=False,
  sku="SAM4S-GIANT100", meta="SAM4S GIANT-100 splash-proof receipt printer — 250mm/s, wall mount, kitchen bell.",
  desc="A splash-proof thermal receipt printer with a wall-mount default and kitchen bell. Built for wet/high-traffic environments where spills happen. 250mm/s on 80mm paper with EPSON/STAR emulation.",
  features=["Thermal line, 180 dpi", "80mm @ 250mm/s", "Splash cover (water-resistant)", "Wall mount (default) + kitchen bell", "Paper separator (58mm) default", "Auto cutter (1.5M cuts)", "EPSON + STAR emulation"],
  specs={"Method": "Thermal line, 180 dpi", "Speed": "80mm @250mm/s; 58mm @150mm/s", "Paper": "Drop-in, max 80mm/58mm, Ø83mm",
         "Cutter": "Auto 1.5M cuts · MCBF 70M lines", "Interfaces": "USB+Serial / USB+Wi-Fi / USB+Serial+Eth",
         "Drawer": "2 ports (+24V)", "Emulation": "EPSON, STAR", "Options": "Splash cover, wall mount (default), kitchen bell",
         "Dimensions": "131 × 155 × 133 mm · 1.0kg"},
  verticals=["Bars", "Kitchens", "Food service", "Wet environments", "Cafés"]))

M.append(dict(slug="ellix30iii", name="ELLIX30III", subtitle="High-Duty Receipt Printer",
  category="Receipt Printer", condition="New", sam4pos=False,
  sku="SAM4S-ELLIX30III", meta="SAM4S ELLIX30III receipt printer — 230mm/s, NFC tag, kitchen bell, splash cover.",
  desc="A high-duty thermal receipt printer with NFC tag and a wide interface set (Serial, Parallel, Wi-Fi, Ethernet combo). 230mm/s with EPSON/STAR emulation and full kitchen options.",
  features=["Thermal line, 180 dpi", "80mm @ 230mm/s", "NFC tag option", "Kitchen bell + splash cover", "USB / Serial / Parallel / Wi-Fi / 3-combo", "Auto cutter (1.5M cuts)", "EPSON + STAR emulation"],
  specs={"Method": "Thermal line, 180 dpi", "Speed": "80mm @230mm/s; 58mm @150mm/s", "Paper": "Drop-in, max 80mm/58mm, Ø83mm",
         "Cutter": "Auto 1.5M cuts · MCBF 70M lines", "Interfaces": "USB+Serial(25) / USB+Serial(9+RJ45) / USB+Parallel / USB+Wi-Fi / 3-combo",
         "Drawer": "2 ports (+24V)", "Emulation": "EPSON, STAR", "Options": "NFC tag, kitchen bell, wall mount, splash cover",
         "Dimensions": "144 × 195 × 137 mm · 2.0kg"},
  verticals=["Retail", "Restaurants", "Kitchens", "High-volume", "Cafés"]))

M.append(dict(slug="ellix40ii", name="ELLIX40II", subtitle="Flagship Receipt Printer",
  category="Receipt Printer", condition="New", sam4pos=False,
  sku="SAM4S-ELLIX40II", meta="SAM4S ELLIX40II flagship receipt printer — 270mm/s, kitchen bell + LCD, full interface set.",
  desc="SAM4S's fastest receipt printer at 270mm/s. Full interface set (USB, Serial, Parallel, Bluetooth, Wi-Fi, Ethernet), kitchen bell + LCD, and 10MB program memory — the flagship for high-volume kitchens and retail.",
  features=["Thermal line, 180 dpi", "80mm @ 270mm/s (fastest)", "Kitchen bell + LCD", "Full interface set (USB/Serial/Parallel/BT/Wi-Fi/Eth)", "Paper near-end sensor (default)", "Auto cutter (1.5M cuts)", "EPSON + STAR emulation"],
  specs={"Method": "Thermal line, 180 dpi", "Speed": "80mm @270mm/s; 58mm @150mm/s", "Paper": "Drop-in, max 80mm/58mm, Ø83mm",
         "Cutter": "Auto 1.5M cuts · MCBF 70M lines", "Memory": "10MB program + 8MB data",
         "Interfaces": "USB / Serial(25) / Serial(9+RJ45) / Parallel / BT / Wi-Fi / 3-combo", "Drawer": "2 ports (+24V)",
         "Options": "Kitchen bell + LCD, wall mount, splash cover, near-end (default)", "Dimensions": "144 × 195 × 137 mm · 2.0kg"},
  verticals=["High-volume kitchens", "Retail", "Restaurants", "Bars", "Franchises"]))

# Drawers
M.append(dict(slug="k-drawer", name="K-Drawer", subtitle="Heavy-Duty Cash Drawer",
  category="Cash Drawer", condition="New", sam4pos=False,
  sku="SAM4S-KDRAWER", meta="SAM4S K-Drawer heavy-duty steel cash drawer — 4B8C, 1,000,000 cycles, 12V/24V.",
  desc="A heavy-duty all-steel cash drawer rated for 1,000,000 cycles. 4-bill / 8-coin configuration with separate bill and coin partitions, RJ11 interface, and 12V/24V solenoid.",
  features=["All-steel construction (top/bottom/till)", "4 bill / 8 coin (4B8C) configuration", "1,000,000 cycle life", "RJ11 interface, 12V/24V solenoid", "2-position lock (3-position optional)", "Coin + bill partition separation", "Locking lid (optional)"],
  specs={"Material": "Steel (top/bottom/till)", "Configuration": "4B8C (bill 87/180/54 · coin 78/67/39)",
         "Dimensions": "400 × 440 × 112 mm", "Interface": "RJ11", "Solenoid": "12V/24V",
         "Life": "1,000,000 cycles", "Lock": "2-position (3-position opt.)", "Weight": "6.7kg"},
  verticals=["Retail", "Restaurants", "High-traffic", "Bars", "Grocery"]))

M.append(dict(slug="bplus-drawer", name="Bplus-Drawer", subtitle="Mid-Tier Cash Drawer",
  category="Cash Drawer", condition="New", sam4pos=False,
  sku="SAM4S-BPLUSDRAWER", meta="SAM4S Bplus-Drawer cash drawer — 3B4C/4B4C, 300,000 cycles, 7V/12V/24V.",
  desc="A mid-tier cash drawer with a steel top and plastic body for a lighter, more affordable option. 3-bill/4-coin or 4-bill/4-coin configuration, RJ11 interface, and flexible 7V/12V/24V solenoid.",
  features=["Steel top, plastic body (lighter)", "3B4C / 4B4C configuration", "300,000 cycle life", "RJ11 interface, 7V/12V/24V solenoid", "3-position key lock", "Coin + bill partition separation"],
  specs={"Material": "Steel top, plastic bottom/till", "Configuration": "3B4C / 4B4C",
         "Dimensions": "325 × 420 × 95 mm", "Interface": "RJ11", "Solenoid": "7V/12V/24V",
         "Life": "300,000 cycles", "Lock": "3-position key", "Weight": "3.1kg"},
  verticals=["Retail", "Cafés", "Light-duty", "Boutiques", "Counter service"]))

M.append(dict(slug="h-drawer", name="H-Drawer", subtitle="Cash Drawer",
  category="Cash Drawer", condition="New", sam4pos=False,
  sku="SAM4S-HDRAWER", meta="SAM4S H-Drawer cash drawer. Specifications available on request.",
  desc="SAM4S H-Drawer cash drawer. Full specifications available on request — contact us for the spec sheet.",
  features=["SAM4S cash drawer", "Specs available on request"],
  specs={"Brand": "SAM4S", "Specs": "Available on request"},
  verticals=["Cash drawer", "Specs on request"]))


# ---------------------------------------------------------------------------
# Generate pages + index
# ---------------------------------------------------------------------------
for m in M:
    with open(os.path.join(OUT, m["slug"] + ".html"), "w") as f:
        f.write(page(m))

# Index page
rows = ""
for m in M:
    rows += f'<li><a href="{m["slug"]}.html">{m["name"]} — {m["subtitle"]}</a> <span style="color:#718096;font-size:.85rem;">({m["category"]})</span></li>'

index = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow"><title>SAM4S Catalog — Staging | Performance Supply Depot</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,Roboto,sans-serif;max-width:900px;margin:2rem auto;padding:0 24px;line-height:1.6;color:#111;}}
h1{{color:#0A1A2F}} .banner{{background:#fff3cd;color:#856404;padding:10px 16px;border-radius:8px;font-weight:600;margin-bottom:1rem}}
li{{margin:.5rem 0}}</style></head><body>
<div class="banner">STAGING — internal preview only (noindex). SAM4S catalog · {TODAY}</div>
<h1>SAM4S Catalog — {len(M)} models</h1>
<p>Default stock: standalone ECR + Android + peripherals. Windows on special order. Pricing/SKU placeholder.</p>
<ul>{rows}</ul>
</body></html>"""

with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(index)

print(f"✅ Generated {len(M)} product pages + index in {OUT}")
for m in M:
    print(f"  - {m['name']} ({m['category']})")
