#!/usr/bin/env python3
"""Add the missing main-nav to pages that have a header but no navigation."""
import os

PAGES = [
    "industries/grocery-stores.html",
    "industries/retail-stores.html",
    "industries/restaurants.html",
    "guides/pos-starter-kit.html",
]
VERSIONS = ["/var/www/psdepot-v0", "/var/www/psdepot-v1"]

NAV_CSS = """        .main-nav {
            background: #12283f;
            border-bottom: 3px solid var(--accent);
        }
        .main-nav .container {
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
        }
        .main-nav a {
            display: inline-block;
            color: #bee3f8;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            padding: 12px 18px;
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
        }
        .main-nav a:hover,
        .main-nav a:focus {
            color: #ffffff;
            background: rgba(255,255,255,0.08);
            border-bottom-color: var(--accent);
        }
        .main-nav a[aria-current="page"] {
            color: #ffffff;
            border-bottom-color: var(--accent);
        }
"""

NAV_MARKUP = """    <nav class="main-nav" aria-label="Primary">
        <div class="container">
            <a href="/">Home</a>
            <a href="/products/index.html">Products</a>
            <a href="/blog/index.html">Blog</a>
            <a href="/services.html">Services</a>
            <a href="/testimonials.html">Testimonials</a>
            <a href="/about.html">About</a>
            <a href="/resources/faq.html">FAQ</a>
            <a href="/contact.html">Contact</a>
            <a href="/locations.html">Service Areas</a>
        </div>
    </nav>
"""

for ver in VERSIONS:
    for page in PAGES:
        path = os.path.join(ver, page)
        if not os.path.exists(path):
            print(f"SKIP (missing): {path}")
            continue
        with open(path) as f:
            content = f.read()

        changed = False

        # 1. Add CSS before </style> if .main-nav not already present
        if ".main-nav {" not in content:
            content = content.replace("    </style>", NAV_CSS + "    </style>", 1)
            changed = True

        # 2. Add nav markup after </header> if not already present
        if '<nav class="main-nav"' not in content:
            if "</header><div" in content:
                # header immediately followed by container (pos-starter-kit)
                content = content.replace("</header><div", "</header>\n" + NAV_MARKUP + "\n<div", 1)
            else:
                content = content.replace("</header>", "</header>\n\n" + NAV_MARKUP, 1)
            changed = True

        if changed:
            with open(path, "w") as f:
                f.write(content)
            print(f"UPDATED: {path}")
        else:
            print(f"NO-OP (already has nav): {path}")
