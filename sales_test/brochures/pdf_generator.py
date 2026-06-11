"""
PDF BROCHURE GENERATOR
Creates product brochures for POS Supplies and DataDepot
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

class BrochureGenerator:
    """Generates professional PDF brochures for AGI Company products"""
    
    def __init__(self, output_dir="/root/.openclaw/workspace/sales_test/brochures/output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#4a4a6a'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a2e'),
            spaceBefore=20,
            spaceAfter=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='ProductName',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#16213e'),
            spaceBefore=12,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='Body',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='Callout',
            parent=self.styles['Normal'],
            fontSize=11,
            backColor=colors.HexColor('#f0f0f5'),
            borderPadding=10,
            spaceBefore=15,
            spaceAfter=15
        ))
        
        self.styles.add(ParagraphStyle(
            name='Price',
            parent=self.styles['Normal'],
            fontSize=24,
            textColor=colors.HexColor('#28a745'),
            alignment=TA_CENTER,
            spaceBefore=10,
            spaceAfter=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='CTA',
            parent=self.styles['Normal'],
            fontSize=12,
            backColor=colors.HexColor('#0066cc'),
            textColor=colors.white,
            borderPadding=12,
            alignment=TA_CENTER,
            spaceBefore=20,
            spaceAfter=20
        ))
    
    def generate_datadepot_brochure(self, customer_name=None, territory=None, filename=None):
        """
        Generate DataDepot Intelligence brochure
        
        Args:
            customer_name: Optional customer name for personalization
            territory: Optional territory for specific data
            filename: Output filename
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"datadepot_brochure_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        elements = []
        
        # Header
        elements.append(Paragraph("DataDepot Intelligence", self.styles['Title']))
        elements.append(Paragraph("AI-Powered Restaurant Lead Generation", self.styles['Subtitle']))
        
        if customer_name:
            elements.append(Paragraph(f"Prepared for: {customer_name}", self.styles['Subtitle']))
        
        if territory:
            elements.append(Paragraph(f"Territory: {territory}", self.styles['Subtitle']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Value Proposition
        elements.append(Paragraph("Stop Cold Calling Blind", self.styles['SectionHeader']))
        elements.append(Paragraph(
            "DataDepot Intelligence gives you verified, AI-analyzed leads for California restaurants "
            "with POS systems approaching end-of-life. Every lead includes system type, replacement timing, "
            "and owner contact information.",
            self.styles['Body']
        ))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # How It Works
        elements.append(Paragraph("How It Works", self.styles['SectionHeader']))
        
        how_it_works = [
            ["1. AI Detection", "Our computer vision identifies POS systems in restaurant photos"],
            ["2. Timing Score", "Machine learning predicts replacement likelihood (0-100)"],
            ["3. Review Analysis", "NLP extracts sentiment about current POS systems"],
            ["4. Verified Contacts", "We validate owner/GM contact information monthly"],
            ["5. Weekly Delivery", "Fresh leads delivered to your inbox every Monday"]
        ]
        
        how_table = Table(how_it_works, colWidths=[1.5*inch, 5*inch])
        how_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f5')),
        ]))
        elements.append(how_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Data Points
        elements.append(Paragraph("What's Included", self.styles['SectionHeader']))
        
        data_points = [
            ["Data Point", "Description", "Updated"],
            ["POS System Type", "Aloha, Square, Toast, Clover, Micros, etc.", "Weekly"],
            ["Replacement Score", "0-100 likelihood of replacement need", "Daily"],
            ["Equipment Age", "Estimated years since installation", "Weekly"],
            ["Review Sentiment", "POS-related review mentions analyzed", "Weekly"],
            ["Owner/GM Contact", "Verified phone, email, name", "Monthly"],
            ["Location Details", "Address, hours, cuisine type, seating", "Weekly"],
            ["License Renewal", "Equipment lease expiration dates", "Quarterly"]
        ]
        
        data_table = Table(data_points, colWidths=[1.8*inch, 3.2*inch, 1.5*inch])
        data_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        elements.append(data_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Pricing
        elements.append(Paragraph("Pricing", self.styles['SectionHeader']))
        
        pricing_data = [
            ["Plan", "Leads/Month", "Price", "Best For"],
            ["Starter", "200", "$197/mo", "Small teams testing the system"],
            ["Professional", "500", "$297/mo", "Growing sales teams (Most Popular)"],
            ["Enterprise", "1,000", "$497/mo", "Multi-territory operations"]
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
        
        # Cost comparison
        elements.append(Paragraph(
            "Cost per qualified lead: $0.59-0.99 (vs. $35-60 for traditional lead lists)",
            self.styles['Subtitle']
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # ROI Example
        elements.append(Paragraph("ROI Example", self.styles['SectionHeader']))
        
        roi_text = """
        <b>Scenario:</b> Professional tier ($297/mo) generates 500 qualified leads<br/>
        <b>Close Rate:</b> 15% (industry average with warm leads)<br/>
        <b>Deals Closed:</b> 75 deals<br/>
        <b>Average Deal Value:</b> $5,000<br/>
        <b>Monthly Revenue:</b> $375,000<br/>
        <b>Cost:</b> $297<br/>
        <b>ROI:</b> 126,000%
        """
        elements.append(Paragraph(roi_text, self.styles['Callout']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Guarantee
        elements.append(Paragraph(
            "30-Day Money-Back Guarantee • Cancel Anytime • No Contracts",
            self.styles['Subtitle']
        ))
        
        # CTA
        elements.append(Paragraph(
            "Start Your Free Sample: psdepot.com/datadepot-sample",
            self.styles['CTA']
        ))
        
        # Footer
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(
            "Performance Supply Depot | 888-881-6834 | miles@psdepot.com | psdepot.com",
            self.styles['Subtitle']
        ))
        
        # Build PDF
        doc.build(elements)
        print(f"✅ Generated DataDepot brochure: {filepath}")
        return filepath
    
    def generate_pos_supplies_brochure(self, customer_name=None, filename=None):
        """
        Generate POS Supplies catalog brochure
        
        Args:
            customer_name: Optional customer name for personalization
            filename: Output filename
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pos_supplies_catalog_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        elements = []
        
        # Header
        elements.append(Paragraph("Performance Supply Depot", self.styles['Title']))
        elements.append(Paragraph("POS Supplies Catalog 2026", self.styles['Subtitle']))
        
        if customer_name:
            elements.append(Paragraph(f"Prepared for: {customer_name}", self.styles['Subtitle']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Thermal Paper Section
        elements.append(Paragraph("Thermal Receipt Paper", self.styles['SectionHeader']))
        
        paper_data = [
            ["Product", "Size", "Qty/Case", "Price/Case", "Price/Roll"],
            ["Standard Thermal", '3 1/8" x 230\'', "50 rolls", "$69", "$1.38"],
            ["Compact Thermal", '2 1/4" x 85\'', "100 rolls", "$45", "$0.45"],
            ["Heavy-Duty Thermal", '3 1/8" x 273\'', "50 rolls", "$79", "$1.58"],
            ["BPA-Free Thermal", '3 1/8" x 230\'', "50 rolls", "$74", "$1.48"]
        ]
        
        paper_table = Table(paper_data, colWidths=[2*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        paper_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        elements.append(paper_table)
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            "Same-day shipping from California • No minimum orders • OEM-grade quality",
            self.styles['Body']
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # POS Systems Section
        elements.append(Paragraph("POS Systems & Hardware", self.styles['SectionHeader']))
        
        pos_data = [
            ["System", "Type", "Price", "Best For"],
            ["SAM4s ER-260", "Cash Register", "$495", "Small cafes, food trucks"],
            ["SAM4s ER-940", "All-in-One POS", "$1,295", "Full-service restaurants"],
            ["SAM4s SAP-630", "Tablet POS", "$895", "Quick service, cafes"],
            ["Clover Mini", "Cloud POS", "$799", "Retail + food hybrid"],
            ["Square Terminal", "Mobile POS", "$299", "Mobile vendors, events"]
        ]
        
        pos_table = Table(pos_data, colWidths=[2*inch, 1.5*inch, 1.2*inch, 2*inch])
        pos_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        elements.append(pos_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Services Section
        elements.append(Paragraph("Services", self.styles['SectionHeader']))
        
        services_data = [
            ["Service", "Rate", "Description"],
            ["Printer Repair", "$195/hour", "On-site diagnosis and repair of POS printers"],
            ["Network Cabling", "$180/hour", "Professional installation and troubleshooting"],
            ["POS Setup", "$150/hour", "System configuration and staff training"],
            ["Emergency Support", "$250/hour", "24/7 after-hours support"]
        ]
        
        services_table = Table(services_data, colWidths=[2*inch, 1.2*inch, 3.5*inch])
        services_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6c757d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        elements.append(services_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Why Choose Us
        elements.append(Paragraph("Why Restaurants Choose Performance Supply Depot", self.styles['SectionHeader']))
        
        why_us = """
        <b>Same-Day Delivery</b> — Order by 2 PM, deliver today (California)<br/>
        <b>No Minimum Orders</b> — Order 1 case or 100, we'll ship it<br/>
        <b>Price Match Guarantee</b> — We'll beat any competitor's price<br/>
        <b>24/7 Support</b> — Call anytime: 888-881-6834<br/>
        <b>30-Day Returns</b> — No questions asked
        """
        elements.append(Paragraph(why_us, self.styles['Callout']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # DataDepot Cross-Sell
        elements.append(Paragraph("Also Available: DataDepot Intelligence", self.styles['SectionHeader']))
        
        elements.append(Paragraph(
            "Get 500 verified California restaurant leads monthly with AI-detected POS system data. "
            "Perfect for growing your customer base. $297/month.",
            self.styles['Body']
        ))
        
        elements.append(Paragraph(
            "Learn more: psdepot.com/datadepot",
            self.styles['CTA']
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        elements.append(Paragraph(
            "Performance Supply Depot | 888-881-6834 | miles@psdepot.com | psdepot.com",
            self.styles['Subtitle']
        ))
        
        # Build PDF
        doc.build(elements)
        print(f"✅ Generated POS Supplies brochure: {filepath}")
        return filepath
    
    def generate_combined_brochure(self, customer_name=None, territory=None, filename=None):
        """Generate a combined brochure with both DataDepot and POS Supplies"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"psdepot_full_catalog_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        elements = []
        
        # Cover Page
        elements.append(Paragraph("Performance Supply Depot", self.styles['Title']))
        elements.append(Paragraph("Complete Solutions for POS Professionals", self.styles['Subtitle']))
        
        if customer_name:
            elements.append(Spacer(1, 0.5*inch))
            elements.append(Paragraph(f"Prepared exclusively for:", self.styles['Subtitle']))
            elements.append(Paragraph(f"{customer_name}", self.styles['SectionHeader']))
        
        elements.append(Spacer(1, 0.5*inch))
        
        cover_text = """
        <b>Two Solutions. One Partner.</b><br/><br/>
        ✓ POS Supplies — Thermal paper, systems, services<br/>
        ✓ DataDepot Intelligence — AI-powered lead generation<br/><br/>
        Everything you need to run and grow your POS business.
        """
        elements.append(Paragraph(cover_text, self.styles['Callout']))
        
        elements.append(PageBreak())
        
        # DataDepot Page
        elements.append(Paragraph("DataDepot Intelligence", self.styles['SectionHeader']))
        elements.append(Paragraph(
            "AI-powered lead generation for POS vendors. 500 verified California restaurant leads monthly.",
            self.styles['Body']
        ))
        
        dd_pricing = [
            ["Plan", "Leads/Month", "Price"],
            ["Starter", "200", "$197/mo"],
            ["Professional", "500", "$297/mo ★"],
            ["Enterprise", "1,000", "$497/mo"]
        ]
        
        dd_table = Table(dd_pricing, colWidths=[2*inch, 2*inch, 2*inch])
        dd_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e6f3ff')),
        ]))
        elements.append(dd_table)
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            "Every lead includes: POS system type, replacement score, review sentiment, owner contact",
            self.styles['Body']
        ))
        
        elements.append(PageBreak())
        
        # POS Supplies Page
        elements.append(Paragraph("POS Supplies & Services", self.styles['SectionHeader']))
        
        pos_pricing = [
            ["Product", "Price", "Ships"],
            ["Thermal Paper (3 1/8\")", "$69/case", "Same Day"],
            ["SAM4s ER-260", "$495", "2-3 Days"],
            ["Printer Repair", "$195/hr", "On-Site"],
            ["Network Cabling", "$180/hr", "Scheduled"]
        ]
        
        pos_table = Table(pos_pricing, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        pos_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(pos_table)
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            "Full catalog available at psdepot.com/catalog",
            self.styles['Body']
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # CTA
        elements.append(Paragraph(
            "Start Today: psdepot.com | 888-881-6834 | miles@psdepot.com",
            self.styles['CTA']
        ))
        
        # Build PDF
        doc.build(elements)
        print(f"✅ Generated combined brochure: {filepath}")
        return filepath

# Export
__all__ = ['BrochureGenerator']

if __name__ == "__main__":
    # Test generation
    gen = BrochureGenerator()
    
    print("\n" + "=" * 60)
    print("GENERATING PDF BROCHURES")
    print("=" * 60 + "\n")
    
    gen.generate_datadepot_brochure(
        customer_name="Alex Johnson",
        territory="Los Angeles County"
    )
    
    gen.generate_pos_supplies_brochure(
        customer_name="Alex Johnson"
    )
    
    gen.generate_combined_brochure(
        customer_name="Alex Johnson",
        territory="Los Angeles County"
    )
    
    print("\n" + "=" * 60)
    print("BROCHURE GENERATION COMPLETE")
    print("=" * 60)