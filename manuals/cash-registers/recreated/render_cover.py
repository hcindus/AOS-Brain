#!/usr/bin/env python3
"""Render Point Richmond Market keyboard cover recreation to PNG."""
from PIL import Image, ImageDraw, ImageFont

# ---- palette (matching the HTML recreation) ----
C = {
    "fn":        ("#4a4a4a", "#ffffff"),
    "num":       ("#2c5f8a", "#ffffff"),
    "cash":      ("#5a7d2a", "#ffffff"),
    "breakfast": ("#f4a460", "#111111"),
    "bread":     ("#d9b382", "#111111"),
    "meat":      ("#e08a7a", "#111111"),
    "sandwich":  ("#c96a6a", "#ffffff"),
    "cheese":    ("#f0e68c", "#111111"),
    "salad":     ("#9fd69f", "#111111"),
    "side":      ("#8fd0d0", "#111111"),
    "extra":     ("#d8a0c8", "#111111"),
    "top":       ("#b8a8d8", "#111111"),
}

# key dimensions (3x for crisp render)
SCALE = 3
KW, KH, GAP = 46*SCALE, 34*SCALE, 3*SCALE
COLS = 16

# ---- grid data: each cell is (label, style) or None ----
# style '' => blank spacer
ROWS = [
    [("RF","fn"),("JF","fn"),("RECPT ON/OFF","fn"),
     ("BRICK YARD COVE","sandwich"),("FIRE HOUSE","sandwich"),("POINT RICH MOND","sandwich"),
     ("TRADITIONAL REUBEN","sandwich"),("MIMI","sandwich"),("R.J. INTERVENTION","sandwich"),
     ("NEW YORKER","sandwich"),("LITTLE ITALY","sandwich"),
     None,
     ("RECPT ISSUE","fn"),("NO SALE","fn"),("LOG ON/OFF","fn"),None],
    [("Burrito","breakfast"),("Taco","bread"),("Quesadilla","meat"),
     ("Asada","sandwich"),("Pastor","sandwich"),("Carnitas","sandwich"),
     ("CHICKEN SALAD","salad"),("BLT","sandwich"),("THE VEGGIE","sandwich"),
     ("HOT HONEY HAM","sandwich"),("ADD BACON","extra"),
     None,("ERROR CORR","fn"),("VOID ITEM","fn"),("MDSE RTRN","fn"),None],
    [("English Muffin","breakfast"),("Soft French","bread"),("Premium Ham","meat"),
     ("Roast Beef","meat"),("Cheddar","cheese"),("Monterey Jack","cheese"),
     ("FRESH SALAD","salad"),("CAESAR SALAD","salad"),("GREEK SALAD","salad"),
     ("THREE BEAN SALAD","salad"),("ADD AVOCADO","extra"),
     None,("DONE","fn"),("ENTER","fn"),("RECALL CHECK","fn"),None],
    [("Bagel","breakfast"),("Dutch Crunch","bread"),("Honey Ham","meat"),
     ("Corned Beef","meat"),("American","cheese"),("Muenster","cheese"),
     ("COLE SLAW","salad"),("POTATO SALAD","salad"),("PASTA ROMA","side"),
     ("CEVICHE","side"),("MACA RONI SALAD","side"),
     None,("↑","fn"),("CANCEL","fn"),("LIST CHECK","fn"),None],
    [("Bacon Egg & Cheese","breakfast"),("Sour dough roll","bread"),("Turkey Breast","meat"),
     ("Round Pastrami","meat"),("Swiss","cheese"),("PICKLE","extra"),
     ("ORZO","side"),("ASIAGO SALAD","side"),("TUNA SALAD","side"),
     ("CHICKEN SALAD","side"),("EGG SALAD","side"),
     None,("←","fn"),("↓","fn"),("→","fn"),("LIST PAID","fn")],
    [("Ham Egg & Cheese","breakfast"),("SLICED","bread"),("Cracked Pepper Turkey","meat"),
     ("Pastrami Brisket","meat"),("Provalone","cheese"),("DEVILED EGG","extra"),
     ("TABOULI","side"),("COUS COUS","side"),("REG HUMMUS","side"),
     ("ROAST PEPPER HUMMUS","side"),("BABA GHA NOUSH","side"),
     None,("@/FOR","fn"),("PLU","fn"),("CLEAR","fn"),None],
    [("Egg Cheese & Avocado","breakfast"),("French","bread"),("Mesquite Turkey","meat"),
     ("Liver Wurst","meat"),("Gouda","cheese"),("BOILED EGG","extra"),
     ("FALAFEL SAND WICH","sandwich"),("MED PLATE","sandwich"),None,None,None,
     None,("7","num"),("8","num"),("9","num"),None],
    [("Egg & Cheese","breakfast"),("Sour dough sliced","bread"),("Salsalito Turkey","meat"),
     ("Salami","meat"),("Havarti","cheese"),("DOLAMAS","extra"),
     None,None,None,None,("ADD BACON","extra"),
     None,("4","num"),("5","num"),("6","num"),None],
    [("Cream Cheese","breakfast"),("Light / Dark Rye","bread"),("Maple Glazed Turkey","meat"),
     None,("Horse radish Cheddar","cheese"),("ADD","extra"),
     ("NO","extra"),("EXTRA","extra"),("SIDE","extra"),None,("ADD AVOCADO","extra"),
     ("EXTRA MEAT","fn"),("1","num"),("2","num"),("3","num"),("SBTL","cash")],
    [("Toasted & Butter","breakfast"),("Wheat","bread"),("Buffalo Chicken","meat"),
     None,("Pepper Jack","cheese"),("Mayo","extra"),
     ("Mustard","extra"),("Tomato","extra"),("Onion","extra"),("Lettuce","extra"),("Pickle","extra"),
     ("Pepperoncini","extra"),("0","num"),("00","num"),(".","num"),("SEND","cash")],
]

