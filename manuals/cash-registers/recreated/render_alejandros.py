#!/usr/bin/env python3
"""Render Alejandros Taqueria keyboard cover (Mexican taqueria template)."""
from PIL import Image, ImageDraw, ImageFont

C = {
    "fn":      ("#4a4a4a", "#ffffff"),
    "num":     ("#2c5f8a", "#ffffff"),
    "cash":    ("#5a7d2a", "#ffffff"),
    "plate":   ("#c96a6a", "#ffffff"),  # preset plates/sandwiches
    "extra":   ("#d8a0c8", "#111111"),  # add-ons
    "taco":    ("#f4a460", "#111111"),  # tacos/burritos
    "mariscos":("#8fd0d0", "#111111"),  # seafood
    "bebida":  ("#9fd69f", "#111111"),  # drinks
    "side":    ("#f0e68c", "#111111"),  # sides
}

SCALE = 3
KW, KH, GAP = 48*SCALE, 34*SCALE, 3*SCALE
COLS = 15

ROWS = [
    # top function + preset plates
    [("RF","fn"),("JF","fn"),("RECPT ON/OFF","fn"),
     ("BURRITO","plate"),("SUPER","plate"),("VEGGIE","plate"),
     ("MOJADO","plate"),("CHIMI-","plate"),("CHANGA","plate"),
     ("SHRIMP","plate"),("BURRITO","plate"),("SUPER","plate"),("SHRIMP","plate"),
     ("RECPT ISSUE","fn"),("NO SALE","fn")],
    [("LOG ON/OFF","fn"),("ERROR CORR","fn"),("VOID ITEM","fn"),
     ("REGULAR","plate"),("BURRITO","plate"),("BURRITO","plate"),
     ("",None),("",None),("",None),
     ("",None),("",None),("",None),("",None),
     ("MDSE RTRN","fn"),("LOG ON/OFF","fn")],
    # extras column + menu
    [("EXTRA","extra"),("MEAT","extra"),("EXTRA","extra"),
     ("QUESO","extra"),("EXTRA","extra"),("CREMA","extra"),
     ("EXTRA","extra"),("GUAC","extra"),("ORDER","extra"),("GUAC","extra"),
     ("RICE &","side"),("BEANS","side"),("LUNCH","side"),("SPECIAL","side"),
     ("DONE","fn"),("ENTER","fn")],
    [("TACO","taco"),("TACO","taco"),("SALAD","taco"),
     ("TACO","taco"),("VEG","taco"),("SUPER","taco"),("TACO","taco"),
     ("FISH","taco"),("TACO","taco"),("FLAUTAS","taco"),
     ("NACHOS","taco"),("VEG","taco"),("NACHOS","taco"),("MEAT","taco"),
     ("CANCEL","fn"),("RECALL","fn")],
    [("QUESA-","taco"),("DILLA","taco"),("QUESA-","taco"),("DILLA","taco"),("MEAT","taco"),
     ("SUPER","taco"),("QUESA","taco"),("SHRIMP","taco"),("QUESA","taco"),
     ("TAMAL","taco"),("TORTA","taco"),("CALDO","taco"),
     ("DESAYUNO","taco"),("",None),
     ("LIST","fn"),("CHECK","fn")],
    [("CARNE","taco"),("ASADA","taco"),("MOJARRA","mariscos"),
     ("MENUDO","taco"),("BIRRIA","taco"),("CHILE","taco"),("RELLENO","taco"),
     ("CHILE","taco"),("VERDE","taco"),("ENCHI-","taco"),("LADAS","taco"),
     ("FAJITA","taco"),("FAJITA","taco"),("MIXTA","taco"),
     ("7","num"),("8","num")],
    [("CAMARONES","mariscos"),("RANCHEROS","mariscos"),("CAMARONES","mariscos"),
     ("DIABLA","mariscos"),("CAMARONES","mariscos"),("AJO","mariscos"),
     ("CAMARONES","mariscos"),("EMPANIZADO","mariscos"),("7","mariscos"),("MARES","mariscos"),
     ("TOSTADA","mariscos"),("CEVICHE","mariscos"),("COCTEL","mariscos"),("MED","mariscos"),
     ("4","num"),("5","num")],
    [("COCTEL","mariscos"),("GRANDE","mariscos"),("OSTIONES","mariscos"),
     ("MEX","bebida"),("SODA","bebida"),("FOUNT","bebida"),("SODA","bebida"),
     ("AGUA","bebida"),("FRESCA","bebida"),("LARGE","bebida"),("SODA","bebida"),
     ("LARGE","bebida"),("JUGO","bebida"),("SMALL","bebida"),("SODA","bebida"),
     ("1","num"),("2","num")],
    [("JUGO","bebida"),("CAN","bebida"),("SODA","bebida"),("CAFE","bebida"),
     ("",None),("",None),("",None),("",None),("",None),("",None),
     ("",None),("",None),("",None),("",None),
     ("3","num"),("SBTL","cash")],
    [("",None),("",None),("",None),("",None),("",None),("",None),("",None),("",None),
     ("",None),("",None),("",None),("",None),("",None),("",None),
     ("0","num"),("SEND","cash")],
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
    out = []
    for ln in lines:
        while len(ln) > max_chars:
            out.append(ln[:max_chars]); ln = ln[max_chars:]
        out.append(ln)
    return out

W = COLS*KW + (COLS+1)*GAP
H = len(ROWS)*KH + (len(ROWS)+1)*GAP
TITLE_H = 34*SCALE
img = Image.new("RGB", (W, H+TITLE_H), "#ffffff")
d = ImageDraw.Draw(img)

def font(sz, bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()

tf = font(13*SCALE, True)
tw = d.textlength("ALEJANDROS TAQUERIA", font=tf)
d.text(((W-tw)/2, 8*SCALE), "ALEJANDROS TAQUERIA", fill="#111111", font=tf)

def fit_font(label, box_w, box_h, max_chars, max_size):
    for sz in range(max_size, 4, -1):
        f = font(sz, True)
        lines = wrap(label, max_chars)
        lh = 0; ok = True
        for l in lines:
            bb = d.textbbox((0,0), l, font=f)
            ok = ok and (bb[2]-bb[0] <= box_w-4)
            lh += bb[3]-bb[1]
        lh += (len(lines)-1)*1
        if ok and lh <= box_h-4:
            return f, lines
    return font(4, True), wrap(label, max_chars)

for r, row in enumerate(ROWS):
    for c, cell in enumerate(row):
        if cell is None or cell[0] == "":
            continue
        label, style = cell
        x = GAP + c*(KW+GAP)
        y = TITLE_H + GAP + r*(KH+GAP)
        bg, fg = C[style]
        d.rounded_rectangle([x, y, x+KW, y+KH], radius=3, fill=bg, outline="#00000055", width=1)
        f, lines = fit_font(label, KW, KH, 10, 9*SCALE)
        total_h = sum(d.textbbox((0,0), l, font=f)[3] for l in lines)
        ty = y + (KH-total_h)/2
        for l in lines:
            bb = d.textbbox((0,0), l, font=f)
            d.text((x + (KW-(bb[2]-bb[0]))/2, ty), l, fill=fg, font=f)
            ty += bb[3]-bb[1] + 1

out = "/root/.openclaw/workspace/manuals/cash-registers/recreated/alejandros-taqueria-cover.png"
img.save(out)
print("saved", out, img.size)
