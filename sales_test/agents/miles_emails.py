"""
MILES - Primary Sales Agent
Cold outreach, qualification, initial contact
3 emails in sequence
"""

MILES_EMAILS = [
    {
        "id": "miles_01_cold",
        "name": "Cold Outreach - POS Pain Points",
        "agent": "Miles",
        "stage": "prospecting",
        "subject": "{{Company}} — CA restaurant intel you don't have",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>I was looking at {{Company}}'s site and saw you specialize in {{POS_Focus}} for restaurants.</p>
        
        <p><strong>Quick question:</strong> Where are you getting your lead lists from?</p>
        
        <p>Most POS vendors I talk to are either:</p>
        <ul>
        <li>Buying stale ZoomInfo data ($10K+/year)</li>
        <li>Paying interns to scrape Google Maps</li>
        <li>Cold-calling blind with no intel on what systems restaurants use</li>
        </ul>
        
        <p>We built something different: <strong>AI-detected POS intelligence on 100K+ California restaurants.</strong></p>
        
        <p>Not website guesses — actual photos of terminals, review analysis, and replacement timing scores.</p>
        
        <p><a href="https://calendly.com/psdepot-miles/7min" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Book a 7-Minute Call</a></p>
        
        <p>-Miles<br>
        Performance Supply Depot / DataDepot Intelligence</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — First 10 companies get a free sample of 50 leads from {{County}}. No pitch, just data.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Company", "POS_Focus", "County"],
        "cta": "Book 7-minute call",
        "follow_up_days": 3
    },
    {
        "id": "miles_02_value",
        "name": "Value Add - Free Sample",
        "agent": "Miles",
        "stage": "qualification",
        "subject": "Free sample: 50 {{County}} restaurants using {{Competitor_System}}",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Following up on my note about California POS intelligence.</p>
        
        <p>Here's what one of your competitors already knows:</p>
        <ul>
        <li>47 restaurants in {{County}} using 5+ year old Aloha systems</li>
        <li>23 of them have left negative reviews mentioning "slow POS"</li>
        <li>12 have license renewals coming up (equipment investment timing)</li>
        </ul>
        
        <p><strong>That's 47 warm leads. Not cold calls. Warm conversations.</strong></p>
        
        <p>Want the same intel for your territory?</p>
        
        <p>I'm sending free 50-record samples to POS vendors this week.</p>
        
        <p><a href="https://psdepot.com/datadepot-sample" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Get My Free Sample</a></p>
        
        <p>-Miles<br>
        Performance Supply Depot</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "County", "Competitor_System"],
        "cta": "Get free sample",
        "follow_up_days": 5
    },
    {
        "id": "miles_03_breakup",
        "name": "Breakup - Last Attempt",
        "agent": "Miles",
        "stage": "breakup",
        "subject": "Last call: {{County}} sample expires Friday",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>{{First_Name}},</p>
        
        <p>Last email — I know you're busy.</p>
        
        <p><strong>Quick question:</strong> What's your current cost per qualified restaurant lead?</p>
        
        <p>If it's more than $2, we should talk.</p>
        
        <p>Our customers pay <strong>$97/month for 500 verified California restaurants</strong> with POS system intelligence attached.</p>
        
        <p>That's <strong>$0.19 per lead</strong>. Updated weekly.</p>
        
        <p><a href="https://psdepot.com/datadepot-sample" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Request Sample</a></p>
        
        <p>Or book 15 minutes: <a href="https://calendly.com/psdepot-miles/15min">calendly.com/psdepot-miles/15min</a></p>
        
        <p>-Miles</p>
        
        <p style="font-size: 12px; color: #666;">If this isn't a fit, just reply "remove" and I'll take you off my list.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "County"],
        "cta": "Request sample or remove",
        "follow_up_days": None
    },
    {
        "id": "miles_04_thermal",
        "name": "Thermal Paper Intro",
        "agent": "Miles",
        "stage": "product",
        "subject": "{{Company}} — Cut your paper costs 30%",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Quick question: What are you paying per case for 3 1/8" thermal paper?</p>
        
        <p>If it's over $75, you're overpaying.</p>
        
        <p>Performance Supply Depot delivers:</p>
        <ul>
        <li><strong>$69/case</strong> for 3 1/8" x 230' thermal rolls (50 rolls)</li>
        <li>Same-day shipping from California</li>
        <li>No minimum orders</li>
        <li>BPA-free, OEM-grade paper</li>
        </ul>
        
        <p>Same paper your customers use. Better price. Faster delivery.</p>
        
        <p><a href="https://psdepot.com/quote?product=thermal" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Get Instant Quote</a></p>
        
        <p>-Miles<br>
        Performance Supply Depot</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — Need a sample roll to test? Reply with your address.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Company"],
        "cta": "Get instant quote",
        "follow_up_days": 3
    },
    {
        "id": "miles_05_referral",
        "name": "Referral Request",
        "agent": "Miles",
        "stage": "referral",
        "subject": "Quick favor, {{First_Name}}?",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Hope the {{Last_Product_Ordered}} is working out well.</p>
        
        <p><strong>Quick favor:</strong> Do you know any other POS vendors or restaurant suppliers who might benefit from our DataDepot intelligence?</p>
        
        <p>We're expanding our partner program and offering <strong>$200 credit</strong> for every referral that becomes a customer.</p>
        
        <p>No hard sell needed — just an introduction.</p>
        
        <p><a href="https://psdepot.com/referral" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Refer a Colleague</a></p>
        
        <p>Appreciate you!</p>
        
        <p>-Miles</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Last_Product_Ordered"],
        "cta": "Refer a colleague",
        "follow_up_days": 7
    }
]

# Export for main system
__all__ = ['MILES_EMAILS']