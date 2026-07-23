# SOP-002 REMEDIATION PLAN
## Quote Generation - Roast Council Feedback Integration
**Roast Score:** 5.5/10 (RESHAPE)  
**Status:** Needs simplification before automation  
**Temporal Integration:** Full workflow with human approval gates

---

## COUNCIL FEEDBACK SUMMARY

| Persona | Concern | Mitigation |
|---------|---------|------------|
| **Contrarian** | Pricing rules will break on edge cases | 10-quote manual validation first |
| **Buyer** | 35% conversion assumes perfect execution | Track actual vs target, adjust |
| **FirstPrinciples** | Core process sound | Keep structure, add validation gates |
| **Researcher** | 2hr SLA aggressive for complex quotes | Emergency vs standard tiers |
| **Expansionist** | Scale potential if automated | Phase 2 full automation after validation |

---

## SIMPLIFIED PROCESS (Phase 1)

### Before (Current - Too Complex)
```
Product Config → Pricing Engine → Approval Matrix → 
Document Gen → Email Send → Follow-up Schedule
```

### After (Simplified - Phase 1)
```
Product Selection → Manual Pricing (10 quotes) → 
Human Approval → Template Send → Calendar Hold
```

---

## TEMPORAL WORKFLOW: QuoteGenerationV2

### Workflow Diagram
```
┌─────────────────────────────────────────────────────────────┐
│  QuoteGenerationWorkflow (Simplified)                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                                           │
│  │  START       │ ◄── QuoteRequestedSignal                   │
│  └──────┬───────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────┐                                       │
│  │ Activity:        │ Validate products in stock            │
│  │ ValidateProducts │ (HubSpot API call)                    │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │ Activity:        │ Manual pricing (Phase 1)              │
│  │ CalculatePricing │ Phase 2: Rules engine                 │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐      ┌──────────────┐                │
│  │ DECISION:        │ No   │ Human Task:  │                │
│  │ Price > $1,000?  │─────►│ Pricing      │                │
│  └────────┬─────────┘      │ Approval     │                │
│           │ Yes            └──────┬───────┘                │
│           │                       │                         │
│           └───────────────────────┘                         │
│                                   │                         │
│                                   ▼                         │
│  ┌──────────────────┐                                       │
│  │ Activity:        │ Generate from template                │
│  │ GenerateQuoteDoc │ (PDF + Email HTML)                    │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │ Activity:        │ Send via email + SMS                  │
│  │ SendQuote        │ (Twilio + SendGrid)                   │
│  └────────┬─────────┘                                       │
│           │                                                 │
│           ▼                                                 │
│  ┌──────────────────┐      ┌──────────────┐                │
│  │ Timer: 2hr SLA   │─────►│ Activity:    │                │
│  │ (30min emergency)│      │ Schedule     │                │
│  └──────────────────┘      │ FollowUp     │                │
│                            └──────┬───────┘                │
│                                   │                         │
│                                   ▼                         │
│  ┌──────────────────┐                                       │
│  │ Signal:          │ Customer responded                    │
│  │ QuoteAccepted    │ or QuoteRejected                      │
│  └──────────────────┘                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Activity Definitions

#### Activity 1: ValidateProducts
```python
@activity.defn
async def validate_products(product_list: List[str]) -> Dict:
    """
    Check inventory availability via HubSpot API
    Returns: {available: bool, alternatives: List[str]}
    """
    # HubSpot API call
    # Check stock levels
    # Suggest alternatives if out of stock
    pass
```

#### Activity 2: CalculatePricing (Phase 1 - Manual)
```python
@activity.defn
async def calculate_pricing_manual(
    products: List[str],
    customer_type: str
) -> Dict:
    """
    Phase 1: Manual pricing with validation tracking
    
    Agent inputs price, system tracks for validation
    After 10 quotes, analyze variance for automation rules
    """
    return {
        "method": "manual",
        "base_price": 0,  # Agent fills
        "discount": 0,   # Agent fills
        "total": 0,      # Agent fills
        "confidence": "low"  # Until rules validated
    }
```

#### Activity 3: CalculatePricing (Phase 2 - Automated)
```python
@activity.defn
async def calculate_pricing_auto(
    products: List[str],
    customer_type: str,
    volume: int
) -> Dict:
    """
    Phase 2: Automated pricing with rules engine
    
    Rules:
    - Retail: List price
    - Wholesale: 15% discount
    - Enterprise: 25% discount + volume tiers
    - Non-profit: 10% discount
    """
    return {
        "method": "automated",
        "base_price": calculate_base(products),
        "discount": apply_rules(customer_type, volume),
        "total": 0,
        "confidence": "high"
    }
```

#### Activity 4: PricingApproval (Human Task)
```python
@activity.defn
async def pricing_approval(quote_details: Dict) -> bool:
    """
    Human-in-the-loop for quotes > $1,000
    
    Sends Slack notification to Pulp/Jordan
    Awaits approval signal
    Timeout: 30 minutes
    """
    return await workflow.execute_activity(
        notify_approver,
        quote_details,
        start_to_close_timeout=timedelta(minutes=30)
    )
```

#### Activity 5: GenerateQuoteDoc
```python
@activity.defn
async def generate_quote_document(
    quote_data: Dict,
    template: str = "standard"
) -> str:
    """
    Generate PDF and HTML versions
    
    Templates:
    - standard: Default B2B
    - emergency: Rush order highlighted
    - enterprise: Multi-year contract terms
    """
    # Jinja2 template rendering
    # PDF generation (WeasyPrint)
    # Return file paths
    pass
