# SOP-005: AI-Powered Lead Qualifying

## Document Control
| Field | Value |
|-------|-------|
| SOP ID | SOP-005 |
| Version | 1.0 |
| Created | 2026-07-24 |
| Author | Miles (AGI Sales Consultant) |
| Review Cycle | Monthly |
| Status | DRAFT |

---

## Purpose
Automate lead qualification using AI voice/chat agents to pre-qualify prospects before booking calendar time. Eliminate unqualified calls and recover 95% of sales time.

**Target:** 95% reduction in unqualified calls, 80%+ of calendar filled with qualified buyers only.

---

## Scope

### Applies To
- AI qualifying agents (voice/chat)
- Sales reps receiving qualified appointments
- Sales managers monitoring qualification quality

### Does NOT Cover
- Prospecting (see SOP-004)
- Sales presentation (see SOP-006)
- Manual qualification (only use if AI unavailable)

---

## Definitions

| Term | Definition |
|------|------------|
| Qualified Lead | Prospect with confirmed pain point, budget, authority, and timeline |
| BANT | Budget, Authority, Need, Timeline qualification framework |
| Ghosted Lead | Prospect who booked but didn't show or respond |
| Spam Filter | AI gatekeeper preventing unqualified leads from booking |

---

## Phase 1: AI Qualification Setup (One-Time)

### Step 1.1: Define Qualification Criteria
**Owner:** Sales Manager
**Time:** 60 minutes

**PSD-Specific BANT Criteria:**

**Budget:**
- Minimum order: $500
- Typical order: $1,000-$5,000
- Enterprise: $10,000+

**Authority:**
- Decision maker: Owner, GM, VP Operations, Purchasing Manager
- Influencer: Floor manager, bartender (route to decision maker)
- Blocker: Route around or disqualify

**Need:**
- Current POS supplies running low
- Expanding locations
- Switching suppliers (pain with current)
- New business opening

**Timeline:**
- Urgent: Need within 1 week
- Active: Need within 1 month
- Future: 1-3 months (nurture)
- Research: No timeline (low priority)

### Step 1.2: Configure AI Qualification Flow
**Owner:** Sales Ops
**Time:** 90 minutes

**Voice AI Configuration (your.com pattern):**

```yaml
agent_name: "DepotQual-1"
voice: "Adam"  # Deep, energetic, professional
language: "English"
tone: "consultative"

qualification_flow:
  greeting: "Hi, this is Miles from Performance Supply Depot. I hope I'm not catching you at a bad time?"
  
  permission_check: "Do you have 2 minutes for a quick conversation about your supply needs?"
  
  discovery_questions:
    - "What type of business are you running?"
    - "How many locations do you have?"
    - "What POS supplies are you currently using?"
    - "Are you happy with your current supplier?"
    - "When do you typically need to restock?"
    - "What's your monthly spend on supplies?"
    - "Who makes the purchasing decisions?"
    
  qualification_logic:
    if budget >= 500 AND authority == "yes" AND need == "confirmed" AND timeline <= 30_days:
      action: "offer_calendar"
    elif need == "confirmed" AND timeline > 30_days:
      action: "nurture_sequence"
    else:
      action: "polite_disqualify"
      
  calendar_integration:
    provider: "calendly"  # or acuity, custom
    calendar: "sales@psdepot.com"
    buffer: "15 minutes"
    
  handoff_message: "Great! I've found a time that works. You'll get a confirmation email with meeting details. Looking forward to speaking with you!"
```

### Step 1.3: Test & Refine
**Owner:** Sales Manager + AI Agent
**Time:** 2 hours

**Test Scenarios:**
1. **Hot Lead:** Has budget, authority, immediate need
2. **Warm Lead:** Has need, no immediate timeline
3. **Cold Lead:** Just researching, no real need
4. **Complicated Lead:** Multiple locations, complex requirements
5. **Difficult Lead:** Short answers, vague responses

