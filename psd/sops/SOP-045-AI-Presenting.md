# SOP-006: AI-Powered Proposal Generation & Presenting

## Document Control
| Field | Value |
|-------|-------|
| SOP ID | SOP-006 |
| Version | 1.0 |
| Created | 2026-07-24 |
| Author | Miles (AGI Sales Consultant) |
| Review Cycle | Monthly |
| Status | DRAFT |

---

## Purpose
Use AI to generate personalized sales proposals from CRM data, transcripts, and research. Deliver proposals human-to-human on scheduled calls for maximum conversion.

**Target:** Custom proposal generated in < 10 minutes, 35%+ close rate on presented offers.

**Key Principle:** "Never send a proposal. Always schedule the call to review it."

---

## Scope

### Applies To
- AI proposal generation (ChatGPT/Mort_II)
- Sales reps delivering proposals
- Sales managers reviewing proposal quality

### Does NOT Cover
- Standard quote generation (see SOP-002)
- Order processing (see SOP-003)

---

## Definitions

| Term | Definition |
|------|------------|
| Proposal | Customized sales presentation addressing specific prospect pain points |
| VSL | Video Sales Letter - short video agitating pain and presenting solution |
| Agitation | Amplifying the prospect's pain/problem before presenting solution |
| Talk Track | Scripted talking points for sales conversation |

---

## Phase 1: Pre-Call Preparation (AI-Generated)

### Step 1.1: Gather Intelligence
**Trigger:** Calendar booking confirmed
**Owner:** AI Agent (automated)
**Time:** 5 minutes

**Data Sources:**
1. CRM record (from SOP-005)
2. Qualification call transcript
3. Additional internet research (LinkedIn, company website)
4. Similar customer case studies
5. Product catalog data

**AI Intelligence Gathering Prompt:**
```
Research [Company Name] and [Decision Maker Name]. Find:
- Company size, revenue, locations
- Recent news or expansions
- Current POS setup (if mentioned online)
- Decision maker's background
- Any pain signals (complaints, reviews, etc.)

Output: 1-page briefing document.
```

### Step 1.2: Generate Custom Proposal
**Owner:** AI Agent
**Time:** 3-5 minutes

**System Prompt:**
```
You are an expert sales consultant for Performance Supply Depot. Create a personalized proposal for this prospect.

PROSPECT INFO:
- Company: {company_name}
- Industry: {industry}
- Locations: {num_locations}
- Decision Maker: {decision_maker_name}, {title}
- Pain Points: {pain_points}
- Budget: {budget_confirmed}
- Timeline: {timeline}

RESEARCH NOTES:
{research_brief}

TEMPLATE OFFER:
{offer_template}

OUTPUT REQUIREMENTS:
1. Pain Agitation (2-3 paragraphs describing their specific pain better than they can)
2. Solution Presentation (how PSD solves each pain point)
3. Specific Product Recommendations (tailored to their needs)
4. Pricing (within their budget range)
5. Social Proof (case study of similar customer)
6. Clear Call to Action

TONE: Consultative, energetic, professional (Miles style)
LENGTH: 1-2 pages
```

### Step 1.3: Generate Talk Track
**Owner:** AI Agent
**Time:** 2 minutes

**Talk Track Prompt:**
```
Based on the proposal above, create a talk track for the sales call.

Include:
1. Opening hook (30 seconds)
2. Pain agitation questions (3-4)
3. Solution walkthrough (key talking points)
4. Objection responses (likely objections + responses)
5. Closing sequence
6. Next steps

Format: Bullet points with suggested phrasing.
```

**Output Package:**
- `Proposal-[PROSPECT]-[DATE].pdf`
- `TalkTrack-[PROSPECT]-[DATE].md`
- `Briefing-[PROSPECT]-[DATE].md`

---

## Phase 2: The Presentation Call

### Step 2.1: Pre-Call Setup (5 minutes before)
**Owner:** Sales Rep

