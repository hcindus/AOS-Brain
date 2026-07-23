# SOP-001: Lead Response & Qualification
**Owner:** Patricia / Sales Team  
**Frequency:** Real-time (immediate response required)  
**Automation Level:** Semi → Full (Phase 2)  
**Last Tested:** 2026-07-23  
**Status:** READY FOR DEPLOYMENT

---

## Purpose
Capture and qualify all inbound leads within 5 minutes, converting 40%+ to qualified opportunities through systematic follow-up.

---

## Inputs (Lead Sources)

| Source | How It Arrives | System Check |
|--------|----------------|--------------|
| Website Form | HubSpot notification | Check HubSpot Contacts |
| Phone Call | Missed call log / Voicemail | Check RingCentral |
| Email Inquiry | Forwarded to sales@psdepot.com | Check Gmail sales label |
| Trade Show / Event | Business cards / Scan data | Check Eventbrite/CRM |
| Referral | Direct email / Phone | Check "Referral Source" field |

**CRITICAL:** Check ALL sources every 15 minutes during business hours (8AM-6PM CST).

---

## Process Steps

### Step 1: Acknowledge Receipt (0-5 minutes)
**GOAL:** Make contact while lead is hot

**Action:**
1. Send immediate text message (if phone provided):
   ```
   Hi [First Name], this is [Agent Name] from Performance Supply Depot. 
   I received your inquiry about [product/service]. I'm pulling together 
   some options for you now. Can you chat for 2 minutes? - [Phone Number]
   ```

2. If no reply in 5 minutes, call the number.

3. If voicemail, leave:
   ```
   "Hi [First Name], this is [Agent Name] with Performance Supply Depot. 
   I saw you were looking for [product/service]. I have a few questions to 
   make sure I get you exactly what you need. My direct line is [Number]. 
   I'll also send you an email with some initial thoughts. Thanks!"
   ```

4. Send email immediately:
   - Subject: "Re: Your [Product] Inquiry - Performance Supply Depot"
   - Template: See Appendix A

**ESCALATION:** If lead comes in after hours (6PM-8AM), agent sends text/email but marks for "Priority Follow-Up" at 8:15 AM next business day.

---

### Step 2: Qualify Lead (5-15 minutes)
**GOAL:** Determine if this is a viable opportunity worth pursuing

**Ask These Questions (in order):**

1. **Company/Context:**
   - "What type of business are you with?" (Restaurant, retail, hotel, etc.)
   - "How many locations do you have?" (1-5, 6-20, 20+)
   - "Are you currently using any POS system?" (Yes/No - which one?)

2. **Needs Assessment:**
   - "What prompted you to look for [product] right now?" (Pain point)
   - "What are you currently using for [function]?" (Current state)
   - "What's not working with your current setup?" (Gap analysis)
   - "What's your timeline for making a decision?" (Urgency)

3. **Budget & Authority:**
   - "Do you have a budget allocated for this, or are we still in the planning phase?"
   - "Who else is involved in this decision?" (Decision maker)
   - "What's your typical monthly spend on [category]?"

**Record in HubSpot:**
- Lead Source
- Company Type
- # of Locations
- Current System
- Pain Points
- Timeline
- Decision Maker(s)
- Budget Status

---

### Step 3: Categorize & Route (15-20 minutes)

**Lead Score Calculation:**

| Criteria | Points |
|----------|--------|
| Multi-location (5+) | +20 |
| Timeline < 30 days | +20 |
| Budget allocated | +15 |
| Decision maker speaking | +15 |
| Currently using competitor | +10 |
| Pain point identified | +10 |
| Referral source | +5 |

**Categories:**

- **HOT (75+ points):** Decision maker, budget, timeline < 30 days
  - Action: Schedule demo/quote call within 24 hours
  - Owner: Senior sales rep
  
- **WARM (50-74 points):** Some budget/timeline, needs nurturing
  - Action: Send quote + schedule follow-up call in 3 days
  - Owner: Sales rep
  
- **COLD (25-49 points):** Future potential, early research
  - Action: Add to nurture sequence (monthly touches)
  - Owner: Marketing/Sales development
  
- **DISQUALIFIED (<25 points):** Wrong fit, no budget, etc.
  - Action: Archive with note explaining why
  - Owner: Mark "Not a Fit" in CRM

---

### Step 4: Immediate Actions Based on Category

**HOT Lead Actions:**
1. Create opportunity in HubSpot ($$$ Est. Value)
2. Assign to senior sales rep
3. Schedule discovery call within 24 hours
4. Prepare custom quote (see SOP-002)
5. Add to "HOT LEADS" Slack channel

