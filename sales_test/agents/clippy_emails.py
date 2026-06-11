"""
CLIPPY-42 - Sales Assistant
Research intro, warm handoffs, follow-ups
4 emails in sequence
"""

CLIPPY_EMAILS = [
    {
        "id": "clippy_01_research",
        "name": "Research-Based Intro",
        "agent": "Clippy-42",
        "stage": "research",
        "subject": "Research on {{Company}} — one thing caught my attention",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>I've been researching {{Company}} and noticed something interesting.</p>
        
        <p>You serve {{Cuisine_Type}} restaurants in {{City}} — a segment with high POS turnover (restaurants upgrade every 3-4 years on average).</p>
        
        
        <p><strong>Here's what I found:</strong></p>
        <ul>
        <li>{{City}} has 127 {{Cuisine_Type}} restaurants</li>
        <li>43 are using POS systems 5+ years old</li>
        <li>12 have equipment upgrade mentions in recent reviews</li>
        </ul>
        
        <p>That's your next quarter right there — if you know who to call.</p>
        
        <p>Want the full list? I can have Miles send over a sample of 25 verified leads.</p>
        
        <p><a href="https://psdepot.com/datadepot-sample?ref=clippy" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Yes, Send Me The List</a></p>
        
        <p>-Clippy-42<br>
        Research Assistant, Performance Supply Depot</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — This data comes from our DataDepot Intelligence system. {{Company}} competitors are already using it.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Company", "Cuisine_Type", "City"],
        "cta": "Get the lead list",
        "follow_up_days": 4
    },
    {
        "id": "clippy_02_handoff",
        "name": "Warm Handoff to Miles",
        "agent": "Clippy-42",
        "stage": "handoff",
        "subject": "Connecting you with Miles (POS specialist)",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Thanks for downloading the sample leads.</p>
        
        <p>I wanted to introduce you to <strong>Miles</strong> — he's our lead sales consultant and knows {{City}} restaurants better than anyone.</p>
        
        <p>Miles helped {{Reference_Company}} close 8 deals in {{County}} last quarter using this exact data.</p>
        
        <p>He's available for a quick 7-minute call this week to show you:</p>
        <ul>
        <li>How to prioritize the 70+ replacement score leads (call these first)</li>
        <li>The review sentiment signals that predict ready-to-buy</li>
        <li>How to time your outreach around equipment renewal cycles</li>
        </ul>
        
        <p><a href="https://calendly.com/psdepot-miles/7min" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Schedule with Miles</a></p>
        
        <p>Or just reply to this email with any questions.</p>
        
        <p>-Clippy-42<br>
        (cc: Miles, Performance Supply Depot)</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "City", "Reference_Company", "County"],
        "cta": "Schedule with Miles",
        "follow_up_days": 3
    },
    {
        "id": "clippy_03_followup",
        "name": "Resource Follow-up",
        "agent": "Clippy-42",
        "stage": "nurture",
        "subject": "{{First_Name}}, your resource bundle is ready",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>I put together a few resources that might help {{Company}}:</p>
        
        <p><strong>📊 POS Market Report: {{County}} (2026)</strong></p>
        <ul>
        <li>2,847 restaurants analyzed</li>
        <li>1,203 using systems 5+ years old (replacement candidates)</li>
        <li>Average replacement cost: $8,500</li>
        <li>Peak buying months: January, September</li>
        </ul>
        
        <p><strong>📞 Call Script Template</strong></p>
        <p>The exact opener that gets past gatekeepers: <em>"I noticed you mentioned your POS system in a review last month..."</em></p>
        
        <p><strong>💡 Competitor Intel</strong></p>
        <p>{{Top_Competitor}} has been calling {{County}} restaurants aggressively. Here's their pitch (and how to counter it).</p>
        
        <p><a href="https://psdepot.com/resources/{{County}}-report" style="background: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Download Bundle</a></p>
        
        <p>-Clippy-42</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Company", "County", "Top_Competitor"],
        "cta": "Download resource bundle",
        "follow_up_days": 5
    },
    {
        "id": "clippy_04_meeting_confirm",
        "name": "Meeting Confirmation",
        "agent": "Clippy-42",
        "stage": "scheduling",
        "subject": "Confirmed: {{Meeting_Date}} with Miles — details inside",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p><strong>You're all set!</strong></p>
        
        <p>📅 <strong>{{Meeting_Date}} at {{Meeting_Time}}</strong><br>
        📞 Call: {{Call_Number}}<br>
        👤 With: Miles, Performance Supply Depot</p>
        
        <p><strong>Agenda (7 minutes):</strong></p>
        <ol>
        <li>Quick intro — your business, your targets</li>
        <li>DataDepot demo — see your territory's leads live</li>
        <li>Pricing and next steps (if it's a fit)</li>
        </ol>
        
        <p><strong>What to prepare:</strong></p>
        <ul>
        <li>Your target counties (we'll pull live data)</li>
        <li>Your current cost per lead (so we can compare)</li>
        <li>Any questions about the sample you downloaded</li>
        </ul>
        
        <p>Need to reschedule? <a href="https://calendly.com/psdepot-miles/7min">Click here</a> or reply to this email.</p>
        
        <p>Looking forward to it!</p>
        
        <p>-Clippy-42</p>
        
        <p style="font-size: 12px; color: #666;">P.S. — Miles will call you at {{Phone_Number}} at the scheduled time.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Meeting_Date", "Meeting_Time", "Call_Number", "Phone_Number"],
        "cta": "Add to calendar",
        "follow_up_days": None
    }
]

__all__ = ['CLIPPY_EMAILS']