def wrap(text, max_chars):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= max_chars:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    # hard-break long single words
    out = []
    for ln in lines:
        while len(ln) > max_chars:
            out.append(ln[:max_chars]); ln = ln[max_chars:]
        out.append(ln)
    return out

def fit_font(text, box_w, box_h, max_chars, max_size):
    """Return (font, lines) for the largest font that fits the box."""
    best = None
    for sz in range(max_size, 4, -1):
        f = font(sz, bold=True)
        lines = wrap(text, max_chars)
        # measure
        lh = 0
        w_ok = True
        for l in lines:
            bb = d.textbbox((0,0), l, font=f)
            w_ok = w_ok and (bb[2]-bb[0] <= box_w - 4)
            lh += bb[3]-bb[1]
        lh += (len(lines)-1)*1
        if w_ok and lh <= box_h - 4:
            return f, lines
    # fallback: smallest + min chars
    f = font(4, bold=True)
    return f, wrap(text, max_chars)

W = COLS*KW + (COLS+1)*GAP
H = len(ROWS)*KH + (len(ROWS)+1)*GAP
TITLE_H = 34*SCALE
img = Image.new("RGB", (W, H+TITLE_H), "#ffffff")
d = ImageDraw.Draw(img)

def font(sz, bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()

# title
tf = font(13*SCALE, bold=True)
tw = d.textlength("ALEJANDROS TAQUERIA  ·  TEST EDIT", font=tf)
d.text(((W-tw)/2, 8*SCALE), "ALEJANDROS TAQUERIA  ·  TEST EDIT", fill="#111111", font=tf)

for r, row in enumerate(ROWS):
    for c, cell in enumerate(row):
        if cell is None:
            continue
        label, style = cell
        x = GAP + c*(KW+GAP)
        y = TITLE_H + GAP + r*(KH+GAP)
        bg, fg = C[style]
        d.rounded_rectangle([x, y, x+KW, y+KH], radius=3, fill=bg, outline="#00000055", width=1)
        # auto-fit font to the key box
        f, lines = fit_font(label, KW, KH, 11, 9*SCALE)
        total_h = sum(d.textbbox((0,0), l, font=f)[3] for l in lines)
        ty = y + (KH - total_h)/2
        for l in lines:
            bb = d.textbbox((0,0), l, font=f)
            tw2 = bb[2]-bb[0]
            d.text((x + (KW-tw2)/2, ty), l, fill=fg, font=f)
            ty += bb[3]-bb[1] + 1

img.save("/tmp/cover-render.png")
print("saved /tmp/cover-render.png", img.size)