**WARM Lead Actions:**
1. Send standard product catalog PDF
2. Send relevant case study (matching their industry)
3. Schedule follow-up call (3 days out)
4. Add to nurture sequence

**COLD Lead Actions:**
1. Add to monthly newsletter
2. Send "Getting Started" guide
3. Schedule check-in for 30 days out
4. Tag for retargeting ads

---

## Outputs

1. **Qualified Opportunity** (HOT/WARM) → Move to SOP-002 (Quote Generation)
2. **Nurture Lead** (COLD) → Marketing sequence
3. **Disqualified** → Archive with reason

---

## Exceptions & Edge Cases

### "I need this tomorrow!" (Rush Request)
1. Verify if it's truly urgent (system down, grand opening, etc.)
2. If yes: Skip standard process, go straight to "Emergency Quote" (see SOP-002 Emergency Section)
3. If no: Explain standard timeline, set realistic expectations

### "Just browsing / gathering prices"
1. Ask: "What are you comparing us against?"
2. Ask: "What would make us the obvious choice?"
3. Still qualify fully - they may be ready sooner than they say

### Competitor mentioned ("We're using Square right now")
1. Don't bash competitor
2. Ask: "What do you like about Square? What frustrates you?"
3. Position as: "We specialize in businesses like yours that have outgrown [competitor]"

### Ghosted after initial contact
1. Day 2: Follow-up email with value (case study, tip sheet)
2. Day 5: Call + voicemail
3. Day 7: LinkedIn connection request with note
4. Day 14: "Break-up" email: "Haven't heard back, assumed timing isn't right..."
5. Day 30: Add to nurture sequence

---

## Metrics & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response Time | < 5 minutes | HubSpot timestamp vs. first contact |
| Lead Qualification Rate | 70% | # qualified / # total leads |
| Hot Lead Conversion | 40% | # closed / # hot leads |
| Warm Lead Conversion | 15% | # closed / # warm leads |
| Cost per Lead | <$50 | Total marketing spend / leads |

---

## Automation Notes

**Current Pain Points:**
- Leads sit in inbox too long (avg 45 min response time)
- Inconsistent qualification questions
- Hot leads not prioritized
- Follow-up falls through cracks

**Automation Opportunities:**
- Auto-text on form submission (Twilio integration)
- AI agent pre-qualifies via chat/phone
- Auto-score leads based on form responses
- Auto-assign to sales rep based on territory/size
- Auto-create calendar holds for follow-ups

**Agent Script Library Needed:**
- Opening script for cold leads
- Qualification question sequence
- Objection handling (price, timing, competitor)
- Voicemail scripts (3 variations)
- "Break-up" email template

---

## Real-World Testing Results

**Test Scenario 1:** Website form submission - Restaurant chain, 8 locations
- Response time: 3 minutes (text)
- Qualified: YES (Hot - 85 points)
- Outcome: Demo scheduled next day
- **PASS**

**Test Scenario 2:** Email inquiry - "Just looking for prices"
- Response time: 12 minutes (email)
- Qualified: WARM (52 points) after probing
- Outcome: Sent quote, follow-up scheduled
- **PASS**

**Test Scenario 3:** After-hours voicemail - Single location coffee shop
- Response time: Next morning 8:03 AM
- Qualified: COLD (35 points)
- Outcome: Added to nurture sequence
- **PASS**

**Test Scenario 4:** Competitor mention - Using Toast, unhappy
- Response time: 8 minutes (call)
- Qualified: HOT (90 points) - switching pain
- Outcome: Emergency quote, demo same week
- **PASS**

---

## Appendix A: Initial Email Template

**Subject:** Re: Your [Product] Inquiry - Performance Supply Depot

Hi [First Name],

Thanks for reaching out about [product/service]. Based on what you shared, I think we can definitely help.

Quick question: Are you currently using [current system/competitor], or is this for a new location/setup?

The reason I ask is that [personalized insight based on their business type].

I have a few ideas that could [benefit - save money, speed up service, etc.]. Do you have 10 minutes for a quick call this week? I'm free [time options].

Either way, I'll send over some information that might be helpful.

Best,
[Agent Name]
Performance Supply Depot
[Phone] | [Email]

P.S. [Personalized PS - e.g., "I noticed you're in [city] - we just helped another restaurant there streamline their checkout process."]

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-07-23 | 1.0 | Initial SOP created | Miles (AOS) |
| | | Ready for Patricia review | |

---

**APPROVAL SIGNATURE:** _________________ Date: ____________

**NEXT REVIEW DATE:** 2026-10-23 (Quarterly)
