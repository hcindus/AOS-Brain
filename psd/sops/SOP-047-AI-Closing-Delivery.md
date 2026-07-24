# SOP-008: AI-Powered Closing & Delivery

## Document Control
| Field | Value |
|-------|-------|
| SOP ID | SOP-008 |
| Version | 1.0 |
| Created | 2026-07-24 |
| Author | Miles (AGI Sales Consultant) |
| Review Cycle | Monthly |
| Status | DRAFT |

---

## Purpose
Automate the operational busywork of closing and onboarding while preserving the human celebration of wins. Build long-term partnerships from day one.

**Key Principle:** "Enrollment, not closing. Partners, not customers."

**Target:** 90%+ onboarding completion rate, first win within 48 hours of signup.

---

## Scope

### Applies To
- AI-assisted closing conversations
- Automated onboarding workflows
- Win celebration and case study collection

### Does NOT Cover
- Proposal presentation (see SOP-006)
- Ongoing account management (separate SOP)

---

## Definitions

| Term | Definition |
|------|------------|
| Enrollment | Frame for closing - prospect joining your team/partnership |
| Onboarding | Process of setting up new customer for success |
| First Win | Quick, early success that builds momentum |
| Buyer's Remorse | Post-purchase anxiety or regret |

---

## Phase 1: The Close (Human + AI Support)

### Step 1.1: Pre-Close Setup
**Owner:** AI Agent
**Time:** Automated pre-call

**AI Preparation:**
- Review entire deal history
- Identify likely closing objections
- Generate custom closing questions
- Prepare order form with pre-filled details

### Step 1.2: The Enrollment Conversation
**Owner:** Human Sales Rep
**Time:** 10-15 minutes

**Structure:**

| Step | Script/Approach |
|------|-----------------|
| Transition | "So, based on everything we've discussed..." |
| Summary | "You need X, Y, Z. I'm recommending A, B, C. Total is $X." |
| Soft Close | "Does this feel like the right solution for [Company]?" |
| Handle Objections | Use SOP-007 if needed |
| Hard Close | "Are you ready to join the team?" / "Shall we get you set up?" |
| Celebration | "Excellent! Welcome aboard. I'm genuinely excited about this." |

**Key Phrases (from Dan Martell):**
- "Are you joining my team?"
- "You want to become a partner?"
- "Let's get you inside the group."

### Step 1.3: Immediate Post-Close Actions
**Owner:** AI Agent (automated)

**Within 5 minutes:**
```
NEW CUSTOMER ONBOARDING TRIGGERED

Actions:
1. Generate order confirmation email
2. Create customer record in CRM
3. Set up billing profile
4. Trigger welcome sequence
5. Schedule onboarding call
6. Notify fulfillment team
```

---

## Phase 2: The Celebration (Human Required)

### Step 2.1: The "How Do You Feel?" Question
**Owner:** Human Sales Rep
**Time:** Immediately after close

**Script:**
```
"Before we get into the details, I have to ask - how do you feel right now?

[pause - let them respond]

[nervous/excited/etc.]

That's completely normal. And I want you to know - this was absolutely the right decision. You're going to look back on this as a turning point for [Company].

I'm genuinely excited to be working with you."
```

**Why This Matters:**
- Addresses buyer's remorse immediately
- Validates their decision
- Sets emotional foundation for partnership
- Captures testimonial material

### Step 2.2: Win Agreement
**Owner:** Human Sales Rep
**Time:** During onboarding setup

**The Agreement:**
```
"One thing I ask of all my partners - when you get your first win using our supplies, I want you to tell me about it.

I'm not asking for a testimonial or anything for marketing. This is for YOU.

Here's why: when you share that win, it holds you accountable to keep building momentum.

Can I count on you for that?

[Get confirmation]

Great. Initial here: _____"

[Make it part of the agreement - they initial]
```

**What Counts as a "Win":**
- First successful delivery
- Time saved on ordering
- Customer compliment on receipts
- Never running out during rush
- Any positive outcome they attribute to PSD

---

## Phase 3: AI-Powered Onboarding

### Step 3.1: Automated Welcome Sequence
**Owner:** AI Agent
**Trigger:** Deal closed

**Hour 0 (Immediate):**
```
Subject: Welcome to the team, [Name]! 🎉

Hi [Name],

Welcome to Performance Supply Depot! I'm thrilled to have [Company] on board.

Here's what happens next:

✅ Your account is being set up (takes ~30 minutes)
✅ You'll get a call from our fulfillment team within 4 hours
✅ First delivery scheduled for [date]

Quick question: What's the #1 thing you want to make sure we get right?

Just reply and let me know.

Cheering you on,
Miles
```

