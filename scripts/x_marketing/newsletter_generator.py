#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weekly Newsletter Generator for Performance Supply Depot
Expounds on X/TikTok topics with in-depth content for customers

NEWSLETTER STRATEGY:
- Aligns with 20-email campaign sequence
- Expands on X/TikTok topics with deeper education
- Provides actionable value for restaurant owners
- Drives traffic to psdepot.com
- Reinforces 888-881-6834 contact

WEEKLY THEMES (Rotating):
Week 1: Supply Chain & Cost Management (aligns with Email #2, #5)
Week 2: Printer Maintenance & Repair (aligns with Email #2, #6)
Week 3: POS Technology & Upgrades (aligns with Email #4, #6)
Week 4: Operational Efficiency (aligns with Email #3, #5)
Week 5: New Business Setup (aligns with Email #1, #11)
Week 6: Seasonal Preparation (aligns with Email #11, #19)
Week 7: Staff Training & Support (aligns with Email #6)
Week 8: Industry Trends & Insights (aligns with Email #14, #17)
"""

import random
import sys
from datetime import datetime

PHONE = "888-881-6834"
WEBSITE = "https://psdepot.com"
EMAIL = "info@psdepot.com"

# Weekly newsletter templates - Deep dive on each topic
NEWSLETTERS = [
    {
        "week": 1,
        "theme": "Supply Chain & Cost Management",
        "subject": "How Vegas restaurants are cutting supply costs 15-20%",
        "preview": "3 strategies that actually work in today's market",
        "header": "The Real Cost of POS Supplies (And How to Fix It)",
        "content": """
Hi {{first_name}},

You've probably noticed: supply costs are up 15-20% this year. Paper, ribbons, printer parts — everything costs more than it did 12 months ago.

But here's what most suppliers won't tell you: the restaurants winning right now aren't just accepting higher prices. They're locking in reliable partnerships.

**Why Local Suppliers Are Winning in 2025**

When supply chains get tight, big distributors prioritize their largest accounts. Local restaurants get pushed to the back of the line.

We've seen it happen:
• Chain restaurants with dedicated contracts get priority
• Independent spots wait weeks for basic supplies  
• Prices spike when inventory runs low

**3 Strategies That Actually Work**

**1. Lock in pricing now**
Restaurants who committed to 6-month supply agreements in Q1 are paying 12-18% less than those ordering month-to-month.

**2. Keep a 2-week buffer**
Sounds simple, but most restaurants keep only 3-5 days of paper on hand. One shipping delay = weekend crisis.

**3. Build relationships with local suppliers**
When you're not just an account number, you get priority during shortages. Same-day delivery isn't a luxury — it's survival.

**The Bottom Line**

You can't control global supply chains. But you can control who you rely on when things get tight.

Questions about your supply setup? I'm here: {PHONE}

Or grab a quick quote: {WEBSITE}

Best,
Miles
Performance Supply Depot

P.S. — Running low on thermal paper? We just restocked all standard sizes. Order by 2 PM for same-day delivery in Vegas.
""".format(PHONE=PHONE, WEBSITE=WEBSITE),
    },
    {
        "week": 2,
        "theme": "Printer Maintenance & Repair",
        "subject": "Why your receipt printer keeps breaking (and how to fix it)",
        "preview": "The $200 mistake every restaurant makes",
        "header": "Your Printer Is Trying to Tell You Something",
        "content": """
Hi {{first_name}},

Last week, I visited a restaurant that spent $847 on receipt printer "repairs" in three months.

The problem? They were fixing symptoms, not causes.

**The Real Cost of Printer Neglect**

Here's what actually happens when you ignore printer maintenance:

• Thermal head wears out prematurely ($180-250 replacement)
• Paper jams damage feed mechanisms ($90-150 repair)
• Debris builds up, causing streaks and misprints
• Small issues become printer replacements ($500-1,200)

That $847 restaurant? A $15 monthly cleaning routine would have prevented 90% of their problems.

**The 5-Minute Monthly Ritual**

Every printer manufacturer recommends this. Almost nobody does it:

1. **Power down** the printer completely
2. **Open** the paper compartment
3. **Apply** 90%+ isopropyl alcohol to lint-free cloth
4. **Gently wipe** the thermal head (the thin metal strip)
5. **Let dry** 30 seconds before reloading paper

Takes 5 minutes. Saves hundreds.

**When to Call a Tech**

Some problems need professional help:
• Feed mechanism not grabbing paper
• Consistent jamming despite cleaning
• Electrical issues (won't power on)
• Network connectivity problems

We handle on-site repairs for all major brands: Epson, Star, Bixolon, Citizen.

**The Math That Matters**

Professional cleaning service: ~$85/month
Emergency repair call: ~$200-400
New printer when yours dies: ~$500-1,200

Prevention beats reaction. Every time.

Questions about your printer setup? Call me: {PHONE}

Or book a diagnostic: {WEBSITE}

Best,
Miles
Performance Supply Depot

P.S. — We offer printer swap programs. Trade your problematic unit for a refurbished, fully-tested replacement. Ask about options.
""".format(PHONE=PHONE, WEBSITE=WEBSITE),
    },
    {
        "week": 3,
        "theme": "POS Technology & Upgrades",
        "subject": "Is it time to upgrade your POS system?",
        "preview": "Samsung vs Sam4s: A restaurant owner's guide",
        "header": "Choosing the Right POS System (Without the Overwhelm)",
        "content": """
Hi {{first_name}},

I get this question every week: "Should I upgrade my POS system?"

The honest answer: Maybe. But probably not for the reasons you think.

**When to Upgrade (And When to Wait)**

**Upgrade if:**
• Your current system crashes more than twice a month
• You're losing transactions to slowdowns
• You're opening a second location and need cloud sync
• Your hardware is 7+ years old and unsupported

**Wait if:**
• Your system works reliably
• Staff knows it well
• You're only upgrading because competitors did
• The new features won't actually help your operation

**Samsung vs Sam4s: What Restaurant Owners Should Know**

**Samsung POS Systems**
• Range: $495-$1,395
• Best for: High-volume, table-service restaurants
• Pros: Robust, reliable, widely supported
• Cons: Higher upfront cost

**Sam4s POS Systems**
• Range: $495-$1,095  
• Best for: Quick-service, cafes, food trucks
• Pros: Compact, affordable, easy to learn
• Cons: Fewer customization options

**The Hidden Cost Nobody Talks About**

It's not the hardware. It's the setup.

A $500 POS system with bad installation:
• Confused staff = slower service
• Wrong configuration = accounting headaches
• Network issues = lost transactions

A $1,200 system with professional setup:
• Smooth staff transition
• Proper reporting from day one
• Reliable operation under pressure

**Our Recommendation**

Don't just buy a POS system. Buy a partnership.

You need:
• Pre-install consultation (what do you actually need?)
• Professional cabling and network setup
• Staff training that sticks
• Ongoing support when things break

That's what we do. Hardware + setup + training + support.

Want to talk through your setup? {PHONE}

See current pricing: {WEBSITE}

Best,
Miles
Performance Supply Depot

P.S. — Opening a new location? We handle end-to-end POS setup. Cabling, configuration, training — done right the first time.
""".format(PHONE=PHONE, WEBSITE=WEBSITE),
    },
    {
        "week": 4,
        "theme": "Operational Efficiency",
        "subject": "The 2-week buffer: Why smart restaurants never run out",
        "preview": "Simple supply habits that save your weekend",
        "header": "Supply Management That Actually Works",
        "content": """
Hi {{first_name}},

Friday, 6 PM. Your busiest night of the week.

Your head server runs to the back: "We're out of receipt paper."

This is the moment that separates prepared restaurants from panicked ones.

**The Psychology of Supply Shortages**

Running out of supplies isn't just inconvenient. It's expensive:
• Staff time spent sourcing emergency stock
• Expedited shipping costs
• Lost sales if you can't print receipts
• Customer frustration when checkout slows

And yet most restaurants operate with just 3-5 days of buffer.

**The 2-Week Rule**

Here's what successful restaurants do differently:

**Week 1:** Use current supplies normally
**Week 2:** Your safety buffer — you never touch this

When Week 1 runs low, you order more. Week 2 becomes your new Week 1.

Simple. Effective. Almost nobody does it.

**Why Most Restaurants Get This Wrong**

Three reasons:

1. **Cash flow concerns** — "I can't afford to stock up"
   Reality: The cost of running out exceeds the cost of stocking up

2. **Space limitations** — "I don't have room to store extras"
   Reality: A case of receipt paper takes 2 square feet

3. **Just-in-time thinking** — "I'll order when I need it"
   Reality: Supply chains fail. Shipping gets delayed. Stuff happens.

**How to Build Your Buffer**

Start small:
• Identify your top 3 critical supplies
• Calculate 2 weeks of usage for each
• Order that amount on your next cycle
• Restock when you hit 50%

Within a month, you'll never panic-order again.

**The Real Benefit**

It's not just avoiding shortages.

With a 2-week buffer:
• You can wait for better pricing
• You consolidate shipping costs
• You negotiate from strength, not desperation
• Your weekends run smoother

**Need help calculating your buffer?**

I do this all the time. Call me: {PHONE}

Or grab supplies with confidence: {WEBSITE}

Best,
Miles
Performance Supply Depot

P.S. — Same-day delivery available when you need it most. But with a 2-week buffer, you'll almost never need it.
""".format(PHONE=PHONE, WEBSITE=WEBSITE),
    },
    {
        "week": 5,
        "theme": "New Business Setup",
        "subject": "Opening a restaurant? Start with your POS foundation",
        "preview": "What 15 years of setups taught us",
        "header": "Your POS Foundation: Get It Right From Day One",
        "content": """
Hi {{first_name}},

Opening a restaurant?

After 15 years and 800+ setups, I've learned one thing: Your POS system is either a foundation or a frustration.

There's no middle ground.

**The Mistake That Haunts New Restaurants**

Here's what usually happens:

Month 1: Buy cheap POS online, self-install
Month 2: Realize nothing talks to each other
Month 3: Fix one problem, create two more
Month 6: Pay someone to rip it out and start over

The restaurants that get it right do one thing differently: They invest in professional setup.

**Your Opening Checklist**

**Before Day One:**
• POS hardware selected and tested
• Network cabling installed (not just WiFi)
• Software configured for your menu
• Payment processing integrated
• Reporting structure designed

**Week One:**
• Staff training on basic transactions
• Manager training on reporting and voids
• Troubleshooting guide printed and posted
• Support contact saved in phones

**Month One:**
• First month's reports reviewed
• Menu/pricing adjustments made
• Additional training for complex scenarios
• Backup and data security verified

**What Professional Setup Includes**

When we handle a new restaurant setup:

1. **Site survey** — What's your layout? Power? Network?
2. **Hardware selection** — What do you actually need? (Not what we want to sell)
3. **Cabling installation** — Clean, organized, future-proof
4. **Configuration** — Menu, taxes, reporting, staff permissions
5. **Training** — Managers + staff, hands-on, until they're confident
6. **Support handoff** — Direct line for questions, not a ticket system

**The Cost of Getting It Wrong**

DIY setup that fails: $2,000-5,000 in lost sales, emergency repairs, and eventually reinstalling

Professional setup that works: $1,500-3,500 depending on complexity

Do it once. Do it right.

**Opening soon?**

We handle 2-3 new restaurant setups per month in Vegas. I know what works.

Call me: {PHONE}

Or see what we offer: {WEBSITE}

Best,
Miles
Performance Supply Depot

P.S. — Opening in Q2? Book your setup consultation now. April-May is our busiest season.
""".format(PHONE=PHONE, WEBSITE=WEBSITE),
    },
    {
        "week": 6,
        "theme": "Seasonal Preparation",
        "subject": "Holiday prep: Is your POS ready for the rush?",
        "preview": "The December checklist every restaurant needs",
        "header": "Holiday Season Survival Guide for POS Systems",
        "content": """
Hi {{first_name}},

December is coming.

If you're in the restaurant business, you know what that means: 40% of your annual revenue crammed into 6 weeks.

Your POS system needs to handle it. Most aren't ready.

**The Holiday Reality Check**

Here's what December actually looks like:
• 2-3x normal transaction volume
• New seasonal staff who need training
• Gift card promotions (and the accounting that comes with them)
• Extended hours, more wear on hardware
• No time for breakdowns

One printer failure on December 23rd can cost you thousands.

**The November Prep Checklist**

**Hardware:**
□ All printers cleaned and tested
□ Backup thermal paper stock (2x normal)
□ Extra ink ribbons on hand
□ Network stress-tested for peak traffic
□ Backup equipment identified (just in case)

**Software:**
□ Holiday menu items entered
□ Gift card system tested
□ Promo codes configured
□ Reporting adjusted for seasonal tracking
□ Backup schedule verified

**Staff:**
□ Holiday-specific training completed
□ Void/discount permissions reviewed
□ Manager override procedures practiced
□ Support contact posted at every station

**The One Thing Most Restaurants Miss**

They prep for the rush. They don't prep for what comes after.

January is accounting nightmare season:
• Reconciling gift card sales
• Processing returns and exchanges
• Analyzing holiday performance
• Planning for next year

Set up your reporting right in November. Thank yourself in January.

**Emergency Planning**

Even with perfect prep, stuff breaks.

Have a plan:
• Local supplier contact saved (that's us: {PHONE})
• Backup receipt method (manual pads, just in case)
• Manager authorized to make emergency purchases
• After-hours support number posted

**Need holiday prep help?**

We do pre-season POS tune-ups: hardware check, software update, staff refresher training.

Call me: {PHONE}

Or book online: {WEBSITE}

Best,
Miles
Performance Supply Depot

P.S. — Ordering holiday supplies? Do it by November 15th. December shipping gets unpredictable.
""".format(PHONE=PHONE, WEBSITE=WEBSITE),
    },
    {
        "week": 7,
        "theme": "Staff Training & Support",
        "subject": "Why your POS training keeps failing (and how to fix it)",
        "preview": "Training that actually sticks",
        "header": "POS Training That Actually Works",
        "content": """
Hi {{first_name}},

You've trained your staff on the POS system three times.

They still call you over for every void, every discount, every weird situation.

It's not them. It's the training.

**Why Most POS Training Fails**

Here's what usually happens:

**Day 1:** New hire watches a 45-minute video about the POS system
**Day 2:** Shadow experienced server for one shift  
**Day 3:** Thrown into lunch rush with "Call if you need help"

By Day 7: They're creating workarounds instead of using the system.

By Day 30: They're teaching new hires the wrong way.

**What Actually Works**

After 800+ setups, here's what separates restaurants that struggle from restaurants that thrive:

**1. Scenario-Based Training**
Don't teach buttons. Teach situations.

"Here's what you do when..."
• The customer wants to split a check 4 ways
• The kitchen is out of the special
• The card reader doesn't work
• The manager needs to comp a table

**2. Just-in-Time Support**
Staff forget 70% of training within a week. Give them quick-reference guides they can actually use during service.

**3. Manager Training (Not Just Staff)**
Your managers need to know:
• How to run end-of-day reports
• How to fix common problems
• When to call for backup (and who to call)
• How to train new hires correctly

**The Training Template That Works**

**Hour 1:** System overview (big picture, not details)
**Hour 2:** Hands-on practice with test transactions
**Hour 3:** Shadow experienced server (with checklist)
**Day 2:** Supervised live service (with coach nearby)
**Day 7:** Refresher on problem areas
**Day 30:** Advanced features training

**The Support System**

Training without support is half a solution.

You need:
• A phone number that actually answers (try ours: {PHONE})
• Same-day response for critical issues
• Staff who can explain problems clearly
• Documentation that's actually useful

**Our Training Approach**

When we set up a POS system:

1. **Manager training first** — They become the in-house expert
2. **Staff training in small groups** — Questions get answered
3. **Scenario practice** — Not just "here's the button"
4. **Quick-reference guides** — Laminated, posted at stations
5. **30-day check-in** — What's working, what needs adjustment

**Struggling with staff training?**

I do refresher training for existing systems, not just new setups.

Call me: {PHONE}

Or see our training options: {WEBSITE}

Best,
Miles
Performance Supply Depot

P.S. — Opening a second location? We train your managers to train their staff. Consistency across locations.
""".format(PHONE=PHONE, WEBSITE=WEBSITE),
    },
    {
        "week": 8,
        "theme": "Industry Trends & Insights",
        "subject": "What POS trends mean for your restaurant",
        "preview": "Cloud vs local: Making the right choice",
        "header": "POS Trends That Actually Matter",
        "content": """
Hi {{first_name}},

Every week, someone tries to sell you the "future of POS."

Tablet ordering. AI recommendations. Facial recognition payment.

Here's what actually matters for your restaurant.

**The Cloud vs Local Debate**

You've heard the pitch: "Everything's in the cloud now!"

Here's the reality:

**Cloud POS (Square, Toast, etc)**
✓ Lower upfront cost
✓ Automatic updates
✓ Work from anywhere
✗ Monthly fees forever
✗ Needs internet connection
✗ You don't own your data

**Local POS (Samsung, Sam4s, etc)**
✓ No ongoing fees
✓ Works without internet
✓ You own everything
✓ Higher upfront cost
✗ You're responsible for updates

**Our Take:** For most Vegas restaurants, local wins. Internet outages happen. Monthly fees add up. And when something breaks, you need it fixed now, not via a support ticket.

**Trends Worth Watching**

**Integrated Kitchen Display Systems (KDS)**
Digital tickets replacing paper chits. Faster, cleaner, easier to track timing.

**Mobile Payment Integration**
Apple Pay, Google Pay, tap-to-pay. Customers expect it. Most systems support it now.

**Tableside Ordering Tablets**
Controversial. Some servers love them (more tips, less running). Some hate them (impersonal, technical issues). Test before you commit.

**Trends You Can Skip (For Now)**

• **AI-powered upselling** — Cool demo, questionable ROI
• **Facial recognition payment** — Privacy concerns + customer confusion
• **Blockchain receipts** — Solution looking for a problem

**The Real Trend: Reliability**

While everyone's chasing the next shiny feature, smart restaurants are investing in:
• Hardware that doesn't break
• Support that answers the phone
• Systems staff actually understand

Boring? Yes. Profitable? Also yes.

**What We Recommend**

Don't chase trends. Solve problems.

Your POS system needs to:
1. Process transactions reliably
2. Generate reports you can actually use
3. Train staff quickly
4. Get fixed fast when it breaks

Everything else is optional.

**Want to talk through your setup?**

No sales pitch. Just honest advice from 15 years in Vegas restaurants.

Call me: {PHONE}

Or see current options: {WEBSITE}

Best,
Miles
Performance Supply Depot

P.S. — Got a POS system question? Reply to this email. I read every one.
""".format(PHONE=PHONE, WEBSITE=WEBSITE),
    },
]

def get_weekly_newsletter(week_number=None):
    """Get newsletter for specific week or current week"""
    if week_number is None:
        # Get current week of year (1-52)
        week_number = datetime.now().isocalendar()[1]
    
    # Map to 1-8 cycle
    cycle_week = ((week_number - 1) % 8) + 1
    
    for newsletter in NEWSLETTERS:
        if newsletter["week"] == cycle_week:
            return newsletter
    
    return NEWSLETTERS[0]

def get_newsletter_by_theme(theme):
    """Get newsletter by theme name"""
    for newsletter in NEWSLETTERS:
        if newsletter["theme"].lower() == theme.lower():
            return newsletter
    return None

def generate_html_newsletter(newsletter):
    """Generate HTML version of newsletter"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{newsletter['subject']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1a365d; color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .content {{ padding: 30px; background: #f7fafc; }}
        .cta {{ background: #c53030; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 30px; color: #666; font-size: 14px; }}
        .phone {{ font-size: 20px; font-weight: bold; color: #1a365d; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{newsletter['header']}</h1>
        <p>Performance Supply Depot Newsletter</p>
    </div>
    <div class="content">
        {newsletter['content'].replace(chr(10), '<br>')}
        <br><br>
        <a href="{WEBSITE}" class="cta">Visit psdepot.com</a>
    </div>
    <div class="footer">
        <p class="phone">📞 {PHONE}</p>
        <p>{EMAIL} | {WEBSITE}</p>
        <p>Las Vegas, NV</p>
    </div>
</body>
</html>"""
    return html

def main():
    if len(sys.argv) < 2:
        print("=" * 70)
        print("Weekly Newsletter Generator - Performance Supply Depot")
        print("8-week rotating cycle, aligns with email campaigns")
        print("Phone:", PHONE)
        print("Website:", WEBSITE)
        print("=" * 70)
        print("\nUsage:")
        print("  newsletter.py current       # This week's newsletter")
        print("  newsletter.py week [1-8]  # Specific week")
        print("  newsletter.py html          # HTML version")
        print("  newsletter.py list          # All themes")
        return
    
    command = sys.argv[1]
    
    if command == "current":
        newsletter = get_weekly_newsletter()
        print(f"\n📧 Week {newsletter['week']}: {newsletter['theme']}")
        print(f"\nSubject: {newsletter['subject']}")
        print(f"Preview: {newsletter['preview']}")
        print("\n" + "=" * 70)
        print(newsletter['content'])
        print("=" * 70)
        
    elif command == "week":
        week = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        newsletter = get_weekly_newsletter(week)
        print(f"\n📧 Week {newsletter['week']}: {newsletter['theme']}")
        print(f"\nSubject: {newsletter['subject']}")
        print(newsletter['content'])
        
    elif command == "html":
        newsletter = get_weekly_newsletter()
        html = generate_html_newsletter(newsletter)
        print(html)
        
    elif command == "list":
        print("\n📅 8-Week Newsletter Cycle:")
        print("=" * 70)
        for n in NEWSLETTERS:
            print(f"\nWeek {n['week']}: {n['theme']}")
            print(f"  Subject: {n['subject']}")
            print(f"  Aligns with: Email sequence #{n['week'] * 2}-{n['week'] * 2 + 2}")
            
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
