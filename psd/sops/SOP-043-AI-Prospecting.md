# SOP-004: AI-Powered Prospecting

## Document Control
| Field | Value |
|-------|-------|
| SOP ID | SOP-004 |
| Version | 1.0 |
| Created | 2026-07-24 |
| Author | Miles (AGI Sales Consultant) |
| Review Cycle | Quarterly |
| Status | DRAFT |

---

## Purpose
Define the AI-powered prospecting workflow that automates Ideal Customer Profile (ICP) identification, lead list generation, and contact research at scale.

**Target:** 10,000+ qualified prospects identified per quarter with 80%+ accuracy match to ICP.

---

## Scope

### Applies To
- AI prospecting agents (Manis.AI, custom scrapers)
- Sales development representatives (SDRs)
- Sales managers reviewing lead quality

### Does NOT Cover
- Manual cold outreach (see SOP-001)
- Lead qualification (see SOP-005)

---

## Definitions

| Term | Definition |
|------|------------|
| ICP | Ideal Customer Profile - detailed description of perfect-fit customer |
| Lead List | Curated database of prospects matching ICP criteria |
| Contact Enrichment | Adding phone, email, social profiles to lead records |
| 10-80-10 Rule | Dan Martell's framework: 10% ideation, 80% AI execution, 10% human integration |

---

## Phase 1: ICP Definition (10% - Human Ideation)

### Step 1.1: Gather Current Customer Data
**Owner:** Sales Manager + AI Agent
**Time:** 60 minutes

**Actions:**
1. Export current customer database (last 12 months)
2. Identify top 20% of customers by revenue
3. Document common attributes:
   - Industry/vertical
   - Company size (employees/revenue)
   - Geographic location
   - Job titles of buyers
   - Common pain points
   - Tech stack (if applicable)

**Output:** `ICP-Profile-[DATE].md`

### Step 1.2: Enrich with AI Analysis
**Owner:** AI Agent (Manis.AI or custom)
**Time:** 30 minutes

**Prompt Template:**
```
Analyze the attached customer database and identify patterns that define our Ideal Customer Profile. Focus on:
- Demographic patterns
- Firmographic patterns  
- Behavioral patterns
- Buying triggers
- Common objections overcome

Output a 1-page ICP document with specific criteria for scoring leads (1-10 scale).
```

**Output:** `ICP-Scoring-Rubric.md`

### Step 1.3: Human Review & Approval
**Owner:** Sales Manager
**Time:** 30 minutes

**Actions:**
1. Review AI-generated ICP
2. Adjust scoring weights based on intuition/experience
3. Approve final ICP profile
4. Store in shared drive: `/sops/icp/`

**Success Criteria:**
- [ ] ICP matches 80%+ of current top customers
- [ ] Scoring rubric is clear and actionable
- [ ] Team has reviewed and agrees

---

## Phase 2: AI Lead Generation (80% - Automated Execution)

### Step 2.1: Configure AI Prospecting Tool
**Owner:** Sales Ops
**Time:** 45 minutes (one-time setup)

**Configuration (Manis.AI example):**
```json
{
  "icp_profile": "/sops/icp/ICP-Profile-[DATE].md",
  "scoring_rubric": "/sops/icp/ICP-Scoring-Rubric.md",
  "geography": ["US", "Canada"],
  "company_size": "50-500 employees",
  "titles": ["Owner", "Manager", "Director", "VP Operations"],
  "exclude": ["competitors", "current customers", "unsubscribes"],
  "enrichment": {
    "linkedin": true,
    "instagram": true,
    "phone": true,
    "email": true,
    "company_revenue": true
  }
}
```

### Step 2.2: Launch Lead Research Campaign
**Owner:** AI Agent
**Time:** 24-72 hours (automated)

**Actions:**
1. AI scans databases, LinkedIn, company websites
2. Matches companies against ICP criteria
3. Identifies decision-makers within target companies
4. Enriches contact data with social profiles
5. Scores each lead 1-10 based on ICP match

**Output:** `Lead-List-[BATCH-ID].csv`

**CSV Structure:**
```csv
lead_id,company_name,industry,employees,decision_maker,title,linkedin_url,instagram_handle,phone,email,icp_score,source,timestamp
```