**Refinement Checklist:**
- [ ] AI asks all BANT questions naturally
- [ ] AI handles objections gracefully
- [ ] Transcription accuracy > 95%
- [ ] Calendar booking works seamlessly
- [ ] CRM integration captures all data

---

## Phase 2: Live Qualification Process

### Step 2.1: Lead Ingest
**Trigger:** New Hot Lead from SOP-004
**Owner:** AI Agent (automated)

**Actions:**
1. Lead enters qualification queue
2. AI determines best contact method (phone/email/chat)
3. Initiates outreach within 5 minutes

### Step 2.2: AI Voice Qualification Call
**Owner:** AI Agent
**Duration:** 3-5 minutes

**Call Flow:**

| Time | Agent | Script/Action |
|------|-------|---------------|
| 0:00 | AI | "Hi, this is Miles from Performance Supply Depot. I hope I'm not catching you at a bad time?" |
| 0:05 | Prospect | Response |
| 0:10 | AI | If good time: "Great! You just popped up on my calendar. Are you looking for POS supplies?" |
| 0:30 | Prospect | Response |
| 0:45 | AI | "What type of business are you running?" |
| 1:00 | Prospect | [Business type] |
| 1:15 | AI | "How many locations? And what's your monthly spend on supplies like receipt paper, labels, that sort of thing?" |
| 1:45 | Prospect | [Budget info] |
| 2:00 | AI | "Got it. Are you the person who handles purchasing, or should I be talking to someone else?" |
| 2:15 | Prospect | [Authority info] |
| 2:30 | AI | "When do you typically need to restock? Any urgency here?" |
| 2:45 | Prospect | [Timeline] |
| 3:00 | AI | **If qualified:** "Perfect. Sounds like we can definitely help. Let me get you scheduled with our team. When's a good time this week?" |
| 3:30 | AI | **If not qualified:** "I appreciate your time. I'll send you some info via email, and feel free to reach out when you're ready to move forward." |

### Step 2.3: Qualification Scoring
**Owner:** AI Agent (automated)

**Scoring Matrix:**

| Criteria | Points | Evidence Required |
|----------|--------|-------------------|
| Budget confirmed | 25 | Specific $ amount or range |
| Decision maker | 25 | Named as purchaser/owner |
| Need confirmed | 25 | Specific pain or requirement stated |
| Timeline < 30 days | 15 | Specific date or "ASAP" |
| Multiple locations | 10 | 2+ locations |
| **TOTAL** | **100** | |

**Routing:**
- 80-100 points: Book immediately with Senior Closer
- 60-79 points: Book with SDR for further qualification
- 40-59 points: Nurture sequence
- < 40 points: Archive (check again in 90 days)

### Step 2.4: CRM Update & Handoff
**Owner:** AI Agent (automated)

**Actions:**
1. Transcribe full call
2. Extract key data points
3. Update CRM record
4. Create calendar event with context
5. Notify assigned sales rep

**CRM Fields Updated:**
```json
{
  "lead_status": "Qualified",
  "qualification_score": 85,
  "discovery_notes": "Full transcript here...",
  "budget_confirmed": 2500,
  "decision_maker": "John Smith, Owner",
  "pain_points": ["Current supplier slow", "Running low on stock"],
  "timeline": "ASAP - running low",
  "next_action": "Booked for 2026-07-25 2pm",
  "call_recording": "[link]",
  "ai_confidence": 0.92
}
```

---

## Phase 3: Human Review & Backup

### Step 3.1: Pre-Call Review (5 minutes before)
**Owner:** Sales Rep
**Time:** 5 minutes

**Review Checklist:**
- [ ] Read AI discovery notes
- [ ] Listen to key call segments (if needed)
- [ ] Check BANT scores
- [ ] Prepare tailored opening
- [ ] Note any red flags from AI

### Step 3.2: Feedback to AI
**Owner:** Sales Rep
**Time:** 2 minutes post-call

