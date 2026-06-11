"""
PULP - The Closer
Discovery, negotiation, contract closing
4 emails in sequence
"""

PULP_EMAILS = [
    {
        "id": "pulp_01_discovery",
        "name": "Discovery Call Follow-up",
        "agent": "Pulp",
        "stage": "discovery",
        "subject": "{{First_Name}}, your custom proposal is ready",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Great talking with you yesterday. I pulled together a custom proposal based on what we discussed.</p>
        
        <p><strong>Your Territory:</strong> {{County}}, {{State}}</p>
        <p><strong>Target:</strong> {{Cuisine_Type}} restaurants, 50+ seats</p>
        
        <p><strong>Here's what I'm recommending:</strong></p>
        
        <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
        <tr style="background: #f5f5f5;">
        <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Package</th>
        <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Leads/Month</th>
        <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Price</th>
        </tr>
        <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">Starter</td>
        <td style="padding: 10px; border: 1px solid #ddd;">200</td>
        <td style="padding: 10px; border: 1px solid #ddd;">$197/mo</td>
        </tr>
        <tr style="background: #e6f3ff;">
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>Professional (Recommended)</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>500</strong></td>
        <td style="padding: 10px; border: 1px solid #ddd;"><strong>$297/mo</strong></td>
        </tr>
        <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">Enterprise</td>
        <td style="padding: 10px; border: 1px solid #ddd;">1,000</td>
        <td style="padding: 10px; border: 1px solid #ddd;">$497/mo</td>
        </tr>
        </table>
        
        <p><strong>The Professional tier includes:</strong></p>
        <ul>
        <li>500 verified {{County}} restaurant leads/month</li>
        <li>AI-detected POS systems + replacement scores</li>
        <li>Review sentiment analysis</li>
        <li>Direct owner/GM contacts</li>
        <li>Export to CSV/Excel</li>
        </ul>
        
        <p>That's <strong>$0.59 per lead</strong> — and they're <em>qualified</em> leads, not cold lists.</p>
        
        <p><a href="https://psdepot.com/checkout?plan=professional&ref={{Customer_ID}}" style="background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">Start Professional Trial</a></p>
        
        <p>Questions? Just hit reply.</p>
        
        <p>-Pulp<br>
        Head of Sales, Performance Supply Depot</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — Based on your close rate of {{Close_Rate}}%, 500 leads should yield {{Projected_Deals}} deals. At {{Average_Deal_Value}}, that's {{Projected_Revenue}} in revenue for $297.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "County", "State", "Cuisine_Type", "Customer_ID", "Close_Rate", "Projected_Deals", "Average_Deal_Value", "Projected_Revenue"],
        "cta": "Start Professional Trial",
        "follow_up_days": 2
    },
    {
        "id": "pulp_02_objection_price",
        "name": "Price Objection Handler",
        "agent": "Pulp",
        "stage": "negotiation",
        "subject": "The ROI math on DataDepot (for {{Company}})",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>I hear you on the budget concern. Let's talk numbers.</p>
        
        <p><strong>Your current approach:</strong></p>
        <ul>
        <li>Buying 500 leads from ZoomInfo: ~$2,500-5,000</li>
        <li>Hours spent qualifying: ~20 hours @ $50/hr = $1,000</li>
        <li>Actual qualified leads: Maybe 100 (20% accuracy)</li>
        <li><strong>True cost per qualified lead: $35-60</strong></li>
        </ul>
        
        <p><strong>DataDepot approach:</strong></p>
        <ul>
        <li>500 pre-qualified leads (POS system verified): $297</li>
        <li>Zero qualification time — start calling today</li>
        <li>All 500 qualified (100% accuracy)</li>
        <li><strong>True cost per qualified lead: $0.59</strong></li>
        </ul>
        
        <p><strong>The difference:</strong> You're paying 60-100x more for unqualified leads right now.</p>
        
        <p>At {{Close_Rate}}% close rate and {{Average_Deal_Value}} average deal, DataDepot should generate {{Projected_Revenue}} in revenue.</p>
        
        <p>ROI: {{ROI_Percentage}}%</p>
        
        <p>Still want to think about it? I'll hold the Professional tier at $297 for 48 hours. After that, it's $397/month for new customers.</p>
        
        <p><a href="https://psdepot.com/checkout?plan=professional&discount=HOLD297" style="background: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">Lock in $297 Rate</a></p>
        
        <p>-Pulp</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Company", "Close_Rate", "Average_Deal_Value", "Projected_Revenue", "ROI_Percentage"],
        "cta": "Lock in discounted rate",
        "follow_up_days": 2
    },
    {
        "id": "pulp_03_urgency",
        "name": "Urgency Close",
        "agent": "Pulp",
        "stage": "closing",
        "subject": "Last chance: {{County}} data ({{Competitor_Count}} competitors already signed up)",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>{{First_Name}},</p>
        
        <p>This is my last email on this.</p>
        
        <p><strong>Here's the situation:</strong></p>
        
        <p>We've signed {{Competitor_Count}} POS vendors in {{County}} this month. They're calling the same restaurants you are — but they know:</p>
        
        <ul>
        <li>Which restaurants use 5+ year old systems</li>
        <li>Which ones complained about "slow POS" in reviews</li>
        <li>Which owners are actively looking for quotes</li>
        </ul>
        
        <p>Every day you wait, they're making calls with intelligence you don't have.</p>
        
        <p><strong>Your options:</strong></p>
        
        <p>1. <strong>Start today</strong> — Get 500 qualified {{County}} leads for $297. Be first to the best prospects.</p>
        
        <p>2. <strong>Wait</strong> — Keep calling blind while competitors have the intel advantage.</p>
        
        <p>I know which one I'd choose.</p>
        
        <p><a href="https://psdepot.com/checkout?plan=professional&county={{County}}" style="background: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">Get {{County}} Data Now</a></p>
        
        <p>-Pulp</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — After Friday, the Professional tier goes to $397 for {{County}} (high demand). Lock in $297 today.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "County", "Competitor_Count"],
        "cta": "Get county data now",
        "follow_up_days": 3
    },
    {
        "id": "pulp_04_won",
        "name": "Welcome/Onboarding",
        "agent": "Pulp",
        "stage": "closed_won",
        "subject": "Welcome to DataDepot — your login + first steps",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p><strong>Welcome to DataDepot Intelligence!</strong> Your Professional subscription is active.</p>
        
        <p><strong>Your Login:</strong></p>
        <ul>
        <li>Portal: <a href="https://psdepot.com/datadepot">psdepot.com/datadepot</a></li>
        <li>Email: {{Email}}</li>
        <li>Temp Password: {{Temp_Password}} (change on first login)</li>
        </ul>
        
        <p><strong>First Steps (do these in order):</strong></p>
        
        <p>1️⃣ <strong>Download your first 500 leads</strong> ({{County}} data is ready)</p>
        <p>2️⃣ <strong>Sort by Replacement Score</strong> — Start with 70+ scores</p>
        <p>3️⃣ <strong>Filter by Review Sentiment</strong> — "Slow POS" = hot lead</p>
        
        <p><strong>Pro Tip:</strong> Your first 50 calls should be to restaurants with 75+ replacement scores + negative POS reviews. Highest conversion rate.</p>
        
        <p>Jane will be reaching out in 7 days to check how your first week went.</p>
        
        <p>Questions? Reply to this email or call 888-881-6834.</p>
        
        <p>Let's close some deals.</p>
        
        <p>-Pulp<br>
        Head of Sales</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — Your next 500 leads refresh on {{Next_Refresh_Date}}. Mark your calendar.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Email", "Temp_Password", "County", "Next_Refresh_Date"],
        "cta": "Access portal",
        "follow_up_days": None
    }
]

__all__ = ['PULP_EMAILS']