### Step 2.3: Batch Quality Control
**Owner:** AI Agent (automated) + Human spot-check
**Time:** Ongoing

**Automated Filters:**
- ICP score >= 7 (Hot leads)
- ICP score 4-6 (Warm leads - review)
- ICP score < 4 (Cold leads - discard)
- Email deliverability check
- Phone validation
- Deduplication against existing database

**Human Spot-Check:**
- Review 20 random Hot leads
- Verify contact accuracy
- Adjust AI parameters if < 80% accuracy

---

## Phase 3: Human Integration (10% - Review & Route)

### Step 3.1: Lead Queue Review
**Owner:** Sales Manager
**Time:** 30 minutes daily

**Actions:**
1. Review new Hot leads (ICP score 8-10)
2. Quick "sniff test" - does this feel right?
3. Approve for outreach or flag for review
4. Assign to appropriate SDR/sales rep

**Routing Rules:**
| ICP Score | Action | Owner |
|-----------|--------|-------|
| 9-10 | Immediate outreach | Senior Closer |
| 7-8 | Qualified outreach | SDR |
| 4-6 | Nurture sequence | Marketing |
| < 4 | Discard / Research only | Archive |

### Step 3.2: Feedback Loop
**Owner:** Sales Manager + AI Agent
**Time:** Weekly

**Actions:**
1. Track conversion rates by ICP score
2. Identify false positives (high score, low conversion)
3. Identify missed opportunities (low score, high conversion)
4. Feed learnings back to ICP profile
5. Retrain AI model monthly

**Success Metrics:**
- Hot lead (9-10) conversion to qualified: > 40%
- Warm lead (7-8) conversion to qualified: > 20%
- Data accuracy (valid contacts): > 85%

---

## Automation Notes

### AI Agent Configuration (DepotChaos Integration)
```python
prospecting_config = {
    "agent_name": "Prospector-1",
    "model": "Mort_II:latest",  # For social profile analysis
    "tools": [
        "linkedin_scraper",
        "company_db_lookup",
        "email_verifier",
        "phone_validator"
    ],
    "daily_quota": 500,  # Leads to process
    "enrichment_depth": "full",  # social + contact + company
    "output_queue": "qualified_leads"
}
```

### Integration Points
- **Input:** ICP profiles, exclusion lists
- **Output:** Lead lists → CRM → SOP-005 (Qualifying)
- **Triggers:** Daily batch runs, real-time webhook on ICP match

---

## Scripts & Templates

### ICP Definition Workshop Script
```
"Let's identify our perfect customer. Looking at our top 20 customers by revenue:

1. What industry are they in?
2. How big are their companies?
3. What's their annual revenue?
4. Who's the decision maker?
5. What problem were they trying to solve?
6. Why did they choose us vs competitors?

Now, what patterns do you see? Let's build our ICP together."
```

### Lead Handoff Template (to SDR)
```
NEW HOT LEAD - ICP Score: [9/10]

Company: [Name]
Industry: [Industry]
Decision Maker: [Name], [Title]
Contact: [Phone] | [Email]
LinkedIn: [URL]

Why they're Hot:
- [Specific ICP match reason 1]
- [Specific ICP match reason 2]

Suggested Opening:
"Hi [Name], I noticed [Company] recently [trigger event]. We help [industry] companies like [similar customer] with [solution]. Worth a quick conversation?"

Next Step: See SOP-005 for qualifying sequence.
```

---

## Quality Assurance

### Daily Checklist (Sales Manager)
- [ ] Review 20 random new leads for accuracy
- [ ] Check ICP score distribution (should be 70% 7+, 20% 4-6, 10% <4)
- [ ] Verify top 10 Hot leads are truly qualified
- [ ] Note any pattern issues for AI retraining

### Weekly Review
- [ ] Conversion rates by ICP score bracket
- [ ] Data accuracy report
- [ ] ICP profile updates based on learnings
- [ ] AI tool performance review

---

## Related Documents
- SOP-001: Lead Response & Qualification (next step)
- ICP-Profile-[DATE].md (living document)
- `/sops/icp/` (central ICP repository)

---

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-24 | Miles | Initial creation based on Dan Martell 5-phase framework |

---

**Next Review Date:** 2026-10-24