```

#### Activity 6: SendQuote
```python
@activity.defn
async def send_quote(
    customer_email: str,
    document_paths: Dict,
    method: str = "email"
) -> bool:
    """
    Multi-channel delivery
    
    Email: Primary (SendGrid)
    SMS: Follow-up with link (Twilio)
    """
    # SendGrid API
    # Twilio SMS
    # Track delivery status
    pass
```

#### Activity 7: ScheduleFollowUp
```python
@activity.defn
async def schedule_follow_up(
    quote_id: str,
    customer_email: str,
    timeline: str = "2_days"
) -> str:
    """
    Create calendar hold for follow-up
    
    Timeline:
    - Standard: 2 days
    - Emergency: 4 hours
    - Enterprise: 1 week (decision maker scheduling)
    """
    # Google Calendar API
    # Return calendar event ID
    pass
```

---

## SIGNALS

### Input Signals
| Signal | Payload | Trigger |
|--------|---------|---------|
| `QuoteRequested` | {products, customer_id, urgency} | HubSpot form submission |
| `PricingApproved` | {approver, timestamp} | Manager Slack approval |
| `CustomerResponded` | {response_type, notes} | Email reply received |

### Output Signals
| Signal | Payload | Recipient |
|--------|---------|-----------|
| `QuoteGenerated` | {quote_id, total, items} | CRM, Slack #sales |
| `QuoteSent` | {customer_email, timestamp} | Analytics |
| `FollowUpDue` | {quote_id, customer_id} | Sales rep calendar |

---

## QUERIES

### Available Queries
```python
@workflow.query
def get_quote_status(quote_id: str) -> str:
    """Returns: PENDING, APPROVED, SENT, ACCEPTED, REJECTED"""
    pass

@workflow.query
def get_pricing_breakdown(quote_id: str) -> Dict:
    """Returns: {base, discounts, fees, total}"""
    pass

@workflow.query
def get_approval_status(quote_id: str) -> Dict:
    """Returns: {approved: bool, approver: str, timestamp: str}"""
    pass
```

---

## ERROR HANDLING

### Retry Policy
```python
retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(minutes=10),
    maximum_attempts=3
)
```

### Compensation (Saga Pattern)
If workflow fails after quote sent:
1. Send "Quote Retracted" email
2. Void quote in system
3. Notify sales rep
4. Log for analytics

---

## SLA MONITORING

### Timer Configuration
```python
# Standard quote
workflow.set_timer(
    timedelta(hours=2),
    lambda: escalate_if_not_sent()
)

# Emergency quote
workflow.set_timer(
    timedelta(minutes=30),
    lambda: escalate_if_not_sent()
)

# Approval timeout
workflow.set_timer(
    timedelta(minutes=30),
    lambda: escalate_to_manager()
)
```

---

## PHASE 1 vs PHASE 2

### Phase 1 (Current - Validation)
- Manual pricing (agents input)
- Human approval >$1K
- Template-based documents
- 10-quote learning period

**Success Criteria:**
- 10 quotes generated
- Pricing variance <10% (ready for rules)
- 35% conversion tracked

### Phase 2 (Automation)
- Automated pricing rules
- Auto-approval <$5K
- Dynamic pricing (volume tiers)
- A/B testing templates

**Trigger:** Phase 1 success + 30-day stability

---

## IMPLEMENTATION CHECKLIST

### Week 1: Setup
- [ ] Temporal Server deployed
- [ ] Worker processes running
- [ ] HubSpot API integration
- [ ] SendGrid/Twilio configured

### Week 2: Pilot
- [ ] Generate 10 manual quotes
- [ ] Track pricing patterns
- [ ] Validate approval workflow
- [ ] Measure SLA compliance

### Week 3: Refine
- [ ] Analyze pricing variance
- [ ] Create automation rules
- [ ] Build approval dashboard
- [ ] Train sales team

### Week 4: Deploy
- [ ] Phase 2 activation
- [ ] Monitor conversion rates
- [ ] Adjust SLA timers
- [ ] Document learnings

---

## METRICS DASHBOARD

### Real-Time Queries
```sql
-- Quote conversion rate
SELECT 
    COUNT(CASE WHEN status = 'ACCEPTED' THEN 1 END) * 100.0 / COUNT(*)
FROM quotes
WHERE created_at > NOW() - INTERVAL '30 days';

-- Average time to quote
SELECT AVG(EXTRACT(EPOCH FROM (sent_at - requested_at)))/60
FROM quotes;

-- Approval bottleneck
SELECT AVG(EXTRACT(EPOCH FROM (approved_at - submitted_at)))/60
FROM quotes WHERE approval_required = true;
```

### Alert Thresholds
- Conversion <30%: Alert Pulp
- Avg time >2.5hrs: Alert Jordan
- Approval time >20min: Alert manager

---

## COUNCIL APPROVAL

**Contrarian:** ✅ Mitigated with manual validation phase  
**Buyer:** ✅ 35% target tracked, adjustable  
**FirstPrinciples:** ✅ Core process preserved  
**Researcher:** ✅ SLA tiers added  
**Expansionist:** ✅ Automation roadmap clear  

**Judge Verdict:** 🟢 Proceed with Phase 1 (Simplified)

---

**Next Steps:**
1. Patricia reviews remediation plan
2. Forge provisions Temporal infrastructure
3. Jane runs 10-quote pilot
4. Re-roast after 30-day validation

**Report Generated:** 2026-07-23  
**By:** Miles with Roast Council feedback  
**Status:** Ready for implementation
