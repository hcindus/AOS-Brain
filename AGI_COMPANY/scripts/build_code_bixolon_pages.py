#!/usr/bin/env python3
"""Replace the 4 recycled printer pages with Code scanners + Bixolon printers."""
import os, re, shutil

MCD = "/var/www/psdepot.com/products/mscashdrawer"
TMPL = os.path.join(MCD, "sam4s-sap-630-ft-flat-keyboard-android-terminal.html")
ARCHIVE = os.path.join(MCD, "_archive")

# old printer pages to replace (keep ASTRA Android kiosk)
OLD = [
    "sam4s-gcube-receipt-printer",
    "sam4s-ellix40ii-receipt-printer",
    "sam4s-giant-100-receipt-printer",
    "sam4s-hcube-receipt-printer",
]

NEW = [
    dict(slug="code-cr950-barcode-scanner", name="Code CR950 Barcode Scanner",
         sku="PSD-CODE-CR950", sub="Code Barcode Scanners", img="CR950-frontleft-400x582-1.png",
         feat=["1D + 2D omnidirectional","Reads mobile device screens","LED + audible feedback","Manual or auto trigger"],
         desc="The Code CR950 is an aggressive barcode reader that rapidly decodes 1D and 2D barcodes. Lightweight, ergonomic design for long shifts, with unmatched durability and efficient power consumption.",
         specs=[("Type","Handheld barcode scanner"),("Reading","1D + 2D (omnidirectional)"),
                ("Trigger","Manual or automatic"),("Feedback","LED + audible tone"),
                ("Extras","Mobile screen reading, driver license parsing")]),
    dict(slug="code-cr2515-barcode-scanner", name="Code CR2515 Barcode Scanner",
         sku="PSD-CODE-CR2515", sub="Code Barcode Scanners", img=None,
         feat=["1D + 2D barcode reading","Ergonomic handheld","USB / RS232 options","Commercial grade"],
         desc="The Code CR2515 is a commercial-grade handheld barcode scanner from Code Corporation, decoding 1D and 2D barcodes for retail and point-of-sale environments.",
         specs=[("Type","Handheld barcode scanner"),("Reading","1D + 2D"),
                ("Interfaces","USB / RS232"),("Brand","Code Corporation")]),
    dict(slug="bixolon-srp-350plusv-thermal-printer", name="Bixolon SRP-350Plus V Thermal Printer",
         sku="PSD-BIXOLON-SRP350V", sub="Bixolon Receipt Printers", img=None,
         feat=["400 mm/sec printing","180 / 203 dpi","Paper save mode","Blue4est® ready"],
         desc="The Bixolon SRP-350Plus V is a premium 3-inch (80mm) thermal printer supporting fast printing up to 400 mm/sec at 180 dpi. Includes paper-save mode and Visibility Intelligence™ for optimal quality on Blue4est® paper.",
         specs=[("Type","3\" (80mm) thermal receipt printer"),("Speed","Up to 400 mm/sec"),
                ("Resolution","180 / 203 dpi"),("Extras","Paper save mode, Visibility Intelligence")]),
    dict(slug="bixolon-srp-275iii-impact-printer", name="Bixolon SRP-275III Impact Printer",
         sku="PSD-BIXOLON-SRP275III", sub="Bixolon Receipt Printers", img="SRP-275III.png",
         feat=["3\" impact dot matrix","5.1 lps (40 col)","Two-color printing","Anti-jam + kitchen buzzer"],
         desc="The Bixolon SRP-275III is a 3-inch impact dot-matrix receipt printer, ideal for hospitality. Compact, cost-efficient, and space-saving with two-color printing and an internal kitchen buzzer.",
         specs=[("Type","3\" impact dot-matrix printer"),("Speed","Up to 5.1 lps (40 columns)"),
                ("Reliability","18 million lines"),("Extras","Two-color, anti-jam, kitchen buzzer"),
                ("Mount","Stand-alone + wall-mount")]),
]

base = open(TMPL).read()

for old in OLD:
    src = os.path.join(MCD, old + ".html")
    if os.path.exists(src):
        shutil.move(src, os.path.join(ARCHIVE, old + ".html"))
        print(f"  archived {old}.html")

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

    feats = "".join(f'<div class="feature-item"><div class="feature-icon">✓</div><span class="feature-text">{f}</span></div>' for f in n["feat"])
    html = re.sub(r'<div class="features-grid">.*?</div>\s*</div>\s*<div class="price-section">',
                  f'<div class="features-grid">{feats}</div>\n            </div>\n            <div class="price-section">', html, count=1, flags=re.S)
    html = html.replace("<p>Sam4s SAP-630-FT flat keyboard Android based Terminal. Needs software. CRS Dealer line required.</p>",
                        f"<p>{n['desc']}</p>")
    rows = "".join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in n["specs"])
    html = re.sub(r'<table class="specs-table">.*?</table>', f'<table class="specs-table">{rows}</table>', html, count=1, flags=re.S)

    out = os.path.join(MCD, n["slug"] + ".html")
    open(out, "w").write(html)
    print(f"✅ {n['slug']}.html  ({n['name']})")

print("Done.")
