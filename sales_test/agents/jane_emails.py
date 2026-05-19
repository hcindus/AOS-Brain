"""
JANE - Customer Nurturer
Post-sale follow-up, retention, upselling
4 emails in sequence
"""

JANE_EMAILS = [
    {
        "id": "jane_01_checkin",
        "name": "30-Day Check-in",
        "agent": "Jane",
        "stage": "retention",
        "subject": "How are those {{County}} leads working out, {{First_Name}}?",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>It's been about a month since you started with DataDepot. Just wanted to check in.</p>
        
        <p><strong>Quick questions:</strong></p>
        <ul>
        <li>How many calls have you made from the {{County}} list?</li>
        <li>Any closed deals yet?</li>
        <li>Running into any issues with the data?</li>
        </ul>
        
        <p><strong>What I'm hearing from other customers:</strong></p>
        <ul>
        <li>Week 1-2: Learning curve on the scoring system</li>
        <li>Week 3-4: First deals start closing</li>
        <li>Month 2-3: Consistent pipeline from weekly refreshes</li>
        </ul>
        
        <p>Most customers tell me the first 500 leads are where you learn the system. The real ROI kicks in at month 2+ when you get into the rhythm.</p>
        
        <p><a href="https://calendly.com/psdepot-jane/15min" style="background: #6c757d; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Schedule a Check-in Call</a></p>
        
        <p>-Jane<br>
        Customer Success, Performance Supply Depot</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — If you're not seeing results yet, let's troubleshoot. Reply with your biggest challenge.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "County"],
        "cta": "Schedule check-in call",
        "follow_up_days": 7
    },
    {
        "id": "jane_02_upsell",
        "name": "Upsell to Enterprise",
        "agent": "Jane",
        "stage": "upsell",
        "subject": "You're crushing it — ready for more leads?",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Saw you've been active in DataDepot — {{Calls_Made}} calls logged. Nice work!</p>
        
        <p><strong>Quick question:</strong> Are you running out of leads before the month ends?</p>
        
        <p>Most Professional customers (500 leads/month) tell me the same thing: <em>"I run out of A-grade prospects by week 3."</em></p>
        
        <p><strong>Solution: Enterprise tier</strong></p>
        <ul>
        <li>1,000 leads/month instead of 500</li>
        <li>Access to adjacent counties ({{Adjacent_Counties}})</li>
        <li>Priority support + custom filters</li>
        <li>Price: $497/mo (vs $297 Professional)</li>
        </ul>
        
        <p>At your close rate of {{Close_Rate}}%, those extra 500 leads = {{Extra_Deals}} more deals per month.</p>
        
        <p>ROI on the upgrade: {{Upsell_ROI}}%</p>
        
        <p><a href="https://psdepot.com/upgrade?to=enterprise" style="background: #17a2b8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Upgrade to Enterprise</a></p>
        
        <p>-Jane</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Calls_Made", "Adjacent_Counties", "Close_Rate", "Extra_Deals", "Upsell_ROI"],
        "cta": "Upgrade to Enterprise",
        "follow_up_days": 5
    },
    {
        "id": "jane_03_reorder",
        "name": "Thermal Paper Reorder",
        "agent": "Jane",
        "stage": "cross_sell",
        "subject": "Running low on paper?",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Quick heads up: It's been {{Days_Since_Order}} days since your last thermal paper order.</p>
        
        <p>Based on {{Monthly_Usage}} cases/month, you're probably down to your last {{Estimated_Remaining}} cases.</p>
        
        <p><strong>Reorder now and save:</strong></p>
        <ul>
        <li>3 1/8" x 230' Thermal Paper: $69/case (50 rolls)</li>
        <li>Same-day shipping from California</li>
        <li>Bundle with DataDepot and save 10%</li>
        </ul>
        
        <p><a href="https://psdepot.com/reorder?sku=THERMAL-3-1-8" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Reorder Paper</a></p>
        
        <p>-Jane<br>
        Customer Success</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — Need to update quantities? Reply with your monthly usage and I'll set up auto-reorder.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Days_Since_Order", "Monthly_Usage", "Estimated_Remaining"],
        "cta": "Reorder paper",
        "follow_up_days": 3
    },
    {
        "id": "jane_04_anniversary",
        "name": "1-Year Anniversary",
        "agent": "Jane",
        "stage": "retention",
        "subject": "Happy 1-year anniversary, {{First_Name}}!",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p><strong>One year ago today</strong> you joined DataDepot Intelligence.</p>
        
        <p>Since then:</p>
        <ul>
        <li><strong>{{Total_Leads_Delivered}}</strong> leads delivered</li>
        <li><strong>{{Total_Calls_Made}}</strong> calls made by your team</li>
        <li><strong>{{Total_Deals_Closed}}</strong> deals closed</li>
        <li><strong>${{Total_Revenue_Generated}}</strong> in revenue generated</li>
        </ul>
        
        <p>ROI on your subscription: <strong>{{Yearly_ROI}}%</strong></p>
        
        <p>That's why companies like {{Company}} stick with us. The data works.</p>
        
        <p><strong>Anniversary gift:</strong> I'm extending your Professional rate of $297 for another year. (New customers pay $397 now.)</p>
        
        <p><a href="https://psdepot.com/renew?term=1year&rate=locked" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Lock in $297 for Another Year</a></p>
        
        <p>Here's to year two!</p>
        
        <p>-Jane</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Company", "Total_Leads_Delivered", "Total_Calls_Made", "Total_Deals_Closed", "Total_Revenue_Generated", "Yearly_ROI"],
        "cta": "Lock in rate for another year",
        "follow_up_days": 7
    }
]

__all__ = ['JANE_EMAILS']