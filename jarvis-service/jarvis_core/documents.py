#!/usr/bin/env python3
"""PDF quote & invoice generator (reportlab) — the "invoice engine"."""
import os
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER

BRAND = "#0A1A2F"       # deep tech blue
ACCENT = "#FF7A00"      # performance orange
COMPANY = "Performance Supply Depot LLC"
PHONE = "(888) 881-6834"
EMAIL = "info@psdepot.com"

OUT_DIR = os.environ.get("JARVIS_OUT", "/var/lib/psdepot/documents")


def _styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle("Company", parent=s["Normal"], fontName="Helvetica-Bold",
                         fontSize=18, textColor=colors.HexColor(BRAND)))
    s.add(ParagraphStyle("DocTitle", parent=s["Normal"], fontName="Helvetica-Bold",
                         fontSize=26, textColor=colors.HexColor(BRAND), spaceAfter=4))
    s.add(ParagraphStyle("Right", parent=s["Normal"], alignment=TA_RIGHT, fontSize=9))
    s.add(ParagraphStyle("Center", parent=s["Normal"], alignment=TA_CENTER, fontSize=9))
    s.add(ParagraphStyle("H3", parent=s["Normal"], fontName="Helvetica-Bold",
                         fontSize=11, textColor=colors.HexColor(BRAND), spaceBefore=10, spaceAfter=4))
    return s


def _line_items(items):
    """items: list of (description, qty, unit_price)."""
    rows = [["Description", "Qty", "Unit", "Amount"]]
    for desc, qty, price in items:
        rows.append([desc, str(qty), f"${price:,.2f}", f"${qty * price:,.2f}"])
    return rows


class _Document:
    def __init__(self, kind: str, lead: dict, items: list, terms: str, notes: str = ""):
        self.kind = kind  # "QUOTE" or "INVOICE"
        self.lead = lead
        self.items = items
        self.terms = terms
        self.notes = notes
        self.total = sum(qty * price for _, qty, price in items)

    def build(self, out_path: str) -> str:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        doc = SimpleDocTemplate(out_path, pagesize=LETTER,
                                leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                                topMargin=0.7 * inch, bottomMargin=0.7 * inch)
        st = _styles()
        story = []

        # Header
        story.append(Paragraph(COMPANY, st["Company"]))
        story.append(Paragraph(f"<font color='{ACCENT}'>{self.kind}</font>", st["DocTitle"]))
        story.append(Paragraph(f"{PHONE} · {EMAIL}", st["Right"]))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor(ACCENT)))

        # Bill-to
        story.append(Paragraph("Bill To", st["H3"]))
        story.append(Paragraph(self.lead.get("name", ""), st["Normal"]))
        if self.lead.get("business"):
            story.append(Paragraph(self.lead.get("business"), st["Normal"]))
        contact = " · ".join(x for x in [self.lead.get("phone"), self.lead.get("email")] if x)
        if contact:
            story.append(Paragraph(contact, st["Normal"]))
        story.append(Spacer(1, 10))

        # Meta
        meta = [
            [f"{self.kind.title()} #", f"J-{datetime.now().strftime('%Y%m%d')}-{self.lead.get('id','?')}"],
            ["Date", datetime.now().strftime("%B %d, %Y")],
        ]
        story.append(Table(meta, colWidths=[1.2 * inch, 4 * inch]))
        story.append(Spacer(1, 14))

        # Line items
        table = Table(_line_items(self.items), colWidths=[3.0 * inch, 0.6 * inch, 0.9 * inch, 1.1 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BRAND)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(table)

        # Total
        total_row = [["", "", "TOTAL", f"${self.total:,.2f}"]]
        t = Table(total_row, colWidths=[3.0 * inch, 0.6 * inch, 0.9 * inch, 1.1 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 14))

        # Terms
        if self.terms:
            story.append(Paragraph("Terms", st["H3"]))
            story.append(Paragraph(self.terms, st["Normal"]))
        if self.notes:
            story.append(Paragraph("Notes", st["H3"]))
            story.append(Paragraph(self.notes, st["Normal"]))

        doc.build(story)
        return out_path


class QuoteEngine:
    DEFAULT_TERMS = "50% deposit to book the build slot; remaining 50% due on delivery."

    def generate(self, lead: dict, items: list, out_dir: str = OUT_DIR,
                 terms: str = DEFAULT_TERMS, notes: str = "") -> str:
        fname = f"quote-{lead.get('id','new')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
        return _Document("QUOTE", lead, items, terms, notes).build(os.path.join(out_dir, fname))


class InvoiceEngine:
    DEFAULT_TERMS = "Payment due within 15 days of invoice date."

    def generate(self, lead: dict, items: list, out_dir: str = OUT_DIR,
                 terms: str = DEFAULT_TERMS, notes: str = "") -> str:
        fname = f"invoice-{lead.get('id','new')}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf"
        return _Document("INVOICE", lead, items, terms, notes).build(os.path.join(out_dir, fname))
