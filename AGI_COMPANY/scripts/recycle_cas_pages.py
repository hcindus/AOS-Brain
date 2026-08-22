#!/usr/bin/env python3
"""Recycle 5 mislabeled CAS 'cash register' pages into SAM4S receipt printers + kiosk."""
import os, re, shutil

MCD = "/var/www/psdepot.com/products/mscashdrawer"
ARCHIVE = os.path.join(MCD, "_archive")
TMPL = os.path.join(MCD, "sam4s-sap-630-ft-flat-keyboard-android-terminal.html")

OLD = [
    "cas-se-c3500mc-split-keyboard-cash-register",
    "cas-sr-4000mc-raised-keyboarddual-station-printer",
    "cas-te-3000-ecr-stroke-keyboard-multi-line-lcd",
    "cas-te-4500fb-cb-with-mid-size-cash-drawer-dl-3616",
    "cas-tk-3200c-flat-keyboard-cash-register",
]

NEW = [
    dict(slug="sam4s-gcube-receipt-printer", name="SAM4S Gcube Compact Receipt Printer",
         sku="PSD-CRS-GCUBE", sub="SAM4s CRS SAM4s Receipt Printer",
         feat=["Compact 123mm cube","250mm/s (80mm)","Kitchen bell + under-shelf mount","EPSON + STAR emulation"],
         desc="A compact 123mm-cube receipt printer built for kitchens and bars. 250mm/s on 80mm paper, auto cutter, and kitchen options (kitchen bell, under-shelf mount) that make it the go-to for restaurant and bar environments.",
         specs=[("Print Method","Thermal line, 180/203 dpi"),("Speed","80mm @250mm/s; 58mm @150mm/s"),
                ("Paper","Drop-in, max 80mm/58mm, Ø83mm"),("Cutter","Auto 1.5M cuts · MCBF 70M lines"),
                ("Interfaces","USB+Serial / USB+BT+Eth / USB+Wi-Fi+Eth"),("Emulation","EPSON, STAR"),
                ("Drawer","2 ports (+24V)"),("Warranty","1 year")]),
    dict(slug="sam4s-ellix40ii-receipt-printer", name="SAM4S ELLIX40II Receipt Printer",
         sku="PSD-CRS-ELLIX40II", sub="SAM4s CRS SAM4s Receipt Printer",
         feat=["Fastest at 270mm/s","Kitchen bell + LCD","Full interface set","EPSON + STAR emulation"],
         desc="SAM4S's fastest receipt printer at 270mm/s. Full interface set (USB, Serial, Parallel, Bluetooth, Wi-Fi, Ethernet), kitchen bell + LCD, and 10MB program memory — the flagship for high-volume kitchens and retail.",
         specs=[("Print Method","Thermal line, 180 dpi"),("Speed","80mm @270mm/s; 58mm @150mm/s"),
                ("Memory","10MB program + 8MB data"),("Cutter","Auto 1.5M cuts"),
                ("Interfaces","USB / Serial / Parallel / BT / Wi-Fi / 3-combo"),("Emulation","EPSON, STAR"),
                ("Drawer","2 ports (+24V)"),("Warranty","1 year")]),
    dict(slug="sam4s-giant-100-receipt-printer", name="SAM4S GIANT-100 Splash-Proof Receipt Printer",
         sku="PSD-CRS-GIANT100", sub="SAM4s CRS SAM4s Receipt Printer",
         feat=["Splash cover (water-resistant)","Wall mount default","Kitchen bell","250mm/s"],
         desc="A splash-proof thermal receipt printer with a wall-mount default and kitchen bell. Built for wet, high-traffic environments where spills happen. 250mm/s on 80mm paper with EPSON/STAR emulation.",
         specs=[("Print Method","Thermal line, 180 dpi"),("Speed","80mm @250mm/s"),
                ("Cutter","Auto 1.5M cuts"),("Options","Splash cover, wall mount, kitchen bell"),
                ("Emulation","EPSON, STAR"),("Drawer","2 ports (+24V)"),("Warranty","1 year")]),
    dict(slug="sam4s-hcube-receipt-printer", name="SAM4S Hcube Entry Receipt Printer",
         sku="PSD-CRS-HCUBE", sub="SAM4s CRS SAM4s Receipt Printer",
         feat=["Direct thermal 203dpi","230mm/s","USB + Serial + Ethernet","ESC/POS emulation"],
         desc="A slim, entry-level direct thermal receipt printer. 72mm print width, auto cutter, and USB + Serial + Ethernet out of the box. A dependable workhorse for simple receipt printing at a low price point.",
         specs=[("Print Method","Direct thermal, 203 dpi"),("Print Width","72mm (576 dots)"),
                ("Speed","230mm/s"),("Interfaces","USB + Serial + Ethernet"),
                ("Cutter","Auto (partial cut)"),("Emulation","ESC/POS"),("Warranty","1 year")]),
    dict(slug="sam4s-astra-android-kiosk", name="SAM4S ASTRA Android Self-Service Kiosk",
         sku="PSD-CRS-ASTRA-A", sub="SAM4s CRS SAM4s Kiosk",
         feat=["Android 13","21.5\" Full HD touch","Integrated receipt printer","MSR / IC / NFC"],
         desc="A 21.5\" full-HD self-service kiosk running Android 13. Ideal for self-ordering and self-checkout with an integrated receipt printer option, 2D barcode scanner, and MSR/IC/NFC payment support. No Windows dependency.",
         specs=[("OS","Android 13 (ARM Cortex-A72 + A53)"),("RAM / Storage","4GB LPDDR4 / 64GB eMMC"),
                ("Display","21.5\" Full HD (1920x1080), 10-pt PCAP"),("Peripherals","2D scanner, receipt printer, 2MP camera, MSR/IC/NFC"),
                ("Install","Floor-standing / wall-mount"),("Warranty","1 year")]),
]

