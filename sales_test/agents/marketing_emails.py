"""
MARKETING TEAM
Product announcements, content, newsletters
5 emails
"""

MARKETING_EMAILS = [
    {
        "id": "marketing_01_product_launch",
        "name": "New Product Launch",
        "agent": "Aurora",
        "stage": "announcement",
        "subject": "NEW: AI-Powered Lead Scoring ({{County}} data just got smarter)",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p><strong>Big news:</strong> We just launched AI-Powered Lead Scoring for DataDepot.</p>
        
        <p>What this means for {{Company}}:</p>
        
        <ul>
        <li>Every lead now has a <strong>0-100 conversion probability score</strong></li>
        <li>Scores factor in: review sentiment, equipment age, neighborhood demographics, seasonal patterns</li>
        <li>Focus your time on the 80+ scores — they convert 3x higher</li>
        </ul>
        
        <p><strong>Live in your account now.</strong> Log in and see the new "AI Score" column.</p>
        
        <p><a href="https://psdepot.com/datadepot" style="background: #6f42c1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">See Your AI Scores</a></p>
        
        <p>-Aurora<br>
        Head of Marketing, Performance Supply Depot</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Company", "County"],
        "cta": "See AI scores",
        "follow_up_days": None
    },
    {
        "id": "marketing_02_newsletter",
        "name": "Monthly Newsletter",
        "agent": "Sage",
        "stage": "content",
        "subject": "Market intel: {{County}} POS trends (May 2026)",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Here's what happened in {{County}} restaurants this month:</p>
        
        <p><strong>📈 Trend Alert: {{Trend_Name}}</strong></p>
        <p>{{Trend_Description}}</p>
        
        <p><strong>🏆 Top Performing Territory:</strong> {{Top_Territory}} ({{Deals_Closed}} deals closed by DataDepot customers)</p>
        
        <p><strong>💡 Pro Tip:</strong> {{Pro_Tip}}</p>
        
        <p><strong>📊 Your Stats This Month:</strong></p>
        <ul>
        <li>Leads accessed: {{Leads_Accessed}}</li>
        <li>Calls made: {{Calls_Made}}</li>
        <li>Your conversion rate: {{Conversion_Rate}}% (vs. avg 15%)</li>
        </ul>
        
        <p>Keep up the great work!</p>
        
        <p>-Sage<br>
        Content Lead, Performance Supply Depot</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "County", "Trend_Name", "Trend_Description", "Top_Territory", "Deals_Closed", "Pro_Tip", "Leads_Accessed", "Calls_Made", "Conversion_Rate"],
        "cta": "Read full report",
        "follow_up_days": None
    },
    {
        "id": "marketing_03_webinar",
        "name": "Webinar Invitation",
        "agent": "Aurora",
        "stage": "event",
        "subject": "Webinar: How {{Reference_Company}} closed 12 deals in 30 days",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p><strong>Live Webinar: {{Webinar_Date}} at {{Webinar_Time}}</strong></p>
        
        <p>Join us as {{Reference_Company}} shares their exact playbook for closing 12 POS deals in one month using DataDepot.</p>
        
        <p><strong>What you'll learn:</strong></p>
        <ul>
        <li>The 70+ replacement score filter (why it matters)</li>
        <li>Review sentiment triggers that predict closes</li>
        <li>Call scripts that get past gatekeepers</li>
        <li>Timing: When restaurants are actually ready to buy</li>
        </ul>
        
        <p><strong>Live Q&A included.</strong> Bring your questions.</p>
        
        <p><a href="https://psdepot.com/webinar/register" style="background: #fd7e14; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Register for Webinar</a></p>
        
        <p>-Aurora</p>
        
        <p style="font-size: 12px; color: #666;">Can't make it? Register anyway — we'll send you the recording.</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Webinar_Date", "Webinar_Time", "Reference_Company"],
        "cta": "Register for webinar",
        "follow_up_days": None
    },
    {
        "id": "marketing_04_case_study",
        "name": "Case Study",
        "agent": "Sage",
        "stage": "social_proof",
        "subject": "Case study: {{Reference_Company}}'s $45K month",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>Just published: How {{Reference_Company}} generated $45K in revenue using DataDepot.</p>
        
        <p><strong>The numbers:</strong></p>
        <ul>
        <li>500 leads/month from DataDepot</li>
        <li>18% close rate (vs. 3% industry average)</li>
        <li>9 deals closed in one month</li>
        <li>Average deal: $5,000</li>
        <li>ROI: 1,500%</li>
        </ul>
        
        <p><strong>Their secret:</strong> They focused on restaurants with 75+ replacement scores + recent negative POS reviews. That's it.</p>
        
        <p><a href="https://psdepot.com/case-studies/{{Reference_Company_Slug}}" style="background: #20c997; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Read Full Case Study</a></p>
        
        <p>-Sage</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Reference_Company", "Reference_Company_Slug"],
        "cta": "Read case study",
        "follow_up_days": None
    },
    {
        "id": "marketing_05_survey",
        "name": "Customer Survey",
        "agent": "Aurora",
        "stage": "feedback",
        "subject": "Quick favor: 2-minute survey",
        "body_html": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>Hi {{First_Name}},</p>
        
        <p>We're always improving DataDepot. Could you help us out?</p>
        
        <p><strong>Quick 2-minute survey:</strong></p>
        
        <ul>
        <li>What's working well?</li>
        <li>What's frustrating?</li>
        <li>What feature would change the game?</li>
        </ul>
        
        <p><a href="https://psdepot.com/survey/{{Survey_ID}}" style="background: #6c757d; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Take Survey</a></p>
        
        <p>As a thank you, everyone who responds gets entered to win a <strong>free month of Enterprise</strong> (1,000 leads).</p>
        
        <p>-Aurora</p>
        </body>
        </html>
        """,
        "variables": ["First_Name", "Survey_ID"],
        "cta": "Take survey",
        "follow_up_days": None
    }
]

__all__ = ['MARKETING_EMAILS']