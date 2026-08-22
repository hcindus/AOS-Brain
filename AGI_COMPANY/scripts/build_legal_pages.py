#!/usr/bin/env python3
"""Generate psdepot.com legal pages: privacy.html, terms.html, return-policy.html."""
import os

SITE = "/var/www/psdepot.com"
TODAY = "2026-08-22"

HEADER = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Performance Supply Depot LLC</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://psdepot.com/{slug}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>
:root {{ --primary:#0A1A2F; --accent:#d69e2e; --text:#111; --muted:#718096; --border:#e2e8f0; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:#F8F9FA; color:var(--text); line-height:1.7; }}
.main-nav {{ background:#12283f; border-bottom:3px solid var(--accent); }}
.main-nav .container {{ display:flex; gap:4px; flex-wrap:wrap; max-width:1000px; margin:0 auto; padding:0 24px; }}
.main-nav a {{ display:inline-block; color:#bee3f8; text-decoration:none; font-weight:600; font-size:15px; padding:12px 18px; }}
.main-nav a:hover {{ color:#fff; }}
.container {{ max-width:900px; margin:0 auto; padding:32px 24px; }}
h1 {{ color:var(--primary); font-size:2rem; margin-bottom:8px; }}
h2 {{ color:var(--primary); font-size:1.4rem; margin:32px 0 12px; }}
p, li {{ margin-bottom:12px; }}
ul {{ padding-left:24px; }}
.updated {{ color:var(--muted); font-size:0.9rem; margin-bottom:24px; }}
footer {{ background:var(--primary); color:#fff; padding:28px 24px; text-align:center; font-size:14px; }}
footer a {{ color:#d69e2e; text-decoration:none; }}
</style>
</head>
<body>
<header style="background:#0A1A2F;color:#fff;padding:14px 24px;"><div style="max-width:1000px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;"><a href="/" style="font-size:22px;font-weight:800;color:#fff;text-decoration:none;">Performance<span style="color:#63b3ed;">Supply</span>Depot</a><div style="display:flex;gap:16px;flex-wrap:wrap;font-size:14px;"><a href="tel:888-881-6834" style="color:#fff;text-decoration:none;">📞 (888) 881-6834</a><a href="mailto:info@psdepot.com" style="color:#bee3f8;text-decoration:none;">✉️ info@psdepot.com</a></div></div></header>
<nav class="main-nav"><div class="container"><a href="/">Home</a><a href="/products/index.html">Products</a><a href="/blog/index.html">Blog</a><a href="/services.html">Services</a><a href="/about.html">About</a><a href="/contact.html">Contact</a></div></nav>
<div class="container">
<h1>{title}</h1>
<div class="updated">Last updated: {today}</div>
'''

FOOTER = '''</div>
<footer><div style="max-width:900px;margin:0 auto;"><p><strong>Performance Supply Depot LLC</strong></p><p style="color:#94a3b8;font-size:13px;">Serving California since 2005 · Authorized Dealer: SAM4S · CAS · ACM Technologies · TST Impresso · Capton</p><p style="margin-top:10px;"><a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a> · <a href="/return-policy.html">Returns</a> · <a href="/contact.html">Contact</a></p></div></footer>
</body>
</html>
'''

PAGES = [
    dict(slug="privacy.html", title="Privacy Policy",
        desc="Performance Supply Depot LLC privacy policy — data collection, cookies, third-party sharing, and your rights (CCPA / GDPR).",
        body="""
<p>Performance Supply Depot LLC ("we", "us", "PSD") respects your privacy. This policy explains what information we collect, how we use it, and the rights you have over it.</p>

<h2>Information We Collect</h2>
<ul>
<li><strong>Contact & order data:</strong> name, email address, phone number, shipping address, and billing details you provide when placing an order or contacting us.</li>
<li><strong>Order & account history:</strong> products purchased, order status, and support correspondence.</li>
<li><strong>Technical data:</strong> IP address, browser type, device, and pages visited (via cookies and server logs).</li>
</ul>

<h2>Cookies</h2>
<p>We use cookies and similar technologies to operate the site, remember your cart, analyze traffic, and improve your experience. You can disable cookies in your browser, though some site features (such as the shopping cart) may not function correctly without them.</p>

<h2>How We Use Your Information</h2>
<ul>
<li>To process and fulfill orders, and to provide customer support.</li>
<li>To communicate about your orders, and (with consent) send marketing updates.</li>
<li>To improve our products, services, and website.</li>
<li>To meet legal, tax, and regulatory obligations.</li>
</ul>

<h2>Third-Party Sharing</h2>
<p>We do not sell your personal information. We share data only with service providers who help us operate (payment processors, shipping carriers, and hosting/email providers), and only as necessary to fulfill orders or comply with law.</p>

<h2>Your Rights (CCPA & GDPR)</h2>
<p>Depending on your location, you may have the right to:</p>
<ul>
<li>Access, correct, or delete your personal information.</li>
<li>Request a copy of the data we hold about you.</li>
<li>Opt out of marketing communications at any time.</li>
<li>Lodge a complaint with a supervisory authority.</li>
</ul>

<h2>Legal Basis for Processing</h2>
<p><strong>CCPA (California):</strong> We collect personal information for providing services (contractual necessity), legal compliance (tax/regulatory), and legitimate business interests (security, fraud prevention). Your CCPA rights include the right to know, request deletion (subject to legal holds), opt out of sale (we do not sell data), and non-discrimination for exercising your rights.</p>
<p><strong>GDPR (EU/UK):</strong> We process data based on contract performance, legal obligations, legitimate interests, and consent where required. You have the right to access, rectify, erase, restrict, port, and object to processing of your personal data.</p>

<h2>Data Inventory & Retention</h2>
<ul>
<li><strong>Order records:</strong> encrypted, retained 7 years (tax)</li>
<li><strong>Customer support:</strong> 3 years</li>
<li><strong>Website/analytics logs:</strong> 6 months</li>
<li><strong>System backups:</strong> 90 days</li>
</ul>

<h2>Data Retention</h2>
<p>We retain order and account records for as long as necessary to fulfill orders, provide support, and meet legal/tax obligations (typically up to 7 years for financial records).</p>

<h2>Security</h2>
<p>We use reasonable administrative, technical, and physical safeguards to protect your information. No method of transmission over the internet is 100% secure, and we cannot guarantee absolute security.</p>

<h2>Contact</h2>
<p>For privacy requests or questions, contact us at <a href="mailto:info@psdepot.com">info@psdepot.com</a> or call (888) 881-6834.</p>
"""),
    dict(slug="terms.html", title="Terms of Service",
        desc="Performance Supply Depot LLC terms of service — agreement, acceptable use, liability, and dispute resolution.",
        body="""
<p>These Terms of Service ("Terms") govern your use of psdepot.com and your purchase of products from Performance Supply Depot LLC. By using the site or placing an order, you agree to these Terms.</p>

<h2>Use of the Site</h2>
<p>You agree to use the site lawfully and not to interfere with its operation, attempt unauthorized access, or misuse any content. You may browse and purchase products for lawful commercial or personal use.</p>

<h2>Orders & Pricing</h2>
<p>All prices are in U.S. dollars. We reserve the right to correct pricing errors and to refuse or cancel orders. Product availability and specifications may change without notice.</p>

<h2>Acceptable Use</h2>
<p>You may use the site to browse and purchase products for lawful purposes. You may not use the site to transmit malware, attempt unauthorized access, scrape content at scale without permission, or otherwise interfere with the site's operation.</p>

<h2>Intellectual Property</h2>
<p>All content on this site (text, images, logos, and product descriptions) is owned by Performance Supply Depot LLC or its licensors and may not be reproduced without permission. Product names and trademarks belong to their respective owners.</p>

<h2>Limitation of Liability</h2>
<p>To the maximum extent permitted by law, Performance Supply Depot LLC shall not be liable for indirect, incidental, special, or consequential damages arising from use of the site or products. Our total liability is limited to the amount you paid for the product at issue.</p>

<h2>Warranty Disclaimer</h2>
<p>Products are sold "as is" except as covered by the applicable manufacturer warranty. We make no warranties beyond those provided by the manufacturer.</p>

<h2>Dispute Resolution & Governing Law</h2>
<p>These Terms are governed by the laws of the State of California. Any dispute shall be resolved in the state or federal courts located in California. You agree to attempt informal resolution by contacting us before pursuing formal action.</p>

<h2>Termination</h2>
<p>We may suspend or terminate access to the site for violations of these Terms or unlawful activity.</p>

<h2>Contact</h2>
<p>Questions about these Terms? Contact us at <a href="mailto:info@psdepot.com">info@psdepot.com</a> or call (888) 881-6834.</p>
"""),
    dict(slug="return-policy.html", title="Return Policy",
        desc="Performance Supply Depot LLC return policy — 30-day returns, refunds, and how to start a return.",
        body="""
<p>We want you to be satisfied with your purchase. This policy explains how returns and refunds work at Performance Supply Depot LLC.</p>

<h2>30-Day Returns</h2>
<p>Most new, unopened products may be returned within <strong>30 days</strong> of delivery for a refund or exchange, subject to the conditions below.</p>

<h2>Eligibility</h2>
<ul>
<li>Item must be in new, resalable condition with original packaging, manuals, and accessories.</li>
<li>Software, opened consumables (thermal paper, ribbons, ink), and custom-configured equipment may be non-returnable.</li>
<li>Return shipping may be the customer's responsibility unless the item is defective or we made an error.</li>
</ul>

<h2>Defective or Damaged Items</h2>
<p>If an item arrives defective or damaged, contact us within <strong>7 days</strong> of delivery with photos. We will arrange a replacement or refund at no cost to you.</p>

<h2>Refunds</h2>
<p>Approved refunds are issued to the original payment method within 5–10 business days of receiving the returned item. Original shipping charges may be deducted for non-defective returns.</p>

<h2>Restocking Fee</h2>
<p>A restocking fee of up to 15% may apply to non-defective returns of opened or special-order equipment.</p>

<h2>How to Start a Return</h2>
<p>Contact us at <a href="mailto:info@psdepot.com">info@psdepot.com</a> or call (888) 881-6834 with your order number to request a Return Authorization (RA) before shipping anything back.</p>
"""),
]

for p in PAGES:
    html = HEADER.format(title=p["title"], desc=p["desc"], slug=p["slug"], today=TODAY) + p["body"] + FOOTER
    out = os.path.join(SITE, p["slug"])
    open(out, "w").write(html)
    print(f"✅ {p['slug']} ({p['title']})")
print("Done.")