# 1. archive old pages
os.makedirs(ARCHIVE, exist_ok=True)
for o in OLD:
    src = os.path.join(MCD, o + ".html")
    if os.path.exists(src):
        shutil.move(src, os.path.join(ARCHIVE, o + ".html"))
        print(f"  archived {o}.html")

# 2. build new pages from template
base = open(TMPL).read()
for n in NEW:
    html = base
    html = html.replace("SAM4s SAP-630-FT Flat Keyboard Android Terminal | Performance Supply Depot LLC",
                        f"{n['name']} | Performance Supply Depot LLC")
    html = html.replace("sam4s-sap-630-ft-flat-keyboard-android-terminal", n["slug"])
    html = html.replace("Sam4s SAP-630-FT flat keyboard Android based Terminal. Needs software. CRS Dealer line required.",
                        n["desc"])
    html = html.replace("SAM4s SAP-630-FT Flat Keyboard Android Terminal", n["name"])
    html = html.replace("SKU: PSD-CRS-SAP-630-FT | MPN: CRS-SAP-630-FT", f"SKU: {n['sku']} | MPN: {n['sku']}")
    html = html.replace("SAM4s CRS SAM4s Cash Registers", n["sub"])
    html = html.replace("const sku = 'PSD-CRS-SAP-630-FT';", f"const sku = '{n['sku']}';")
    html = html.replace("const name = 'SAM4s SAP-630-FT Flat Keyboard Android Terminal';", f"const name = '{n['name']}';")
    html = html.replace("const price = 1331.67;", "const price = 0;")
    html = html.replace('<div class="price">$1331.67</div>', '<div class="price">Call for Pricing</div>')
    html = html.replace('<div class="price-note">MSRP: $1665.00 — You save $333.33</div>', '<div class="price-note">Pricing available on request</div>')
    html = html.replace("Out of Stock", "Call for availability")

    # features grid
    feats = "".join(f'<div class="feature-item"><div class="feature-icon">✓</div><span class="feature-text">{f}</span></div>' for f in n["feat"])
    html = re.sub(r'<div class="features-grid">.*?</div>\s*</div>\s*<div class="price-section">',
                  f'<div class="features-grid">{feats}</div>\n            </div>\n            <div class="price-section">', html, count=1, flags=re.S)

    # description overview
    html = html.replace("<p>Sam4s SAP-630-FT flat keyboard Android based Terminal. Needs software. CRS Dealer line required.</p>",
                        f"<p>{n['desc']}</p>")

    # specs table
    rows = "".join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in n["specs"])
    html = re.sub(r'<table class="specs-table">.*?</table>', f'<table class="specs-table">{rows}</table>', html, count=1, flags=re.S)

    out = os.path.join(MCD, n["slug"] + ".html")
    open(out, "w").write(html)
    print(f"✅ {n['slug']}.html  ({n['name']})")

print("\nDone.")
