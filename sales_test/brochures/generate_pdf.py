#!/usr/bin/env python3
"""
SIMPLE PDF BROCHURE GENERATOR (Fallback version)
Generates product brochures without full reportlab import path issues
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/sales_test')

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def generate_sample_brochure(output_path="/root/.openclaw/workspace/sales_test/brochures/output/sample_brochure.pdf"):
    """Generate a sample DataDepot brochure"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'], fontSize=28,
        textColor=colors.HexColor('#1a1a2e'), spaceAfter=30, alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'], fontSize=14,
        textColor=colors.HexColor('#4a4a6a'), alignment=TA_CENTER, spaceAfter=20
    )
    
    section_style = ParagraphStyle(
        'Section', parent=styles['Heading2'], fontSize=16,
        textColor=colors.HexColor('#1a1a2e'), spaceBefore=20, spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontSize=10,
        alignment=TA_JUSTIFY, spaceAfter=10
    )
    
    elements = []
    
    # Header
    elements.append(Paragraph("DataDepot Intelligence", title_style))
    elements.append(Paragraph("AI-Powered Restaurant Lead Generation", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Value Prop
    elements.append(Paragraph("Stop Cold Calling Blind", section_style))
    elements.append(Paragraph(
        "DataDepot Intelligence gives you verified, AI-analyzed leads for California restaurants "
        "with POS systems approaching end-of-life. Every lead includes system type, replacement timing, "
        "and owner contact information.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Pricing Table
    elements.append(Paragraph("Pricing", section_style))
    
    pricing_data = [
        ["Plan", "Leads/Month", "Price", "Best For"],
        ["Starter", "200", "$197/mo", "Small teams"],
        ["Professional", "500", "$297/mo", "Most Popular ★"],
        ["Enterprise", "1,000", "$497/mo", "Multi-territory"]
    ]
    
    pricing_table = Table(pricing_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 2.3*inch])
    pricing_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e6f3ff')),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold')
    ]))
    elements.append(pricing_table)
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph(
        "Cost per qualified lead: $0.59-0.99 (vs. $35-60 for traditional lead lists)",
        subtitle_style
    ))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # CTA
    elements.append(Paragraph(
        "Start Your Free Sample: psdepot.com/datadepot-sample",
        ParagraphStyle('CTA', parent=styles['Normal'], fontSize=12,
                      backColor=colors.HexColor('#0066cc'), textColor=colors.white,
                      borderPadding=12, alignment=TA_CENTER)
    ))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    elements.append(Paragraph(
        "Performance Supply Depot | 888-881-6834 | miles@psdepot.com | psdepot.com",
        subtitle_style
    ))
    
    doc.build(elements)
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING SAMPLE PDF BROCHURE")
    print("=" * 60)
    
    output = generate_sample_brochure()
    print(f"\n✅ Generated: {output}")
    
    # Also create a POS supplies version
    output2 = "/root/.openclaw/workspace/sales_test/brochures/output/pos_supplies_catalog.pdf"
    
    doc = SimpleDocTemplate(output2, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    elements = []
    
    elements.append(Paragraph("Performance Supply Depot", 
                              ParagraphStyle('Title', parent=styles['Heading1'], fontSize=28,
                                            textColor=colors.HexColor('#1a1a2e'), 
                                            alignment=TA_CENTER)))
    elements.append(Paragraph("POS Supplies Catalog 2026", 
                              ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14,
                                            alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.3*inch))
    
    # Thermal Paper
    elements.append(Paragraph("Thermal Receipt Paper", 
                           ParagraphStyle('Section', parent=styles['Heading2'], fontSize=16)))
    
    paper_data = [
        ["Product", "Size", "Qty/Case", "Price/Case"],
        ["Standard Thermal", '3 1/8" x 230\'', "50 rolls", "$69"],
        ["Compact Thermal", '2 1/4" x 85\'', "100 rolls", "$45"],
        ["BPA-Free Thermal", '3 1/8" x 230\'', "50 rolls", "$74"]
    ]
    
    t = Table(paper_data, colWidths=[2*inch, 1.5*inch, 1.2*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.3*inch))
    
    # CTA
    elements.append(Paragraph(
        "Order Now: psdepot.com | 888-881-6834",
        ParagraphStyle('CTA', parent=styles['Normal'], fontSize=12,
                      backColor=colors.HexColor('#28a745'), textColor=colors.white,
                      borderPadding=12, alignment=TA_CENTER)
    ))
    
    doc.build(elements)
    print(f"✅ Generated: {output2}")
    
    print("\n" + "=" * 60)