**Feedback Form:**
```
Qualification Accuracy:
[ ] Perfect - exactly as described
[ ] Good - minor details off
[ ] Fair - some misqualification
[ ] Poor - completely wrong

Notes for AI improvement:
___________________________
```

---

## Ghosted Lead Recovery

### Trigger: No-show or no-response within 24 hours

### Recovery Sequence:

**Hour 24:** AI Email
```
Subject: Did I catch you at a bad time?

Hi [Name],

I hope I'm not catching you at a bad time. We were scheduled to talk about your POS supply needs yesterday.

If now isn't a good time, no worries - just reply with "LATER" and I'll circle back in a few weeks.

If you're still interested, here's my calendar: [link]

Best,
Miles
Performance Supply Depot
```

**Day 3:** AI Email
```
Subject: Quick question about [Company]

Hi [Name],

Quick question - are you still looking for a POS supplies partner, or should I close out your file?

Just reply "YES" if you're still interested, or "NO" if you've got it handled.

Thanks,
Miles
```

**Day 7:** Final AI Email
```
Subject: Last follow-up

Hi [Name],

This is my last follow-up. If you're still interested in supplies for [Company], book a time here: [link]

If not, no hard feelings - good luck with your business!

Miles
```

**Day 14:** Archive as "Nurture"

---

## Automation Notes

### AI Agent Configuration (DepotChaos)
```python
qualifying_config = {
    "agent_name": "DepotQual-1",
    "voice": "Adam",
    "model": "Mort_II:latest",
    "capabilities": [
        "voice_call",
        "transcription",
        "sentiment_analysis",
        "calendar_booking",
        "crm_update"
    ],
    "qualification_rubric": "bant_v2",
    "min_qualification_score": 60,
    "max_call_duration": 600,  # seconds
    "follow_up_enabled": True,
    "ghost_recovery_enabled": True
}
```

### Integration Points
- **Input:** Hot leads from SOP-004
- **Output:** Qualified appointments → SOP-006 (Presenting)
- **Side Output:** Nurture leads → Marketing automation

---

## Scripts & Templates

### Opening Script (AI Voice)
```
"Hi, this is Miles from Performance Supply Depot. I hope I'm not catching you at a bad time?

[pause for response]

Great! You just popped up on my calendar. I was just checking in to see if you need anything - specifically around POS supplies like receipt paper, labels, or bar supplies?

[pause]

Actually, let me ask you a couple quick questions so I can make sure I'm not wasting your time..."
```

### Disqualification Script (Graceful Exit)
```
"I totally understand. Sounds like now might not be the right time, and that's okay. 

What I'll do is send you our catalog via email - no pressure, just so you have it when you need it. And if things change, just reply to that email or give us a call.

Sound fair?"
```

### Calendar Booking Script
```
"Perfect! Based on what you told me, I think we can definitely help. Let me get you scheduled with our team.

I see [day] at [time] works - does that still work for you?

[confirm]

Great! You'll get a confirmation email with all the details. Looking forward to speaking with you then. Have a great day!"
```

---

## Quality Assurance

### Daily Metrics (Automated Dashboard)
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Leads qualified | 20/day | < 15 |
| Qualification rate | 60% | < 50% |
| Avg qualification score | 75 | < 65 |
| Calendar bookings | 12/day | < 8 |
| Show rate | 80% | < 70% |
| Ghost recovery rate | 25% | < 15% |

### Weekly Review (Sales Manager)
- [ ] Listen to 5 random AI qualification calls
- [ ] Review 10 disqualified leads - any false negatives?
- [ ] Check ghost recovery performance
- [ ] Update qualification criteria based on learnings
- [ ] Refine AI scripts based on feedback

---

## Related Documents
- SOP-004: AI Prospecting (input)
- SOP-006: AI-Powered Presenting (output)
- `/sops/qualification/bant-rubric.md`

---

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-24 | Miles | Initial creation based on Dan Martell framework |

---

**Next Review Date:** 2026-08-24
