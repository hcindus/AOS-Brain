#!/usr/bin/env python3
"""Generate editable .xlsx keyboard cover (Point Richmond Market) with grid in cells."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

C = {
    "fn":        ("4a4a4a", "ffffff"),
    "num":       ("2c5f8a", "ffffff"),
    "cash":      ("5a7d2a", "ffffff"),
    "breakfast": ("f4a460", "111111"),
    "bread":     ("d9b382", "111111"),
    "meat":      ("e08a7a", "111111"),
    "sandwich":  ("c96a6a", "ffffff"),
    "cheese":    ("f0e68c", "111111"),
    "salad":     ("9fd69f", "111111"),
    "side":      ("8fd0d0", "111111"),
    "extra":     ("d8a0c8", "111111"),
    "top":       ("b8a8d8", "111111"),
}

ROWS = [
    [("RF","fn"),("JF","fn"),("RECPT ON/OFF","fn"),
     ("BRICK YARD COVE","sandwich"),("FIRE HOUSE","sandwich"),("POINT RICH MOND","sandwich"),
     ("TRADITIONAL REUBEN","sandwich"),("MIMI","sandwich"),("R.J. INTERVENTION","sandwich"),
     ("NEW YORKER","sandwich"),("LITTLE ITALY","sandwich"),
     None,
     ("RECPT ISSUE","fn"),("NO SALE","fn"),("LOG ON/OFF","fn"),None],
    [("BREAK FAST","breakfast"),("ROLL","bread"),("MEATS","meat"),
     ("CHEVRON","sandwich"),("LITE ITALIAN","sandwich"),("TUNA MELT","sandwich"),
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

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Keyboard Cover"

thin = Side(style="thin", color="999999")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

# Title row
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=16)
tc = ws.cell(row=1, column=1, value="POINT RICHMOND MARKET  ·  MI PUEBLO RESTAURANT")
tc.font = Font(bold=True, size=13)
tc.alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[1].height = 28

for r, row in enumerate(ROWS, start=2):
    ws.row_dimensions[r].height = 34
    for c, cell in enumerate(row, start=1):
        xc = ws.cell(row=r, column=c)
        if cell is None:
            continue
        label, style = cell
        bg, fg = C[style]
        xc.value = label
        xc.fill = PatternFill("solid", fgColor=bg)
        xc.font = Font(size=9, bold=True, color=fg)
        xc.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        xc.border = border

for col in range(1, 17):
    ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 14

wb.save("manuals/cash-registers/recreated/point-richmond-market-cover.xlsx")
print("saved xlsx")