**Checklist:**
- [ ] Review proposal (skim, don't memorize)
- [ ] Review talk track (know key points)
- [ ] Open CRM to take notes
- [ ] Have proposal PDF ready to screen share
- [ ] Test audio/video if virtual

### Step 2.2: Call Structure (30-45 minutes)

| Phase | Duration | Owner | Activity |
|-------|----------|-------|----------|
| Rapport | 5 min | Human | "How's business?" "How'd that expansion go?" |
| Agenda | 2 min | Human | "Here's what I'd like to cover..." |
| Pain Agitation | 10 min | Human + AI Talk Track | Deep dive into pain points using AI-generated questions |
| Solution | 10 min | Human | Present proposal, screen share PDF |
| Objections | 10 min | Human | Handle concerns (see SOP-007) |
| Close | 5 min | Human | Ask for the business |
| Next Steps | 3 min | Human | Confirm action items |

### Step 2.3: Proposal Delivery Script

**Opening Hook:**
```
"Thanks for taking the time today, [Name]. I spent some time looking into [Company] and I've got to say, I'm excited about what you're building.

Before I show you what I put together, I want to make sure I understand your situation correctly...

From what [AI Agent] told me, you're dealing with [pain point 1] and [pain point 2]. Is that right?

[pause]

And how is that impacting your day-to-day operations?"
```

**Solution Presentation:**
```
"Here's what I put together for you...

[Screen share proposal]

I looked at your [specific detail from research], and I thought about what [similar customer] went through. They were dealing with the same thing.

So here's my recommendation..."
```

---

## Phase 3: Post-Call Actions

### Step 3.1: Immediate Follow-Up (within 1 hour)
**Owner:** Human Sales Rep

**Email Template:**
```
Subject: Our conversation today + next steps

Hi [Name],

Thanks for taking the time today. Great conversation about [Company].

As promised, attached is the proposal we reviewed.

Key points we covered:
- [Bullet 1 from proposal]
- [Bullet 2 from proposal]
- [Pricing]

Next steps: [specific action agreed upon]

Questions? Just reply to this email or call me at [phone].

Looking forward to working together,

[Name]
Performance Supply Depot
```

### Step 3.2: AI-Generated Case Study Video (Optional)
**Owner:** AI Agent
**Time:** 10 minutes generation

**Use Case:** For prospects who need social proof or want to share with team

**VSL Prompt:**
```
Create a 2-minute video script for a sales video addressing [specific prospect pain points].

Structure:
1. Hook (5 sec) - "Are you tired of...?"
2. Agitation (30 sec) - Describe the pain vividly
3. Solution (45 sec) - How PSD solved it for [similar customer]
4. Proof (30 sec) - Specific results/numbers
5. CTA (10 sec) - "Ready to solve this?"

Generate script + suggested visuals.
```

---

## Proposal Template Library

### Template 1: Restaurant/Bar
**Pain Points:** Running out of receipt paper during rush, slow supplier delivery
**Products:** Thermal rolls, liquor pourers, cleaning supplies
**Value Prop:** Never run out, 24-hour delivery guarantee

### Template 2: Retail Chain
**Pain Points:** Inconsistent quality across locations, complex ordering
**Products:** Custom labels, branded bags, inventory management
**Value Prop:** Centralized ordering, location-specific delivery

### Template 3: New Business Opening
**Pain Points:** Don't know what they need, tight timeline
**Products:** Starter kit consultation, setup checklist
**Value Prop:** Complete setup in 48 hours, ongoing support

---

## Quality Metrics

### Per-Proposal Tracking
| Metric | Target |
|--------|--------|
| Generation time | < 10 minutes |
| Proposal quality score | > 8/10 |
| Call-to-close rate | > 35% |
| Avg deal size | > $2,000 |
| Proposal-to-meeting conversion | > 80% |

### Review Process
**Weekly:**
- Sales manager reviews 5 random proposals
- Score against rubric (1-10)
- Provide feedback to AI training

**Monthly:**
- Analyze closed-won vs closed-lost proposals
- Identify patterns in successful proposals
- Update templates and prompts

---

## Automation Notes

### AI Agent Configuration
```python
proposal_config = {
    "agent_name": "DepotProposal-1",
    "model": "qwen2.5:14b",  # Deep reasoning for custom proposals
    "voice_model": "Mort_II:latest",  # For VSL generation
    "capabilities": [
        "research",
        "proposal_generation",
        "talk_track_generation",
        "vsl_script_creation"
    ],
    "templates": [
        "restaurant_bar",
        "retail_chain", 
        "new_business",
        "custom"
    ],
    "output_formats": ["pdf", "md", "talk_track"],
    "max_proposal_length": "2_pages"
}
```

### Integration Points
- **Input:** Qualified lead data from SOP-005
- **Output:** Closed deals → Order processing, Lost deals → Nurture

---

## Related Documents
- SOP-005: AI Qualifying (input)
- SOP-007: AI Objection Handling (support)
- `/sops/proposals/templates/`

---

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-24 | Miles | Initial creation |

---

**Next Review Date:** 2026-08-24
