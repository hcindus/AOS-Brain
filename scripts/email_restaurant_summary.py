#!/usr/bin/env python3
"""
Email Restaurant Lead Summary to PSDepot Team
Sends summary of imported customers to specified email addresses
"""

import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime

# Configuration
DB_PATH = "/root/.openclaw/workspace/data/depot_chaos/unified.db"

# Email recipients
RECIPIENTS = [
    "info@psdepot.com",
    "antonio.hudnall@gmail.com",
    "performancesupplydepot@gmail.com"
]

# SMTP Configuration (using Hostinger as per previous configs)
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 587
SMTP_USER = "miles@myl0nr0s.cloud"
SMTP_PASS = "Myl0n.R0s"

class EmailSender:
    def __init__(self):
        self.db_path = Path(DB_PATH)
        
    def get_customer_summary(self):
        """Get summary of customer data"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Total customers
        c.execute('SELECT COUNT(*) FROM customers')
        total = c.fetchone()[0]
        
        # By state
        c.execute('SELECT state, COUNT(*) FROM customers GROUP BY state ORDER BY COUNT(*) DESC')
        by_state = c.fetchall()
        
        # By business type
        c.execute('SELECT business_type, COUNT(*) FROM customers GROUP BY business_type ORDER BY COUNT(*) DESC LIMIT 10')
        by_type = c.fetchall()
        
        # By POS urgency
        c.execute('SELECT pos_urgency, COUNT(*) FROM customers WHERE pos_urgency IS NOT NULL GROUP BY pos_urgency ORDER BY COUNT(*) DESC')
        by_urgency = c.fetchall()
        
        # By region (CA only)
        c.execute('SELECT region, COUNT(*) FROM customers WHERE state="CA" AND region IS NOT NULL GROUP BY region ORDER BY COUNT(*) DESC')
        by_region = c.fetchall()
        
        # Sample high-priority leads
        c.execute('''
            SELECT company, city, state, business_type, pos_urgency, phone 
            FROM customers 
            WHERE pos_urgency = "High" OR priority = "A"
            LIMIT 10
        ''')
        high_priority = c.fetchall()
        
        conn.close()
        
        return {
            'total': total,
            'by_state': by_state,
            'by_type': by_type,
            'by_urgency': by_urgency,
            'by_region': by_region,
            'high_priority': high_priority
        }
    
    def format_email(self, data):
        """Format email content"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                h1 {{ color: #1a5276; }}
                h2 {{ color: #2874a6; border-bottom: 2px solid #2874a6; padding-bottom: 5px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
                th {{ background-color: #2874a6; color: white; padding: 10px; text-align: left; }}
                td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .highlight {{ background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; }}
                .total {{ font-size: 24px; font-weight: bold; color: #1a5276; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <h1>🍽️ Performance Supply Depot - Restaurant Lead Import</h1>
            <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
            
            <div class="highlight">
                <p class="total">{data['total']:,} Total Restaurant Leads</p>
                <p>Successfully imported into DepotChaos CRM</p>
            </div>
            
            <h2>📍 Leads by State</h2>
            <table>
                <tr><th>State</th><th>Count</th></tr>
        """
        
        for state, count in data['by_state']:
            html += f"<tr><td>{state}</td><td>{count:,}</td></tr>\n"
        
        html += """
            </table>
            
            <h2>🏢 Top Business Types</h2>
            <table>
                <tr><th>Type</th><th>Count</th></tr>
        """
        
        for btype, count in data['by_type']:
            html += f"<tr><td>{btype}</td><td>{count:,}</td></tr>\n"
        
        html += """
            </table>
            
            <h2>🚨 POS Urgency Distribution</h2>
            <table>
                <tr><th>Urgency</th><th>Count</th></tr>
        """
        
        for urgency, count in data['by_urgency']:
            html += f"<tr><td>{urgency}</td><td>{count:,}</td></tr>\n"
        
        html += """
            </table>
            
            <h2>🌟 California Regions</h2>
            <table>
                <tr><th>Region</th><th>Count</th></tr>
        """
        
        for region, count in data['by_region']:
            html += f"<tr><td>{region}</td><td>{count:,}</td></tr>\n"
        
        html += """
            </table>
            
            <h2>🔥 High Priority Sample Leads</h2>
            <table>
                <tr><th>Company</th><th>Location</th><th>Type</th><th>Urgency</th><th>Phone</th></tr>
        """
        
        for company, city, state, btype, urgency, phone in data['high_priority']:
            html += f"<tr><td>{company}</td><td>{city}, {state}</td><td>{btype}</td><td>{urgency}</td><td>{phone}</td></tr>\n"
        
        html += f"""
            </table>
            
            <h2>📁 File Locations</h2>
            <ul>
                <li>Master CSV: <code>/root/.openclaw/workspace/AGI_COMPANY/data/restaurants/</code></li>
                <li>DepotChaos DB: <code>{DB_PATH}</code></li>
                <li>Regional splits: <code>by_region/</code> and <code>by_city/</code> folders</li>
            </ul>
            
            <h2>🎯 PSDepot Value Proposition for Restaurants</h2>
            <ul>
                <li><strong>Reliable POS Supplies:</strong> Receipt paper, ribbons, kitchen printer paper</li>
                <li><strong>Printer Repair Services:</strong> On-site repair for receipt printers, kitchen printers, POS terminals</li>
                <li><strong>Cabling & Installation:</strong> Network cabling, POS terminal setup, kitchen display systems</li>
                <li><strong>Same-Day Shipping:</strong> Get supplies when you need them</li>
                <li><strong>Bulk Discounts:</strong> Special pricing for multi-location chains</li>
                <li><strong>24/7 Support:</strong> Because restaurants never sleep</li>
                <li><strong>Payment Processing:</strong> Terminals, card readers, accessories</li>
            </ul>
            
            <h2>📞 Next Steps</h2>
            <ol>
                <li>Review high-priority leads (High POS Urgency)</li>
                <li>Assign sales reps by region/state</li>
                <li>Launch targeted email campaigns</li>
                <li>Track responses in DepotChaos CRM</li>
            </ol>
            
            <div class="footer">
                <p>Performance Supply Depot LLC | <a href="https://psdepot.com">psdepot.com</a></p>
                <p>Generated by Miles - AGI Company Autonomous Operations Engine</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email(self):
        """Send email to all recipients"""
        # Get data
        data = self.get_customer_summary()
        html_content = self.format_email(data)
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🍽️ PSDepot Restaurant Leads: {data['total']:,} Customers Imported"
        msg['From'] = SMTP_USER
        msg['To'] = ", ".join(RECIPIENTS)
        
    msg["Bcc"] = "info@psdepot.com"
        # Attach HTML
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, RECIPIENTS, msg.as_string())
            server.quit()
            print(f"✅ Email sent to: {', '.join(RECIPIENTS)}")
            return True
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("EMAILING RESTAURANT LEAD SUMMARY")
    print("=" * 60)
    print()
    
    sender = EmailSender()
    success = sender.send_email()
    
    if success:
        print()
        print("✅ Summary email delivered successfully!")
        print("   Recipients:")
        for r in RECIPIENTS:
            print(f"   • {r}")
    else:
        print()
        print("⚠️ Email delivery failed. Check SMTP credentials.")