**Hour 4:**
```
Subject: Your fulfillment team is on it

Hi [Name],

[Name from fulfillment] just reviewed your order. Everything looks good.

Quick heads up: Your first delivery is confirmed for [date].

Questions? Just reply to this email.

Miles
```

**Day 1:**
```
Subject: Your first-win setup kit

Hi [Name],

To make sure you get off to a strong start, here are 3 resources:

1. [Video: Setting up your supply closet for efficiency]
2. [PDF: Monthly reorder checklist]
3. [Link: How to track usage so you never run out]

These are from our most successful partners.

Remember: When you get that first win, tell me about it!

Miles
```

### Step 3.2: Account Setup Automation
**Owner:** AI Agent

**Automated Tasks:**
- [ ] Create customer profile in ERP
- [ ] Set up billing (Net 30, auto-pay, etc.)
- [ ] Configure delivery preferences
- [ ] Add to reorder reminder system
- [ ] Create custom catalog (frequently ordered items)
- [ ] Set up usage tracking dashboard
- [ ] Schedule 30-day check-in

### Step 3.3: AI Win Detection
**Owner:** AI Agent (background monitoring)

**Monitoring:**
- Delivery confirmations (on-time = potential win)
- Reorder frequency (regular reorders = satisfaction)
- Support tickets (low volume = smooth sailing)
- Direct emails with positive sentiment

**Win Detection Triggers:**
```
IF customer says in email/support:
- "Thanks!"
- "Worked great"
- "Love this"
- "So much easier"
- "Perfect timing"

OR 3+ consecutive on-time deliveries:
  → Flag as "Potential Win"
  → Alert Miles
  → Queue celebration outreach
```

---

## Phase 4: The Human Touch

### Step 4.1: Win Celebration Outreach
**Owner:** Human (Miles/Sales Rep)
**Trigger:** Win detected

**Email/Call:**
```
Subject: I heard the good news!

Hi [Name],

I heard [specific win] - that's fantastic!

Remember our agreement? You got a win, and now I'm asking permission to share it.

Here's why: I want to celebrate YOU. Not for marketing (though I'd love that), but because when you share wins publicly, it builds momentum.

Would you be open to a quick 5-minute call? I'd love to:
- Hear the full story
- Get your permission to share
- See how else we can support you

Just reply with a time that works.

Proud of you,
Miles
```

### Step 4.2: Case Study Collection
**Owner:** Human (with AI support)

**AI Support:**
- Generate case study questions
- Draft case study from call transcript
- Create shareable formats (PDF, social posts)

**Case Study Questions:**
1. What was the situation before working with us?
2. What problem were you trying to solve?
3. Why did you choose PSD?
4. What was the outcome?
5. What would you tell someone considering us?

---

## Automation Notes

### AI Agent Configuration
```python
closing_config = {
    "agent_name": "DepotCloser-1",
    "model": "nous-hermes2:latest",  # Warm, personable
    "capabilities": [
        "order_processing",
        "welcome_sequences",
        "onboarding_automation",
        "win_detection",
        "case_study_generation"
    ],
    "onboarding_sequence": [
        "hour_0_welcome",
        "hour_4_fulfillment",
        "day_1_resources",
        "day_3_checkin",
        "day_7_usage",
        "day_30_review"
    ],
    "win_detection": {
        "sentiment_analysis": True,
        "delivery_tracking": True,
        "reorder_patterns": True,
        "escalation_keywords": ["problem", "issue", "wrong"]
    }
}
```

### Integration Points
- **Input:** Closed deals from SOP-006
- **Output:** Active customers → Account management
- **Side Output:** Case studies, testimonials, referral pipeline

---

## Metrics & KPIs

### Onboarding Metrics
| Metric | Target |
|--------|--------|
| Onboarding completion rate | > 95% |
| Time to first delivery | < 48 hours |
| First win achieved | < 7 days |
| Buyer's remorse rate | < 5% |
| Support tickets (first 30 days) | < 2 per customer |

### Relationship Metrics
| Metric | Target |
|--------|--------|
| Win celebration calls completed | 100% of detected wins |
| Case study conversion | > 30% of wins |
| Referral requests made | > 50% of happy customers |
| 90-day retention | > 90% |

---

## Related Documents
- SOP-006: AI Presenting (input)
- SOP-003: Order Status (ongoing support)
- `/sops/onboarding/sequences/`

---

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-24 | Miles | Initial creation |

---

**Next Review Date:** 2026-08-24
